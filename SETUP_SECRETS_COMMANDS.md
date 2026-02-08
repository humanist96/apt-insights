# GitHub Secrets 설정 명령어 모음

## ⚠️ 중요 알림

자동화 스크립트는 **대화형 터미널**에서만 작동합니다.
아래 명령어를 **순서대로** 복사하여 터미널에서 실행하세요.

---

## 📋 사전 준비 (필수)

### 1. GitHub CLI 설치 및 로그인
```bash
# GitHub CLI 설치 (없다면)
brew install gh

# GitHub 로그인 (브라우저가 열림)
gh auth login

# 로그인 확인
gh auth status
```

### 2. Railway CLI 설치 및 로그인
```bash
# Railway CLI 설치
brew install railway

# Railway 로그인 (브라우저가 열림)
railway login

# 로그인 확인
railway whoami
```

### 3. Vercel CLI 설치 및 로그인
```bash
# Vercel CLI 설치
npm install -g vercel

# Vercel 로그인 (브라우저가 열림)
vercel login

# 로그인 확인
vercel whoami
```

---

## 🔑 Secret 1: RAILWAY_TOKEN

### 방법 1: CLI로 토큰 생성 (권장)
```bash
# Railway 토큰 생성 (출력값 복사하세요)
railway tokens create
```

### 방법 2: 웹에서 생성
1. https://railway.app/account/tokens
2. "Create New Token" → 이름: "GitHub Actions" → Full Access
3. 토큰 복사

### GitHub Secret 설정
```bash
# 복사한 토큰을 여기 붙여넣고 실행
gh secret set RAILWAY_TOKEN
# 프롬프트에서 토큰 입력 → Enter
```

---

## 🔑 Secret 2: VERCEL_TOKEN

### 웹에서 생성 (자동 생성 불가)
1. https://vercel.com/account/tokens
2. "Create" 버튼 클릭
3. Name: "GitHub Actions"
4. Scope: "Full Account"
5. Expiration: "No Expiration"
6. "Create Token" → 토큰 복사

### GitHub Secret 설정
```bash
# 복사한 토큰을 여기 붙여넣고 실행
gh secret set VERCEL_TOKEN
# 프롬프트에서 토큰 입력 → Enter
```

---

## 🔑 Secret 3-4: VERCEL_ORG_ID, VERCEL_PROJECT_ID

### 프로젝트 연결 (처음 한 번만)
```bash
cd nextjs-frontend
vercel link
# 질문에 답변:
# - Link to existing project? → Yes
# - What's your project's name? → apt-insights (또는 직접 입력)
# - Which directory? → nextjs-frontend

cd ..
```

### ID 추출
```bash
# Organization ID 추출
VERCEL_ORG_ID=$(cat nextjs-frontend/.vercel/project.json | grep -o '"orgId": "[^"]*"' | cut -d'"' -f4)
echo "Organization ID: $VERCEL_ORG_ID"

# Project ID 추출
VERCEL_PROJECT_ID=$(cat nextjs-frontend/.vercel/project.json | grep -o '"projectId": "[^"]*"' | cut -d'"' -f4)
echo "Project ID: $VERCEL_PROJECT_ID"
```

### GitHub Secret 설정
```bash
# Organization ID 설정
echo "$VERCEL_ORG_ID" | gh secret set VERCEL_ORG_ID

# Project ID 설정
echo "$VERCEL_PROJECT_ID" | gh secret set VERCEL_PROJECT_ID
```

---

## 🔑 Secret 5: SENTRY_AUTH_TOKEN (선택)

### 웹에서 생성
1. https://sentry.io/settings/account/api/auth-tokens/
2. "Create New Token" 클릭
3. Scopes 선택:
   - `project:read` ✅
   - `project:releases` ✅
   - `org:read` ✅
4. "Create Token" → 토큰 복사

### GitHub Secret 설정
```bash
# 복사한 토큰을 여기 붙여넣고 실행
gh secret set SENTRY_AUTH_TOKEN
# 프롬프트에서 토큰 입력 → Enter
```

---

## ✅ 설정 확인

### 모든 Secrets 확인
```bash
gh secret list
```

