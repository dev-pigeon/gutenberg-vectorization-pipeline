def isTextFile(path):
    if (len(path) < 5):
        return False

    REQUIRED_EXTENSION = '.txt'
    actual_extension = path[-4]
    return REQUIRED_EXTENSION == actual_extension
