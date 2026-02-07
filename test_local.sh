#!/bin/bash

# Local Testing Script for carconnectivity-webui-by-m7xlab
# This script helps test the package locally before uploading to PyPI

set -e  # Exit on error

echo "================================================"
echo "CarConnectivity WebUI by m7xlab - Local Testing"
echo "================================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}Error: pyproject.toml not found${NC}"
    exit 1
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info src/*.egg-info
echo -e "${GREEN}✓ Cleaned${NC}"
echo ""

# Build the package
echo "Building package..."
python3 -m build
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Build failed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Package built${NC}"
echo ""

# Show built files
echo "Built files:"
ls -lh dist/
echo ""

# Check the package
echo "Checking package..."
python3 -m twine check dist/*
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Package check failed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Package check passed${NC}"
echo ""

# Install locally in development mode
echo "Installing package in development mode..."
pip install -e .
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Installation failed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Package installed${NC}"
echo ""

# Test imports
echo "Testing imports..."
python3 -c "from carconnectivity_plugins.webui import plugin" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Plugin import successful${NC}"
else
    echo -e "${RED}Error: Plugin import failed${NC}"
    exit 1
fi

python3 -c "import django; print(f'Django version: {django.VERSION}')"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Django import successful${NC}"
else
    echo -e "${RED}Error: Django import failed${NC}"
    exit 1
fi
echo ""

# Show package info
echo "Package information:"
pip show carconnectivity-webui-by-m7xlab
echo ""

echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}✓ Local testing completed successfully!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo "Next steps:"
echo "1. Test with CarConnectivity using your config"
echo "2. Access http://localhost:4000 in your browser"
echo "3. Verify all features work correctly"
echo "4. Run ./upload_pypi.sh to publish to PyPI"
echo ""
