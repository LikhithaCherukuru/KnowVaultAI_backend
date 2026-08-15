import time

from app.services.jobs.job_service import JobService
from app.repositories.files.file_repository import FileRepository
from app.ai.pipeline.processing_pipeline import ProcessingPipeline


class BackgroundWorker:

    def __init__(self):

        self.jobs = JobService()

        self.files = FileRepository()

        self.pipeline = ProcessingPipeline()

    def run(self):

        print("Background Worker Started...")

        while True:

            jobs = self.jobs.get_pending_jobs()

            if not jobs:

                time.sleep(3)

                continue

            for job in jobs:

                try:

                    file = self.files.get_file_by_id(
                        job["file_id"]
                    )

                    if file is None:

                        continue

                    self.pipeline.process_file(

                        file_path=file["local_path"],

                        file_id=file["id"],

                        job_id=job["id"]

                    )

                except Exception as e:

                    print(e)

            time.sleep(1)