import pytest
from faker import Faker
from fastapi import FastAPI, Response, status
from fastapi.testclient import TestClient

from tests.fixtures import create_table  # noqa isort:skip


@pytest.mark.usefixtures("create_table")
def test_get_all_tables_endpoint(client: TestClient, app: FastAPI):
    url = app.url_path_for("get_all_tables")

    response: Response = client.get(url)

    assert response.status_code == status.HTTP_200_OK, "Status code should be 200"
    assert len(response.json()) == 2, "Response shouldn't be empty"


def test_create_new_table_succes(client: TestClient, app: FastAPI, faker: Faker):
    url_post = app.url_path_for("create_new_table")
    url_get = app.url_path_for("get_all_tables")

    empty_get_response = client.get(url_get)

    assert empty_get_response.status_code == status.HTTP_200_OK, (
        "Status code should be 200"
    )
    assert len(empty_get_response.json()) == 0, "Response shouldn't be empty"

    response: Response = client.post(
        url_post,
        json={
            "name": faker.word(),
            "seats": faker.random_int(),
            "location": faker.word(),
        },
    )

    assert response.status_code == status.HTTP_201_CREATED, "Status code should be 201"

    for field in ["id", "created_at", "name", "seats", "location"]:
        assert field in response.json(), (
            f"Should return all fields {field} in the response"
        )

    get_response_after_post = client.get(url_get)

    assert len(empty_get_response.json()) < len(get_response_after_post.json()), (
        "New table wasn't created"
    )
    assert len(get_response_after_post.json()) == 1, "Response shouldn't be empty"


def test_create_new_table_failed(client: TestClient, app: FastAPI):
    # TODO: Implement this test after change validation in api
    pass


@pytest.mark.usefixtures("create_table")
def test_delete_table_succes(client: TestClient, app: FastAPI):
    url_get = app.url_path_for("get_all_tables")
    url_delete = app.url_path_for("delete_table", table_id=1)

    get_response_before_delete = client.get(url_get)

    assert get_response_before_delete.status_code == status.HTTP_200_OK, (
        "Status code before delete should be 200"
    )
    assert len(get_response_before_delete.json()) == 2, "Response shouldn't be empty"

    response = client.delete(url_delete)

    assert response.status_code == status.HTTP_204_NO_CONTENT, (
        "Status code should be 204"
    )
    assert response.content == b"", "Response should be empty"

    get_response_after_delete = client.get(url_get)

    assert get_response_after_delete.status_code == status.HTTP_200_OK, (
        "Status code after delete should be 200"
    )
    assert len(get_response_after_delete.json()) < len(
        get_response_before_delete.json()
    ), "Response after delete should be smaller than before"

    response_after_delete = client.delete(url_delete)

    assert response_after_delete.status_code == status.HTTP_404_NOT_FOUND, (
        "Status code should be 404"
    )
