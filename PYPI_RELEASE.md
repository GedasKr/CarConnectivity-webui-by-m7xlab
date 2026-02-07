# PyPI Release Guide

## Package Information

- **Package Name**: `carconnectivity-webui-by-m7xlab`
- **PyPI URL**: https://pypi.org/project/carconnectivity-webui-by-m7xlab/
- **Author**: m7xlab (based on original by Till Steinbach)
- **Framework**: Django 5.0
- **Design**: Apple-inspired with glassmorphism

## Pre-Release Checklist

### 1. Test Locally

```bash
# Run local tests
./test_local.sh

# Or manually:
python3 -m build
python3 -m twine check dist/*
pip install -e .
```

### 2. Verify Package Contents

```bash
# Check what will be included
python3 -m build
tar -tzf dist/carconnectivity-webui-by-m7xlab-*.tar.gz | head -20
```

### 3. Test with CarConnectivity

Create a test configuration:

```json
{
    "carConnectivity": {
        "log_level": "debug",
        "connectors": [],
        "plugins": [
            {
                "type": "webui",
                "config": {
                    "username": "admin",
                    "password": "test123",
                    "port": 4000
                }
            }
        ]
    }
}
```

Run CarConnectivity and test:
- Login at http://localhost:4000
- Check all pages load
- Test theme toggle
- Verify responsive design
- Test API endpoints

### 4. Version Check

Ensure version is set correctly in `src/carconnectivity_plugins/webui/_version.py` or via setuptools_scm.

## Release Process

### Step 1: Clean Build

```bash
# Remove old builds
rm -rf dist/ build/ *.egg-info src/*.egg-info

# Clean Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

### Step 2: Build Package

```bash
# Install build tools if needed
pip install build twine

# Build the package
python3 -m build
```

This creates:
- `dist/carconnectivity-webui-by-m7xlab-X.Y.Z.tar.gz` (source distribution)
- `dist/carconnectivity_webui_by_m7xlab-X.Y.Z-py3-none-any.whl` (wheel)

### Step 3: Check Package

```bash
# Verify package integrity
python3 -m twine check dist/*
```

Should show:
```
Checking dist/carconnectivity-webui-by-m7xlab-X.Y.Z.tar.gz: PASSED
Checking dist/carconnectivity_webui_by_m7xlab-X.Y.Z-py3-none-any.whl: PASSED
```

### Step 4: Upload to PyPI

```bash
# Using the upload script (recommended)
./upload_pypi.sh

# Or manually with twine
python3 -m twine upload dist/* --config-file .pypirc
```

### Step 5: Verify Upload

1. Visit: https://pypi.org/project/carconnectivity-webui-by-m7xlab/
2. Check package metadata
3. Verify README renders correctly
4. Test installation:

```bash
# In a fresh virtual environment
python3 -m venv test_env
source test_env/bin/activate
pip install carconnectivity-webui-by-m7xlab
```

## Post-Release

### Update Documentation

Update these files with new version number:
- README.md
- QUICKSTART.md
- DJANGO_MIGRATION.md

### Tag Release

```bash
git tag -a v1.0.0 -m "Release v1.0.0 - Django-based UI with Apple design"
git push origin v1.0.0
```

### Announce

- Update GitHub releases
- Announce in CarConnectivity community
- Update documentation

## Troubleshooting

### Build Fails

```bash
# Check pyproject.toml syntax
python3 -c "import tomli; tomli.load(open('pyproject.toml', 'rb'))"

# Check for missing files
python3 -m build --verbose
```

### Upload Fails

```bash
# Check credentials
cat .pypirc

# Try with verbose output
python3 -m twine upload dist/* --config-file .pypirc --verbose
```

### Package Not Found After Upload

- Wait a few minutes for PyPI to index
- Check package name spelling
- Verify upload completed successfully

### Import Errors After Install

```bash
# Check package contents
pip show -f carconnectivity-webui-by-m7xlab

# Verify Django is installed
pip list | grep Django

# Check Python path
python3 -c "import sys; print('\n'.join(sys.path))"
```

## Version Management

This package uses setuptools_scm for automatic versioning from git tags.

To set a specific version:

```bash
# Tag the commit
git tag v1.0.0

# Build will use this version
python3 -m build
```

## Security Notes

- ⚠️ Never commit `.pypirc` to git
- ⚠️ Keep PyPI token secure
- ⚠️ Rotate token if exposed
- ✅ Token is in `.gitignore`

## Support

For issues:
- GitHub Issues: https://github.com/m7xlab/CarConnectivity-plugin-webui/issues
- PyPI: https://pypi.org/project/carconnectivity-webui-by-m7xlab/

Original project:
- GitHub: https://github.com/tillsteinbach/CarConnectivity-plugin-webui

## License

MIT License - Same as CarConnectivity
