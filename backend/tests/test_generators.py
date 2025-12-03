"""
Hypothesis generators for property-based testing.
Generates random valid data for testing.
"""

from hypothesis import strategies as st
from hypothesis.strategies import composite
import string


# URL Generators
@composite
def generate_git_url(draw):
    """Generate valid Git repository URLs in https, git, or ssh formats."""
    user = draw(st.text(
        alphabet=string.ascii_lowercase + string.digits + '-',
        min_size=3,
        max_size=20
    ).filter(lambda x: not x.startswith('-') and not x.endswith('-')))
    
    repo = draw(st.text(
        alphabet=string.ascii_lowercase + string.digits + '-_.',
        min_size=3,
        max_size=30
    ).filter(lambda x: not x.startswith('-') and not x.endswith('-')))
    
    # Choose between different Git URL formats
    format_choice = draw(st.sampled_from(['https', 'git', 'ssh']))
    
    if format_choice == 'https':
        # https://github.com/user/repo.git or https://gitlab.com/user/repo.git
        host = draw(st.sampled_from(['github.com', 'gitlab.com', 'bitbucket.org']))
        return f"https://{host}/{user}/{repo}.git"
    elif format_choice == 'git':
        # git://github.com/user/repo.git
        host = draw(st.sampled_from(['github.com', 'gitlab.com']))
        return f"git://{host}/{user}/{repo}.git"
    else:  # ssh
        # git@github.com:user/repo.git
        host = draw(st.sampled_from(['github.com', 'gitlab.com', 'bitbucket.org']))
        return f"git@{host}:{user}/{repo}.git"


@composite
def generate_invalid_url(draw):
    """Generate invalid repository URLs for testing rejection."""
    invalid_patterns = [
        st.just("not-a-url"),
        st.just("http://"),
        st.just("github.com/user"),
        st.just("https://github.com/"),
        st.just("https://github.com/user/"),
        st.just("ftp://invalid.com/repo"),
        st.just(""),
        st.just("   "),
        st.just("https://"),
        st.just("git@"),
        st.just("git@github.com"),
        st.just("git@github.com:"),
        st.text(alphabet=string.ascii_letters + ' !@#$%', min_size=1, max_size=10),
        st.builds(lambda x: f"https://github.com/{x}", 
                 st.text(alphabet=string.whitespace, min_size=1, max_size=5)),
    ]
    return draw(st.one_of(*invalid_patterns))


# Code Generators
@composite
def generate_python_code(draw):
    """Generate syntactically valid Python code that can be parsed by ast.parse()."""
    # Python keywords to avoid
    keywords = {'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
               'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
               'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
               'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
               'try', 'while', 'with', 'yield'}
    
    # Generate different types of valid Python constructs
    code_type = draw(st.sampled_from([
        'function_def',
        'import',
        'assignment',
        'class_def',
        'for_loop',
        'if_statement',
    ]))
    
    if code_type == 'function_def':
        func_name = draw(st.text(
            alphabet=string.ascii_lowercase + '_',
            min_size=3,
            max_size=15
        ).filter(lambda x: x[0] != '_' and not x[0].isdigit() and x not in keywords))
        
        param = draw(st.text(
            alphabet=string.ascii_lowercase + '_',
            min_size=1,
            max_size=10
        ).filter(lambda x: x[0] != '_' and not x[0].isdigit() and x not in keywords))
        
        return f"def {func_name}({param}):\n    return {param}"
    
    elif code_type == 'import':
        module = draw(st.sampled_from(['os', 'sys', 'json', 'math', 're', 'datetime']))
        return f"import {module}"
    
    elif code_type == 'assignment':
        var_name = draw(st.text(
            alphabet=string.ascii_lowercase + '_',
            min_size=3,
            max_size=15
        ).filter(lambda x: x[0] != '_' and not x[0].isdigit() and x not in keywords))
        
        value_type = draw(st.sampled_from(['int', 'str', 'list', 'dict']))
        
        if value_type == 'int':
            value = draw(st.integers(0, 1000))
            return f"{var_name} = {value}"
        elif value_type == 'str':
            return f'{var_name} = "hello"'
        elif value_type == 'list':
            return f"{var_name} = [1, 2, 3]"
        else:  # dict
            return f"{var_name} = {{'key': 'value'}}"
    
    elif code_type == 'class_def':
        class_name = draw(st.text(
            alphabet=string.ascii_uppercase + string.ascii_lowercase,
            min_size=3,
            max_size=15
        ).filter(lambda x: x[0].isupper() and x not in keywords))
        
        return f"class {class_name}:\n    pass"
    
    elif code_type == 'for_loop':
        var = draw(st.text(
            alphabet=string.ascii_lowercase,
            min_size=1,
            max_size=5
        ).filter(lambda x: not x[0].isdigit() and x not in keywords))
        
        return f"for {var} in range(10):\n    pass"
    
    else:  # if_statement
        var = draw(st.text(
            alphabet=string.ascii_lowercase + '_',
            min_size=3,
            max_size=10
        ).filter(lambda x: x[0] != '_' and not x[0].isdigit() and x not in keywords))
        
        return f"if {var}:\n    pass"


