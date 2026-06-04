from backend.app.services.text_extractor import (
    extract_text
)

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)

import os

UPLOAD_DIR = "uploads"


def check_plagiarism(file_path: str):

    new_text = extract_text(file_path)

    if not new_text.strip():

        return {

            "similarity": 0,

            "level": "low",

            "matches": []
        }

    texts = []
    filenames = []

    for filename in os.listdir(UPLOAD_DIR):

        existing_path = os.path.join(
            UPLOAD_DIR,
            filename
        )

        if existing_path == file_path:
            continue

        try:

            text = extract_text(existing_path)

            if text.strip():

                texts.append(text)

                filenames.append(filename)

        except:
            pass

    if not texts:

        return {

            "similarity": 0,

            "level": "low",

            "matches": []
        }

    all_texts = texts + [new_text]

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        all_texts
    )

    similarity_scores = cosine_similarity(
        vectors[-1],
        vectors[:-1]
    )[0]

    max_similarity = max(similarity_scores)

    similarity_percent = round(
        max_similarity * 100,
        2
    )

    if similarity_percent < 30:

        level = "low"

    elif similarity_percent < 70:

        level = "medium"

    else:

        level = "high"

    matches = []

    for i, score in enumerate(similarity_scores):

        if score > 0.1:

            matches.append({

                "source": filenames[i],

                "similarity": round(
                    score * 100,
                    2
                ),

                "fragment":
                "Виявлено схожий текст"
            })

    return {

        "similarity": similarity_percent,

        "level": level,

        "matches": matches
    }