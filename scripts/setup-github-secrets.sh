#!/bin/bash

# GitHub Secrets Setup Automation Script
# 이 스크립트는 GitHub Secrets 설정에 필요한 모든 토큰을 자동으로 생성하고 설정합니다.

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  GitHub Secrets 자동 설정 스크립트"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) not found"
    echo "📦 Installing via Homebrew..."
    brew install gh
fi

# Check if user is logged in
if ! gh auth status &> /dev/null; then
    echo "🔐 GitHub 로그인이 필요합니다..."
    gh auth login
fi

# Get repository info
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo "📁 Repository: $REPO"
echo ""

# Function to set secret
set_secret() {
    local name=$1
    local value=$2

    if [ -z "$value" ]; then
        echo "⚠️  $name 값이 비어있습니다. 건너뜁니다."
        return
    fi

    echo "✓ Setting $name..."
    echo "$value" | gh secret set "$name" --repo="$REPO"
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  1️⃣  Railway Token 생성"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Railway CLI 설치 중..."
    brew install railway
fi

# Railway login check
if ! railway whoami &> /dev/null; then
    echo "🔐 Railway 로그인..."
    railway login
fi

echo "🎫 Railway token 생성 중..."
RAILWAY_TOKEN=$(railway tokens create 2>/dev/null | grep -o 'railway_.*' || echo "")

if [ -z "$RAILWAY_TOKEN" ]; then
    echo "⚠️  자동 생성 실패. 수동으로 생성하세요:"
    echo "   1. railway login"
    echo "   2. railway tokens create"
    echo ""
    read -p "Railway Token을 입력하세요 (railway_...): " RAILWAY_TOKEN
fi

set_secret "RAILWAY_TOKEN" "$RAILWAY_TOKEN"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  2️⃣  Vercel Token 생성"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Vercel CLI 설치 중..."
    npm install -g vercel
fi

# Vercel login check
if ! vercel whoami &> /dev/null; then
    echo "🔐 Vercel 로그인..."
    vercel login
fi

echo "ℹ️  Vercel Token은 웹에서 수동으로 생성해야 합니다:"
echo "   1. https://vercel.com/account/tokens"
echo "   2. 'Create' 버튼 클릭"
echo "   3. 이름: 'GitHub Actions'"
echo "   4. Scope: 'Full Account'"
echo "   5. Expiration: 'No Expiration'"
echo ""
read -p "Vercel Token을 입력하세요: " VERCEL_TOKEN

set_secret "VERCEL_TOKEN" "$VERCEL_TOKEN"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  3️⃣  Vercel Project ID 가져오기"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd nextjs-frontend

# Link Vercel project if not already linked
if [ ! -d ".vercel" ]; then
    echo "🔗 Vercel 프로젝트 연결 중..."
    vercel link
fi

# Extract IDs from .vercel/project.json
if [ -f ".vercel/project.json" ]; then
    VERCEL_ORG_ID=$(cat .vercel/project.json | grep -o '"orgId": "[^"]*"' | cut -d'"' -f4)
    VERCEL_PROJECT_ID=$(cat .vercel/project.json | grep -o '"projectId": "[^"]*"' | cut -d'"' -f4)

    echo "✓ Organization ID: $VERCEL_ORG_ID"
    echo "✓ Project ID: $VERCEL_PROJECT_ID"
else
    echo "⚠️  .vercel/project.json을 찾을 수 없습니다."
    read -p "Vercel Organization ID를 입력하세요: " VERCEL_ORG_ID
    read -p "Vercel Project ID를 입력하세요: " VERCEL_PROJECT_ID
fi

cd ..

set_secret "VERCEL_ORG_ID" "$VERCEL_ORG_ID"
set_secret "VERCEL_PROJECT_ID" "$VERCEL_PROJECT_ID"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  4️⃣  Sentry Auth Token (선택)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "ℹ️  Sentry Token은 선택사항입니다. 건너뛰려면 Enter를 누르세요."
echo "   생성하려면:"
echo "   1. https://sentry.io/settings/account/api/auth-tokens/"
echo "   2. 'Create New Token' 클릭"
echo "   3. Scopes: project:read, project:releases, org:read"
echo ""
read -p "Sentry Auth Token (선택): " SENTRY_AUTH_TOKEN

if [ -n "$SENTRY_AUTH_TOKEN" ]; then
    set_secret "SENTRY_AUTH_TOKEN" "$SENTRY_AUTH_TOKEN"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ GitHub Secrets 설정 완료!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "설정된 Secrets:"
gh secret list --repo="$REPO"
echo ""
echo "🚀 다음 단계:"
echo "   1. GitHub Actions 워크플로우가 자동으로 시작됩니다"
echo "   2. 또는 수동 트리거: gh workflow run deploy-production.yml"
echo "   3. 진행 상황 확인: gh run watch"
echo ""
