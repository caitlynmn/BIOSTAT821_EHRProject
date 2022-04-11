"""Class objects."""


class Student:
    """Student object."""

    def __init__(self, grade: float, name: str):
        """Student attributes."""
        self.name = name
        self.grade = grade


class Class:
    """Class object."""

    def __init__(self, roster: list[Student], course_id: str, instructor: str):
        """Class attributes."""
        self.roster = roster
        self.course_id = course_id
        self.instructor = instructor

    @property
    def num_student(self):
        """Calculate number of students."""
        return len(self.roster)

    def add_student(self, student: Student):
        """Add student to class."""
        self.roster.append(student)
        return self.roster
