from difflib import SequenceMatcher


# =====================================================
# CHECK PLAGIARISM
# =====================================================

def check_plagiarism(
    new_text,
    existing_documents
):

    # =========================
    # NO DOCUMENTS
    # =========================

    if len(existing_documents) == 0:

        return {
            "similarity": 0,
            "level": "low",
            "matches": []
        }

    max_similarity = 0

    matches = []

    # =========================
    # COMPARE
    # =========================

    for doc in existing_documents:

        old_text = doc.get("text", "")

        similarity = SequenceMatcher(

            None,

            new_text.lower(),

            old_text.lower()

        ).ratio()

        similarity_percent = round(
            similarity * 100,
            2
        )

        if similarity_percent > max_similarity:

            max_similarity = similarity_percent

        if similarity_percent > 20:

            matches.append({

                "source":
                    doc["filename"],

                "similarity":
                    similarity_percent,

                "fragment":
                    old_text[:300]
            })

    # =========================
    # LEVEL
    # =========================

    level = "low"

    if max_similarity >= 30:
        level = "medium"

    if max_similarity >= 70:
        level = "high"

    # =========================
    # RESULT
    # =========================

    return {

        "similarity":
            max_similarity,

        "level":
            level,

        "matches":
            matches
    }