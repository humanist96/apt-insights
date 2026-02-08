#!/bin/bash

# GitHub Secrets Verification Script
# GitHub Secrets가 올바르게 설정되었는지 확인합니다.

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  GitHub Secrets 검증 스크립트"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Required secrets
REQUIRED_SECRETS=(
    "RAILWAY_TOKEN"
    "VERCEL_TOKEN"
    "VERCEL_ORG_ID"
    "VERCEL_PROJECT_ID"
)

OPTIONAL_SECRETS=(
    "SENTRY_AUTH_TOKEN"
)

# Get repository info
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "")

if [ -z "$REPO" ]; then
    echo "❌ GitHub repository를 찾을 수 없습니다."
    echo "   현재 디렉토리가 git repository인지 확인하세요."
    exit 1
fi

echo "📁 Repository: $REPO"
echo ""

# Get all secrets
SECRETS=$(gh secret list --repo="$REPO" 2>/dev/null || echo "")

if [ -z "$SECRETS" ]; then
    echo "❌ Secrets를 가져올 수 없습니다."
    echo "   gh CLI가 올바르게 인증되었는지 확인하세요: gh auth status"
    exit 1
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  필수 Secrets 검증"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

MISSING_COUNT=0

for SECRET in "${REQUIRED_SECRETS[@]}"; do
    if echo "$SECRETS" | grep -q "^$SECRET"; then
        echo "✅ $SECRET - 설정됨"
    else
        echo "❌ $SECRET - 누락"
        ((MISSING_COUNT++))
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  선택 Secrets 검증"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

for SECRET in "${OPTIONAL_SECRETS[@]}"; do
    if echo "$SECRETS" | grep -q "^$SECRET"; then
        echo "✅ $SECRET - 설정됨"
    else
        echo "⚠️  $SECRET - 미설정 (선택사항)"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  검증 결과"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ $MISSING_COUNT -eq 0 ]; then
    echo "✅ 모든 필수 Secrets가 올바르게 설정되었습니다!"
    echo ""
    echo "🚀 다음 단계:"
    echo "   1. GitHub Actions 워크플로우 트리거:"
    echo "      gh workflow run deploy-production.yml --ref main"
    echo ""
    echo "   2. 진행 상황 실시간 모니터링:"
    echo "      gh run watch"
    echo ""
    echo "   3. 최근 워크플로우 실행 확인:"
    echo "      gh run list --limit 5"
    echo ""
else
    echo "❌ $MISSING_COUNT 개의 필수 Secrets가 누락되었습니다."
    echo ""
    echo "📝 누락된 Secrets 설정 방법:"
    echo "   ./scripts/setup-github-secrets.sh"
    echo ""
    exit 1
fi
