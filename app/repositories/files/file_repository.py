from supabase import Client

from app.core.database import get_supabase


class FileRepository:

    def __init__(self):
        self.db: Client = get_supabase()

    # -----------------------------
    # Register File Metadata
    # -----------------------------
    def register_file(self, file_data: dict):

        response = (
            self.db
            .table("files")
            .insert(file_data)
            .execute()
        )

        return response.data[0]

    # -----------------------------
    # Register Folder Metadata
    # -----------------------------
    def register_folder(self, folder_data: dict):

        response = (
            self.db
            .table("folders")
            .insert(folder_data)
            .execute()
        )

        return response.data[0]

    # -----------------------------
    # Get All Files
    # -----------------------------
    def get_all_files(self):

        response = (
            self.db
            .table("files")
            .select("*")
            .execute()
        )

        return response.data

    # -----------------------------
    # Get All Folders
    # -----------------------------
    def get_all_folders(self):

        response = (
            self.db
            .table("folders")
            .select("*")
            .execute()
        )

        return response.data

    # -----------------------------
    # Find Duplicate
    # -----------------------------
    def get_file_by_hash(self, file_hash: str):

        response = (
            self.db
            .table("files")
            .select("*")
            .eq("file_hash", file_hash)
            .execute()
        )

        return response.data

    # -----------------------------
    # Get File By ID
    # -----------------------------
    def get_file_by_id(self, file_id: str):

        response = (
            self.db
            .table("files")
            .select("*")
            .eq("id", file_id)
            .execute()
        )

        if not response.data:
            return None

        return response.data[0]

    # -----------------------------
    # Delete File
    # -----------------------------
    def delete_file(self, file_id: str):

        response = (
            self.db
            .table("files")
            .delete()
            .eq("id", file_id)
            .execute()
        )

        return response.data

    # -----------------------------
    # Delete Folder
    # -----------------------------
    def delete_folder(self, folder_id: str):

        response = (
            self.db
            .table("folders")
            .delete()
            .eq("id", folder_id)
            .execute()
        )

        return response.data