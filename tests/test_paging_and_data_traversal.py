import api.client
import pytest
import json

'''
limit: 本次请求最多返回多少条数据
offset：偏移量/跳过条数
'''
@pytest.mark.parametrize(
    "limit, offset",
    [
        (10, 0),
        (100, 20),
        (250, 50),
        (1000,300)
    ]
)
def test_limit_and_offset(limit, offset):

    params = {'limit': limit, 'offset': offset}

    # GET /pokemon
    search_res = api.client.send_request(method="get",
                                  path=f"/pokemon",
                                  params=params,
                                  expected_status=200)
    assert search_res.status_code == 200

    # 将服务器返回的 JSON 格式文本，转换dict类型
    textDict = json.loads(search_res.text)

    # 校验：返回的数据列表长度，必须等于我们请求时限制的 limit 条数
    assert len(textDict['results']) == limit

