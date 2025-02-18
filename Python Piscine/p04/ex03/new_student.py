import random
import string
from dataclasses import dataclass, field


def generate_id() -> str:
    """
    Generate a random 15-character lowercase string ID.

    Returns:
        str: A randomly generated ID consisting of 15 lowercase
        alphabetic characters.
    """
    return "".join(random.choices(string.ascii_lowercase, k=15))


@dataclass
class Student:
    """
    A class representing a student.

    Attributes:
        name (str): The first name of the student. Initialized during
                    object creation.
        surname (str): The last name of the student. Initialized during
                       object creation.
        active (bool): Indicates whether the student is active.
                       Defaults to True.
        login (str): The student's login name, generated automatically
                     during initialization. It is the first letter of the name
                     capitalized and concatenated with the lowercase surname.
        id (str): A unique identifier for the student, generated automatically
                  using `generate_id()`.
    """
    name: str = field(init=True)
    surname: str = field(init=True)
    active: bool = field(default=True)
    login: str = field(init=False)
    id: str = field(init=False, default=generate_id())

    def __post_init__(self):
        self.login = self.name[0].capitalize() + self.surname.lower()
