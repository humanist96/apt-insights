"""
Streamlit 프론트엔드 앱
아파트 실거래가 데이터 분석 및 시각화
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
import calendar
import os
import importlib

# 프로젝트 루트를 path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.data_loader import load_and_process_data, normalize_data
from backend import analyzer as analyzer_module
from batch_collector import BatchCollector
from datetime import datetime, timedelta
import time

try:
    from streamlit_plotly_events import plotly_events
    HAS_PLOTLY_EVENTS = True
except Exception:
    HAS_PLOTLY_EVENTS = False

# analyzer 모듈 최신화 (Streamlit 재실행 없이도 새 함수 반영)
if not hasattr(analyzer_module, "summarize_period"):
    analyzer_module = importlib.reload(analyzer_module)

_required_analyzer = [
    "calculate_basic_stats",
    "calculate_price_trend",
    "analyze_by_area",
    "analyze_by_floor",
    "analyze_by_build_year",
    "analyze_by_region",
    "calculate_price_per_area",
    "analyze_price_per_area_trend",
    "analyze_by_apartment",
    "get_apartment_detail",
    "calculate_jeonse_ratio",
    "analyze_gap_investment",
    "detect_bargain_sales",
    "analyze_floor_premium",
    "analyze_building_age_premium",
    "analyze_rent_vs_jeonse",
    "analyze_dealing_type",
    "analyze_buyer_seller_type",
    "analyze_cancelled_deals",
    "summarize_period",
    "build_baseline_summary",
    "compare_periods",
    "detect_market_signals",
]

missing = [name for name in _required_analyzer if not hasattr(analyzer_module, name)]
if missing:
    raise ImportError(
        f"backend.analyzer에 필요한 함수가 없습니다: {', '.join(missing)}"
    )

calculate_basic_stats = analyzer_module.calculate_basic_stats
calculate_price_trend = analyzer_module.calculate_price_trend
analyze_by_area = analyzer_module.analyze_by_area
analyze_by_floor = analyzer_module.analyze_by_floor
analyze_by_build_year = analyzer_module.analyze_by_build_year
analyze_by_region = analyzer_module.analyze_by_region
calculate_price_per_area = analyzer_module.calculate_price_per_area
analyze_price_per_area_trend = analyzer_module.analyze_price_per_area_trend
analyze_by_apartment = analyzer_module.analyze_by_apartment
get_apartment_detail = analyzer_module.get_apartment_detail
calculate_jeonse_ratio = analyzer_module.calculate_jeonse_ratio
analyze_gap_investment = analyzer_module.analyze_gap_investment
detect_bargain_sales = analyzer_module.detect_bargain_sales
analyze_floor_premium = analyzer_module.analyze_floor_premium
analyze_building_age_premium = analyzer_module.analyze_building_age_premium
analyze_rent_vs_jeonse = analyzer_module.analyze_rent_vs_jeonse
analyze_dealing_type = analyzer_module.analyze_dealing_type
analyze_buyer_seller_type = analyzer_module.analyze_buyer_seller_type
analyze_cancelled_deals = analyzer_module.analyze_cancelled_deals
summarize_period = analyzer_module.summarize_period
build_baseline_summary = analyzer_module.build_baseline_summary
compare_periods = analyzer_module.compare_periods
detect_market_signals = analyzer_module.detect_market_signals

# API 클래스 import
from api_01.api_01_silv_trade import SilvTradeAPI
from api_02.api_02_apt_trade import AptTradeAPI
from api_03.api_03_apt_trade_dev import AptTradeDevAPI
from api_04.api_04_apt_rent import AptRentAPI

# 페이지 설정
st.set_page_config(page_title="아파트 실거래가 분석", page_icon="🏠", layout="wide")

# 사이드바
st.sidebar.title("설정")

# 데이터 소스 선택
data_source = st.sidebar.radio(
    "데이터 소스",
    ["Output JSON 파일", "실시간 API 호출"],
    help="Output JSON 파일: 저장된 테스트 결과 사용\n실시간 API 호출: API를 직접 호출하여 데이터 가져오기",
)

# 지역 필터
region_filter = st.sidebar.text_input(
    "지역 필터 (선택사항)",
    placeholder="예: 수원, 종로구, 강남구",
    help="지역명을 입력하면 해당 지역 데이터만 표시됩니다",
)

# 실시간 API 호출 설정
realtime_api_type = None
realtime_lawd_cd = None
realtime_deal_ymd = None
realtime_num_of_rows = 100

if data_source == "실시간 API 호출":
    st.sidebar.markdown("---")
    st.sidebar.subheader("실시간 API 설정")

    realtime_api_type = st.sidebar.selectbox(
        "API 타입",
        ["API 01: 분양권전매", "API 02: 매매", "API 03: 매매상세", "API 04: 전월세"],
        key="realtime_api_type",
    )

    realtime_lawd_cd = st.sidebar.text_input(
        "법정동코드 (5자리)",
        value="11680",
        help="예: 11680 (강남구), 11110 (종로구), 41117 (수원 영통구)",
        key="realtime_lawd_cd",
    )

    # 주요 지역코드 참고
    with st.sidebar.expander("📍 전국 주요 지역코드", expanded=False):
        st.markdown("""
        ### 서울특별시 (11xxx)
        - 종로구: `11110` | 중구: `11140` | 용산구: `11170`
        - 성동구: `11200` | 광진구: `11215` | 동대문구: `11230`
        - 중랑구: `11260` | 성북구: `11290` | 강북구: `11305`
        - 도봉구: `11320` | 노원구: `11350` | 은평구: `11380`
        - 서대문구: `11410` | 마포구: `11440` | 양천구: `11470`
        - 강서구: `11500` | 구로구: `11530` | 금천구: `11545`
        - 영등포구: `11560` | 동작구: `11590` | 관악구: `11620`
        - **서초구: `11650`** | **강남구: `11680`** | **송파구: `11710`** | 강동구: `11740`

        ### 부산광역시 (26xxx)
        - 중구: `26110` | 서구: `26140` | 동구: `26170` | 영도구: `26200`
        - 부산진구: `26230` | 동래구: `26260` | 남구: `26290` | 북구: `26320`
        - **해운대구: `26350`** | 사하구: `26380` | 금정구: `26410` | 강서구: `26440`
        - 연제구: `26470` | 수영구: `26500` | 사상구: `26530` | 기장군: `26710`

        ### 대구광역시 (27xxx)
        - 중구: `27110` | 동구: `27140` | 서구: `27170` | 남구: `27200`
        - 북구: `27230` | **수성구: `27260`** | 달서구: `27290` | 달성군: `27710`

        ### 인천광역시 (28xxx)
        - 중구: `28110` | 동구: `28140` | 미추홀구: `28177` | **연수구: `28185`**
        - **남동구: `28200`** | 부평구: `28237` | 계양구: `28245` | 서구: `28260`
        - 강화군: `28710` | 옹진군: `28720`

        ### 광주광역시 (29xxx)
        - 동구: `29110` | 서구: `29140` | 남구: `29155`
        - 북구: `29170` | 광산구: `29200`

        ### 대전광역시 (30xxx)
        - 동구: `30110` | 중구: `30140` | 서구: `30170`
        - 유성구: `30200` | 대덕구: `30230`

        ### 울산광역시 (31xxx)
        - 중구: `31110` | 남구: `31140` | 동구: `31170`
        - 북구: `31200` | 울주군: `31710`

        ### 세종특별자치시 (36xxx)
        - 세종시: `36110`

        ### 경기도 주요 시 (41xxx)
        **수원시**
        - 장안구: `41111` | **권선구: `41113`** | 팔달구: `41115` | **영통구: `41117`**

        **성남시**
        - 수정구: `41131` | 중원구: `41133` | **분당구: `41135`**

        **고양시**
        - 덕양구: `41281` | 일산동구: `41285` | **일산서구: `41287`**

        **용인시**
        - 처인구: `41461` | **기흥구: `41463`** | **수지구: `41465`**

        **안산시**
        - 상록구: `41271` | 단원구: `41273`

        **안양시**
        - 만안구: `41171` | 동안구: `41173`

        **기타 주요 시**
        - 의정부시: `41150` | 부천시: `41190` | 광명시: `41210`
        - 평택시: `41220` | 과천시: `41290` | 구리시: `41310`
        - 남양주시: `41360` | 파주시: `41480` | **화성시: `41590`**
        - 광주시: `41610` | 하남시: `41450` | 김포시: `41570`

        ### 강원특별자치도 (51xxx)
        - 춘천시: `51110` | 원주시: `51130` | 강릉시: `51150`

        ### 충청북도 (43xxx)
        - 청주시 상당구: `43111` | 청주시 서원구: `43112`
        - 청주시 흥덕구: `43113` | 청주시 청원구: `43114`
        - 충주시: `43130` | 제천시: `43150`

        ### 충청남도 (44xxx)
        - 천안시 동남구: `44131` | 천안시 서북구: `44133`
        - 공주시: `44150` | 아산시: `44200`

        ### 전북특별자치도 (52xxx)
        - 전주시 완산구: `52111` | 전주시 덕진구: `52113`
        - 군산시: `52130` | 익산시: `52140`

        ### 전라남도 (46xxx)
        - 목포시: `46110` | 여수시: `46130` | 순천시: `46150`

        ### 경상북도 (47xxx)
        - 포항시 남구: `47111` | 포항시 북구: `47113`
        - 경주시: `47130` | 구미시: `47190`

        ### 경상남도 (48xxx)
        - 창원시 의창구: `48121` | 창원시 성산구: `48123`
        - 창원시 마산합포구: `48125` | 창원시 마산회원구: `48127`
        - 창원시 진해구: `48129` | 진주시: `48170`
        - 김해시: `48250` | 양산시: `48330`

        ### 제주특별자치도 (50xxx)
        - 제주시: `50110` | 서귀포시: `50130`

        💡 **볼드체**는 거래량이 많은 주요 지역입니다.
        """)

    # 년월 선택
    current_year = datetime.now().year
    current_month = datetime.now().month

    col_year, col_month = st.sidebar.columns(2)
    with col_year:
        realtime_year = st.number_input(
            "년도",
            min_value=2006,
            max_value=current_year,
            value=current_year,
            key="realtime_year",
        )
    with col_month:
        realtime_month = st.number_input(
            "월", min_value=1, max_value=12, value=current_month, key="realtime_month"
        )

    realtime_deal_ymd = f"{realtime_year}{realtime_month:02d}"

    realtime_num_of_rows = st.sidebar.number_input(
        "최대 조회 건수",
        min_value=10,
        max_value=1000,
        value=100,
        step=10,
        help="API 호출당 최대 조회 건수",
        key="realtime_num_rows",
    )

# 메인 영역
st.title("🏠 아파트 실거래가 데이터 분석")

# 데이터 로드 함수들


def get_latest_file_timestamp(base_path: Path) -> float:
    """모든 JSON 파일 중 가장 최근 수정 시간 반환"""
    latest_time = 0.0
    for api_dir in base_path.glob("api_*/output"):
        for json_file in api_dir.glob("*test_results*.json"):
            mtime = json_file.stat().st_mtime
            if mtime > latest_time:
                latest_time = mtime
    return latest_time


@st.cache_data
def load_data_from_files(region_filter=None, cache_key=None):
    """
    실제 output 디렉토리의 JSON 파일에서만 데이터를 로드합니다.
    목업 데이터나 샘플 데이터를 사용하지 않습니다.

    Args:
        region_filter: 지역 필터
        cache_key: 캐시 키 (파일 타임스탬프 포함)
    """
    try:
        items, debug_info = load_and_process_data(
            base_path=project_root,
            region_filter=region_filter if region_filter else None,
            remove_dup=True,
            debug=True,  # 디버깅 정보 활성화
        )
        return items, debug_info
    except Exception as e:
        import traceback

        error_trace = traceback.format_exc()
        st.error(f"데이터 로드 실패: {e}")
        st.code(error_trace, language="python")
        return [], None


def load_data_from_api(
    api_type: str, lawd_cd: str, deal_ymd: str, num_of_rows: int = 100
):
    """
    실시간 API 호출로 데이터를 로드합니다.

    Args:
        api_type: API 타입 문자열 (예: "API 01: 분양권전매")
        lawd_cd: 법정동코드 (5자리)
        deal_ymd: 계약년월 (YYYYMM)
        num_of_rows: 최대 조회 건수

    Returns:
        (items, debug_info) 튜플
    """
    # API 타입에 따라 적절한 클래스 선택
    api_map = {
        "API 01: 분양권전매": ("api_01", SilvTradeAPI),
        "API 02: 매매": ("api_02", AptTradeAPI),
        "API 03: 매매상세": ("api_03", AptTradeDevAPI),
        "API 04: 전월세": ("api_04", AptRentAPI),
    }

    api_key, api_class = api_map.get(api_type, ("api_02", AptTradeAPI))

    debug_info = {
        "successful_files": [],
        "failed_files": [],
        "total_files": 1,
        "total_items": 0,
        "errors": [],
        "api_call": {
            "api_type": api_type,
            "lawd_cd": lawd_cd,
            "deal_ymd": deal_ymd,
            "num_of_rows": num_of_rows,
        },
    }

    try:
        # API 인스턴스 생성 및 호출
        api = api_class()
        result = api.get_trade_data_parsed(
            lawd_cd=lawd_cd, deal_ymd=deal_ymd, num_of_rows=num_of_rows, page_no=1
        )

        if result.get("error"):
            debug_info["errors"].append(
                {
                    "file": f"API Call ({api_type})",
                    "error": result.get("message", "Unknown error"),
                    "traceback": None,
                }
            )
            debug_info["failed_files"].append(
                {
                    "file": f"API Call ({api_type})",
                    "error": result.get("message", "Unknown error"),
                    "error_type": "APIError",
                }
            )
            return [], debug_info

        items = result.get("items", [])

        # 각 item에 API 타입 정보 추가
        for item in items:
            item["_api_type"] = api_key
            item["_source_file"] = f"realtime_api_{api_key}"

        # 데이터 정규화
        items = normalize_data(items)

        debug_info["total_items"] = len(items)
        debug_info["successful_files"].append(
            {"file": f"API Call ({api_type})", "size_mb": 0, "items_count": len(items)}
        )

        return items, debug_info

    except Exception as e:
        import traceback

        error_trace = traceback.format_exc()
        debug_info["errors"].append(
            {
                "file": f"API Call ({api_type})",
                "error": str(e),
                "traceback": error_trace,
            }
        )
        debug_info["failed_files"].append(
            {
                "file": f"API Call ({api_type})",
                "error": str(e),
                "error_type": type(e).__name__,
            }
        )
        return [], debug_info


# 수동 이벤트 맵 (필요 시 하드코딩)
MANUAL_EVENT_MAP = [
    # {
    #     "start": datetime(2024, 1, 1),
    #     "end": datetime(2024, 1, 31),
    #     "title": "예시 이벤트",
    #     "summary": "이벤트 설명을 여기에 입력하세요.",
    # },
]


def month_bounds(year_month: str):
    year, month = map(int, year_month.split("-"))
    start = datetime(year, month, 1)
    last_day = calendar.monthrange(year, month)[1]
    end = datetime(year, month, last_day)
    return start, end


def create_monthly_trend_chart(
    trend_df: pd.DataFrame,
    highlight_range: tuple = None,
    chart_title: str = "월별 가격 추이",
    height: int = 500,
    show_hover_unified: bool = True
) -> go.Figure:
    """
    월별 가격 추이 차트 생성

    Args:
        trend_df: 월별 집계 데이터 (year_month, avg_price, median_price, count)
        highlight_range: 강조할 기간 튜플 (start_month, end_month) 예: ("2023-01", "2023-06")
        chart_title: 차트 제목
        height: 차트 높이 (픽셀)
        show_hover_unified: hover 통합 모드 사용 여부

    Returns:
        Plotly Figure 객체
    """
    # 데이터 정제
    df = trend_df.copy()
    df["avg_price"] = pd.to_numeric(df["avg_price"], errors="coerce")
    df["median_price"] = pd.to_numeric(df["median_price"], errors="coerce")
    df = df.dropna(subset=["avg_price", "median_price"])

    # Figure 생성
    fig = go.Figure()

    # 기간 하이라이트 (먼저 추가해서 배경에 표시)
    if highlight_range:
        start_month, end_month = highlight_range
        # 선택 기간 강조 (반투명 노란색 사각형)
        fig.add_vrect(
            x0=start_month,
            x1=end_month,
            fillcolor="rgba(255, 215, 0, 0.2)",  # 연한 노란색
            layer="below",
            line_width=2,
            line_color="orange",
            line_dash="dash",
        )

    # 평균가격 라인
    fig.add_trace(go.Scatter(
        x=df["year_month"],
        y=df["avg_price"],
        mode="lines+markers",
        name="평균가격",
        line=dict(color="#1f77b4", width=3),
        hovertemplate="년월=%{x}<br>평균가격=%{y:,.0f}만원<extra></extra>",
    ))

    # 중앙가격 라인
    fig.add_trace(go.Scatter(
        x=df["year_month"],
        y=df["median_price"],
        mode="lines+markers",
        name="중앙가격",
        line=dict(color="#ff7f0e", width=3, dash="dash"),
        hovertemplate="년월=%{x}<br>중앙가격=%{y:,.0f}만원<extra></extra>",
    ))

    # 레이아웃
    fig.update_layout(
        title=chart_title,
        xaxis_title="년월",
        yaxis_title="가격 (만원)",
        height=height,
        hovermode="x unified" if show_hover_unified else "closest",
    )
    fig.update_yaxes(
        tickformat=",.0f",
        exponentformat="none",
        showexponent="none"
    )

    return fig


def match_manual_events(events, start_date: datetime, end_date: datetime):
    matched = []
    for event in events:
        event_start = event.get("start")
        event_end = event.get("end") or event_start
        if not event_start or not event_end:
            continue
        if event_start <= end_date and event_end >= start_date:
            matched.append(event)
    return matched


def format_pct(value):
    if value is None:
        return "N/A"
    return f"{value:+.1f}%"


def build_period_report(summary, baseline, comparison, signals, manual_events):
    if not summary.get("has_data"):
        return "선택한 기간에 거래 데이터가 없습니다."

    start_date = summary["start_date"]
    end_date = summary["end_date"]
    month_count = len(summary.get("months", []))

    lines = [
        f"분석 기간: {start_date:%Y-%m-%d} ~ {end_date:%Y-%m-%d} ({month_count}개월)",
        f"거래건수: {summary['count']:,}건",
        f"가격 요약: 평균 {summary['avg_price']:,.0f}만원 | 중앙 {summary['median_price']:,.0f}만원 | 범위 {summary['min_price']:,.0f}~{summary['max_price']:,.0f}만원",
    ]

    if summary.get("avg_area"):
        lines.append(f"평균 전용면적: {summary['avg_area']:.1f}㎡")
    if summary.get("avg_price_per_area"):
        lines.append(
            f"㎡당 가격: 평균 {summary['avg_price_per_area']:,.1f}만원 | 중앙 {summary['median_price_per_area']:,.1f}만원"
        )

    if comparison.get("has_data"):
        lines.append(
            "직전 동기간 대비: "
            f"평균가격 {format_pct(comparison.get('price_change_pct'))}, "
            f"거래건수 {format_pct(comparison.get('count_change_pct'))}, "
            f"㎡당 가격 {format_pct(comparison.get('ppa_change_pct'))}"
        )
        baseline_start = baseline.get("baseline_start")
        baseline_end = baseline.get("baseline_end")
        if baseline_start and baseline_end:
            lines.append(
                f"기준선 기간: {baseline_start:%Y-%m-%d} ~ {baseline_end:%Y-%m-%d} ({baseline.get('count', 0):,}건)"
            )
    else:
        lines.append("직전 동기간 데이터가 부족하여 기준선 비교 불가.")

    top_regions = summary.get("top_regions") or []
    if top_regions:
        region_text = ", ".join(
            [
                f"{region['region']}({region['count']}건)"
                for region in top_regions[:3]
            ]
        )
        lines.append(f"상위 거래 지역: {region_text}")

    api_mix = summary.get("api_mix") or []
    if api_mix:
        api_text = ", ".join(
            [f"{api['api_type']} {api['count']}건" for api in api_mix]
        )
        lines.append(f"데이터 구성: {api_text}")

    if signals:
        lines.append("이벤트 신호:")
        for signal in signals:
            lines.append(f"- {signal['title']}: {signal['detail']}")
    else:
        lines.append("이벤트 신호: 뚜렷한 급변 신호는 감지되지 않음.")

    if manual_events:
        lines.append("등록된 외부 이벤트:")
        for event in manual_events:
            event_start = event.get("start")
            event_end = event.get("end") or event_start
            date_range = (
                f"{event_start:%Y-%m-%d}"
                if event_start == event_end
                else f"{event_start:%Y-%m-%d}~{event_end:%Y-%m-%d}"
            )
            lines.append(f"- {event.get('title', '이벤트')}: {date_range} | {event.get('summary', '')}")
    else:
        lines.append("등록된 외부 이벤트: 없음 (MANUAL_EVENT_MAP에 추가 가능).")

    return "\n".join(lines)


def build_llm_prompt(summary, baseline, comparison, signals, manual_events):
    if not summary.get("has_data"):
        return ""

    baseline_start = baseline.get("baseline_start")
    baseline_end = baseline.get("baseline_end")
    baseline_range = ""
    if baseline_start and baseline_end:
        baseline_range = f"{baseline_start:%Y-%m-%d} ~ {baseline_end:%Y-%m-%d}"

    signal_lines = []
    for signal in signals or []:
        signal_lines.append(f"- {signal['title']}: {signal['detail']}")

    event_lines = []
    for event in manual_events or []:
        event_start = event.get("start")
        event_end = event.get("end") or event_start
        if event_start and event_end:
            if event_start == event_end:
                date_range = f"{event_start:%Y-%m-%d}"
            else:
                date_range = f"{event_start:%Y-%m-%d}~{event_end:%Y-%m-%d}"
        else:
            date_range = "기간 미상"
        event_lines.append(
            f"- {event.get('title', '이벤트')}: {date_range} | {event.get('summary', '')}"
        )

    prompt = f"""
