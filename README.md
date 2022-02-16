# BIOSTAT821_EHRProject

# Setup and installation
To install Python, please refer to [Python Packaging Installation Instructions](https://packaging.python.org/en/latest/tutorials/installing-packages/).

To install Git, please refer to [Git Guides](https://github.com/git-guides/install-git).

To install Pytest, please refer to [Pytest Documentation](https://docs.pytest.org/en/6.2.x/getting-started.html).

The module `ehr_analysis.py` contains the functions `parse_data`, `num_older_than`, `sick_patients`, and `age_at_admission`.

Patient demographic EHR data is taken in as a tab-separated table .txt file with the following columns of data as its variables: `PatientID`, `PatientGender`, `PatientDateOfBirth`, `PatientRace`, `PatientMaritalStatus`, `PatientLanguage`, and `PatientPopulationPercentageBelowPoverty`. The .txt. file `PatientCorePopulatedTable.txt` is included as an example file for demographic EHR data.

Laboratory EHR data is taken in as a tab-separated table .txt file with the following columns of data as its variables: `PatientID`, `AdmissionID`, `LabName`, `LabValue`, `LabUnits`, and `LabDateTime`. The .txt. file `LabsCorePopulatedTable.txt` is included as an example file for laboratory EHR data.

# Function Descriptions

## Data parsing

The function `parse_data(filename: str) -> parse_data(filename: str) -> list[list[str]]` takes in 
* A table of patients with demographic data. For example, `PatientCorePopulatedTable.txt`.
* A table of laboratory results. For example, `LabsCorePopulatedTable.txt`.

The output is a list of list of strings of the parsed data, with each nested list being a patient's unique data.

Assumptions:
* filename is a string of the name of the EHR data .txt file.
* Each line in the data .txt file is a patient's data.
* Each column in the data .txt file is an EHR variable.
* Values within a row are separated by the tab character '\t\'.

## Analysis

### Old patients

The function `num_older_than(compared_age: float, patient_data: list[list[str]]) -> int` takes the data and returns the number of patients older than a given age (in years). For example,

```python
>> num_older_than(52, patient_data)
74
```

Assumptions:
* All the assumptions in the parse_data function.
* The first row in the EHR data is the variable names.
* Patient ID is recorded in the first column.
* Patient date of birth is recorded in the third column of the EHR file.
* Patient date of birth is recorded as "YYYY-MM-DD".

### Sick patients

The function `sick_patients(
    lab: str, gt_lt: str, value: float, lab_data: list[list[str]]
) -> set[str]` takes the data and returns a (unique) list of patients who have a given test with value above (">") or below ("<") a given level. For example,

```python
>> sick_patients("CBC: LYMPHOCYTES", "<", 0.8, lab_data)
{'016A590E-D093-4667-A5DA-D68EA6987D93',
 '0681FA35-A794-4684-97BD-00B88370DB41', ...}
```

Assumptions:
* All the assumptions in the parse_data function.
* The first row in the EHR data is the variable names.
* Patient ID is recorded in the first column.
* Lab name is recorded in the third column.
* Lab value is recorded in the fourth column.

### Age at admission

The function `age_at_admission(
    patID: str, patient_data: list[list[str]], lab_data: list[list[str]]
) -> float` takes the patient demographic data and lab data and returns the age at admission (first lab encounter) for a given patient ID. For example,

```python
>> age_at_admission("6985D824-3269-4D12-A9DD-B932D640E26E", patient_data, lab_data)
23
```

Assumptions:
* All the assumptions in the parse_data function.
* All assumptions in the num_older_than function.
* Lab date is recorded in the sixth column of the lab data file.
* Lab dates are recorded as "YYYY-MM-DD".

# Testing

The files `LabData_Test.txt` and `PatientData_Test.txt` are included to be used with the `ehr_analysis_test.py` testing module. To test the `ehr_analysis.py` module, run the `ehr_analysis_test.py` module by typing in the console:

``` python
pytest ehr_analysis_test.py
```

A 100% passed test result should appear similar to:

``` python
ehr_analysis_test.py ....                                                                    [100%]

======================================== 4 passed in 0.11s ========================================
```
