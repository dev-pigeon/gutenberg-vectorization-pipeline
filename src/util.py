def isTextFile(path):
    REQUIRED_EXTENSION = '.txt'
    actual_extension = path[-4]
    return REQUIRED_EXTENSION == actual_extension
