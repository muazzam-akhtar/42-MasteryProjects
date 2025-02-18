from S1E9 import Character


class Baratheon(Character):
    """Representing the Baratheon family."""

    def __init__(self, first_name: str, is_alive=True) -> None:
        """
        Initialize a Baratheon character with the provided first name.

        Parameters:
            first_name (str): The first name of the character.
            super: calling the __init__ method of the parent class Character
        """
        super().__init__(first_name, is_alive)
        self.family_name = "Baratheon"
        self.eyes = "brown"
        self.hair = "dark"

    def die(self):
        """
        Mark the character as not alive.
        """
        self.is_alive = False

    def __str__(self) -> str:
        return f"Vector: ('{self.family_name}', '{self.eyes}', '{self.hair}')"

    def __repr__(self) -> str:
        return self.__str__()


class Lannister(Character):
    """Representing the Lannister family."""

    def __init__(self, first_name: str, is_alive=True) -> None:
        """
        Initialize a Lannister character with the provided first name.

        Parameters:
            first_name (str): The first name of the character.
        """
        super().__init__(first_name, is_alive)
        self.family_name = "Lannister"
        self.eyes = "blue"
        self.hair = "light"

    def die(self):
        """
        Mark the character as not alive.
        """
        self.is_alive = False

    def __str__(self) -> str:
        return f"Vector: ('{self.family_name}', '{self.eyes}', '{self.hair}')"

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def create_lannister(cls, first_name: str, is_alive: bool):
        """
        Create a Lannister character instance with custom is_alive status.

        Parameters:
            first_name (str): The first name of the character.
            is_alive (bool): The status of the character's life.
            cls refers to the class itself, a method that is defined on a
            class and can be called on the class itself,
            without creating an instance of the class.

        Returns:
            Lannister: An instance of the Lannister character.
        """
        instance = cls(first_name)
        instance.is_alive = is_alive
        return instance
