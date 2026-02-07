# 🚀 m7xlab PyPI Release Guide

## Package Information

**Package Name**: `carconnectivity-webui-by-m7xlab`  
**PyPI Account**: m7xlab  
**PyPI URL**: https://pypi.org/project/carconnectivity-webui-by-m7xlab/  
**GitHub**: https://github.com/m7xlab/CarConnectivity-plugin-webui  

## ✅ Configuration Complete

All package metadata has been updated to reflect m7xlab ownership:

- ✅ Author set to "m7xlab"
- ✅ Maintainer set to "m7xlab"
- ✅ GitHub URLs point to m7xlab account
- ✅ PyPI credentials configured in `.pypirc`
- ✅ CREDITS.md created acknowledging original author
- ✅ README updated with m7xlab branding

## 📦 What's Being Published

### Package Details
- **Name**: carconnectivity-webui-by-m7xlab
- **Version**: Auto-generated from git tags (via setuptools_scm)
- **Framework**: Django 5.0
- **Python**: 3.9+
- **License**: MIT (same as original)

### Key Features
- 🎨 Apple-inspired design with glassmorphism
- 🌓 Dark mode with automatic detection
- 📱 Fully responsive (mobile, tablet, desktop)
- ⚡ Optimized performance
- 🔒 Enhanced security with Django
- ♿ WCAG 2.1 AA accessible
- 🎭 Smooth 60fps animations
- 🎯 Modern Heroicons SVG icons

## 🧪 Pre-Release Testing

### 1. Quick Test

```bash
cd "/Users/gediminas.kristopaitis/Documents/Private & Shared/CarConnectivityPlus/CarConnectivity-plugin-webui"

# Run automated test
./test_local.sh
```

### 2. Build and Check

```bash
# Clean and build
rm -rf dist/ build/ *.egg-info src/*.egg-info
python3 -m build

# Verify package
python3 -m twine check dist/*

# Should show:
# Checking dist/carconnectivity-webui-by-m7xlab-*.tar.gz: PASSED
# Checking dist/carconnectivity_webui_by_m7xlab-*-py3-none-any.whl: PASSED
```

### 3. Test Installation

```bash
# Install in development mode
pip install -e .

# Test import
python3 -c "from carconnectivity_plugins.webui import plugin; print('✓ Success')"
```

## 🚀 Publishing to PyPI

### Method 1: Automated (Recommended)

```bash
cd "/Users/gediminas.kristopaitis/Documents/Private & Shared/CarConnectivityPlus/CarConnectivity-plugin-webui"

# Run upload script
./upload_pypi.sh
```

The script will:
1. Clean previous builds
2. Build the package
3. Check package integrity
4. Ask for confirmation: **Type "yes" to proceed**
5. Upload to PyPI using your token
6. Display success message

### Method 2: Manual

```bash
# Build
python3 -m build

# Upload
python3 -m twine upload dist/* --config-file .pypirc
```

## ✅ Post-Release Verification

### 1. Check PyPI Page

Visit: https://pypi.org/project/carconnectivity-webui-by-m7xlab/

Verify:
- ✅ Package appears
- ✅ README renders correctly
- ✅ Version number is correct
- ✅ Author shows "m7xlab"
- ✅ Links work (GitHub, documentation)
- ✅ Dependencies are listed

### 2. Test Installation from PyPI

```bash
# Create fresh virtual environment
python3 -m venv test_env
source test_env/bin/activate

# Install from PyPI
pip install carconnectivity-webui-by-m7xlab

# Verify
pip show carconnectivity-webui-by-m7xlab

# Test
python3 -c "from carconnectivity_plugins.webui import plugin; print('✓ Works!')"

# Cleanup
deactivate
rm -rf test_env
```

### 3. Integration Test

Create `test_config.json`:
```json
{
    "carConnectivity": {
        "log_level": "info",
        "connectors": [],
        "plugins": [{
            "type": "webui",
            "config": {
                "username": "admin",
                "password": "test123",
                "port": 4000
            }
        }]
    }
}
```

Run:
```bash
pip install carconnectivity
pip install carconnectivity-webui-by-m7xlab
carconnectivity --config test_config.json
```

Test in browser:
- Open http://localhost:4000
- Login with admin/test123
- Verify all features work
- Test dark mode toggle
- Check responsive design on mobile

## 📋 Release Checklist

### Pre-Release
- [ ] All code tested locally
- [ ] `./test_local.sh` passes
- [ ] Package builds successfully
- [ ] `twine check` passes
- [ ] Integration test with CarConnectivity works
- [ ] All features verified in browser
- [ ] Documentation reviewed

### Release
- [ ] Run `./upload_pypi.sh`
- [ ] Type "yes" when prompted
- [ ] Wait for upload to complete
- [ ] Note the success message

### Post-Release
- [ ] Visit PyPI page and verify
- [ ] Test installation from PyPI
- [ ] Test with real CarConnectivity setup
- [ ] Update GitHub repository (if applicable)
- [ ] Tag release in git (optional)

## 🔐 Security Notes

### Token Security
- ✅ Token is stored in `.pypirc`
- ✅ `.pypirc` is in `.gitignore`
- ✅ Token will NOT be committed to git
- ⚠️ Never share `.pypirc` or commit it

### If Token is Compromised
1. Go to https://pypi.org/manage/account/token/
2. Revoke the compromised token
3. Generate a new token
4. Update `.pypirc` with new token

## 📊 Package Contents

### Included Files
- All Django application code
- 15+ HTML templates
- 4 CSS files (~1,600 lines)
- JavaScript (~400 lines)
- 9 SVG icons
- Complete documentation
- License and credits

### Excluded Files
- Test files
- Upload scripts
- PyPI credentials
- Old Flask backup
- Development files

## 🎯 Installation for Users

Once published, users can install with:

```bash
pip install carconnectivity-webui-by-m7xlab
```

Then use in their CarConnectivity config:

```json
{
    "plugins": [{
        "type": "webui",
        "config": {
            "username": "admin",
            "password": "your-password",
            "port": 4000
        }
    }]
}
```

## 📝 Version Management

This package uses `setuptools_scm` for automatic versioning from git tags.

To set a specific version:
```bash
git tag v1.0.0
git push origin v1.0.0
python3 -m build
```

The version will be automatically extracted from the tag.

## 🆘 Troubleshooting

### Build Fails
```bash
# Check pyproject.toml syntax
python3 -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb')))"

# Reinstall build tools
pip install --upgrade build twine
```

### Upload Fails
```bash
# Check credentials
cat .pypirc

# Try with verbose output
python3 -m twine upload dist/* --config-file .pypirc --verbose
```

### Import Errors After Install
```bash
# Check installation
pip show carconnectivity-webui-by-m7xlab
pip show Django

# Reinstall
pip uninstall carconnectivity-webui-by-m7xlab
pip install carconnectivity-webui-by-m7xlab
```

## 🎉 Ready to Release!

Everything is configured for the m7xlab account. To publish:

```bash
cd "/Users/gediminas.kristopaitis/Documents/Private & Shared/CarConnectivityPlus/CarConnectivity-plugin-webui"
./upload_pypi.sh
```

**Type "yes" when prompted to confirm the upload.**

The package will be live on PyPI in 1-2 minutes! 🚀

---

**Published by**: m7xlab  
**Based on**: Original CarConnectivity-plugin-webui by Till Steinbach  
**License**: MIT  
**Support**: https://github.com/m7xlab/CarConnectivity-plugin-webui/issues