@composite
def python2_code(draw):
    """Generate Python 2 code snippets."""
    patterns = [
        'print "Hello, World!"',
        'for k, v in data.iteritems():\n    pass',
        'result = eval(user_input)',
        'for i in xrange(10):\n    pass',
        'text = unicode(data)',
    ]
    return draw(st.sampled_from(patterns))


@composite
def python3_code(draw):
    """Generate Python 3 code snippets."""
    patterns = [
        'print("Hello, World!")',
        'for k, v in data.items():\n    pass',
        'result = ast.literal_eval(user_input)',
        'for i in range(10):\n    pass',
        'text = str(data)',
    ]
    return draw(st.sampled_from(patterns))


# Dependency Generators
@composite
def generate_dependency_spec(draw, format_type='pip'):
    """
    Generate dependency specifications in various formats.
    
    Args:
        format_type: One of 'pip', 'npm', or 'poetry'
    
    Returns:
        String representation of a dependency specification
    """
    package = draw(st.text(
        alphabet=string.ascii_lowercase + '-_',
        min_size=3,
        max_size=20
    ).filter(lambda x: x[0] not in '-_' and x[-1] not in '-_'))
    
    major = draw(st.integers(0, 10))
    minor = draw(st.integers(0, 20))
    patch = draw(st.integers(0, 50))
    
    if format_type == 'pip':
        # pip format: package==1.0.0, package>=1.0.0, package~=1.0.0
        operator = draw(st.sampled_from(['==', '>=', '~=', '<=', '>']))
        return f"{package}{operator}{major}.{minor}.{patch}"
    
    elif format_type == 'npm':
        # npm format: "package": "^1.0.0", "package": "~1.0.0", "package": "1.0.0"
        prefix = draw(st.sampled_from(['^', '~', '']))
        return f'"{package}": "{prefix}{major}.{minor}.{patch}"'
    
    elif format_type == 'poetry':
        # poetry format: package = "^1.0.0", package = "~1.0.0"
        prefix = draw(st.sampled_from(['^', '~', '']))
        return f'{package} = "{prefix}{major}.{minor}.{patch}"'
    
    else:
        raise ValueError(f"Unknown format type: {format_type}")


@composite
def pip_requirements(draw):
    """Generate valid pip requirement strings."""
    return draw(generate_dependency_spec(format_type='pip'))


@composite
def npm_dependency(draw):
    """Generate valid npm dependency entry."""
    return draw(generate_dependency_spec(format_type='npm'))


@composite
def poetry_dependency(draw):
    """Generate valid poetry dependency entry."""
    return draw(generate_dependency_spec(format_type='poetry'))


@composite
def npm_package_json(draw):
    """Generate valid package.json dependency objects."""
    num_deps = draw(st.integers(0, 10))
    dependencies = {}
    
    for _ in range(num_deps):
        name = draw(st.text(
            alphabet=string.ascii_lowercase + '-',
            min_size=3,
            max_size=15
        ).filter(lambda x: x[0] != '-' and x[-1] != '-'))
        
        major = draw(st.integers(0, 10))
        minor = draw(st.integers(0, 20))
        patch = draw(st.integers(0, 50))
        prefix = draw(st.sampled_from(['^', '~', '']))
        
        dependencies[name] = f"{prefix}{major}.{minor}.{patch}"
    
    return {"dependencies": dependencies}


