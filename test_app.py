from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_comparison_before_comparing_files():
    """Test to get the results of the comparison before we compare the files"""
    response = client.get('/comparison_results/')
    assert response.status_code == 200
    assert response.json() == {"result": []}

def test_when_2_files_are_not_uploaded():
    """Test when we do not upload 2 files"""
    response = client.post(
        "/process_csv", files={"files": ("pay.csv", open("pay.csv", "rb"), "text/csv")}
    )
    assert response.status_code == 401
    assert response.json() == {"error": "Please upload 2 csv files"}

def test_uploading_csv():
    """Test when we successfully compare the files"""
    response = client.post(
        "/process_csv", files=[
            ("files", ("pay.csv", open("pay.csv", "rb"), "text/csv")),
            ("files", ("client.csv", open("client.csv", "rb"), "text/csv"))
        ]
    )
    assert response.status_code == 200
    {'message': 'Files successfully compared'}

def test_clear_results_after_comparison():
    """Test when we successfully clear the comparison array after comparing our files"""
    response = client.post(
        "/process_csv", files=[
            ("files", ("pay.csv", open("pay.csv", "rb"), "text/csv")),
            ("files", ("client.csv", open("client.csv", "rb"), "text/csv"))
        ]
    )
    response = client.post('/clear_data')
    assert response.status_code == 200
    assert response.json() == {"message": "Data has been cleared"}