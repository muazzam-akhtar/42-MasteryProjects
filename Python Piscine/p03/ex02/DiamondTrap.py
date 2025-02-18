from S1E7 import Baratheon, Lannister


class King(Baratheon, Lannister):
    """The mad King himself"""
    def __init__(self, first_name: str, is_alive=True):
        super().__init__(first_name, is_alive)

    def set_eyes(self, color: str):
        self.eyes = color

    def set_hairs(self, color: str):
        self.hair = color

    def get_eyes(self):
        return self.eyes

    def get_hair(self):
        return self.hair
