from fastapi.testclient import TestClient
from app.main import app

def test_register_login_me_and_role_boundary():
    client=TestClient(app)
    email="ecoscholar-test@example.org"
    client.post("/api/auth/register",json={"email":email,"display_name":"Test Learner","password":"strong-test-password"})
    response=client.post("/api/auth/login",json={"email":email,"password":"strong-test-password"})
    assert response.status_code==200
    token=response.json()["access_token"]
    assert client.get("/api/auth/me",headers={"Authorization":f"Bearer {token}"}).json()["role"]=="learner"
    assert client.get("/api/auth/users",headers={"Authorization":f"Bearer {token}"}).status_code==403

def test_invalid_credentials_rejected():
    response=TestClient(app).post("/api/auth/login",json={"email":"nobody@example.org","password":"wrong"})
    assert response.status_code==401
