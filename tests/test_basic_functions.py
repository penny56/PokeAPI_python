import api.client
import pytest
import json

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
