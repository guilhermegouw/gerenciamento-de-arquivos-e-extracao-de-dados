import logging
import os

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .pagination import CustomPagination
from .serializers import FileListSerializer, FileUploadSerializer
from .utils import (
    is_valid_file_name,
    parse_line,
    run_script,
    save_file,
    setup_file_paths,
)


class FileUploadView(APIView):
    serializer_class = FileUploadSerializer

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data["file"]
            file_name = file.name

            # Validate file name
            if not is_valid_file_name(file_name):
                return Response(
                    {"error": "File name has invalid characters."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            status_code = save_file(file, file_name)

            return Response(status=status_code)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileListView(APIView):
    def get(self, request):
        upload_dir = os.path.join(settings.MEDIA_ROOT, "uploaded_files")
        files = []

        if os.path.exists(upload_dir):
            for file_name in os.listdir(upload_dir):
                file_path = os.path.join(upload_dir, file_name)
                if os.path.isfile(file_path):
                    files.append(
                        {
                            "file_name": file_name,
                            "file_size": os.path.getsize(file_path),
                        }
                    )

        paginator = CustomPagination()
        paginated_files = paginator.paginate_queryset(files, request)
        serializer = FileListSerializer(paginated_files, many=True)
        return paginator.get_paginated_response(serializer.data)


class UserMaxSizeView(APIView):
    def get(self, request, file_name):
        file_path, script_path = setup_file_paths(file_name, "max-min-size.sh")
        if file_path is None:
            return script_path

        line, error_response = run_script(script_path, file_path)
        if error_response:
            return error_response

        if line:
            data = parse_line(line)
            logging.info("Successfully parsed line: %s", data)
            return Response(data, status=status.HTTP_200_OK)
        else:
            logging.error("No data found in file: %s", file_path)
            return Response(
                {"error": "No data found in file."},
                status=status.HTTP_404_NOT_FOUND,
            )


class UserMinSizeView(APIView):
    def get(self, request, file_name):
        file_path, script_path = setup_file_paths(file_name, "max-min-size.sh")
        if file_path is None:
            return script_path

        line, error_response = run_script(script_path, file_path, "-min")
        if error_response:
            return error_response

        if line:
            data = parse_line(line)
            logging.info("Successfully parsed line: %s", data)
            return Response(data, status=status.HTTP_200_OK)
        else:
            logging.error("No data found in file: %s", file_path)
            return Response(
                {"error": "No data found in file."},
                status=status.HTTP_404_NOT_FOUND,
            )


class UserListView(APIView):
    def get(self, request, file_name):
        file_path, script_path = setup_file_paths(
            file_name, "order-by-username.sh"
        )
        if file_path is None:
            return script_path

        lines, error_response = run_script(script_path, file_path)
        if error_response:
            return error_response

        if lines:
            data = [
                parse_line(line) for line in lines.split("\n") if line.strip()
            ]
            paginator = CustomPagination()
            paginated_data = paginator.paginate_queryset(data, request)
            logging.info("Successfully parsed lines: %s", paginated_data)
            return paginator.get_paginated_response(paginated_data)
        else:
            logging.error("No data found in file: %s", file_path)
            return Response(
                {"error": "No data found in file."},
                status=status.HTTP_404_NOT_FOUND,
            )


class UserListDescView(APIView):
    def get(self, request, file_name):
        file_path, script_path = setup_file_paths(
            file_name, "order-by-username.sh"
        )
        if file_path is None:
            return script_path

        lines, error_response = run_script(script_path, file_path, "-desc")
        if error_response:
            return error_response

        if lines:
            data = [
                parse_line(line) for line in lines.split("\n") if line.strip()
            ]
            paginator = CustomPagination()
            paginated_data = paginator.paginate_queryset(data, request)
            logging.info("Successfully parsed lines: %s", paginated_data)
            return paginator.get_paginated_response(paginated_data)
        else:
            logging.error("No data found in file: %s", file_path)
            return Response(
                {"error": "No data found in file."},
                status=status.HTTP_404_NOT_FOUND,
            )


class UserRangeMessagesView(APIView):
    def get(self, request, file_name, min_msgs, max_msgs):
        file_path, script_path = setup_file_paths(file_name, "between-msgs.sh")
        if file_path is None:
            return script_path

        lines, error_response = run_script(
            script_path, file_path, str(min_msgs), str(max_msgs)
        )
        if error_response:
            return error_response

        if lines:
            data = [
                parse_line(line) for line in lines.split("\n") if line.strip()
            ]
            paginator = CustomPagination()
            paginated_data = paginator.paginate_queryset(data, request)
            logging.info("Successfully parsed lines: %s", paginated_data)
            return paginator.get_paginated_response(paginated_data)
        else:
            logging.error("No data found in file: %s", file_path)
            return Response(
                {"error": "No data found in file."},
                status=status.HTTP_404_NOT_FOUND,
            )
