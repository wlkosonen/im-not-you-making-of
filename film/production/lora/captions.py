#!/usr/bin/env python3
"""Captions for her 80s LoRA (Illustrious-type SDXL): Danbooru tags, written by Kiln from the images, 7 Nov 2026.

What every image shares and should become `clxudia80s` is left untagged: the face, the black blunt bob with bangs,
the single orange streak, the star hair clip, the headset mic. What should stay promptable is tagged: framing, view,
gaze, expression, pose, outfit pieces, setting, light. Writes one .txt per image beside it and captions.jsonl here.

    python3 production/lora/captions.py
"""
import glob, json, os

TRIGGER = "clxudia80s, 1girl, solo"
STYLE = "retro artstyle, 1980s (style)"
FULL = "white shirt, puffy short sleeves, suspenders, belt, black skirt, pleated skirt, black gloves, elbow gloves, black pantyhose, black boots, knee boots"
THIGH = "white shirt, puffy short sleeves, suspenders, belt, black skirt, pleated skirt, black gloves, elbow gloves, black pantyhose"
WAIST = "white shirt, puffy short sleeves, suspenders, belt, black skirt, black gloves, elbow gloves"
UPPER = "white shirt, collared shirt, puffy short sleeves, suspenders"

C = {
 "d03": f"portrait, from side, profile, looking to the side, closed mouth, serious, {UPPER}, city, skyscraper, night, neon lights, pink rim light",
 "d06": f"portrait, upper body, looking up, open mouth, awe, {UPPER}, starry sky, space, night",
 "d09": f"cowboy shot, from side, sitting, typing, keyboard, computer, monitor, control room, looking down, closed mouth, {WAIST}, black pantyhose, indoors, screen light",
 "d10": f"cowboy shot, from front, looking at viewer, crossed arms, closed mouth, serious, {WAIST}, bridge, spaceship interior, window, space, spaceship, people in background, indoors",
 "d11": f"cowboy shot, three-quarter view, hand on headset, talking, looking to the side, {THIGH}, control panel, monitor, orange screen light, indoors",
 "d13": f"full body, from front, walking, walking towards viewer, looking at viewer, closed mouth, {FULL}, corridor, spaceship interior, ceiling light, indoors",
 "d14": f"cowboy shot, three-quarter view, holding tablet, looking down, smile, {THIGH}, laboratory, computer, indoors",
 "d15": f"full body, wide shot, standing, looking up, {FULL}, cherry blossoms, falling petals, night, starry sky, outdoors",
 "d16": f"cowboy shot, from front, standing, looking to the side, closed mouth, {THIGH}, city, street, neon lights, rain, wet ground, crowd, night, outdoors",
 "d18": f"cowboy shot, wide shot, standing, looking at viewer, wind, {THIGH}, hangar, mecha, robot, indoors",
 "d20": f"full body, three-quarter view, walking, looking at viewer, closed mouth, {FULL}, id card, simple background, beige background",
 "d22": f"full body, from front, sitting, chair, hands on armrests, looking at viewer, closed mouth, serious, {FULL}, bridge, cockpit, control panel, window, space, starry sky, indoors",
 "d25": f"cowboy shot, three-quarter view, pointing, looking to the side, {THIGH}, hologram, monitor, computer, blue light, indoors",
 "d26": f"cowboy shot, from above, looking up, parted lips, hands on control panel, {THIGH}, control room, monitor, indoors",
 "d27": f"cowboy shot, from front, looking at viewer, closed mouth, serious, {WAIST}, red light, alarm, spaceship interior, indoors",
 "d29": f"upper body, from side, profile, looking afar, closed mouth, {UPPER}, black gloves, window, curtains, sunlight, morning, indoors",
 "d30": f"portrait, from front, looking at viewer, closed mouth, {UPPER}, green light, glowing text, code, light on face, dark background",
 "d31": f"upper body, from front, looking at viewer, closed mouth, expressionless, {UPPER}, belt, black gloves, bridge, monitor, spaceship, indoors",
 "d32": f"portrait, upper body, from front, looking at viewer, open mouth, talking, {UPPER}, bridge, monitor, indoors",
 "d35": f"portrait, upper body, three-quarter view, looking at viewer, open mouth, talking, {UPPER}, bridge, spaceship interior, indoors",
 "d36": f"full body, from front, standing, looking at viewer, closed mouth, serious, {FULL}, red light, rim light, bridge, control panel, window, space, indoors",
 "d37": f"close-up, portrait, from front, looking at viewer, closed mouth, expressionless, {UPPER}, white background, simple background",
 "d38": f"upper body, from front, looking at viewer, closed mouth, {UPPER}, through screen, monitor, crt, green light, scanlines, control room",
 "d39": f"portrait, upper body, from front, looking at viewer, smile, closed mouth, {UPPER}, white background, simple background",
 "d41": f"cowboy shot, three-quarter view, looking to the side, closed mouth, {THIGH}, window, city, flying car, daylight, desk, indoors",
 "d42": f"portrait, upper body, three-quarter view, eyes closed, open mouth, singing, {UPPER}, starry sky, space",
 "d44": f"upper body, three-quarter view, looking at viewer, parted lips, leaning forward, hands on table, {UPPER}, black gloves, hologram, control panel, bridge, indoors",
 "d45": f"portrait, upper body, three-quarter view, looking at viewer, smile, closed mouth, {UPPER}, cherry blossoms, night",
 "d46": f"upper body, three-quarter view, sitting, chair, looking to the side, open mouth, talking, {UPPER}, black gloves, bridge, control panel, window, space, spaceship, indoors",
 "d47": f"portrait, upper body, from side, profile, open mouth, talking, {UPPER}, city, neon lights, night, rain, bokeh",
 "d48": f"cowboy shot, from front, looking at viewer, closed mouth, wind, {THIGH}, id card, observation deck, window, earth (planet), space, indoors",
 "d50": f"upper body, three-quarter view, looking at viewer, closed mouth, {UPPER}, belt, id card, window, space, spaceship, explosion, battle, indoors",
 "d72": f"full body, three-quarter view, walking, walking towards viewer, looking at viewer, closed mouth, {FULL}, corridor, spaceship interior, door, indoors",
 "d74": f"full body, from front, standing, looking up, parted lips, {FULL}, cherry blossoms, tree, falling petals, night, outdoors",
 "d75": f"full body, three-quarter view, standing, looking at viewer, closed mouth, {FULL}, city, street, neon lights, rain, wet ground, night, outdoors",
 "d77": f"full body, three-quarter view, standing, looking at viewer, closed mouth, {FULL}, monitor, many monitors, control room, blue light, indoors",
 "d79": f"full body, three-quarter view, standing, looking at viewer, closed mouth, {FULL}, id card, simple background, grey background",
 "d80": f"full body, from behind, looking back, looking at viewer, closed mouth, {FULL}, simple background, white background",
 "d81": f"full body, three-quarter view, walking, looking ahead, closed mouth, {FULL}, simple background, beige background",
 "d82": f"full body, from below, standing, looking at viewer, closed mouth, {FULL}, city, futuristic city, spire, flying car, blue sky, daylight, outdoors",
 "d84": f"full body, three-quarter view, standing, hand on wall, looking at viewer, closed mouth, {FULL}, airlock, hatch, hazard stripes, indoors",
 "d85": f"full body, from front, standing, legs apart, looking at viewer, serious, {FULL}, id card, electricity, lightning, machinery, dark, indoors",
 "d86": f"full body, from front, standing, looking at viewer, closed mouth, wind, {FULL}, id card, rooftop, city, cityscape, night, city lights, outdoors",
 "d87": f"cowboy shot, three-quarter view, standing, hand on control panel, looking at viewer, closed mouth, {THIGH}, bridge, monitor, control panel, indoors",
 "d88": f"full body, from front, standing, holding tablet, looking down, closed mouth, {FULL}, id card, computer, many monitors, crt, cable, room, indoors",
}

here = os.path.dirname(os.path.abspath(__file__))
imgs = os.path.join(here, "..", "..", "media", "lora", "claudia-80s", "images")
rows = []
for p in sorted(glob.glob(os.path.join(imgs, "*.jpg"))):
    key = os.path.basename(p)[:3]
    cap = f"{TRIGGER}, {C[key]}, {STYLE}"
    open(p[:-4] + ".txt", "w").write(cap + "\n")
    rows.append({"file": os.path.basename(p), "caption": cap})
assert len(rows) == len(C), (len(rows), len(C))
with open(os.path.join(here, "captions.jsonl"), "w") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(len(rows), "captions")
