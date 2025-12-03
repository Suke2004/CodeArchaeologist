# Modernization Standards - Source of Truth

This document defines the authoritative standards for modern code. All refactoring operations MUST follow these rules to ensure consistency and quality.

## Core Principles

1. **Readability over cleverness** - Code should be self-documenting
2. **Type safety** - Use type hints (Python) or TypeScript where possible
3. **Immutability** - Prefer immutable data structures and pure functions
4. **Async-first** - Use async/await for I/O operations
5. **Testing** - All new code must be testable
6. **Security** - Follow OWASP guidelines and principle of least privilege

## Python Modernization Standards

### Python Version Target
- **Target Version**: Python 3.11+ (or latest stable)
- Use modern syntax features: walrus operator, f-strings, type hints, dataclasses

### Print Statements
```python
# ❌ LEGACY
print "Hello, World!"
print variable

# ✅ MODERN
print("Hello, World!")
print(variable)
```

### String Formatting
```python
# ❌ LEGACY
"Hello, %s" % name
"Hello, {}".format(name)

# ✅ MODERN
f"Hello, {name}"
f"Result: {calculation()}"
```

### Type Hints
```python
# ❌ LEGACY
def process_data(data, count):
    return data * count

# ✅ MODERN
def process_data(data: list[str], count: int) -> list[str]:
    return data * count

# ✅ MODERN (with complex types)
from typing import Optional, Union
from collections.abc import Callable

def fetch_user(user_id: int) -> Optional[dict[str, str]]:
    ...

def apply_transform(data: list[int], func: Callable[[int], int]) -> list[int]:
    return [func(x) for x in data]
```

### Exception Handling
```python
# ❌ LEGACY
try:
    risky_operation()
except Exception, e:
    print e

# ✅ MODERN
try:
    risky_operation()
except ValueError as e:
    logger.error(f"Operation failed: {e}")
    raise
except Exception as e:
    logger.exception("Unexpected error occurred")
    raise
```

### Dictionary Operations
```python
# ❌ LEGACY
for key in dict.iterkeys():
    ...
for key, value in dict.iteritems():
    ...

# ✅ MODERN
for key in dict.keys():
    ...
for key, value in dict.items():
    ...
```

### File Operations
```python
# ❌ LEGACY
f = open('file.txt')
data = f.read()
f.close()

# ✅ MODERN
with open('file.txt', encoding='utf-8') as f:
    data = f.read()

# ✅ MODERN (pathlib)
from pathlib import Path

data = Path('file.txt').read_text(encoding='utf-8')
```

### Dataclasses over Manual Classes
```python
# ❌ LEGACY
class User:
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age
    
    def __repr__(self):
        return f"User({self.name}, {self.email}, {self.age})"

# ✅ MODERN
from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str
    age: int
```

### Async/Await
```python
# ❌ LEGACY (callback-based)
def fetch_data(callback):
    result = slow_operation()
    callback(result)

# ✅ MODERN
async def fetch_data() -> dict:
    result = await slow_operation()
    return result

# Usage
data = await fetch_data()
```

### List Comprehensions
```python
# ❌ LEGACY
result = []
for item in items:
    if item > 0:
        result.append(item * 2)

# ✅ MODERN
result = [item * 2 for item in items if item > 0]

# ✅ MODERN (generator for large datasets)
result = (item * 2 for item in items if item > 0)
```

### Pathlib over os.path
```python
# ❌ LEGACY
import os
path = os.path.join(base_dir, 'subdir', 'file.txt')
if os.path.exists(path):
    with open(path) as f:
        ...

# ✅ MODERN
from pathlib import Path

path = Path(base_dir) / 'subdir' / 'file.txt'
if path.exists():
    content = path.read_text()
```

## JavaScript/TypeScript Modernization Standards

### Variable Declarations
```javascript
// ❌ LEGACY
var count = 0;
var name = "John";

// ✅ MODERN
const count = 0;
let name = "John";
```

### Arrow Functions
```javascript
// ❌ LEGACY
function add(a, b) {
    return a + b;
}

const numbers = [1, 2, 3].map(function(n) {
    return n * 2;
});

// ✅ MODERN
const add = (a, b) => a + b;

const numbers = [1, 2, 3].map(n => n * 2);
```

### Template Literals
```javascript
// ❌ LEGACY
const message = "Hello, " + name + "!";
const multiline = "Line 1\n" +
                  "Line 2\n" +
                  "Line 3";

// ✅ MODERN
const message = `Hello, ${name}!`;
const multiline = `
    Line 1
    Line 2
    Line 3
`;
```

