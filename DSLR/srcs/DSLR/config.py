from dataclasses import dataclass, FrozenInstanceError


# * The frozen=True argument when used with the @dataclass decorator in
# * Python creates immutable instances of a data class. This means that
# * once an object of that data class is created, its attributes cannot
# * be modified. Attempting to change an attribute after instantiation
# * will result in a FrozenInstanceError.
@dataclass(frozen=True)
class Config:
    """
    Config(DataClass):
        Dataclass to hold constants to avoid the use of GLOBAL VARIABLES.\b
        Decorator has frozen=True to make values immutable in code.
    Variables:
        houses[dict[int, str]: The total unique class labels.
        colFeatures[list]:      The column features labels.
        learningRate[float]:    Learning rate set for training model.
        iterations[int]:        The Gradient Descent steps.
        epoch[int]:             As iterations but smaller values for SGD and\b
                                MBGD.
        batchSize[int]:         The size of each training sample per epoch\b
                                for MBGD.
        dataTrain[str]:         The training Dataset path.
        dataTest[str]:          The testing for prediction Dataset path.
        storeThetas[str]:       The output file stores thetas for prediction.
        normData[str]:          The training Mean and STD for prediction.
        predictions[str]:       The output file for predictions.
        exceptions[tuple] :     Tuple of commone exceptions.
    Methods:
        loadExceptions(self):   The exceptions getter.
    Raises:
        FrozenInstanceError:    When attempting to change an attribute after\b
                                instantiation.
    """
    houses = {
        0: 'Gryffindor',
        1: 'Hufflepuff',
        2: 'Ravenclaw',
        3: 'Slytherin',
    }
    colFeatures = [
        "Arithmancy",
        "Astronomy",
        "Herbology",
        "Defense Against the Dark Arts",
        "Divination",
        "Muggle Studies",
        "Ancient Runes",
        "History of Magic",
        "Transfiguration",
        "Potions",
        "Care of Magical Creatures",
        "Charms",
        "Flying"
    ]
    learningRate: float = 0.001
    epoch: int = 1000
    batchSize: int = 10
    dataTrain: str = "datasets/dataset_train.csv"
    dataTest: str = "datasets/dataset_test.csv"
    storeThetas: str = "data/store_thetas.csv"
    normData: str = "data/norm_params.npz"
    predictions: str = "data/houses.csv"
    exceptions: tuple = (
        TypeError,
        IndexError,
        FileNotFoundError,
        ValueError,
        AttributeError,
        OSError,
        KeyboardInterrupt,
        KeyError,
        StopIteration,
        ZeroDivisionError,
        EOFError,
        NameError,
        FrozenInstanceError
    )

    @staticmethod
    def setColour(text: str, col: int, content=None) -> None:
        """
        """
        colDict = {
            0: '\033[91m',
            1: '\033[92m',
            2: '\033[93m',
            3: '\033[0m'
        }

        if content:
            print(colDict[col] + text + colDict[3] + content)
        else:
            print(colDict[col] + text + colDict[3])
