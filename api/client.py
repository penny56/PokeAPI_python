import requests
import urllib3

BASE_URL = "https://pokeapi.co/api/v2"

# 在 pokeapi 里，不需要 token
BASE_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

'''
在这里，path需要包含 path parameter，而 query parameters需要以 dict 格式放在 params 参数中。
如果需要login的情况下，如果使用的是token认证，token要带在 headers 参数中传入。
'''
def send_request(method: str,
                 path: str,
                 headers: dict = None,
                 json: dict = None,
                 params: dict = None,
                 expected_status: int = None):

    '''
    把 disable_warnings() 放在函数内部
    以防止 Pytest 会在执行用例前重置警告配置
    '''
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    url = f"{BASE_URL}{path}"

    # add thd access token to header
    if headers is None:
        headers = BASE_HEADERS.copy()
    else:
        headers.update(BASE_HEADERS)
    
    # 调用 requests.request() 方法
    response = requests.request(
        method=method.upper(),
        url=url,
        headers=headers,
        json=json,
        params=params,
        verify=False            # turn off SSL verification
    )

    # FYI：这里，如果带有 expected_status 的情况下，会判断一下，但是这种情况下，caller如果也有assert，会卡在这里，那边其实就没有用了
    if expected_status is not None:
        assert response.status_code == expected_status, (
            f"Expected {expected_status}, got {response.status_code}. \n"
            f"Response Reason: {response.reason}. \n"
            f"Response Text: {response.text[:100]}. \n"
        )
    return response
