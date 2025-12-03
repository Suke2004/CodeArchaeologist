/**
 * Test script for GitHub MCP connector
 * Run with: node mcp/test_mcp.js
 */

console.log('Testing GitHub MCP Connector...\n');

// Check if compiled JS exists
const fs = require('fs');
const path = require('path');

const jsFile = path.join(__dirname, 'github_connector.js');
const tsFile = path.join(__dirname, 'github_connector.ts');

if (fs.existsSync(jsFile)) {
    console.log('✅ Compiled JavaScript file exists');
} else {
    console.log('❌ Compiled JavaScript file not found');
    console.log('   Run: npm run build (in mcp directory)');
}

if (fs.existsSync(tsFile)) {
    console.log('✅ TypeScript source file exists');
} else {
    console.log('❌ TypeScript source file not found');
}

// Check dependencies
const packageJsonPath = path.join(__dirname, 'package.json');
if (fs.existsSync(packageJsonPath)) {
    console.log('✅ package.json exists');
    const pkg = require(packageJsonPath);
    console.log('\nDependencies:');
    Object.keys(pkg.dependencies || {}).forEach(dep => {
        console.log(`  - ${dep}: ${pkg.dependencies[dep]}`);
    });
} else {
    console.log('❌ package.json not found');
}

// Check node_modules
const nodeModulesPath = path.join(__dirname, 'node_modules');
if (fs.existsSync(nodeModulesPath)) {
    console.log('\n✅ node_modules directory exists');
} else {
    console.log('\n❌ node_modules not found');
    console.log('   Run: npm install (in mcp directory)');
}

console.log('\n--- Setup Instructions ---');
console.log('1. cd mcp');
console.log('2. npm install');
console.log('3. npm run build');
console.log('4. Configure .env with GITHUB_TOKEN');
console.log('5. Test with: node github_connector.js');
