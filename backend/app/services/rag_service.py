from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)
import uuid


class ResumeRAG:

    def __init__(self):

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        self.client = QdrantClient(
            path="./qdrant_data"
        )

        self.collection = "resume_chunks"

        self.vector_size = 384

        self._initialize_collection()

    def _initialize_collection(self):

        collections = [
            collection.name
            for collection in
            self.client.get_collections().collections
        ]

        if self.collection not in collections:

            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE
                )
            )

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 500,
        overlap: int = 75
    ):

        words = text.split()

        chunks = []

        start = 0

        while start < len(words):

            end = start + chunk_size

            chunks.append(
                " ".join(words[start:end])
            )

            start += chunk_size - overlap

        return chunks

    def index_resume(
        self,
        resume_id: str,
        text: str
    ):

        chunks = self.chunk_text(text)

        embeddings = self.model.encode(
            chunks,
            normalize_embeddings=True
        )

        points = []

        for chunk, embedding in zip(
            chunks,
            embeddings
        ):

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),

                    vector=embedding.tolist(),

                    payload={
                        "resume_id": resume_id,
                        "text": chunk
                    }
                )
            )

        if points:

            self.client.upsert(
                collection_name=self.collection,
                points=points
            )

    def retrieve(
        self,
        resume_id: str,
        query: str,
        limit: int = 3
    ):

        query_vector = self.model.encode(
            query,
            normalize_embeddings=True
        ).tolist()

        results = self.client.query_points(
            collection_name=self.collection,

            query=query_vector,

            query_filter={
                "must": [
                    {
                        "key": "resume_id",
                        "match": {
                            "value": resume_id
                        }
                    }
                ]
            },

            limit=limit
        )

        return [
            result.payload["text"]
            for result in results.points
        ]