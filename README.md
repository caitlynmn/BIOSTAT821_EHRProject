# BIOSTAT821_EHRProject

# Part 1:
# Computational complexity/Data structures

Develop a Python module that provides some simple analytical capabilities on some (synthetic) EHR data. This is provided as:

* A table of patients with demographic data: `PatientCorePopulatedTable.txt`
* A table of laboratory results: `LabsCorePopulatedTable.txt`

## Data parsing

Define a function `parse_data(filename: str) -> ???` that reads and parses the data files. Choose appropriate data structures such that the expected analyses (below) are efficient.

Include a module docstring describing your rationale for choosing these data structures.

Include a function docstring analyzing the computational complexity of the data parser.

## Analysis

Define the following functions to interrogate the data. In each one, include a function docstring describing its computational complexity _at runtime_ (i.e. after parsing into the global data structures).

### Old patients

The function `num_older_than(age, ???)` should take the data and return the number of patients older than a given age (in years). For example,

```python
>> num_older_than(51.2)
52
```

### Sick patients

The function `sick_patients(lab, gt_lt, value, ???)` should take the data and return a (unique) list of patients who have a given test with value above (">") or below ("<") a given level. For example,

```python
>> sick_patients("METABOLIC: ALBUMIN", ">", 4.0)
["FB2ABB23-C9D0-4D09-8464-49BF0B982F0F", "64182B95-EB72-4E2B-BE77-8050B71498CE"]
```

## Notes

All of this should be generalizable, i.e. it should be designed to work with files with these formats, not just these _specific_ files. State (in module/function docstrings) any assumptions that you make about the input data.

When describing computational complexity, document your thought process in detail. For example:

> 5 is added to `element`, which is a single operation. This operation is performed twice for each element, leading to 2N operations. For big-O analysis, we drop the constant factor, yielding O(N) complexity.

You may like to use the `datetime` (standard) library. _Do not import any other libraries._

Your submission should be a single file titled `ehr_analysis.py`.

## Submission

1. Create a _private_ GitHub repository.
2. Invite `patrickkwang` to collaborate.
3. Create a branch called `part1` and complete this assignment there.
4. Make a pull request `part1` -> `main`. _DO NOT MERGE IT._
5. Request a review from `patrickkwang`.
6. Submit the link to your repository on Sakai by the due date.
