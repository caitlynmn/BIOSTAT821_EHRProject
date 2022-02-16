"""EHR Analysis.

Caitlyn Nguyen
BIOSTAT821

Description:
This module defines three functions (parse_data, num_older_than, and
sick_patients) for analyzing EHR data. The EHR data is read from a .txt file
and is outputted into a list of lists. Each row in the EHR data is an element
in the outer list with the different EHR variables as elements within the
inner list. This data structure was used to preserve the order of each
EHR variable value with the corresponding patient ID and allow for
multiple EHR entries for the same patient ID.

"""
from datetime import datetime


def parse_data(filename: str) -> list[list[str]]:
    r"""Parse data in text file to a list of lists.

    Assumptions:
    - filename is a string of the name of the EHR data .txt file.
    - Each line in the data .txt file is a patient's data.
    - Each column in the data .txt file is an EHR variable.
    - Values within a row are separated by the tab character '\t\'.

    Computational complexity:
    Opening the file is one operation. It takes another operation
    to create an empty list. For each line in the file, the line is
    isolated (first operation), then stripped at all tab characters
    (second operatoin), and finally appended to a lsit (final operation).
    These three operations are repeated for N times, making 3*N complexity.
    The list of lists is then returned for a final single operation.
    For big-O analysis, the constant factors can be ignored, so
    this function is of O(N) complexity.

    """
    with open(filename) as file:  # O(1)
        results = []  # O(1)
        for line in file:  # N times
            single_line = line.strip()  # O(1)
            line_list = single_line.split("\t")  # O(1)
            results.append(line_list)  # O(1)
    return results  # O(1)


def num_older_than(compared_age: float, patient_data: list[list[str]]) -> int:
    """Compute the number of individuals older than a given age.

    Assumptions:
    - All the assumptions in the parse_data function.
    - The first row in the EHR data is the variable names.
    - Patient ID is recorded in the first column.
    - Patient date of birth is recorded in the third column of the EHR file.
    - Patient date of birth is recorded as "YYYY-MM-DD".

    Computational complexity:
    Establishing count as 0 and the current day count as two single operations.
    A for-loop is used to iterate over each row, excluding the header row,
    for a total of N - 1 times. The patient's birthday is then used to
    calculate age over 3 operations. It takes one operation to compare age,
    and one operation to add to count. The for-loop thus has a complexity
    of 5*(N-1). Returning count is an additional single operation. For
    big-O analysis, constants can be ignored, leaving a complexity
    of O(N).

    """
    count = 0  # O(1)
    today = datetime.today()  # O(1)
    for patient in patient_data[1:]:  # N - 1 times
        DOB = patient[2][0:10]  # O(1)
        birthday = datetime.strptime(DOB, "%Y-%m-%d")  # O(1)
        age = (
            today.year
            - birthday.year
            - ((today.month, today.day) < (birthday.month, birthday.day))
        )  # O(1)
        if age > compared_age:  # O(1)
            count += 1  # O(1)
    return count  # O(1)


def sick_patients(
    lab: str, gt_lt: str, value: float, lab_data: list[list[str]]
) -> set[str]:
    """Find unique patient IDs with a lab value greater/less than given value.

    Assumptions:
    - All the assumptions in the parse_data function.
    - The first row in the EHR data is the variable names.
    - Patient ID is recorded in the first column.
    - Lab name is recorded in the third column.
    - Lab value is recorded in the fourth column.

    Computational complexity:
    A blank list is created with a single operation. Each patient encounter is
    checked to see if the lab name matches the inputted one, for a total
    of N - 1 operations as the header row is excluded. Up to four operations
    are then computed for each loop, resulting in 4*(N-1) operations from
    the for-loop. Return adds another single operation. Constant factors
    are ignored for big-O analysis, so this is of O(N) complexity.

    """
    pat_ids = set()  # O(1)
    for encounter in lab_data[1:]:  # N - 1 times
        if encounter[2] == lab:  # O(1)
            if gt_lt == ">":  # O(1)
                if float(encounter[3]) > value:  # O(1)
                    pat_ids.add(encounter[0])  # O(1)
            elif gt_lt == "<":  # O(1)
                if float(encounter[3]) < value:  # O(1)
                    pat_ids.add(encounter[0])  # O(1)
            else:
                raise ValueError("Second input should be '<' or '>'")
    return pat_ids  # O(1)


def age_at_admission(
    patID: str, patient_data: list[list[str]], lab_data: list[list[str]]
) -> float:
    """Compute age at first admission for any given patient.

    Assumptions:
    - All the assumptions in the parse_data function.
    - All assumptions in the num_older_than function.
    - Lab date is recorded in the sixth column of the lab data file.
    - Lab dates are recorded as "YYYY-MM-DD".

    Computational complexity:
    The provided patient ID is searched for within the provided patient data
    by looping over the patient dataset up to N times, where N = number
    of patients in the patient dataset. If the patient ID is in the
    dataset, then the patient's date of birth is recorded and the
    algorithm stops iterating for a total of 3 operations. If the patient
    ID is not found in the patient dataset, then a ValueError is raised using
    two single operations. If the ID is in the dataset, then only
    two single operations are done. Then a single operation is used
    to assign patient age to a large number. The algorithm then iterates
    M times, where M = the number of lab encounters in the lab dataset. Up to
    six single operations are used to calculate and store the patient's
    age at a lab encounter if the age is lower than previously checked
    lab encounters. Finally, if the patient age is not the initially
    assigned 999 value, then the patient's age at first encounter is
    returned using two operations. Else, a ValueError is returned to
    report that the patient ID was not found in the lab data.
    Constant factors are ignored for big-O analysis, so this
    function is of O(N + M) complexity, where N = number of patients
    in the patient dataset, and M = number of lab encounters in the
    lab dataset.

    """
    for patient in patient_data[1:]:  # N times
        if patID == patient[0]:  # O(1)
            patient_DOB = patient[2][0:10]  # O(1)
            break  # O(1)
        elif patient == patient_data[-1]:  # O(1)
            raise ValueError(
                "Patient ID is not found in the provided patient dataset."
            )  # O(1)

    patient_age = 999  # O(1)
    for encounter in lab_data[1:]:  # M times
        if patID == encounter[0]:  # O(1)
            encounter_date = datetime.strptime(encounter[5][0:10], "%Y-%m-%d")  # O(1)
            birthday = datetime.strptime(patient_DOB, "%Y-%m-%d")  # O(1)
            age = (
                encounter_date.year
                - birthday.year
                - (
                    (encounter_date.month, encounter_date.day)
                    < (birthday.month, birthday.day)
                )
            )  # O(1)
            if age < patient_age:  # O(1)
                patient_age = age  # O(1)
    if patient_age != 999:  # O(1)
        return patient_age  # O(1)
    else:  # O(1)
        raise ValueError("Patient ID is not found in the provided lab dataset.")  # O(1)
