# GitHub Secrets 설정 가이드

## 🚀 빠른 시작 (자동 설정)

```bash
# 1. 스크립트 실행 (모든 토큰 자동 생성 및 설정)
./scripts/setup-github-secrets.sh

# 2. 설정 확인
./scripts/verify-secrets.sh

# 3. 배포 시작
gh workflow run deploy-production.yml --ref main

# 4. 실시간 모니터링
gh run watch
```

## 📋 필요한 Secrets (5개)

### 1. RAILWAY_TOKEN
**목적**: Railway 백엔드 자동 배포

**자동 생성**:
```bash
railway login
railway tokens create
```

**수동 생성**:
1. https://railway.app/account/tokens
2. "Create New Token" 클릭
3. 이름: "GitHub Actions"
4. 권한: Full Access
5. 토큰 복사

### 2. VERCEL_TOKEN
**목적**: Vercel 프론트엔드 자동 배포

**수동 생성** (자동 생성 불가):
1. https://vercel.com/account/tokens
2. "Create" 버튼 클릭
3. 이름: "GitHub Actions"
4. Scope: "Full Account"
5. Expiration: "No Expiration"
6. 토큰 복사

### 3. VERCEL_ORG_ID
**목적**: Vercel 조직 식별

**자동 추출**:
```bash
cd nextjs-frontend
vercel link  # 프로젝트 연결
cat .vercel/project.json | grep orgId
```

**출력 예시**: `"orgId": "team_xxxxxxxxxxxxxxxxxxxxx"`

### 4. VERCEL_PROJECT_ID
**목적**: Vercel 프로젝트 식별

**자동 추출**:
```bash
cd nextjs-frontend
cat .vercel/project.json | grep projectId
```

**출력 예시**: `"projectId": "prj_xxxxxxxxxxxxxxxxxxxxx"`

### 5. SENTRY_AUTH_TOKEN (선택)
**목적**: Sentry 에러 추적 릴리즈 생성

**수동 생성**:
1. https://sentry.io/settings/account/api/auth-tokens/
2. "Create New Token" 클릭
3. Scopes 선택:
   - `project:read`
   - `project:releases`
   - `org:read`
4. 토큰 복사

## 🛠️ 수동 설정 방법

### GitHub CLI 사용

```bash
# 1. GitHub 로그인
gh auth login

# 2. Secrets 설정
echo "your-railway-token" | gh secret set RAILWAY_TOKEN
echo "your-vercel-token" | gh secret set VERCEL_TOKEN
echo "your-org-id" | gh secret set VERCEL_ORG_ID
echo "your-project-id" | gh secret set VERCEL_PROJECT_ID
echo "your-sentry-token" | gh secret set SENTRY_AUTH_TOKEN  # 선택

# 3. 확인
gh secret list
```

### GitHub Web UI 사용

1. Repository → **Settings** 탭
2. 좌측 메뉴 → **Secrets and variables** → **Actions**
3. **New repository secret** 버튼 클릭
4. Name과 Value 입력 후 **Add secret**
5. 5개 모두 반복

## ✅ 설정 확인

### 1. Secrets 목록 확인
```bash
gh secret list
```

**예상 출력**:
```
RAILWAY_TOKEN          Updated 2026-02-08
VERCEL_TOKEN           Updated 2026-02-08
VERCEL_ORG_ID          Updated 2026-02-08
VERCEL_PROJECT_ID      Updated 2026-02-08
SENTRY_AUTH_TOKEN      Updated 2026-02-08
```

### 2. 자동 검증 스크립트
```bash
./scripts/verify-secrets.sh
```

**성공 시 출력**:
```
✅ RAILWAY_TOKEN - 설정됨
✅ VERCEL_TOKEN - 설정됨
✅ VERCEL_ORG_ID - 설정됨
✅ VERCEL_PROJECT_ID - 설정됨
✅ SENTRY_AUTH_TOKEN - 설정됨

✅ 모든 필수 Secrets가 올바르게 설정되었습니다!
```