# File Path Generators
@composite
def generate_file_tree(draw):
    """
    Generate valid directory structures with files.
    
    Returns a dictionary representing a file tree where:
    - Keys are directory/file names
    - Values are either nested dicts (for directories) or strings (for file content)
    """
    # Invalid path characters to avoid
    invalid_chars = '<>:"|?*\x00'
    
    def generate_name(draw, is_file=False):
        """Generate a valid file or directory name."""
        name = draw(st.text(
            alphabet=string.ascii_lowercase + string.digits + '_-',
            min_size=1,
            max_size=15
        ).filter(lambda x: x[0] not in '-_' and x[-1] not in '-_' and 
                not any(c in invalid_chars for c in x)))
        
        if is_file:
            extension = draw(st.sampled_from(['.py', '.js', '.ts', '.jsx', '.tsx', '.txt', '.md']))
            return name + extension
        return name
    
    def generate_directory(draw, depth=0, max_depth=3):
        """Recursively generate directory structure."""
        if depth >= max_depth:
            return {}
        
        tree = {}
        num_items = draw(st.integers(1, 5))
        
        for _ in range(num_items):
            # Decide if this should be a file or directory
            is_file = draw(st.booleans())
            
            if is_file:
                filename = generate_name(draw, is_file=True)
                # Simple file content
                tree[filename] = "# File content"
            else:
                dirname = generate_name(draw, is_file=False)
                # Maybe include ignored directories
                if draw(st.booleans()) and depth == 0:
                    dirname = draw(st.sampled_from(['node_modules', '__pycache__', '.git', 
                                                   '.venv', 'dist', 'build', dirname]))
                
                # Recursively generate subdirectory
                tree[dirname] = generate_directory(draw, depth + 1, max_depth)
        
        return tree
    
    return generate_directory(draw)


@composite
def generate_repository_metadata(draw):
    """
    Generate repository metadata with all required fields.
    
    Returns a dictionary with repository metadata including:
    - default_branch: Main branch name
    - last_commit: Last commit hash
    - last_commit_date: ISO format date string
    - size: Repository size in bytes
    - language: Primary language
    - stars: Number of stars
    - forks: Number of forks
    """
    branch_names = ['main', 'master', 'develop', 'dev']
    languages = ['Python', 'JavaScript', 'TypeScript', 'Java', 'Go', 'Ruby', 'PHP']
    
    # Generate a realistic commit hash (40 hex characters)
    commit_hash = ''.join(draw(st.lists(
        st.sampled_from('0123456789abcdef'),
        min_size=40,
        max_size=40
    )))
    
    # Generate a date in ISO format
    from datetime import datetime, timedelta
    days_ago = draw(st.integers(0, 365))
    commit_date = (datetime.now() - timedelta(days=days_ago)).isoformat()
    
    return {
        'default_branch': draw(st.sampled_from(branch_names)),
        'last_commit': commit_hash,
        'last_commit_date': commit_date,
        'size': draw(st.integers(1000, 100000000)),  # 1KB to 100MB
        'language': draw(st.sampled_from(languages)),
        'stars': draw(st.integers(0, 10000)),
        'forks': draw(st.integers(0, 1000)),
        'open_issues': draw(st.integers(0, 500)),
        'description': draw(st.text(min_size=10, max_size=200)),
    }


