import pytest

from .test_factories import make_batch_payload


def test_create_and_get_batch(client):
    # Создание
    payload = [make_batch_payload(batch_number=42)]
    r1 = client.post("/batches", json=payload)
    print([r.path for r in client.app.router.routes])
    assert r1.status_code == 200, r1.text
    batch = r1.json()[0]
    assert batch["batch_number"] == 42

    # Чтение по ID
    bid = batch["id"]
    r2 = client.get(f"/batches/{bid}")
    assert r2.status_code == 200, r2.text
    detail = r2.json()
    assert detail["id"] == bid
    assert detail["work_center"] == payload[0]["work_center"]


@pytest.mark.parametrize("patch_body, field, expected", [
    ({"task_description": "NEW"}, "task_description", "NEW"),
    ({"is_closed": True}, "is_closed", True),
    ({"is_closed": False}, "is_closed", False),
])
def test_patch_batch(client, patch_body, field, expected):
    # Сначала создаём
    r = client.post("/batches", json=[make_batch_payload(7)])
    bid = r.json()[0]["id"]

    # Патчим
    rp = client.patch(f"/batches/{bid}", json=patch_body)
    assert rp.status_code == 200, rp.text
    assert rp.json()[field] == expected


def test_get_batches_filters_and_pagination(client):
    # Генерим три партии
    for i in (10, 20, 30):
        client.post("/batches", json=[make_batch_payload(i)])

    # limit=2
    r = client.get("/batches?limit=2")
    assert r.status_code == 200
    assert len(r.json()) == 2

    # фильтр по batch_number=20
    r2 = client.get("/batches?batch_number=20")
    lst = r2.json()
    assert len(lst) == 1 and lst[0]["batch_number"] == 20
