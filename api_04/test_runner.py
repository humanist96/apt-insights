#!/usr/bin/env python3
"""
API 04 테스트 실행 스크립트
여러 테스트 케이스를 실행하고 결과를 보고서로 저장합니다.
"""
import sys
from pathlib import Path
from datetime import datetime
import json

# 상위 디렉토리를 path에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from api_04.api_04_apt_rent import AptRentAPI


class TestRunner:
    """테스트 실행 및 결과 수집 클래스"""
    
    def __init__(self):
        self.api = AptRentAPI()
        self.results = []
        self.output_dir = Path(__file__).parent / 'output'
        self.output_dir.mkdir(exist_ok=True)
    
    def run_test_case(self, name: str, lawd_cd: str, deal_ymd: str, description: str = ""):
        """
        단일 테스트 케이스 실행
        
        Args:
            name: 테스트 케이스 이름
            lawd_cd: 지역코드
            deal_ymd: 계약년월
            description: 테스트 설명
        """
        print(f"\n{'='*60}")
        print(f"테스트 케이스: {name}")
        print(f"{'='*60}")
        if description:
            print(f"설명: {description}")
        print(f"지역코드: {lawd_cd}")
        print(f"계약년월: {deal_ymd}")
        print("-" * 60)
        
        start_time = datetime.now()
        result = self.api.get_trade_data_parsed(lawd_cd, deal_ymd)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        test_result = {
            'test_name': name,
            'description': description,
            'lawd_cd': lawd_cd,
            'deal_ymd': deal_ymd,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'duration_seconds': duration,
            'success': not result.get('error', False),
            'result': result
        }
        
        self.results.append(test_result)
        
        # 결과 출력
        if result.get('error'):
            print("❌ 실패")
            print(f"오류 메시지: {result.get('message', result.get('result_msg', 'Unknown error'))}")
        else:
            print("✅ 성공")
            print(f"결과 코드: {result.get('result_code')}")
            print(f"결과 메시지: {result.get('result_msg')}")
            print(f"전체 건수: {result.get('total_count')}")
            print(f"조회된 건수: {result.get('item_count')}")
            print(f"응답 시간: {duration:.2f}초")
            
            if result.get('items'):
                print("\n거래 정보 샘플 (최대 3건):")
                for idx, item in enumerate(result.get('items', [])[:3], 1):
                    apt_name = item.get('aptNm') or item.get('아파트', 'N/A')
                    deal_amount = item.get('dealAmount') or item.get('거래금액', 'N/A')
                    rent_type = item.get('거래유형') or item.get('rentGb', 'N/A')
                    print(f"  [{idx}] {apt_name} - {rent_type} {deal_amount}만원")
        
        return test_result
    
    def generate_report(self):
        """테스트 결과 보고서 생성"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.output_dir / f"test_report_{timestamp}.md"
        json_file = self.output_dir / f"test_results_{timestamp}.json"
        
        # 통계 계산
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r['success'])
        failed_tests = total_tests - successful_tests
        total_duration = sum(r['duration_seconds'] for r in self.results)
        avg_duration = total_duration / total_tests if total_tests > 0 else 0
        
        # 전세/월세 통계 계산
        total_jeonse = 0
        total_wolse = 0
        for r in self.results:
            if r['success']:
                items = r['result'].get('items', [])
                for item in items:
                    rent_type = item.get('거래유형') or item.get('rentGb', '')
                    if rent_type == '전세':
                        total_jeonse += 1
                    elif rent_type == '월세':
                        total_wolse += 1
        
        # 마크다운 보고서 생성
        report_content = f"""# API 04 테스트 결과 보고서

## 테스트 정보
- **테스트 일시**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **API**: 아파트 전월세 실거래가 자료
- **Base URL**: https://apis.data.go.kr/1613000/RTMSDataSvcAptRent

## 테스트 요약
- **전체 테스트 수**: {total_tests}
- **성공**: {successful_tests} ✅
- **실패**: {failed_tests} ❌
- **성공률**: {(successful_tests/total_tests*100):.1f}%
- **총 소요 시간**: {total_duration:.2f}초
- **평균 응답 시간**: {avg_duration:.2f}초

## 거래 유형 통계
- **전세**: {total_jeonse}건
- **월세**: {total_wolse}건

---

## 상세 테스트 결과

"""
        
        for idx, test_result in enumerate(self.results, 1):
            result = test_result['result']
            status = "✅ 성공" if test_result['success'] else "❌ 실패"
            
            report_content += f"""### 테스트 {idx}: {test_result['test_name']}

