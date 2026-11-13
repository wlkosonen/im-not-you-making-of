# Fleet test 3: an even mix of the four lines (8 Nov 2026)

Lati, 8 Nov: "f5-2 is workable. but lets compact now, new prompt. we will continue right afterm wiht your two suggested
tests." Then: "yes to both, let em rip". Why: F5·2's escorts are mostly Claude's white line (`fleet-test-2.md`).
Seedream 5 Pro (6a50079fc28ed5bfe5576f54), medium tier, 5.85 + 0.39 per reference.

References: V1·1 Claude 6aefc73d4882a6c43792a738, V2·2 Gemini 6aefc7423f29a0ea51821d5f, V3·2 ChatGPT
6aefc7451e8e47e222dd3b3e, V4·1 Grok 6aefc747c6cf1e266452f067; F5·2 6aefc8eb1465638e136a936b.

## A: line sheets, then the fleet

1. **L1-L4 (line sheets):** per maker, its escort classes side by side, noses left, plain grey; the maker's side view as
   the reference. 4 × 2 options × 6.24 = ~50.
2. **F6 (fleet):** the F5 prompt with the escorts evenly divided among the four lines; references = 4 side views + 4
   picked line sheets. 4 × 8.97 = ~36.

## B: layers composited onto F5·2

1. **G2-G4 (escort groups):** Gemini, ChatGPT, Grok escorts on a flat background, F5·2's light, angle and heading;
   references = the line's side view and line sheet. 3 × 2 × ~6.6 = ~40 (est. 37 with one reference).
2. Cut out (0.1 each), composite onto F5·2 in code.
3. **H (harmonise):** one Seedream pass with the composite as reference, 2 × 6.24 = ~13.

Total ~137 credits; balance before 4,409.

## Result (8 Nov), 139.53 credits (est. ~137); balance 4,269.56

Files `media/images/fleet-test-3/` (named `<label>-<mediaId>.jpg`).

| Label | What | mediaId |
|---|---|---|
| L1·1, L1·2 | Claude line sheets | 6aefcbf43a7aea32784999d5, 6aefcbf655205186be26a673 |
| L2·1, L2·2 | Gemini line sheets | 6aefcbf7fd4543e277764ba7, 6aefcbf8a256872491bfba57 |
| L3·1, L3·2 | ChatGPT line sheets | 6aefcbf9512a32c5e50829f8, 6aefcbfb072d03e3c3183866 |
| L4·1, L4·2 | Grok line sheets | 6aefcbfc81748bd39358f131, 6aefcbfd55205186be26ab5c |
| F6·1, F6·2 | fleet, squadrons mixed | 6aefccb393ee9cffa17f1db2, 6aefccb43a7aea32784a384f |
| F6·3, F6·4 | fleet, four wedges | 6aefccb7cc5136e5b26a449b, 6aefccb8fc70b24e0c9c0ffe |
| G2·1/2, G3·1/2, G4·1/2 | escort groups on grey | 6aefccdf…2c28, 6aefcce0…af28, 6aefcce1…3a62, 6aefcce2…148b, 6aefcce4…ed05, 6aefcce5…67c4 |
| C·2 | composite (`tools/fleet/composite.py`, G2·1, G3·2, G4·1 cut out) | 6aefce1981748bd3935aa06c |
| H·1 | harmonised, composite only | 6aefce2d9d0370332ceec26f |
| H·2 | harmonised + V2·2, V3·2, V4·1 | 6aefce2f74ceab81ded9861b |

Kiln's picks to keep A moving (Lati's to change): L1·2, L2·2 (L2·1 copied V2·2's top-down pose), L3·1 (the
rosette exhaust), L4·1. Sheets: `fleet-test-3-sheet-1.jpg` (lines), `-sheet-2.jpg` (F6), `-groups.jpg`, `-sheet-3.jpg`
(B: F5·2, composite, H·1, H·2).

Kiln's read:
- **A works.** F6·1 and F6·2 mix all four lines through the whole frame, every flagship held, noses left. F6·2 is
  the densest. F6·3 splits the fleet into four even wedges but its ChatGPT flagship turns into a fat cylinder;
  F6·4's vessels fly toward the camera, not left.
- **B works too and keeps F5·2.** The 24 composited escorts (8 per line) sit where F5·2 had only white ones. The
  harmonising pass kept every vessel in place: H·1 changes almost nothing; H·2 redraws the linework and grain a little
  more evenly. Where it shows: the ChatGPT exhaust rosettes read as white flowers at small sizes, and a few pasted
  escorts are lit flatter than the plate.
- A gives new frames with an even mix; B keeps the picked F5·2 and fixes its mix. Lati decides.

## Recolour: Gemini iridescent in the picked plates (8 Nov)

Lati: "Recolour the fleet shots." then "Yes to both". Seedream edits with the plate and I·1 as references, 2 each, 26.52
credits. R·F6·4·1 6af07189512a32c5e58155df, R·F6·4·2 6af0718a3a93c271b51bcf6c, R·H·2·1 6af0718b81748bd393d83c49,
R·H·2·2 6af0718c5661f7145fa3d181; sheet `fleet-recolour.jpg`. Kiln's read: composition, every vessel and the black hole
held in all four; the Gemini flagship and its escorts carry the sheen, no stripe left. Lati picks which replace F6·4
and H·2.