@composite
def generate_analysis_result(draw):
    """
    Generate complete analysis results with internal consistency.
    
    Ensures:
    - Language percentages sum to 100%
    - File counts are consistent
    - Issue file paths are valid
    - Technical debt grade matches score
    """
    # Generate languages with percentages that sum to 100%
    num_languages = draw(st.integers(1, 5))
    language_names = draw(st.lists(
        st.sampled_from(['Python', 'JavaScript', 'TypeScript', 'Java', 'Go', 'Ruby', 'PHP', 'C++', 'C#']),
        min_size=num_languages,
        max_size=num_languages,
        unique=True
    ))
    
    # Generate percentages that sum to 100
    if num_languages == 1:
        percentages = [100.0]
    else:
        # Generate random percentages and normalize to 100
        raw_percentages = [draw(st.floats(min_value=1.0, max_value=100.0)) for _ in range(num_languages)]
        total = sum(raw_percentages)
        percentages = [round((p / total) * 100, 2) for p in raw_percentages]
        
        # Adjust last percentage to ensure exact sum of 100
        percentages[-1] = round(100.0 - sum(percentages[:-1]), 2)
    
    # Generate file counts for each language
    total_files = draw(st.integers(10, 1000))
    file_counts = []
    remaining = total_files
    
    for i in range(num_languages - 1):
        count = int(total_files * percentages[i] / 100)
        file_counts.append(count)
        remaining -= count
    file_counts.append(remaining)  # Last language gets remaining files
    
    languages = [
        {
            'name': lang,
            'percentage': pct,
            'file_count': count
        }
        for lang, pct, count in zip(language_names, percentages, file_counts)
    ]
    
    # Generate frameworks
    framework_options = {
        'Python': ['Django', 'Flask', 'FastAPI', 'Pyramid'],
        'JavaScript': ['React', 'Vue', 'Angular', 'Express'],
        'TypeScript': ['React', 'Angular', 'NestJS', 'Next.js'],
        'Java': ['Spring', 'Hibernate', 'Struts'],
        'Go': ['Gin', 'Echo', 'Fiber'],
        'Ruby': ['Rails', 'Sinatra'],
        'PHP': ['Laravel', 'Symfony', 'CodeIgniter'],
    }
    
    frameworks = []
    for lang in language_names:
        if lang in framework_options and draw(st.booleans()):
            framework = draw(st.sampled_from(framework_options[lang]))
            frameworks.append({
                'name': framework,
                'language': lang,
                'version': f"{draw(st.integers(1, 5))}.{draw(st.integers(0, 20))}.{draw(st.integers(0, 50))}"
            })
    
    # Generate issues with valid file paths
    num_issues = draw(st.integers(0, 50))
    issues = []
    severity_levels = ['critical', 'high', 'medium', 'low']
    issue_types = ['deprecated_api', 'security_vulnerability', 'code_smell', 'performance_issue']
    
    for _ in range(num_issues):
        # Generate valid relative file path
        depth = draw(st.integers(1, 4))
        path_parts = []
        for _ in range(depth):
            part = draw(st.text(
                alphabet=string.ascii_lowercase + '_',
                min_size=3,
                max_size=10
            ).filter(lambda x: x[0] != '_'))
            path_parts.append(part)
        
        extension = draw(st.sampled_from(['.py', '.js', '.ts', '.java', '.go']))
        path_parts[-1] += extension
        file_path = '/'.join(path_parts)
        
        issues.append({
            'type': draw(st.sampled_from(issue_types)),
            'severity': draw(st.sampled_from(severity_levels)),
            'file': file_path,
            'line': draw(st.integers(1, 1000)),
            'message': draw(st.text(min_size=10, max_size=100))
        })
    
    # Generate technical debt with consistent grade
    maintainability_score = draw(st.integers(0, 100))
    
    # Determine grade based on score
    if maintainability_score >= 80:
        grade = 'A'
    elif maintainability_score >= 60:
        grade = 'B'
    elif maintainability_score >= 40:
        grade = 'C'
    elif maintainability_score >= 20:
        grade = 'D'
    else:
        grade = 'F'
    
    tech_debt = {
        'maintainability_score': maintainability_score,
        'grade': grade,
        'estimated_hours': draw(st.integers(1, 1000)),
        'complexity_score': draw(st.floats(min_value=1.0, max_value=10.0)),
        'duplication_percentage': draw(st.floats(min_value=0.0, max_value=50.0))
    }
    
    return {
        'languages': languages,
        'frameworks': frameworks,
        'issues': issues,
        'tech_debt': tech_debt,
        'total_files': total_files,
        'total_lines': draw(st.integers(total_files * 10, total_files * 500))
    }


@composite
def file_paths(draw):
    """Generate valid file paths."""
    depth = draw(st.integers(1, 5))
    parts = []
    
    for _ in range(depth):
        part = draw(st.text(
            alphabet=string.ascii_lowercase + '_',
            min_size=1,
            max_size=10
        ))
        parts.append(part)
    
    extension = draw(st.sampled_from(['.py', '.js', '.ts', '.txt']))
    parts[-1] += extension
    
    return '/'.join(parts)


