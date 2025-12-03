/**
 * GitHub MCP Server - Model Context Protocol connector for repository resurrection
 *
 * This MCP server provides GitHub integration for CodeArchaeologist, enabling:
 * - Repository cloning to temporary sandboxes
 * - Commit history analysis to determine project abandonment
 * - Authentication via GitHub personal access tokens
 *
 * SETUP:
 * 1. Install dependencies: npm install @modelcontextprotocol/sdk simple-git dotenv
 * 2. Create .env file with: GITHUB_TOKEN=your_github_token_here
 * 3. Configure in .kiro/settings/mcp.json:
 *    {
 *      "mcpServers": {
 *        "github-connector": {
 *          "command": "node",
 *          "args": ["mcp/github_connector.js"],
 *          "env": {
 *            "GITHUB_TOKEN": "${GITHUB_TOKEN}"
 *          }
 *        }
 *      }
 *    }
 *
 * USAGE:
 * - cloneResurrectionTarget(url: string): Clone a GitHub repo to temp sandbox
 * - getCommitHistory(repoPath: string): Analyze commit history and detect abandonment
 */
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema, } from '@modelcontextprotocol/sdk/types.js';
import simpleGit from 'simple-git';
import { promises as fs } from 'fs';
import { tmpdir } from 'os';
import { join } from 'path';
import * as dotenv from 'dotenv';
// Load environment variables
dotenv.config();
class GitHubMCPServer {
    server;
    githubToken;
    constructor() {
        this.githubToken = process.env.GITHUB_TOKEN || '';
        if (!this.githubToken) {
            console.error('WARNING: GITHUB_TOKEN not found in environment variables');
        }
        this.server = new Server({
            name: 'github-connector',
            version: '1.0.0',
        }, {
            capabilities: {
                tools: {},
            },
        });
        this.setupHandlers();
    }
    setupHandlers() {
        // List available tools
        this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
            tools: [
                {
                    name: 'cloneResurrectionTarget',
                    description: 'Clone a GitHub repository to a temporary sandbox directory for analysis',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            url: {
                                type: 'string',
                                description: 'GitHub repository URL (HTTPS or SSH format)',
                            },
                        },
                        required: ['url'],
                    },
                },
                {
                    name: 'getCommitHistory',
                    description: 'Analyze commit history to determine when the project was abandoned',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            repoPath: {
                                type: 'string',
                                description: 'Local path to the cloned repository',
                            },
                            abandonmentThresholdDays: {
                                type: 'number',
                                description: 'Number of days without commits to consider abandoned (default: 365)',
                                default: 365,
                            },
                        },
                        required: ['repoPath'],
                    },
                },
            ],
        }));
        // Handle tool calls
        this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
            const { name, arguments: args } = request.params;
            try {
                if (name === 'cloneResurrectionTarget') {
                    const result = await this.cloneResurrectionTarget(args.url);
                    return {
                        content: [
                            {
                                type: 'text',
                                text: JSON.stringify(result, null, 2),
                            },
                        ],
                    };
                }
                if (name === 'getCommitHistory') {
                    const result = await this.getCommitHistory(args.repoPath, args.abandonmentThresholdDays || 365);
                    return {
                        content: [
                            {
                                type: 'text',
                                text: JSON.stringify(result, null, 2),
                            },
                        ],
                    };
                }
                throw new Error(`Unknown tool: ${name}`);
            }
            catch (error) {
                return {
                    content: [
                        {
                            type: 'text',
                            text: JSON.stringify({
                                success: false,
                                error: error instanceof Error ? error.message : String(error),
                            }),
                        },
                    ],
                    isError: true,
                };
            }
        });
    }
    /**
     * Clone a GitHub repository to a temporary sandbox directory
     */
    async cloneResurrectionTarget(url) {
        try {
            // Validate URL
            if (!url || typeof url !== 'string') {
                throw new Error('Invalid repository URL provided');
            }
            // Extract repo name from URL
            const repoName = this.extractRepoName(url);
            // Create temporary sandbox directory
            const sandboxPath = join(tmpdir(), 'code-archaeologist', `repo-${Date.now()}-${repoName}`);
            await fs.mkdir(sandboxPath, { recursive: true });
            // Prepare authenticated URL if token is available
            const cloneUrl = this.prepareAuthenticatedUrl(url);
            // Clone repository
            const git = simpleGit();
            await git.clone(cloneUrl, sandboxPath, ['--depth', '1000']); // Limit depth for performance
            console.log(`Successfully cloned ${repoName} to ${sandboxPath}`);
            return {
                success: true,
                sandboxPath,
                repoName,
            };
        }
        catch (error) {
            console.error('Clone error:', error);
            return {
                success: false,
                sandboxPath: '',
                repoName: '',
                error: error instanceof Error ? error.message : String(error),
            };
        }
    }
    /**
     * Analyze commit history to determine project abandonment
     */
    async getCommitHistory(repoPath, abandonmentThresholdDays = 365) {
        try {
            // Validate repo path
            const stats = await fs.stat(repoPath);
            if (!stats.isDirectory()) {
                throw new Error('Provided path is not a directory');
            }
            const git = simpleGit(repoPath);
            // Get commit log
            const log = await git.log();
            if (!log.all || log.all.length === 0) {
                throw new Error('No commits found in repository');
            }
            // Get last commit date
            const lastCommit = log.latest;
            if (!lastCommit) {
                throw new Error('Could not retrieve latest commit');
            }
            const lastCommitDate = new Date(lastCommit.date);
            const now = new Date();
            const daysSinceLastCommit = Math.floor((now.getTime() - lastCommitDate.getTime()) / (1000 * 60 * 60 * 24));
            // Determine if abandoned
            const isAbandoned = daysSinceLastCommit > abandonmentThresholdDays;
            // Calculate top contributors
            const contributorMap = new Map();
            for (const commit of log.all) {
                const key = `${commit.author_name}|${commit.author_email}`;
                const existing = contributorMap.get(key);
                if (existing) {
                    existing.commits++;
                }
                else {
                    contributorMap.set(key, {
                        name: commit.author_name,
                        email: commit.author_email,
                        commits: 1,
                    });
                }
            }
            const topContributors = Array.from(contributorMap.values())
                .sort((a, b) => b.commits - a.commits)
                .slice(0, 5);
            console.log(`Analyzed ${log.total} commits. Last commit: ${lastCommitDate.toISOString()}`);
            return {
                success: true,
                lastCommitDate: lastCommitDate.toISOString(),
                daysSinceLastCommit,
                totalCommits: log.total,
                isAbandoned,
                abandonmentThresholdDays,
                topContributors,
            };
        }
        catch (error) {
            console.error('Commit history analysis error:', error);
            return {
                success: false,
                lastCommitDate: '',
                daysSinceLastCommit: 0,
                totalCommits: 0,
                isAbandoned: false,
                abandonmentThresholdDays,
                topContributors: [],
                error: error instanceof Error ? error.message : String(error),
            };
        }
    }
    /**
     * Extract repository name from GitHub URL
     */
    extractRepoName(url) {
        // Handle HTTPS URLs: https://github.com/user/repo.git
        // Handle SSH URLs: git@github.com:user/repo.git
        const httpsMatch = url.match(/github\.com\/([^\/]+)\/([^\/\.]+)/);
        const sshMatch = url.match(/github\.com:([^\/]+)\/([^\/\.]+)/);
        const match = httpsMatch || sshMatch;
        if (match) {
            return match[2].replace('.git', '');
        }
        // Fallback: use last part of URL
        return url.split('/').pop()?.replace('.git', '') || 'unknown-repo';
    }
    /**
     * Prepare authenticated GitHub URL using token
     */
    prepareAuthenticatedUrl(url) {
        if (!this.githubToken) {
            return url;
        }
        // Convert SSH to HTTPS if needed
        if (url.startsWith('git@github.com:')) {
            url = url.replace('git@github.com:', 'https://github.com/');
        }
        // Add token to HTTPS URL
        if (url.startsWith('https://github.com/')) {
            return url.replace('https://github.com/', `https://${this.githubToken}@github.com/`);
        }
        return url;
    }
    async run() {
        const transport = new StdioServerTransport();
        await this.server.connect(transport);
        console.error('GitHub MCP Server running on stdio');
    }
}
// Start the server
const server = new GitHubMCPServer();
server.run().catch(console.error);
//# sourceMappingURL=github_connector.js.map