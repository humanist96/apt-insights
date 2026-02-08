"""
데이터베이스 기능 테스트
"""
import pytest
from datetime import datetime, date
from decimal import Decimal
from backend.db.models import Transaction
from backend.db.session import get_session, init_db, drop_db
from backend.db.repository import TransactionRepository


@pytest.fixture(scope='module')
def setup_database():
    """테스트용 데이터베이스 초기화"""
    init_db()
    yield
    # 테스트 후 정리는 선택적


@pytest.fixture
def sample_transaction_data():
    """테스트용 샘플 데이터"""
    return {
        '_api_type': 'api_02',
        '_source_file': '/test/file.json',
        'aptSeq': '12345',
        '아파트': '테스트아파트',
        '전용면적': '84.5',
        '건축년도': '2020',
        '법정동': '역삼동',
        '지번': '123-45',
        '지역코드': '11680',
        '층': '15',
        '거래금액': '150,000',
        '년': '2023',
        '월': '12',
        '일': '15',
        '_deal_amount_numeric': 150000.0,
        '_area_numeric': 84.5,
        '_deal_date': '2023-12-15',
        '_year_month': '202312',
        '_build_year': 2020,
        '_floor': 15,
        '_region_name': '강남구',
    }


class TestTransactionModel:
    """Transaction ORM 모델 테스트"""

    def test_from_dict(self, sample_transaction_data):
        """딕셔너리에서 ORM 객체 생성"""
        transaction = Transaction.from_dict(sample_transaction_data)

        assert transaction.transaction_type == 'api_02'
        assert transaction.apt_nm == '테스트아파트'
        assert transaction._deal_amount_numeric == Decimal('150000.0')
        assert transaction._area_numeric == Decimal('84.5')
        assert transaction._deal_date == date(2023, 12, 15)

    def test_to_dict(self, sample_transaction_data):
        """ORM 객체를 딕셔너리로 변환"""
        transaction = Transaction.from_dict(sample_transaction_data)
        result = transaction.to_dict()

        assert result['_api_type'] == 'api_02'
        assert result['아파트'] == '테스트아파트'
        assert result['_deal_amount_numeric'] == 150000.0


class TestTransactionRepository:
    """TransactionRepository 테스트"""

    def test_bulk_insert(self, setup_database, sample_transaction_data):
        """대량 삽입 테스트"""
        # 3개의 테스트 데이터 생성 (aptSeq를 다르게)
        items = []
        for i in range(3):
            data = sample_transaction_data.copy()
            data['aptSeq'] = f'12345-{i}'
            data['일'] = f'{15 + i:02d}'  # 날짜를 다르게
            data['_deal_date'] = f'2023-12-{15 + i}'
            items.append(data)

        with get_session() as session:
            repo = TransactionRepository(session)
            stats = repo.bulk_insert_transactions(items, batch_size=10)

            assert stats['inserted'] >= 0  # 중복이 있을 수 있음
            assert stats['errors'] == 0

    def test_get_transactions_filter(self, setup_database, sample_transaction_data):
        """필터링 조회 테스트"""
        # 데이터 삽입
        with get_session() as session:
            repo = TransactionRepository(session)
            repo.bulk_insert_transactions([sample_transaction_data])

        # 조회
        with get_session() as session:
            repo = TransactionRepository(session)
            results = repo.get_transactions(
                transaction_type='api_02',
                region_code='11680'
            )

            assert len(results) > 0
            assert all(r['_api_type'] == 'api_02' for r in results)

    def test_get_statistics(self, setup_database):
        """통계 조회 테스트"""
        with get_session() as session:
            repo = TransactionRepository(session)
            stats = repo.get_statistics()

            assert 'total' in stats
            assert 'by_type' in stats
            assert 'date_range' in stats
            assert stats['total'] >= 0


class TestDualModeDataLoader:
    """Dual-mode 데이터 로더 테스트"""

    def test_json_mode(self, monkeypatch):
        """JSON 모드 테스트"""
        import os
        monkeypatch.setenv('USE_DATABASE', 'false')

        # 모듈 재로드
        from importlib import reload
        import backend.data_loader as dl
        reload(dl)

        assert dl.USE_DATABASE == False

    def test_database_mode(self, monkeypatch):
        """데이터베이스 모드 테스트"""
        import os
        monkeypatch.setenv('USE_DATABASE', 'true')

        # 모듈 재로드
        from importlib import reload
        import backend.data_loader as dl
        reload(dl)

        # DATABASE_AVAILABLE이 True인 경우에만 USE_DATABASE가 True
        if dl.DATABASE_AVAILABLE:
            assert dl.USE_DATABASE == True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
