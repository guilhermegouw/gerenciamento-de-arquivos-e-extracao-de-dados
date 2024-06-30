import os

import pytest
from django.conf import settings
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def upload_url():
    return "/upload/"


@pytest.fixture
def upload_dir():
    upload_dir = os.path.join(settings.MEDIA_ROOT, "uploaded_files")
    os.makedirs(upload_dir, exist_ok=True)

    yield upload_dir

    # Clean up the test uploaded files after each test
    for file_name in os.listdir(upload_dir):
        file_path = os.path.join(upload_dir, file_name)
        os.remove(file_path)


@pytest.fixture
def test_files_dir():
    test_files_dir = os.path.join(
        settings.BASE_DIR, "files", "tests", "test_files"
    )
    os.makedirs(test_files_dir, exist_ok=True)

    yield test_files_dir

    # Clean up the test files after each test
    for file_name in os.listdir(test_files_dir):
        file_path = os.path.join(test_files_dir, file_name)
        os.remove(file_path)
