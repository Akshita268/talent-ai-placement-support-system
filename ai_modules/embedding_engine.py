try:
    # pyrefly: ignore [missing-import]
    from sentence_transformers import SentenceTransformer
    HAS_TRANSFORMERS = True
except Exception:
    HAS_TRANSFORMERS = False

try:
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.feature_extraction.text import TfidfVectorizer
    HAS_SKLEARN = True
except Exception:
    HAS_SKLEARN = False

_model = None

def get_model():
    global _model
    if HAS_TRANSFORMERS and _model is None:
        try:
            _model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception:
            _model = None
    return _model

def get_similarity_score(text1, text2):
    """
    Returns similarity score between 0 and 100.
    Falls back gracefully if sentence-transformers is not available.
    """
    text1 = text1 or ""
    text2 = text2 or ""
    
    # Try using SentenceTransformers if available
    model = get_model()
    if model is not None and HAS_SKLEARN:
        try:
            embedding1 = model.encode([text1])
            embedding2 = model.encode([text2])
            similarity = float(cosine_similarity(embedding1, embedding2)[0][0])
            return round(similarity * 100, 2)
        except Exception:
            pass # Fallback to TF-IDF if model execution fails

    # Fallback 1: TF-IDF Similarity
    if HAS_SKLEARN:
        try:
            vectorizer = TfidfVectorizer()
            tfidf = vectorizer.fit_transform([text1, text2])
            similarity = float((tfidf * tfidf.T).toarray()[0, 1])
            return round(similarity * 100, 2)
        except Exception:
            pass

    # Fallback 2: Python built-in difflib SequenceMatcher
    import difflib
    similarity = difflib.SequenceMatcher(None, text1, text2).ratio()
    return round(similarity * 100, 2)
