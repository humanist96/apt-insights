#!/bin/bash
# =============================================================================
# Database Backup Script
# =============================================================================
# This script creates a backup of the PostgreSQL database

set -e

# Configuration
BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="apt_insights_backup_${TIMESTAMP}.dump"

# Load environment variables
if [ -f .env.production ]; then
    export $(cat .env.production | grep -v '^#' | xargs)
fi

# Create backup directory
mkdir -p "$BACKUP_DIR"

echo "========================================"
echo "  Database Backup"
echo "========================================"
echo "Timestamp: $(date)"
echo "Backup file: $BACKUP_FILE"
echo ""

# Create backup
docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump \
    -U postgres \
    -d apt_insights \
    -F c \
    -f "/backups/$BACKUP_FILE"

echo "✅ Backup created successfully!"
echo "Location: $BACKUP_DIR/$BACKUP_FILE"

# Keep only last 7 backups
cd "$BACKUP_DIR"
ls -t apt_insights_backup_*.dump | tail -n +8 | xargs -r rm -f

echo ""
echo "Backup retention: 7 most recent backups kept"
echo ""
echo "Existing backups:"
ls -lh apt_insights_backup_*.dump 2>/dev/null || echo "No backups found"