**예상 출력**:
```
RAILWAY_TOKEN          Updated 2026-02-08
VERCEL_TOKEN           Updated 2026-02-08
VERCEL_ORG_ID          Updated 2026-02-08
VERCEL_PROJECT_ID      Updated 2026-02-08
SENTRY_AUTH_TOKEN      Updated 2026-02-08 (선택)
```

### 자동 검증
```bash
./scripts/verify-secrets.sh
```

**성공 메시지**:
```
✅ 모든 필수 Secrets가 올바르게 설정되었습니다!
```

---

## 🚀 배포 실행

### 자동 배포 (Push 시 자동 실행)
```bash
# 현재까지의 모든 변경사항 커밋 및 푸시
git add .
git commit -m "docs: add GitHub Secrets setup guides and automation scripts"
git push origin main
```

### 수동 배포 트리거
```bash
# 전체 배포 (백엔드 + 프론트엔드 + DB 마이그레이션)
gh workflow run deploy-production.yml \
  --ref main \
  -f deploy_backend=true \
  -f deploy_frontend=true \
  -f run_migrations=true
```

### 실시간 모니터링
```bash
# 워크플로우 실행 관찰 (자동 새로고침)
gh run watch

# 또는 상태만 확인
gh run list --limit 5
```

---

## 🔍 문제 해결

### Railway 로그인 안됨
```bash
# 로그아웃 후 재로그인
railway logout
railway login
railway whoami
```

### Vercel 프로젝트 연결 안됨
```bash
# .vercel 폴더 삭제 후 재연결
cd nextjs-frontend
rm -rf .vercel
vercel link
cd ..
```

### Secrets 설정 안됨
```bash
# GitHub 인증 재확인
gh auth status

# 권한 재부여
gh auth refresh -h github.com -s admin:org,repo,workflow
```

### .vercel/project.json 없음
```bash
# 파일 존재 확인
ls -la nextjs-frontend/.vercel/

# 없다면 vercel link 다시 실행
cd nextjs-frontend && vercel link && cd ..
```

---

## 📊 전체 프로세스 요약

```bash
# === 1단계: CLI 도구 설치 및 로그인 (5분) ===
brew install gh railway
npm install -g vercel

gh auth login
railway login
vercel login

# === 2단계: 토큰 생성 및 Secret 설정 (10분) ===

# RAILWAY_TOKEN
railway tokens create
gh secret set RAILWAY_TOKEN
# (토큰 붙여넣기)

# VERCEL_TOKEN (웹에서 생성)
# https://vercel.com/account/tokens → Create → Full Account
gh secret set VERCEL_TOKEN
# (토큰 붙여넣기)

# VERCEL_ORG_ID, VERCEL_PROJECT_ID
cd nextjs-frontend && vercel link && cd ..
VERCEL_ORG_ID=$(cat nextjs-frontend/.vercel/project.json | grep -o '"orgId": "[^"]*"' | cut -d'"' -f4)
VERCEL_PROJECT_ID=$(cat nextjs-frontend/.vercel/project.json | grep -o '"projectId": "[^"]*"' | cut -d'"' -f4)
echo "$VERCEL_ORG_ID" | gh secret set VERCEL_ORG_ID
echo "$VERCEL_PROJECT_ID" | gh secret set VERCEL_PROJECT_ID

# SENTRY_AUTH_TOKEN (선택)
# https://sentry.io/settings/account/api/auth-tokens/ → Create
gh secret set SENTRY_AUTH_TOKEN
# (토큰 붙여넣기)

# === 3단계: 검증 (1분) ===
gh secret list
./scripts/verify-secrets.sh

# === 4단계: 배포 실행 (자동, 15분) ===
gh workflow run deploy-production.yml --ref main -f deploy_backend=true -f deploy_frontend=true -f run_migrations=true
gh run watch
```

---

## 🎯 다음 단계

Secrets 설정이 완료되면:

1. ✅ GitHub Actions 자동 실행
2. ✅ Backend → Railway 배포
3. ✅ Frontend → Vercel 배포
4. ✅ Database 마이그레이션
5. ✅ Smoke 테스트
6. ✅ 배포 완료!

**예상 총 소요 시간**: 20-30분

---

**작성일**: 2026-02-08
**버전**: 1.0
**상태**: ✅ 바로 사용 가능
