import os
import subprocess

from django.conf import settings

from files.tests.utils import create_test_file


def test_upload_new_file(client, upload_url, upload_dir, test_files_dir):
    test_file_path = create_test_file(
        test_files_dir, "testfile1", "This is a test file 1."
    )

    print(f"upload_dir: {upload_dir}")
    print(f"test_file_path: {test_file_path}")
    print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")

    # Upload the file
    with open(test_file_path, "rb") as f:
        response = client.put(upload_url, {"file": f}, format="multipart")

    # Ensure the response is correct
    assert (
        response.status_code == 201
    ), f"Expected 201, got {response.status_code}"
    assert os.path.exists(os.path.join(upload_dir, "testfile1"))


def test_upload_existing_file(client, upload_url, upload_dir, test_files_dir):
    test_file_path = os.path.join(test_files_dir, "testfile2")
    with open(test_file_path, "w") as f:
        f.write("This is an existing test file.")

    # First upload
    with open(test_file_path, "rb") as f:
        response = client.put(upload_url, {"file": f}, format="multipart")
    assert (
        response.status_code == 201
    ), f"Expected 201, got {response.status_code}"

    # Second upload (should replace the file)
    with open(test_file_path, "rb") as f:
        response = client.put(upload_url, {"file": f}, format="multipart")
    assert (
        response.status_code == 204
    ), f"Expected 204, got {response.status_code}"

    # Ensure the file still exists on the server
    uploaded_file_path = os.path.join(upload_dir, "testfile2")
    assert os.path.exists(
        uploaded_file_path
    ), f"File {uploaded_file_path} does not exist"


def test_upload_invalid_file_name(client, upload_url, test_files_dir):
    file_path = os.path.join(test_files_dir, "invalid@file#name.txt")
    with open(file_path, "w") as f:
        f.write("This file has an invalid name.")

    with open(file_path, "rb") as f:
        response = client.put(upload_url, {"file": f}, format="multipart")

    assert response.status_code == 400
    assert "error" in response.data
    assert response.data["error"] == "File name has invalid characters."


def test_list_files_empty(client):
    response = client.get("/files/")
    assert response.status_code == 200
    assert response.data["count"] == 0
    assert len(response.data["results"]) == 0


def test_list_files_with_files(client, upload_dir):
    create_test_file(upload_dir, "testfile1.txt", "This is a test file 1.")
    create_test_file(upload_dir, "testfile2.txt", "This is a test file 2.")

    response = client.get("/files/")
    assert response.status_code == 200
    assert response.data["count"] == 2
    assert len(response.data["results"]) == 2


def test_list_files_pagination(client, upload_dir):
    for i in range(15):
        create_test_file(
            upload_dir, f"testfile{i}.txt", f"This is test file {i}."
        )

    response = client.get("/files/?page=1&page_size=10")
    assert response.status_code == 200
    assert response.data["count"] == 15
    assert len(response.data["results"]) == 10

    response = client.get("/files/?page=2&page_size=10")
    assert response.status_code == 200
    assert len(response.data["results"]) == 5


def test_user_max_size_file_not_found(client, upload_dir):
    response = client.get("/files/user_max_size/nonexistentfile/")
    assert response.status_code == 404
    assert response.data["error"] == "File not found."


def test_user_max_size_file_with_data(client, upload_dir, mocker):
    # Create a test file
    test_file_name = "testfile"
    test_file_path = create_test_file(
        upload_dir,
        test_file_name,
        "juvati_be@uol.com.br inbox 000232478 size 012345671",
    )

    # Mock subprocess.run to simulate script output
    mocker.patch(
        "subprocess.run",
        return_value=mocker.Mock(
            stdout="juvati_be@uol.com.br inbox 000232478 size 012345671\n"
        ),
    )

    response = client.get(f"/files/user_max_size/{test_file_name}/")
    assert response.status_code == 200
    assert response.data == {
        "username": "juvati_be@uol.com.br",
        "folder": "inbox",
        "numberMessages": 232478,
        "size": 12345671,
    }


def test_user_max_size_script_error(client, upload_dir, mocker):
    # Create a test file
    test_file_name = "testfile"
    create_test_file(
        upload_dir,
        test_file_name,
        "juvati_be@uol.com.br inbox 000232478 size 012345671",
    )

    # Mock subprocess.run to raise a CalledProcessError
    mocker.patch(
        "subprocess.run", side_effect=subprocess.CalledProcessError(1, "cmd")
    )

    response = client.get(f"/files/user_max_size/{test_file_name}/")
    assert response.status_code == 500
    assert "error" in response.data


def test_user_min_size_file_not_found(client, upload_dir):
    response = client.get("/files/user_min_size/nonexistentfile/")
    assert response.status_code == 404
    assert response.json()["error"] == "File not found."


def test_user_min_size_file_with_data(client, upload_dir, mocker):
    # Create a test file
    test_file_name = "testfile"
    create_test_file(
        upload_dir,
        test_file_name,
        "juvati_be@uol.com.br inbox 000232478 size 012345671",
    )

    # Mock subprocess.run to simulate script output
    mocker.patch(
        "subprocess.run",
        return_value=mocker.Mock(
            stdout="juvati_be@uol.com.br inbox 000232478 size 000123456\n"
        ),
    )

    response = client.get(f"/files/user_min_size/{test_file_name}/")
    assert response.status_code == 200
    assert response.json() == {
        "username": "juvati_be@uol.com.br",
        "folder": "inbox",
        "numberMessages": 232478,
        "size": 123456,
    }