# Tests for generators themselves
def test_generate_git_url_produces_valid_patterns():
    """Test that generate_git_url produces URLs matching expected patterns."""
    import re
    
    # Patterns for valid Git URLs
    https_pattern = r'^https://[a-z0-9.-]+/[a-z0-9-]+/[a-z0-9._-]+\.git$'
    git_pattern = r'^git://[a-z0-9.-]+/[a-z0-9-]+/[a-z0-9._-]+\.git$'
    ssh_pattern = r'^git@[a-z0-9.-]+:[a-z0-9-]+/[a-z0-9._-]+\.git$'
    
    # Generate several URLs and check they match one of the patterns
    for _ in range(20):
        url = generate_git_url().example()
        assert (re.match(https_pattern, url) or 
                re.match(git_pattern, url) or 
                re.match(ssh_pattern, url)), f"Generated URL doesn't match expected pattern: {url}"


def test_generate_invalid_url_produces_invalid_patterns():
    """Test that generate_invalid_url produces URLs that should be rejected."""
    import re
    
    # Pattern for valid Git URLs (should NOT match)
    valid_pattern = r'^(https://|git://|git@)[a-z0-9.-]+[:/][a-z0-9-]+/[a-z0-9._-]+\.git$'
    
    # Generate several invalid URLs and check they don't match valid pattern
    for _ in range(20):
        url = generate_invalid_url().example()
        # Most invalid URLs should not match the valid pattern
        # (Some edge cases might accidentally match, but most shouldn't)
        if url.strip():  # Skip empty/whitespace-only strings
            assert not re.match(valid_pattern, url) or len(url) < 10, \
                f"Generated invalid URL accidentally matches valid pattern: {url}"


def test_generate_python_code_produces_parseable_code():
    """Test that generate_python_code produces code that can be parsed by ast.parse()."""
    import ast
    
    # Generate several code snippets and verify they parse
    for _ in range(20):
        code = generate_python_code().example()
        try:
            ast.parse(code)
        except SyntaxError as e:
            raise AssertionError(f"Generated code has syntax error: {code}\nError: {e}")


def test_generate_dependency_spec_pip_format():
    """Test that generate_dependency_spec produces valid pip format."""
    import re
    
    # Pattern for pip dependencies: package==1.0.0, package>=1.0.0, etc.
    pip_pattern = r'^[a-z][a-z0-9_-]*[a-z0-9](==|>=|~=|<=|>)\d+\.\d+\.\d+$'
    
    for _ in range(20):
        dep = generate_dependency_spec(format_type='pip').example()
        assert re.match(pip_pattern, dep), f"Generated pip dependency doesn't match pattern: {dep}"


def test_generate_dependency_spec_npm_format():
    """Test that generate_dependency_spec produces valid npm format."""
    import re
    
    # Pattern for npm dependencies: "package": "^1.0.0"
    npm_pattern = r'^"[a-z][a-z0-9_-]*[a-z0-9]": "[\^~]?\d+\.\d+\.\d+"$'
    
    for _ in range(20):
        dep = generate_dependency_spec(format_type='npm').example()
        assert re.match(npm_pattern, dep), f"Generated npm dependency doesn't match pattern: {dep}"


def test_generate_dependency_spec_poetry_format():
    """Test that generate_dependency_spec produces valid poetry format."""
    import re
    
    # Pattern for poetry dependencies: package = "^1.0.0"
    poetry_pattern = r'^[a-z][a-z0-9_-]*[a-z0-9] = "[\^~]?\d+\.\d+\.\d+"$'
    
    for _ in range(20):
        dep = generate_dependency_spec(format_type='poetry').example()
        assert re.match(poetry_pattern, dep), f"Generated poetry dependency doesn't match pattern: {dep}"


