"""
Hypothesis generators for property-based testing.
Generates random valid data for testing.
"""

from hypothesis import strategies as st
from hypothesis.strategies import composite
import string


# URL Generators
@composite
def github_urls(draw):
    """Generate valid GitHub repository URLs."""
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
    
    return f"https://github.com/{user}/{repo}"


@composite
def invalid_urls(draw):
    """Generate invalid repository URLs."""
    invalid_patterns = [
        st.just("not-a-url"),
        st.just("http://"),
        st.just("github.com/user"),
        st.just("https://github.com/"),
        st.just("https://github.com/user/"),
        st.text(alphabet=string.ascii_letters, min_size=1, max_size=10),
    ]
    return draw(st.one_of(*invalid_patterns))


# Code Generators
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
def pip_requirements(draw):
    """Generate valid pip requirement strings."""
    package = draw(st.text(
        alphabet=string.ascii_lowercase + '-_',
        min_size=3,
        max_size=20
    ))
    
    version = draw(st.one_of(
        st.just(""),
        st.builds(lambda x, y, z: f"=={x}.{y}.{z}",
                 st.integers(0, 10),
                 st.integers(0, 20),
                 st.integers(0, 50)),
        st.builds(lambda x, y, z: f">={x}.{y}.{z}",
                 st.integers(0, 10),
                 st.integers(0, 20),
                 st.integers(0, 50)),
    ))
    
    return f"{package}{version}"


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
        ))
        version = draw(st.builds(
            lambda x, y, z: f"^{x}.{y}.{z}",
            st.integers(0, 10),
            st.integers(0, 20),
            st.integers(0, 50)
        ))
        dependencies[name] = version
    
    return {"dependencies": dependencies}


# File Path Generators
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
