#!/bin/bash

# Upload to PyPI Script for carconnectivity-webui-by-m7xlab
# This script builds and uploads the package to PyPI

set -e  # Exit on error

echo "================================================"
echo "CarConnectivity WebUI by m7xlab - PyPI Upload"
echo "================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}Error: pyproject.toml not found. Are you in the project root?${NC}"
    exit 1
fi

# Check if required tools are installed
echo "Checking required tools..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 is not installed${NC}"
    exit 1
fi

if ! python3 -c "import build" 2>/dev/null; then
    echo -e "${YELLOW}Installing build tool...${NC}"
    pip install build
fi

if ! python3 -c "import twine" 2>/dev/null; then
    echo -e "${YELLOW}Installing twine...${NC}"
    pip install twine
fi

echo -e "${GREEN}✓ All required tools are available${NC}"
echo ""

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
echo -e "${GREEN}✓ Package built successfully${NC}"
echo ""

# List built files
echo "Built files:"
ls -lh dist/
echo ""

# Check the package
echo "Checking package with twine..."
python3 -m twine check dist/*
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Package check failed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Package check passed${NC}"
echo ""

# Ask for confirmation before uploading
echo -e "${YELLOW}Ready to upload to PyPI!${NC}"
echo ""
echo "Package name: carconnectivity-webui-by-m7xlab"
echo "Files to upload:"
ls -1 dist/
echo ""
read -p "Do you want to proceed with upload? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo -e "${YELLOW}Upload cancelled${NC}"
    exit 0
fi

# Upload to PyPI
echo ""
echo "Uploading to PyPI..."
python3 -m twine upload dist/* --config-file .pypirc

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}================================================${NC}"
    echo -e "${GREEN}✓ Successfully uploaded to PyPI!${NC}"
    echo -e "${GREEN}================================================${NC}"
    echo ""
    echo "Package URL: https://pypi.org/project/carconnectivity-webui-by-m7xlab/"
    echo ""
    echo "To install:"
    echo "  pip install carconnectivity-webui-by-m7xlab"
    echo ""
else
    echo -e "${RED}Error: Upload failed${NC}"
    exit 1
fi
