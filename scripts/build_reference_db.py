"""
Build the reference embedding database from verified handloom photos.

Usage:
    1. Collect 15-30 verified, well-lit, close-up photos per weave tradition
       (ideally photographed/sourced directly from weaver cooperatives, GI
       registry listings, or your own verified purchases -- not random
       internet thumbnails, since image quality directly affects accuracy).
    2. Drop them into data/raw/<region_name>/*.jpg
       e.g. data/raw/kanjivaram/*.jpg, data/raw/pochampally_ikat/*.jpg
    3. Run:  python scripts/build_reference_db.py
    4. model/reference_db.pkl is created/updated. Commit this file to your
       repo (it's small -- a few hundred KB) so the deployed app has it.
"""

import sys
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).parent.parent))
from model.embedder import embed_image, save_reference_db  # noqa: E402

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
VALID_EXT = {".jpg", ".jpeg", ".png", ".webp"}


def build():
    if not RAW_DIR.exists():
        print(f"No data found at {RAW_DIR}. Create region subfolders first.")
        return

    db = {}
    for region_dir in sorted(RAW_DIR.iterdir()):
        if not region_dir.is_dir():
            continue

        images = [p for p in region_dir.iterdir() if p.suffix.lower() in VALID_EXT]
        if not images:
            print(f"  skip '{region_dir.name}' (no images)")
            continue

        print(f"  embedding {len(images)} images for '{region_dir.name}'...")
        vectors = []
        for img_path in images:
            try:
                vectors.append(embed_image(img_path))
            except Exception as e:
                print(f"    failed on {img_path.name}: {e}")

        if vectors:
            db[region_dir.name] = {
                "vectors": np.stack(vectors),
                "meta": {"n_refs": len(vectors)},
            }

    if not db:
        print("No valid region folders with images were found. Nothing built.")
        return

    save_reference_db(db)
    total = sum(v["meta"]["n_refs"] for v in db.values())
    print(f"\nDone. Reference DB built: {len(db)} regions, {total} reference photos.")
    print("Saved to model/reference_db.pkl -- commit this file to git.")


if __name__ == "__main__":
    build()