### Destructuring
```javascript
// ❌ LEGACY
const name = user.name;
const email = user.email;
const first = array[0];
const second = array[1];

// ✅ MODERN
const { name, email } = user;
const [first, second] = array;

// ✅ MODERN (with defaults)
const { name = "Anonymous", email } = user;
```

### Async/Await over Promises
```javascript
// ❌ LEGACY
function fetchData() {
    return fetch('/api/data')
        .then(response => response.json())
        .then(data => processData(data))
        .catch(error => console.error(error));
}

// ✅ MODERN
async function fetchData() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        return processData(data);
    } catch (error) {
        console.error(error);
        throw error;
    }
}
```

### Optional Chaining and Nullish Coalescing
```javascript
// ❌ LEGACY
const street = user && user.address && user.address.street;
const count = value !== null && value !== undefined ? value : 0;

// ✅ MODERN
const street = user?.address?.street;
const count = value ?? 0;
```

### Modules
```javascript
// ❌ LEGACY
const module = require('./module');
module.exports = MyClass;

// ✅ MODERN
import { specificFunction } from './module';
export class MyClass { }
export default MyClass;
```

## React Modernization Standards

### Functional Components over Class Components
```javascript
// ❌ LEGACY
class UserProfile extends React.Component {
    constructor(props) {
        super(props);
        this.state = { count: 0 };
    }
    
    componentDidMount() {
        this.fetchData();
    }
    
    fetchData() {
        // fetch logic
    }
    
    render() {
        return <div>{this.state.count}</div>;
    }
}

// ✅ MODERN
import { useState, useEffect } from 'react';

function UserProfile({ userId }) {
    const [count, setCount] = useState(0);
    
    useEffect(() => {
        fetchData();
    }, []);
    
    const fetchData = async () => {
        // fetch logic
    };
    
    return <div>{count}</div>;
}
```

### Hooks over Lifecycle Methods
```javascript
// ❌ LEGACY
componentDidMount() {
    this.fetchData();
}

componentWillUnmount() {
    this.cleanup();
}

// ✅ MODERN
useEffect(() => {
    fetchData();
    
    return () => {
        cleanup();
    };
}, []);
```

### Custom Hooks for Reusable Logic
```javascript
// ❌ LEGACY (HOC or render props)
class DataFetcher extends React.Component {
    // complex logic
}

// ✅ MODERN
function useDataFetch(url) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(url);
                const result = await response.json();
                setData(result);
            } catch (err) {
                setError(err);
            } finally {
                setLoading(false);
            }
        };
        
        fetchData();
    }, [url]);
    
    return { data, loading, error };
}

// Usage
function MyComponent() {
    const { data, loading, error } = useDataFetch('/api/users');
    
    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;
    return <div>{JSON.stringify(data)}</div>;
}
```

### PropTypes to TypeScript
```javascript
// ❌ LEGACY
import PropTypes from 'prop-types';

function Button({ label, onClick, disabled }) {
    return <button onClick={onClick} disabled={disabled}>{label}</button>;
}

Button.propTypes = {
    label: PropTypes.string.isRequired,
    onClick: PropTypes.func.isRequired,
    disabled: PropTypes.bool
};

// ✅ MODERN (TypeScript)
interface ButtonProps {
    label: string;
    onClick: () => void;
    disabled?: boolean;
}

function Button({ label, onClick, disabled = false }: ButtonProps) {
    return <button onClick={onClick} disabled={disabled}>{label}</button>;
}
```

### Context API over Prop Drilling
```javascript
// ❌ LEGACY (prop drilling)
function App() {
    const [user, setUser] = useState(null);
    return <Parent user={user} setUser={setUser} />;
}

function Parent({ user, setUser }) {
    return <Child user={user} setUser={setUser} />;
}

function Child({ user, setUser }) {
    return <div>{user?.name}</div>;
}

// ✅ MODERN (Context)
const UserContext = createContext(null);

function App() {
    const [user, setUser] = useState(null);
    
    return (
        <UserContext.Provider value={{ user, setUser }}>
            <Parent />
        </UserContext.Provider>
    );
}

function Child() {
    const { user } = useContext(UserContext);
    return <div>{user?.name}</div>;
}
```

## Django Modernization Standards

### URL Patterns
```python
# ❌ LEGACY
from django.conf.urls import url

urlpatterns = [
    url(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
]

# ✅ MODERN
from django.urls import path, re_path

urlpatterns = [
    path('articles/<int:year>/', views.year_archive),
    # Use re_path only when regex is necessary
    re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
]
```

### Class-Based Views
```python
# ❌ LEGACY (function-based views for complex logic)
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'articles/list.html', {'articles': articles})

# ✅ MODERN
from django.views.generic import ListView

class ArticleListView(ListView):
    model = Article
    template_name = 'articles/list.html'
    context_object_name = 'articles'
```

