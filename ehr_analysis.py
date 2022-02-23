"""EHR Analysis.

Caitlyn Nguyen
BIOSTAT821

"""
from datetime import datetime


class Lab:
    """Lab object."""

    def __init__(
        self,
        PATID: str,
        AdmissionID: str,
        LabName: str,
        LabValue: float,
        LabUnits: str,
        LabDateTime: datetime,
    ):
        """Initialize."""
        self.PATID = PATID
        self.AdmissionID = AdmissionID
        self.LabName = LabName
        self.LabValue = LabValue
        self.LabUnits = LabUnits
        self.LabDateTime = LabDateTime


class Patient:
    """Patient object."""

    def __init__(
        self,
        PATID: str,
        gender: str,
        DOB: datetime,
        race: str,
        marital: str,
        labs: list[Lab],
    ):
        """Initialize."""
        self.PATID = PATID
        self.gender = gender
        self.DOB = DOB
        self.race = race
        self.marital = marital
        self.labs = labs
        self._lab_dict = None

    @property
    def age(self):
        """Calculate patient age."""
        today = datetime.today()
        age = (
            today.year
            - self.DOB.year
            - ((today.month, today.day) < (self.DOB.month, self.DOB.day))
        )
        return age

    @property
    def lab_dict(self):
        """Transform lab objects to dictionary.

        Creates a dictionary with the lab names as keys and
        a dictionary with the keys "Value", "Units", "Date", and "Age"
        for the corresponding lab name as the the value.

        Complexity is O(M) as it is required to loop over each lab for
        the patient, assuming that this is the first call to the property.
        All other single operations are ignored for big O analysis.
        """
        if self._lab_dict is None:  # O(1)
            lab_dict: dict = dict()  # O(1)
            for lab in self.labs:  # M times
                if lab.LabName not in lab_dict.keys():  # O(1)
                    nested_dict: dict = dict()  # O(1)
                    nested_dict["Value"] = [lab.LabValue]  # O(1)
                    nested_dict["Units"] = [lab.LabUnits]  # O(1)
                    nested_dict["Date"] = [lab.LabDateTime]  # O(1)
                    age = (
                        lab.LabDateTime.year
                        - self.DOB.year
                        - (
                            (lab.LabDateTime.month, lab.LabDateTime.day)
                            < (self.DOB.month, self.DOB.day)
                        )
                    )  # O(1)
                    nested_dict["Age"] = [age]  # O(1)
                    lab_dict[lab.LabName] = nested_dict  # O(1)
                else:  # O(1)
                    nested_dict = lab_dict[lab.LabName]  # O(1)
                    nested_dict["Value"].append(lab.LabValue)  # O(1)
                    nested_dict["Units"].append(lab.LabUnits)  # O(1)
                    nested_dict["Date"].append(lab.LabDateTime)  # O(1)
                    age = (
                        lab.LabDateTime.year
                        - self.DOB.year
                        - (
                            (lab.LabDateTime.month, lab.LabDateTime.day)
                            < (self.DOB.month, self.DOB.day)
                        )
                    )  # O(1)
                    nested_dict["Age"].append(age)  # O(1)
                    lab_dict[lab.LabName] = nested_dict  # O(1)
            self._lab_dict = lab_dict  # O(1)
        return self._lab_dict  # O(1)

    def check_lab_values(self, lab_name: str, gt_lt: str, value: float):
        """Check if lab values are greater/less than given value.

        Returns True if lab values are greater/less than given value,
        False if condition is not met.

        Complexity is O(M) assuming self.lab_dict has not been run yet in
        the worst-case scenario. All other operations are single, which are
        ignored for big O analysis.
        """
        lab_values = self.lab_dict[lab_name]["Value"]  # O(M)
        if gt_lt == ">":  # O(1)
            if max(lab_values) > value:  # O(1)
                return True  # O(1)
            else:  # O(1)
                return False  # O(1)
        elif gt_lt == "<":  # O(1)
            if min(lab_values) < value:  # O(1)
                return True  # O(1)
            else:  # O(1)
                return False  # O(1)
        else:  # O(1)
            raise ValueError("Second input should be '<' or '>'")  # O(1)


