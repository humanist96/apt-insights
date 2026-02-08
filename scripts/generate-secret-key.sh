#!/bin/bash
# =============================================================================
# Generate Secure Secret Key
# =============================================================================
# This script generates a cryptographically secure random secret key
# suitable for production use (JWT signing, session encryption, etc.)

echo "Generating secure secret key..."
echo ""

# Generate 32-byte random string and encode as base64
SECRET_KEY=$(openssl rand -base64 32)

echo "Generated Secret Key:"
echo "====================="
echo "$SECRET_KEY"
echo ""
echo "Add this to your .env.production file:"
echo "SECRET_KEY=$SECRET_KEY"
echo ""
echo "⚠️  Keep this secret secure and never commit it to version control!"
