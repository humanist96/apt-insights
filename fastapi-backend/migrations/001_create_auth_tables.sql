-- Migration: Create authentication tables
-- Date: 2026-02-08
-- Description: Create users and subscriptions tables for authentication system

-- Create enum types
CREATE TYPE subscription_tier AS ENUM ('free', 'premium', 'enterprise');
CREATE TYPE subscription_status AS ENUM ('active', 'expired', 'cancelled');

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100),
    subscription_tier subscription_tier DEFAULT 'free' NOT NULL,
    subscription_expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    last_login_at TIMESTAMP
);

-- Create indexes for users table
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_subscription_tier ON users(subscription_tier);

-- Create subscriptions table
CREATE TABLE IF NOT EXISTS subscriptions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    plan VARCHAR(20) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    started_at TIMESTAMP DEFAULT NOW() NOT NULL,
    expires_at TIMESTAMP,
    status subscription_status DEFAULT 'active' NOT NULL
);

-- Create indexes for subscriptions table
CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);

-- Add comments
COMMENT ON TABLE users IS 'User accounts for the apartment analysis platform';
COMMENT ON TABLE subscriptions IS 'Subscription history and status for users';

COMMENT ON COLUMN users.email IS 'User email address (unique)';
COMMENT ON COLUMN users.password_hash IS 'Bcrypt hashed password';
COMMENT ON COLUMN users.subscription_tier IS 'Current subscription tier (free, premium, enterprise)';
COMMENT ON COLUMN users.subscription_expires_at IS 'When the current subscription expires (NULL for free tier)';

COMMENT ON COLUMN subscriptions.plan IS 'Subscription plan name (e.g., monthly, yearly)';
COMMENT ON COLUMN subscriptions.amount IS 'Subscription amount in KRW';
COMMENT ON COLUMN subscriptions.status IS 'Current status of the subscription';
