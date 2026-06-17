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
    """
    Search the mock listings dataset for items matching the description,
    optional size, and optional price ceiling.

    Args:
        description: Keywords describing what the user is looking for
                     (e.g., "vintage graphic tee").
        size:        Size string to filter by, or None to skip size filtering.
                     Matching is case-insensitive (e.g., "M" matches "S/M").
        max_price:   Maximum price (inclusive), or None to skip price filtering.

    Returns:
        A list of matching listing dicts, sorted by relevance (best match first).
        Returns an empty list if nothing matches — does NOT raise an exception.

    Each listing dict has the following fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand, platform

    TODO:
        1. Load all listings with load_listings().
        2. Filter by max_price and size (if provided).
        3. Score each remaining listing by keyword overlap with `description`.
        4. Drop any listings with a score of 0 (no relevant matches).
        5. Sort by score, highest first, and return the listing dicts.

    Before writing code, fill in the Tool 1 section of planning.md.
    """
    listings = load_listings()

    keywords = description.lower().split()
    matches = []

    for listing in listings:

        if max_price is not None and listing["price"] > max_price:
            continue

        if size is not None and size.strip():
            if size.lower() not in listing["size"].lower():
                continue

        text = (
            listing["title"] + " "
            + listing["description"] + " "
            + " ".join(listing["style_tags"])
        ).lower()

        score = sum(1 for word in keywords if word in text)

        if score > 0:
            matches.append((score, listing))

    matches.sort(key=lambda x: x[0], reverse=True)

    return [listing for score, listing in matches]
    
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

    results = search_listings(
        description="vintage graphic tee",
        max_price=30
    )

    wardrobe = get_example_wardrobe()

    outfit = suggest_outfit(
        results[0],
        wardrobe
    )

    fit_card = create_fit_card(
    outfit,
    results[0]
    )

    print(fit_card)
