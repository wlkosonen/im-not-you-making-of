#!/usr/bin/env python3
"""Look test for her LoRA's base model: the same prompts on Illustrious-XL v2.0 and Anima, no LoRA, local ComfyUI.

    ~/workshop/bin/comfy start --out "media/images/looktest-2"
    python3 production/tools/looktest.py production/lora/looktest-2.json [--seeds 2] [--only illu,anima-aes]

The JSON holds {"negative": {...}, "shots": [{"id", "w", "h", "illu", "anima"}]}: one tag prompt for Illustrious and
one tag-plus-sentences prompt for Anima per shot. Images land in ComfyUI's output directory as
<model>_<shot>_s<seed>_00001_.png; each render is logged to production/images/renders.jsonl. Settings follow the model
cards: Illustrious euler_a 28 steps CFG 5.5; Anima er_sde 32 steps CFG 4.5 (card: 30-50 steps, CFG 4-5).
"""

import argparse
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
URL = "http://127.0.0.1:8188"
LOG = ROOT / "production/images/renders.jsonl"

MODELS = {
    "illu": {"kind": "sdxl", "ckpt": "Illustrious-XL-v2.0.safetensors"},
    "anima-aes": {"kind": "anima", "unet": "anima-aesthetic-v1.1.safetensors"},
    "anima-base": {"kind": "anima", "unet": "anima-base-v1.0.safetensors"},
}


def graph(m, pos, neg, w, h, seed, prefix):
    if m["kind"] == "sdxl":
        g = {
            "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": m["ckpt"]}},
            "4": {"class_type": "CLIPTextEncode", "inputs": {"text": pos, "clip": ["1", 1]}},
            "5": {"class_type": "CLIPTextEncode", "inputs": {"text": neg, "clip": ["1", 1]}},
            "6": {"class_type": "EmptyLatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}},
            "7": {"class_type": "KSampler", "inputs": {"model": ["1", 0], "positive": ["4", 0], "negative": ["5", 0],
                                                       "latent_image": ["6", 0], "seed": seed, "steps": 28, "cfg": 5.5,
                                                       "sampler_name": "euler_ancestral", "scheduler": "normal",
                                                       "denoise": 1.0}},
            "8": {"class_type": "VAEDecode", "inputs": {"samples": ["7", 0], "vae": ["1", 2]}},
        }
    else:
        g = {
            "1": {"class_type": "UNETLoader", "inputs": {"unet_name": m["unet"], "weight_dtype": "default"}},
            "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen_3_06b_base.safetensors",
                                                         "type": "stable_diffusion", "device": "default"}},
            "3": {"class_type": "VAELoader", "inputs": {"vae_name": "qwen_image_vae.safetensors"}},
            "4": {"class_type": "CLIPTextEncode", "inputs": {"text": pos, "clip": ["2", 0]}},
            "5": {"class_type": "CLIPTextEncode", "inputs": {"text": neg, "clip": ["2", 0]}},
            "6": {"class_type": "EmptySD3LatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}},
            "7": {"class_type": "KSampler", "inputs": {"model": ["1", 0], "positive": ["4", 0], "negative": ["5", 0],
                                                       "latent_image": ["6", 0], "seed": seed, "steps": 32, "cfg": 4.5,
                                                       "sampler_name": "er_sde", "scheduler": "simple", "denoise": 1.0}},
            "8": {"class_type": "VAEDecode", "inputs": {"samples": ["7", 0], "vae": ["3", 0]}},
        }
    g["9"] = {"class_type": "SaveImage", "inputs": {"images": ["8", 0], "filename_prefix": prefix}}
    return g


def post(path, body):
    req = urllib.request.Request(URL + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    body = urllib.request.urlopen(req).read()
    return json.loads(body) if body.strip() else {}


def get(path):
    return json.load(urllib.request.urlopen(URL + path))


def render(name, shot, neg, seed):
    m = MODELS[name]
    pos = shot["illu"] if m["kind"] == "sdxl" else shot["anima"]
    prefix = f"{name}_{shot['id']}_s{seed}"
    t0 = time.time()
    pid = post("/prompt", {"prompt": graph(m, pos, neg[m["kind"]], shot["w"], shot["h"], seed, prefix)})["prompt_id"]
    while True:
        h = get(f"/history/{pid}")
        if pid in h:
            st = h[pid].get("status", {})
            if st.get("status_str") == "error":
                raise SystemExit(f"{prefix}: ComfyUI error: {st}")
            if st.get("completed"):
                break
        time.sleep(2)
    dt = round(time.time() - t0, 1)
    with open(LOG, "a") as f:
        f.write(json.dumps({"id": prefix, "model": name, "prompt": pos, "negative": neg[m["kind"]], "seed": seed,
                            "w": shot["w"], "h": shot["h"], "seconds": dt, "film": "looktest-2"},
                           ensure_ascii=False) + "\n")
    print(prefix, dt, "s", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--first", type=int, default=1, help="first seed index (seed = 1000 + index)")
    ap.add_argument("--only", default=",".join(MODELS))
    a = ap.parse_args()
    spec = json.loads(Path(a.spec).read_text())
    # one model at a time, so each loads once
    for name in a.only.split(","):
        for shot in spec["shots"]:
            for seed in range(a.first, a.first + a.seeds):
                render(name, shot, spec["negative"], 1000 + seed)


if __name__ == "__main__":
    main()
