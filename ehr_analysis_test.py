"""Test EHR analysis."""

import pytest
from ehr_analysis import parse_data, num_older_than, sick_patients, age_at_admission
from datetime import datetime

# Create dictionary of possible options in lab and patient data
options_dict = {}
options_dict["PatientGender"] = ["Male", "Female"]
options_dict["PatientRace"] = ["Unknown", "African American", "Asian", "White"]
options_dict["PatientMaritalStatus"] = [
    "Married",
    "Single",
    "Divorced",
    "Unknown",
    "Separated",
]
options_dict["PatientLanguage"] = ["English", "Spanish", "Unknown", "Icelandic"]
options_dict["LabName"] = [
    "METABOLIC: POTASSIUM",
    "METABOLIC: CREATININE",
    "CBC: RED BLOOD CELL COUNT",
]
options_dict["LabUnits"] = ["mmol/L", "mg/dL", "m/cumm"]

# Run parse_data on test patient and lab EHR txt files
pat_data_example = parse_data("PatientData_Test.txt")
lab_data_example = parse_data("LabData_Test.txt")


def test_parse_data():
    """Test parse_data() function."""
    # Test patient data
    assert type(pat_data_example) == list
    assert type(pat_data_example[0]) == list
    assert type(pat_data_example[0][2]) == str
    assert len(pat_data_example) == 10
    assert len(pat_data_example[0]) == 7
    assert pat_data_example[4][1] in options_dict["PatientGender"]
    assert pat_data_example[6][3] in options_dict["PatientRace"]
    assert pat_data_example[8][4] in options_dict["PatientMaritalStatus"]
    assert pat_data_example[2][5] in options_dict["PatientLanguage"]
    # Test lab data
    assert len(lab_data_example) == 20
    assert len(lab_data_example[0]) == 6
    assert lab_data_example[2][2] in options_dict["LabName"]
    assert lab_data_example[5][4] in options_dict["LabUnits"]


def test_num_older_than():
    """Test num_older_than() function."""
    assert type(num_older_than(20, pat_data_example)) == int
    assert num_older_than(52, pat_data_example) == 6
    assert num_older_than(92, pat_data_example) == 2
    assert num_older_than(72, pat_data_example) == 6


def test_sick_patients():
    """Test sick_patients() function."""
    assert type(sick_patients("METABOLIC: POTASSIUM", ">", 30, lab_data_example)) == set
    assert (
        type(
            list(sick_patients("METABOLIC: POTASSIUM", ">", 30, lab_data_example)).pop()
        )
        == str
    )
    assert (
        len(sick_patients("CBC: RED BLOOD CELL COUNT", "<", 80, lab_data_example)) == 2
    )
    assert len(sick_patients("METABOLIC: CREATININE", ">", 90, lab_data_example)) == 2
    with pytest.raises(ValueError):
        sick_patients("CBC: RED BLOOD CELL COUNT", ">=", 10, lab_data_example)
        sick_patients("CBC: RED BLOOD CELL COUNT", "wrong input", 10, lab_data_example)
        sick_patients("CBC: RED BLOOD CELL COUNT", "< ", 10, lab_data_example)


def test_age_at_admission():
    """Test age_at_admission() function."""
    assert (
        age_at_admission(
            "EITSIO5D-YZF2-KYU2-QYVB-0CYV1AQ4AWH3", pat_data_example, lab_data_example
        )
        == 6
    )
    assert (
        age_at_admission(
            "315AHQQH-Y4MW-MDY4-UDYX-ESTMBGKASAGY", pat_data_example, lab_data_example
        )
        == 15
    )
    assert (
        age_at_admission(
            "5UGO1HF9-QFVJ-PW9E-WMS5-SLCOUGK8NAZ7", pat_data_example, lab_data_example
        )
        == 18
    )
    assert (
        age_at_admission(
            "ORM1FW1N-BYOI-J3ZA-0PLB-MJ9SNP3H1WFF", pat_data_example, lab_data_example
        )
        == 7
    )
    assert (
        age_at_admission(
            "UWO429L9-E60B-LJEO-M1U2-NHJSBHCSOZDD", pat_data_example, lab_data_example
        )
    ) == 24
    with pytest.raises(ValueError):
        age_at_admission("aaa", pat_data_example, lab_data_example)
        age_at_admission(
            "9VWI26ZY-R196-J48V-TLUK-E045NMVQ0KYG", pat_data_example, lab_data_example
        )
        age_at_admission(
            "EITSIO5D-YZF2-KYU2-QYVB-0CYV1AQ4AWH3 ", pat_data_example, lab_data_example
        )
