# FitFindr — planning.md

> Complete this document before writing any implementation code.
> Your spec and agent diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Your planning.md will be reviewed as part of your submission.
> Update it before starting any stretch features.

---

## Tools

List every tool your agent will use. For each tool, fill in all four fields.
You must have at least 3 tools. The three required tools are listed — add any additional tools below them.

### Tool 1: search_listings

**What it does:**
Searches the clothing listings dataset and returns items that match the user's preferences such as style, category, size, color, and budget.

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `description` (str): User's description of the desired item.
- `size` (str): Desired clothing size.
- `max_price` (float): Maximum budget.


**What it returns:**
<!-- Describe the return value — what fields does a result contain? -->
- id
- title
- description
- category
- size
- condition
- price
- colors
- style_tags
- platform

**What happens if it fails or returns nothing:**
<!-- What should the agent do if no listings match? -->
The agent informs the user that no exact matches were found and suggests similar alternatives.

---

### Tool 2: suggest_outfit

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
Uses a selected listing together with the user's wardrobe to suggest a complete outfit.

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `new_item` (dict): The selected clothing item.
- `wardrobe` (dict): User wardrobe data.

**What it returns:**
<!-- Describe the return value -->
A recommended outfit containing the new item and matching wardrobe pieces.

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the wardrobe is empty or no outfit can be suggested? -->
If the wardrobe is empty, the agent recommends how the item could generally be styled and asks the user to add wardrobe items.

---

### Tool 3: create_fit_card

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
Creates a final outfit summary that explains how the clothing pieces work together.

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `outfit` (str): Outfit recommendation.
- `new_item` (dict): Selected listing.

**What it returns:**
<!-- Describe the return value -->
A formatted fit card containing:

- Item name
- Price
- Platform
- Outfit description
- Styling explanation

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the outfit data is incomplete? -->
The agent returns a simplified recommendation using whatever information is available.

---

### Additional Tools (if any)

<!-- Copy the block above for any tools beyond the required three -->

---

## Planning Loop

**How does your agent decide which tool to call next?**
<!-- Describe the logic your planning loop uses. What does it look at? What conditions change its behavior? How does it know when it's done? --> The agent first calls search_listings() using the user's description, size, and budget. If matching listings are found, the top result is stored and passed to suggest_outfit(). The outfit recommendation is then passed to create_fit_card(). If no listings are found, the workflow stops and the agent returns an informative message instead of continuing.

---

## State Management

**How does information from one tool get passed to the next?**
<!-- Describe how your agent stores and accesses state within a session. What data is tracked? How is it passed between tool calls? -->
The agent stores:

- User query
- Search results
- Selected listing
- Wardrobe information
- Outfit recommendation
- Final fit card

The selected listing returned by search_listings() is stored in the session and passed directly into suggest_outfit(). The outfit returned by suggest_outfit() is stored and then passed into create_fit_card(). All information remains available throughout the session without requiring the user to re-enter it.

---

## Error Handling

For each tool, describe the specific failure mode you're handling and what the agent does in response.

| Tool | Failure mode | Agent response |
|------|-------------|----------------|
| search_listings | No results match the query | Inform the user that no matching items were found and suggest broadening the search. |
| suggest_outfit | Wardrobe is empty | Provide general styling advice and explain that wardrobe-specific recommendations are unavailable. |
| create_fit_card | Outfit input is missing or incomplete | Return a simplified recommendation instead of generating a fit card. |

---

## Architecture

<!-- Draw a diagram of your agent showing how the components connect:
     User input → Planning Loop → Tools (search_listings, suggest_outfit, create_fit_card)
                                                                          ↕
                                                                   State / Session
     Show what triggers each tool, how state flows between them, and where error paths branch off.
     Use ASCII art or a Mermaid diagram (https://mermaid.js.org/syntax/flowchart.html).
     Do NOT embed an image — graders need to read your diagram directly in the file;
     an embedded image or screenshot cannot be evaluated.
     You'll share this diagram with an AI tool when asking it to implement
     the planning loop and each individual tool. -->

---

## AI Tool Plan

<!-- For each part of the implementation below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, your agent diagram)
     - What you expect it to produce
     - How you'll verify the output matches your spec before moving on

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Tool 1 spec (inputs, return value, failure mode) and ask it to implement
     search_listings() using load_listings() from the data loader — then test it against 3 queries
     before trusting it" is a plan. -->

```text
User Query
     |
     v
Planning Loop
     |
     v
search_listings(description, size, max_price)
     |
     +---- No Results ----> Return helpful message
     |
     v
results[0]
     |
     v
Session: selected_item = results[0]
     |
     v
suggest_outfit(selected_item, wardrobe)
     |
     +---- Empty Wardrobe ----> Return general styling advice
     |
     v
Session: outfit_suggestion
     |
     v
create_fit_card(outfit_suggestion, selected_item)
     |
     +---- Missing Data ----> Return simplified recommendation
     |
     v
Session: fit_card
     |
     v
Final Response
```


**Milestone 3 — Individual tool implementations:**
I will generate each tool individually. For search_listings, I will provide the tool specification, inputs, outputs, and failure conditions. I will verify that the implementation correctly filters listings from load_listings() using multiple test queries. For suggest_outfit, I will provide the wardrobe schema and verify that recommended outfits contain matching categories and styles. For create_fit_card, I will provide example outfit outputs and verify that the returned fit card includes all required fields.

**Milestone 4 — Planning loop and state management:**
I will use ChatGPT to generate the planning loop after the tools are complete. I will provide the completed tool specifications and architecture diagram. I will verify that tool outputs are correctly passed between functions and that all failure conditions are handled properly before final testing.
---

## A Complete Interaction (Step by Step)

Write out what a full user interaction looks like from start to finish — tool call by tool call. Use a specific example query.

**Example user query:** "I'm looking for a vintage graphic tee under $30. I mostly wear baggy jeans and chunky sneakers. What's out there and how would I style it?"

**Step 1:**
The agent receives the query:
"I'm looking for a vintage graphic tee under $30."

The agent calls:

search_listings(
    description="vintage graphic tee",
    size=None,
    max_price=30
)

**Step 2:**
search_listings() returns a list of matching items.

The agent selects the top result and stores it as selected_item.

The agent calls:

suggest_outfit(selected_item, wardrobe)

**Step 3:**
suggest_outfit() returns an outfit recommendation.

The agent calls:

create_fit_card(
    outfit_suggestion,
    selected_item
)

**Final output to user:**
The user receives a fit card containing:

- Item name
- Price
- Platform
- Outfit recommendation
- Styling notes
