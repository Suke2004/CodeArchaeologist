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
export {};
//# sourceMappingURL=github_connector.d.ts.map