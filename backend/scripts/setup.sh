#!/bin/bash

# SEO Sentinel - Automated Setup Script
# Run this to set up the complete project in one command

set -e  # Exit on any error

echo "=========================================="
echo "🎯 SEO Sentinel - Setup Script"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✓ Found Python ${PYTHON_VERSION}${NC}"

# Create virtual environment
echo ""
echo -e "${YELLOW}Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment already exists. Skipping...${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo ""
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Upgrade pip
echo ""
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓ pip upgraded${NC}"

# Install dependencies
echo ""
echo -e "${YELLOW}Installing dependencies...${NC}"
echo "This may take a few minutes..."

pip install scrapy reportlab Pillow python-dotenv requests > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

# Create necessary directories
echo ""
echo -e "${YELLOW}Creating project directories...${NC}"
mkdir -p reports logs
echo -e "${GREEN}✓ Directories created${NC}"

# Create .env file if it doesn't exist
echo ""
echo -e "${YELLOW}Setting up environment variables...${NC}"
if [ ! -f ".env" ]; then
    cat > .env << EOF
# SEO Sentinel Environment Variables
ENVIRONMENT=development
SENDGRID_API_KEY=your_sendgrid_key_here
DATABASE_URL=postgresql://user:pass@localhost/seo_sentinel
REDIS_URL=redis://localhost:6379/0
EOF
    echo -e "${GREEN}✓ Created .env file (update with your API keys)${NC}"
else
    echo -e "${YELLOW}⚠️  .env file already exists. Skipping...${NC}"
fi

# Create .gitignore
echo ""
echo -e "${YELLOW}Creating .gitignore...${NC}"
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# SEO Sentinel
reports/*.pdf
reports/*.json
logs/*.log
*.json
*.pdf
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF
    echo -e "${GREEN}✓ .gitignore created${NC}"
else
    echo -e "${YELLOW}⚠️  .gitignore already exists. Skipping...${NC}"
fi

# Run demo to verify installation
echo ""
echo -e "${YELLOW}Running demo to verify installation...${NC}"
python demo.py

# Display next steps
echo ""
echo "=========================================="
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "📚 Next Steps:"
echo ""
echo "1. Activate the virtual environment:"
echo "   ${YELLOW}source venv/bin/activate${NC}"
echo ""
echo "2. Run the demo:"
echo "   ${YELLOW}python demo.py${NC}"
echo ""
echo "3. Scan your first website:"
echo "   ${YELLOW}python seo_sentinel.py example.com${NC}"
echo ""
echo "4. Customize your branding:"
echo "   ${YELLOW}Edit config.py${NC}"
echo ""
echo "5. Update API keys in:"
echo "   ${YELLOW}.env${NC}"
echo ""
echo "📄 Documentation: README.md"
echo "🐛 Issues: https://github.com/yourusername/seo-sentinel/issues"
echo ""
echo "=========================================="
echo -e "${GREEN}🚀 Start making money!${NC}"
echo "=========================================="