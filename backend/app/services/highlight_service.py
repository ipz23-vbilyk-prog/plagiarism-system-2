import re


# =====================================================
# CLEAN FRAGMENT
# =====================================================

def clean_fragment(

    text: str
):

    # remove extra spaces
    text = re.sub(

        r"\s+",

        " ",

        text
    )

    # remove garbage chars
    text = re.sub(

        r"[^\w\s.,:;()%\-–]",

        "",

        text
    )

    return text.strip()


# =====================================================
# GET CONTEXT
# =====================================================

def get_context(

    full_text: str,

    fragment: str,

    window: int = 120
):

    idx = full_text.find(
        fragment
    )

    if idx == -1:

        return "", ""

    start = max(
        0,
        idx - window
    )

    end = min(
        len(full_text),
        idx + len(fragment) + window
    )

    before = full_text[
        start:idx
    ]

    after = full_text[
        idx + len(fragment):end
    ]

    return (

        before.strip(),

        after.strip()
    )


# =====================================================
# BUILD MATCH
# =====================================================

def build_match(

    full_text: str,

    fragment: str,

    source: str,

    similarity: float
):

    fragment_clean = clean_fragment(
        fragment
    )

    before, after = get_context(

        full_text,

        fragment_clean
    )

    return {

        # IMPORTANT
        # NO *100 HERE
        "similarity": round(
            similarity,
            2
        ),

        "fragment":
            fragment_clean,

        "source":
            source,

        "context_before":
            before,

        "context_after":
            after
    }