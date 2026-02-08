# PostgreSQL Quick Start Guide

## 🚀 30-Second Setup

```bash
# 1. Start PostgreSQL
docker-compose up -d postgres

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create tables
python -c "from backend.db.session import init_db; init_db()"

# 4. Migrate data
python backend/db/migrate_json_to_postgres.py

# 5. Enable database mode
echo "USE_DATABASE=true" >> .env

# 6. Launch app
streamlit run frontend/app.py
```

✅ **Done!** Your app now uses PostgreSQL.

---

## 🔄 Switch Between Modes

### Use PostgreSQL
```bash
# .env
USE_DATABASE=true
```

### Use JSON Files (Rollback)
```bash
# .env
USE_DATABASE=false
```

**Instant switch** - no code changes needed!

---

## 📊 Verify Migration

```bash
# Check record count
docker exec apt_insights_postgres psql -U postgres -d apt_insights -c \
  "SELECT COUNT(*) FROM transactions;"

# Check by API type
docker exec apt_insights_postgres psql -U postgres -d apt_insights -c \
  "SELECT transaction_type, COUNT(*) FROM transactions GROUP BY transaction_type;"

# Check date range
docker exec apt_insights_postgres psql -U postgres -d apt_insights -c \
  "SELECT MIN(_deal_date), MAX(_deal_date) FROM transactions;"
```

---

## 🐛 Common Issues

### PostgreSQL won't start?
```bash
# Check logs
docker-compose logs postgres

# Restart
docker-compose restart postgres
```

### Migration errors?
```bash
# Dry-run first
python backend/db/migrate_json_to_postgres.py --dry-run

# Clear and retry
docker exec apt_insights_postgres psql -U postgres -d apt_insights -c "TRUNCATE transactions;"
python backend/db/migrate_json_to_postgres.py
```

### App won't connect?
```bash
# Test connection
docker exec apt_insights_postgres pg_isready -U postgres

# Check .env
cat .env | grep DATABASE_URL
# Should be: DATABASE_URL=postgresql://postgres:postgres@localhost:5432/apt_insights
```

---

## 📈 Performance Test

```python
import time
from backend.data_loader import load_all_json_data

start = time.time()
items, info = load_all_json_data()
elapsed = time.time() - start

print(f"Loaded {len(items):,} records in {elapsed:.2f}s")
print(f"Mode: {'PostgreSQL' if info.get('database_mode') else 'JSON'}")

# Target: <2s for PostgreSQL
```

---

## 📚 Full Documentation

- **Detailed Guide**: [docs/migration_guide.md](docs/migration_guide.md)
- **Schema Reference**: [docs/database_schema.md](docs/database_schema.md)
- **Implementation Status**: [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md)

---

## 💡 Pro Tips

1. **Always dry-run first**
   ```bash
   python backend/db/migrate_json_to_postgres.py --dry-run
   ```

2. **Check migration report**
   ```bash
   ls -lt backend/db/migration_report_*.md | head -1 | awk '{print $NF}' | xargs cat
   ```

3. **Test rollback before production**
   ```bash
   # Switch to DB
   USE_DATABASE=true streamlit run frontend/app.py
   
   # Switch back to JSON (instant)
   USE_DATABASE=false streamlit run frontend/app.py
   ```

4. **Monitor query performance**
   ```bash
   # Enable SQL logging
   SQL_ECHO=true streamlit run frontend/app.py
   ```

---

**Need Help?** Check [docs/migration_guide.md](docs/migration_guide.md) for detailed troubleshooting.
