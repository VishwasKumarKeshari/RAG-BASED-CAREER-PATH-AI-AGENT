from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class NLPCareerMatcher:
    def __init__(self, career_file='data/careers.csv'):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        df = pd.read_csv(career_file)
        self.careers = dict(zip(df['career'], df['description']))
        self.embeddings = {c: self.model.encode(desc) for c, desc in self.careers.items()}

    def predict(self, user_text):
        user_emb = self.model.encode(user_text)
        sims = {c: cosine_similarity([user_emb], [emb])[0][0] for c, emb in self.embeddings.items()}
        best = max(sims, key=sims.get)
        return best, sims[best]
