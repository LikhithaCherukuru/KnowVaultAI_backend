from fastapi.encoders import jsonable_encoder

from app.repositories.files.file_repository import FileRepository
from app.services.jobs.job_service import JobService


class FileService:

    def __init__(self):

        self.repository = FileRepository()
        self.job_service = JobService()

    # --------------------------------------------------
    # Register File Metadata
    # --------------------------------------------------

    def register_file(self, file_data: dict):

        file_data = jsonable_encoder(file_data)

        # Check duplicate using SHA-256 hash
        existing = self.repository.get_file_by_hash(
            file_data["file_hash"]
        )

        if existing:
            return {
                "success": False,
                "message": "Duplicate file already exists.",
                "data": existing
            }

        # Save file metadata
        file = self.repository.register_file(file_data)

        # Create processing job ONLY
        job = self.job_service.create_job(
            user_id=file["user_id"],
            file_id=file["id"]
        )

        # Processing will be handled separately
        # DO NOT call process_file() here

        return {
            "success": True,
            "message": "File registered successfully.",
            "file": file,
            "job": job
        }

    # --------------------------------------------------
    # Register Folder Metadata
    # --------------------------------------------------

    def register_folder(self, folder_data: dict):

        folder_data = jsonable_encoder(folder_data)

        folder = self.repository.register_folder(
            folder_data
        )

        return {
            "success": True,
            "message": "Folder registered successfully.",
            "folder": folder
        }

    # --------------------------------------------------
    # Get All Files
    # --------------------------------------------------

    def get_all_files(self):

        return self.repository.get_all_files()

    # --------------------------------------------------
    # Get All Folders
    # --------------------------------------------------

    def get_all_folders(self):

        return self.repository.get_all_folders()

    # --------------------------------------------------
    # Delete File
    # --------------------------------------------------

    def delete_file(self, file_id: str):

        file = self.repository.get_file_by_id(file_id)

        if not file:
            return {
                "success": False,
                "message": "File not found."
            }

        deleted = self.repository.delete_file(file_id)

        return {
            "success": True,
            "message": "File deleted successfully.",
            "data": deleted
        }

    # --------------------------------------------------
    # Delete Folder
    # --------------------------------------------------

    def delete_folder(self, folder_id: str):

        deleted = self.repository.delete_folder(
            folder_id
        )

        return {
            "success": True,
            "message": "Folder deleted successfully.",
            "data": deleted
        }

    # --------------------------------------------------
    # Scan Folder
    # --------------------------------------------------

    def scan_folder(
        self,
        user_id: str,
        folder_path: str
    ):

        return {
            "success": True,
            "message": "Folder scan request received.",
            "user_id": user_id,
            "folder_path": folder_path
        }

    # --------------------------------------------------
    # Scan Single File
    # --------------------------------------------------

    def scan_single_file(
        self,
        user_id: str,
        file_path: str
    ):

        return {
            "success": True,
            "message": "File scan request received.",
            "data": {
                "user_id": user_id,
                "file_path": file_path
            }
        }