"""Test EHR analysis."""

import pytest
from ehr_analysis import (
    Patient,
    parse_data,
    num_older_than,
    sick_patients,
    age_at_admission,
)
from datetime import datetime


def test_parse_data():
    """Test parse_data() function."""
    # Test patient data

    # Run parse_data on test patient and lab EHR txt files
    data_test = parse_data("PatientData_Test.txt", "LabData_Test.txt")
    assert isinstance(data_test, list)

    patient_test = data_test[0]

    assert isinstance(patient_test, Patient)
    assert isinstance(patient_test.patid, str)
    assert isinstance(patient_test.date_of_birth, str)
    assert isinstance(patient_test.age, int)
    assert isinstance(patient_test.age_at_admiss, int)


def test_num_older_than():
    """Test num_older_than() function."""
    data_test = parse_data("PatientData_Test.txt", "LabData_Test.txt")

    assert isinstance(num_older_than(20, data_test), int)
    assert num_older_than(52, data_test) == 4
    assert num_older_than(92, data_test) == 2
    assert num_older_than(86, data_test) == 3


def test_sick_patients():
    """Test sick_patients() function."""
    data_test = parse_data("PatientData_Test.txt", "LabData_Test.txt")

    assert isinstance(sick_patients("METABOLIC: POTASSIUM", ">", 30, data_test), set)
    assert isinstance(
        list(sick_patients("METABOLIC: POTASSIUM", ">", 30, data_test)).pop(),
        str,
    )
    assert len(sick_patients("CBC: RED BLOOD CELL COUNT", "<", 80, data_test)) == 3
    assert len(sick_patients("METABOLIC: CREATININE", ">", 90, data_test)) == 3
    with pytest.raises(ValueError):
        sick_patients("CBC: RED BLOOD CELL COUNT", ">=", 10, data_test)
        sick_patients("CBC: RED BLOOD CELL COUNT", "wrong input", 10, data_test)
        sick_patients("CBC: RED BLOOD CELL COUNT", "< ", 10, data_test)


def test_age_at_admission():
    """Test age_at_admission() function."""
    data_test = parse_data("PatientData_Test.txt", "LabData_Test.txt")

    assert age_at_admission("EITSIO5D-YZF2-KYU2-QYVB-0CYV1AQ4AWH3", data_test) == 6
    assert age_at_admission("315AHQQH-Y4MW-MDY4-UDYX-ESTMBGKASAGY", data_test) == 15
    assert age_at_admission("5UGO1HF9-QFVJ-PW9E-WMS5-SLCOUGK8NAZ7", data_test) == 18
    assert age_at_admission("ORM1FW1N-BYOI-J3ZA-0PLB-MJ9SNP3H1WFF", data_test) == 7
    assert age_at_admission("UWO429L9-E60B-LJEO-M1U2-NHJSBHCSOZDD", data_test) == 24
    with pytest.raises(ValueError):
        age_at_admission("aaa", data_test)
        age_at_admission("9VWI26ZY-R196-J48V-TLUK-E045NMVQ0KYG", data_test)
        age_at_admission("EITSIO5D-YZF2-KYU2-QYVB-0CYV1AQ4AWH3 ", data_test)
