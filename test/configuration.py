import os

_test_files_directory_name = 'test_files'
project_directory = os.path.dirname(os.path.dirname(__file__))
test_files_directory = os.path.join(project_directory, _test_files_directory_name)


def test_file_path(file_name):
    return os.path.join(test_files_directory, file_name)
