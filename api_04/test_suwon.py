#!/usr/bin/env python3
"""
수원시 권선구 테스트 스크립트 (API 04)
"""
import sys
from pathlib import Path
from datetime import datetime
import json

# 상위 디렉토리를 path에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from api_04.api_04_apt_rent import AptRentAPI


def test_suwon_gwonseon():
    """수원시 권선구 테스트"""
    api = AptRentAPI()
    
    # 수원시 권선구 지역코드 (41113)
    lawd_cd = '41113'
    
    # 현재 시간부터 3년 전까지의 기간 생성
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    
    # 3년 전부터 현재까지의 모든 월 생성
    test_periods = []
    for year in range(current_year - 3, current_year + 1):
        # 시작 월 결정
        start_month = 1
        if year == current_year - 3:
            # 3년 전의 경우, 현재 월과 같은 월부터 시작 (예: 현재가 1월이면 1월부터)
            start_month = current_month
        
        # 종료 월 결정
        end_month = 12
        if year == current_year:
            # 현재 년도의 경우, 현재 월까지만
            end_month = current_month
        
        # 해당 년도의 모든 월 추가
        for month in range(start_month, end_month + 1):
            test_periods.append(f"{year}{month:02d}")
    
    # 최신순으로 정렬 (최신이 먼저)
    test_periods.reverse()
    
    print("=" * 70)
    print("수원시 권선구 전월세 실거래가 테스트")
    print("=" * 70)
    print(f"지역코드: {lawd_cd} (수원시 권선구)")
    print("=" * 70)
    
    results = []
    
    for deal_ymd in test_periods:
        print(f"\n{'='*70}")
        print(f"테스트 기간: {deal_ymd}")
        print(f"{'='*70}")
        
        start_time = datetime.now()
        result = api.get_trade_data_parsed(lawd_cd, deal_ymd)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        if result.get('error'):
            print(f"❌ 오류: {result.get('message', result.get('result_msg', 'Unknown error'))}")
        else:
            total_count = result.get('total_count', 0)
            item_count = result.get('item_count', 0)
            
            if total_count > 0:
                print(f"✅ 성공 - 데이터 발견!")
                print(f"   전체 건수: {total_count}")
                print(f"   조회된 건수: {item_count}")
                print(f"   응답 시간: {duration:.2f}초")
                
                # 거래 정보 출력
                items = result.get('items', [])
                if items:
                    print(f"\n   거래 정보:")
                    for idx, item in enumerate(items[:5], 1):  # 최대 5건만
                        apt_name = item.get('aptNm') or item.get('아파트', 'N/A')
                        deal_amount = item.get('dealAmount') or item.get('거래금액', 'N/A')
                        rent_type = item.get('거래유형') or item.get('rentGb', 'N/A')
                        area = item.get('excluUseAr') or item.get('전용면적', 'N/A')
                        dong = item.get('umdNm') or item.get('법정동', 'N/A')
                        print(f"   [{idx}] {apt_name} ({dong}) - {rent_type} {deal_amount}만원 ({area}㎡)")
            else:
                print(f"⚠️  성공 (데이터 없음)")
                print(f"   응답 시간: {duration:.2f}초")
        
        results.append({
            'period': deal_ymd,
            'result': result,
            'duration': duration
        })
    
    # 결과 요약
    print(f"\n{'='*70}")
    print("테스트 요약")
    print(f"{'='*70}")
    
    total_tests = len(results)
    data_found = sum(1 for r in results if r['result'].get('total_count', 0) > 0)
    no_data = total_tests - data_found
    
    # 전세/월세 통계
    total_jeonse = 0
    total_wolse = 0
    for r in results:
        if r['result'].get('total_count', 0) > 0:
            items = r['result'].get('items', [])
            for item in items:
                rent_type = item.get('거래유형') or item.get('rentGb', '')
                if rent_type == '전세':
                    total_jeonse += 1
                elif rent_type == '월세':
                    total_wolse += 1
    
    print(f"전체 테스트: {total_tests}건")
    print(f"데이터 발견: {data_found}건")
    print(f"데이터 없음: {no_data}건")
    print(f"전세: {total_jeonse}건")
    print(f"월세: {total_wolse}건")
    
    # 데이터가 있는 기간 출력
    if data_found > 0:
        print(f"\n데이터가 있는 기간:")
        for r in results:
            if r['result'].get('total_count', 0) > 0:
                print(f"  - {r['period']}: {r['result'].get('total_count')}건")
    
    # 보고서 저장
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = output_dir / f"test_suwon_gwonseon_{timestamp}.md"
    
    report_content = f"""# 수원시 권선구 테스트 결과 보고서 (API 04)

## 테스트 정보
- **테스트 일시**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **지역**: 수원시 권선구
- **지역코드**: 41113
- **API**: 아파트 전월세 실거래가 자료

## 테스트 요약
- **전체 테스트 수**: {total_tests}
- **데이터 발견**: {data_found}건
- **데이터 없음**: {no_data}건
- **전세**: {total_jeonse}건
- **월세**: {total_wolse}건

---

## 상세 결과

"""
    
    for r in results:
        result = r['result']
        period = r['period']
        
        report_content += f"""### {period} (계약년월)

"""
        
        if result.get('error'):
            report_content += f"**상태**: ❌ 오류\n"
            report_content += f"**오류 메시지**: {result.get('message', result.get('result_msg', 'Unknown error'))}\n\n"
        else:
            total_count = result.get('total_count', 0)
            if total_count > 0:
                report_content += f"**상태**: ✅ 데이터 발견\n"
                report_content += f"**전체 건수**: {total_count}\n"
                report_content += f"**조회된 건수**: {result.get('item_count', 0)}\n"
                report_content += f"**응답 시간**: {r['duration']:.2f}초\n\n"
                
                items = result.get('items', [])
                if items:
                    report_content += "**거래 정보**:\n\n"
                    for idx, item in enumerate(items, 1):
                        apt_name = item.get('aptNm') or item.get('아파트', 'N/A')
                        dong = item.get('umdNm') or item.get('법정동', 'N/A')
                        sgg_nm = item.get('sggNm', 'N/A')
                        deal_amount = item.get('dealAmount') or item.get('거래금액', 'N/A')
                        area = item.get('excluUseAr') or item.get('전용면적', 'N/A')
                        floor = item.get('floor') or item.get('층', 'N/A')
                        rent_type = item.get('거래유형') or item.get('rentGb', 'N/A')
                        year = item.get('dealYear') or item.get('년', 'N/A')
                        month = item.get('dealMonth') or item.get('월', 'N/A')
                        day = item.get('dealDay') or item.get('일', 'N/A')
                        
                        if month != 'N/A' and day != 'N/A':
                            deal_date = f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"
                        else:
                            deal_date = 'N/A'
                        
                        report_content += f"""#### 거래 {idx}
- **아파트명**: {apt_name}
- **지역**: {sgg_nm} {dong}
- **거래유형**: {rent_type}
- **거래금액**: {deal_amount}만원
"""
                        
                        # 전세/월세 금액 파싱
                        if deal_amount != 'N/A' and rent_type != 'N/A':
                            parsed_amount = api.parse_rent_amount(deal_amount, rent_type)
                            if rent_type == '전세':
                                report_content += f"- **보증금**: {parsed_amount['deposit']:,}원\n"
                            elif rent_type == '월세':
                                report_content += f"- **보증금**: {parsed_amount['deposit']:,}원\n"
                                if parsed_amount['monthly']:
                                    report_content += f"- **월세**: {parsed_amount['monthly']:,}원\n"
                        
                        report_content += f"""- **전용면적**: {area}㎡
- **층수**: {floor}층
- **거래일자**: {deal_date}
- **지번**: {item.get('jibun') or item.get('지번', 'N/A')}

"""
            else:
                report_content += f"**상태**: ⚠️ 데이터 없음\n"
                report_content += f"**응답 시간**: {r['duration']:.2f}초\n\n"
        
        report_content += "---\n\n"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"\n보고서 저장: {report_file}")


if __name__ == "__main__":
    test_suwon_gwonseon()
