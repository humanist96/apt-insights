"""
구조화된 로깅 시스템 (structlog)

Features:
- JSON 포맷 로깅 (프로덕션)
- 컬러 출력 (개발 환경)
- 요청/응답 추적
- 성능 메트릭
- 에러 컨텍스트
"""
import sys
import logging
from pathlib import Path
from typing import Any, Dict
import structlog
from structlog.types import EventDict, WrappedLogger

from config import settings


# 로그 디렉토리 생성
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)


def add_app_context(
    logger: WrappedLogger, method_name: str, event_dict: EventDict
) -> EventDict:
    """
    애플리케이션 컨텍스트 추가

    환경, 버전 등 공통 필드를 모든 로그에 추가
    """
    event_dict["environment"] = settings.ENVIRONMENT
    event_dict["app"] = "apt-insights"
    event_dict["version"] = "0.1.0"
    return event_dict


def add_log_level(
    logger: WrappedLogger, method_name: str, event_dict: EventDict
) -> EventDict:
    """
    로그 레벨 추가 (대문자)

    'info' → 'INFO'
    """
    if method_name == "info":
        event_dict["level"] = "INFO"
    elif method_name == "warning":
        event_dict["level"] = "WARNING"
    elif method_name == "error":
        event_dict["level"] = "ERROR"
    elif method_name == "debug":
        event_dict["level"] = "DEBUG"
    elif method_name == "critical":
        event_dict["level"] = "CRITICAL"
    else:
        event_dict["level"] = method_name.upper()

    return event_dict


def censor_sensitive_data(
    logger: WrappedLogger, method_name: str, event_dict: EventDict
) -> EventDict:
    """
    민감한 데이터 마스킹

    API 키, 비밀번호 등을 로그에서 제외
    Note: params는 이미 log_request에서 deep copy됨
    """
    sensitive_keys = [
        "serviceKey", "service_key", "api_key", "password", "token",
        "secret", "authorization", "cookie"
    ]

    for key in sensitive_keys:
        if key in event_dict:
            event_dict[key] = "***REDACTED***"

        # 중첩된 딕셔너리도 검사
        if isinstance(event_dict.get("params"), dict):
            if key in event_dict["params"]:
                event_dict["params"][key] = "***REDACTED***"

    return event_dict


def configure_logging(
    log_level: str = None,
    json_logs: bool = None,
    log_file: str = None
) -> None:
    """
    로깅 시스템 설정

    Args:
        log_level: 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_logs: JSON 포맷 사용 여부 (None이면 환경에 따라 자동)
        log_file: 로그 파일 경로 (None이면 기본값)
    """
    # 기본값 설정
    if log_level is None:
        log_level = settings.LOG_LEVEL

    if json_logs is None:
        # 프로덕션: JSON, 개발: 컬러 출력
        json_logs = settings.ENVIRONMENT == "production"

    if log_file is None:
        log_file = LOG_DIR / "apt_insights.log"

    # 로그 레벨 변환
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # 표준 라이브러리 로거 설정
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=numeric_level,
    )

    # structlog 프로세서 체인
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        add_app_context,
        add_log_level,
        censor_sensitive_data,
        structlog.processors.StackInfoRenderer(),
    ]

    # 예외 정보 포맷터
    if json_logs:
        processors.append(structlog.processors.format_exc_info)
    else:
        processors.append(structlog.dev.set_exc_info)

    # 최종 렌더러
    if json_logs:
        # 프로덕션: JSON
        processors.append(structlog.processors.JSONRenderer())
    else:
        # 개발: 컬러 출력
        processors.append(
            structlog.dev.ConsoleRenderer(
                colors=True,
                exception_formatter=structlog.dev.plain_traceback
            )
        )

    # structlog 설정
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # 파일 핸들러 추가 (선택적)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(numeric_level)

        # 파일은 항상 JSON 포맷
        file_formatter = logging.Formatter('%(message)s')
        file_handler.setFormatter(file_formatter)

        # 루트 로거에 추가
        root_logger = logging.getLogger()
        root_logger.addHandler(file_handler)


def get_logger(name: str = None) -> structlog.stdlib.BoundLogger:
    """
    로거 인스턴스 반환

    Args:
        name: 로거 이름 (보통 __name__ 사용)

    Returns:
        structlog 로거 인스턴스

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("api_call", url="https://api.example.com", status=200)
    """
    if name is None:
        name = "apt-insights"

    return structlog.get_logger(name)


