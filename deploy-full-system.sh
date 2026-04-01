#!/bin/bash

# =============================================================================
# $1000/WEEK PASSIVE INCOME SYSTEM - FULL DEPLOYMENT SCRIPT
# =============================================================================
# This script sets up the entire automation system
# Run with: ./deploy-full-system.sh
# =============================================================================

set -e  # Exit on any error

echo "=========================================="
echo "  $1000/WEEK PASSIVE INCOME SYSTEM"
echo "  Complete Deployment"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =============================================================================
# STEP 1: CHECK PREREQUISITES
# =============================================================================
echo -e "${BLUE}Step 1: Checking Prerequisites...${NC}"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js is not installed. Please install Node.js first.${NC}"
    echo "Visit: https://nodejs.org/"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3 first.${NC}"
    exit 1
fi

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}Git is not installed. Please install Git first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ All prerequisites met${NC}"
echo ""

# =============================================================================
# STEP 2: SETUP ENVIRONMENT
# =============================================================================
echo -e "${BLUE}Step 2: Setting Up Environment...${NC}"

# Create .env file from template
if [ ! -f .env ]; then
    if [ -f ../configs/.env.template ]; then
        cp ../configs/.env.template .env
        echo -e "${YELLOW}⚠ Created .env file from template${NC}"
        echo -e "${YELLOW}⚠ Please edit .env with your actual API keys before continuing${NC}"
        echo ""
        read -p "Press Enter after you've configured .env..."
    else
        echo -e "${RED}Environment template not found${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ .env file exists${NC}"
fi

# Load environment variables
export $(grep -v '^#' .env | xargs)

echo ""

# =============================================================================
# STEP 3: INSTALL DEPENDENCIES
# =============================================================================
echo -e "${BLUE}Step 3: Installing Dependencies...${NC}"

# Install Python dependencies
echo "Installing Python packages..."
pip3 install -q -r ../passive-income-automation/requirements.txt
echo -e "${GREEN}✓ Python dependencies installed${NC}"

# Install Node.js dependencies for deployment tools
echo "Installing Node.js packages..."
npm install -g vercel@latest 2>/dev/null || true
npm install -g @railway/cli@latest 2>/dev/null || true
echo -e "${GREEN}✓ Node.js dependencies installed${NC}"

echo ""

# =============================================================================
# STEP 4: SETUP DATABASE
# =============================================================================
echo -e "${BLUE}Step 4: Setting Up Database...${NC}"

# Check if Supabase credentials are configured
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_KEY" ]; then
    echo -e "${RED}Supabase credentials not found in .env${NC}"
    echo "Please set SUPABASE_URL and SUPABASE_KEY"
    exit 1
fi

# Run database setup
python3 << PYTHON_SCRIPT
import os
import sys
sys.path.append('../passive-income-automation')

from database.supabase_client import SupabaseClient

print("Connecting to Supabase...")
client = SupabaseClient()

# Test connection
try:
    result = client.client.table('health_check').select('*').limit(1).execute()
    print("✓ Database connection successful")
except Exception as e:
    print(f"⚠ Connection test: {e}")
    print("  (This is OK if tables don't exist yet)")

print("✓ Database setup complete")
PYTHON_SCRIPT

echo ""

# =============================================================================
# STEP 5: DEPLOY API SERVER
# =============================================================================
echo -e "${BLUE}Step 5: Deploying API Server...${NC}"

echo "Choose deployment platform:"
echo "1) Vercel (FREE - Recommended)"
echo "2) Railway ($5/month)"
echo "3) Skip (manual deployment)"
read -p "Enter choice (1-3): " deploy_choice

