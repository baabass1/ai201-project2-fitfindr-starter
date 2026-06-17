"""
tools.py

The three required FitFindr tools. Each tool is a standalone function that
can be called and tested independently before being wired into the agent loop.

Complete and test each tool before moving to agent.py.

Tools:
    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)              → str
    create_fit_card(outfit, new_item)               → str
"""

import os

from dotenv import load_dotenv
from groq import Groq

from utils.data_loader import load_listings

load_dotenv()


# ── Groq client ───────────────────────────────────────────────────────────────

def _get_groq_client():
    """Initialize and return a Groq client using GROQ_API_KEY from .env."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not set. Add it to a .env file in the project root."
        )
    return Groq(api_key=api_key)


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:

    listings = load_listings()

    NOISE_WORDS = {"size", "8", "7", "9", "10", "the", "a", "an"}

    query_words = [
        w for w in description.lower().split()
    if w not in NOISE_WORDS
]
    matches = []

    for item in listings:

        # ── PRICE FILTER ─────────────────────────────
        if max_price is not None and item["price"] > max_price:
            continue

        # ── SIZE FILTER ──────────────────────────────
        if size is not None and size.strip():
            if size.lower() not in item["size"].lower():
                continue

        # ── BUILD SEARCH TEXT ────────────────────────
        text = (
            item["title"] + " " +
            item["description"] + " " +
            " ".join(item["style_tags"])
        ).lower()

        # ── SCORING SYSTEM (KEY FIX) ─────────────────
        score = 0

        for word in query_words:
            if word in text:
                score += 2   # stronger weight

        # boost exact title match
        if any(word in item["title"].lower() for word in query_words):
            score += 3

        # discard weak matches
        if score == 0:
            continue

        matches.append((score, item))

    # ── SORT BY BEST MATCH ─────────────────────────
    matches.sort(key=lambda x: x[0], reverse=True)

    return [item for score, item in matches]
    
# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest 1–2 complete outfits.

    Args:
        new_item: A listing dict (the item the user is considering buying).
        wardrobe: A wardrobe dict with an 'items' key containing a list of
                  wardrobe item dicts. May be empty — handle this gracefully.

    Returns:
        A non-empty string with outfit suggestions.
        If the wardrobe is empty, offer general styling advice for the item
        rather than raising an exception or returning an empty string.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If empty: call the LLM with a prompt for general styling ideas
           (what kinds of items pair well, what vibe it suits, etc.).
        3. If not empty: format the wardrobe items into a prompt and ask
           the LLM to suggest specific outfit combinations using the new item
           and named pieces from the wardrobe.
        4. Return the LLM's response as a string.

    Before writing code, fill in the Tool 2 section of planning.md.
    """
    if not wardrobe.get("items"):
        return f"""
        The {new_item['title']} would pair well with jeans, neutral sneakers,
        and a simple jacket. It works best for a casual everyday streetwear look.
        """

    wardrobe_items = wardrobe["items"][:3]

    outfit = f"Style the {new_item['title']} with "

    for item in wardrobe_items:
        outfit += item["name"] + ", "

    outfit += "for a coordinated outfit."

    return outfit
    


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Generate a short, shareable outfit caption for the thrifted find.
    """

    if not outfit.strip():
        return "Unable to create fit card because outfit information is missing."

    fit_card = f"""
FIT CARD

Item: {new_item['title']}
Price: ${new_item['price']}
Platform: {new_item['platform']}

Outfit:
{outfit}

Style Notes:
This outfit creates a clean and coordinated look while keeping the thrifted item as the main focus.
"""

    return fit_card


from utils.data_loader import get_example_wardrobe

if __name__ == "__main__":

    tests = [
        "white sneakers size 8",
        "vintage graphic tee",
        "grunge jacket",
        "black hoodie"
    ]

    for q in tests:
        print("\n====================")
        print("QUERY:", q)
        print("====================")

        results = search_listings(q, size=None, max_price=100)

        for r in results[:3]:
            print(r["title"], "-", r["price"])