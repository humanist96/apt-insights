#!/usr/bin/env python3
"""
API 04 CLI 실행 스크립트
"""
import sys
from pathlib import Path

# 상위 디렉토리를 path에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from api_04.api_04_apt_rent import AptRentAPI
import json


def main():
    """CLI 테스트 함수"""
    # 기본 테스트 파라미터
    lawd_cd = '11110'  # 종로구
    deal_ymd = '202401'  # 2024년 1월
    
    # 커맨드라인 인자 처리
    if len(sys.argv) > 1:
        lawd_cd = sys.argv[1]
    if len(sys.argv) > 2:
        deal_ymd = sys.argv[2]
    
    print("=" * 60)
    print("API 04: 아파트 전월세 실거래가 자료 테스트")
    print("=" * 60)
    print(f"지역코드: {lawd_cd}")
    print(f"계약년월: {deal_ymd}")
    print("-" * 60)
    
    # API 호출
    api = AptRentAPI()
    result = api.get_trade_data_parsed(lawd_cd, deal_ymd)
    
    # 결과 출력
    if result.get('error'):
        print("❌ 오류 발생:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("✅ 성공:")
        print(f"결과 코드: {result.get('result_code')}")
        print(f"결과 메시지: {result.get('result_msg')}")
        print(f"전체 건수: {result.get('total_count')}")
        print(f"현재 페이지 결과 수: {result.get('item_count')}")
        print("-" * 60)
        
        items = result.get('items', [])
        if items:
            print("\n거래 정보:")
            for idx, item in enumerate(items, 1):
                print(f"\n[{idx}]")
                # 필드명 매핑 (한글/영문 모두 지원)
                apt_name = item.get('아파트') or item.get('aptNm') or item.get('apt', 'N/A')
                dong = item.get('법정동') or item.get('umdNm') or item.get('법정동명', 'N/A')
                deal_amount = item.get('거래금액') or item.get('dealAmount') or item.get('거래가격', 'N/A')
                area = item.get('전용면적') or item.get('excluUseAr') or item.get('면적', 'N/A')
                floor = item.get('층') or item.get('floor') or item.get('층수', 'N/A')
                build_year = item.get('건축년도') or item.get('buildYear') or item.get('건축연도', 'N/A')
                rent_type = item.get('거래유형') or item.get('rentGb', 'N/A')
                
                # 거래일자
                year = item.get('년') or item.get('dealYear') or item.get('year', 'N/A')
                month = item.get('월') or item.get('dealMonth') or item.get('month', 'N/A')
                day = item.get('일') or item.get('dealDay') or item.get('day', 'N/A')
                
                if month != 'N/A' and day != 'N/A':
                    deal_date = f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"
                else:
                    deal_date = 'N/A'
                
                print(f"  아파트명: {apt_name}")
                print(f"  지역: {item.get('sggNm', 'N/A')} {dong}")
                print(f"  거래유형: {rent_type}")
                
                # 전세/월세 금액 파싱
                if deal_amount != 'N/A' and rent_type != 'N/A':
                    parsed_amount = api.parse_rent_amount(deal_amount, rent_type)
                    if rent_type == '전세':
                        print(f"  보증금: {parsed_amount['deposit']:,}원 ({deal_amount}만원)")
                    elif rent_type == '월세':
                        print(f"  보증금: {parsed_amount['deposit']:,}원 ({deal_amount.split('/')[0] if '/' in deal_amount else deal_amount}만원)")
                        if parsed_amount['monthly']:
                            print(f"  월세: {parsed_amount['monthly']:,}원 ({deal_amount.split('/')[1] if '/' in deal_amount else 'N/A'}만원)")
                else:
                    print(f"  거래금액: {deal_amount}만원")
                
                print(f"  전용면적: {area}㎡")
                print(f"  층수: {floor}층")
                if build_year != 'N/A':
                    print(f"  건축년도: {build_year}년")
                print(f"  거래일자: {deal_date}")
                print(f"  지번: {item.get('지번') or item.get('jibun') or 'N/A'}")
        else:
            print("\n조회된 데이터가 없습니다.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
