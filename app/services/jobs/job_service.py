from fastapi.encoders import jsonable_encoder

from app.repositories.jobs.jobs_repository import JobRepository


class JobService:

    def __init__(self):

        self.repository = JobRepository()

    # -----------------------------
    # Create Job
    # -----------------------------
    def create_job(
        self,
        user_id: str,
        file_id: str,
    ):

        job = {

            "user_id": user_id,

            "file_id": file_id,

            "status": "PENDING",

            "progress": 0,

            "message": "Waiting to start"

        }

        return self.repository.create_job(
            jsonable_encoder(job)
        )

    # -----------------------------
    # Get Job
    # -----------------------------
    def get_job(self, job_id: str):

        return self.repository.get_job(job_id)

    # -----------------------------
    # Update Job
    # -----------------------------
    def update_job(
        self,
        job_id: str,
        *,
        status=None,
        progress=None,
        message=None,
        error=None,
    ):

        update_data = {}

        if status is not None:
            update_data["status"] = status

        if progress is not None:
            update_data["progress"] = progress

        if message is not None:
            update_data["message"] = message

        if error is not None:
            update_data["error"] = error

        return self.repository.update_job(
            job_id,
            update_data,
        )

    # -----------------------------
    # Convenience Methods
    # -----------------------------
    def mark_processing(self, job_id: str, message: str):

        return self.update_job(
            job_id,
            status="PROCESSING",
            message=message,
        )

    def mark_completed(self, job_id: str):

        return self.update_job(
            job_id,
            status="COMPLETED",
            progress=100,
            message="Completed",
        )

    def mark_failed(
        self,
        job_id: str,
        error: str,
    ):

        return self.update_job(
            job_id,
            status="FAILED",
            message="Failed",
            error=error,
        )

    def get_pending_jobs(self):

        return self.repository.get_pending_jobs()