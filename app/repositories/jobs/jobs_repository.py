from datetime import datetime

from app.core.database import get_supabase


class JobRepository:

    def __init__(self):

        self.db = get_supabase()

    # -----------------------------------
    # Create Job
    # -----------------------------------
    def create_job(self, data: dict):

        result = (

            self.db

            .table("processing_jobs")

            .insert(data)

            .execute()

        )

        return result.data[0]

    # -----------------------------------
    # Get Job
    # -----------------------------------
    def get_job(self, job_id: str):

        result = (

            self.db

            .table("processing_jobs")

            .select("*")

            .eq("id", job_id)

            .single()

            .execute()

        )

        return result.data

    # -----------------------------------
    # Get Pending Job
    # -----------------------------------
    def get_pending_job(self):

        result = (

            self.db

            .table("processing_jobs")

            .select("*")

            .eq("status", "PENDING")

            .order("created_at")

            .limit(1)

            .execute()

        )

        if not result.data:

            return None

        return result.data[0]

    # -----------------------------------
    # Update Job
    # -----------------------------------
    def update_job(

        self,

        job_id: str,

        data: dict,

    ):

        result = (

            self.db

            .table("processing_jobs")

            .update(data)

            .eq("id", job_id)

            .execute()

        )

        return result.data[0]

    # -----------------------------------
    # Start Job
    # -----------------------------------
    def start_job(

        self,

        job_id: str,

        worker_name: str,

    ):

        result = (

            self.db

            .table("processing_jobs")

            .update(

                {

                    "status": "PROCESSING",

                    "started_at": datetime.utcnow().isoformat(),

                    "worker_name": worker_name,

                }

            )

            .eq("id", job_id)

            .execute()

        )

        return result.data[0]

    # -----------------------------------
    # Finish Job
    # -----------------------------------
    def finish_job(self, job_id: str):

        result = (

            self.db

            .table("processing_jobs")

            .update(

                {

                    "status": "COMPLETED",

                    "progress": 100,

                    "completed_at": datetime.utcnow().isoformat(),

                }

            )

            .eq("id", job_id)

            .execute()

        )

        return result.data[0]

    # -----------------------------------
# Get Pending Jobs
# -----------------------------------

def get_pending_jobs(self):

    result = (

        self.db

        .table("processing_jobs")

        .select("*")

        .eq("status", "PENDING")

        .order("created_at")

        .execute()

    )

    return result.data