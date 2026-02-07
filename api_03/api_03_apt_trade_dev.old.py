"""
API 03: 아파트 매매 실거래가 상세 자료
국토교통부 공공데이터 API
"""
import requests
import sys
from pathlib import Path
from typing import Dict

# 상위 디렉토리의 모듈 import
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import SERVICE_KEY
from common import parse_xml_response, parse_api_response, API_TIMEOUT_SECONDS


class AptTradeDevAPI:
    """아파트 매매 실거래가 상세 API 클라이언트"""
    
    BASE_URL = "https://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev"
    ENDPOINT = "/getRTMSDataSvcAptTradeDev"
    
    def __init__(self, service_key: str = SERVICE_KEY):
        """
        Args:
            service_key: 공공데이터포털 인증키
        """
        self.service_key = service_key
    
    def get_trade_data(
        self,
        lawd_cd: str,
        deal_ymd: str,
        num_of_rows: int = 10,
        page_no: int = 1
    ) -> Dict:
        """
        매매 실거래가 상세 데이터 조회
        
        Args:
            lawd_cd: 지역코드 (법정동코드 5자리, 예: '11110')
            deal_ymd: 계약년월 (YYYYMM 형식, 예: '202401')
            num_of_rows: 한 페이지 결과 수 (기본값: 10)
            page_no: 페이지 번호 (기본값: 1)
        
        Returns:
            API 응답 데이터 (dict)
        """
        url = f"{self.BASE_URL}{self.ENDPOINT}"
        
        params = {
            'serviceKey': self.service_key,
            'LAWD_CD': lawd_cd,
            'DEAL_YMD': deal_ymd,
            'numOfRows': num_of_rows,
            'pageNo': page_no
        }
        
        try:
            response = requests.get(url, params=params, timeout=API_TIMEOUT_SECONDS)
            response.raise_for_status()
            
            # 응답 내용 확인
            text_response = response.text.strip()
            
            # XML 응답 처리
            if text_response.startswith('<?xml') or text_response.startswith('<'):
                return parse_xml_response(text_response)
            # JSON 응답 처리
            elif text_response.startswith('{') or text_response.startswith('['):
                return response.json()
            else:
                return {
                    'error': True,
                    'message': '예상치 못한 응답 형식',
                    'raw_response': text_response[:500]
                }
        except requests.exceptions.RequestException as e:
            return {
                'error': True,
                'message': f'API 요청 실패: {str(e)}'
            }
        except Exception as e:
            return {
                'error': True,
                'message': f'응답 처리 실패: {str(e)}',
                'raw_response': response.text[:500] if 'response' in locals() else 'N/A'
            }
    
    def parse_response(self, response: Dict) -> Dict:
        """
        API 응답 파싱 및 정리
        
        Args:
            response: API 응답 데이터
        
        Returns:
            파싱된 데이터
        """
        return parse_api_response(response)
    
    def get_trade_data_parsed(
        self,
        lawd_cd: str,
        deal_ymd: str,
        num_of_rows: int = 10,
        page_no: int = 1
    ) -> Dict:
        """
        매매 실거래가 상세 데이터 조회 및 파싱 (통합 메서드)
        
        Args:
            lawd_cd: 지역코드 (법정동코드 5자리)
            deal_ymd: 계약년월 (YYYYMM 형식)
            num_of_rows: 한 페이지 결과 수
            page_no: 페이지 번호
        
        Returns:
            파싱된 데이터
        """
        response = self.get_trade_data(lawd_cd, deal_ymd, num_of_rows, page_no)
        return self.parse_response(response)
