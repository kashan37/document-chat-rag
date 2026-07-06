from sentence_transformers import SentenceTransformer


class EmbeddingModel:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def encode_chunks(self, chunks):
        embeddings = self.model.encode(chunks)

        return embeddings