from fastapi import APIRouter, HTTPException, BackgroundTasks

from app.schemas.files.register_file_schema import RegisterFileRequest
from app.schemas.files.register_folder_schema import RegisterFolderRequest
from app.schemas.files.scan_folder_schema import ScanFolderRequest
from app.schemas.files.scan_file_schema import ScanFileRequest

from app.services.files.file_service import FileService
from app.services.jobs.job_service import JobService

from app.ai.pipeline.processing_pipeline import ProcessingPipeline


router = APIRouter(
    prefix="/api/v1/files",
    tags=["Files"],
)


# --------------------------------------------------
# Services
# --------------------------------------------------

service = FileService()
job_service = JobService()
pipeline = ProcessingPipeline()


# --------------------------------------------------
# Sync File Metadata
# --------------------------------------------------

@router.post("/sync")
def sync_file(request: RegisterFileRequest):

    try:

        result = service.register_file(
            request.model_dump(mode="json")
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# --------------------------------------------------
# Sync Folder Metadata
# --------------------------------------------------

@router.post("/folders/sync")
def sync_folder(request: RegisterFolderRequest):

    try:

        result = service.register_folder(
            request.model_dump(mode="json")
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# --------------------------------------------------
# Get All Files
# --------------------------------------------------

@router.get("/")
def get_files():

    try:

        return service.get_all_files()

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# --------------------------------------------------
# Get All Folders
# --------------------------------------------------

@router.get("/folders")
def get_folders():

    try:

        return service.get_all_folders()

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# --------------------------------------------------
# Delete File
# --------------------------------------------------

@router.delete("/{file_id}")
def delete_file(file_id: str):

    try:

        return service.delete_file(file_id)

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# --------------------------------------------------
# Delete Folder
# --------------------------------------------------

@router.delete("/folders/{folder_id}")
def delete_folder(folder_id: str):

    try:

        return service.delete_folder(folder_id)

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# --------------------------------------------------
# Scan Folder
# --------------------------------------------------

@router.post("/scan-folder")
def scan_folder(request: ScanFolderRequest):

    try:

        return service.scan_folder(
            request.user_id,
            request.folder_path
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# --------------------------------------------------
# Scan Single File
# --------------------------------------------------

@router.post("/scan-file")
def scan_file(
    request: ScanFileRequest,
    background_tasks: BackgroundTasks
):

    try:

        result = service.scan_single_file(
            request.user_id,
            request.file_path
        )

        if not result["success"]:
            return result

        file = result["data"]

        # Create processing job
        job = job_service.create_job(
            user_id=file["user_id"],
            file_id=file["id"]
        )

        # Start background processing
        background_tasks.add_task(
            pipeline.process_file,
            file["local_path"],
            file["id"],
            job["id"]
        )

        return {
            "success": True,
            "message": "File queued for processing.",
            "file": file,
            "job": job
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )