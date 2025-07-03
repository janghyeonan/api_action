import requests
import pytest
import json

BASE_URL = "http://localhost:8000"

def test_health_check():
    """헬스 체크 엔드포인트 테스트"""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_root_endpoint():
    """루트 엔드포인트 테스트"""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello World!"
    assert "timestamp" in data

def test_get_user():
    """사용자 조회 엔드포인트 테스트"""
    user_id = 123
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert data["name"] == f"User {user_id}"
    assert data["email"] == f"user{user_id}@example.com"
    assert "created_at" in data

def test_create_user():
    """사용자 생성 엔드포인트 테스트"""
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    }
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User created successfully"
    assert data["user_id"] == 123
    assert data["data"] == user_data
    assert "created_at" in data

def test_invalid_user_id():
    """잘못된 사용자 ID 테스트"""
    response = requests.get(f"{BASE_URL}/users/invalid")
    assert response.status_code == 422  # FastAPI validation error

if __name__ == "__main__":
    pytest.main([__file__, "-v"])