# API 요청 로깅 헬퍼
class APILogger:
    """
    API 요청/응답 로깅 유틸리티

    Example:
        >>> api_logger = APILogger("api_01")
        >>> api_logger.log_request("GET", "https://api.example.com", {"param": "value"})
        >>> api_logger.log_response(200, 0.5, item_count=10)
        >>> api_logger.log_error("Connection failed", error_code="TIMEOUT")
    """

    def __init__(self, api_name: str):
        """
        Args:
            api_name: API 이름 (예: "api_01", "api_02")
        """
        self.logger = get_logger(f"api.{api_name}")
        self.api_name = api_name

    def log_request(
        self,
        method: str,
        url: str,
        params: Dict[str, Any] = None,
        **extra
    ) -> None:
        """
        API 요청 로깅

        Args:
            method: HTTP 메서드
            url: 요청 URL
            params: 요청 파라미터
            **extra: 추가 컨텍스트
        """
        import copy

        # 원본 params를 수정하지 않도록 깊은 복사
        params_copy = copy.deepcopy(params) if params else {}

        self.logger.info(
            "api_request",
            api=self.api_name,
            method=method,
            url=url,
            params=params_copy,
            **extra
        )

    def log_response(
        self,
        status_code: int,
        response_time: float,
        **extra
    ) -> None:
        """
        API 응답 로깅

        Args:
            status_code: HTTP 상태 코드
            response_time: 응답 시간 (초)
            **extra: 추가 메트릭
        """
        self.logger.info(
            "api_response",
            api=self.api_name,
            status_code=status_code,
            response_time=response_time,
            **extra
        )

    def log_error(
        self,
        message: str,
        error_code: str = None,
        **extra
    ) -> None:
        """
        API 에러 로깅

        Args:
            message: 에러 메시지
            error_code: 에러 코드
            **extra: 추가 컨텍스트
        """
        self.logger.error(
            "api_error",
            api=self.api_name,
            error_message=message,
            error_code=error_code,
            **extra
        )

    def log_retry(
        self,
        attempt: int,
        max_retries: int,
        reason: str
    ) -> None:
        """
        재시도 로깅

        Args:
            attempt: 현재 시도 횟수
            max_retries: 최대 재시도 횟수
            reason: 재시도 사유
        """
        self.logger.warning(
            "api_retry",
            api=self.api_name,
            attempt=attempt,
            max_retries=max_retries,
            reason=reason
        )


# 성능 메트릭 로깅
class PerformanceLogger:
    """
    성능 측정 및 로깅

    Example:
        >>> with PerformanceLogger("data_processing") as perf:
        >>>     # 처리 로직
        >>>     process_data()
        >>>     perf.add_metric("records_processed", 1000)
    """

    def __init__(self, operation: str):
        """
        Args:
            operation: 작업 이름
        """
        self.logger = get_logger("performance")
        self.operation = operation
        self.start_time = None
        self.metrics: Dict[str, Any] = {}

    def __enter__(self):
        """컨텍스트 매니저 진입"""
        import time
        self.start_time = time.time()
        self.logger.debug(
            "operation_start",
            operation=self.operation
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """컨텍스트 매니저 종료"""
        import time
        elapsed = time.time() - self.start_time

        if exc_type is None:
            # 정상 종료
            self.logger.info(
                "operation_complete",
                operation=self.operation,
                duration=elapsed,
                **self.metrics
            )
        else:
            # 예외 발생
            self.logger.error(
                "operation_failed",
                operation=self.operation,
                duration=elapsed,
                error=str(exc_val),
                **self.metrics
            )

    def add_metric(self, key: str, value: Any) -> None:
        """
        메트릭 추가

        Args:
            key: 메트릭 이름
            value: 메트릭 값
        """
        self.metrics[key] = value


# 초기화 (모듈 로드 시 자동 실행)
configure_logging()


# 사용 예시
if __name__ == "__main__":
    # 기본 로깅
    logger = get_logger(__name__)

    logger.debug("디버그 메시지", user_id=123)
    logger.info("정보 메시지", action="login", success=True)
    logger.warning("경고 메시지", disk_usage=95)
    logger.error("에러 메시지", error_code="DB_CONNECTION_FAILED")

    print("\n" + "="*60 + "\n")

    # API 로깅
    api_logger = APILogger("api_01")
    api_logger.log_request(
        "GET",
        "https://apis.data.go.kr/api",
        params={"LAWD_CD": "11680", "DEAL_YMD": "202312"}
    )
    api_logger.log_response(200, 0.5, item_count=10, total_count=100)
    api_logger.log_retry(2, 3, "Timeout")
    api_logger.log_error("Connection failed", error_code="TIMEOUT")

    print("\n" + "="*60 + "\n")

    # 성능 로깅
    with PerformanceLogger("data_processing") as perf:
        import time
        time.sleep(0.1)
        perf.add_metric("records_processed", 1000)
        perf.add_metric("errors", 0)

    print("\n" + "="*60 + "\n")

    # 예외 로깅
    try:
        raise ValueError("테스트 예외")
    except Exception as e:
        logger.error("예외 발생", exc_info=True)