def parse_data(patient_file: str, lab_file: str) -> list[Patient]:
    r"""Parse lab and patient data to a list of patient objects.

    Assumptions:
    - filename is a string of the name of the lab EHR data .txt file.
    - Each line in the data .txt file is a lab's data.
    - Each column in the data .txt file is an EHR variable.
    - Values within a row are separated by the tab character '\t\'.
    - All patients in the patient EHR file have labs in the lab EHR file.

    Computational complexity:
    The labs are looped over for M*N times to produce a dictionary of labs,
    where the keys are the PATIDs and the values are a list of Lab objects
    which correspond to the patient. The patients are looped over for
    N times to produce a list of Patient objects. For big-O analysis,
    the constant factors can be ignored, so this function is of
    O(M*N + N) complexity.

    """
    lab_dictionary: dict = {}  # O(1)

    with open(lab_file) as file:  # O(1)
        next(file)  # O(1)
        for line in file:  # M*N times
            lab_line = line.strip().split("\t")  # O(1)
            if lab_line[0] not in lab_dictionary.keys():  # O(1)
                lab_dictionary[lab_line[0]] = [
                    Lab(
                        lab_line[0],
                        lab_line[1],
                        lab_line[2],
                        float(lab_line[3]),
                        lab_line[4],
                        datetime.strptime(lab_line[5][0:10], "%Y-%m-%d"),
                    )
                ]  # O(1)
            else:  # O(1)
                lab_dictionary[lab_line[0]].append(
                    Lab(
                        lab_line[0],
                        lab_line[1],
                        lab_line[2],
                        float(lab_line[3]),
                        lab_line[4],
                        datetime.strptime(lab_line[5][0:10], "%Y-%m-%d"),
                    )
                )  # O(1)

    with open(patient_file) as file:  # O(1)
        next(file)  # O(1)
        results = []  # O(1)
        for line in file:  # N times
            patient_line = line.strip().split("\t")  # O(1)
            results.append(
                Patient(
                    patient_line[0],
                    patient_line[1],
                    datetime.strptime(patient_line[2][0:10], "%Y-%m-%d"),
                    patient_line[3],
                    patient_line[4],
                    lab_dictionary[patient_line[0]],
                )
            )  # O(1)

    return results  # O(1)


def num_older_than(compared_age: float, patient_list: list[Patient]) -> int:
    """Compute the number of individuals older than a given age.

    Assumptions:
    - All the assumptions in the parse_data function.
    - The first row in the EHR data is the variable names.
    - Patient ID is recorded in the first column.
    - Patient date of birth is recorded in the third column of the EHR file.
    - Patient date of birth is recorded as "YYYY-MM-DD".

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
    - All the assumptions in the parse_data function.
    - The first row in the EHR data is the variable names.
    - Patient ID is recorded in the first column.
    - Lab name is recorded in the third column.
    - Lab value is recorded in the fourth column.
    - All patients have the desired lab in their lab records.

    Computational complexity:
    A blank set is created with a single operation. Each patient is checked
    to see if lab values are greater than or less than given value which uses
    a function of O(M). It takes a single operation to add the patient ID
    to the set if the condition is met. Return adds another single operation.
    Constant factors are ignored for big-O analysis, so this is of
    O(M*N) complexity.

    """
    pat_ids = set()  # O(1)
    for patient in patient_list:  # N times
        if patient.check_lab_values(lab, gt_lt, value):  # O(M)
            pat_ids.add(patient.PATID)  # O(1)
    return pat_ids  # O(1)


def age_at_admission(patID: str, patient_list: list[Patient]) -> float:
    """Compute age at first admission for any given patient.

    Assumptions:
    - All the assumptions in the parse_data function.
    - All assumptions in the num_older_than function.
    - Lab date is recorded in the sixth column of the lab data file.
    - Lab dates are recorded as "YYYY-MM-DD".
    - All patients in the patient data have labs in the lab data.

    Computational complexity:
    The provided patient ID is searched for within the provided patient data
    by looping over the patient dataset up to N times. If the patient ID is
    in the dataset, then the patient's lab data is recorded and the
    algorithm stops iterating for a total of 3 operations. Recording the lab
    data is O(M), assuming lab_dict property has not been called upon yet.
    If the patient ID is not found in the patient dataset, then a
    ValueError is raised using two single operations. Then a single
    operation is used to assign patient age to a large number.
    The algorithm then iterates M times. with three single operations
    each loop. Constant factors are ignored for big-O analysis, so this
    function is of O(M*N + M) complexity.

    """
    for patient in patient_list:  # N times
        if patient.PATID == patID:  # O(1)
            lab_data = patient.lab_dict  # O(M)
            break  # O(1)
        elif patient == patient_list[-1]:  # O(1)
            raise ValueError("Patient is not in the provided dataset.")  # O(1)

    patient_age = 999  # O(1)

    for lab_values in lab_data.values():  # M times
        min_age = min(lab_values["Age"])  # O(1)
        if min_age < patient_age:  # O(1)
            patient_age = min_age  # O(1)
    return patient_age  # O(1)
