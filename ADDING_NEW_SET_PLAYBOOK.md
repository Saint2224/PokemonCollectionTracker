# Adding A New Set Playbook

This playbook documents the exact workflow used to add recent sets (including API-backed additions) with high accuracy and low request usage.

## Goal

Add a new set to the tracker with:
- Correct card list (card-only unless intentionally including sealed)
- Correct order (collector-number order)
- Correct image source (front-facing art)
- Working ownership/pending controls (already generic in app)
- Minimal JustTCG API usage (free-tier friendly)

## Where Set Data Lives

- Main app/data file: index.html
- Set arrays: inline JS arrays (for example: baseCards, thirtyAnniversaryMainCards, destinedRivalsCards)
- Set registry: the sets object
- Image resolution: getCardThumbUrl and getCardLargeUrl

## Recommended Low-Request Workflow

### 1) Find the set slug once (1 request)

Use the sets endpoint with a narrow query:
- GET /v1/sets?limit=20&offset=0&q=Destined Rivals

Capture:
- set id slug (example: sv10-destined-rivals-pokemon)
- display name (example: SV10: Destined Rivals)
- cards_count for sanity checks

### 2) Pull cards by set slug with pagination (few requests)

Use:
- GET /v1/cards?set=<set-slug>&limit=20&offset=<offset>

Notes:
- Free tier requires limit <= 20.
- Increment offset by 20 until meta.hasMore is false.
- Add small delay between requests (for example 300-500ms).
- On 429, use exponential backoff and retry.

### 3) Filter to card rows (exclude sealed/product rows)

Keep rows where:
- number is present
- number is not N/A
- number matches collector format (for numbered sets, usually NNN/DDD)

This removes bundles/tins/boxes/cases and similar non-card records.

### 4) Dedupe and sort

- Dedupe by collector number string (first occurrence is usually fine)
- Sort by leading numeric collector value
- Keep collectorNum exactly as returned (for display and traceability)

### 5) Generate the array block

Create entries like:
- num: numeric sort/display anchor
- name: card name
- collectorNum: exact collector number text
- imageToken: API card id slug
- tcgplayerId: for front-image resolution

Example shape:

```js
{num:1,name:"Card Name",collectorNum:"001/182",imageToken:"pokemon-...",tcgplayerId:"123456"}
```

### 6) Register set in sets object

Add a set entry with:
- Stable key (for example destinedrivals)
- name
- justtcgSetNames (array with canonical set name)
- color variable
- src (short code, informational for custom sets)
- vars: ['unl']
- cards: the array variable

### 7) Wire image strategy

Preferred for custom sets:
- Use tcgplayerId URLs first (front images)
- Fallback only if needed

For thumb:
- https://product-images.tcgplayer.com/fit-in/437x437/<tcgplayerId>.jpg

For large:
- https://product-images.tcgplayer.com/<tcgplayerId>.jpg

If tcgplayerId is missing, fallback to existing resolver strategy for that set.

## Validation Checklist

1. Syntax/diagnostics:
- No errors in index.html

2. Render checks in localhost:
- New set appears in UI
- Card count matches filtered list
- First cards start at expected numbers
- Last cards end at expected numbers
- No sealed products mixed into card list (unless intended)

3. Image checks:
- Thumbnails are front-facing
- Large image modal opens expected art

4. Order checks:
- Cards are in collector-number order

## Request Budgeting (100/day Friendly)

Use this estimate before import:
- requests ~= ceil(total_rows / 20)

Example:
- 281 rows -> 15 requests

Best practices:
- Do one set pull, then transform locally.
- Avoid per-card search endpoints for whole-set ingestion.
- Reuse fetched payload to generate array and stats in one run.
- Log request count and stop if nearing daily limit.

## Common Pitfalls

- Using public Explore HTML/RSC only: often incomplete vs API dataset.
- Mixing set search query results from neighboring sets/promos.
- Treating cards_count as guaranteed numbered-card count.
- Using image sources that return placeholders/backs for some custom sets.

## Minimal Repeatable Procedure

1. Discover set slug from /v1/sets.
2. Page /v1/cards?set=<slug>&limit=20&offset=...
3. Filter to numbered card rows.
4. Dedupe by collector number.
5. Sort numerically.
6. Emit array into index.html.
7. Register set in sets object.
8. Use tcgplayerId image URLs (thumb + large).
9. Reload localhost and verify counts/order/images.

## Notes For Future Automation

This process can be scripted safely for future sets:
- Input: set slug
- Output: ready-to-paste array + optional set registry snippet
- Add dry-run mode to print request count, first/last numbers, and sample rows before writing.
