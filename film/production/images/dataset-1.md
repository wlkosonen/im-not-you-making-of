# Dataset 1: training candidates for her LoRA (7 Nov 2026)

Lati: "her sheet first, fix the layout and build the dataset, Let me review and pick generated images before those are
used for LoRA training." Seedream 5 Pro edits, references: the turnaround and the expression sheet split from sheet E
(`media/images/face-sheet-1/`). Every candidate is checked for adult proportions first (her.md); Lati picks.

Each prompt is the style block + the identity block + one variation line. Varied on purpose: framing, angle,
expression, light, setting; no low angles on the skirt (canon).

**Style block:** 1980年代の劇場用SFアニメの一場面、手描きセル画、作画と原画の緻密な線、二値のセル塗り、手描きの背景美術、柔らかなフィルムグレイン。

**Identity block:** 参照画像の女性と同一人物（同じ顔、同じ髪型、同じ服装）：32歳の成熟した大人の女性、大人びた面長の顔立ち、シャープな顎のライン、切れ長の目、長身で長い首と長い脚。艶のある黒髪のぱっつんボブ、前髪にクレイオレンジのメッシュが一筋だけ、八芒星のヘアクリップ、細いヘッドセットマイク。パフスリーブの白いシャツ、膝上丈の黒いプリーツスカート、黒革のサスペンダー、肘上までの黒革のオペラグローブ、黒いタイツ、膝丈の黒革ブーツ。

| # | Variation | Aspect | mediaId |
|---|---|---|---|
| 01-06 | close-ups: front on the bridge; 3/4 smile at sunset; profile in magenta neon; eyes extreme close-up; singing, eyes closed; looking up at stars | 3:4, 16:9 (04) | in `media/images/dataset-1/` file names |
| 07-14 | over-shoulder in a corridor; laughing on a street; typing at a terminal; arms crossed on the bridge; hand to the mic; at the railing by a viewport; walking down a corridor; reading a tablet in a lab | mixed | |
| 15-22 | under the sakura at night; rainy neon street; turning toward camera, battle outside; hangar with mechs; full body front on grey; walking on beige; full body on the bridge; seated in the captain's chair | mixed | |
| 23-30 | back view at a window over Earth; running, side view; pointing at a hologram; high angle at a console; red emergency light; park in daylight; profile at a morning window; code light on her face | mixed | |

File names carry the number and the ISEKAI ZERO mediaId (`dNN-<mediaId>.jpg`). Review sheets: `images/dataset-1-sheet-1..3.jpg`
(labels D01-D30). Spent: 30 × 6.63 = 198.9 credits, plus 12.48 for the turnaround and expression sheets.

Kiln's first pass (adult read first, then design; Lati decides):
- Reads young or off: D06 (wide-eyed wonder), D08 (laughing), D26 (high angle), D28 (park; no orange streak visible).
- Design errors: D04 (two star clips, one each side).
- Framing to leave out of training: D22 (seated, the camera at knee height puts her legs at the centre).
- Fine but note for captions: D10 (crew in the background), D16 (crowd), D15 and D21 (she's small in frame).

**Lati's picks, 7 Nov:** "Good: D03 D06 D09 D10 D11 D13 D14 D15 D16 D18 D20 D22 D25 D26 D27 D29 D30" (17). Copied to
`media/lora/claudia-80s/images/`. By framing: close-ups 5 (D03, D06, D27, D29, D30), medium 8 (D09, D10, D11, D14, D16,
D18, D25, D26), full length 4 (D13, D15, D20, D22). Not in the set: a straight front close-up, a back view, a smile.
