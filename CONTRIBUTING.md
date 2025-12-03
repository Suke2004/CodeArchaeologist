# Contributing to CodeArchaeologist

Thank you for your interest in contributing to CodeArchaeologist! This document provides guidelines and instructions for contributing.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Making Changes](#making-changes)
5. [Testing](#testing)
6. [Code Style](#code-style)
7. [Commit Guidelines](#commit-guidelines)
8. [Pull Request Process](#pull-request-process)
9. [Adding New Features](#adding-new-features)
10. [Reporting Bugs](#reporting-bugs)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors.

### Expected Behavior

- Be respectful and considerate
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Accept responsibility for mistakes

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Publishing others' private information
- Other unprofessional conduct

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- Git
- Basic knowledge of FastAPI and React/Next.js

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/codearchaeologist.git
   cd codearchaeologist
   ```
3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/codearchaeologist.git
   ```

## Development Setup

### Automated Setup

```bash
# Linux/macOS
./setup.sh

# Windows
setup.bat
```

### Manual Setup

See `README.md` for detailed manual setup instructions.

### Verify Setup

```bash
python setup_verify.py
```

## Making Changes

### Create a Branch

```bash
# Update your fork
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
```

### Branch Naming Convention

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `test/` - Test additions or changes
- `refactor/` - Code refactoring
- `chore/` - Maintenance tasks

Examples:
- `feature/javascript-detection`
- `fix/api-error-handling`
- `docs/update-readme`
- `test/add-detector-tests`

### Make Your Changes

1. Write your code
2. Add tests
3. Update documentation
4. Run tests locally
5. Commit your changes

## Testing

### Run All Tests

```bash
cd backend
pytest
```

### Run Specific Tests

```bash
# Run specific test file
pytest tests/test_legacy_detector.py -v

# Run specific test
pytest tests/test_legacy_detector.py::TestLegacyDetector::test_detect_eval_usage -v

# Run tests matching pattern
pytest -k "security" -v
```

### Run with Coverage

```bash
pytest --cov=. --cov-report=html
```

### Interactive Testing

```bash
python backend/test_detector.py
```

### Test Requirements

- All new features must have tests
- Maintain or improve code coverage
- Tests must pass before submitting PR
- Include both unit and integration tests

## Code Style

### Python (Backend)

**Style Guide:** PEP 8 with modern Python 3.11+ features

**Key Points:**
- Use type hints for all functions
- Use f-strings for formatting
- Use dataclasses or Pydantic models
- Follow async/await patterns
- Add docstrings to all public functions

**Example:**
```python
from typing import Dict, List

def process_data(data: Dict[str, int]) -> List[int]:
    """
    Process data and return transformed values.
    
    Args:
        data: Dictionary mapping strings to integers
    
    Returns:
        List of transformed integer values
    """
    return [value * 2 for key, value in data.items()]
```

**Formatting:**
```bash
# Install formatters
pip install black ruff

# Format code
black .

# Lint code
ruff check .
```

### TypeScript (Frontend)

**Style Guide:** TypeScript with React best practices

**Key Points:**
- Use functional components with hooks
- Use TypeScript interfaces for props
- Use async/await for API calls
- Follow Next.js conventions
- Use Tailwind CSS for styling

**Example:**
```typescript
interface ButtonProps {
    label: string;
    onClick: () => void;
    disabled?: boolean;
}

export function Button({ label, onClick, disabled = false }: ButtonProps) {
    return (
        <button onClick={onClick} disabled={disabled}>
            {label}
        </button>
    );
}
```

**Formatting:**
```bash
# Format code
npm run format

# Lint code
npm run lint
```

### Documentation

- Use clear, concise language
- Include code examples
- Update README.md for user-facing changes
- Add inline comments for complex logic
- Follow documentation style guide in `.kiro/steering/documentation_style.md`

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Test additions or changes
- `chore`: Maintenance tasks

### Examples

```
feat(detector): add JavaScript legacy pattern detection

- Add detection for var declarations
- Add detection for callback-based async
- Add tests for new patterns

Closes #123
```

```
fix(api): handle empty response from AI model

Previously, empty responses would cause unhandled exceptions.
Now returns appropriate error message.

Fixes #456
```

### Commit Best Practices

- Write clear, descriptive messages
- Use present tense ("add feature" not "added feature")
- Keep subject line under 50 characters
- Wrap body at 72 characters
- Reference issues and PRs

## Pull Request Process

### Before Submitting

1. **Update your branch**
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-branch
   git rebase main
   ```

2. **Run tests**
   ```bash
   cd backend
   pytest
   ```

3. **Check code style**
   ```bash
   black .
   ruff check .
   ```

4. **Update documentation**
   - Update README.md if needed
   - Add/update docstrings
   - Update CHANGELOG.md

### Submit Pull Request

1. Push to your fork:
   ```bash
   git push origin your-branch
   ```

2. Create PR on GitHub

3. Fill out PR template:
   - Description of changes
   - Related issues
   - Testing performed
   - Screenshots (if UI changes)

### PR Template

```markdown
## Description
Brief description of changes

## Related Issues
Closes #123

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed
- [ ] All tests passing

## Screenshots (if applicable)
[Add screenshots here]

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Commit messages follow guidelines
```

### Review Process

1. Maintainer reviews PR
2. Address feedback
3. Update PR as needed
4. Maintainer approves and merges

### After Merge

1. Delete your branch:
   ```bash
   git branch -d your-branch
   git push origin --delete your-branch
   ```

2. Update your fork:
   ```bash
   git checkout main
   git pull upstream main
   ```

## Adding New Features

### Detection Rules

To add new legacy pattern detection rules:

1. **Add pattern to `backend/services/legacy_detector.py`:**
   ```python
   NEW_PATTERNS = [
       (r'pattern_regex', Severity.HIGH, "Description", "Suggestion"),
   ]
   ```

2. **Add tests to `backend/tests/test_legacy_detector.py`:**
   ```python
   def test_detect_new_pattern(self, detector):
       code = "code with pattern"
       issues = detector.detect_python_issues(code)
       assert len(issues) > 0
   ```

3. **Update documentation:**
   - Add to `README.md` under "What It Detects"
   - Add to `.kiro/steering/legacy_detection.md`

### Language Support

To add support for a new language:

1. Create new detector class (e.g., `JavaScriptDetector`)
2. Define language-specific patterns
3. Add tests
4. Update API to handle new language
5. Update frontend to support new language
6. Document in README.md

### UI Components

To add new UI components:

1. Create component in `frontend/components/`
2. Use TypeScript with proper interfaces
3. Follow existing component patterns
4. Add to Storybook (if available)
5. Document props and usage

## Reporting Bugs

### Before Reporting

1. Check existing issues
2. Verify it's reproducible
3. Test with latest version
4. Gather relevant information

### Bug Report Template

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Windows 11, macOS 14, Ubuntu 22.04]
- Python version: [e.g., 3.11.5]
- Node.js version: [e.g., 20.10.0]
- Browser: [e.g., Chrome 120]

## Additional Context
- Error messages
- Screenshots
- Logs
```

## Feature Requests

### Feature Request Template

```markdown
## Feature Description
Clear description of the feature

## Use Case
Why is this feature needed?

## Proposed Solution
How should it work?

## Alternatives Considered
Other approaches you've thought about

## Additional Context
- Examples from other tools
- Mockups or diagrams
- Related issues
```

## Development Tips

### Hot Reload

Both backend and frontend support hot reload:

```bash
# Backend (auto-reloads on file changes)
uvicorn main:app --reload

# Frontend (auto-reloads on file changes)
npm run dev
```

### Debugging

**Backend:**
```python
# Add breakpoints
import pdb; pdb.set_trace()

# Or use VS Code debugger
# See .vscode/launch.json
```

**Frontend:**
```typescript
// Use browser DevTools
console.log('Debug info:', data);

// Or use VS Code debugger
```

### Common Issues

**Import Errors:**
```bash
# Make sure you're in the right directory
cd backend
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Port Already in Use:**
```bash
# Backend
uvicorn main:app --reload --port 8001

# Frontend
npm run dev -- --port 3001
```

**Dependencies Out of Sync:**
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

## Resources

### Documentation

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)
- [pytest Docs](https://docs.pytest.org/)
- [TypeScript Docs](https://www.typescriptlang.org/docs/)

### Project Documentation

- `README.md` - Project overview
- `TESTING.md` - Testing guide
- `SECURITY.md` - Security policy
- `.kiro/steering/` - Development standards

### Getting Help

- Open an issue for questions
- Check existing issues and PRs
- Review documentation
- Ask in discussions (if enabled)

## Recognition

Contributors will be recognized in:
- `README.md` acknowledgments section
- Release notes
- GitHub contributors page

Thank you for contributing to CodeArchaeologist! 🏛️⚡

---

**Questions?** Open an issue or reach out to maintainers.
