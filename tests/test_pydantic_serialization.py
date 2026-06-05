from typing import FrozenSet, Set

from ninja import Router, Schema
from ninja.testing import TestClient

router = Router()


class SetResponse(Schema):
    tags: Set[str]


class FrozenSetResponse(Schema):
    ids: FrozenSet[int]


class BytesResponse(Schema):
    blob: bytes


@router.get("/set", response=SetResponse)
def get_set(request):
    return {"tags": {"a", "b", "c"}}


@router.get("/frozenset", response=FrozenSetResponse)
def get_frozenset(request):
    return {"ids": frozenset({1, 2, 3})}


@router.get("/bytes", response=BytesResponse)
def get_bytes(request):
    return {"blob": b"hello"}


client = TestClient(router)


def test_set_field_serializes_to_list():
    response = client.get("/set")
    assert response.status_code == 200
    assert sorted(response.json()["tags"]) == ["a", "b", "c"]


def test_frozenset_field_serializes_to_list():
    response = client.get("/frozenset")
    assert response.status_code == 200
    assert sorted(response.json()["ids"]) == [1, 2, 3]


def test_bytes_field_serializes_to_string():
    response = client.get("/bytes")
    assert response.status_code == 200
    assert response.json()["blob"] == "hello"
