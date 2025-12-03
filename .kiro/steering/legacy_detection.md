# Legacy Detection Rules

This document defines strict rules for identifying deprecated packages, outdated patterns, and legacy code that requires modernization.

## Severity Levels

- **CRITICAL**: Security vulnerabilities or completely unsupported packages
- **HIGH**: Major version behind, breaking changes available, or deprecated APIs
- **MEDIUM**: Minor versions behind, better alternatives exist
- **LOW**: Cosmetic improvements, style updates

## Python Package Detection Rules

### Django
- If `requirements.txt` or `pyproject.toml` contains `Django<2.0`, flag as **CRITICAL** (unsupported, security risks)
- If `Django>=2.0,<3.0`, flag as **HIGH** (Django 2.x EOL, upgrade to 4.x+)
- If `Django>=3.0,<4.0`, flag as **MEDIUM** (upgrade to Django 4.x or 5.x)
- If using `django.conf.urls.url()`, flag as **HIGH** (deprecated, use `path()` or `re_path()`)

### Flask
- If `Flask<1.0`, flag as **HIGH** (major API changes in 1.0+)
- If `Flask>=1.0,<2.0`, flag as **MEDIUM** (upgrade to Flask 2.x or 3.x)
- If using `flask.ext.*` imports, flag as **HIGH** (deprecated extension import style)

### Python Version
- If `.python-version` or `runtime.txt` contains `2.7` or `3.0-3.6`, flag as **CRITICAL** (EOL versions)
- If `3.7` or `3.8`, flag as **HIGH** (approaching EOL, upgrade to 3.11+)
- If `3.9` or `3.10`, flag as **MEDIUM** (upgrade to 3.11+ for performance)

### Common Python Packages
- If `requests<2.20`, flag as **CRITICAL** (security vulnerabilities)
- If `urllib3<1.24`, flag as **CRITICAL** (security vulnerabilities)
- If `Pillow<8.0`, flag as **HIGH** (security issues)
- If `numpy<1.20`, flag as **MEDIUM** (performance improvements in newer versions)
- If `pandas<1.0`, flag as **HIGH** (major API improvements)
- If `pytest<6.0`, flag as **MEDIUM** (better fixtures and async support)
- If `celery<5.0`, flag as **MEDIUM** (Python 3.7+ required for 5.x)

## JavaScript/TypeScript Package Detection Rules

### React
- If `package.json` contains `"react": "^15.x"` or `"react": "^16.x"`, flag as **HIGH** (upgrade to React 18+)
- If using `React.createClass`, flag as **HIGH** (deprecated, use functional components or ES6 classes)
- If using class components without hooks, flag as **MEDIUM** (modernize to functional components with hooks)
- If `componentWillMount`, `componentWillReceiveProps`, or `componentWillUpdate` are used, flag as **HIGH** (unsafe lifecycle methods)
- If `PropTypes` imported from `react`, flag as **MEDIUM** (move to `prop-types` package or TypeScript)

### Node.js
- If `.nvmrc` or `package.json` engines contains `<12.x`, flag as **CRITICAL** (EOL versions)
- If `12.x` or `14.x`, flag as **HIGH** (EOL, upgrade to 18.x LTS or 20.x LTS)
- If `16.x`, flag as **MEDIUM** (upgrade to 18.x LTS or 20.x LTS)

### Build Tools
- If using `webpack<5.0`, flag as **HIGH** (major performance improvements in v5)
- If using `babel<7.0`, flag as **HIGH** (upgrade to Babel 7+)
- If using `gulp` or `grunt`, flag as **MEDIUM** (consider modern alternatives like Vite or esbuild)
- If using `create-react-app` without ejecting, flag as **LOW** (consider Vite or Next.js for better DX)

### Common JavaScript Packages
- If `axios<0.21`, flag as **CRITICAL** (security vulnerabilities)
- If `lodash<4.17.20`, flag as **CRITICAL** (prototype pollution vulnerabilities)
- If `moment.js` is used, flag as **MEDIUM** (deprecated, use `date-fns` or `dayjs`)
- If `request` package is used, flag as **HIGH** (fully deprecated, use `axios` or `node-fetch`)
- If `express<4.17`, flag as **HIGH** (security updates)

### TypeScript
- If `typescript<4.0`, flag as **HIGH** (major improvements in 4.x+)
- If `typescript>=4.0,<5.0`, flag as **MEDIUM** (upgrade to TypeScript 5.x)
- If using `namespace` keyword, flag as **MEDIUM** (use ES6 modules instead)
- If using `/// <reference>` tags, flag as **MEDIUM** (use ES6 imports)

## Code Pattern Detection Rules

