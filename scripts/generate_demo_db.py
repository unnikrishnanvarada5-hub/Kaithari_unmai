"""
Generates a SYNTHETIC demo reference database so the app is fully
interactive the moment you clone it -- before you've gathered real
verified weave photographs. The app clearly labels results as
"Demo Mode" whenever this synthetic DB is in use, and the banner
disappears automatically once you run build_reference_db.py with
real photos (which overwrites this file).

Run:  python scripts/generate_demo_db.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).parent.parent))
from model.embedder import save_reference_db  # noqa: E402

REGIONS = [
    "kanjivaram",
    "banarasi",
    "pochampally_ikat",
    "chanderi",
    "sambalpuri",
    "bandhani",
]

RNG = np.random.default_rng(seed=42)


def random_unit_vectors(centroid: np.ndarray, n: int, spread: float = 0.15):
    vecs = centroid + RNG.normal(scale=spread, size=(n, len(centroid)))
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    return vecs / norms


def build():
    db = {}
    for region in REGIONS:
        centroid = RNG.normal(size=512)
        centroid /= np.linalg.norm(centroid)
        vectors = random_unit_vectors(centroid, n=12)
        db[region] = {
            "vectors": vectors,
            "meta": {"n_refs": len(vectors), "demo": True},
        }

    save_reference_db(db)
    print(f"Demo DB created with {len(REGIONS)} synthetic regions.")
    print("Replace it any time by running scripts/build_reference_db.py with real photos.")


if __name__ == "__main__":
    build()
