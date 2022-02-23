# BIOSTAT821_EHRProject

# Setup and installation
To install Python, please refer to [Python Packaging Installation Instructions](https://packaging.python.org/en/latest/tutorials/installing-packages/).

To install Git, please refer to [Git Guides](https://github.com/git-guides/install-git).

To install Pytest, please refer to [Pytest Documentation](https://docs.pytest.org/en/6.2.x/getting-started.html).

The module `ehr_analysis.py` contains the functions `parse_data`, `num_older_than`, `sick_patients`, and `age_at_admission`.

Patient demographic EHR data is taken in as a tab-separated table .txt file with the following columns of data as its variables: `PatientID`, `PatientGender`, `PatientDateOfBirth`, `PatientRace`, `PatientMaritalStatus`, `PatientLanguage`, and `PatientPopulationPercentageBelowPoverty`. The .txt. file `PatientData_Test.txt` is included as an example file for demographic EHR data.

Laboratory EHR data is taken in as a tab-separated table .txt file with the following columns of data as its variables: `PatientID`, `AdmissionID`, `LabName`, `LabValue`, `LabUnits`, and `LabDateTime`. The .txt. file `LabData_Test.txt` is included as an example file for laboratory EHR data.

# Class Descriptions

## Lab Class
The Lab class is initialized as: `Lab(PATID: str, AdmissionID: str, LabName: str, LabValue: float, LabUnits: str, LabDateTime: datetime`.

The Lab class has the following instance attributes:
* PATID
* AdmissionID
* LabName
* LabValue
* LabUnits
* LabDateTime

Each instance of the Lab class stores attributes for a single lab datapoint.

## Patient Class
The Patient class is initialized as: `Patient(PATID: str, gender: str, DOB: datetime, race: str, marital: str, labs: list[Lab]`.

Each instance of the Patient class stores attributes for a single patient.

The Patient class has the following instance attributes:
* PATID
* gender
* DOB
* race
* marital
* labs

The Patient class has the following properties:
* age
* lab_dict, a dictionary with the keys being the lab names available for the patient and the values being a dictionary with the keys "Value", "Units", "Date", and "Age" for the corresponding lab.

The method `check_lab_values(self, lab_name: str, gt_lt: str, value: float)` is used to check if lab values for that patient are greater/less than a given value. The method returns True if lab values are greater/less than given value or False if the condition is not met.

# Function Descriptions

## Data parsing

The function `parse_data(patient_file: str, lab_file: str) -> list[Patient]` takes in 
* A table of patients with demographic data. For example, `PatientData_Test.txt`.
* A table of laboratory results. For example, `LabData_Test.txt`.

The output is a list of Patient objects.

Assumptions:
* patient_file is a string of the name of the patient EHR data .txt file.
* lab_file is a string of the name of the lab EHR data .txt file.
* Each line in the data .txt file is single datapoint.
* Each column in the data .txt file is an EHR variable.
* Values within a row are separated by the tab character '\t\'.
* All patients in the patient EHR file have labs in the lab EHR file.
* For the Lab data file:
    * The first row in the EHR data is the variable names.
    * The columns of data are in the following order: PatientID, AdmissionID, LabName, LabValue, LabUnits, LabDateTime
    * LabeDateTime is recorded as "YYYY-MM-DD".
* For the Patient data file:
    * The first row in the EHR data is the variable names.
    * The columns of data are in the following order: PatientID, PatientGender, PatientDateOfBirth, PatientRace, PatientMaritalStatus, PatientLanguage, PatientPopulationPercentageBelowPoverty
    * PatientDatOfBirth is recorded as "YYYY-MM-DD".

## Analysis

### Old patients

The function `num_older_than(compared_age: float, patient_list: list[Patient]) -> int` takes the data and returns the number of patients older than a given age (in years). For example,

```python
>> num_older_than(52, patient_data)
74
```

Assumptions:
* All the assumptions in the parse_data function.

### Sick patients

The function `sick_patients(
    lab: str, gt_lt: str, value: float, patient_list: list[Patient]
) -> set[str]` takes the data and returns a (unique) list of patients who have a given test with value above (">") or below ("<") a given level. For example,

```python
>> sick_patients("CBC: LYMPHOCYTES", "<", 0.8, lab_data)
{'016A590E-D093-4667-A5DA-D68EA6987D93',
 '0681FA35-A794-4684-97BD-00B88370DB41', ...}
```

Assumptions:
* All the assumptions in the parse_data function.
* All patients have the desired lab in their lab records.

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
