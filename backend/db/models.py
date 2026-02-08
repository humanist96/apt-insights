"""
SQLAlchemy ORM 모델
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from sqlalchemy import (
    Column, Integer, String, DateTime, Date, Numeric,
    UniqueConstraint, Index
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Transaction(Base):
    """
    아파트 실거래가 데이터 모델 (통합: API 01~04)

    - 48개 원본 필드 (JSON 필드 그대로)
    - 9개 정규화 필드 (_ prefix)
    """
    __tablename__ = 'transactions'

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # API 메타 정보
    transaction_type = Column(String(10), nullable=False, comment='API 타입')
    source_file = Column(String(500), comment='소스 JSON 파일 경로')
    created_at = Column(DateTime, default=datetime.now, comment='생성 시각')

    # 아파트 정보
    apt_seq = Column(String(50), comment='아파트 일련번호')
    apt_nm = Column(String(100), comment='아파트 이름')
    excl_use_ar = Column(String(20), comment='전용면적')
    build_year = Column(String(4), comment='건축년도')

    # 위치 정보
    umd_nm = Column(String(100), comment='읍면동명')
    jibun = Column(String(50), comment='지번')
    sgg_cd = Column(String(5), comment='시군구 코드')
    floor = Column(String(10), comment='층')

    # 거래 정보
    deal_amount = Column(String(50), comment='거래금액 (문자열)')
    deal_year = Column(String(4), comment='거래년도')
    deal_month = Column(String(2), comment='거래월')
    deal_day = Column(String(2), comment='거래일')
    req_gbn = Column(String(10), comment='요청구분')

    # 전월세 정보 (API 04)
    deposit = Column(String(50), comment='보증금')
    monthly_rent = Column(String(50), comment='월세금')
    previous_contract_deposit = Column(String(50), comment='종전 계약 보증금')
    previous_contract_monthly_rent = Column(String(50), comment='종전 계약 월세')
    contract_term = Column(String(50), comment='계약기간')
    contract_type = Column(String(20), comment='계약유형')
    contract_gbn = Column(String(10), comment='계약구분')

    # 상세 정보 (API 03)
    buyer_gbn = Column(String(20), comment='매수자 구분')
    seller_gbn = Column(String(20), comment='매도자 구분')
    registration_gbn = Column(String(20), comment='등기 구분')
    deal_gbn = Column(String(20), comment='거래 구분')
    cancel_deal_day = Column(String(10), comment='해제 사유 발생일')
    cancel_deal_type = Column(String(20), comment='해제 여부')
    dealer_lawdnm = Column(String(100), comment='중개사 소재지 법정동')
    dealer_sigungu = Column(String(100), comment='중개사 소재지 시군구')

    # 정규화된 필드 (9 fields with _ prefix)
    _deal_amount_numeric = Column(Numeric(15, 2), comment='거래금액 (숫자)')
    _area_numeric = Column(Numeric(10, 2), comment='면적 (숫자)')
    _deal_date = Column(Date, comment='거래일자 (DATE)')
    _year_month = Column(String(6), comment='년월 (YYYYMM)')
    _build_year_int = Column(Integer, comment='건축년도 (정수)')
    _floor_int = Column(Integer, comment='층 (정수)')
    _deposit_numeric = Column(Numeric(15, 2), comment='보증금 (숫자)')
    _monthly_rent_numeric = Column(Numeric(15, 2), comment='월세 (숫자)')
    _region_name = Column(String(100), comment='지역명')

    # Unique Constraint (중복 방지)
    __table_args__ = (
        UniqueConstraint(
            'transaction_type', 'apt_seq', 'deal_year', 'deal_month', 'deal_day', 'deal_amount',
            name='unique_transaction'
        ),
        Index('idx_deal_date', '_deal_date'),
        Index('idx_region', 'sgg_cd'),
        Index('idx_transaction_type', 'transaction_type'),
        Index('idx_apt_nm', 'apt_nm'),
        Index('idx_year_month', '_year_month'),
        Index('idx_apt_seq', 'apt_seq'),
        Index('idx_composite_region_date', 'sgg_cd', '_deal_date'),
    )

    def __repr__(self):
        return (
            f"<Transaction(id={self.id}, type={self.transaction_type}, "
            f"apt={self.apt_nm}, date={self._deal_date}, amount={self._deal_amount_numeric})>"
        )

    def to_dict(self) -> dict:
        """
        ORM 객체를 딕셔너리로 변환 (data_loader.py 형식과 동일)
        """
        return {
            # 원본 필드
            'aptSeq': self.apt_seq,
            '아파트': self.apt_nm,
            '전용면적': self.excl_use_ar,
            '건축년도': self.build_year,
            '법정동': self.umd_nm,
            '지번': self.jibun,
            '지역코드': self.sgg_cd,
            '층': self.floor,
            '거래금액': self.deal_amount,
            '년': self.deal_year,
            '월': self.deal_month,
            '일': self.deal_day,
            '보증금액': self.deposit,
            '월세금액': self.monthly_rent,
            '계약기간': self.contract_term,
            '계약유형': self.contract_type,
            '매수자': self.buyer_gbn,
            '매도자': self.seller_gbn,
            '거래유형': self.deal_gbn,
            '해제사유발생일': self.cancel_deal_day,
            '해제여부': self.cancel_deal_type,

            # 메타 정보
            '_api_type': self.transaction_type,
            '_source_file': self.source_file,

            # 정규화된 필드
            '_deal_amount_numeric': float(self._deal_amount_numeric) if self._deal_amount_numeric else None,
            '_area_numeric': float(self._area_numeric) if self._area_numeric else None,
            '_deal_date': self._deal_date.isoformat() if self._deal_date else None,
            '_year_month': self._year_month,
            '_build_year': self._build_year_int,
            '_floor': self._floor_int,
            '_deposit_numeric': float(self._deposit_numeric) if self._deposit_numeric else None,
            '_monthly_rent_numeric': float(self._monthly_rent_numeric) if self._monthly_rent_numeric else None,
            '_region_name': self._region_name,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Transaction':
        """
        딕셔너리에서 ORM 객체 생성 (JSON 데이터 마이그레이션용)

        Normalized fields가 없으면 자동으로 생성합니다.
        """
        import re

        # 원본 필드 추출 (영문/한글 모두 지원)
        deal_year = data.get('dealYear') or data.get('년', '')
        deal_month = data.get('dealMonth') or data.get('월', '')
        deal_day = data.get('dealDay') or data.get('일', '')
        deal_amount = data.get('dealAmount') or data.get('거래금액', '')
        excl_use_ar = data.get('excluUseAr') or data.get('전용면적', '')
        build_year = data.get('buildYear') or data.get('건축년도', '')
        floor = data.get('floor') or data.get('층', '')
        deposit = data.get('deposit') or data.get('보증금액', '')
        monthly_rent = data.get('monthlyRent') or data.get('월세금액', '')
        umd_nm = data.get('umdNm') or data.get('법정동', '')

        # Normalized fields 자동 생성 (없으면)

        # 1. _deal_date (YYYY-MM-DD)
        deal_date = data.get('_deal_date')
        if not deal_date and deal_year and deal_month and deal_day:
            try:
                year = deal_year.strip()
                month = deal_month.strip().zfill(2)
                day = deal_day.strip().zfill(2)
                deal_date_str = f"{year}-{month}-{day}"
                deal_date = datetime.strptime(deal_date_str, '%Y-%m-%d').date()
            except:
                deal_date = None
        elif isinstance(deal_date, str):
            try:
                deal_date = datetime.strptime(deal_date, '%Y-%m-%d').date()
            except:
                deal_date = None

        # 2. _year_month (YYYYMM)
        year_month = data.get('_year_month')
        if not year_month and deal_year and deal_month:
            year_month = f"{deal_year.strip()}{deal_month.strip().zfill(2)}"

        # 3. _deal_amount_numeric
        deal_amount_numeric = data.get('_deal_amount_numeric')
        if deal_amount_numeric is None and deal_amount:
            try:
                amount_str = re.sub(r'[^\d.]', '', str(deal_amount))
                deal_amount_numeric = Decimal(amount_str) if amount_str else None
            except:
                deal_amount_numeric = None

        # 4. _area_numeric
        area_numeric = data.get('_area_numeric')
        if area_numeric is None and excl_use_ar:
            try:
                area_str = re.sub(r'[^\d.]', '', str(excl_use_ar))
                area_numeric = Decimal(area_str) if area_str else None
            except:
                area_numeric = None

        # 5. _build_year_int
        build_year_int = data.get('_build_year')
        if build_year_int is None and build_year:
            try:
                build_year_int = int(re.sub(r'[^\d]', '', str(build_year)))
            except:
                build_year_int = None

        # 6. _floor_int
        floor_int = data.get('_floor')
        if floor_int is None and floor:
            try:
                floor_int = int(re.sub(r'[^\d]', '', str(floor)))
            except:
                floor_int = None

        # 7. _deposit_numeric
        deposit_numeric = data.get('_deposit_numeric')
        if deposit_numeric is None and deposit:
            try:
                deposit_str = re.sub(r'[^\d.]', '', str(deposit))
                deposit_numeric = Decimal(deposit_str) if deposit_str else None
            except:
                deposit_numeric = None

        # 8. _monthly_rent_numeric
        monthly_rent_numeric = data.get('_monthly_rent_numeric')
        if monthly_rent_numeric is None and monthly_rent:
            try:
                rent_str = re.sub(r'[^\d.]', '', str(monthly_rent))
                monthly_rent_numeric = Decimal(rent_str) if rent_str else None
            except:
                monthly_rent_numeric = None

        # 9. _region_name
        region_name = data.get('_region_name', umd_nm)

        return cls(
            # API 메타 정보
            transaction_type=data.get('_api_type', ''),
            source_file=data.get('_source_file', ''),

            # 아파트 정보 (영문/한글 모두 지원)
            apt_seq=data.get('aptSeq', ''),
            apt_nm=data.get('aptNm') or data.get('아파트', ''),
            excl_use_ar=excl_use_ar,
            build_year=build_year,

            # 위치 정보
            umd_nm=umd_nm,
            jibun=data.get('jibun') or data.get('지번', ''),
            sgg_cd=data.get('sggCd') or data.get('지역코드', ''),
            floor=floor,

            # 거래 정보
            deal_amount=deal_amount,
            deal_year=str(deal_year) if deal_year else '',
            deal_month=str(deal_month) if deal_month else '',
            deal_day=str(deal_day) if deal_day else '',
            req_gbn=data.get('reqGbn') or data.get('req_gbn', ''),

            # 전월세 정보
            deposit=deposit,
            monthly_rent=monthly_rent,
            previous_contract_deposit=data.get('priorDpsit') or data.get('종전계약보증금', ''),
            previous_contract_monthly_rent=data.get('priorMtRentAmt') or data.get('종전계약월세', ''),
            contract_term=data.get('cntrctPrd') or data.get('계약기간', ''),
            contract_type=data.get('cntrctTp') or data.get('계약유형', ''),
            contract_gbn=data.get('renewRightOptnUseYn') or data.get('갱신요구권사용', ''),

            # 상세 정보
            buyer_gbn=data.get('buyerGbn') or data.get('매수자', ''),
            seller_gbn=data.get('slerGbn') or data.get('매도자', ''),
            registration_gbn=data.get('ownershipGbn') or data.get('등기여부', ''),
            deal_gbn=data.get('dealingGbn') or data.get('거래유형', ''),
            cancel_deal_day=data.get('cdealDay') or data.get('해제사유발생일', ''),
            cancel_deal_type=data.get('cdealType') or data.get('해제여부', ''),
            dealer_lawdnm=data.get('estateAgentSggNm') or data.get('중개사소재지', ''),
            dealer_sigungu=data.get('dealer_sigungu', ''),

            # 정규화된 필드 (자동 생성됨)
            _deal_amount_numeric=deal_amount_numeric,
            _area_numeric=area_numeric,
            _deal_date=deal_date,
            _year_month=year_month,
            _build_year_int=build_year_int,
            _floor_int=floor_int,
            _deposit_numeric=deposit_numeric,
            _monthly_rent_numeric=monthly_rent_numeric,
            _region_name=region_name,
        )
