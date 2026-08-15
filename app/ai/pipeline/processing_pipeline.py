from pathlib import Path

from app.ai.extractors.extractor_factory import ExtractorFactory
from app.ai.preprocessing.cleaner import TextCleaner
from app.ai.preprocessing.chunker import TextChunker
from app.ai.embeddings.embedding_service import EmbeddingService
from app.ai.vector_store.qdrant_service import QdrantService
from app.services.jobs.job_service import JobService


class ProcessingPipeline:

    def __init__(self):

        self.cleaner = TextCleaner()

        self.chunker = TextChunker(
            chunk_size=500,
            overlap=50,
        )

        self.embedding_service = EmbeddingService()

        self.qdrant_service = QdrantService()

        self.job_service = JobService()

    def process_file(
        self,
        file_path: str,
        file_id: str,
        job_id: str | None = None,
        page_number: int | None = None,
    ):

        try:

            extension = Path(file_path).suffix.lower()

            extractor = ExtractorFactory.get_extractor(extension)

            if extractor is None:
                raise ValueError(
                    f"Unsupported file type: {extension}"
                )

            # -----------------------------
            # Extract Text
            # -----------------------------
            if job_id:
                self.job_service.mark_processing(
                    job_id,
                    "Extracting text..."
                )

            text = extractor.extract_text(file_path)

            # -----------------------------
            # Clean Text
            # -----------------------------
            if job_id:
                self.job_service.update_job(
                    job_id,
                    progress=20,
                    message="Cleaning text..."
                )

            cleaned_text = self.cleaner.clean(text)

            # -----------------------------
            # Chunk Text
            # -----------------------------
            if job_id:
                self.job_service.update_job(
                    job_id,
                    progress=40,
                    message="Chunking document..."
                )

            chunks = self.chunker.split_text(cleaned_text)

            # -----------------------------
            # Generate Embeddings
            # -----------------------------
            if job_id:
                self.job_service.update_job(
                    job_id,
                    progress=60,
                    message="Generating embeddings..."
                )

            total_chunks = len(chunks)

            for index, chunk in enumerate(chunks):

                embedding = self.embedding_service.create_embedding(chunk)

                self.qdrant_service.upsert_embedding(

                    embedding=embedding,

                    chunk_text=chunk,

                    metadata={
                        "file_id": file_id,
                        "file_name": Path(file_path).name,
                        "chunk_index": index,
                        "page_number": page_number,
                        "token_count": len(chunk.split()),
                        "embedding_model": "all-MiniLM-L6-v2",
                    },
                )

                if job_id:

                    progress = 60 + int(
                        ((index + 1) / total_chunks) * 35
                    )

                    self.job_service.update_job(
                        job_id,
                        progress=progress,
                        message=f"Embedding chunk {index + 1}/{total_chunks}"
                    )

            # -----------------------------
            # Completed
            # -----------------------------
            if job_id:
                self.job_service.mark_completed(job_id)

            return total_chunks

        except Exception as e:

            if job_id:
                self.job_service.mark_failed(
                    job_id,
                    str(e)
                )

            raise