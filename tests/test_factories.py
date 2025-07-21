from datetime import datetime, date


def make_batch_payload(
        batch_number: int = 1,
        batch_date: date = date.today(),
        work_center: str = "Цех №1",
        shift: str = "1 смена",
) -> dict:
    now = datetime.now().replace(microsecond=0).isoformat()
    return {
        "is_closed": False,
        "task_description": f"TASK {batch_number}",
        "work_center": work_center,
        "shift": shift,
        "brigade": f"Бригада-{batch_number}",
        "batch_number": batch_number,
        "batch_date": batch_date.isoformat(),
        "nomenclature": f"Номенклатура-{batch_number}",
        "ekn_code": f"EKN-{batch_number}",
        "work_center_id": 1,
        "rc_identifier": f"RC-{batch_number}",
        "shift_start_datetime": now,
        "shift_end_datetime": now,
    }


def make_product_payload(
        unique_code: str = "CODE123",
        batch_number: int = 1,
        batch_date: date = date.today(),
) -> dict:
    return {
        "unique_code": unique_code,
        "batch_number": batch_number,
        "batch_date": batch_date.isoformat(),
    }
