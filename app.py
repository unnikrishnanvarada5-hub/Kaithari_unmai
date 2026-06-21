"""
Kaithari Unmai (கைத்தறி உண்மை) -- "Handloom Truth"
A pattern-conformity verification atlas for India's handloom weaving
traditions. Upload a photo of a saree/handloom textile; the app compares
its woven-pattern fingerprint against a curated reference atlas and shows
how closely it conforms to verified regional weaves -- with the honesty
that this is a conformity signal, not a legal fraud determination.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).parent))
from model.embedder import embed_image, load_reference_db, match_against_db, confidence_label
from model.region_info import REGION_INFO
from model.heritage_narrator import generate_heritage_note

TEMPLE_TILE_B64 = "PHN2ZyB3aWR0aD0iNDQiIGhlaWdodD0iMjgiIHZpZXdCb3g9IjAgMCA0NCAyOCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cGF0aCBkPSJNMiAyNiBMMTEgOCBMMjAgMjYiIGZpbGw9Im5vbmUiIHN0cm9rZT0iI0M5QTIyNyIgc3Ryb2tlLXdpZHRoPSIxLjYiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgogIDxjaXJjbGUgY3g9IjMyIiBjeT0iMjAiIHI9IjIuNiIgZmlsbD0iI0M5QTIyNyIvPgogIDxwYXRoIGQ9Ik0yNCAyNiBMMjQgMjYiIHN0cm9rZT0ibm9uZSIvPgo8L3N2Zz4K"

st.set_page_config(
    page_title="Kaithari Unmai | கைத்தறி உண்மை",
    page_icon="\U0001FAA1",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------------------------------
# Design tokens & CSS
# ----------------------------------------------------------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Work+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {{
    --ink: #2B0A1F;
    --ink-deep: #1C0614;
    --panel: #3A1228;
    --ivory: #F7EFE1;
    --gold: #C9A227;
    --gold-soft: #E3C56B;
    --peacock: #1B6E59;
    --vermilion: #B3402F;
    --text-ivory: #F2E8D8;
    --text-muted: #C9B79F;
}}

html, body, [class*="css"] {{
    font-family: 'Work Sans', sans-serif;
}}

.stApp {{
    background: radial-gradient(ellipse at top, var(--panel) 0%, var(--ink) 55%, var(--ink-deep) 100%);
    color: var(--text-ivory);
}}

#MainMenu, header, footer {{ visibility: hidden; }}

.temple-border {{
    height: 22px;
    width: 100%;
    background-image: url('data:image/svg+xml;base64,{TEMPLE_TILE_B64}');
    background-repeat: repeat-x;
    background-size: 44px 22px;
    opacity: 0.85;
    margin: 0.4rem 0;
}}

.kw-hero {{
    text-align: center;
    padding: 1.2rem 0 0.4rem 0;
}}
.kw-tamil {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.1rem;
    font-weight: 600;
    color: var(--gold-soft);
    letter-spacing: 0.02em;
    margin-bottom: -0.3rem;
}}
.kw-eng {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.55rem;
    font-weight: 500;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: var(--text-ivory);
}}
.kw-tagline {{
    font-family: 'Work Sans', sans-serif;
    font-size: 0.95rem;
    color: var(--text-muted);
    letter-spacing: 0.02em;
    margin-top: 0.3rem;
}}

.kw-card {{
    background: linear-gradient(160deg, rgba(247,239,225,0.06), rgba(247,239,225,0.02));
    border: 1px solid rgba(201,162,39,0.35);
    border-radius: 6px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1rem;
}}

.kw-seal-wrap {{
    display: flex;
    align-items: center;
    gap: 1.6rem;
}}
.kw-seal {{
    width: 116px;
    height: 116px;
    min-width: 116px;
    border-radius: 50%;
    border: 2.5px solid var(--gold);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    background: radial-gradient(circle, rgba(201,162,39,0.12), transparent 70%);
    position: relative;
}}
.kw-seal::before {{
    content: "";
    position: absolute;
    inset: 8px;
    border: 1px dashed rgba(201,162,39,0.55);
    border-radius: 50%;
}}
.kw-seal-pct {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.6rem;
    font-weight: 500;
    color: var(--gold-soft);
}}
.kw-seal-label {{
    font-family: 'Work Sans', sans-serif;
    font-size: 0.62rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--text-muted);
    margin-top: 0.1rem;
}}

.kw-region-name {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 2rem;
    color: var(--ivory);
    font-weight: 600;
    margin-bottom: -0.2rem;
}}
.kw-region-tamil {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.15rem;
    color: var(--gold-soft);
}}
.kw-meta-row {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: var(--text-muted);
    margin-top: 0.5rem;
}}
.kw-confidence-tag {{
    display: inline-block;
    font-family: 'Work Sans', sans-serif;
    font-size: 0.75rem;
    letter-spacing: 0.05em;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    margin-top: 0.6rem;
}}
.tag-high {{ background: rgba(27,110,89,0.25); color: #6fd6b8; border: 1px solid #1B6E59; }}
.tag-mod {{ background: rgba(201,162,39,0.2); color: var(--gold-soft); border: 1px solid var(--gold); }}
.tag-low {{ background: rgba(179,64,47,0.2); color: #e08f7d; border: 1px solid var(--vermilion); }}

.kw-bar-row {{
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin: 0.55rem 0;
}}
.kw-bar-name {{
    width: 150px;
    font-size: 0.82rem;
    color: var(--text-ivory);
    flex-shrink: 0;
}}
.kw-bar-track {{
    flex-grow: 1;
    height: 8px;
    background: rgba(247,239,225,0.1);
    border-radius: 4px;
    overflow: hidden;
}}
.kw-bar-fill {{
    height: 100%;
    background: linear-gradient(90deg, var(--peacock), var(--gold));
    border-radius: 4px;
}}
.kw-bar-pct {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: var(--text-muted);
    width: 48px;
    text-align: right;
}}

.kw-heritage-note {{
    font-family: 'Work Sans', sans-serif;
    font-size: 0.92rem;
    line-height: 1.6;
    color: var(--text-ivory);
    font-style: italic;
    border-left: 2px solid var(--gold);
    padding-left: 1rem;
    margin-top: 1rem;
}}

.kw-atlas-card {{
    background: linear-gradient(160deg, rgba(247,239,225,0.06), rgba(247,239,225,0.02));
    border: 1px solid rgba(201,162,39,0.3);
    border-radius: 6px;
    padding: 1.3rem 1.4rem;
    height: 100%;
}}
.kw-atlas-name {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.5rem;
    color: var(--gold-soft);
}}
.kw-atlas-state {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}
.kw-atlas-gi {{
    display: inline-block;
    font-size: 0.7rem;
    color: var(--peacock);
    border: 1px solid var(--peacock);
    border-radius: 20px;
    padding: 0.1rem 0.6rem;
    margin: 0.4rem 0;
}}
.kw-atlas-body {{
    font-size: 0.85rem;
    color: var(--text-ivory);
    line-height: 1.5;
}}

.kw-demo-banner {{
    background: rgba(179,64,47,0.15);
    border: 1px solid var(--vermilion);
    border-radius: 6px;
    padding: 0.7rem 1.1rem;
    font-size: 0.85rem;
    color: #e08f7d;
    margin-bottom: 1rem;
}}

.kw-footer {{
    text-align: center;
    color: var(--text-muted);
    font-size: 0.78rem;
    margin-top: 2.5rem;
    letter-spacing: 0.04em;
}}

div[data-testid="stFileUploaderDropzone"] {{
    background: rgba(247,239,225,0.04);
    border: 1.5px dashed rgba(201,162,39,0.45) !important;
    border-radius: 8px;
}}
.stTabs [data-baseweb="tab"] {{
    font-family: 'Work Sans', sans-serif;
    font-size: 0.95rem;
    letter-spacing: 0.03em;
}}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
st.markdown('<div class="temple-border"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="kw-hero">
    <div class="kw-tamil">கைத்தறி உண்மை</div>
    <div class="kw-eng">Kaithari&nbsp;Unmai</div>
    <div class="kw-tagline">A pattern-conformity atlas for India's handloom weaving traditions</div>
</div>
""", unsafe_allow_html=True)
st.markdown('<div class="temple-border"></div>', unsafe_allow_html=True)
st.write("")

