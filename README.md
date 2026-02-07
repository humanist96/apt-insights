# 🏠 아파트 실거래가 인사이트 플랫폼

> 한국 부동산 시장의 데이터 기반 의사결정을 위한 분석 플랫폼

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 개요

국토교통부 공공데이터 API를 활용하여 아파트 실거래가 데이터를 수집, 분석, 시각화하는 웹 기반 플랫폼입니다.

### 주요 기능

- 🔍 **실시간 데이터 조회**: 국토교통부 4개 API 통합 (매매, 전월세, 분양권 등)
- 📊 **25+ 분석 기능**: 가격 추이, 지역별 비교, 갭투자 분석, 급매물 탐지
- 📈 **인터랙티브 차트**: Plotly 기반 동적 시각화
- 🤖 **AI 인사이트**: Google Gemini 기반 자연어 요약
- 🎯 **배치 수집**: 대량 데이터 자동 수집 및 리포트 생성

### 지원 데이터

| API | 설명 | 모듈 |
|-----|------|------|
| 분양권전매 | 아파트 분양권 거래 | `api_01/` |
| 아파트 매매 | 아파트 매매 거래 | `api_02/` |
| 매매 상세 | 아파트 매매 상세 정보 | `api_03/` |
| 아파트 전월세 | 전세/월세 거래 | `api_04/` |

### ⚡ 최신 아키텍처 (2026-02)

**모듈화된 Analyzer**: 23개 분석 함수를 6개 전문 모듈로 분리
```
backend/analyzer/
├── basic_stats.py        # 기본 통계 (2 functions)
├── segmentation.py       # 세분화 분석 (6 functions)
├── investment.py         # 투자 분석 (3 functions) - 전세가율, 갭투자
├── premium_analysis.py   # 프리미엄 분석 (4 functions) - 평당가, 층수
├── market_signals.py     # 시장 신호 (8 functions) - 월세/전세, 추세
└── utils.py              # 공통 유틸 (10 functions)
```

**주요 개선사항**:
- ✅ **유지보수성 향상**: 평균 모듈 크기 486줄 (기존 2,784줄 대비 83% 감소)
- ✅ **테스트 커버리지**: 166개 테스트, 86.7% 통과율
- ✅ **제로 브레이킹 체인지**: 기존 코드 100% 호환
- ✅ **명확한 책임 분리**: 각 모듈이 특정 분석 영역 담당

자세한 내용: [ANALYZER_ARCHITECTURE.md](docs/ANALYZER_ARCHITECTURE.md)

## 🚀 빠른 시작

### 1. 환경 설정

**Python 3.9 이상 필요**

```bash
# 저장소 클론
git clone https://github.com/your-username/apt-insights.git
cd apt-insights

# 가상환경 생성 (권장)
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt
```

### 2. API 키 설정

1. [공공데이터포털](https://www.data.go.kr/)에서 API 신청
2. `.env.example` 파일을 `.env`로 복사:
   ```bash
   cp .env.example .env
   ```
3. `.env` 파일 편집:
   ```bash
   SERVICE_KEY=your_api_key_here
   ```

> ⚠️ **중요**: `.env` 파일은 절대 Git에 커밋하지 마세요!

### 3. 실행

#### 웹 대시보드 (Streamlit)

```bash
streamlit run frontend/app.py
```

브라우저에서 `http://localhost:8501` 접속

#### 개별 API 테스트

```bash
# 강남구(11680) 2023년 12월 분양권 거래
python api_01/main.py 11680 202312

# 배치 테스트 + 리포트 생성
python api_01/test_runner.py
python api_02/test_runner.py
python api_03/test_runner.py
python api_04/test_runner.py
```

## 📁 프로젝트 구조

```
apt_test/
├── config.py                 # 환경변수 기반 설정
├── common.py                 # XML/JSON 파싱 유틸리티
├── .env                      # 환경변수 (Git 제외)
├── .env.example              # 환경변수 템플릿
├── requirements.txt          # Python 의존성
│
├── api_01/                   # 분양권전매 API
│   ├── api_01_silv_trade.py
│   ├── main.py
│   ├── test_runner.py
│   └── output/               # 테스트 결과 (JSON, MD)
│
├── api_02/                   # 아파트 매매 API
│   ├── api_02_apt_trade.py
│   ├── main.py
│   ├── test_runner.py
│   └── output/
│
├── api_03/                   # 매매 상세 API
│   ├── api_03_apt_trade_dev.py
│   ├── main.py
│   ├── test_runner.py
│   └── output/
│
├── api_04/                   # 전월세 API
│   ├── api_04_apt_rent.py
│   ├── main.py
│   ├── test_runner.py
│   └── output/
│
├── backend/
│   ├── data_loader.py        # JSON 데이터 로더
│   ├── analyzer.py           # 분석 함수 (25+ 함수)
│   └── api_modules/          # API 클라이언트 복사본
│
└── frontend/
    └── app.py                # Streamlit 웹 UI (3,360줄)
```

## 🎯 사용 예시

### 1. 웹 대시보드

```python
# Streamlit 앱 실행 후:
# 1. 사이드바에서 지역, 기간, API 유형 선택
# 2. "데이터 로드" 버튼 클릭
# 3. 분석 탭 선택 (가격 추이, 지역별 분석 등)
```

### 2. Python API 직접 사용

```python
from api_02.api_02_apt_trade import AptTradeAPI

# API 클라이언트 초기화
api = AptTradeAPI()

# 강남구 2023년 12월 매매 데이터 조회
result = api.get_trade_data_parsed('11680', '202312')

# 결과 출력
for item in result['items']:
    print(f"{item['아파트']} {item['전용면적']}㎡ - {item['거래금액']}")
```

### 3. 배치 데이터 수집

```python
from api_01.test_runner import TestRunner

runner = TestRunner()

# 여러 지역 테스트
runner.run_test_case(
    name='서울 강남구',
    lawd_cd='11680',
    deal_ymd='202312',
    description='강남구 분양권 거래'
)

# 리포트 생성 (Markdown)
runner.generate_report()
```

## 📊 분석 기능

### 기본 분석
- 📈 가격 추이 분석 (시계열)
- 🗺️ 지역별 비교
- 📐 면적대별 분석
- 🏢 층별 가격 분석

### 고급 분석
- 💰 갭투자 분석 (매매가 - 전세가)
- 📊 전세가율 계산
- 🔥 급매물 탐지 (평균 대비 -10% 이상)
- 📉 가격 급등/급락 탐지
- 🤖 AI 기반 시장 요약

### 시각화
- 📊 막대 그래프, 선 그래프, 산점도
- 🗺️ 지역별 히트맵
- 📈 박스플롯, 바이올린 플롯
- 🔄 인터랙티브 필터링

## 🛠️ 개발 로드맵

현재 **Phase 0** 진행 중 (상품화 준비 단계)

### ✅ Phase 0: 기술 부채 해결 (완료!)
- [x] API 키 환경변수화
- [x] .env 기반 설정 시스템
- [x] BaseAPIClient 리팩토링
- [x] Logging 시스템 (structlog)
- [x] 테스트 커버리지 86% (목표 40% 초과달성)

### 📅 Phase 1: 기술 기반 강화 (8주)
- [ ] PostgreSQL 마이그레이션
- [ ] API 비동기 처리 + 캐싱
- [ ] analyzer.py 모듈화 (5개 모듈)
- [ ] 테스트 커버리지 80%

### 📅 Phase 2: 프리미엄 기능 (10주)
- [ ] 사용자 인증 (FastAPI + JWT)
- [ ] CSV/PDF 내보내기
- [ ] 포트폴리오 관리
- [ ] 가격 알림
- [ ] 월간 자동 리포트

### 📅 Phase 3: 프로덕션 배포 (6주)
- [ ] Docker 컨테이너화
- [ ] AWS/Railway 배포
- [ ] 모니터링 (Prometheus, Grafana)
- [ ] CI/CD 파이프라인

## 🔒 보안

- ✅ 환경변수 기반 API 키 관리
- ✅ `.gitignore`에 민감 정보 제외
- ⏳ Phase 2: JWT 인증, Rate Limiting
- ⏳ Phase 3: HTTPS, Secrets Manager

자세한 내용은 [SECURITY.md](SECURITY.md) 참조

## 🧪 테스트

```bash
# 단위 테스트 실행 (Phase 0 완료 후)
pytest tests/

# 커버리지 리포트
pytest --cov=. --cov-report=html

# 특정 API 테스트
python api_01/test_runner.py
```

## 📖 문서

- [CLAUDE.md](CLAUDE.md) - 프로젝트 가이드 (Claude Code용)
- [SECURITY.md](SECURITY.md) - 보안 가이드
- [상품화 기획서](docs/commercialization_plan.md) - 6개월 로드맵

## 🐛 문제 해결

### API 호출 오류
```
❌ Error: SERVICE_KEY not configured
```
→ `.env` 파일에 `SERVICE_KEY` 설정 확인

### 데이터 로드 실패
```
❌ No data found in api_*/output/
```
→ 먼저 테스트 러너 실행: `python api_01/test_runner.py`

### Streamlit 실행 오류
```
❌ ModuleNotFoundError: No module named 'streamlit'
```
→ 의존성 재설치: `pip install -r requirements.txt`

## 📄 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

## 🙏 기여

이슈 제보 및 Pull Request 환영합니다!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 연락처

- 프로젝트 링크: [https://github.com/your-username/apt-insights](https://github.com/your-username/apt-insights)
- 이슈: [https://github.com/your-username/apt-insights/issues](https://github.com/your-username/apt-insights/issues)

## 🌟 Star History

도움이 되셨다면 ⭐️ Star를 눌러주세요!

---

**버전**: 0.2.0 (Phase 0 완료)
**최종 업데이트**: 2026-02-07
**상태**: ✅ Phase 0 완료 - Phase 1 준비 중
