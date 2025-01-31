import sys


def calcString(_str):
    upperCaseLetters = 0
    lowerCaseLetters = 0
    digits = 0
    spaces = 0
    punctuations = 0

    for i in _str:
        if i.isupper():
            upperCaseLetters += 1
        elif i.islower():
            lowerCaseLetters += 1
        elif i.isdigit():
            digits += 1
        elif i.isspace():
            spaces += 1
        else:
            punctuations += 1

    print("The text contains " + str(len(_str)) + " characters:")
    print(str(upperCaseLetters) + " upper letters")
    print(str(lowerCaseLetters) + " lower letters")
    print(str(punctuations) + " punctuation marks")
    print(str(spaces) + " spaces")
    print(str(digits) + " digits")


def main():
    _arg = sys.argv
    if len(_arg) == 1:
        # Prompt user input
        user_input = input("What is the text to count?\n")
        calcString(user_input)
    elif len(_arg) == 2:
        # Handle argument passed via command line
        calcString(_arg[1])
    else:
        print("Error: Too many arguments provided.")
        sys.exit(1)


if __name__ == "__main__":
    main()
