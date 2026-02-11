def errorHandler(e) -> int:
    """
    errorHandler(e):

    Description:
        Error handler that prints out the error with message. Special case\b
        with CTRL + C adds message, and EOFError adds message.
    Parameters:
        e:      The exception caught.
    Raises:
        None
    Returns:
        int:    Value of 1 to indicate EXIT_FAILURE
    """
    name = type(e).__name__

    match name:
        case "KeyboardInterrupt":
            print('\n\033[91m', name + ":", "CTRL + C\033[0m")
        case "EOFError":
            print(f'\033[91m{name} :', "CTRL + D or EOF\033[0m")
        case _:
            print(f'\033[91m{name} :', f'{e}\033[0m')

    return 1
