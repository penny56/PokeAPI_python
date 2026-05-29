import api.client
import pytest

@pytest.mark.parametrize(
    # pokemon_input 包括 name 或 id
    "pokemon_input, expected_status",
    [
        ("pikachu", 200),
        ("not_exist_pokemon", 404),
        ("mewtwo", 200),
        (99, 200),
        (999999999, 404),
        (199, 200),
    ]
)
def test_search_pokemon(pokemon_input, expected_status):

    # GET /pokemon/{id or name}
    search_res = api.client.send_request(method="get",
                                  path=f"/pokemon/{pokemon_input}",
                                  expected_status=expected_status)
    assert search_res.status_code == expected_status

    response_time = search_res.elapsed.total_seconds()

    if search_res.status_code == 200:
        search_res_dict = search_res.json()
        print(f"{search_res_dict['name']} 的第一个技能(move)的名字 : {search_res_dict['moves'][0]['move']['name']}, elapse time: {response_time} s")
    
    else:
        print(f"{pokemon_input}: {search_res.text}")

@pytest.mark.parametrize(
    "pokemon_name",
    [
        "ho-oh",      # 测试连字符
        "farfetchd",  # 测试撇号特殊转换
        "porygon-z",  # 测试复合后缀
        "mr-mime",    # 测试空格变连字符
        "flabebe"     # 测试重音变音符号消除
    ]
)
def test_response_fields_validation(pokemon_name):

    # GET /pokemon/{id or name}
    search_res = api.client.send_request(method="get",
                                  path=f"/pokemon/{pokemon_name}",
                                  expected_status=200)
    assert search_res.status_code == 200

    # search_res 的类型是 requests.models.Response
    search_data = search_res.json()

    # 1 Verify required fields exist
    assert "id" in search_data, f"Expected 'id' field, got {search_res.keys()}"
    assert "name" in search_data, f"Expected 'name' field, got {search_res.keys()}"

    # 2 Verify field data types
    assert isinstance(search_data["id"], int), f"Expected id to be int, got {type(search_data['id']).__name__}"
    assert isinstance(search_data["name"], str), f"Expected name to be str, got {type(search_data['name']).__name__}"

    # 3 Verify nested object structure
    ''' 验证：在species元素中，有2个子元素：name 与 url
    "species": {
        "name": "ho-oh",
        "url": "https://pokeapi.co/api/v2/pokemon-species/250/"
    },
    '''
    assert "species" in search_data
    assert "name" in search_data["species"], f"'species' object should contain 'name' field"
    assert "url" in search_data["species"], f"'species' object should contain 'url' field"

    # 4 Verify list is not empty
    assert "moves" in search_data, f"Expected 'moves' field in response"
    assert isinstance(search_data["moves"], list), f"Expected 'moves' to be list, got {type(search_data['moves']).__name__}"
    assert len(search_data["moves"]) > 0, f"'moves' list should not be empty"