[승인] 국토교통부_아파트 분양권전매 실거래가 자료
    [Base URL] apis.data.go.kr/1613000/RTMSDataSvcSilvTrade
    GET
    /getRTMSDataSvcSilvTrade
    아파트 분양권전매 실거래가 공개 자료
    Models
    getRTMSDataSvcSilvTrade_response{
    header	{
    description:	
    header

    resultCode	string
    결과코드

    resultMsg	string
    결과메세지

    }
    body	{
    description:	
    body

    items	{
    description:	
    items

    item	{...}
    }
    totalCount	number
    전체 결과 수

    numOfRows	number
    한 페이지 결과 수

    pageNo	number
    페이지 번호

    }
    }
[승인] 국토교통부_아파트 매매 실거래가 자료
    [ Base URL: apis.data.go.kr/1613000/RTMSDataSvcAptTrade ]
    GET
    /getRTMSDataSvcAptTrade
    아파트 매매 실거래가 공개 자료

    Models
    getRTMSDataSvcAptTrade_response{
    header	{
    description:	
    header

    resultCode	string
    결과코드

    resultMsg	string
    결과메세지

    }
    body	{
    description:	
    body

    items	{
    description:	
    items

    item	{...}
    }
    totalCount	number
    전체 결과 수

    numOfRows	number
    한 페이지 결과 수

    pageNo	number
    페이지 번호

    }
    }
[승인] 국토교통부_아파트 매매 실거래가 상세 자료
    [ Base URL: apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev ]
    GET
    /getRTMSDataSvcAptTradeDev
    아파트 매매 실거래가 공개 자료(상세)

    Models
    getRTMSDataSvcAptTradeDev_response{
    header	{
    description:	
    header

    resultCode	string
    결과코드

    resultMsg	string
    결과메세지

    }
    body	{
    description:	
    body

    items	{
    description:	
    items

    item	{...}
    }
    numOfRows	number
    한 페이지 결과 수

    pageNo	number
    페이지 번호

    totalCount	number
    전체 결과 수

    }
    }
[승인] 국토교통부_아파트 전월세 실거래가 자료
    [ Base URL: apis.data.go.kr/1613000/RTMSDataSvcAptRent ]
    GET
    /getRTMSDataSvcAptRent
    아파트 전월세 실거래가 공개 자료
    Models
    getRTMSDataSvcAptRent_response{
    header	{
    description:	
    header

    resultCode	string
    결과코드

    resultMsg	string
    결과메세지

    }
    body	{
    description:	
    body

    items	{
    description:	
    items

    item	{...}
    }
    totalCount	number
    전체 결과 수

    numOfRows	number
    한 페이지 결과 수

    pageNo	number
    페이지 번호

    }
    }