### Settings Configuration
```python
# ❌ LEGACY
DEBUG = True
SECRET_KEY = 'hardcoded-secret-key'

# ✅ MODERN
import os
from pathlib import Path

DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY')

if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable must be set")
```

## Testing Standards

### Python Testing (pytest)
```python
# ❌ LEGACY (unittest)
import unittest

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

# ✅ MODERN (pytest)
import pytest

def test_add():
    assert add(2, 3) == 5

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5]

def test_with_fixture(sample_data):
    assert len(sample_data) == 5
```

### JavaScript Testing (Jest/Vitest)
```javascript
// ❌ LEGACY (no tests or old frameworks)

// ✅ MODERN
import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('Button', () => {
    it('calls onClick when clicked', async () => {
        const handleClick = vi.fn();
        render(<Button onClick={handleClick}>Click me</Button>);
        
        await userEvent.click(screen.getByText('Click me'));
        
        expect(handleClick).toHaveBeenCalledTimes(1);
    });
});
```

## Documentation Standards

### Python Docstrings
```python
# ❌ LEGACY
def calculate(x, y):
    # This function calculates something
    return x + y

# ✅ MODERN
def calculate(x: int, y: int) -> int:
    """
    Calculate the sum of two integers.
    
    Args:
        x: The first integer
        y: The second integer
    
    Returns:
        The sum of x and y
    
    Raises:
        TypeError: If x or y are not integers
    
    Example:
        >>> calculate(2, 3)
        5
    """
    return x + y
```

### JSDoc/TSDoc
```typescript
// ✅ MODERN
/**
 * Fetches user data from the API
 * 
 * @param userId - The unique identifier for the user
 * @returns A promise that resolves to the user object
 * @throws {Error} If the user is not found or network error occurs
 * 
 * @example
 * ```ts
 * const user = await fetchUser(123);
 * console.log(user.name);
 * ```
 */
async function fetchUser(userId: number): Promise<User> {
    // implementation
}
```

## Configuration File Standards

### Package Management
```json
// ✅ MODERN package.json
{
    "name": "my-app",
    "version": "1.0.0",
    "type": "module",
    "engines": {
        "node": ">=18.0.0",
        "npm": ">=9.0.0"
    },
    "scripts": {
        "dev": "vite",
        "build": "vite build",
        "test": "vitest",
        "lint": "eslint . --ext .ts,.tsx",
        "format": "prettier --write ."
    }
}
```

```toml
# ✅ MODERN pyproject.toml
[project]
name = "my-app"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.104.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]

[tool.black]
line-length = 100
target-version = ['py311']

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W"]
```

## Security Standards

### Environment Variables
```python
# ❌ LEGACY
API_KEY = "sk-1234567890abcdef"
DATABASE_URL = "postgresql://user:pass@localhost/db"

# ✅ MODERN
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

if not API_KEY:
    raise ValueError("API_KEY must be set in environment")
```

### Password Hashing
```python
# ❌ LEGACY
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()

# ✅ MODERN
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password_hash = pwd_context.hash(password)
is_valid = pwd_context.verify(plain_password, hashed_password)
```

## Performance Standards

### Database Queries (Django)
```python
# ❌ LEGACY (N+1 queries)
articles = Article.objects.all()
for article in articles:
    print(article.author.name)  # Triggers query for each article

# ✅ MODERN
articles = Article.objects.select_related('author').all()
for article in articles:
    print(article.author.name)  # No additional queries
```

### React Performance
```javascript
// ❌ LEGACY (unnecessary re-renders)
function ExpensiveComponent({ data }) {
    const processed = expensiveOperation(data);
    return <div>{processed}</div>;
}

// ✅ MODERN
import { useMemo } from 'react';

function ExpensiveComponent({ data }) {
    const processed = useMemo(() => expensiveOperation(data), [data]);
    return <div>{processed}</div>;
}
```

## Migration Checklist

When modernizing code, ensure:

- [ ] All Python 2 syntax converted to Python 3.11+
- [ ] All `var` declarations converted to `const`/`let`
- [ ] All class components converted to functional components with hooks
- [ ] Type hints added to Python functions
- [ ] TypeScript used instead of JavaScript where possible
- [ ] Async/await used for all I/O operations
- [ ] Environment variables used for all secrets
- [ ] Modern package versions specified
- [ ] Tests added or updated
- [ ] Documentation updated with examples
- [ ] Security best practices followed
- [ ] Performance optimizations applied
- [ ] Linting and formatting configured