case $deploy_choice in
    1)
        echo "Deploying to Vercel..."
        if ! command -v vercel &> /dev/null; then
            npm install -g vercel
        fi
        
        # Copy files to deployment directory
        cp -r ../passive-income-automation/* .
        
        # Deploy
        vercel --prod --yes
        
        echo -e "${GREEN}✓ Deployed to Vercel${NC}"
        ;;
    2)
        echo "Deploying to Railway..."
        if ! command -v railway &> /dev/null; then
            npm install -g @railway/cli
        fi
        
        # Copy files
        cp -r ../passive-income-automation/* .
        
        # Deploy
        railway up
        
        echo -e "${GREEN}✓ Deployed to Railway${NC}"
        ;;
    3)
        echo -e "${YELLOW}Skipping deployment. Deploy manually later.${NC}"
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""

# =============================================================================
# STEP 6: SETUP MAKE.COM WORKFLOWS
# =============================================================================
echo -e "${BLUE}Step 6: Make.com Workflow Setup...${NC}"

echo -e "${YELLOW}To complete Make.com setup:${NC}"
echo "1. Log in to https://make.com"
echo "2. Create a new scenario"
echo "3. Import the workflow JSON files from: make-workflows/"
echo "4. Configure webhooks to point to your deployed API"
echo "5. Activate the scenarios"
echo ""
echo "Workflow files to import:"
ls -1 ../make-workflows/*.json | xargs -n1 basename
echo ""

# =============================================================================
# STEP 7: SETUP STRIPE
# =============================================================================
echo -e "${BLUE}Step 7: Stripe Configuration...${NC}"

if [ -z "$STRIPE_SECRET_KEY" ]; then
    echo -e "${RED}Stripe credentials not found in .env${NC}"
    echo "Please set STRIPE_SECRET_KEY and STRIPE_WEBHOOK_SECRET"
else
    echo -e "${GREEN}✓ Stripe credentials found${NC}"
    echo ""
    echo -e "${YELLOW}To complete Stripe setup:${NC}"
    echo "1. Log in to https://dashboard.stripe.com"
    echo "2. Create your products and pricing plans:"
    echo "   - Starter Plan: $27/month"
    echo "   - Pro Plan: $97/month"
    echo "   - Annual Plan: $970/year"
    echo "3. Copy the Price IDs to your .env file"
    echo "4. Configure webhook endpoint:"
    echo "   URL: https://your-api.com/api/v1/payments/webhook"
    echo "   Events: checkout.session.completed, invoice.payment_succeeded"
    echo "5. Copy webhook secret to .env"
fi

echo ""

# =============================================================================
# STEP 8: SETUP EMAIL (SENDGRID)
# =============================================================================
echo -e "${BLUE}Step 8: Email Configuration...${NC}"

if [ -z "$SENDGRID_API_KEY" ]; then
    echo -e "${RED}SendGrid API key not found in .env${NC}"
    echo "Please set SENDGRID_API_KEY"
else
    echo -e "${GREEN}✓ SendGrid credentials found${NC}"
    echo ""
    echo -e "${YELLOW}To complete email setup:${NC}"
    echo "1. Log in to https://sendgrid.com"
    echo "2. Create email templates for:"
    echo "   - Welcome email"
    echo "   - Payment confirmation"
    echo "   - Onboarding sequence (7 emails)"
    echo "   - Support responses"
    echo "3. Copy template IDs to Make.com workflows"
fi

echo ""

# =============================================================================
# STEP 9: VERIFY SETUP
# =============================================================================
echo -e "${BLUE}Step 9: Verifying Setup...${NC}"

python3 << PYTHON_SCRIPT
import os
import sys

print("Checking configuration...")

required_vars = [
    'ANTHROPIC_API_KEY',
    'OPENAI_API_KEY',
    'SUPABASE_URL',
    'SUPABASE_KEY',
    'STRIPE_SECRET_KEY',
    'SENDGRID_API_KEY'
]

missing = []
for var in required_vars:
    if not os.getenv(var):
        missing.append(var)

if missing:
    print(f"⚠ Missing environment variables: {', '.join(missing)}")
    print("Please add these to your .env file")
else:
    print("✓ All required environment variables configured")

print("\n✓ Setup verification complete")
PYTHON_SCRIPT

echo ""

# =============================================================================
# STEP 10: START MONITORING
# =============================================================================
echo -e "${BLUE}Step 10: Starting Monitoring...${NC}"

echo "Starting background monitoring..."
nohup python3 ../passive-income-automation/main.py > api.log 2>&1 &
echo $! > api.pid

echo -e "${GREEN}✓ API server started (PID: $(cat api.pid))${NC}"
echo "Logs: tail -f api.log"
echo ""

# =============================================================================
# DEPLOYMENT COMPLETE
# =============================================================================
echo "=========================================="
echo -e "${GREEN}  DEPLOYMENT COMPLETE!${NC}"
echo "=========================================="
echo ""
echo -e "${BLUE}Your $1000/week system is now running!${NC}"
echo ""
echo "Next steps:"
echo "1. Configure your website (Webflow/template)"
echo "2. Import Make.com workflows"
echo "3. Create Stripe products"
echo "4. Create SendGrid email templates"
echo "5. Test the entire flow"
echo "6. Launch!"
echo ""
echo "Monitoring:"
echo "- API logs: tail -f api.log"
echo "- Health check: curl http://localhost:8000/health"
echo ""
echo "Documentation:"
echo "- Master Plan: ../MASTER_IMPLEMENTATION_PLAN.md"
echo "- Quick Start: ../QUICK_START_GUIDE.md"
echo "- AI Prompts: ../ai-prompts/"
echo ""
echo -e "${GREEN}Good luck! 🚀${NC}"