# ----------------------------------------------------------------------------
# Ensure a reference DB exists (demo fallback on very first run)
# ----------------------------------------------------------------------------
db = load_reference_db()
is_demo = False
if not db:
    from scripts.generate_demo_db import build as build_demo_db
    build_demo_db()
    db = load_reference_db()

is_demo = any(payload.get("meta", {}).get("demo") for payload in db.values())

tab_verify, tab_atlas, tab_about = st.tabs(["Verify a Weave", "Heritage Atlas", "About the Method"])

# ----------------------------------------------------------------------------
# TAB: Verify
# ----------------------------------------------------------------------------
with tab_verify:
    if is_demo:
        st.markdown(
            '<div class="kw-demo-banner">'
            'Demo Mode &mdash; this atlas is currently using synthetic reference vectors. '
            'Run <code>scripts/build_reference_db.py</code> with real verified weave photos '
            'to replace it with genuine results.'
            '</div>',
            unsafe_allow_html=True,
        )

    col_upload, col_result = st.columns([1, 1.3], gap="large")

    with col_upload:
        st.markdown("##### Upload a close-up photo of the weave")
        uploaded = st.file_uploader(
            "Drop a photo here, ideally a close, well-lit shot of the border or motif",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed",
        )
        if uploaded:
            st.image(uploaded, use_container_width=True)

    with col_result:
        if uploaded:
            with st.spinner("Reading the weave's fingerprint..."):
                image_bytes = uploaded.getvalue()
                query_vec = embed_image(image_bytes)
                results, best = match_against_db(query_vec, db, k=5)

            if best:
                region_key, score, n_refs = best
                info = REGION_INFO.get(region_key, {})
                label = confidence_label(score)
                tag_class = "tag-high" if "High" in label else ("tag-mod" if "Moderate" in label else "tag-low")
                pct = max(0, min(100, round((score + 1) / 2 * 100)))  # cosine [-1,1] -> [0,100]

                st.markdown(f"""
                <div class="kw-card">
                    <div class="kw-seal-wrap">
                        <div class="kw-seal">
                            <div class="kw-seal-pct">{pct}%</div>
                            <div class="kw-seal-label">conformity</div>
                        </div>
                        <div>
                            <div class="kw-region-name">{info.get('display_name', region_key.title())}</div>
                            <div class="kw-region-tamil">{info.get('tamil_name', '')}</div>
                            <div class="kw-meta-row">{info.get('state', '')} &middot; {info.get('gi_status', '')}</div>
                            <span class="kw-confidence-tag {tag_class}">{label}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                note = generate_heritage_note(
                    info.get("display_name", region_key), info.get("state", ""), info.get("signature_motif", "")
                )
                if not note:
                    note = info.get("fallback_note", "")
                st.markdown(f'<div class="kw-heritage-note">{note}</div>', unsafe_allow_html=True)

                st.write("")
                st.markdown("###### Conformity across the full atlas")
                bars_html = ""
                for r_key, r_score, r_n in results:
                    r_info = REGION_INFO.get(r_key, {})
                    r_pct = max(0, min(100, round((r_score + 1) / 2 * 100)))
                    bars_html += f"""
                    <div class="kw-bar-row">
                        <div class="kw-bar-name">{r_info.get('display_name', r_key.title())}</div>
                        <div class="kw-bar-track"><div class="kw-bar-fill" style="width:{r_pct}%"></div></div>
                        <div class="kw-bar-pct">{r_pct}%</div>
                    </div>
                    """
                st.markdown(bars_html, unsafe_allow_html=True)
            else:
                st.warning("No reference data available to compare against yet.")
        else:
            st.markdown("""
            <div class="kw-card" style="text-align:center; padding: 3rem 1.6rem;">
                <div style="font-size:0.95rem; color:var(--text-muted);">
                    Your result will appear here as a verification certificate &mdash;
                    a conformity score, the closest-matching weave tradition, and how it
                    compares across the whole atlas.
                </div>
            </div>
            """, unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# TAB: Heritage Atlas
# ----------------------------------------------------------------------------
with tab_atlas:
    st.write("")
    cols = st.columns(3, gap="medium")
    for i, (key, info) in enumerate(REGION_INFO.items()):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="kw-atlas-card">
                <div class="kw-atlas-name">{info['display_name']}</div>
                <div class="kw-atlas-state">{info['tamil_name']} &middot; {info['state']}</div>
                <div class="kw-atlas-gi">{info['gi_status']}</div>
                <div class="kw-atlas-body">{info['fallback_note']}</div>
            </div>
            <div style="height:1rem;"></div>
            """, unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# TAB: About
# ----------------------------------------------------------------------------
with tab_about:
    st.write("")
    st.markdown("""
    <div class="kw-card">
    <h4 style="color:var(--gold-soft); font-family:'Cormorant Garamond',serif;">What this actually measures</h4>
    <p style="color:var(--text-ivory); line-height:1.7; font-size:0.95rem;">
    Kaithari Unmai does not run a "real vs. fake" fraud classifier &mdash; no honest,
    legally verified public dataset of counterfeit handloom photographs exists for
    a model to learn from. Building one would also require sourcing confirmed
    fakes from sellers, which isn't something we'll do.
    </p>
    <p style="color:var(--text-ivory); line-height:1.7; font-size:0.95rem;">
    Instead, the app extracts a 512-dimension visual fingerprint from your photo
    using a pretrained ResNet18, and measures how closely that fingerprint sits to
    a small reference cluster of verified, region-specific weaves &mdash; a
    similarity / few-shot retrieval approach. A high conformity score means the
    photo's woven pattern closely resembles confirmed examples of that tradition.
    A low score is a signal to look closer, ask the seller for provenance, or check
    for the official GI tag &mdash; not a legal verdict.
    </p>
    <p style="color:var(--text-ivory); line-height:1.7; font-size:0.95rem;">
    The reference atlas is intentionally small and meant to grow: weaver
    cooperatives and GI registries are the right long-term source of verified
    images, not random internet photos.
    </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="temple-border"></div>', unsafe_allow_html=True)
st.markdown('<div class="kw-footer">Kaithari Unmai &middot; built in support of India\'s handloom weavers</div>', unsafe_allow_html=True)
