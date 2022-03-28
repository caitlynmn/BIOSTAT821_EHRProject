"""EHR Analysis Part 4."""
import sqlite3
import os


def establish_con():
    os.remove("ehr_data.db")
    con = sqlite3.connect("ehr_data.db")
    return con


def parse_data(patient_file: str, lab_file: str):
    """Parse lab and patient data to a SQL database."""

    con = establish_con()
    cur = con.cursor()

    cur.execute(
        "CREATE TABLE patient_data([patient_id] TEXT, \
            [gender] TEXT, \
                [date_of_birth] TEXT, \
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
                            [lab_date_time] TEXT)"
    )

    with open(patient_file) as file:  # O(1)
        next(file)  # O(1)
        for line in file:  # N times
            patient_line = line.strip().split("\t")  # O(1)
            cur.execute(
                "INSERT INTO patient_data VALUES (?, ?, ?, ?, ?, ?, ?)",
                patient_line,
            )

    with open(lab_file) as file:  # O(1)
        next(file)  # O(1)
        for line in file:  # M*N times
            lab_line = line.strip().split("\t")  # O(1)
            cur.execute(
                "INSERT INTO lab_data VALUES (?, ?, ?, ?, ?, ?)",
                lab_line,
            )

    cur.execute(
        "CREATE TABLE ehr_data AS SELECT * FROM patient_data INNER JOIN lab_data \
        USING(patient_id)"
    )

    con.commit()


def num_older_than(compared_age: float):
    """Compute the number of individuals older than a given age."""
    con = sqlite3.connect("ehr_data.db")
    cur = con.cursor()

    cur.execute(
        "ALTER TABLE ehr_data ADD COLUMN age AS SELECT (strftime('%Y', 'now') \
             - strftime('%Y', date_of_birth)) - (strftime('%m-%d', 'now') < \
                  strftime('%m-%d', date_of_birth))"
    )

    cur.execute("SELECT ehr_data.patient_id WHERE age > 20")


if __name__ == "__main__":
    parse_data("PatientCorePopulatedTable.txt", "LabsCorePopulatedTable.txt")
    num_older_than(20)

rows = cur.execute(
    "SELECT * FROM ehr_data WHERE patient_id = 'FB2ABB23-C9D0-4D09-8464-49BF0B982F0F' LIMIT 5"
)

for row in rows:
    print(row)

con.close()
