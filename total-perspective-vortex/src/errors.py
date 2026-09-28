def errorHandler(error: Exception, msg: str):
    """
    Description:
        Prints out the Exception and Message
    Parameters:
        error(Exception):   The exception caught
        msg(str):           The message to print
    Returns
        None
    """
    if error == KeyboardInterrupt:
        msg = 'Ctrl + C'
        print()

    print(error.__name__ + ":", msg)
    return 1