당신은 부동산 시장 분석가입니다. 아래 요약 데이터를 근거로 기간 내 '이벤트'와 '시장 상황'을 설명하세요.

[분석 기간]
- {summary['start_date']:%Y-%m-%d} ~ {summary['end_date']:%Y-%m-%d}

[거래 데이터 요약]
- 거래건수: {summary['count']}
- 평균/중앙 가격: {summary['avg_price']:.0f} / {summary['median_price']:.0f} (만원)
- 가격 범위: {summary['min_price']:.0f} ~ {summary['max_price']:.0f} (만원)
- 평균 전용면적: {summary['avg_area']:.1f} ㎡
- ㎡당 평균/중앙: {summary['avg_price_per_area']:.1f} / {summary['median_price_per_area']:.1f} (만원)

[직전 동기간 대비]
- 기준선 기간: {baseline_range}
- 평균가격: {format_pct(comparison.get('price_change_pct'))}
- 거래건수: {format_pct(comparison.get('count_change_pct'))}
- ㎡당 가격: {format_pct(comparison.get('ppa_change_pct'))}

[감지된 시장 신호]
{chr(10).join(signal_lines) if signal_lines else "- 감지된 주요 신호 없음"}

[등록된 외부 이벤트]
{chr(10).join(event_lines) if event_lines else "- 등록된 외부 이벤트 없음"}

