"""
Database migration script for payments table

Run this script to create the payments table in the database:
    python -m auth.migrate_payments
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()


def create_payments_table():
    """Create payments table and related indexes"""

    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/apartment_db"
    )

    engine = create_engine(database_url)

    migration_sql = """
    -- Create payment status enum type if not exists
    DO $$ BEGIN
        CREATE TYPE payment_status AS ENUM ('pending', 'processing', 'completed', 'failed', 'refunded');
    EXCEPTION
        WHEN duplicate_object THEN null;
    END $$;

    -- Create payments table
    CREATE TABLE IF NOT EXISTS payments (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        amount NUMERIC(10,2) NOT NULL CHECK (amount > 0),
        currency VARCHAR(3) NOT NULL DEFAULT 'KRW',
        status payment_status NOT NULL DEFAULT 'pending',
        payment_method VARCHAR(50),
        portone_payment_id VARCHAR(100) UNIQUE,
        receipt_number VARCHAR(100) UNIQUE,
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        completed_at TIMESTAMP
    );

    -- Create indexes for performance
    CREATE INDEX IF NOT EXISTS idx_payments_user_id ON payments(user_id);
    CREATE INDEX IF NOT EXISTS idx_payments_portone_id ON payments(portone_payment_id);
    CREATE INDEX IF NOT EXISTS idx_payments_status ON payments(status);
    CREATE INDEX IF NOT EXISTS idx_payments_created_at ON payments(created_at);

    -- Create composite index for user payment history queries
    CREATE INDEX IF NOT EXISTS idx_payments_user_created ON payments(user_id, created_at DESC);

    -- Add comment to table
    COMMENT ON TABLE payments IS 'Payment records for subscription purchases';
    COMMENT ON COLUMN payments.user_id IS 'User who made the payment';
    COMMENT ON COLUMN payments.amount IS 'Payment amount';
    COMMENT ON COLUMN payments.currency IS 'Currency code (default: KRW)';
    COMMENT ON COLUMN payments.status IS 'Payment status: pending, processing, completed, failed, refunded';
    COMMENT ON COLUMN payments.payment_method IS 'Payment method: card, bank_transfer';
    COMMENT ON COLUMN payments.portone_payment_id IS 'PortOne payment gateway ID';
    COMMENT ON COLUMN payments.receipt_number IS 'Receipt number for completed payments';
    COMMENT ON COLUMN payments.created_at IS 'Payment creation timestamp';
    COMMENT ON COLUMN payments.completed_at IS 'Payment completion timestamp';
    """

    try:
        with engine.begin() as conn:
            # Split and execute each statement
            statements = [s.strip() for s in migration_sql.split(';') if s.strip()]
            for statement in statements:
                conn.execute(text(statement))

        print("✅ Successfully created payments table and indexes")
        print("\nTable structure:")
        print("  - id: SERIAL PRIMARY KEY")
        print("  - user_id: INTEGER (FK to users)")
        print("  - amount: NUMERIC(10,2)")
        print("  - currency: VARCHAR(3) DEFAULT 'KRW'")
        print("  - status: payment_status ENUM")
        print("  - payment_method: VARCHAR(50)")
        print("  - portone_payment_id: VARCHAR(100) UNIQUE")
        print("  - receipt_number: VARCHAR(100) UNIQUE")
        print("  - created_at: TIMESTAMP")
        print("  - completed_at: TIMESTAMP")
        print("\nIndexes created:")
        print("  - idx_payments_user_id")
        print("  - idx_payments_portone_id")
        print("  - idx_payments_status")
        print("  - idx_payments_created_at")
        print("  - idx_payments_user_created (composite)")

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)
    finally:
        engine.dispose()


def rollback_payments_table():
    """Rollback payments table (drop table)"""

    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/apartment_db"
    )

    engine = create_engine(database_url)

    rollback_sql = """
    DROP TABLE IF EXISTS payments CASCADE;
    DROP TYPE IF EXISTS payment_status CASCADE;
    """

    try:
        with engine.begin() as conn:
            conn.execute(text(rollback_sql))

        print("✅ Successfully rolled back payments table")

    except Exception as e:
        print(f"❌ Rollback failed: {e}")
        sys.exit(1)
    finally:
        engine.dispose()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Database migration for payments table")
    parser.add_argument(
        "--rollback",
        action="store_true",
        help="Rollback migration (drop payments table)"
    )

    args = parser.parse_args()

    if args.rollback:
        confirm = input("⚠️  This will DROP the payments table. Are you sure? (yes/no): ")
        if confirm.lower() == "yes":
            rollback_payments_table()
        else:
            print("❌ Rollback cancelled")
    else:
        create_payments_table()
