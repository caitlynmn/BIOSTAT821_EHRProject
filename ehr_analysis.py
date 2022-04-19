"""EHR Analysis Part 4."""
from ast import Raise
import sqlite3
import os
from datetime import datetime
from xmlrpc.client import boolean


def establish_con():
    """Establish connection."""
    if os.path.exists("ehr_data.db"):
        os.remove("ehr_data.db")
    con = sqlite3.connect("ehr_data.db")
    return con


def calculate_age(dob: str, doi: str) -> int:
    """Calculate age from date of birth (dob) and date of interest (doi)."""
    date_of_birth = datetime.strptime(dob, "%Y-%m-%d")
    if doi == "today":
        date_of_interest = datetime.today()
    else:
        date_of_interest = datetime.strptime(doi, "%Y-%m-%d")
    age = (
        date_of_interest.year
        - date_of_birth.year
        - (
            (date_of_interest.month, date_of_interest.day)
            < (date_of_birth.month, date_of_birth.day)
        )
    )
    return age


class Patient:
    """Patient object."""

    def __init__(self, patid: str):
        """Initialize."""
        self.patid = patid
        self.con = sqlite3.connect("ehr_data.db")
        self.cur = self.con.cursor()

    @property
    def date_of_birth(self) -> str:
        """Patient date of birth."""
        date_of_birth = self.cur.execute(
            "SELECT date_of_birth FROM patient_data WHERE [patient_id] = ?",
            (self.patid,),
        ).fetchone()
        date_of_birth = "".join(date_of_birth)[0:10]
        return date_of_birth

    @property
    def age(self) -> int:
        """Calculate patient age."""
        age = calculate_age(self.date_of_birth, "today")
        return age

    def check_lab_values(self, lab_name: str, gt_lt: str, lab_val: float) -> bool:
        """Check if there is a patient lab value < or > given value."""
        lab_value = str(lab_val)

        if gt_lt != ">" and gt_lt != "<":
            raise ValueError("Second input should be '<' or '>'")

        if gt_lt == "<":
            labs = self.cur.execute(
                "SELECT [lab_value], [lab_date] FROM lab_data WHERE \
                    [patient_id] = ? AND [lab_name] = ? AND [lab_value] < ?",
                (self.patid, lab_name, lab_value),
            ).fetchall()
        elif gt_lt == ">":
            labs = self.cur.execute(
                "SELECT [lab_value] FROM lab_data WHERE \
                    [patient_id] = ? AND [lab_name] = ? AND [lab_value] > ?",
                (self.patid, lab_name, lab_value),
            ).fetchall()

        if len(labs) > 0:
            return True
        else:
            return False

    @property
    def age_at_admiss(self) -> int:
        """Find age at admission."""
        admission_date = self.cur.execute(
            "SELECT MIN([lab_date]) FROM lab_data WHERE [patient_id] = ?",
            (self.patid,),
        ).fetchone()
        admission_date = "".join(admission_date)[0:10]
        age = calculate_age(self.date_of_birth, admission_date)
        return age


def parse_data(patient_file: str, lab_file: str) -> list[Patient]:
    """Parse lab and patient data to a SQL database."""
    con = establish_con()
    cur = con.cursor()

    cur.execute(
        "CREATE TABLE patient_data([patient_id] TEXT, \
            [gender] TEXT, \
                [date_of_birth] DATE, \
                    [race] TEXT, \
                        [marital_status] TEXT, \
                            [language] TEXT, \
                                [percent_below_poverty] FLOAT)"
    )

    cur.execute(
        "CREATE TABLE lab_data([patient_id] TEXT, \
            [admission_id] TEXT, \
                [lab_name] TEXT, \
                    [lab_value] FLOAT, \
                        [lab_units] TEXT, \
                            [lab_date] DATE)"
    )

    with open(lab_file) as file:  # O(1)
        next(file)  # O(1)
        for line in file:  # M*N times
            lab_line = line.strip().split("\t")  # O(1)
            lab_line[5] = datetime.strptime(lab_line[5][0:10], "%Y-%m-%d")
            cur.execute(
                "INSERT INTO lab_data VALUES (?, ?, ?, ?, ?, ?)",
                lab_line,
            )

    with open(patient_file) as file:  # O(1)
        next(file)  # O(1)
        results = []
        for line in file:  # N times
            patient_line = line.strip().split("\t")  # O(1)
            patient_line[2] = datetime.strptime(patient_line[2][0:10], "%Y-%m-%d")
            cur.execute(
                "INSERT INTO patient_data VALUES (?, ?, ?, ?, ?, ?, ?)",
                patient_line,
            )
            results.append(Patient(patient_line[0]))  # O(1)

    con.commit()

    return results


def num_older_than(compared_age: float, patient_list: list[Patient]) -> int:
    """Compute the number of individuals older than a given age.

    Assumptions:
    * All the assumptions in the parse_data function.

    Computational complexity:
    Establishing count as 0 is a single operation. A for-loop is used to
    iterate over each patient for a total of N - 1 times. It takes one
    operation to compare the patient's age and one operation to add to count.
    The for-loop thus has a complexity of 2*N. Returning count is an
    additional single operation. For big-O analysis, constants can be
    ignored, leaving a complexity of O(N).

    """
    count = 0  # O(1)
    for patient in patient_list:  # N times
        if patient.age > compared_age:  # O(1)
            count += 1  # O(1)
    return count  # O(1)


def sick_patients(
    lab: str, gt_lt: str, value: float, patient_list: list[Patient]
) -> set[str]:
    """Find unique patient IDs with a lab value greater/less than given value.

    Assumptions:
    * All the assumptions in the parse_data function.
    * All patients have the desired lab in their lab records.

    Computational complexity:
    A blank set is created with a single operation. Each patient is checked
    to see if lab values are greater than or less than given value which uses
    a function of O(1). It takes a single operation to add the patient ID
    to the set if the condition is met. Return adds another single operation.
    Constant factors are ignored for big-O analysis, so this is of
    O(N) complexity.

    """
    pat_ids = set()  # O(1)
    for patient in patient_list:  # N times
        if patient.check_lab_values(lab, gt_lt, value):  # O(1)
            pat_ids.add(patient.patid)  # O(1)
    return pat_ids  # O(1)


def age_at_admission(patid: str, patient_list: list[Patient]) -> float:
    """Compute age at first admission for any given patient.

    Assumptions:
    * All the assumptions in the parse_data function.

    Computational complexity:
    The provided patient ID is searched for within the provided patient data
    by looping over the patient dataset up to N times. If the patient ID is
    in the dataset, then the patient class age_at_admiss property is returned.
    The function thus has a computational complexity of O(N).

    """
    for patient in patient_list:  # N times
        if patient.patid == patid:  # O(1)
            return patient.age_at_admiss  # O(1)
    else:
        raise ValueError("Patient is not in the provided dataset.")  # O(1)
