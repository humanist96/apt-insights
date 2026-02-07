"""
공통 유틸리티 모듈
모든 API 모듈에서 공통으로 사용하는 기능
"""
import xml.etree.ElementTree as ET
from typing import Dict

API_TIMEOUT_SECONDS = 10
SUCCESS_CODES = ['00', '000']


def parse_xml_response(xml_text: str) -> Dict:
    """
    XML 응답을 파싱하여 JSON 형식으로 변환
    
    Args:
        xml_text: XML 응답 텍스트
    
    Returns:
        파싱된 데이터 (dict)
    """
    try:
        root = ET.fromstring(xml_text)
        
        # response 구조 파싱
        result = {
            'response': {
                'header': {},
                'body': {}
            }
        }
        
        # header 파싱
        header = root.find('header')
        if header is not None:
            result['response']['header'] = {
                'resultCode': header.findtext('resultCode', ''),
                'resultMsg': header.findtext('resultMsg', '')
            }
        
        # body 파싱
        body = root.find('body')
        if body is not None:
            result['response']['body'] = {
                'totalCount': int(body.findtext('totalCount', '0')),
                'numOfRows': int(body.findtext('numOfRows', '0')),
                'pageNo': int(body.findtext('pageNo', '0')),
                'items': {'item': []}
            }
            
            # items 파싱
            items = body.find('items')
            if items is not None:
                item_list = []
                # item이 여러 개인 경우
                item_elements = items.findall('item')
                if not item_elements:
                    # item이 하나인 경우
                    item_elem = items.find('item')
                    if item_elem is not None:
                        item_elements = [item_elem]
                
                for item in item_elements:
                    item_dict = {}
                    for child in item:
                        tag_name = child.tag
                        text_value = child.text if child.text else ''
                        item_dict[tag_name] = text_value
                    item_list.append(item_dict)
                result['response']['body']['items']['item'] = item_list
        
        return result
    except ET.ParseError as e:
        return {
            'error': True,
            'message': f'XML 파싱 실패: {str(e)}',
            'raw_response': xml_text[:500]
        }


def parse_api_response(response: Dict) -> Dict:
    """
    API 응답 파싱 및 정리
    
    Args:
        response: API 응답 데이터
    
    Returns:
        파싱된 데이터
    """
    if 'error' in response:
        return response
    
    try:
        header = response.get('response', {}).get('header', {})
        body = response.get('response', {}).get('body', {})
        
        result_code = header.get('resultCode', '')
        result_msg = header.get('resultMsg', '')
        
        # 정상 코드: '00' 또는 '000'
        if result_code not in SUCCESS_CODES:
            return {
                'error': True,
                'result_code': result_code,
                'result_msg': result_msg
            }
        
        items = body.get('items', {})
        item_list = items.get('item', [])
        
        # item이 단일 객체인 경우 리스트로 변환
        if isinstance(item_list, dict):
            item_list = [item_list]
        
        return {
            'error': False,
            'result_code': result_code,
            'result_msg': result_msg,
            'total_count': body.get('totalCount', 0),
            'num_of_rows': body.get('numOfRows', 0),
            'page_no': body.get('pageNo', 0),
            'items': item_list,
            'item_count': len(item_list)
        }
    except Exception as e:
        return {
            'error': True,
            'message': f'응답 파싱 실패: {str(e)}',
            'raw_response': response
        }
