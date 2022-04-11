"""EHR Analysis.

Caitlyn Nguyen
BIOSTAT821

"""
from datetime import datetime


class Lab:
    """Lab object."""

    def __init__(
        self,
        patid: str,
        admission_id: str,
        lab_name: str,
        lab_value: float,
        lab_units: str,
        lab_datetime: datetime,
    ):
        """Initialize."""
        self.patid = patid
        self.admission_id = admission_id
        self.lab_name = lab_name
        self.lab_value = lab_value
        self.lab_units = lab_units
        self.lab_datetime = lab_datetime


class Patient:
    """Patient object."""

    def __init__(
        self,
        patid: str,
        gender: str,
        dob: datetime,
        race: str,
        marital: str,
        labs: list[Lab],
    ):
        """Initialize."""
        self.patid = patid
        self.gender = gender
        self.dob = dob
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
            - self.dob.year
            - ((today.month, today.day) < (self.dob.month, self.dob.day))
        )
        return age

    @property
    def lab_dict(self):
        """Transform lab objects to dictionary.

        Creates a dictionary with the keys being the lab names and the values
        being a dictionary with the keys "Value", "Units", "Date", and "Age"
        for the corresponding lab. Complexity is O(M) as it is required to
        loop over each lab for the patient, assuming that this is the first
        call to the property. All other single operations are ignored for
        big O analysis.
        """
        if self._lab_dict is None:  # O(1)
            lab_dict: dict = dict()  # O(1)
            for lab in self.labs:  # M times
                if lab.lab_name not in lab_dict.keys():  # O(1)
                    nested_lab_list = [lab]
                    lab_dict[lab.lab_name] = nested_lab_list  # O(1)
                else:  # O(1)
                    nested_lab_list = lab_dict[lab.lab_name]
                    nested_lab_list.append(lab)
                    lab_dict[lab.lab_name] = nested_lab_list  # O(1)
            self._lab_dict = lab_dict  # O(1)
        return self._lab_dict  # O(1)

    def check_lab_values(self, lab_name: str, gt_lt: str, value: float):
        """Check if lab values are greater/less than given value.

        Returns True if lab values are greater/less than given value or
        False if the condition is not met.

        Complexity is O(M) assuming self.lab_dict has not been run yet in
        the worst-case scenario. All other operations are single, which are
        ignored for big O analysis.
        """

        if gt_lt != ">" and gt_lt != "<":
            raise ValueError("Second input should be '<' or '>'")
        lab_list = self.lab_dict[lab_name]  # O(M)
        for each_lab in lab_list:
            if gt_lt == ">":  # O(1)
                if each_lab.lab_value > value:  # O(1)
                    return True  # O(1)
                else:  # O(1)
                    continue  # O(1)
            elif gt_lt == "<":  # O(1)
                if each_lab.lab_value < value:  # O(1)
                    return True  # O(1)
                else:  # O(1)
                    continue  # O(1)
        else:
            return False  # O(1)


def parse_data(patient_file: str, lab_file: str) -> list[Patient]:
    r"""Parse lab and patient data to a list of patient objects.

    Assumptions:
    * patient_file is a string of the name of the patient EHR data .txt file.
    * lab_file is a string of the name of the lab EHR data .txt file.
    * Each line in the data .txt file is single datapoint.
    * Each column in the data .txt file is an EHR variable.
    * Values within a row are separated by the tab character '\t\'.
    * All patients in the patient EHR file have labs in the lab EHR file.
    * For the Lab data file:
        * The first row in the EHR data is the variable names.
        * The columns of data are in the following order: PatientID,
            admission_id, lab_name, lab_value, lab_units, lab_datetime
        * LabeDateTime is recorded as "YYYY-MM-DD".
    * For the Patient data file:
        * The first row in the EHR data is the variable names.
        * The columns of data are in the following order: PatientID,
            PatientGender, PatientDateOfBirth, PatientRace,
            PatientMaritalStatus, PatientLanguage,
            PatientPopulationPercentageBelowPoverty
        * PatientDatOfBirth is recorded as "YYYY-MM-DD".

    Computational complexity:
    The labs are looped over for M*N times to produce a dictionary of labs,
    where the keys are the patids and the values are a list of Lab objects
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
    a function of O(M). It takes a single operation to add the patient ID
    to the set if the condition is met. Return adds another single operation.
    Constant factors are ignored for big-O analysis, so this is of
    O(M*N) complexity.

    """
    pat_ids = set()  # O(1)
    for patient in patient_list:  # N times
        if patient.check_lab_values(lab, gt_lt, value):  # O(M)
            pat_ids.add(patient.patid)  # O(1)
    return pat_ids  # O(1)


def age_at_admission(patid: str, patient_list: list[Patient]) -> float:
    """Compute age at first admission for any given patient.

    Assumptions:
    * All the assumptions in the parse_data function.

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
        if patient.patid == patid:  # O(1)
            lab_data = patient.lab_dict  # O(M)
            patient_dob = patient.dob
            break  # O(1)
    else:
        raise ValueError("Patient is not in the provided dataset.")  # O(1)

    patient_age = 999  # O(1)

    for each_lab_cluster in lab_data.values():
        for each_lab in each_lab_cluster:
            age = (
                each_lab.lab_datetime.year
                - patient_dob.year
                - (
                    (each_lab.lab_datetime.month, each_lab.lab_datetime.day)
                    < (patient_dob.month, patient_dob.day)
                )
            )
            if age < patient_age:
                patient_age = age
    return patient_age
