#!/bin/bash
# Quick Start Script for MLOps Heart Disease Project
# Runs all steps in sequence

set -e

echo "╔══════════════════════════════════════════════════════════╗"
echo "║   MLOps Heart Disease Prediction - Quick Start          ║"
echo "╚══════════════════════════════════════════════════════════╝"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Setup
echo -e "\n${BLUE}[1/6] Setting up environment...${NC}"
if [ ! -d "venv" ]; then
    python -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment exists${NC}"
fi

source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Step 2: Install dependencies
echo -e "\n${BLUE}[2/6] Installing dependencies...${NC}"
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Step 3: Download data
echo -e "\n${BLUE}[3/6] Downloading dataset...${NC}"
python data/download_data.py
echo -e "${GREEN}✓ Dataset downloaded${NC}"

# Step 4: Train models
echo -e "\n${BLUE}[4/6] Training models...${NC}"
python train.py
echo -e "${GREEN}✓ Models trained${NC}"

# Step 5: Run tests
echo -e "\n${BLUE}[5/6] Running tests...${NC}"
pytest tests/ -v --tb=short 2>&1 | tail -20
echo -e "${GREEN}✓ Tests completed${NC}"

# Step 6: Summary
echo -e "\n${BLUE}[6/6] Setup complete!${NC}"
echo -e "\n${YELLOW}Next steps:${NC}"
echo "  1. View experiments:       mlflow ui --port 5001"
echo "  2. Start API:              python -m src.api.app"
echo "  3. Or start full stack:    docker-compose up -d"
echo "  4. Test API:               curl http://localhost:5000/health"
echo ""
echo -e "${GREEN}✓ MLOps project is ready!${NC}"
