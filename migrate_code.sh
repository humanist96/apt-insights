#!/bin/bash

# Code Migration Script
# Replaces old API files with new refactored versions

echo "🔄 Starting code migration..."
echo

# Backup old files
echo "📦 Creating backups..."
mv api_01/api_01_silv_trade.py api_01/api_01_silv_trade.old.py 2>/dev/null || true
mv api_02/api_02_apt_trade.py api_02/api_02_apt_trade.old.py 2>/dev/null || true
mv api_03/api_03_apt_trade_dev.py api_03/api_03_apt_trade_dev.old.py 2>/dev/null || true
mv api_04/api_04_apt_rent.py api_04/api_04_apt_rent.old.py 2>/dev/null || true

echo "✅ Old files backed up (.old.py)"
echo

# Migrate new files
echo "🚀 Migrating new files..."
mv api_01/api_01_silv_trade_new.py api_01/api_01_silv_trade.py
mv api_02/api_02_apt_trade_new.py api_02/api_02_apt_trade.py
mv api_03/api_03_apt_trade_dev_new.py api_03/api_03_apt_trade_dev.py
mv api_04/api_04_apt_rent_new.py api_04/api_04_apt_rent.py

echo "✅ New files migrated"
echo

# List files
echo "📁 New file structure:"
ls -lh api_01/api_01_silv_trade.py
ls -lh api_02/api_02_apt_trade.py
ls -lh api_03/api_03_apt_trade_dev.py
ls -lh api_04/api_04_apt_rent.py

echo
echo "✅ Migration complete!"
echo
echo "Old files saved as:"
echo "  - api_*/api_*_*.old.py"
