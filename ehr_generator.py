"""Random patient data generator."""

import string
import random
from random import randrange
from datetime import timedelta
from datetime import datetime


def id_generator(n):
    """Generate random string of letters and numbers."""
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(n)
    )


def patid_generator():
    """Generate random patID."""
    patID = (
        id_generator(8)
        + "-"
        + id_generator(4)
        + "-"
        + id_generator(4)
        + "-"
        + id_generator(4)
        + "-"
        + id_generator(12)
    )
    return patID


def random_date(start, end):
    """Return a random datetime between two datetimeobjects."""
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


d1 = datetime.strptime("01/01/1920 12:30 AM", "%m/%d/%Y %I:%M %p")
d2 = datetime.strptime("01/01/2003 12:30 AM", "%m/%d/%Y %I:%M %p")

random_dict = {}
random_dict["PatientGender"] = ["Male", "Female"]
random_dict["PatientRace"] = ["Unknown", "African American", "Asian", "White"]
random_dict["PatientMaritalStatus"] = [
    "Married",
    "Single",
    "Divorced",
    "Unknown",
    "Separated",
]
random_dict["PatientLanguage"] = ["English", "Spanish", "Unknown", "Icelandic"]
random_dict["LabName"] = [
    "METABOLIC: POTASSIUM",
    "METABOLIC: CREATININE",
    "CBC: RED BLOOD CELL COUNT",
]
random_dict["LabUnits"] = ["mmol/L", "mg/dL", "m/cumm"]


def rand_pat_generator():
    """Generate text file of EHR data."""
    random_line = []
    random_line.append(patid_generator())
    random_line.append(random.choice(random_dict["PatientGender"]))
    random_line.append(str(random_date(d1, d2)))
    random_line.append(random.choice(random_dict["PatientRace"]))
    random_line.append(random.choice(random_dict["PatientMaritalStatus"]))
    random_line.append(random.choice(random_dict["PatientLanguage"]))
    random_line.append(str(round(random.uniform(0.01, 99.99), 2)))
    return random_line


def rand_lab_generator():
    """Generate text file of EHR data."""
    random_line = []
    random_line.append(patid_generator())
    random_line.append(str(random.choice(range(1, 5))))
    lab_name = random.choice(random_dict["LabName"])
    random_line.append(lab_name)
    random_line.append(str(round(random.uniform(0.01, 99.99), 2)))
    lab_index = random_dict["LabName"].index(lab_name)
    random_line.append(random_dict["LabUnits"][lab_index])
    random_line.append(str(random_date(d1, d2)))
    return random_line


pat_headers = [
    "PatientID",
    "PatientGender",
    "PatientDateOfBirth",
    "PatientRace",
    "PatientMaritalStatus",
    "PatientLanguage",
    "PatientPopulationPercentageBelowPoverty",
]

lab_headers = [
    "PatientID",
    "AdmissionID",
    "LabName",
    "LabValue",
    "LabUnits",
    "LabDateTime",
]


def write_patient_data(filename, n):
    """Write randomly generated patient data."""
    with open(filename, "w") as f:
        f.write("\t".join(pat_headers) + "\n")
        for i in range(1, n):
            random_line = rand_pat_generator()
            f.write("\t".join(random_line) + "\n")


def write_lab_data(filename, n):
    """Write randomly generated lab data."""
    with open(filename, "w") as f:
        f.write("\t".join(lab_headers) + "\n")
        for i in range(1, n):
            random_line = rand_lab_generator()
            f.write("\t".join(random_line) + "\n")


# write_patient_data("PatientData_Test.txt", 10)
# write_lab_data("LabData_Test.txt", 20)
