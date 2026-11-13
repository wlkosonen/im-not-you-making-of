# Plates v2 · round 5 · iteration (Lati's notes on rounds 1-4)

9 Nov 2026 · run by a helper for Claude (Kiln, local) · Lati's go: "core plus optional"

Spec: `plates-v2-rounds.json`, round "5 · iteration (Lati's notes on rounds 1-4)", all ten shots including the three
marked optional (s080, s092, s107). Model 6a50079fc28ed5bfe5576f54, 16:9, edit_image with each shot's refs (in the
given order) and prompt exactly as written. Files: `media/plates/v2/<shot>-<k>-<mediaId>.jpg`, with k continuing after
the takes already in that folder. Sheet: `plates-v2-round-5-sheet.jpg` (spec shot order, 4 columns; each cell's
caption shows its sheet label and the file name, which starts with `<shot>-<k>`).

## Credits

- Charged: **209.82** (sum of costCredits over all 30 jobs) against the round's est **209.82** (core 168.48 +
  optional 41.34). Per image: 8.19 with six refs, 6.63 with two, 6.24 with one.
- Balance at the end (get_balance): **2007.31** (2217.13 before this round; the difference is 209.82).

## Failures

None. All 30 jobs completed on the first try; nothing was rerun.

## Images

The last column is the mean absolute pixel difference against each reference image at 128x72 (0-255). Under ~15
means a near-copy. The references were read from their local copies under `media/images/` (same mediaIds). None is
under 15 this round; the closest is s033-8 at 40.5 against R·F6·4·1.

| Label | Sheet | mediaId | Status | Credits | Mean diff vs refs (0-255) |
|---|---|---|---|---|---|
| s033-5 | R1·1 | 6af2053c813fa29c9697cf98 | completed | 8.19 | S1·1:114.8 S1·2:110.8 S2·1:97.7 S3·1:121.7 S3·2:121.6 R·F6·4·1:44.7 |
| s033-6 | R1·2 | 6af20564c02b732b4ddc2c15 | completed | 8.19 | S1·1:116.9 S1·2:111.7 S2·1:97.8 S3·1:121.8 S3·2:120.3 R·F6·4·1:41.5 |
| s033-7 | R1·3 | 6af205665c0f2a0eaa63eece | completed | 8.19 | S1·1:116.3 S1·2:110.1 S2·1:98.9 S3·1:124.7 S3·2:122.6 R·F6·4·1:42.0 |
| s033-8 | R1·4 | 6af20568c7a8a80012b769fe | completed | 8.19 | S1·1:117.5 S1·2:111.3 S2·1:96.8 S3·1:124.7 S3·2:121.9 R·F6·4·1:40.5 |
| s036-3 | R2·1 | 6af2056903aee40cefc95d43 | completed | 6.63 | M2·A·1:105.4 S1·1:101.3 |
| s036-4 | R2·2 | 6af2056b8f223af9194b4c89 | completed | 6.63 | M2·A·1:110.3 S1·1:104.8 |
| s036-5 | R2·3 | 6af2056cc0556c901db956cf | completed | 6.63 | M2·A·1:95.7 S1·1:93.4 |
| s036-6 | R2·4 | 6af2056d6561fec160c2a4df | completed | 6.63 | M2·A·1:103.8 S1·1:99.7 |
| s056-3 | R3·1 | 6af2056f980a783a4e9bdd82 | completed | 6.24 | M1·A·1:105.0 |
| s056-4 | R3·2 | 6af20570f8e1d1a541103b2f | completed | 6.24 | M1·A·1:105.6 |
| s087-3 | R3·3 | 6af2059a882ea414a26c5fc8 | completed | 6.63 | M3·C·1:99.8 S1·2:97.8 |
| s087-4 | R3·4 | 6af2059b113363c9992571d9 | completed | 6.63 | M3·C·1:101.8 S1·2:101.8 |
| s087-5 | R4·1 | 6af2059dc7a8a80012b7924c | completed | 6.63 | M3·C·1:99.7 S1·2:97.8 |
| s087-6 | R4·2 | 6af2059ef8e1d1a541105a02 | completed | 6.63 | M3·C·1:88.7 S1·2:84.0 |
| s094-5 | R4·3 | 6af2059fc7a8a80012b79415 | completed | 8.19 | S1·1:113.3 S1·2:107.7 S2·1:96.0 S3·1:120.1 S3·2:118.0 R·H·2·1:50.0 |
| s094-6 | R4·4 | 6af205a12fd3a11d57004378 | completed | 8.19 | S1·1:108.6 S1·2:104.0 S2·1:94.5 S3·1:115.9 S3·2:115.4 R·H·2·1:54.2 |
| s094-7 | R5·1 | 6af205a25ddbc7f45c732de6 | completed | 8.19 | S1·1:111.4 S1·2:105.5 S2·1:95.5 S3·1:118.2 S3·2:116.7 R·H·2·1:51.1 |
| s094-8 | R5·2 | 6af205a42fd3a11d570046fb | completed | 8.19 | S1·1:108.8 S1·2:103.3 S2·1:95.3 S3·1:115.4 S3·2:116.3 R·H·2·1:50.6 |
| s101-3 | R5·3 | 6af205bd031eda9ce3417e8d | completed | 6.24 | SI·1:74.0 |
| s101-4 | R5·4 | 6af205be882ea414a26c7afc | completed | 6.24 | SI·1:76.3 |
| s101-5 | R6·1 | 6af205c0e7cb0a7f2f938ceb | completed | 6.24 | SI·1:75.1 |
| s101-6 | R6·2 | 6af205c1e7cb0a7f2f938d60 | completed | 6.24 | SI·1:80.8 |
| s102-3 | R6·3 | 6af205c3f8f4544bfcef7be2 | completed | 6.24 | SI·1:69.7 |
| s102-4 | R6·4 | 6af205c5b1f22843f2263ebf | completed | 6.24 | SI·1:66.1 |
| s080-2 | R7·1 | 6af205e26561fec160c30825 | completed | 6.24 | M3·C·1:84.4 |
| s080-3 | R7·2 | 6af205e31aeccf1839d985fb | completed | 6.24 | M3·C·1:83.2 |
| s092-3 | R7·3 | 6af205e44004dbc5ab8164b0 | completed | 6.24 | P3·B·2:61.3 |
| s092-4 | R7·4 | 6af205e60aa9ce1245b15735 | completed | 6.24 | P3·B·2:60.7 |
| s107-5 | R8·1 | 6af205e7f8f4544bfcef98eb | completed | 8.19 | S1·1:109.3 S1·2:102.5 S2·1:93.2 S3·1:114.1 S3·2:114.2 R·F6·4·1:51.0 |
| s107-6 | R8·2 | 6af205e9c7a8a80012b7c708 | completed | 8.19 | S1·1:112.6 S1·2:108.3 S2·1:95.9 S3·1:120.3 S3·2:118.5 R·F6·4·1:47.1 |
