# 보안 가이드

## ⚠️ 중요: API 키 관리

### 환경변수 설정 방법

1. `.env.example` 파일을 `.env`로 복사:
```bash
cp .env.example .env
```

2. `.env` 파일에 실제 API 키 입력:
```bash
# .env 파일 편집
SERVICE_KEY=your_actual_api_key_here
```

3. **절대 `.env` 파일을 Git에 커밋하지 마세요!**
   - `.gitignore`에 이미 추가되어 있음
   - 실수로 커밋하면 즉시 API 키를 재발급하세요

### API 키 발급 방법

1. [공공데이터포털](https://www.data.go.kr/) 접속
2. 회원가입 / 로그인
3. 다음 API 신청:
   - 국토교통부 아파트매매 실거래 상세 자료
   - 국토교통부 아파트매매 실거래자료
   - 국토교통부 아파트 전월세 자료
   - 국토교통부 분양권전매 신고 자료
4. 승인 후 (보통 1-2시간) 인증키 확인
5. `.env` 파일에 `SERVICE_KEY` 설정

## 🔒 보안 체크리스트

### Phase 0 (현재)
- [x] API 키를 환경변수로 이동 (.env)
- [x] .gitignore에 .env 추가
- [x] config.py를 pydantic-settings 기반으로 변경
- [ ] Git 저장소 초기화 시 config.py 커밋 전 확인

### Phase 1 (데이터베이스 도입 시)
- [ ] DATABASE_URL에 강력한 비밀번호 사용
- [ ] 프로덕션 환경에서 SECRET_KEY 변경
  ```bash
  # 강력한 시크릿 키 생성
  python3 -c "import secrets; print(secrets.token_urlsafe(32))"
  ```
- [ ] PostgreSQL 접속을 localhost만 허용 (방화벽)
- [ ] SSL/TLS 인증서 설정 (프로덕션)

### Phase 2 (사용자 시스템 도입 시)
- [ ] 비밀번호 해싱 (bcrypt, argon2)
- [ ] JWT 토큰에 짧은 만료 시간 설정 (1시간)
- [ ] Refresh 토큰 구현
- [ ] Rate Limiting 설정 (slowapi)
- [ ] CORS 설정 (허용된 도메인만)
- [ ] SQL Injection 방지 (ORM 사용)
- [ ] XSS 방지 (입력 검증)
- [ ] CSRF 토큰 구현

### Phase 3 (프로덕션 배포 시)
- [ ] HTTPS 필수 (Let's Encrypt)
- [ ] 환경변수를 AWS Secrets Manager 또는 Railway Secrets 사용
- [ ] 정기적인 보안 스캔 (Snyk, Dependabot)
- [ ] 로그에 민감 정보 제외 (API 키, 비밀번호)
- [ ] 백업 암호화
- [ ] DDoS 방어 (CloudFlare)

## 🚨 보안 사고 대응

### API 키 유출 시
1. **즉시 조치**:
   - 공공데이터포털에서 API 키 재발급
   - `.env` 파일 업데이트
   - 서비스 재시작

2. **Git 이력에 커밋된 경우**:
   ```bash
   # BFG Repo-Cleaner 사용 (권장)
   brew install bfg  # macOS
   bfg --replace-text passwords.txt .git
   git reflog expire --expire=now --all
   git gc --prune=now --aggressive

   # Force push (주의: 협업 시 팀원에게 알림 필수)
   git push --force
   ```

3. **GitHub에 푸시된 경우**:
   - GitHub에서 자동 경고 발생 가능
   - API 키 즉시 재발급
   - GitHub Secrets 스캔 활성화

### 데이터베이스 침해 시
1. 서비스 즉시 중단
2. 데이터베이스 접속 로그 확인
3. 모든 사용자 비밀번호 초기화 강제
4. 보안 패치 적용
5. 사용자에게 공지

## 📚 참고 자료

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Pydantic Settings 문서](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Python Secrets Management](https://docs.python.org/3/library/secrets.html)

## 🔍 정기 보안 점검

**매월 1일**:
- [ ] 의존성 업데이트 (pip list --outdated)
- [ ] 보안 취약점 스캔 (pip-audit)
- [ ] 로그 리뷰 (비정상 접속 시도)
- [ ] 백업 테스트 (복구 가능성 확인)

**매 분기**:
- [ ] 침투 테스트
- [ ] 코드 보안 리뷰
- [ ] 사용자 권한 감사

---

**최종 업데이트**: 2026-02-07
**담당자**: 개발팀
**문의**: security@apt-insights.kr (예시)