## 🚀 배포 실행

### 자동 배포 (Secrets 설정 후 즉시 실행)
```bash
# Push하면 자동으로 Deploy Production 워크플로우 실행
git push origin main
```

### 수동 배포 트리거
```bash
# 전체 배포 (백엔드 + 프론트엔드 + 마이그레이션)
gh workflow run deploy-production.yml \
  --ref main \
  -f deploy_backend=true \
  -f deploy_frontend=true \
  -f run_migrations=true

# 백엔드만 배포
gh workflow run deploy-production.yml \
  --ref main \
  -f deploy_backend=true \
  -f deploy_frontend=false

# 프론트엔드만 배포
gh workflow run deploy-production.yml \
  --ref main \
  -f deploy_backend=false \
  -f deploy_frontend=true
```

### 실시간 모니터링
```bash
# 현재 실행 중인 워크플로우 관찰
gh run watch

# 최근 워크플로우 목록
gh run list --limit 10

# 특정 워크플로우 로그 보기
gh run view <run-id> --log

# 실패한 워크플로우만 보기
gh run list --status failure
```

## 🔍 문제 해결

### 문제 1: `gh` 명령어를 찾을 수 없음
```bash
# macOS
brew install gh

# GitHub 로그인
gh auth login
```

### 문제 2: Railway CLI를 찾을 수 없음
```bash
# macOS
brew install railway

# Railway 로그인
railway login
```

### 문제 3: Vercel CLI를 찾을 수 없음
```bash
# npm으로 설치
npm install -g vercel

# Vercel 로그인
vercel login
```

### 문제 4: Secrets가 설정되었는데도 배포 실패
```bash
# 1. Secrets 재확인
gh secret list

# 2. 워크플로우 재실행
gh run rerun <run-id>

# 3. 특정 실패 단계 로그 확인
gh run view <run-id> --log-failed
```

### 문제 5: VERCEL_ORG_ID를 찾을 수 없음
```bash
# Vercel 프로젝트 재연결
cd nextjs-frontend
rm -rf .vercel
vercel link

# .vercel/project.json 확인
cat .vercel/project.json
```

## 📊 배포 진행 상황 확인

### GitHub Actions 웹 대시보드
- 전체: https://github.com/humanist96/apt-insights/actions
- Frontend CI: https://github.com/humanist96/apt-insights/actions/workflows/frontend-ci.yml
- Backend CI: https://github.com/humanist96/apt-insights/actions/workflows/backend-ci.yml
- Deploy: https://github.com/humanist96/apt-insights/actions/workflows/deploy-production.yml

### CLI로 상태 확인
```bash
# 실시간 상태 (자동 새로고침)
watch -n 5 'gh run list --limit 5'

# JSON 형식으로 상세 정보
gh run list --json status,conclusion,name,createdAt --limit 5
```

## 🎯 성공 기준

배포가 성공하면 다음을 확인할 수 있습니다:

1. **GitHub Actions**: 모든 워크플로우 ✅
2. **Railway 백엔드**: https://your-backend.railway.app/health
3. **Vercel 프론트엔드**: https://your-domain.vercel.app
4. **Sentry 대시보드**: 에러 추적 활성화

## 📞 도움말

**자동화 스크립트 문제**:
```bash
# 로그 확인
./scripts/setup-github-secrets.sh 2>&1 | tee setup.log
```

**수동 설정 권장**:
- 자동화 스크립트가 실패하면 수동으로 설정 (GitHub Web UI 사용)
- 각 토큰을 개별적으로 생성하고 복사/붙여넣기

**추가 문서**:
- [DEPLOYMENT_SUCCESS.md](DEPLOYMENT_SUCCESS.md) - 전체 배포 가이드
- [PRODUCTION_READY.md](PRODUCTION_READY.md) - 프로덕션 체크리스트
- [RUNBOOK.md](RUNBOOK.md) - 운영 가이드

---

**작성일**: 2026-02-08
**버전**: 1.0
**상태**: ✅ Ready for use
