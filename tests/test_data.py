from coronabot import data

def test_get_global_cases():
    response = data.get_global_cases()
    assert isinstance(response["cases"], int)
    assert isinstance(response["deaths"], int)
    assert isinstance(response["recovered"], int)
