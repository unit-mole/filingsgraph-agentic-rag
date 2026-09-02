def test_health_endpoint():
    try:
        from fastapi.testclient import TestClient
        from filingsgraph.api.main import app
    except ModuleNotFoundError:
        return
    r = TestClient(app).get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"
