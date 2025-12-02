#!/bin/sh
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Define paths
PRISMA_DIR="/app/prisma"
PRISMA_TEMPLATE_DIR="/app/prisma-template"
DB_FILE="$PRISMA_DIR/db.sqlite"
LOCAL_DB_DIR="/app/local-db"

echo "${GREEN}=== Easy Dataset Database Initialization ===${NC}"

# Create prisma directory if it doesn't exist
if [ ! -d "$PRISMA_DIR" ]; then
    echo "${YELLOW}Creating prisma directory...${NC}"
    mkdir -p "$PRISMA_DIR"
fi

# Check if database file exists
if [ ! -f "$DB_FILE" ]; then
    echo "${YELLOW}Database file not found at: $DB_FILE${NC}"

    # Check if local-db has files (possible configuration issue)
    if [ -d "$LOCAL_DB_DIR" ] && [ -n "$(ls -A $LOCAL_DB_DIR 2>/dev/null | grep -v 'empty.txt')" ]; then
        echo "${YELLOW}Note: local-db contains files but database is missing.${NC}"
        echo "${YELLOW}If you have existing data, ensure prisma volume is mounted.${NC}"
    fi

    # Safety check: only initialize if directory is completely empty
    if [ -z "$(ls -A $PRISMA_DIR 2>/dev/null)" ]; then
        # Directory is completely empty - safe to initialize
        echo "${GREEN}Prisma directory is empty. Initializing from template...${NC}"

        if [ -d "$PRISMA_TEMPLATE_DIR" ]; then
            cp -r "$PRISMA_TEMPLATE_DIR"/* "$PRISMA_DIR/"
            echo "${GREEN}Database initialized from template!${NC}"
        else
            echo "${YELLOW}No template found. Running prisma db push...${NC}"
            cd /app
            pnpm prisma db push --accept-data-loss
            echo "${GREEN}Database created successfully!${NC}"
        fi
    else
        # Directory is not empty but database is missing - error out
        echo "${RED}ERROR: Database file missing but prisma directory is not empty!${NC}"
        echo "${YELLOW}This may indicate a configuration problem.${NC}"
        echo ""
        echo "${YELLOW}Files in $PRISMA_DIR:${NC}"
        ls -lh "$PRISMA_DIR"
        echo ""
        echo "${YELLOW}Please either:${NC}"
        echo "  1. Remove all files in prisma directory to re-initialize"
        echo "  2. Or run: pnpm prisma db push --accept-data-loss"
        echo ""
        exit 1
    fi
else
    echo "${GREEN}Database file exists: $DB_FILE${NC}"
fi

echo "${GREEN}=== Database Ready! Starting application... ===${NC}"
echo ""

# Execute the command passed to the container
exec "$@"