분석 지침:
1) 한국 부동산 시장의 {summary['start_date']:%Y년 %m월}부터 {summary['end_date']:%Y년 %m월}까지의 주요 이슈를 구글 검색을 통해 조사하세요.
2) 해당 기간의 부동산 정책, 금리 변동, 경제 이벤트, 규제 변화 등을 찾아보세요.
3) 검색 결과와 위 거래 데이터를 결합하여 분석하세요.
4) 한국어로 6~10문장, 두 단락 구성: 첫 단락은 '해당 기간의 주요 이벤트', 두 번째 단락은 '시장 상황 분석'.
5) 검색으로 확인된 사실은 명확히 언급하고, 추측은 '가능성'으로 표현하세요.
6) 출처가 있는 정보는 간략히 인용하세요.
"""
    return prompt.strip()


def generate_gemini_summary(prompt: str, model: str, api_key_override: str = ""):
    if not prompt:
        return "", "요약 프롬프트가 비어 있습니다."

    api_key = api_key_override or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "", "GEMINI_API_KEY 환경변수가 설정되어 있지 않습니다."

    try:
        from google import genai
        from google.genai import types
    except Exception as exc:
        return "", f"google-genai 라이브러리를 불러올 수 없습니다: {exc}"

    def build_config():
        try:
            thinking = types.ThinkingConfig(thinking_level="MINIMAL")
            grounding_tool = types.Tool(google_search=types.GoogleSearch())
            return types.GenerateContentConfig(
                thinking_config=thinking,
                tools=[grounding_tool]
            )
        except Exception:
            try:
                thinking = types.ThinkingConfig(thinking_budget=0)
                grounding_tool = types.Tool(google_search=types.GoogleSearch())
                return types.GenerateContentConfig(
                    thinking_config=thinking,
                    tools=[grounding_tool]
                )
            except Exception:
                try:
                    grounding_tool = types.Tool(google_search=types.GoogleSearch())
                    return types.GenerateContentConfig(tools=[grounding_tool])
                except Exception:
                    return None

    try:
        client = genai.Client(api_key=api_key)
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)],
            ),
        ]
        config = build_config()

        output = []
        call_kwargs = dict(model=model, contents=contents)
        if config is not None:
            call_kwargs["config"] = config
        for chunk in client.models.generate_content_stream(**call_kwargs):
            if chunk.text:
                output.append(chunk.text)
        return "".join(output), ""
    except Exception as exc:
        return "", f"Gemini 호출 실패: {exc}"


def build_trend_df(trend_data: dict):
    if not trend_data:
        return None
    trend_df = pd.DataFrame(
        [
            {
                "year_month": k,
                "avg_price": v["avg_price"],
                "median_price": v["median_price"],
                "count": v["count"],
            }
            for k, v in trend_data.items()
        ]
    )
    return trend_df.sort_values("year_month")


# 데이터 로드 (소스에 따라 분기)
items = []
debug_info = None

if data_source == "Output JSON 파일":
    # 파일 타임스탬프를 캐시 키로 사용하여 파일 변경 시 캐시 무효화
    latest_timestamp = get_latest_file_timestamp(project_root)
    cache_key = f"{region_filter if region_filter else 'all'}_{latest_timestamp}"

    # 실제 JSON 파일에서만 데이터를 로드합니다.
    with st.spinner("output 디렉토리의 JSON 파일에서 데이터를 로드하는 중..."):
        items, debug_info = load_data_from_files(
            region_filter if region_filter else None, cache_key=cache_key
        )

else:  # 실시간 API 호출
    # 입력값 검증
    if (
        not realtime_lawd_cd
        or len(realtime_lawd_cd) != 5
        or not realtime_lawd_cd.isdigit()
    ):
        st.error(
            "❌ 법정동코드는 5자리 숫자여야 합니다. 사이드바에서 올바른 값을 입력해주세요."
        )
        st.stop()

    # API 호출
    with st.spinner(
        f"🔄 실시간 API 호출 중... ({realtime_api_type}, {realtime_lawd_cd}, {realtime_deal_ymd})"
    ):
        items, debug_info = load_data_from_api(
            api_type=realtime_api_type,
            lawd_cd=realtime_lawd_cd,
            deal_ymd=realtime_deal_ymd,
            num_of_rows=realtime_num_of_rows,
        )

    # 지역 필터 적용 (실시간 데이터에도)
    if region_filter and items:
        from backend.data_loader import filter_by_region

        items = filter_by_region(items, region_filter)

# 디버깅 정보 표시
if debug_info:
    # 실시간 API 호출인 경우 호출 정보 표시
    if debug_info.get("api_call"):
        api_call = debug_info["api_call"]
        st.info(
            f"📡 **실시간 API 호출**: {api_call['api_type']} | 지역코드: {api_call['lawd_cd']} | 년월: {api_call['deal_ymd']} | 최대 {api_call['num_of_rows']}건"
        )

    with st.expander("🔍 데이터 로딩 디버깅 정보", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            label = "API 호출 수" if debug_info.get("api_call") else "전체 파일 수"
            st.metric(label, debug_info["total_files"])
        with col2:
            st.metric("성공", len(debug_info["successful_files"]))
        with col3:
            st.metric("실패", len(debug_info["failed_files"]))

        st.metric("총 로드된 데이터 건수", f"{debug_info['total_items']:,}건")

        if debug_info["successful_files"]:
            st.subheader("✅ 성공한 소스 목록")
            success_df = pd.DataFrame(debug_info["successful_files"])
            st.dataframe(success_df, use_container_width=True, hide_index=True)

        if debug_info["failed_files"]:
            st.subheader("❌ 실패한 소스 목록")
            failed_df = pd.DataFrame(debug_info["failed_files"])
            st.dataframe(failed_df, use_container_width=True, hide_index=True)

            # 상세 오류 정보
            with st.expander("상세 오류 정보"):
                for error in debug_info["errors"]:
                    st.error(f"**소스**: `{error['file']}`")
                    st.code(error["error"], language="text")
                    if error.get("traceback"):
                        with st.expander("스택 트레이스"):
                            st.code(error["traceback"], language="python")

# 데이터가 없으면 안내 메시지 표시
if not items:
    if data_source == "실시간 API 호출":
        st.warning(f"⚠️ 해당 조건으로 조회된 데이터가 없습니다.")
        st.info(f"""
        **조회 조건**:
        - API 타입: {realtime_api_type}
        - 법정동코드: {realtime_lawd_cd}
        - 계약년월: {realtime_deal_ymd}

        다른 조건으로 다시 조회해 보세요.
        """)
    else:
        st.error(
            "❌ 로드된 데이터가 없습니다. output 디렉토리에 JSON 파일이 있는지 확인해주세요."
        )
        st.info(
            "데이터를 로드하려면 api_*/output/ 디렉토리에 *test_results*.json 파일이 있어야 합니다."
        )

    # 디버깅 정보가 있으면 표시
    if debug_info and debug_info["failed_files"]:
        st.warning(
            f"⚠️ {len(debug_info['failed_files'])}개 소스에서 오류가 발생했습니다. 위의 디버깅 정보를 확인하세요."
        )

    st.stop()

# 기본 통계 카드
st.subheader("📊 기본 통계")
stats = calculate_basic_stats(items)

# 월별 가격 추이 데이터 (탭 2, 탭 2b 공용)
trend_data_global = calculate_price_trend(items)
trend_df_global = build_trend_df(trend_data_global)
trend_months_global = (
    trend_df_global["year_month"].tolist() if trend_df_global is not None else []
)
trend_analysis_items = [
    item
    for item in items
    if item.get("_deal_amount_numeric") is not None and item.get("_deal_date") is not None
]

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("총 거래건수", f"{stats['total_count']:,}건")

with col2:
    st.metric("평균 거래가격", f"{stats['avg_price']:,.0f}만원")

with col3:
    st.metric("최고 거래가격", f"{stats['max_price']:,.0f}만원")

with col4:
    st.metric("최저 거래가격", f"{stats['min_price']:,.0f}만원")

with col5:
    st.metric("평균 전용면적", f"{stats['avg_area']:.2f}㎡")

# 탭 구성
tab1, tab2, tab2b, tab3, tab4, tab5, tab6, tab6b, tab6c, tab7, tab8, tab9 = st.tabs(
    [
        "지역별 분석",
        "가격 추이",
        "🧭 시기 이벤트 분석",
        "면적별 분석",
        "📊 평당가 분석",
        "🏢 아파트별 분석",
        "💰 전세가율/갭투자",
        "🏠 월세/전세 분석",
        "📈 매매 심층 분석",
        "🔥 급매물/프리미엄",
        "상세 데이터",
        "데이터 수집",
    ]
)

# 탭 1: 지역별 분석
with tab1:
    st.subheader("지역별 통계")

    region_analysis = analyze_by_region(items)
    region_df = pd.DataFrame(region_analysis["data"])

    if not region_df.empty:
        # 지역별 평균가격 막대 그래프
        fig_region = px.bar(
            region_df.sort_values("avg_price", ascending=False).head(20),
            x="region",
            y="avg_price",
            title="지역별 평균 거래가격 (상위 20개)",
            labels={"region": "지역", "avg_price": "평균 거래가격 (만원)"},
            color="avg_price",
            color_continuous_scale="Viridis",
        )
        fig_region.update_layout(xaxis_tickangle=-45, height=500)
        st.plotly_chart(fig_region, use_container_width=True)

        # 지역별 거래건수
        col1, col2 = st.columns(2)

        with col1:
            fig_count = px.bar(
                region_df.sort_values("count", ascending=False).head(15),
                x="region",
                y="count",
                title="지역별 거래건수 (상위 15개)",
                labels={"region": "지역", "count": "거래건수"},
                color="count",
                color_continuous_scale="Blues",
            )
            fig_count.update_layout(xaxis_tickangle=-45, height=400)
            st.plotly_chart(fig_count, use_container_width=True)

        with col2:
            # 지역별 데이터 테이블
            st.subheader("지역별 상세 통계")
            display_df = region_df[
                ["region", "count", "avg_price", "median_price", "avg_area"]
            ].copy()
            display_df.columns = [
                "지역",
                "거래건수",
                "평균가격(만원)",
                "중앙가격(만원)",
                "평균면적(㎡)",
            ]
            display_df = display_df.sort_values("평균가격(만원)", ascending=False)
            st.dataframe(display_df, use_container_width=True, hide_index=True)

# 탭 2: 가격 추이
with tab2:
    st.subheader("월별 가격 추이")

    if trend_df_global is not None and not trend_df_global.empty:
        # 🎯 통일된 차트 생성 함수 사용
        fig_trend = create_monthly_trend_chart(
            trend_df_global,
            chart_title="월별 가격 추이",
            height=500
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        # trend_df는 통계 테이블용으로 유지
        trend_df = trend_df_global.copy()
        trend_df["avg_price"] = pd.to_numeric(trend_df["avg_price"], errors="coerce")
        trend_df["median_price"] = pd.to_numeric(
            trend_df["median_price"], errors="coerce"
        )
        trend_df = trend_df.dropna(subset=["avg_price", "median_price"])

        # 통계 테이블
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("월별 통계")
            display_trend_df = trend_df[
                ["year_month", "count", "avg_price", "median_price"]
            ].copy()
            display_trend_df.columns = [
                "년월",
                "거래건수",
                "평균가격(만원)",
                "중앙가격(만원)",
            ]
            display_trend_df["평균가격(만원)"] = display_trend_df[
                "평균가격(만원)"
            ].map(lambda x: f"{x:,.0f}")
            display_trend_df["중앙가격(만원)"] = display_trend_df[
                "중앙가격(만원)"
            ].map(lambda x: f"{x:,.0f}")
            st.dataframe(display_trend_df, use_container_width=True, hide_index=True)

            with st.expander("차트 값 검증", expanded=False):
                if "2020-01" in trend_df["year_month"].values:
                    row = trend_df[trend_df["year_month"] == "2020-01"].iloc[0]
                    st.write(
                        f"2020-01 평균가격: {row['avg_price']:,.0f}만원 | 중앙가격: {row['median_price']:,.0f}만원"
                    )
                st.dataframe(
                    trend_df.head(5),
                    use_container_width=True,
                    hide_index=True,
                )

        with col2:
            # 거래건수 바 차트
            fig_count_trend = px.bar(
                trend_df,
                x="year_month",
                y="count",
                title="월별 거래건수",
                labels={"year_month": "년월", "count": "거래건수"},
                color="count",
                color_continuous_scale="Greens",
            )
            fig_count_trend.update_layout(xaxis_tickangle=-45, height=400)
            st.plotly_chart(fig_count_trend, use_container_width=True)
    else:
        st.info("가격 추이 데이터가 없습니다.")

# 탭 2b: 시기 이벤트 분석
with tab2b:
    st.subheader("🧭 시기 이벤트 분석")
    st.caption("선택한 시기의 시장 상황을 요약하고 데이터 기반 이벤트 신호를 제공합니다.")

    if trend_df_global is None or trend_df_global.empty:
        st.info("월별 가격 추이 데이터가 없어 시기 분석을 할 수 없습니다.")
    elif not trend_analysis_items:
        st.info("가격/날짜 정보가 있는 데이터가 없어 시기 분석을 할 수 없습니다.")
    else:
        st.caption(
            f"월별 가격 추이 탭의 실제 데이터와 동일합니다. (적용 데이터: {len(trend_analysis_items):,}건)"
        )
        min_date = min(item["_deal_date"] for item in trend_analysis_items)
        max_date = max(item["_deal_date"] for item in trend_analysis_items)
        months = trend_months_global

        # 🎯 기간 선택 UI (차트 위에 배치)
        selection_mode = st.radio(
            "선택 방식",
            ["월 단일", "월 범위", "날짜 범위"],
            horizontal=True,
        )

        start_date = None
        end_date = None
        start_month = None
        end_month = None

        if selection_mode == "월 단일" and months:
            if "analysis_month" not in st.session_state:
                st.session_state["analysis_month"] = months[-1]
            selected_month = st.selectbox("분석 월", months, key="analysis_month")
            start_date, end_date = month_bounds(selected_month)
            start_month = end_month = selected_month

        elif selection_mode == "월 범위" and months:
            default_start = months[-6] if len(months) >= 6 else months[0]
            default_end = months[-1]
            start_month, end_month = st.select_slider(
                "월 범위 선택",
                options=months,
                value=(default_start, default_end),
                key="analysis_month_range",
            )
            start_date, _ = month_bounds(start_month)
            _, end_date = month_bounds(end_month)

        else:
            min_day = min_date.date()
            max_day = max_date.date()
            default_start_day = max_day - timedelta(days=90)
            if default_start_day < min_day:
                default_start_day = min_day
            start_day, end_day = st.slider(
                "날짜 범위 선택",
                min_value=min_day,
                max_value=max_day,
                value=(default_start_day, max_day),
                format="YYYY-MM-DD",
            )
            start_date = datetime.combine(start_day, datetime.min.time())
            end_date = datetime.combine(end_day, datetime.max.time())
            # 날짜를 년월로 변환 (차트 하이라이트용)
            start_month = start_date.strftime("%Y-%m")
            end_month = end_date.strftime("%Y-%m")

        if start_date and end_date and start_date > end_date:
            st.error("선택한 기간이 올바르지 않습니다. 시작일이 종료일보다 늦습니다.")
            st.stop()

        # 🎯 선택된 기간이 하이라이트된 차트 표시
        if start_month and end_month:
            fig_event = create_monthly_trend_chart(
                trend_df_global,
                highlight_range=(start_month, end_month),
                chart_title="월별 가격 추이 (분석 기간 강조)",
                height=450
            )
            st.plotly_chart(fig_event, use_container_width=True)
        else:
            # 기간이 선택되지 않은 경우 기본 차트 표시
            fig_event = create_monthly_trend_chart(
                trend_df_global,
                chart_title="월별 가격 추이 (기간을 선택하세요)",
                height=450
            )
            st.plotly_chart(fig_event, use_container_width=True)

        # 월별 실제 값 보기 expander
        with st.expander("월별 실제 값 보기", expanded=False):
            trend_df = trend_df_global.copy()
            trend_df["avg_price"] = pd.to_numeric(trend_df["avg_price"], errors="coerce")
            trend_df["median_price"] = pd.to_numeric(trend_df["median_price"], errors="coerce")
            trend_df = trend_df.dropna(subset=["avg_price", "median_price"])

            display_trend_df = trend_df[["year_month", "avg_price", "median_price", "count"]].copy()
            display_trend_df.columns = ["년월", "평균 가격(만원)", "중앙 가격(만원)", "거래건수"]
            display_trend_df["평균 가격(만원)"] = display_trend_df["평균 가격(만원)"].map(lambda x: f"{x:,.0f}")
            display_trend_df["중앙 가격(만원)"] = display_trend_df["중앙 가격(만원)"].map(lambda x: f"{x:,.0f}")
            st.dataframe(display_trend_df, use_container_width=True, hide_index=True)

        if start_date and end_date:
            period_summary = summarize_period(
                trend_analysis_items, start_date, end_date
            )
            baseline_summary = build_baseline_summary(
                trend_analysis_items, start_date, end_date
            )
            comparison = compare_periods(period_summary, baseline_summary)
            signals = detect_market_signals(
                period_summary, baseline_summary, comparison
            )
            matched_events = match_manual_events(
                MANUAL_EVENT_MAP, start_date, end_date
            )

            report_text = build_period_report(
                period_summary, baseline_summary, comparison, signals, matched_events
            )

            st.text_area("분석 결과", report_text, height=320)

            st.markdown("---")
            st.subheader("AI 요약 (선택)")
            st.caption("환경변수 `GEMINI_API_KEY`가 필요합니다.")

            if "llm_summary_text" not in st.session_state:
                st.session_state["llm_summary_text"] = ""
            if "gemini_api_key" not in st.session_state:
                st.session_state["gemini_api_key"] = ""

            model_name = st.text_input(
                "모델 이름",
                value="gemini-3-flash-preview",
                help="환경에 설치된 google-genai SDK가 지원하는 모델 이름을 입력하세요.",
            )
            api_key_input = st.text_input(
                "Gemini API Key (세션 한정)",
                type="password",
                help="로컬 세션에서만 사용되며 저장되지 않습니다.",
                value=st.session_state["gemini_api_key"],
            )
            st.session_state["gemini_api_key"] = api_key_input

            if st.button("AI 요약 생성", use_container_width=True):
                prompt = build_llm_prompt(
                    period_summary,
                    baseline_summary,
                    comparison,
                    signals,
                    matched_events,
                )
                with st.spinner("Gemini 요약 생성 중..."):
                    summary_text, error = generate_gemini_summary(
                        prompt, model_name, api_key_override=api_key_input.strip()
                    )
                if error:
                    st.error(error)
                else:
                    st.session_state["llm_summary_text"] = summary_text

            if st.session_state["llm_summary_text"]:
                st.text_area(
                    "AI 요약 결과",
                    st.session_state["llm_summary_text"],
                    height=260,
                )

# 탭 3: 면적별 분석
with tab3:
    st.subheader("면적별 가격 분석")

    area_analysis = analyze_by_area(items)

    if area_analysis["data"]:
        area_df = pd.DataFrame(area_analysis["data"])

        # 면적별 평균가격 막대 그래프
        fig_area = px.bar(
            area_df,
            x="area_range",
            y="avg_price",
            title="면적 구간별 평균 거래가격",
            labels={
                "area_range": "면적 구간 (㎡)",
                "avg_price": "평균 거래가격 (만원)",
            },
            color="avg_price",
            color_continuous_scale="Reds",
        )
        fig_area.update_layout(xaxis_tickangle=-45, height=500)
        st.plotly_chart(fig_area, use_container_width=True)

        # 면적별 가격 분포 산점도
        valid_items = [
            item
            for item in items
            if item.get("_area_numeric") is not None
            and item.get("_deal_amount_numeric") is not None
        ]

        if valid_items:
            scatter_df = pd.DataFrame(
                [
                    {
                        "area": item.get("_area_numeric"),
                        "price": item.get("_deal_amount_numeric"),
                        "region": item.get("_region_name", "미지정"),
                    }
                    for item in valid_items
                ]
            )

            fig_scatter = px.scatter(
                scatter_df,
                x="area",
                y="price",
                color="region",
                title="면적 vs 거래가격 분포",
                labels={
                    "area": "전용면적 (㎡)",
                    "price": "거래가격 (만원)",
                    "region": "지역",
                },
                hover_data=["region"],
            )
            fig_scatter.update_layout(height=500)
            st.plotly_chart(fig_scatter, use_container_width=True)

        # 면적별 통계 테이블
        st.subheader("면적 구간별 상세 통계")
        display_area_df = area_df[
            ["area_range", "count", "avg_price", "avg_area", "price_per_area"]
        ].copy()
        display_area_df.columns = [
            "면적구간(㎡)",
            "거래건수",
            "평균가격(만원)",
            "평균면적(㎡)",
            "㎡당 가격(만원)",
        ]
        st.dataframe(display_area_df, use_container_width=True, hide_index=True)

        # 층수별 분석
        st.subheader("층수별 평균가격")
        floor_analysis = analyze_by_floor(items)

        if floor_analysis["data"]:
            floor_df = pd.DataFrame(floor_analysis["data"])
            floor_df = floor_df.sort_values("floor")

            fig_floor = px.bar(
                floor_df.head(30),  # 상위 30개만 표시
                x="floor",
                y="avg_price",
                title="층수별 평균 거래가격",
                labels={"floor": "층수", "avg_price": "평균 거래가격 (만원)"},
                color="avg_price",
                color_continuous_scale="Purples",
            )
            fig_floor.update_layout(height=400)
            st.plotly_chart(fig_floor, use_container_width=True)

        # 건축년도별 분석
        st.subheader("건축년도별 평균가격")
        build_year_analysis = analyze_by_build_year(items)

        if build_year_analysis["data"]:
            year_df = pd.DataFrame(build_year_analysis["data"])
            year_df = year_df.sort_values("build_year")

            fig_year = px.line(
                year_df,
                x="build_year",
                y="avg_price",
                title="건축년도별 평균 거래가격",
                labels={"build_year": "건축년도", "avg_price": "평균 거래가격 (만원)"},
                markers=True,
            )
            fig_year.update_layout(height=400)
            st.plotly_chart(fig_year, use_container_width=True)
    else:
        st.info("면적별 분석 데이터가 없습니다.")

# 탭 4: 평당가 분석
with tab4:
    st.subheader("📊 평당가(㎡당 가격) 분석")
    st.info(
        "평당가는 면적에 따른 가격 차이를 정규화하여 실질적인 가격 비교를 가능하게 합니다."
    )

    # 평당가 분석 실행
    price_per_area_analysis = calculate_price_per_area(items)

    if price_per_area_analysis["stats"]:
        ppa_stats = price_per_area_analysis["stats"]

        # 전체 평당가 통계 카드
        st.subheader("전체 평당가 통계")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("평균 평당가", f"{ppa_stats['avg_price_per_area']:,.1f}만원/㎡")
        with col2:
            st.metric(
                "중앙 평당가", f"{ppa_stats['median_price_per_area']:,.1f}만원/㎡"
            )
        with col3:
            st.metric("최고 평당가", f"{ppa_stats['max_price_per_area']:,.1f}만원/㎡")
        with col4:
            st.metric("최저 평당가", f"{ppa_stats['min_price_per_area']:,.1f}만원/㎡")

        # 지역별 평당가 TOP 10
        st.subheader("지역별 평당가 TOP 10")
        if price_per_area_analysis["by_region"]:
            region_ppa_df = pd.DataFrame(price_per_area_analysis["by_region"][:10])

            fig_region_ppa = px.bar(
                region_ppa_df,
                x="region",
                y="avg_price_per_area",
                title="지역별 평균 평당가 (TOP 10)",
                labels={
                    "region": "지역",
                    "avg_price_per_area": "평균 평당가 (만원/㎡)",
                },
                color="avg_price_per_area",
                color_continuous_scale="Reds",
                text=region_ppa_df["avg_price_per_area"].apply(lambda x: f"{x:,.0f}"),
            )
            fig_region_ppa.update_traces(textposition="outside")
            fig_region_ppa.update_layout(xaxis_tickangle=-45, height=500)
            st.plotly_chart(fig_region_ppa, use_container_width=True)

            # 지역별 평당가 테이블 (BOTTOM 10 포함)
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("고가 지역 TOP 10")
                top_regions_df = pd.DataFrame(price_per_area_analysis["by_region"][:10])
                top_regions_df = top_regions_df[
                    ["region", "count", "avg_price_per_area", "median_price_per_area"]
                ]
                top_regions_df.columns = [
                    "지역",
                    "거래건수",
                    "평균 평당가(만원/㎡)",
                    "중앙 평당가(만원/㎡)",
                ]
                top_regions_df["평균 평당가(만원/㎡)"] = top_regions_df[
                    "평균 평당가(만원/㎡)"
                ].apply(lambda x: f"{x:,.1f}")
                top_regions_df["중앙 평당가(만원/㎡)"] = top_regions_df[
                    "중앙 평당가(만원/㎡)"
                ].apply(lambda x: f"{x:,.1f}")
                st.dataframe(top_regions_df, use_container_width=True, hide_index=True)

            with col2:
                st.subheader("저가 지역 BOTTOM 10")
                bottom_regions = price_per_area_analysis["by_region"][-10:]
                bottom_regions_df = pd.DataFrame(list(reversed(bottom_regions)))
                bottom_regions_df = bottom_regions_df[
                    ["region", "count", "avg_price_per_area", "median_price_per_area"]
                ]
                bottom_regions_df.columns = [
                    "지역",
                    "거래건수",
                    "평균 평당가(만원/㎡)",
                    "중앙 평당가(만원/㎡)",
                ]
                bottom_regions_df["평균 평당가(만원/㎡)"] = bottom_regions_df[
                    "평균 평당가(만원/㎡)"
                ].apply(lambda x: f"{x:,.1f}")
                bottom_regions_df["중앙 평당가(만원/㎡)"] = bottom_regions_df[
                    "중앙 평당가(만원/㎡)"
                ].apply(lambda x: f"{x:,.1f}")
                st.dataframe(
                    bottom_regions_df, use_container_width=True, hide_index=True
                )

        # 면적대별 평당가 분석
        st.subheader("면적대별 평당가 (소형 vs 대형)")
        if price_per_area_analysis["by_area_range"]:
            area_range_df = pd.DataFrame(price_per_area_analysis["by_area_range"])

            fig_area_ppa = px.bar(
                area_range_df,
                x="area_range",
                y="avg_price_per_area",
                title="면적대별 평균 평당가",
                labels={
                    "area_range": "면적대",
                    "avg_price_per_area": "평균 평당가 (만원/㎡)",
                },
                color="avg_price_per_area",
                color_continuous_scale="Viridis",
                text=area_range_df["avg_price_per_area"].apply(lambda x: f"{x:,.0f}"),
            )
            fig_area_ppa.update_traces(textposition="outside")
            fig_area_ppa.update_layout(height=400)
            st.plotly_chart(fig_area_ppa, use_container_width=True)

            # 면적대별 상세 테이블
            area_detail_df = area_range_df[
                [
                    "area_range",
                    "count",
                    "avg_price_per_area",
                    "avg_total_price",
                    "avg_area",
                ]
            ].copy()
            area_detail_df.columns = [
                "면적대",
                "거래건수",
                "평균 평당가(만원/㎡)",
                "평균 총가격(만원)",
                "평균 면적(㎡)",
            ]
            area_detail_df["평균 평당가(만원/㎡)"] = area_detail_df[
                "평균 평당가(만원/㎡)"
            ].apply(lambda x: f"{x:,.1f}")
            area_detail_df["평균 총가격(만원)"] = area_detail_df[
                "평균 총가격(만원)"
            ].apply(lambda x: f"{x:,.0f}")
            area_detail_df["평균 면적(㎡)"] = area_detail_df["평균 면적(㎡)"].apply(
                lambda x: f"{x:.1f}"
            )
            st.dataframe(area_detail_df, use_container_width=True, hide_index=True)

        # 건축년도별 평당가 (신축 프리미엄 분석)
        st.subheader("건축년도별 평당가 (신축 프리미엄)")
        if price_per_area_analysis["by_build_year"]:
            build_year_df = pd.DataFrame(price_per_area_analysis["by_build_year"])

            fig_build_ppa = px.bar(
                build_year_df,
                x="build_year_range",
                y="avg_price_per_area",
                title="건축년도별 평균 평당가 (신축 프리미엄 분석)",
                labels={
                    "build_year_range": "건축연도 구분",
                    "avg_price_per_area": "평균 평당가 (만원/㎡)",
                },
                color="avg_price_per_area",
                color_continuous_scale="Blues",
                text=build_year_df["avg_price_per_area"].apply(lambda x: f"{x:,.0f}"),
            )
            fig_build_ppa.update_traces(textposition="outside")
            fig_build_ppa.update_layout(height=400)
            st.plotly_chart(fig_build_ppa, use_container_width=True)

            # 신축 프리미엄 계산
            if len(build_year_df) >= 2:
                newest = build_year_df.iloc[0]["avg_price_per_area"]
                oldest = build_year_df.iloc[-1]["avg_price_per_area"]
                premium_pct = ((newest - oldest) / oldest) * 100 if oldest > 0 else 0
                st.info(
                    f"💡 **신축 프리미엄**: 신축(5년 이내) 대비 노후(30년+) 평당가 차이 = **{premium_pct:+.1f}%**"
                )

        # 월별 평당가 추이
        st.subheader("월별 평당가 추이")
        ppa_trend = analyze_price_per_area_trend(items)

        if ppa_trend["trend"]:
            trend_df = pd.DataFrame(ppa_trend["trend"])

            fig_trend = go.Figure()

            fig_trend.add_trace(
                go.Scatter(
                    x=trend_df["year_month"],
                    y=trend_df["avg_price_per_area"],
                    mode="lines+markers",
                    name="평균 평당가",
                    line=dict(color="#e74c3c", width=3),
                )
            )

            fig_trend.add_trace(
                go.Scatter(
                    x=trend_df["year_month"],
                    y=trend_df["median_price_per_area"],
                    mode="lines+markers",
                    name="중앙 평당가",
                    line=dict(color="#3498db", width=2, dash="dash"),
                )
            )

            fig_trend.update_layout(
                title="월별 평당가 추이",
                xaxis_title="년월",
                yaxis_title="평당가 (만원/㎡)",
                height=500,
                hovermode="x unified",
            )

            st.plotly_chart(fig_trend, use_container_width=True)

            # 월별 변동률 표시
            if "change_rate" in trend_df.columns:
                fig_change = px.bar(
                    trend_df[1:],  # 첫 번째 달 제외 (변동률 없음)
                    x="year_month",
                    y="change_rate",
                    title="월별 평당가 변동률",
                    labels={"year_month": "년월", "change_rate": "변동률 (%)"},
                    color="change_rate",
                    color_continuous_scale="RdYlGn",
                    color_continuous_midpoint=0,
                )
                fig_change.update_layout(height=300)
                st.plotly_chart(fig_change, use_container_width=True)

        # TOP 10 고가/저가 거래
        st.subheader("평당가 기준 TOP 10 거래")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### 🔺 최고가 거래 TOP 10")
            if price_per_area_analysis["top_expensive"]:
                expensive_df = pd.DataFrame(price_per_area_analysis["top_expensive"])
                expensive_df = expensive_df[
                    [
                        "apt_name",
                        "region",
                        "price_per_area",
                        "total_price",
                        "area",
                        "deal_date",
                    ]
                ]
                expensive_df.columns = [
                    "아파트",
                    "지역",
                    "평당가(만원/㎡)",
                    "총가격(만원)",
                    "면적(㎡)",
                    "거래일",
                ]
                expensive_df["평당가(만원/㎡)"] = expensive_df["평당가(만원/㎡)"].apply(
                    lambda x: f"{x:,.1f}"
                )
                expensive_df["총가격(만원)"] = expensive_df["총가격(만원)"].apply(
                    lambda x: f"{x:,.0f}"
                )
                expensive_df["면적(㎡)"] = expensive_df["면적(㎡)"].apply(
                    lambda x: f"{x:.1f}"
                )
                st.dataframe(expensive_df, use_container_width=True, hide_index=True)

        with col2:
            st.markdown("##### 🔻 최저가 거래 TOP 10")
            if price_per_area_analysis["top_affordable"]:
                affordable_df = pd.DataFrame(price_per_area_analysis["top_affordable"])
                affordable_df = affordable_df[
                    [
                        "apt_name",
                        "region",
                        "price_per_area",
                        "total_price",
                        "area",
                        "deal_date",
                    ]
                ]
                affordable_df.columns = [
                    "아파트",
                    "지역",
                    "평당가(만원/㎡)",
                    "총가격(만원)",
                    "면적(㎡)",
                    "거래일",
                ]
                affordable_df["평당가(만원/㎡)"] = affordable_df[
                    "평당가(만원/㎡)"
                ].apply(lambda x: f"{x:,.1f}")
                affordable_df["총가격(만원)"] = affordable_df["총가격(만원)"].apply(
                    lambda x: f"{x:,.0f}"
                )
                affordable_df["면적(㎡)"] = affordable_df["면적(㎡)"].apply(
                    lambda x: f"{x:.1f}"
                )
                st.dataframe(affordable_df, use_container_width=True, hide_index=True)
    else:
        st.warning(
            "평당가 분석을 위한 데이터가 부족합니다. 가격과 면적 정보가 있는 데이터가 필요합니다."
        )

# 탭 5: 아파트별 분석
with tab5:
    st.subheader("🏢 아파트별 분석")
    st.info(
        "동일 아파트의 거래 내역을 묶어서 분석합니다. 아파트를 선택하면 면적별 상세 정보를 확인할 수 있습니다."
    )

    # 아파트별 분석 실행
    apt_analysis = analyze_by_apartment(items)

    if apt_analysis["data"]:
        # 상단 통계
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("총 아파트 수", f"{apt_analysis['total_apartments']:,}개")
        with col2:
            st.metric("총 거래건수", f"{apt_analysis['total_deals']:,}건")
        with col3:
            avg_deals = (
                apt_analysis["total_deals"] / apt_analysis["total_apartments"]
                if apt_analysis["total_apartments"] > 0
                else 0
            )
            st.metric("아파트당 평균 거래", f"{avg_deals:.1f}건")

        # 아파트 검색 및 필터
        col1, col2 = st.columns([2, 1])
        with col1:
            search_apt = st.text_input(
                "🔍 아파트 검색",
                placeholder="아파트명을 입력하세요 (예: 래미안, 자이, 힐스테이트)",
                key="apt_search",
            )
        with col2:
            sort_option = st.selectbox(
                "정렬 기준",
                [
                    "거래건수 순",
                    "평균가격 높은순",
                    "평균가격 낮은순",
                    "평당가 높은순",
                    "평당가 낮은순",
                ],
                key="apt_sort",
            )

        # 데이터 필터링 및 정렬
        apt_list = apt_analysis["data"]

        if search_apt:
            apt_list = [
                apt for apt in apt_list if search_apt.lower() in apt["apt_name"].lower()
            ]

        # 정렬
        if sort_option == "평균가격 높은순":
            apt_list = sorted(
                apt_list, key=lambda x: x.get("avg_price", 0), reverse=True
            )
        elif sort_option == "평균가격 낮은순":
            apt_list = sorted(apt_list, key=lambda x: x.get("avg_price", 0))
        elif sort_option == "평당가 높은순":
            apt_list = sorted(
                apt_list, key=lambda x: x.get("avg_price_per_area", 0), reverse=True
            )
        elif sort_option == "평당가 낮은순":
            apt_list = sorted(apt_list, key=lambda x: x.get("avg_price_per_area", 0))
        # 기본은 거래건수 순 (이미 정렬되어 있음)

        # 아파트 목록 테이블
        st.subheader(f"아파트 목록 ({len(apt_list)}개)")

        # 데이터프레임 생성
        apt_df_data = []
        for apt in apt_list[:100]:  # 최대 100개
            apt_df_data.append(
                {
                    "아파트명": apt["apt_name"],
                    "지역": apt.get("region", "N/A"),
                    "거래건수": apt["count"],
                    "평균가격(만원)": f"{apt.get('avg_price', 0):,.0f}"
                    if apt.get("avg_price")
                    else "N/A",
                    "평당가(만원/㎡)": f"{apt.get('avg_price_per_area', 0):,.1f}"
                    if apt.get("avg_price_per_area")
                    else "N/A",
                    "건축년도": apt.get("build_year", "N/A"),
                    "층수범위": apt.get("floor_range", "N/A"),
                }
            )

        if apt_df_data:
            apt_df = pd.DataFrame(apt_df_data)
            st.dataframe(apt_df, use_container_width=True, hide_index=True)

            if len(apt_list) > 100:
                st.info(f"상위 100개만 표시됩니다. 전체 {len(apt_list)}개 중")

        # 거래 많은 아파트 TOP 10 차트
        st.subheader("거래 활발 아파트 TOP 10")
        top_apt = apt_analysis["data"][:10]

        if top_apt:
            top_apt_df = pd.DataFrame(
                [
                    {
                        "apt_name": f"{apt['apt_name']}\n({apt.get('region', '')})",
                        "count": apt["count"],
                        "avg_price": apt.get("avg_price", 0),
                    }
                    for apt in top_apt
                ]
            )

            fig_top = px.bar(
                top_apt_df,
                x="apt_name",
                y="count",
                title="거래건수 TOP 10 아파트",
                labels={"apt_name": "아파트", "count": "거래건수"},
                color="avg_price",
                color_continuous_scale="Viridis",
                text="count",
            )
            fig_top.update_traces(textposition="outside")
            fig_top.update_layout(xaxis_tickangle=-45, height=500)
            st.plotly_chart(fig_top, use_container_width=True)

        # 아파트 상세 정보 섹션
        st.subheader("📋 아파트 상세 조회")

        # 아파트 선택 (selectbox)
        apt_names = [
            f"{apt['apt_name']} ({apt.get('region', 'N/A')}) - {apt['count']}건"
            for apt in apt_list[:50]
        ]

        if apt_names:
            selected_apt_idx = st.selectbox(
                "상세 정보를 볼 아파트 선택",
                range(len(apt_names)),
                format_func=lambda x: apt_names[x],
                key="apt_select",
            )

            if selected_apt_idx is not None:
                selected_apt = apt_list[selected_apt_idx]

                # 상세 정보 조회
                apt_detail = get_apartment_detail(
                    items, selected_apt["apt_name"], selected_apt.get("region")
                )

                if apt_detail["found"]:
                    st.markdown(f"### 🏠 {apt_detail['apt_name']}")

                    # 전체 통계
                    overall = apt_detail.get("overall", {})
                    if overall:
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric(
                                "총 거래건수", f"{overall.get('total_count', 0)}건"
                            )
                        with col2:
                            st.metric(
                                "평균 가격", f"{overall.get('avg_price', 0):,.0f}만원"
                            )
                        with col3:
                            st.metric(
                                "평당가",
                                f"{overall.get('avg_price_per_area', 0):,.1f}만원/㎡",
                            )
                        with col4:
                            st.metric("건축년도", overall.get("build_year", "N/A"))

                        # 가격 범위
                        st.write(
                            f"**가격 범위**: {overall.get('min_price', 0):,.0f}만원 ~ {overall.get('max_price', 0):,.0f}만원"
                        )

                    # 면적별 분석
                    st.subheader("면적별 거래 현황")
                    if apt_detail.get("by_area"):
                        area_df_data = []
                        for area_info in apt_detail["by_area"]:
                            area_df_data.append(
                                {
                                    "면적(㎡)": f"{area_info['area']:.1f}",
                                    "거래건수": area_info["count"],
                                    "평균가격(만원)": f"{area_info.get('avg_price', 0):,.0f}",
                                    "최고가(만원)": f"{area_info.get('max_price', 0):,.0f}",
                                    "최저가(만원)": f"{area_info.get('min_price', 0):,.0f}",
                                    "평당가(만원/㎡)": f"{area_info.get('avg_price_per_area', 0):,.1f}",
                                }
                            )

                        area_df = pd.DataFrame(area_df_data)
                        st.dataframe(area_df, use_container_width=True, hide_index=True)

                        # 면적별 가격 차트
                        if len(apt_detail["by_area"]) > 1:
                            area_chart_df = pd.DataFrame(
                                [
                                    {
                                        "area": a["area"],
                                        "avg_price": a.get("avg_price", 0),
                                        "count": a["count"],
                                    }
                                    for a in apt_detail["by_area"]
                                ]
                            )

                            fig_area = px.bar(
                                area_chart_df,
                                x="area",
                                y="avg_price",
                                title=f"{apt_detail['apt_name']} - 면적별 평균 가격",
                                labels={
                                    "area": "면적(㎡)",
                                    "avg_price": "평균 가격(만원)",
                                },
                                text="count",
                            )
                            fig_area.update_traces(
                                texttemplate="%{text}건", textposition="outside"
                            )
                            st.plotly_chart(fig_area, use_container_width=True)

                    # 최근 거래 내역
                    st.subheader("최근 거래 내역")
                    recent_deals = selected_apt.get("deals", [])[:20]

                    if recent_deals:
                        deals_df_data = []
                        for deal in recent_deals:
                            deals_df_data.append(
                                {
                                    "거래일": deal.get("deal_date", "N/A"),
                                    "가격(만원)": f"{deal.get('price', 0):,.0f}"
                                    if deal.get("price")
                                    else "N/A",
                                    "면적(㎡)": f"{deal.get('area', 0):.1f}"
                                    if deal.get("area")
                                    else "N/A",
                                    "층": deal.get("floor", "N/A"),
                                    "평당가(만원/㎡)": f"{deal.get('price_per_area', 0):,.1f}"
                                    if deal.get("price_per_area")
                                    else "N/A",
                                }
                            )

                        deals_df = pd.DataFrame(deals_df_data)
                        st.dataframe(
                            deals_df, use_container_width=True, hide_index=True
                        )
                else:
                    st.warning("선택한 아파트의 상세 정보를 찾을 수 없습니다.")
    else:
        st.warning("아파트별 분석을 위한 데이터가 없습니다.")

# 탭 6: 전세가율/갭투자 분석
with tab6:
    st.subheader("💰 전세가율 & 갭투자 분석")
    st.info("""
    **전세가율** = 전세가 ÷ 매매가 × 100
    - 80% 이상: 🔴 위험 (매매가 하락 시 역전세 위험)
    - 70~80%: 🟡 주의
    - 70% 미만: 🟢 안전

    **갭** = 매매가 - 전세가 (실제 필요 투자금)
    """)

    # 전세가율 분석 실행
    jeonse_analysis = calculate_jeonse_ratio(items)

    if jeonse_analysis.get("has_data"):
        jeonse_stats = jeonse_analysis["stats"]
        risk_summary = jeonse_analysis["risk_summary"]

        # 전체 통계 카드
        st.subheader("전체 전세가율 통계")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            avg_ratio = jeonse_stats["avg_jeonse_ratio"]
            color = "🔴" if avg_ratio >= 80 else ("🟡" if avg_ratio >= 70 else "🟢")
            st.metric(f"{color} 평균 전세가율", f"{avg_ratio:.1f}%")
        with col2:
            st.metric("중앙 전세가율", f"{jeonse_stats['median_jeonse_ratio']:.1f}%")
        with col3:
            st.metric("평균 갭", f"{jeonse_stats['avg_gap']:,.0f}만원")
        with col4:
            st.metric("매칭된 아파트", f"{jeonse_stats['matched_apartments']}개")

        # 위험도 분류
        st.subheader("위험도 분류")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🔴 위험 (80% 이상)", f"{risk_summary['high_risk_count']}개")
        with col2:
            st.metric("🟡 주의 (70~80%)", f"{risk_summary['medium_risk_count']}개")
        with col3:
            st.metric("🟢 안전 (70% 미만)", f"{risk_summary['low_risk_count']}개")

        # 위험도 파이 차트
        risk_df = pd.DataFrame(
            [
                {"위험도": "🔴 위험 (80%+)", "개수": risk_summary["high_risk_count"]},
                {
                    "위험도": "🟡 주의 (70-80%)",
                    "개수": risk_summary["medium_risk_count"],
                },
                {"위험도": "🟢 안전 (<70%)", "개수": risk_summary["low_risk_count"]},
            ]
        )

        if risk_df["개수"].sum() > 0:
            fig_risk = px.pie(
                risk_df,
                values="개수",
                names="위험도",
                title="전세가율 위험도 분포",
                color="위험도",
                color_discrete_map={
                    "🔴 위험 (80%+)": "#e74c3c",
                    "🟡 주의 (70-80%)": "#f39c12",
                    "🟢 안전 (<70%)": "#27ae60",
                },
            )
            st.plotly_chart(fig_risk, use_container_width=True)

        # 지역별 전세가율
        st.subheader("지역별 전세가율")
        if jeonse_analysis.get("by_region"):
            region_df = pd.DataFrame(jeonse_analysis["by_region"])

            fig_region = px.bar(
                region_df.head(15),
                x="region",
                y="avg_jeonse_ratio",
                title="지역별 평균 전세가율 (상위 15개)",
                labels={"region": "지역", "avg_jeonse_ratio": "평균 전세가율 (%)"},
                color="avg_jeonse_ratio",
                color_continuous_scale="RdYlGn_r",
                text=region_df.head(15)["avg_jeonse_ratio"].apply(
                    lambda x: f"{x:.1f}%"
                ),
            )
            fig_region.update_traces(textposition="outside")
            fig_region.update_layout(xaxis_tickangle=-45, height=500)
            fig_region.add_hline(
                y=80, line_dash="dash", line_color="red", annotation_text="위험선 (80%)"
            )
            fig_region.add_hline(
                y=70,
                line_dash="dash",
                line_color="orange",
                annotation_text="주의선 (70%)",
            )
            st.plotly_chart(fig_region, use_container_width=True)

            # 지역별 테이블
            region_table = region_df[
                ["region", "avg_jeonse_ratio", "avg_gap", "count"]
            ].copy()
            region_table.columns = [
                "지역",
                "평균 전세가율(%)",
                "평균 갭(만원)",
                "데이터수",
            ]
            region_table["평균 전세가율(%)"] = region_table["평균 전세가율(%)"].apply(
                lambda x: f"{x:.1f}"
            )
            region_table["평균 갭(만원)"] = region_table["평균 갭(만원)"].apply(
                lambda x: f"{x:,.0f}"
            )
            st.dataframe(region_table, use_container_width=True, hide_index=True)

        # 면적대별 전세가율
        st.subheader("면적대별 전세가율")
        if jeonse_analysis.get("by_area"):
            area_df = pd.DataFrame(jeonse_analysis["by_area"])

            fig_area = px.bar(
                area_df,
                x="area_group",
                y="avg_jeonse_ratio",
                title="면적대별 평균 전세가율",
                labels={
                    "area_group": "면적대",
                    "avg_jeonse_ratio": "평균 전세가율 (%)",
                },
                color="avg_jeonse_ratio",
                color_continuous_scale="RdYlGn_r",
                text=area_df["avg_jeonse_ratio"].apply(lambda x: f"{x:.1f}%"),
            )
            fig_area.update_traces(textposition="outside")
            fig_area.update_layout(height=400)
            st.plotly_chart(fig_area, use_container_width=True)

        # 고위험 아파트 TOP 10
        st.subheader("🔴 고위험 아파트 TOP 10 (전세가율 높은 순)")
        if jeonse_analysis.get("high_ratio_apartments"):
            high_risk_df = pd.DataFrame(jeonse_analysis["high_ratio_apartments"])
            high_risk_df = high_risk_df[
                [
                    "apt_name",
                    "region",
                    "jeonse_ratio",
                    "avg_trade_price",
                    "avg_jeonse_price",
                    "gap",
                ]
            ]
            high_risk_df.columns = [
                "아파트",
                "지역",
                "전세가율(%)",
                "매매가(만원)",
                "전세가(만원)",
                "갭(만원)",
            ]
            high_risk_df["전세가율(%)"] = high_risk_df["전세가율(%)"].apply(
                lambda x: f"{x:.1f}"
            )
            high_risk_df["매매가(만원)"] = high_risk_df["매매가(만원)"].apply(
                lambda x: f"{x:,.0f}"
            )
            high_risk_df["전세가(만원)"] = high_risk_df["전세가(만원)"].apply(
                lambda x: f"{x:,.0f}"
            )
            high_risk_df["갭(만원)"] = high_risk_df["갭(만원)"].apply(
                lambda x: f"{x:,.0f}"
            )
            st.dataframe(high_risk_df, use_container_width=True, hide_index=True)

        # 갭투자 분석 섹션
        st.markdown("---")
        st.subheader("📈 갭투자 분석")

        gap_analysis = analyze_gap_investment(items)

        if gap_analysis.get("has_data"):
            gap_stats = gap_analysis["gap_stats"]

            # 갭 통계
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("평균 갭", f"{gap_stats['avg_gap']:,.0f}만원")
            with col2:
                st.metric("중앙 갭", f"{gap_stats['median_gap']:,.0f}만원")
            with col3:
                st.metric("최소 갭", f"{gap_stats['min_gap']:,.0f}만원")
            with col4:
                st.metric("분석 대상", f"{gap_stats['total_count']}개")

            # 갭 금액 구간별 분포
            st.subheader("갭 금액 구간별 분포")
            if gap_analysis.get("by_gap_range"):
                gap_range_df = pd.DataFrame(gap_analysis["by_gap_range"])

                fig_gap = px.bar(
                    gap_range_df,
                    x="gap_range",
                    y="count",
                    title="갭 금액 구간별 아파트 수",
                    labels={"gap_range": "갭 금액 구간", "count": "아파트 수"},
                    color="avg_jeonse_ratio",
                    color_continuous_scale="Viridis",
                    text="count",
                )
                fig_gap.update_traces(textposition="outside")
                fig_gap.update_layout(height=400)
                st.plotly_chart(fig_gap, use_container_width=True)

            # 소액 투자 가능 물건 (갭 1억 이하)
            st.subheader("💡 소액 투자 가능 물건 (갭 1억 이하)")
            if gap_analysis.get("small_gap_items"):
                small_gap_df = pd.DataFrame(gap_analysis["small_gap_items"])
                small_gap_df = small_gap_df[
                    [
                        "apt_name",
                        "region",
                        "gap",
                        "avg_trade_price",
                        "avg_jeonse_price",
                        "jeonse_ratio",
                    ]
                ]
                small_gap_df.columns = [
                    "아파트",
                    "지역",
                    "갭(만원)",
                    "매매가(만원)",
                    "전세가(만원)",
                    "전세가율(%)",
                ]
                small_gap_df["갭(만원)"] = small_gap_df["갭(만원)"].apply(
                    lambda x: f"{x:,.0f}"
                )
                small_gap_df["매매가(만원)"] = small_gap_df["매매가(만원)"].apply(
                    lambda x: f"{x:,.0f}"
                )
                small_gap_df["전세가(만원)"] = small_gap_df["전세가(만원)"].apply(
                    lambda x: f"{x:,.0f}"
                )
                small_gap_df["전세가율(%)"] = small_gap_df["전세가율(%)"].apply(
                    lambda x: f"{x:.1f}"
                )
                st.dataframe(small_gap_df, use_container_width=True, hide_index=True)
            else:
                st.info("갭 1억 이하 물건이 없습니다.")

            # 예상 ROI 높은 물건
            st.subheader("📊 예상 수익률(ROI) 높은 물건 TOP 10")
            st.caption("※ 전세가의 연 4% 월세 전환 가정 시 투자금 대비 수익률")
            if gap_analysis.get("high_roi_items"):
                roi_df = pd.DataFrame(gap_analysis["high_roi_items"])
                roi_df = roi_df[
                    [
                        "apt_name",
                        "region",
                        "estimated_roi",
                        "gap",
                        "avg_trade_price",
                        "jeonse_ratio",
                    ]
                ]
                roi_df.columns = [
                    "아파트",
                    "지역",
                    "예상ROI(%)",
                    "갭(만원)",
                    "매매가(만원)",
                    "전세가율(%)",
                ]
                roi_df["예상ROI(%)"] = roi_df["예상ROI(%)"].apply(lambda x: f"{x:.1f}")
                roi_df["갭(만원)"] = roi_df["갭(만원)"].apply(lambda x: f"{x:,.0f}")
                roi_df["매매가(만원)"] = roi_df["매매가(만원)"].apply(
                    lambda x: f"{x:,.0f}"
                )
                roi_df["전세가율(%)"] = roi_df["전세가율(%)"].apply(
                    lambda x: f"{x:.1f}"
                )
                st.dataframe(roi_df, use_container_width=True, hide_index=True)
        else:
            st.warning(gap_analysis.get("message", "갭투자 분석 데이터가 부족합니다."))
    else:
        st.warning(f"""
        전세가율 분석을 위해서는 **API 02(매매)**와 **API 04(전월세)** 데이터가 모두 필요합니다.

        현재 데이터:
        - 매매 데이터: {jeonse_analysis.get("trade_count", 0)}건
        - 전세 데이터: {jeonse_analysis.get("jeonse_count", 0)}건

        **데이터 수집** 탭에서 동일 지역의 매매/전월세 데이터를 모두 수집해주세요.
        """)

# 탭 6b: 월세/전세 분석
with tab6b:
    st.subheader("🏠 월세 전환율 & 월세/전세 선호도 분석")
    st.info("""
    **월세 전환율** = (월세 × 12) ÷ 보증금 × 100 (연 환산)
    - 은행 금리보다 높으면 월세가 유리, 낮으면 전세가 유리
    - 일반적으로 4~6%가 적정 수준
    """)

    rent_analysis = analyze_rent_vs_jeonse(items)

    if rent_analysis.get("has_data"):
        rent_stats = rent_analysis["stats"]

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "전세 거래",
                f"{rent_stats['jeonse_count']:,}건 ({rent_stats['jeonse_ratio']:.1f}%)",
            )
        with col2:
            st.metric(
                "월세 거래",
                f"{rent_stats['wolse_count']:,}건 ({rent_stats['wolse_ratio']:.1f}%)",
            )
        with col3:
            st.metric("평균 월세 전환율", f"{rent_stats['avg_conversion_rate']:.2f}%")
        with col4:
            st.metric(
                "중앙 월세 전환율", f"{rent_stats['median_conversion_rate']:.2f}%"
            )

        col1, col2 = st.columns(2)

        with col1:
            pie_data = pd.DataFrame(
                [
                    {"유형": "전세", "건수": rent_stats["jeonse_count"]},
                    {"유형": "월세", "건수": rent_stats["wolse_count"]},
                ]
            )
            fig_pie = px.pie(
                pie_data,
                values="건수",
                names="유형",
                title="월세 vs 전세 거래 비율",
                color="유형",
                color_discrete_map={"전세": "#3498db", "월세": "#e74c3c"},
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            if rent_analysis.get("by_area"):
                area_df = pd.DataFrame(rent_analysis["by_area"])
                fig_area = px.bar(
                    area_df,
                    x="area_range",
                    y=["jeonse_ratio", "wolse_ratio"],
                    title="면적대별 월세/전세 비율",
                    labels={
                        "value": "비율 (%)",
                        "area_range": "면적대",
                        "variable": "유형",
                    },
                    barmode="stack",
                )
                fig_area.update_layout(height=400)
                st.plotly_chart(fig_area, use_container_width=True)

        st.subheader("지역별 월세/전세 비율")
        if rent_analysis.get("by_region"):
            region_df = pd.DataFrame(rent_analysis["by_region"][:15])

            fig_region = px.bar(
                region_df,
                x="region",
                y="wolse_ratio",
                title="지역별 월세 비율 (상위 15개)",
                labels={"region": "지역", "wolse_ratio": "월세 비율 (%)"},
                color="avg_conversion_rate",
                color_continuous_scale="Reds",
                text=region_df["wolse_ratio"].apply(lambda x: f"{x:.1f}%"),
            )
            fig_region.update_traces(textposition="outside")
            fig_region.update_layout(xaxis_tickangle=-45, height=500)
            st.plotly_chart(fig_region, use_container_width=True)

            region_table = region_df[
                [
                    "region",
                    "jeonse_count",
                    "wolse_count",
                    "wolse_ratio",
                    "avg_conversion_rate",
                ]
            ].copy()
            region_table.columns = [
                "지역",
                "전세 건수",
                "월세 건수",
                "월세 비율(%)",
                "평균 전환율(%)",
            ]
            region_table["월세 비율(%)"] = region_table["월세 비율(%)"].apply(
                lambda x: f"{x:.1f}"
            )
            region_table["평균 전환율(%)"] = region_table["평균 전환율(%)"].apply(
                lambda x: f"{x:.2f}"
            )
            st.dataframe(region_table, use_container_width=True, hide_index=True)

        st.subheader("층수별 월세/전세 선호도")
        if rent_analysis.get("by_floor"):
            floor_df = pd.DataFrame(rent_analysis["by_floor"])

            fig_floor = px.bar(
                floor_df,
                x="floor_category",
                y=["jeonse_ratio", "wolse_ratio"],
                title="층수별 월세/전세 비율",
                labels={
                    "value": "비율 (%)",
                    "floor_category": "층수 구간",
                    "variable": "유형",
                },
                barmode="group",
                color_discrete_map={
                    "jeonse_ratio": "#3498db",
                    "wolse_ratio": "#e74c3c",
                },
            )
            fig_floor.update_layout(height=400)
            st.plotly_chart(fig_floor, use_container_width=True)

        st.subheader("보증금 구간별 월세 전환율")
        if rent_analysis.get("by_deposit"):
            deposit_df = pd.DataFrame(rent_analysis["by_deposit"])

            fig_deposit = px.bar(
                deposit_df,
                x="deposit_range",
                y="avg_conversion_rate",
                title="보증금 구간별 평균 월세 전환율",
                labels={
                    "deposit_range": "보증금 구간",
                    "avg_conversion_rate": "평균 전환율 (%)",
                },
                color="avg_conversion_rate",
                color_continuous_scale="Viridis",
                text=deposit_df["avg_conversion_rate"].apply(lambda x: f"{x:.2f}%"),
            )
            fig_deposit.update_traces(textposition="outside")
            fig_deposit.update_layout(height=400)
            fig_deposit.add_hline(
                y=rent_stats["avg_conversion_rate"],
                line_dash="dash",
                line_color="red",
                annotation_text=f"전체 평균: {rent_stats['avg_conversion_rate']:.2f}%",
            )
            st.plotly_chart(fig_deposit, use_container_width=True)

            deposit_table = deposit_df[
                [
                    "deposit_range",
                    "count",
                    "avg_conversion_rate",
                    "avg_monthly_rent",
                    "avg_deposit",
                ]
            ].copy()
            deposit_table.columns = [
                "보증금 구간",
                "거래 수",
                "평균 전환율(%)",
                "평균 월세(만원)",
                "평균 보증금(만원)",
            ]
            deposit_table["평균 전환율(%)"] = deposit_table["평균 전환율(%)"].apply(
                lambda x: f"{x:.2f}"
            )
            deposit_table["평균 월세(만원)"] = deposit_table["평균 월세(만원)"].apply(
                lambda x: f"{x:,.0f}"
            )
            deposit_table["평균 보증금(만원)"] = deposit_table[
                "평균 보증금(만원)"
            ].apply(lambda x: f"{x:,.0f}")
            st.dataframe(deposit_table, use_container_width=True, hide_index=True)

        st.subheader("🔥 고수익 월세 물건 TOP 10 (전환율 높은 순)")
        if rent_analysis.get("high_conversion_items"):
            high_conv_df = pd.DataFrame(rent_analysis["high_conversion_items"])
            high_conv_df = high_conv_df[
                [
                    "apt_name",
                    "region",
                    "conversion_rate",
                    "deposit",
                    "monthly_rent",
                    "area",
                    "floor",
                ]
            ]
            high_conv_df.columns = [
                "아파트",
                "지역",
                "전환율(%)",
                "보증금(만원)",
                "월세(만원)",
                "면적(㎡)",
                "층",
            ]
            high_conv_df["전환율(%)"] = high_conv_df["전환율(%)"].apply(
                lambda x: f"{x:.2f}"
            )
            high_conv_df["보증금(만원)"] = high_conv_df["보증금(만원)"].apply(
                lambda x: f"{x:,.0f}"
            )
            high_conv_df["월세(만원)"] = high_conv_df["월세(만원)"].apply(
                lambda x: f"{x:,.0f}"
            )
            high_conv_df["면적(㎡)"] = high_conv_df["면적(㎡)"].apply(
                lambda x: f"{x:.1f}" if x else "N/A"
            )
            st.dataframe(high_conv_df, use_container_width=True, hide_index=True)
    else:
        st.warning("""
        월세/전세 분석을 위해서는 **API 04(전월세)** 데이터가 필요합니다.

        **데이터 수집** 탭에서 전월세 데이터를 수집해주세요.
        """)

# 탭 6c: 매매 심층 분석 (거래유형, 매수자/매도자, 취소거래)
with tab6c:
    st.subheader("📈 매매 심층 분석")
    st.info("거래유형(중개/직거래), 매수자/매도자 유형(개인/법인), 취소거래 분석")

    analysis_type = st.radio(
        "분석 유형 선택",
        ["🏢 거래유형 분석", "👥 매수자/매도자 유형", "❌ 취소거래 분석"],
        horizontal=True,
        key="trade_analysis_type",
    )

    if analysis_type == "🏢 거래유형 분석":
        st.markdown("### 🏢 거래유형(중개거래 vs 직거래) 분석")

        dealing_analysis = analyze_dealing_type(items)

        if dealing_analysis.get("has_data"):
            deal_stats = dealing_analysis["stats"]

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(
                    "중개거래",
                    f"{deal_stats['broker_count']:,}건 ({deal_stats['broker_ratio']:.1f}%)",
                )
            with col2:
                st.metric(
                    "직거래",
                    f"{deal_stats['direct_count']:,}건 ({deal_stats['direct_ratio']:.1f}%)",
                )
            with col3:
                st.metric(
                    "중개거래 평균가", f"{deal_stats['broker_avg_price']:,.0f}만원"
                )
            with col4:
                st.metric("직거래 평균가", f"{deal_stats['direct_avg_price']:,.0f}만원")

            if deal_stats["price_diff"] != 0:
                diff_sign = "+" if deal_stats["price_diff"] > 0 else ""
                st.info(
                    f"💡 중개거래가 직거래보다 평균 **{diff_sign}{deal_stats['price_diff']:,.0f}만원** ({diff_sign}{deal_stats['price_diff_pct']:.1f}%) 더 {'비쌉니다' if deal_stats['price_diff'] > 0 else '저렴합니다'}"
                )

            col1, col2 = st.columns(2)

            with col1:
                pie_data = pd.DataFrame(
                    [
                        {"유형": "중개거래", "건수": deal_stats["broker_count"]},
                        {"유형": "직거래", "건수": deal_stats["direct_count"]},
                    ]
                )
                fig_pie = px.pie(
                    pie_data,
                    values="건수",
                    names="유형",
                    title="거래유형 비율",
                    color="유형",
                    color_discrete_map={"중개거래": "#3498db", "직거래": "#e74c3c"},
                )
                st.plotly_chart(fig_pie, use_container_width=True)

            with col2:
                if dealing_analysis.get("by_price_range"):
                    price_df = pd.DataFrame(dealing_analysis["by_price_range"])
                    fig_price = px.bar(
                        price_df,
                        x="price_range",
                        y=["broker_ratio", "direct_ratio"],
                        title="가격대별 거래유형 비율",
                        labels={
                            "value": "비율 (%)",
                            "price_range": "가격대",
                            "variable": "유형",
                        },
                        barmode="group",
                    )
                    st.plotly_chart(fig_price, use_container_width=True)

            st.subheader("지역별 직거래 비율")
            if dealing_analysis.get("by_region"):
                region_df = pd.DataFrame(dealing_analysis["by_region"][:15])
                fig_region = px.bar(
                    region_df,
                    x="region",
                    y="direct_ratio",
                    title="지역별 직거래 비율 (상위 15개)",
                    labels={"region": "지역", "direct_ratio": "직거래 비율 (%)"},
                    color="direct_ratio",
                    color_continuous_scale="Reds",
                    text=region_df["direct_ratio"].apply(lambda x: f"{x:.1f}%"),
                )
                fig_region.update_traces(textposition="outside")
                fig_region.update_layout(xaxis_tickangle=-45, height=500)
                st.plotly_chart(fig_region, use_container_width=True)

            if (
                dealing_analysis.get("by_month")
                and len(dealing_analysis["by_month"]) > 1
            ):
                st.subheader("월별 직거래 비율 추이")
                month_df = pd.DataFrame(dealing_analysis["by_month"])
                fig_month = px.line(
                    month_df,
                    x="year_month",
                    y="direct_ratio",
                    title="월별 직거래 비율 추이",
                    labels={"year_month": "년월", "direct_ratio": "직거래 비율 (%)"},
                    markers=True,
                )
                st.plotly_chart(fig_month, use_container_width=True)
        else:
            st.warning(
                dealing_analysis.get("message", "거래유형 분석 데이터가 없습니다.")
            )

    elif analysis_type == "👥 매수자/매도자 유형":
        st.markdown("### 👥 매수자/매도자 유형(개인 vs 법인) 분석")

        buyer_seller_analysis = analyze_buyer_seller_type(items)

        if buyer_seller_analysis.get("has_data"):
            bs_stats = buyer_seller_analysis["stats"]

            st.markdown("#### 매수자 유형")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "법인 매수",
                    f"{bs_stats.get('buyer_법인_count', 0):,}건 ({bs_stats.get('buyer_법인_ratio', 0):.1f}%)",
                )
            with col2:
                st.metric(
                    "개인 매수",
                    f"{bs_stats.get('buyer_개인_count', 0):,}건 ({bs_stats.get('buyer_개인_ratio', 0):.1f}%)",
                )
            with col3:
                st.metric(
                    "미공개",
                    f"{bs_stats.get('buyer_미공개_count', 0):,}건 ({bs_stats.get('buyer_미공개_ratio', 0):.1f}%)",
                )

            st.markdown("#### 매도자 유형")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "법인 매도",
                    f"{bs_stats.get('seller_법인_count', 0):,}건 ({bs_stats.get('seller_법인_ratio', 0):.1f}%)",
                )
            with col2:
                st.metric(
                    "개인 매도",
                    f"{bs_stats.get('seller_개인_count', 0):,}건 ({bs_stats.get('seller_개인_ratio', 0):.1f}%)",
                )
            with col3:
                st.metric(
                    "미공개",
                    f"{bs_stats.get('seller_미공개_count', 0):,}건 ({bs_stats.get('seller_미공개_ratio', 0):.1f}%)",
                )

            if bs_stats.get("buyer_법인_count", 0) > bs_stats.get(
                "seller_법인_count", 0
            ):
                st.success(
                    f"💡 법인 순매수: 법인 매수({bs_stats.get('buyer_법인_count', 0)}건) > 법인 매도({bs_stats.get('seller_법인_count', 0)}건) → 투자 유입 신호"
                )
            elif bs_stats.get("buyer_법인_count", 0) < bs_stats.get(
                "seller_법인_count", 0
            ):
                st.warning(
                    f"⚠️ 법인 순매도: 법인 매수({bs_stats.get('buyer_법인_count', 0)}건) < 법인 매도({bs_stats.get('seller_법인_count', 0)}건) → 투자 이탈 신호"
                )

            st.subheader("지역별 법인 거래 비율")
            if buyer_seller_analysis.get("by_region"):
                region_df = pd.DataFrame(buyer_seller_analysis["by_region"][:15])
                fig_region = px.bar(
                    region_df,
                    x="region",
                    y=["buyer_법인_ratio", "seller_법인_ratio"],
                    title="지역별 법인 거래 비율 (상위 15개)",
                    labels={"value": "비율 (%)", "region": "지역", "variable": "유형"},
                    barmode="group",
                )
                fig_region.update_layout(xaxis_tickangle=-45, height=500)
                st.plotly_chart(fig_region, use_container_width=True)

            if (
                buyer_seller_analysis.get("by_month")
                and len(buyer_seller_analysis["by_month"]) > 1
            ):
                st.subheader("월별 법인 거래 비율 추이")
                month_df = pd.DataFrame(buyer_seller_analysis["by_month"])
                fig_month = px.line(
                    month_df,
                    x="year_month",
                    y=["buyer_법인_ratio", "seller_법인_ratio"],
                    title="월별 법인 매수/매도 비율 추이",
                    labels={
                        "year_month": "년월",
                        "value": "비율 (%)",
                        "variable": "유형",
                    },
                    markers=True,
                )
                st.plotly_chart(fig_month, use_container_width=True)
        else:
            st.warning(
                buyer_seller_analysis.get(
                    "message", "매수자/매도자 유형 분석 데이터가 없습니다."
                )
            )

    else:  # 취소거래 분석
        st.markdown("### ❌ 취소거래 분석")
        st.info("취소거래 비율이 높은 지역 = 시장 불안정 신호")

        cancel_analysis = analyze_cancelled_deals(items)

        if cancel_analysis.get("has_data"):
            cancel_stats = cancel_analysis["stats"]

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("전체 거래", f"{cancel_stats['total_count']:,}건")
            with col2:
                cancel_ratio = cancel_stats["cancel_ratio"]
                color = (
                    "🔴"
                    if cancel_ratio >= 10
                    else ("🟡" if cancel_ratio >= 5 else "🟢")
                )
                st.metric(
                    f"{color} 취소 거래",
                    f"{cancel_stats['cancelled_count']:,}건 ({cancel_ratio:.1f}%)",
                )
            with col3:
                st.metric(
                    "취소거래 평균가", f"{cancel_stats['cancelled_avg_price']:,.0f}만원"
                )
            with col4:
                st.metric(
                    "정상거래 평균가", f"{cancel_stats['normal_avg_price']:,.0f}만원"
                )

            if cancel_stats.get("cancel_types"):
                st.markdown("#### 취소 유형별 현황")
                cancel_type_df = pd.DataFrame(
                    [
                        {"취소유형": k, "건수": v}
                        for k, v in cancel_stats["cancel_types"].items()
                    ]
                )
                st.dataframe(cancel_type_df, use_container_width=True, hide_index=True)

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("지역별 취소율")
                if cancel_analysis.get("by_region"):
                    region_df = pd.DataFrame(cancel_analysis["by_region"][:10])
                    fig_region = px.bar(
                        region_df,
                        x="region",
                        y="cancel_ratio",
                        title="지역별 취소율 TOP 10",
                        labels={"region": "지역", "cancel_ratio": "취소율 (%)"},
                        color="cancel_ratio",
                        color_continuous_scale="Reds",
                        text=region_df["cancel_ratio"].apply(lambda x: f"{x:.1f}%"),
                    )
                    fig_region.update_traces(textposition="outside")
                    fig_region.update_layout(xaxis_tickangle=-45, height=400)
                    st.plotly_chart(fig_region, use_container_width=True)

            with col2:
                st.subheader("가격대별 취소율")
                if cancel_analysis.get("by_price_range"):
                    price_df = pd.DataFrame(cancel_analysis["by_price_range"])
                    fig_price = px.bar(
                        price_df,
                        x="price_range",
                        y="cancel_ratio",
                        title="가격대별 취소율",
                        labels={"price_range": "가격대", "cancel_ratio": "취소율 (%)"},
                        color="cancel_ratio",
                        color_continuous_scale="Oranges",
                        text=price_df["cancel_ratio"].apply(lambda x: f"{x:.1f}%"),
                    )
                    fig_price.update_traces(textposition="outside")
                    fig_price.update_layout(height=400)
                    st.plotly_chart(fig_price, use_container_width=True)

            if cancel_analysis.get("by_month") and len(cancel_analysis["by_month"]) > 1:
                st.subheader("월별 취소율 추이")
                month_df = pd.DataFrame(cancel_analysis["by_month"])
                fig_month = px.line(
                    month_df,
                    x="year_month",
                    y="cancel_ratio",
                    title="월별 취소율 추이 (시장 불안정성 지표)",
                    labels={"year_month": "년월", "cancel_ratio": "취소율 (%)"},
                    markers=True,
                )
                fig_month.add_hline(
                    y=cancel_stats["cancel_ratio"],
                    line_dash="dash",
                    line_color="red",
                    annotation_text=f"전체 평균: {cancel_stats['cancel_ratio']:.1f}%",
                )
                st.plotly_chart(fig_month, use_container_width=True)

            if cancel_analysis.get("cancelled_items"):
                st.subheader("취소거래 상세 목록")
                cancel_df = pd.DataFrame(cancel_analysis["cancelled_items"][:30])
                cancel_df = cancel_df[
                    ["apt_name", "region", "price", "cancel_type", "deal_date"]
                ]
                cancel_df.columns = [
                    "아파트",
                    "지역",
                    "가격(만원)",
                    "취소유형",
                    "거래일",
                ]
                cancel_df["가격(만원)"] = cancel_df["가격(만원)"].apply(
                    lambda x: f"{x:,.0f}" if x else "N/A"
                )
                st.dataframe(cancel_df, use_container_width=True, hide_index=True)
        else:
            st.warning(
                cancel_analysis.get("message", "취소거래 분석 데이터가 없습니다.")
            )

# 탭 7: 급매물/프리미엄 분석
with tab7:
    st.subheader("🔥 급매물 탐지 & 프리미엄 분석")

    # 급매물 탐지 섹션
    st.markdown("### 🏷️ 급매물 탐지")
    st.info("급매물: 동일 아파트+면적대의 최근 평균가 대비 10% 이상 낮은 거래")

    # 급매물 기준 설정
    threshold = st.slider(
        "급매 판단 기준 (%)",
        min_value=5,
        max_value=30,
        value=10,
        step=5,
        key="bargain_threshold",
    )

    bargain_analysis = detect_bargain_sales(items, threshold_pct=threshold)

    if bargain_analysis.get("has_data"):
        bargain_stats = bargain_analysis["stats"]

        # 통계 카드
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("급매물 수", f"{bargain_stats['bargain_count']}건")
        with col2:
            st.metric("급매율", f"{bargain_stats['bargain_rate']:.1f}%")
        with col3:
            st.metric("평균 할인율", f"{bargain_stats['avg_discount']:.1f}%")
        with col4:
            st.metric("최대 할인율", f"{bargain_stats['max_discount']:.1f}%")

        # 지역별 급매율
        if bargain_analysis.get("by_region"):
            st.subheader("지역별 급매율")
            region_df = pd.DataFrame(bargain_analysis["by_region"][:10])

            fig_region = px.bar(
                region_df,
                x="region",
                y="bargain_rate",
                title="지역별 급매율 TOP 10",
                labels={"region": "지역", "bargain_rate": "급매율 (%)"},
                color="bargain_rate",
                color_continuous_scale="Reds",
                text=region_df["bargain_rate"].apply(lambda x: f"{x:.1f}%"),
            )
            fig_region.update_traces(textposition="outside")
            fig_region.update_layout(xaxis_tickangle=-45, height=400)
            st.plotly_chart(fig_region, use_container_width=True)

        # 급매물 리스트
        st.subheader("🔥 급매물 리스트 (할인율 높은 순)")
        if bargain_analysis.get("bargain_items"):
            bargain_df = pd.DataFrame(bargain_analysis["bargain_items"][:20])
            bargain_df = bargain_df[
                [
                    "apt_name",
                    "region",
                    "discount_pct",
                    "current_price",
                    "avg_price",
                    "deal_date",
                    "floor",
                ]
            ]
            bargain_df.columns = [
                "아파트",
                "지역",
                "할인율(%)",
                "거래가(만원)",
                "평균가(만원)",
                "거래일",
                "층",
            ]
            bargain_df["할인율(%)"] = bargain_df["할인율(%)"].apply(
                lambda x: f"{x:.1f}"
            )
            bargain_df["거래가(만원)"] = bargain_df["거래가(만원)"].apply(
                lambda x: f"{x:,.0f}"
            )
            bargain_df["평균가(만원)"] = bargain_df["평균가(만원)"].apply(
                lambda x: f"{x:,.0f}"
            )
            st.dataframe(bargain_df, use_container_width=True, hide_index=True)
    else:
        st.warning(
            bargain_analysis.get("message", "급매물 탐지를 위한 데이터가 부족합니다.")
        )

    st.markdown("---")

    # 층수 프리미엄 분석 섹션
    st.markdown("### 🏗️ 층수 프리미엄 분석")

    floor_analysis = analyze_floor_premium(items)

    if floor_analysis.get("has_data"):
        floor_stats = floor_analysis["stats"]

        # 로열층 정보
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "로열층",
                f"{floor_stats['royal_floor']}층"
                if floor_stats["royal_floor"]
                else "N/A",
            )
        with col2:
            st.metric("로열층 프리미엄", f"{floor_stats['royal_premium_pct']:+.1f}%")
        with col3:
            st.metric("분석 대상", f"{floor_stats['total_count']}건")

        # 층수 구간별 프리미엄
        if floor_analysis.get("by_floor_category"):
            floor_cat_df = pd.DataFrame(floor_analysis["by_floor_category"])

            fig_floor = px.bar(
                floor_cat_df,
                x="floor_category",
                y="premium_pct",
                title="층수 구간별 프리미엄 (기준: 중층 11-15층)",
                labels={"floor_category": "층수 구간", "premium_pct": "프리미엄 (%)"},
                color="premium_pct",
                color_continuous_scale="RdYlGn",
                color_continuous_midpoint=0,
                text=floor_cat_df["premium_pct"].apply(lambda x: f"{x:+.1f}%"),
            )
            fig_floor.update_traces(textposition="outside")
            fig_floor.update_layout(height=400)
            fig_floor.add_hline(y=0, line_dash="dash", line_color="gray")
            st.plotly_chart(fig_floor, use_container_width=True)

            # 층수 구간별 테이블
            floor_table = floor_cat_df[
                ["floor_category", "count", "avg_price_per_area", "premium_pct"]
            ].copy()
            floor_table.columns = [
                "층수 구간",
                "거래건수",
                "평균 평당가(만원/㎡)",
                "프리미엄(%)",
            ]
            floor_table["평균 평당가(만원/㎡)"] = floor_table[
                "평균 평당가(만원/㎡)"
            ].apply(lambda x: f"{x:,.1f}")
            floor_table["프리미엄(%)"] = floor_table["프리미엄(%)"].apply(
                lambda x: f"{x:+.1f}"
            )
            st.dataframe(floor_table, use_container_width=True, hide_index=True)

        # 개별 층수별 프리미엄 차트
        if floor_analysis.get("by_individual_floor"):
            st.subheader("개별 층수별 프리미엄")
            ind_floor_df = pd.DataFrame(floor_analysis["by_individual_floor"])

            fig_ind = px.line(
                ind_floor_df,
                x="floor",
                y="premium_pct",
                title="층수별 프리미엄 추이",
                labels={"floor": "층", "premium_pct": "프리미엄 (%)"},
                markers=True,
            )
            fig_ind.add_hline(y=0, line_dash="dash", line_color="gray")
            fig_ind.update_layout(height=400)
            st.plotly_chart(fig_ind, use_container_width=True)
    else:
        st.warning(
            floor_analysis.get(
                "message", "층수 프리미엄 분석을 위한 데이터가 부족합니다."
            )
        )

    st.markdown("---")

    # 건축년도별 프리미엄 분석 섹션
    st.markdown("### 🏠 건축년도별 프리미엄 (신축 프리미엄)")

    age_analysis = analyze_building_age_premium(items)

    if age_analysis.get("has_data"):
        age_stats = age_analysis["stats"]

        # 통계 카드
        col1, col2, col3 = st.columns(3)
        with col1:
            if age_stats["new_building_price"]:
                st.metric(
                    "신축 평당가", f"{age_stats['new_building_price']:,.0f}만원/㎡"
                )
        with col2:
            st.metric("연간 감가상각률", f"{age_stats['annual_depreciation_pct']:.2f}%")
        with col3:
            st.metric("재건축 대상", f"{age_stats['rebuild_candidate_count']}건")

        # 연식 구간별 프리미엄
        if age_analysis.get("by_age_range"):
            age_range_df = pd.DataFrame(age_analysis["by_age_range"])

            fig_age = px.bar(
                age_range_df,
                x="age_range",
                y="vs_new_pct",
                title="건물 연식별 신축 대비 가격 변화",
                labels={"age_range": "연식 구간", "vs_new_pct": "신축 대비 (%)"},
                color="vs_new_pct",
                color_continuous_scale="RdYlGn",
                color_continuous_midpoint=0,
                text=age_range_df["vs_new_pct"].apply(lambda x: f"{x:+.1f}%"),
            )
            fig_age.update_traces(textposition="outside")
            fig_age.update_layout(height=400)
            fig_age.add_hline(y=0, line_dash="dash", line_color="gray")
            st.plotly_chart(fig_age, use_container_width=True)

            # 연식 구간별 테이블
            age_table = age_range_df[
                ["age_range", "count", "avg_price_per_area", "vs_new_pct"]
            ].copy()
            age_table.columns = [
                "연식 구간",
                "거래건수",
                "평균 평당가(만원/㎡)",
                "신축대비(%)",
            ]
            age_table["평균 평당가(만원/㎡)"] = age_table["평균 평당가(만원/㎡)"].apply(
                lambda x: f"{x:,.1f}"
            )
            age_table["신축대비(%)"] = age_table["신축대비(%)"].apply(
                lambda x: f"{x:+.1f}"
            )
            st.dataframe(age_table, use_container_width=True, hide_index=True)

        # 재건축 대상 아파트
        if age_analysis.get("rebuild_candidates"):
            st.subheader("🔧 재건축 대상 아파트 (30년 이상)")
            rebuild_df = pd.DataFrame(age_analysis["rebuild_candidates"])
            rebuild_df = rebuild_df[
                ["apt_name", "region", "build_year", "building_age", "price_per_area"]
            ]
            rebuild_df.columns = [
                "아파트",
                "지역",
                "건축년도",
                "건물연식(년)",
                "평당가(만원/㎡)",
            ]
            rebuild_df["평당가(만원/㎡)"] = rebuild_df["평당가(만원/㎡)"].apply(
                lambda x: f"{x:,.1f}"
            )
            st.dataframe(rebuild_df, use_container_width=True, hide_index=True)
    else:
        st.warning(
            age_analysis.get(
                "message", "건축년도 프리미엄 분석을 위한 데이터가 부족합니다."
            )
        )

# 탭 8: 상세 데이터
with tab8:
    st.subheader("상세 거래 데이터")

    # 필터 옵션
    col1, col2, col3 = st.columns(3)

    with col1:
        min_price = st.number_input("최소 가격 (만원)", min_value=0, value=0)

    with col2:
        max_price = st.number_input(
            "최대 가격 (만원)",
            min_value=0,
            value=int(stats["max_price"]) if stats["max_price"] > 0 else 100000,
        )

    with col3:
        min_area = st.number_input("최소 면적 (㎡)", min_value=0.0, value=0.0, step=1.0)

    # 데이터 필터링
    filtered_items = items.copy()

    if min_price > 0:
        filtered_items = [
            item
            for item in filtered_items
            if item.get("_deal_amount_numeric")
            and item.get("_deal_amount_numeric") >= min_price
        ]

    if max_price > 0:
        filtered_items = [
            item
            for item in filtered_items
            if item.get("_deal_amount_numeric")
            and item.get("_deal_amount_numeric") <= max_price
        ]

    if min_area > 0:
        filtered_items = [
            item
            for item in filtered_items
            if item.get("_area_numeric") and item.get("_area_numeric") >= min_area
        ]

    # 데이터프레임 생성
    display_items = []
    for item in filtered_items:
        display_items.append(
            {
                "아파트명": item.get("aptNm", "") or item.get("아파트", "N/A"),
                "지역": item.get("_region_name", "N/A"),
                "거래가격(만원)": item.get("_deal_amount_numeric", "N/A"),
                "전용면적(㎡)": item.get("_area_numeric", "N/A"),
                "층수": item.get("_floor_numeric", "N/A"),
                "건축년도": item.get("_build_year_numeric", "N/A"),
                "거래일자": item.get("_deal_date_str", "N/A"),
                "API타입": item.get("_api_type", "N/A"),
            }
        )

    if display_items:
        df = pd.DataFrame(display_items)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.info(f"총 {len(df)}건의 데이터가 표시됩니다.")
    else:
        st.warning("필터 조건에 맞는 데이터가 없습니다.")

# 탭 9: 데이터 수집
with tab9:
    st.subheader("📥 배치 데이터 수집")
    st.info(
        "법정동코드와 기간 범위를 지정하여 여러 API에서 데이터를 일괄 수집할 수 있습니다."
    )

    # 수집 설정
    col1, col2 = st.columns(2)

    with col1:
        lawd_cd = st.text_input(
            "법정동코드 (5자리)",
            placeholder="예: 11680 (강남구)",
            help="5자리 법정동코드를 입력하세요",
        )

        # 주요 지역코드 안내
        with st.expander("주요 지역코드 참고"):
            st.markdown("""
            - 서울특별시 종로구: `11110`
            - 서울특별시 강남구: `11680`
            - 서울특별시 서초구: `11650`
            - 서울특별시 송파구: `11710`
            - 경기도 수원시 영통구: `41117`
            - 경기도 수원시 권선구: `41113`
            """)

    with col2:
        # 기간 선택
        current_year = datetime.now().year
        current_month = datetime.now().month

        col_start, col_end = st.columns(2)

        with col_start:
            start_year = st.number_input(
                "시작년도", min_value=2000, max_value=current_year, value=2023
            )
            start_month = st.number_input("시작월", min_value=1, max_value=12, value=1)

        with col_end:
            end_year = st.number_input(
                "종료년도", min_value=2000, max_value=current_year, value=2023
            )
            end_month = st.number_input("종료월", min_value=1, max_value=12, value=12)

        start_ym = f"{start_year}{start_month:02d}"
        end_ym = f"{end_year}{end_month:02d}"

    # API 타입 선택
    st.subheader("수집할 API 선택")
    api_options = {
        "api_01": "API 01: 분양권전매 실거래가",
        "api_02": "API 02: 매매 실거래가",
        "api_03": "API 03: 매매 실거래가 상세",
        "api_04": "API 04: 전월세 실거래가",
    }

    selected_apis = []
    cols = st.columns(4)
    for idx, (api_key, api_label) in enumerate(api_options.items()):
        with cols[idx]:
            if st.checkbox(api_label, value=True, key=f"api_{api_key}"):
                selected_apis.append(api_key)

    # 고급 설정
    with st.expander("고급 설정"):
        col_delay, col_retries = st.columns(2)
        with col_delay:
            delay_seconds = st.number_input(
                "API 호출 딜레이 (초)",
                min_value=0.1,
                max_value=5.0,
                value=0.5,
                step=0.1,
                help="API 호출 간 대기 시간",
            )
        with col_retries:
            max_retries = st.number_input(
                "최대 재시도 횟수",
                min_value=1,
                max_value=10,
                value=3,
                help="API 호출 실패 시 재시도 횟수",
            )

    # 수집 시작 버튼
    if st.button("🚀 데이터 수집 시작", type="primary", use_container_width=True):
        # 입력 검증
        if not lawd_cd or len(lawd_cd) != 5 or not lawd_cd.isdigit():
            st.error("❌ 법정동코드는 5자리 숫자여야 합니다.")
        elif not selected_apis:
            st.error("❌ 최소 하나 이상의 API를 선택해주세요.")
        elif start_ym > end_ym:
            st.error("❌ 시작년월이 종료년월보다 큽니다.")
        else:
            try:
                # BatchCollector 초기화
                collector = BatchCollector(delay_seconds=delay_seconds)

                # 진행 상황 표시를 위한 컨테이너
                progress_container = st.container()
                status_container = st.container()
                result_container = st.container()

                with progress_container:
                    st.subheader("수집 진행 상황")
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                # 진행 상황 콜백 함수 정의
                def progress_callback(
                    current_api: str,
                    api_index: int,
                    total_apis: int,
                    current_month: str,
                    month_index: int,
                    total_months: int,
                    overall_progress: float,
                    status_message: str,
                ):
                    """진행 상황 업데이트 콜백"""
                    # 진행 바 업데이트
                    progress_bar.progress(overall_progress)

                    # 상태 메시지 업데이트
                    if current_month:
                        status_text.info(
                            f"📊 진행률: {overall_progress * 100:.1f}% | {status_message}"
                        )
                    else:
                        status_text.info(
                            f"📊 진행률: {overall_progress * 100:.1f}% | {status_message}"
                        )

                # 데이터 수집 실행
                with status_container:
                    status_text.info(
                        f"수집 시작: 법정동코드 {lawd_cd}, 기간 {start_ym} ~ {end_ym}"
                    )

                    try:
                        result = collector.collect_data(
                            lawd_cd=lawd_cd,
                            start_ym=start_ym,
                            end_ym=end_ym,
                            api_types=selected_apis,
                            max_retries=max_retries,
                            progress_callback=progress_callback,
                        )

                        # 수집 완료
                        progress_bar.progress(1.0)
                        status_text.success("✅ 데이터 수집이 완료되었습니다!")

                        # 결과 저장
                        with result_container:
                            st.subheader("수집 결과")

                            # 요약 정보
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric(
                                    "전체 성공",
                                    f"{result['summary']['total_successful']}건",
                                )
                            with col2:
                                st.metric(
                                    "전체 실패",
                                    f"{result['summary']['total_failed']}건",
                                )
                            with col3:
                                st.metric(
                                    "전체 데이터",
                                    f"{result['summary']['total_items']:,}건",
                                )

                            # API별 상세 결과
                            st.subheader("API별 수집 결과")

                            for api_type, api_result in result["api_results"].items():
                                with st.expander(
                                    f"{api_result['api_name']} - 성공: {api_result['successful_count']}건, 실패: {api_result['failed_count']}건, 데이터: {api_result['total_items']:,}건"
                                ):
                                    # API별 통계
                                    api_stats_df = pd.DataFrame(
                                        [
                                            {
                                                "월": test_result["deal_ymd"],
                                                "상태": "✅ 성공"
                                                if test_result["success"]
                                                else "❌ 실패",
                                                "데이터 건수": test_result[
                                                    "result"
                                                ].get("item_count", 0)
                                                if test_result["success"]
                                                else 0,
                                                "오류 메시지": test_result[
                                                    "result"
                                                ].get("message")
                                                or test_result["result"].get(
                                                    "result_msg", ""
                                                )
                                                if not test_result["success"]
                                                else "",
                                            }
                                            for test_result in api_result["results"]
                                        ]
                                    )
                                    st.dataframe(
                                        api_stats_df,
                                        use_container_width=True,
                                        hide_index=True,
                                    )

                                    # 결과 저장
                                    try:
                                        filepath = collector.save_results(
                                            result, api_type
                                        )
                                        st.success(f"✅ 저장 완료: `{filepath}`")
                                    except Exception as e:
                                        st.error(f"❌ 저장 실패: {e}")

                            # 데이터 새로고침 안내
                            st.info(
                                "💡 수집된 데이터를 확인하려면 페이지를 새로고침하거나 '데이터 소스'를 다시 선택해주세요."
                            )

                    except ValueError as e:
                        progress_bar.empty()
                        status_text.error(f"❌ 오류: {e}")
                    except Exception as e:
                        progress_bar.empty()
                        status_text.error(f"❌ 예상치 못한 오류 발생: {e}")
                        st.exception(e)

            except Exception as e:
                st.error(f"❌ 수집기 초기화 실패: {e}")
                st.exception(e)

    # 기존 수집 결과 파일 목록 표시
    st.subheader("📁 저장된 수집 결과 파일")

    result_files = {}
    for api_type in ["api_01", "api_02", "api_03", "api_04"]:
        api_dir = project_root / api_type / "output"
        if api_dir.exists():
            json_files = list(api_dir.glob("test_results_*.json"))
            if json_files:
                result_files[api_type] = sorted(
                    json_files, key=lambda x: x.stat().st_mtime, reverse=True
                )

    if result_files:
        for api_type, files in result_files.items():
            api_name = BatchCollector.API_MAP[api_type]["name"]
            with st.expander(f"{api_name} ({len(files)}개 파일)"):
                for file in files[:10]:  # 최대 10개만 표시
                    file_size = file.stat().st_size / 1024  # KB
                    file_time = datetime.fromtimestamp(file.stat().st_mtime)
                    st.text(
                        f"📄 {file.name} ({file_size:.1f} KB, {file_time.strftime('%Y-%m-%d %H:%M:%S')})"
                    )
    else:
        st.info("저장된 수집 결과 파일이 없습니다.")

# 푸터
st.markdown("---")
st.markdown("**아파트 실거래가 데이터 분석** - 국토교통부 공공데이터 API 기반")