def test_generate_file_tree_produces_valid_structure():
    """Test that generate_file_tree produces valid directory structures."""
    import os
    
    # Invalid path characters that should not appear
    invalid_chars = '<>:"|?*\x00'
    
    def validate_tree(tree, path=""):
        """Recursively validate the file tree structure."""
        assert isinstance(tree, dict), f"Tree should be a dict at {path}"
        
        for name, content in tree.items():
            # Check for invalid characters
            assert not any(c in invalid_chars for c in name), \
                f"Invalid character in name: {name}"
            
            # Check name is not empty
            assert len(name) > 0, f"Empty name in tree at {path}"
            
            # Check if it's a file or directory
            if isinstance(content, str):
                # It's a file - should have an extension
                assert '.' in name, f"File should have extension: {name}"
                assert name.split('.')[-1] in ['py', 'js', 'ts', 'jsx', 'tsx', 'txt', 'md'], \
                    f"File has unexpected extension: {name}"
            elif isinstance(content, dict):
                # It's a directory - recursively validate
                validate_tree(content, os.path.join(path, name))
            else:
                raise AssertionError(f"Unexpected content type at {path}/{name}: {type(content)}")
    
    # Generate and validate several file trees
    for _ in range(10):
        tree = generate_file_tree().example()
        validate_tree(tree)


def test_generate_repository_metadata_has_required_fields():
    """Test that generate_repository_metadata produces complete metadata."""
    required_fields = [
        'default_branch',
        'last_commit',
        'last_commit_date',
        'size',
        'language',
        'stars',
        'forks',
    ]
    
    for _ in range(10):
        metadata = generate_repository_metadata().example()
        
        # Check all required fields are present
        for field in required_fields:
            assert field in metadata, f"Missing required field: {field}"
        
        # Validate field types and values
        assert isinstance(metadata['default_branch'], str)
        assert metadata['default_branch'] in ['main', 'master', 'develop', 'dev']
        
        assert isinstance(metadata['last_commit'], str)
        assert len(metadata['last_commit']) == 40  # Git commit hash length
        
        assert isinstance(metadata['last_commit_date'], str)
        # Should be ISO format date
        from datetime import datetime
        datetime.fromisoformat(metadata['last_commit_date'])  # Will raise if invalid
        
        assert isinstance(metadata['size'], int)
        assert metadata['size'] > 0
        
        assert isinstance(metadata['language'], str)
        assert isinstance(metadata['stars'], int)
        assert metadata['stars'] >= 0
        
        assert isinstance(metadata['forks'], int)
        assert metadata['forks'] >= 0


def test_generate_analysis_result_has_consistent_data():
    """Test that generate_analysis_result produces internally consistent data."""
    for _ in range(10):
        result = generate_analysis_result().example()
        
        # Check required fields
        assert 'languages' in result
        assert 'frameworks' in result
        assert 'issues' in result
        assert 'tech_debt' in result
        assert 'total_files' in result
        assert 'total_lines' in result
        
        # Validate language percentages sum to 100% (with small tolerance for rounding)
        total_percentage = sum(lang['percentage'] for lang in result['languages'])
        assert abs(total_percentage - 100.0) < 0.1, \
            f"Language percentages sum to {total_percentage}, expected 100"
        
        # Validate file counts sum to total_files
        total_file_count = sum(lang['file_count'] for lang in result['languages'])
        assert total_file_count == result['total_files'], \
            f"File counts sum to {total_file_count}, expected {result['total_files']}"
        
        # Validate issue file paths are valid (no absolute paths, no null bytes)
        for issue in result['issues']:
            assert 'file' in issue
            file_path = issue['file']
            assert not file_path.startswith('/'), f"Issue has absolute path: {file_path}"
            assert not file_path.startswith('\\'), f"Issue has absolute path: {file_path}"
            assert '\x00' not in file_path, f"Issue has null byte in path: {file_path}"
            assert '..' not in file_path, f"Issue has path traversal: {file_path}"
        
        # Validate technical debt grade matches score
        score = result['tech_debt']['maintainability_score']
        grade = result['tech_debt']['grade']
        
        if score >= 80:
            assert grade == 'A', f"Score {score} should be grade A, got {grade}"
        elif score >= 60:
            assert grade == 'B', f"Score {score} should be grade B, got {grade}"
        elif score >= 40:
            assert grade == 'C', f"Score {score} should be grade C, got {grade}"
        elif score >= 20:
            assert grade == 'D', f"Score {score} should be grade D, got {grade}"
        else:
            assert grade == 'F', f"Score {score} should be grade F, got {grade}"