def test_user_min_size_script_error(client, upload_dir, mocker):
    # Create a test file
    test_file_name = "testfile"
    create_test_file(
        upload_dir,
        test_file_name,
        "juvati_be@uol.com.br inbox 000232478 size 012345671",
    )

    # Mock subprocess.run to raise a CalledProcessError
    mocker.patch(
        "subprocess.run", side_effect=subprocess.CalledProcessError(1, "cmd")
    )

    response = client.get(f"/files/user_min_size/{test_file_name}/")
    assert response.status_code == 500
    assert "error" in response.json()


def test_user_list_file_not_found(client, upload_dir):
    response = client.get("/files/users/nonexistentfile/")
    assert response.status_code == 404
    assert response.json()["error"] == "File not found."


def test_user_list_file_with_data(client, upload_dir, mocker):
    # Create a test file
    test_file_name = "input"
    test_file_content = """juvati_be@uol.com.br inbox 000232478 size 012345671
                           bikafmito@uol.com.br inbox 001304054 size 010301448
                        """
    create_test_file(upload_dir, test_file_name, test_file_content)

    # Mock subprocess.run to simulate script output
    mocker.patch(
        "subprocess.run", return_value=mocker.Mock(stdout=test_file_content)
    )

    response = client.get(f"/files/users/{test_file_name}/")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 2
    assert len(response_json["results"]) == 2
    assert response_json["results"][0] == {
        "username": "juvati_be@uol.com.br",
        "folder": "inbox",
        "numberMessages": 232478,
        "size": 12345671,
    }


def test_user_list_script_error(client, upload_dir, mocker):
    # Create a test file
    test_file_name = "input"
    create_test_file(
        upload_dir,
        test_file_name,
        "juvati_be@uol.com.br inbox 000232478 size 012345671",
    )

    # Mock subprocess.run to raise a CalledProcessError
    mocker.patch(
        "subprocess.run", side_effect=subprocess.CalledProcessError(1, "cmd")
    )

    response = client.get(f"/files/users/{test_file_name}/")
    assert response.status_code == 500
    assert "error" in response.json()


def test_user_list_desc_file_not_found(client, upload_dir):
    response = client.get("/files/users_desc/nonexistentfile/")
    assert response.status_code == 404
    assert response.json()["error"] == "File not found."


def test_user_list_desc_file_with_data(client, upload_dir, mocker):
    # Create a test file
    test_file_name = "input"
    test_file_content = """juvati_be@uol.com.br inbox 000232478 size 012345671
                           bikafmito@uol.com.br inbox 001304054 size 010301448
                        """
    create_test_file(upload_dir, test_file_name, test_file_content)

    # Mock subprocess.run to simulate script output
    reversed_content = """bikafmito@uol.com.br inbox 001304054 size 010301448
                          juvati_be@uol.com.br inbox 000232478 size 012345671
                       """
    mocker.patch(
        "subprocess.run", return_value=mocker.Mock(stdout=reversed_content)
    )

    response = client.get(f"/files/users_desc/{test_file_name}/")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 2
    assert len(response_json["results"]) == 2
    assert response_json["results"][0] == {
        "username": "bikafmito@uol.com.br",
        "folder": "inbox",
        "numberMessages": 1304054,
        "size": 10301448,
    }


def test_user_list_desc_script_error(client, upload_dir, mocker):
    # Create a test file
    test_file_name = "input"
    create_test_file(
        upload_dir,
        test_file_name,
        "juvati_be@uol.com.br inbox 000232478 size 012345671",
    )

    # Mock subprocess.run to raise a CalledProcessError
    mocker.patch(
        "subprocess.run", side_effect=subprocess.CalledProcessError(1, "cmd")
    )

    response = client.get(f"/files/users_desc/{test_file_name}/")
    assert response.status_code == 500
    assert "error" in response.json()


def test_user_range_messages_file_not_found(client, upload_dir):
    response = client.get(
        "/files/users_range_messages/nonexistentfile/10/100/"
    )
    assert response.status_code == 404
    assert response.json()["error"] == "File not found."


def test_user_range_messages_file_with_data(client, upload_dir, mocker):
    # Create a test file
    test_file_name = "input"
    test_file_content = """juvati_be@uol.com.br inbox 000232478 size 012345671
                           bikafmito@uol.com.br inbox 000004054 size 010301448
                           thirduser@uol.com.br inbox 000004500 size 012301448
                        """
    create_test_file(upload_dir, test_file_name, test_file_content)

    # Mock subprocess.run to simulate script output
    script_output = """bikafmito@uol.com.br inbox 000004054 size 010301448
                       thirduser@uol.com.br inbox 000004500 size 012301448
                    """
    mocker.patch(
        "subprocess.run", return_value=mocker.Mock(stdout=script_output)
    )

    response = client.get(
        f"/files/users_range_messages/{test_file_name}/10/5000/"
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 2
    assert len(response_json["results"]) == 2
    assert response_json["results"][0] == {
        "username": "bikafmito@uol.com.br",
        "folder": "inbox",
        "numberMessages": 4054,
        "size": 10301448,
    }


def test_user_range_messages_script_error(client, upload_dir, mocker):
    # Create a test file
    test_file_name = "input"
    create_test_file(
        upload_dir,
        test_file_name,
        "juvati_be@uol.com.br inbox 000232478 size 012345671",
    )

    # Mock subprocess.run to raise a CalledProcessError
    mocker.patch(
        "subprocess.run", side_effect=subprocess.CalledProcessError(1, "cmd")
    )

    response = client.get(
        f"/files/users_range_messages/{test_file_name}/10/100/"
    )
    assert response.status_code == 500
    assert "error" in response.json()
