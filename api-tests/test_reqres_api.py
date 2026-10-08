"""Tests API Reqres.in : GET / POST / PUT / DELETE /users.

Variables d'environnement :
  REQRES_BASE_URL  (défaut https://reqres.in/api)
  REQRES_API_KEY   clé gratuite créée sur https://app.reqres.in (obligatoire depuis 2025)
"""
import os

import allure
import pytest
import requests
from jsonschema import validate

BASE_URL = os.getenv("REQRES_BASE_URL", "https://reqres.in/api")
API_KEY = os.getenv("REQRES_API_KEY", "")
HEADERS = {"x-api-key": API_KEY, "Content-Type": "application/json"}
TIMEOUT = 15

USER_SCHEMA = {
    "type": "object",
    "required": ["id", "email", "first_name", "last_name", "avatar"],
    "properties": {
        "id": {"type": "integer"},
        "email": {"type": "string", "pattern": r"^[^@\s]+@[^@\s]+$"},
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "avatar": {"type": "string"},
    },
}
LIST_SCHEMA = {
    "type": "object",
    "required": ["page", "per_page", "total", "total_pages", "data"],
    "properties": {
        "page": {"type": "integer"},
        "per_page": {"type": "integer"},
        "total": {"type": "integer"},
        "total_pages": {"type": "integer"},
        "data": {"type": "array", "items": USER_SCHEMA},
    },
}


@pytest.fixture(scope="module", autouse=True)
def _check_key():
    if not API_KEY:
        pytest.skip("REQRES_API_KEY non défini (clé gratuite sur app.reqres.in)")


def call(method, path, **kw):
    return requests.request(method, f"{BASE_URL}{path}", headers=HEADERS, timeout=TIMEOUT, **kw)


@allure.feature("API Reqres")
class TestUsersAPI:
    @allure.story("API-01 GET /users?page=2")
    def test_api01_list_users(self):
        r = call("GET", "/users", params={"page": 2})
        assert r.status_code == 200
        body = r.json()
        validate(body, LIST_SCHEMA)
        assert body["page"] == 2
        assert len(body["data"]) == body["per_page"] or len(body["data"]) > 0
        assert r.elapsed.total_seconds() < 3

    @allure.story("API-02 GET /users/2")
    def test_api02_single_user(self):
        r = call("GET", "/users/2")
        assert r.status_code == 200
        user = r.json()["data"]
        validate(user, USER_SCHEMA)
        assert user["id"] == 2
        assert "application/json" in r.headers["Content-Type"]

    @allure.story("API-03 GET /users/23 (inexistant)")
    def test_api03_user_not_found(self):
        r = call("GET", "/users/23")
        assert r.status_code == 404
        assert r.json() == {}

    @allure.story("API-04 POST /users")
    @pytest.mark.parametrize("name,job", [("morpheus", "leader"), ("Sara Alaoui", "QA Engineer")])
    def test_api04_create_user(self, name, job):
        r = call("POST", "/users", json={"name": name, "job": job})
        assert r.status_code == 201
        body = r.json()
        assert body["name"] == name and body["job"] == job
        assert str(body["id"]).isdigit()
        assert "createdAt" in body

    @allure.story("API-05 PUT /users/2")
    def test_api05_update_user(self):
        r = call("PUT", "/users/2", json={"name": "morpheus", "job": "zion resident"})
        assert r.status_code == 200
        body = r.json()
        assert body["job"] == "zion resident"
        assert "updatedAt" in body

    @allure.story("API-06 DELETE /users/2")
    def test_api06_delete_user(self):
        r = call("DELETE", "/users/2")
        assert r.status_code == 204
        assert r.text == ""

    @allure.story("API-07 Login invalide (cas négatif)")
    def test_api07_login_missing_password(self):
        r = call("POST", "/login", json={"email": "peter@klaven"})
        assert r.status_code == 400
        assert r.json().get("error") == "Missing password"
