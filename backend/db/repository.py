"""
트랜잭션 데이터 저장소 (Repository Pattern)
data_loader.py의 데이터베이스 버전
"""
from typing import List, Dict, Optional, Tuple
from datetime import datetime, date
from sqlalchemy import func, and_, or_
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from .models import Transaction
from .session import get_session


class TransactionRepository:
    """
    트랜잭션 데이터 저장소

    data_loader.py의 load_all_json_data() 인터페이스를 대체하며
    동일한 형식의 데이터를 반환
    """

    def __init__(self, session: Optional[Session] = None):
        """
        Args:
            session: SQLAlchemy 세션 (None이면 자동 생성)
        """
        self.session = session
        self._auto_session = session is None

    def __enter__(self):
        if self._auto_session:
            self.session = get_session().__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._auto_session and self.session:
            if exc_type:
                self.session.rollback()
            else:
                self.session.commit()
            self.session.close()

    def load_all_transactions(self) -> Tuple[List[Dict], Dict]:
        """
        모든 거래 데이터 로드 (data_loader.load_all_json_data() 호환)

        Returns:
            (items 리스트, 디버깅 정보 딕셔너리)
            - items: 딕셔너리 형식의 거래 데이터 리스트
            - debug_info: 통계 정보
        """
        if not self.session:
            with get_session() as session:
                self.session = session
                return self._load_all_transactions_internal()
        else:
            return self._load_all_transactions_internal()

    def _load_all_transactions_internal(self) -> Tuple[List[Dict], Dict]:
        """내부 구현"""
        transactions = self.session.query(Transaction).all()

        # ORM 객체를 딕셔너리로 변환
        items = [t.to_dict() for t in transactions]

        # 통계 정보
        debug_info = {
            'successful_files': [],  # DB에서는 사용 안 함
            'failed_files': [],
            'total_files': 0,
            'total_items': len(items),
            'errors': [],
            'database_mode': True,
            'query_time_ms': 0,  # 필요시 측정
        }

        return items, debug_info

    def get_transactions(
        self,
        transaction_type: Optional[str] = None,
        region_code: Optional[str] = None,
        apt_name: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Dict]:
        """
        필터링된 거래 데이터 조회

        Args:
            transaction_type: API 타입 (api_01, api_02, etc.)
            region_code: 지역 코드 (sgg_cd)
            apt_name: 아파트 이름
            start_date: 시작 날짜
            end_date: 종료 날짜
            limit: 최대 결과 수
            offset: 오프셋

        Returns:
            딕셔너리 형식의 거래 데이터 리스트
        """
        if not self.session:
            with get_session() as session:
                self.session = session
                return self._get_transactions_internal(
                    transaction_type, region_code, apt_name,
                    start_date, end_date, limit, offset
                )
        else:
            return self._get_transactions_internal(
                transaction_type, region_code, apt_name,
                start_date, end_date, limit, offset
            )

    def _get_transactions_internal(
        self,
        transaction_type: Optional[str],
        region_code: Optional[str],
        apt_name: Optional[str],
        start_date: Optional[date],
        end_date: Optional[date],
        limit: Optional[int],
        offset: Optional[int],
    ) -> List[Dict]:
        """내부 구현"""
        query = self.session.query(Transaction)

        # 필터 적용
        if transaction_type:
            query = query.filter(Transaction.transaction_type == transaction_type)
        if region_code:
            query = query.filter(Transaction.sgg_cd == region_code)
        if apt_name:
            query = query.filter(Transaction.apt_nm.like(f'%{apt_name}%'))
        if start_date:
            query = query.filter(Transaction._deal_date >= start_date)
        if end_date:
            query = query.filter(Transaction._deal_date <= end_date)

        # 정렬 (최신순)
        query = query.order_by(Transaction._deal_date.desc())

        # 페이지네이션
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)

        transactions = query.all()
        return [t.to_dict() for t in transactions]

    def bulk_insert_transactions(
        self,
        items: List[Dict],
        batch_size: int = 1000,
        on_conflict: str = 'ignore'
    ) -> Dict[str, int]:
        """
        대량 삽입 (마이그레이션용)

        Args:
            items: 딕셔너리 형식의 거래 데이터 리스트
            batch_size: 배치 크기
            on_conflict: 충돌 시 처리 방법 ('ignore', 'update')

        Returns:
            {'inserted': N, 'updated': M, 'errors': E}
        """
        if not self.session:
            with get_session() as session:
                self.session = session
                return self._bulk_insert_internal(items, batch_size, on_conflict)
        else:
            return self._bulk_insert_internal(items, batch_size, on_conflict)

    def _bulk_insert_internal(
        self,
        items: List[Dict],
        batch_size: int,
        on_conflict: str
    ) -> Dict[str, int]:
        """내부 구현"""
        stats = {'inserted': 0, 'updated': 0, 'errors': 0}

        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]

            try:
                # 모든 경우에 Transaction.from_dict 사용 (normalized fields 자동 생성)
                transactions = [Transaction.from_dict(item) for item in batch]

                if on_conflict == 'ignore':
                    # PostgreSQL INSERT ... ON CONFLICT DO NOTHING
                    for transaction in transactions:
                        stmt = insert(Transaction).values(
                            **{c.name: getattr(transaction, c.name) for c in Transaction.__table__.columns if c.name != 'id'}
                        )
                        stmt = stmt.on_conflict_do_nothing(
                            constraint='unique_transaction'
                        )
                        result = self.session.execute(stmt)
                        stats['inserted'] += result.rowcount

                elif on_conflict == 'update':
                    # PostgreSQL INSERT ... ON CONFLICT DO UPDATE
                    for transaction in transactions:
                        stmt = insert(Transaction).values(
                            **{c.name: getattr(transaction, c.name) for c in Transaction.__table__.columns if c.name != 'id'}
                        )
                        # 업데이트할 필드만 지정
                        update_dict = {
                            '_deal_amount_numeric': transaction._deal_amount_numeric,
                            '_area_numeric': transaction._area_numeric,
                        }
                        stmt = stmt.on_conflict_do_update(
                            constraint='unique_transaction',
                            set_=update_dict
                        )
                        result = self.session.execute(stmt)
                        stats['updated'] += result.rowcount

                else:
                    # 기본 삽입 (중복 시 에러)
                    for transaction in transactions:
                        self.session.add(transaction)
                    self.session.flush()
                    stats['inserted'] += len(batch)

            except Exception as e:
                print(f"배치 삽입 오류 (batch {i}-{i+batch_size}): {e}")
                stats['errors'] += len(batch)
                self.session.rollback()

        self.session.commit()
        return stats

    def _dict_to_insert_values(self, data: Dict) -> Dict:
        """딕셔너리를 INSERT VALUES로 변환"""
        return {
            'transaction_type': data.get('_api_type', ''),
            'source_file': data.get('_source_file', ''),
            'apt_seq': data.get('aptSeq', ''),
            'apt_nm': data.get('아파트', ''),
            'excl_use_ar': data.get('전용면적', ''),
            'build_year': data.get('건축년도', ''),
            'umd_nm': data.get('법정동', ''),
            'jibun': data.get('지번', ''),
            'sgg_cd': data.get('지역코드', ''),
            'floor': data.get('층', ''),
            'deal_amount': data.get('거래금액', ''),
            'deal_year': data.get('년', ''),
            'deal_month': data.get('월', ''),
            'deal_day': data.get('일', ''),
            'deposit': data.get('보증금액', ''),
            'monthly_rent': data.get('월세금액', ''),
            'contract_term': data.get('계약기간', ''),
            'contract_type': data.get('계약유형', ''),
            'buyer_gbn': data.get('매수자', ''),
            'seller_gbn': data.get('매도자', ''),
            'deal_gbn': data.get('거래유형', ''),
            'cancel_deal_day': data.get('해제사유발생일', ''),
            'cancel_deal_type': data.get('해제여부', ''),
            '_deal_amount_numeric': data.get('_deal_amount_numeric'),
            '_area_numeric': data.get('_area_numeric'),
            '_deal_date': datetime.strptime(data['_deal_date'], '%Y-%m-%d').date() if data.get('_deal_date') else None,
            '_year_month': data.get('_year_month'),
            '_build_year_int': data.get('_build_year'),
            '_floor_int': data.get('_floor'),
            '_deposit_numeric': data.get('_deposit_numeric'),
            '_monthly_rent_numeric': data.get('_monthly_rent_numeric'),
            '_region_name': data.get('_region_name'),
        }

    def _dict_to_update_values(self, data: Dict) -> Dict:
        """UPDATE SET 절 생성"""
        # 필요시 업데이트할 필드 지정
        return {
            '_deal_amount_numeric': data.get('_deal_amount_numeric'),
            '_area_numeric': data.get('_area_numeric'),
        }

    def get_statistics(self) -> Dict:
        """
        데이터베이스 통계 정보

        Returns:
            {'total': N, 'by_type': {...}, 'date_range': (...)}
        """
        if not self.session:
            with get_session() as session:
                self.session = session
                return self._get_statistics_internal()
        else:
            return self._get_statistics_internal()

    def _get_statistics_internal(self) -> Dict:
        """내부 구현"""
        total = self.session.query(func.count(Transaction.id)).scalar()

        # API 타입별 통계
        by_type = {}
        type_stats = self.session.query(
            Transaction.transaction_type,
            func.count(Transaction.id)
        ).group_by(Transaction.transaction_type).all()

        for api_type, count in type_stats:
            by_type[api_type] = count

        # 날짜 범위
        date_range = self.session.query(
            func.min(Transaction._deal_date),
            func.max(Transaction._deal_date)
        ).first()

        return {
            'total': total,
            'by_type': by_type,
            'date_range': {
                'min': date_range[0].isoformat() if date_range[0] else None,
                'max': date_range[1].isoformat() if date_range[1] else None,
            }
        }
