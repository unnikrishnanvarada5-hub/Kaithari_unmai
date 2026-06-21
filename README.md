# Kaithari Unmai (கைத்தறி உண்மை) — Handloom Truth

A pattern-conformity verification atlas for India's handloom weaving traditions.
Upload a photo of a saree or handloom textile. The app extracts a 512-dim
visual fingerprint (pretrained ResNet18) and compares it against a curated
reference atlas of verified regional weaves — Kanjivaram, Banarasi, Pochampally
Ikat, Chanderi, Sambalpuri, Bandhani — returning a conformity score, the
closest-matching tradition, and a heritage note.

This is a similarity / few-shot retrieval system, not a fraud classifier — see
the "About the Method" tab in the app for why, and why that's the technically
honest choice given the data that actually exists.

## What's inside

```
kaithari-unmai/
├── app.py                          # Streamlit app (entry point)
├── model/
│   ├── embedder.py                 # ResNet18 feature extraction + matching
│   ├── region_info.py              # Heritage metadata per weave tradition
│   ├── heritage_narrator.py        # Optional Groq-powered heritage notes
│   └── reference_db.pkl            # Generated — embeddings DB (created by you)
├── scripts/
│   ├── build_reference_db.py       # Builds the REAL reference DB from your photos
│   └── generate_demo_db.py         # Builds a synthetic demo DB (auto-runs on first launch)
├── data/raw/<region>/              # Drop your reference photos here
├── requirements.txt
└── .streamlit/config.toml          # Theme
```

## Run it locally

Step 1. Clone your repo and enter it:
```
git clone https://github.com/YOUR_USERNAME/kaithari-unmai.git
cd kaithari-unmai
```

Step 2. Create a virtual environment and install dependencies:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Step 3. Run the app:
```
streamlit run app.py
```

Step 4. Open the URL shown in the terminal (usually http://localhost:8501).

On first launch, the app auto-generates a synthetic "Demo Mode" reference
database so the UI is fully interactive immediately. A banner tells you this
clearly. Replace it with real data in the next section.

## Building the real reference database

The conformity score is only as good as the verified photos you feed it.

Step 1. For each weave tradition, collect 15–30 close-up, well-lit photos of
the border/motif area, ideally sourced from weaver cooperatives, official GI
registry listings, or your own verified purchases — not random web thumbnails.

Step 2. Place them here:
```
data/raw/kanjivaram/photo1.jpg
data/raw/kanjivaram/photo2.jpg
data/raw/banarasi/photo1.jpg
...
```

Step 3. Build the database:
```
python scripts/build_reference_db.py
```

Step 4. Commit the generated `model/reference_db.pkl` to your repo:
```
git add model/reference_db.pkl
git commit -m "Add real reference embeddings"
git push
```

The Demo Mode banner disappears automatically once real data replaces it.

## Adding the optional Groq heritage narration

Step 1. Get a free API key at https://console.groq.com/keys

Step 2. Open `model/heritage_narrator.py` and replace the placeholder:
```
GROQ_API_KEY = "your-groq-api-key-here"
```
with your real key.

Step 3. Save the file. The app will now generate a fresh heritage note per
result instead of using the static fallback text. If the key is missing or
the call fails for any reason, the app silently falls back — nothing breaks.

## Push to GitHub

Step 1. Create a new empty repository on GitHub named `kaithari-unmai`
(don't initialize it with a README — you already have one).

Step 2. From inside the project folder:
```
git init
git add .
git commit -m "Initial commit: Kaithari Unmai"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/kaithari-unmai.git
git push -u origin main
```

## Deploy on Streamlit Community Cloud

Step 1. Go to https://share.streamlit.io and sign in with your GitHub account.

Step 2. Click "New app".

Step 3. Select your `kaithari-unmai` repository, branch `main`, and main file
path `app.py`.

Step 4. Click "Deploy". The first build takes a few minutes — it needs to
download PyTorch and the pretrained ResNet18 weights.

Step 5. Once live, your app URL will look like:
```
https://YOUR_USERNAME-kaithari-unmai.streamlit.app
```

That's it — no servers to manage, no Docker, nothing else to configure.

## Why a similarity approach instead of a classifier

A real fake-vs-authentic classifier needs confirmed labeled examples of
counterfeits, which would mean sourcing actual fraudulent listings to train
on — not something to build casually, and not something a public dataset
honestly provides at scale for Indian handloom textiles. Measuring
conformity to verified references is the technique that's actually
supportable with real, ethically-sourced data, and it's still useful: a low
score is a legitimate signal to ask for provenance or check the GI tag
yourself.
