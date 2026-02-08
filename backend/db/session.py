"""
데이터베이스 세션 관리
"""
import os
from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv

from .models import Base

# .env 파일 로드
load_dotenv()

# 데이터베이스 URL 설정
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:postgres@localhost:5432/apt_insights'
)

# 엔진 생성
# - pool_pre_ping: 연결 유효성 자동 체크
# - echo: SQL 쿼리 로그 (개발 시 True, 운영 시 False)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=os.getenv('SQL_ECHO', 'False').lower() == 'true',
    poolclass=NullPool if os.getenv('USE_NULL_POOL', 'False').lower() == 'true' else None,
)

# 세션 팩토리
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def init_db():
    """
    데이터베이스 초기화 (테이블 생성)
    """
    Base.metadata.create_all(bind=engine)


def drop_db():
    """
    데이터베이스 삭제 (모든 테이블 삭제)
    주의: 운영 환경에서 사용 금지
    """
    Base.metadata.drop_all(bind=engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """
    데이터베이스 세션 컨텍스트 매니저

    Usage:
        with get_session() as session:
            result = session.query(Transaction).all()
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_session_direct() -> Session:
    """
    직접 세션 반환 (FastAPI Depends 등에서 사용)

    Usage:
        @app.get("/transactions")
        def get_transactions(session: Session = Depends(get_session_direct)):
            return session.query(Transaction).all()
    """
    return SessionLocal()
