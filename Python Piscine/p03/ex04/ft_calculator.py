class calculator:
    """
    A calculator class for performing arithmetic operations between
    two vectors.

    Attributes:
        vector (list): The vector on which operations will be performed.

    Methods:
        dotproduct(V1: list, V2: list): Dot product of two vectors.

        add_vec(V1: list[float], V2: list[float]): Addition of two vectors.

        sous_vec(V1: list[float], V2: list[float]): Subtraction of two vectors.
    """

    @staticmethod
    def dotproduct(V1: list[float], V2: list[float]) -> None:
        dot_product = 0.0
        for i in V1:
            dot_product += i * V2[V1.index(i)]
        print(f"Dot product is: {round(dot_product)}")

    @staticmethod
    def add_vec(V1: list[float], V2: list[float]) -> None:
        res = []
        for i in V1:
            res.append(i + V2[V1.index(i)])
        print(f"Add Vector is: {[f'{val:.1f}' for val in res]}")

    @staticmethod
    def sous_vec(V1: list[float], V2: list[float]) -> None:
        res = []
        for i in V1:
            res.append(i - V2[V1.index(i)])
        print(f"Sous Vector is: {[f'{val:.1f}' for val in res]}")
