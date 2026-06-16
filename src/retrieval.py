from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class HybridRetriever:

    def __init__(self, events):

        self.events = events

        corpus = [
            e.content.lower().split()
            for e in events
        ]

        self.bm25 = BM25Okapi(corpus)

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.embeddings = self.model.encode(
            [e.content for e in events],
            normalize_embeddings=True
        )

    def retrieve(
        self,
        query,
        k=40
    ):

        bm25_scores = self.bm25.get_scores(
            query.lower().split()
        )

        query_embedding = self.model.encode(
            query,
            normalize_embeddings=True
        )

        vector_scores = cosine_similarity(
            [query_embedding],
            self.embeddings
        )[0]

        combined = []

        for idx, event in enumerate(self.events):

            score = (
                0.4 * bm25_scores[idx]
                + 0.6 * vector_scores[idx]
            )

            combined.append(
                (event, float(score))
            )

        combined.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return combined[:k]