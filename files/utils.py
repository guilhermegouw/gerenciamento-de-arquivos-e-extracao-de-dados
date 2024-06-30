import logging
import os
import re
import subprocess

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response


def is_valid_file_name(file_name):
    return re.match(r"^[a-zA-Z0-9_-]+$", file_name) is not None


def save_file(file, file_name):
    upload_dir = os.path.join(settings.MEDIA_ROOT, "uploaded_files")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file_name)

    if os.path.exists(file_path):
        status_code = status.HTTP_204_NO_CONTENT
    else:
        status_code = status.HTTP_201_CREATED

    with open(file_path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return status_code


def setup_file_paths(file_name, script_name):
    logging.info(
        "Received request to get max size data for file: %s", file_name
    )
    upload_dir = os.path.join(settings.MEDIA_ROOT, "uploaded_files")
    file_path = os.path.join(upload_dir, file_name)

    if not os.path.exists(file_path):
        logging.error("File not found: %s", file_path)
        return None, Response(
            {"error": "File not found."}, status=status.HTTP_404_NOT_FOUND
        )

    script_path = os.path.join(settings.BASE_DIR, "scripts", script_name)
    return file_path, script_path


def run_script(script_path, file_path, *args):
    try:
        result = subprocess.run(
            [script_path, file_path, *args],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip(), None
    except subprocess.CalledProcessError as e:
        logging.error("Error running script: %s", str(e))
        return None, Response(
            {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def parse_line(line):
    parts = line.split()
    return {
        "username": parts[0],
        "folder": parts[1],
        "numberMessages": int(parts[2]),
        "size": int(parts[4]),
    }
