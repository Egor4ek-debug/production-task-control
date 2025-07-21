import pytest

from .test_factories import make_batch_payload, make_product_payload


def test_add_and_aggregate_product_flow(client):
    # 1) Создаём партию #5
    r = client.post("/batches", json=[make_batch_payload(5)])
    bid = r.json()[0]["id"]

    # 2) Добавляем продукты: один валидный, один несуществующий
    ok = make_product_payload("OKCODE", 5)
    bad = make_product_payload("XCODE", 9999)
    r2 = client.post("/product", json=[ok, bad])
    assert r2.status_code == 200
    body = r2.json()
    assert body["inserted"] == 1
    assert body["skipped_no_batch"] == 1

    # 3) Агрегируем корректный
    resp3 = client.post(f"/batches/{bid}/aggregated", json={"unique_code": "OKCODE"})
    assert resp3.status_code == 200
    out = resp3.json()
    assert out["is_aggregated"] is True

    # 4) Повторная агрегация → 400
    resp4 = client.post(f"/batches/{bid}/aggregated", json={"unique_code": "OKCODE"})
    assert resp4.status_code == 400
    assert "already used" in resp4.json()["detail"]


@pytest.mark.parametrize("dups", [2, 3])
def test_add_product_duplicates(client, dups):
    # Партия #7
    bid = client.post("/batches", json=[make_batch_payload(7)]).json()[0]["id"]
    payload = [make_product_payload("DUP", 7) for _ in range(dups)]
    r = client.post("/product", json=payload)
    assert r.status_code == 200
    b = r.json()
    assert b["inserted"] == 1
    assert b["skipped_existing"] == dups - 1