**상태**: {status}  
**설명**: {test_result['description']}  
**지역코드**: {test_result['lawd_cd']}  
**계약년월**: {test_result['deal_ymd']}  
**실행 시간**: {test_result['start_time']}  
**소요 시간**: {test_result['duration_seconds']:.2f}초  

"""
            
            if test_result['success']:
                report_content += f"""**결과 코드**: {result.get('result_code')}  
**결과 메시지**: {result.get('result_msg')}  
**전체 건수**: {result.get('total_count')}  
**조회된 건수**: {result.get('item_count')}  

"""
                
                items = result.get('items', [])
                if items:
                    report_content += "**거래 정보**:\n\n"
                    for item_idx, item in enumerate(items[:10], 1):  # 최대 10건만 표시
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
                        
                        report_content += f"""#### 거래 {item_idx}
- **아파트명**: {apt_name}
- **지역**: {sgg_nm} {dong}
- **거래유형**: {rent_type}
- **거래금액**: {deal_amount}만원
"""
                        
                        # 전세/월세 금액 파싱
                        if deal_amount != 'N/A' and rent_type != 'N/A':
                            parsed_amount = self.api.parse_rent_amount(deal_amount, rent_type)
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
                    
                    if len(items) > 10:
                        report_content += f"*... 외 {len(items) - 10}건 더 있음*\n\n"
                else:
                    report_content += "**거래 정보**: 조회된 데이터가 없습니다.\n\n"
            else:
                error_msg = result.get('message') or result.get('result_msg') or 'Unknown error'
                report_content += f"**오류**: {error_msg}\n\n"
            
            report_content += "---\n\n"
        
        # JSON 결과 저장
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'test_summary': {
                    'total_tests': total_tests,
                    'successful_tests': successful_tests,
                    'failed_tests': failed_tests,
                    'success_rate': successful_tests/total_tests*100 if total_tests > 0 else 0,
                    'total_duration': total_duration,
                    'avg_duration': avg_duration,
                    'total_jeonse': total_jeonse,
                    'total_wolse': total_wolse
                },
                'test_results': self.results
            }, f, indent=2, ensure_ascii=False)
        
        # 마크다운 보고서 저장
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"\n{'='*60}")
        print("테스트 완료")
        print(f"{'='*60}")
        print(f"보고서 저장 위치:")
        print(f"  - 마크다운: {report_file}")
        print(f"  - JSON: {json_file}")
        print(f"\n테스트 요약:")
        print(f"  - 전체: {total_tests}건")
        print(f"  - 성공: {successful_tests}건")
        print(f"  - 실패: {failed_tests}건")
        print(f"  - 성공률: {(successful_tests/total_tests*100):.1f}%")
        print(f"  - 평균 응답 시간: {avg_duration:.2f}초")
        print(f"  - 전세: {total_jeonse}건")
        print(f"  - 월세: {total_wolse}건")


def main():
    """메인 테스트 실행 함수"""
    runner = TestRunner()
    
    # 테스트 케이스 정의
    test_cases = [
        {
            'name': '기본 테스트 - 종로구 2024년 1월',
            'lawd_cd': '11110',
            'deal_ymd': '202401',
            'description': '기본 파라미터로 테스트 (데이터 없을 수 있음)'
        },
        {
            'name': '강남구 2023년 12월',
            'lawd_cd': '11680',
            'deal_ymd': '202312',
            'description': '강남구 전월세 거래 데이터 조회'
        },
        {
            'name': '강남구 2023년 11월',
            'lawd_cd': '11680',
            'deal_ymd': '202311',
            'description': '강남구 2023년 11월 전월세 데이터 조회'
        },
        {
            'name': '서초구 2023년 12월',
            'lawd_cd': '11650',
            'deal_ymd': '202312',
            'description': '서초구 전월세 거래 데이터 조회'
        },
        {
            'name': '송파구 2023년 12월',
            'lawd_cd': '11710',
            'deal_ymd': '202312',
            'description': '송파구 전월세 거래 데이터 조회'
        }
    ]
    
    # 각 테스트 케이스 실행
    for test_case in test_cases:
        runner.run_test_case(
            name=test_case['name'],
            lawd_cd=test_case['lawd_cd'],
            deal_ymd=test_case['deal_ymd'],
            description=test_case['description']
        )
    
    # 보고서 생성
    runner.generate_report()


if __name__ == "__main__":
    main()