### Python Patterns
- If `print` statements without parentheses (Python 2 style), flag as **HIGH**
- If `except Exception, e:` syntax, flag as **HIGH** (Python 2 syntax)
- If `file()` builtin used, flag as **HIGH** (removed in Python 3, use `open()`)
- If `xrange()` used, flag as **HIGH** (use `range()` in Python 3)
- If `dict.iteritems()`, `dict.iterkeys()`, or `dict.itervalues()` used, flag as **HIGH** (use `.items()`, `.keys()`, `.values()`)
- If `__future__` imports present, flag as **MEDIUM** (may indicate Python 2 compatibility code)
- If `unicode()` builtin used, flag as **HIGH** (use `str()` in Python 3)

### JavaScript/React Patterns
- If `var` keyword used, flag as **MEDIUM** (use `const` or `let`)
- If `React.createClass` used, flag as **HIGH** (use functional components or ES6 classes)
- If `componentWillMount`, `componentWillReceiveProps`, `componentWillUpdate` used, flag as **HIGH** (unsafe lifecycle methods)
- If `findDOMNode()` used, flag as **HIGH** (deprecated, use refs)
- If `String.prototype.substr()` used, flag as **MEDIUM** (deprecated, use `substring()` or `slice()`)
- If callback-based async code without Promises, flag as **MEDIUM** (modernize to async/await)
- If `require()` used in ES6+ codebase, flag as **MEDIUM** (use ES6 `import`)

### Configuration Files
- If `.babelrc` without `.js` extension, flag as **LOW** (use `babel.config.js` for better flexibility)
- If `webpack.config.js` uses CommonJS, flag as **LOW** (consider ES6 modules)
- If `.eslintrc` without extension, flag as **LOW** (use `.eslintrc.js` or `.eslintrc.json`)

## Dependency Management

### Python
- If using `requirements.txt` without version pinning, flag as **MEDIUM** (pin versions for reproducibility)
- If no `requirements.txt` or `pyproject.toml` found, flag as **HIGH** (add dependency management)
- If using `setup.py` without `pyproject.toml`, flag as **MEDIUM** (modernize to PEP 517/518)

### JavaScript
- If `package-lock.json` or `yarn.lock` missing, flag as **MEDIUM** (add lockfile for reproducibility)
- If using `npm` with Node 16+, flag as **LOW** (consider `pnpm` or `yarn` for performance)
- If `node_modules` committed to git, flag as **HIGH** (remove and use lockfiles)

## Security Vulnerabilities

### Always Flag as CRITICAL
- Any package with known CVEs (check npm audit, pip-audit, or safety)
- Hardcoded credentials or API keys in code
- SQL injection vulnerabilities (raw SQL without parameterization)
- XSS vulnerabilities (unescaped user input in templates)
- CSRF protection disabled
- Debug mode enabled in production configurations

### Always Flag as HIGH
- Missing HTTPS/TLS configuration
- Weak password hashing (MD5, SHA1 without salt)
- Missing input validation
- Insecure deserialization (pickle, eval)
- Missing authentication on sensitive endpoints

## Testing Frameworks

### Python
- If using `unittest` exclusively, flag as **LOW** (consider `pytest` for better DX)
- If using `nose`, flag as **HIGH** (unmaintained, migrate to `pytest`)
- If no test files found, flag as **MEDIUM** (add test coverage)

### JavaScript
- If using `jasmine` or `mocha` without modern alternatives, flag as **MEDIUM** (consider Jest or Vitest)
- If using `karma`, flag as **MEDIUM** (consider modern test runners)
- If no test files found, flag as **MEDIUM** (add test coverage)

## Detection Priority

When analyzing a repository, detect issues in this order:

1. **Security vulnerabilities** (CRITICAL)
2. **EOL/unsupported versions** (CRITICAL)
3. **Deprecated APIs and patterns** (HIGH)
4. **Outdated major versions** (HIGH)
5. **Outdated minor versions** (MEDIUM)
6. **Code style and patterns** (MEDIUM/LOW)
7. **Missing best practices** (LOW)

## Output Format

When flagging issues, always include:
- **Severity level**
- **Package/pattern name and current version**
- **Recommended version/alternative**
- **Reason for upgrade** (security, performance, maintainability)
- **Breaking changes to be aware of**
- **Migration effort estimate** (low, medium, high)

Example:
```
[CRITICAL] Django 1.11.29
→ Upgrade to: Django 4.2 LTS
→ Reason: Django 1.11 reached EOL in April 2020, contains unpatched security vulnerabilities
→ Breaking Changes: URL routing, middleware, template context processors
→ Migration Effort: HIGH (requires code changes across views, URLs, and middleware)
```
