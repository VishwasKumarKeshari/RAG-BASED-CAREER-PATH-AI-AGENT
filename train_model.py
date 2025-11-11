import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from utils import skills_normalizer_fn, to_dense_fn


os.makedirs('models', exist_ok=True)
data = pd.read_csv('data/careers.csv')

X = data[['degree', 'branch', 'skills']]
y = data['career']

# Define a small preprocessing pipeline:
# - OneHotEncode categorical columns (degree, branch)
# - Convert skills separators (| or ,) to spaces and apply TF-IDF

skills_transformer = Pipeline([
    ("norm", FunctionTransformer(skills_normalizer_fn, validate=False)),
    ("tfidf", TfidfVectorizer())
])

preprocessor = ColumnTransformer(transformers=[
    ("cat", OneHotEncoder(handle_unknown='ignore'), ['degree', 'branch']),
    ("skills", skills_transformer, 'skills')
], remainder='drop')

# Some transformers (like OneHotEncoder or TfidfVectorizer) may produce sparse output.
# RandomForestClassifier requires dense arrays, so convert to dense if needed before the classifier.
to_dense = FunctionTransformer(to_dense_fn, validate=False)

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("to_dense", to_dense),
    ("clf", RandomForestClassifier(random_state=42))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit expects a 2D input with column names (DataFrame)
pipeline.fit(X_train, y_train)

joblib.dump(pipeline, 'models/career_classifier.pkl')
print('✅ Pipeline trained and saved at models/career_classifier.pkl')
