import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FilterSelector,
    FieldCondition,
    MatchValue,
    PayloadSchemaType,
)

from app.core.config import settings


class QdrantService:

    def __init__(self):

        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            timeout=300,
        )

        self.collection_name = settings.QDRANT_COLLECTION_NAME

    # --------------------------------------------------
    # Create Collection
    # --------------------------------------------------
    def create_collection(self):

        collections = self.client.get_collections()

        exists = any(
            collection.name == self.collection_name
            for collection in collections.collections
        )

        if not exists:

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE,
                ),
            )

            print(f"Created collection: {self.collection_name}")

        else:

            print("Collection already exists")

        # Always ensure payload index exists
        self.create_payload_indexes()

    # --------------------------------------------------
    # Create Payload Indexes
    # --------------------------------------------------
    def create_payload_indexes(self):

        try:

            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="file_id",
                field_schema=PayloadSchemaType.KEYWORD,
            )

            print("Payload index created for file_id")

        except Exception:

            print("Payload index already exists")

    # --------------------------------------------------
    # Insert Embedding
    # --------------------------------------------------
    def upsert_embedding(
        self,
        embedding: list[float],
        chunk_text: str,
        metadata: dict,
    ):

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "chunk_text": chunk_text,
                **metadata,
            },
        )

        self.client.upsert(
            collection_name=self.collection_name,
            points=[point],
        )

        return point.id

    # --------------------------------------------------
    # Search
    # --------------------------------------------------
    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ):

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=top_k,
        )

        output = []

        for point in results.points:

            output.append(
                {
                    "chunk_text": point.payload.get("chunk_text"),
                    "file_id": point.payload.get("file_id"),
                    "chunk_index": point.payload.get("chunk_index"),
                    "page_number": point.payload.get("page_number"),
                    "score": point.score,
                }
            )

        return output

    # --------------------------------------------------
    # Delete Embeddings for a File
    # --------------------------------------------------
    def delete_file_embeddings(
        self,
        file_id: str,
    ):

        records, _ = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="file_id",
                    match=MatchValue(value=file_id),
                )
            ]
        ),
        with_payload=False,
        with_vectors=False,
        limit=10000,
        )

        if not records:
            print("No embeddings found.")
            return

        point_ids = [record.id for record in records]

        self.client.delete(
            collection_name=self.collection_name,
            points_selector=point_ids,
        )

        print(f"Deleted {len(point_ids)} embeddings.")