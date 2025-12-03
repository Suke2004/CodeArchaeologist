# GitHub MCP Connector

Model Context Protocol server for GitHub integration with CodeArchaeologist.

## Features

- **cloneResurrectionTarget**: Clone GitHub repositories to temporary sandboxes for analysis
- **getCommitHistory**: Analyze commit history to detect project abandonment

## Setup

1. **Install dependencies:**
   ```bash
   cd mcp
   npm install
   ```

2. **Build TypeScript:**
   ```bash
   npm run build
   ```

3. **Configure GitHub token:**
   ```bash
   cp ../.env.example ../.env
   # Edit .env and add your GitHub token
   ```

4. **Configure MCP in Kiro:**
   
   Add to `.kiro/settings/mcp.json`:
   ```json
   {
     "mcpServers": {
       "github-connector": {
         "command": "node",
         "args": ["mcp/github_connector.js"],
         "env": {
           "GITHUB_TOKEN": "${GITHUB_TOKEN}"
         },
         "disabled": false
       }
     }
   }
   ```

## Usage

### Clone a Repository

```typescript
// Call from Kiro AI agent
const result = await cloneResurrectionTarget({
  url: "https://github.com/user/abandoned-repo"
});

// Returns:
{
  "success": true,
  "sandboxPath": "/tmp/code-archaeologist/repo-1234567890-abandoned-repo",
  "repoName": "abandoned-repo"
}
```

### Analyze Commit History

```typescript
const result = await getCommitHistory({
  repoPath: "/tmp/code-archaeologist/repo-1234567890-abandoned-repo",
  abandonmentThresholdDays: 365
});

// Returns:
{
  "success": true,
  "lastCommitDate": "2020-03-15T10:30:00.000Z",
  "daysSinceLastCommit": 1724,
  "totalCommits": 342,
  "isAbandoned": true,
  "abandonmentThresholdDays": 365,
  "topContributors": [
    { "name": "John Doe", "email": "john@example.com", "commits": 156 },
    { "name": "Jane Smith", "email": "jane@example.com", "commits": 89 }
  ]
}
```

## GitHub Token

Generate a personal access token at: https://github.com/settings/tokens

**Required scopes:**
- `repo` (for private repositories)
- `public_repo` (for public repositories only)

## Troubleshooting

**Token not found:**
- Ensure `.env` file exists in project root
- Verify `GITHUB_TOKEN` is set in `.env`
- Check MCP configuration includes the env variable

**Clone fails:**
- Verify repository URL is correct
- Check token has appropriate permissions
- Ensure network connectivity to GitHub

**Commit history fails:**
- Verify repository path exists
- Ensure path points to a valid git repository
- Check repository has commits
