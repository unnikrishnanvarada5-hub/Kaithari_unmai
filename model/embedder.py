"""
Kaithari Unmai - Embedding Engine
-----------------------------------
Extracts a 512-dim visual fingerprint from a saree/handloom image using a
pretrained ResNet18 (ImageNet weights). We do NOT train a fake-vs-real
classifier -- no honest public dataset of "counterfeit" handloom photos
exists. Instead we measure how closely a photo's woven-pattern fingerprint
sits next to a curated reference cluster of verified, region-specific
weaves (Kanjivaram korvai borders, Pochampally ikat diamonds, etc).

This is a similarity / few-shot retrieval approach (cosine distance in
embedding space + k-NN voting), which is the technically honest way to
solve this problem with the realistically small amount of artisan-verified
reference photos a student project can gather.
"""

import io
import pickle
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms

EMBED_DIM = 512
DB_PATH = Path(__file__).parent / "reference_db.pkl"

_preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

_model = None


def _load_backbone():
    """Lazily load the pretrained ResNet18 with its classification head removed."""
    global _model
    if _model is None:
        net = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
        net.fc = nn.Identity()  # strip the 1000-class head, keep the 512-d feature vector
        net.eval()
        _model = net
    return _model


def embed_image(image_bytes_or_path) -> np.ndarray:
    """Turn a photo into a 512-dim L2-normalized fingerprint vector."""
    if isinstance(image_bytes_or_path, (str, Path)):
        img = Image.open(image_bytes_or_path).convert("RGB")
    else:
        img = Image.open(io.BytesIO(image_bytes_or_path)).convert("RGB")

    tensor = _preprocess(img).unsqueeze(0)
    net = _load_backbone()
    with torch.no_grad():
        vec = net(tensor).squeeze(0).numpy()

    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec


def load_reference_db() -> dict:
    """
    Reference DB shape:
        { region_name: { "vectors": np.ndarray [n,512], "meta": {...} } }
    Returns {} if no DB has been built yet.
    """
    if not DB_PATH.exists():
        return {}
    with open(DB_PATH, "rb") as f:
        return pickle.load(f)


def save_reference_db(db: dict):
    with open(DB_PATH, "wb") as f:
        pickle.dump(db, f)


def match_against_db(query_vec: np.ndarray, db: dict, k: int = 5):
    """
    Returns a ranked list of (region_name, mean_cosine_similarity, n_refs)
    for every region in the DB, plus the single best match.
    """
    if not db:
        return [], None

    results = []
    for region, payload in db.items():
        vectors = payload["vectors"]
        sims = vectors @ query_vec  # cosine sim, vectors already L2-normalized
        top_k = np.sort(sims)[-min(k, len(sims)):]
        results.append((region, float(top_k.mean()), len(vectors)))

    results.sort(key=lambda r: r[1], reverse=True)
    best = results[0] if results else None
    return results, best


def confidence_label(score: float) -> str:
    """Map a raw cosine similarity (-1..1) to a human confidence band."""
    if score >= 0.80:
        return "High conformity"
    if score >= 0.65:
        return "Moderate conformity"
    if score >= 0.50:
        return "Low conformity"
    return "Pattern mismatch"
