import pandas as pd


def normalize_skills(series_like):
    # Accept pandas Series or numpy array-like and return a pandas Series of cleaned strings
    if hasattr(series_like, 'fillna'):
        s = series_like.fillna('').astype(str)
    else:
        s = pd.Series(series_like).fillna('').astype(str)
    return s.str.replace(r'[|,]', ' ', regex=True)


def skills_normalizer_fn(X):
    # Function for FunctionTransformer: return a 1D numpy array of cleaned skill strings
    return normalize_skills(X).to_numpy()


def to_dense_fn(X):
    return X.toarray() if hasattr(X, "toarray") else X
