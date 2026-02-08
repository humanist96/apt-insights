#!/bin/bash
# =============================================================================
# Database Restore Script
# =============================================================================
# This script restores a PostgreSQL database from a backup file

set -e

# Configuration
BACKUP_DIR="./backups"

echo "========================================"
echo "  Database Restore"
echo "========================================"
echo ""

# Check if backup directory exists
if [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ Error: Backup directory not found: $BACKUP_DIR"
    exit 1
fi

# List available backups
echo "Available backups:"
ls -lh "$BACKUP_DIR"/apt_insights_backup_*.dump 2>/dev/null || {
    echo "❌ No backup files found!"
    exit 1
}

echo ""
read -p "Enter backup filename to restore: " BACKUP_FILE

if [ ! -f "$BACKUP_DIR/$BACKUP_FILE" ]; then
    echo "❌ Error: Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo ""
echo "⚠️  WARNING: This will REPLACE the current database!"
echo "⚠️  All existing data will be lost!"
echo ""
read -p "Are you sure you want to continue? (type 'yes'): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Restore cancelled."
    exit 0
fi

echo ""
echo "Restoring database from: $BACKUP_FILE"

# Drop existing database and recreate
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U postgres -c "DROP DATABASE IF EXISTS apt_insights;"
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U postgres -c "CREATE DATABASE apt_insights;"

# Restore from backup
docker-compose -f docker-compose.prod.yml exec -T postgres pg_restore \
    -U postgres \
    -d apt_insights \
    -F c \
    "/backups/$BACKUP_FILE"

echo ""
echo "✅ Database restored successfully!"
echo ""
echo "Verify restoration:"
echo "  docker-compose -f docker-compose.prod.yml exec postgres psql -U postgres -d apt_insights -c 'SELECT COUNT(*) FROM transactions;'"
