import pytest
from httpx import AsyncClient
from sqlalchemy import select

from models import ProductCode


@pytest.mark.asyncio
async def test_batches(client: AsyncClient,db_session):
    # 1. Создание рабочего центра
    response = await client.post("/work-centers/", json={"id": 1, "name": "Test Center"})
    # Получение work_center по ID
    assert response.status_code == 200
    assert response.json()["name"] == "Test Center"
    # 2. Создание партии
    response = await client.post("/batches/", json={
        "task_description": "Test batch",
        "shift": "A",
        "team": "Alpha",
        "work_center_id": 1,
        "is_closed": False,
        "batch_number": 1,
        "batch_date": "2025-07-28",
        "nomenclature": "ABC123",
        "ekn_code": "EK0001",
        "start_time": "2025-07-28T08:00:01",
        "end_time": "2025-07-28T20:00:01"
    })
    assert response.status_code == 200
    assert response.json()["nomenclature"] == "ABC123"
    # Проверка на некорректных данных
    response = await client.post("/batches/", json={
        "task_description": "Bad batch",
        "shift": "B",
        "team": "Beta",
        "work_center_id": 999,  # такого нет
        "is_closed": False,
        "batch_number": 2,
        "batch_date": "invalid-date",
        "nomenclature": "XYZ",
        "ekn_code": "EK0002",
        "start_time": "2025-07-28T20:00:01",
        "end_time": "2025-07-28T08:00:01"
    })
    assert response.status_code == 422
    # 3. Получение партии по ID
    response = await client.get("/batches/1")
    assert response.status_code == 200
    data = response.json()
    assert data["nomenclature"] == "ABC123"

    # Обновляем партию по ID
    response = await client.patch("/batches/1", json={
        "task_description": "Updated batch",
        "is_closed": True
    })


    assert response.status_code == 200
    data = response.json()
    assert data["task_description"] == "Updated batch"
    assert data["is_closed"] is True

    #Обновление по несуществующему ID
    response = await client.patch("/batches/3", json={
        "task_description": "Updated batch",
        "is_closed": True
    })

    assert response.status_code == 404


    # Проверяем фильтр по is_closed
    response = await client.get("/batches/", params={"is_closed": True})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(batch["is_closed"] is True for batch in data)

    # Проверяем фильтр по batch_number
    response = await client.get("/batches/", params={"batch_number": 1})
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["batch_number"] == 1

    # Проверяем по нескольким фильтрам

    response = await client.get("/batches/", params={
        "is_closed": True,
        "batch_number": 1,
        "shift": "A",
        "team": "Alpha",
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(
        batch["is_closed"] is True and batch["shift"] == "A" and batch["batch_number"] == 1 and batch["team"] == "Alpha"
        for batch in data)

    # Проверка на добавление продуктов
    response = await client.post("/products/", json=[
        {
            "code": "ABC-001",
            "batch_number": 1,
            "batch_date": "2025-07-28"
        },
        {
            "code": "ABC-002",
            "batch_number": 1,
            "batch_date": "2025-07-28"
        }
    ])
    assert response.status_code == 200
    assert len(response.json()) == 2

    # Попытка добавить такой же код

    response = await client.post("/products/", json=[
        {"code": "ABC-001", "batch_id": 1}
    ])
    assert response.status_code == 422
    # Агрегация продукции
    response = await client.post("/products/aggregate", json={
        "code": "ABC-002",
        "batch_id": 1
    })
    assert response.status_code == 200
    print(f'test for {response.json()}')
    data = response.json()
    assert data["aggregated_at"] is not None
    result = await db_session.execute(select(ProductCode).where(ProductCode.code == "ABC-002"))
    result_from_db = result.scalar_one_or_none()
    assert result_from_db.is_aggregated is True

    #  Агрегация несуществующего кода

    response = await client.post("/products/aggregate", json={
        "code": "NOT-FOUND",
        "batch_id": 999
    })
    assert response.status_code == 404