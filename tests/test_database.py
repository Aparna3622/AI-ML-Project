from database import init_db, add_patient, get_all_patients, get_patient, update_patient, delete_patient


def test_database_crud(tmp_path):
    db_path = tmp_path / "test.db"
    init_db(str(db_path))
    pid = add_patient("Test", "2000-01-01", "a@b.com", 80.0, 13.0, 150.0, "Healthy", str(db_path))
    rows = get_all_patients(str(db_path))
    assert len(rows) == 1
    row = get_patient(pid, str(db_path))
    assert row["full_name"] == "Test"
    update_patient(pid, "Test2", "2000-01-01", "a@b.com", 85.0, 13.5, 155.0, "Healthy", str(db_path))
    row2 = get_patient(pid, str(db_path))
    assert row2["full_name"] == "Test2"
    delete_patient(pid, str(db_path))
    rows2 = get_all_patients(str(db_path))
    assert len(rows2) == 0
