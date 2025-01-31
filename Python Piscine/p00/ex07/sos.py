import sys


def checkArg(string: str) -> bool:
    splitted_data = string.split(' ')
    for i in splitted_data:
        if any(not char.isalnum() for char in i):  # Check for non-alphanumeric
            return False
    return True


def createMorseCodeData() -> dict:
    morse_code = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
        'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
        'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
        'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
        'U': '..-', 'V': '...-.', 'W': '.--', 'X': '-..-', 'Y': '-.--',
        'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
        '4': '....-', '5': '.....', '6': '-....', '7': '--...',
        '8': '---..', '9': '----.', '0': '-----', ' ': '/'
        }
    return morse_code


def translateToMorseCode(morse_code: dict, args: str) -> str:
    results = ''
    for i in args:
        if i.isalpha() is True:
            results += morse_code[i.upper()]
        else:
            results += morse_code[i]
        results += " "
    return results


def main():
    assert len(sys.argv) == 2, "the arguments are bad"
    assert checkArg(sys.argv[1]) is True, "the arguments are bad"
    morse_code = createMorseCodeData()
    results = translateToMorseCode(morse_code, sys.argv[1])
    print(results)


if __name__ == '__main__':
    main()
