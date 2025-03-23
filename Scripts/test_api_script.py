import api_script
import pytest
import requests
import requests_mock
from collections import defaultdict


URL = "http://netbox:8080/api/dcim/devices/"

@pytest.fixture
def mock_requests():
    with requests_mock.Mocker() as m:
        yield m

def test_make_query_with_status(mock_requests):
    """
    Test when a specific status is provided.
    """
    status = "active"
    mock_response = {
        "count": 8,
        "results": []
    }
    mock_requests.get(f"{URL}?status={status}", json=mock_response, status_code=200)

    result = api_script.make_query(status)
    assert result == "Exist 8 with status active"

def test_make_query_without_status(mock_requests):
    """
    Test when no status is provided, checking grouped count of devices by status.
    """
    mock_response = {
        "count": 10,
        "results": [
            {"status": {"value": "active"}},
            {"status": {"value": "active"}},
            {"status": {"value": "offline"}},
            {"status": {"value": "offline"}},
            {"status": {"value": "offline"}},
            {"status": {"value": "planned"}},
            {"status": {"value": "planned"}},
            {"status": {"value": "planned"}},
            {"status": {"value": "active"}},
            {"status": {"value": "active"}}
        ]
    }
    mock_requests.get(URL, json=mock_response, status_code=200)

    result = api_script.make_query(None)
    expected_output = "Exist this quantity of devices: \n defaultdict(<class 'int'>, {'active': 4, 'offline': 3, 'planned': 3})"
    assert result == expected_output

def test_make_query_no_devices(mock_requests):
    """
    Test when there are no devices in the response.
    """
    mock_response = {"count": 0, "results": []}
    mock_requests.get(URL, json=mock_response, status_code=200)

    with pytest.raises(ValueError, match="There is no devices"):
        api_script.make_query(None)

def test_make_query_api_error(mock_requests):
    """
    Test when the API returns an error response.
    """
    mock_requests.get(URL, status_code=500, json={"error": "Server error"})

    with pytest.raises(ConnectionError):
        api_script.make_query(None)