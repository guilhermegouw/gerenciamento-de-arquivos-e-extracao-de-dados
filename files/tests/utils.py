import os


def create_test_file(directory, file_name, content="This is a test file"):
    file_path = os.path.join(directory, file_name)
    with open(file_path, "w") as f:
        f.write(content)
    return file_path
