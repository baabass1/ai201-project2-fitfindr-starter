# FitFindr — Starter Kit

This starter kit contains everything you need to begin Project 2.

## What's Included

```
ai201-project2-fitfindr-starter/
├── data/
│   ├── listings.json          # 40 mock secondhand listings
│   └── wardrobe_schema.json   # Wardrobe format + example wardrobe
├── utils/
│   └── data_loader.py         # Helper functions for loading the data
├── planning.md                # Your planning template — fill this out first
└── requirements.txt           # Python dependencies
```

## Setup

**macOS / Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

Set your Groq API key in a `.env` file (get a free key at [console.groq.com](https://console.groq.com)):
```
GROQ_API_KEY=your_key_here
```

## The Mock Listings Dataset

`data/listings.json` contains 40 mock secondhand listings across categories (tops, bottoms, outerwear, shoes, accessories) and styles (vintage, y2k, grunge, cottagecore, streetwear, and more).

Each listing has: `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`.

Load it with:
```python
from utils.data_loader import load_listings
listings = load_listings()
```

## The Wardrobe Schema

`data/wardrobe_schema.json` defines the format your agent uses to represent a user's existing wardrobe. It includes:

- `schema`: field definitions for a wardrobe item
- `example_wardrobe`: a sample wardrobe with 10 items you can use for testing
- `empty_wardrobe`: a starting template for a new user

Load an example wardrobe with:
```python
from utils.data_loader import get_example_wardrobe
wardrobe = get_example_wardrobe()
```

## Tool Inventory

### 1. search_listings

- **Inputs:**
  - description (str)
  - size (str or None)
  - max_price (float)

- **Returns:**
  - List of matching clothing items (dicts)
  - Each item includes: id, title, description, size, price, condition, platform


### 2. suggest_outfit

- **Inputs:**
  - selected_item (dict)
  - wardrobe (dict)

- **Returns:**
  - A string describing outfit combinations using wardrobe items + selected item


### 3. create_fit_card

- **Inputs:**
  - outfit_suggestion (str)
  - selected_item (dict)

- **Returns:**
  - Formatted string "fit card" summarizing item + outfit + style notes

---

## Interaction Walkthrough

**User query:**
"vintage graphic tee under $30, size M"


**Step 1 — Tool called:**
- Tool: search_listings
- Input:
  description = "vintage graphic tee under $30"
  size = "M"
  max_price = 30
- Why this tool:
  To find matching clothing items from the dataset
- Output:
  List of matching vintage graphic tees, ranked by relevance


**Step 2 — Tool called:**
- Tool: suggest_outfit
- Input:
  selected_item = top search result
  wardrobe = user wardrobe
- Why this tool:
  To generate styling suggestions using existing wardrobe items
- Output:
  Outfit description combining tee with jeans/tops/etc.


**Step 3 — Tool called:**
- Tool: create_fit_card
- Input:
  outfit_suggestion + selected_item
- Why this tool:
  To format final output into a clean user-facing card
- Output:
  Final structured fit card


**Final output to user:**
A formatted listing + outfit suggestion + fit card

---

## Error Handling and Fail Points

| Tool | Failure mode | Agent response |
|------|-------------|----------------|
| search_listings | No matching items found | Set `session["error"] = "No matching items found."` and stop pipeline |
| suggest_outfit | Wardrobe is empty | Return general styling advice instead of outfit combinations |
| create_fit_card | Missing or empty outfit string | Return fallback message: "Unable to create fit card due to missing data." |

---

## Spec Reflection

**One way planning.md helped during implementation:**

It helped structure the overall flow of the agent by clearly defining how the query should move through search, outfit generation, and final formatting. This made it easier to implement the tool chain step-by-step without mixing responsibilities.

---

**One divergence from your spec, and why:**

I simplified the parsing step in agent.py by directly using the raw query instead of building a complex NLP parser. This was done to prioritize correctness and ensure reliable matching with the mock dataset.

---

## Where to Start

1. **Read `planning.md` and fill it out before writing any code.**
2. Verify the data loads correctly by running `python utils/data_loader.py`.
3. Build and test each tool individually before connecting them through your planning loop.

Your implementation files go in this same directory. There's no required file structure for your agent code — organize it however makes sense for your design.
