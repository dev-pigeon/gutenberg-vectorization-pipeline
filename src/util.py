def isTextFile(path):
    if (len(path) < 5):
        raise ValueError(
            "ERROR: The input path must point to a .txt file to vectorize.")

    REQUIRED_EXTENSION = '.txt'
    actual_extension = path[-4:]
    if REQUIRED_EXTENSION != actual_extension:
        raise ValueError(
            "ERROR: The input path must point to a .txt file to vectorize.")
