"""Static heritage metadata for each weave tradition in the reference atlas.
Used both for display copy and as an offline fallback when no Groq API call
is made (or it fails), so the app never shows a broken/empty result.
"""

REGION_INFO = {
    "kanjivaram": {
        "display_name": "Kanjivaram",
        "tamil_name": "காஞ்சீவரம்",
        "state": "Tamil Nadu",
        "gi_status": "GI Registered (2005)",
        "signature_motif": "Korvai border join, temple (gopuram) and rudraksha motifs, contrast pallu",
        "fallback_note": (
            "Woven in Kanchipuram using the korvai technique, where the body and "
            "border are woven separately and interlocked on the loom -- a join "
            "strong enough that the border won't tear away from the body even "
            "after years of wear. Pure mulberry silk and real zari are traditional "
            "markers of authenticity."
        ),
    },
    "banarasi": {
        "display_name": "Banarasi",
        "tamil_name": "பனாரசி",
        "state": "Uttar Pradesh",
        "gi_status": "GI Registered (2009)",
        "signature_motif": "Mughal-influenced brocade, intricate zari buti and jaal patterns",
        "fallback_note": (
            "Woven in Varanasi on handlooms using a brocade technique descended "
            "from Mughal court weaving traditions, recognisable by dense floral "
            "buti work and fine gold or silver zari thread running through the weave."
        ),
    },
    "pochampally_ikat": {
        "display_name": "Pochampally Ikat",
        "tamil_name": "போச்சம்பள்ளி இகத்",
        "state": "Telangana",
        "gi_status": "GI Registered (2004)",
        "signature_motif": "Diamond and geometric tie-dye patterns, double ikat technique",
        "fallback_note": (
            "The yarn itself is tie-dyed in a precise sequence before it ever "
            "reaches the loom, so the geometric diamond pattern is built into the "
            "thread, not printed afterward. A soft, slightly blurred edge on the "
            "motif boundary is a sign of genuine hand ikat."
        ),
    },
    "chanderi": {
        "display_name": "Chanderi",
        "tamil_name": "சந்தேரி",
        "state": "Madhya Pradesh",
        "gi_status": "GI Registered (2005)",
        "signature_motif": "Sheer, lightweight weave with delicate gold coin and floral butis",
        "fallback_note": (
            "Woven from a silk-cotton blend that gives the fabric its characteristic "
            "translucent, lightweight feel -- a quality that's very difficult to "
            "replicate in mass-produced synthetic copies."
        ),
    },
    "sambalpuri": {
        "display_name": "Sambalpuri",
        "tamil_name": "சாம்பல்பூரி",
        "state": "Odisha",
        "gi_status": "GI Registered (2005)",
        "signature_motif": "Bandha tie-dye ikat, shankha (conch), chakra and phula (flower) motifs",
        "fallback_note": (
            "Recognisable by traditional Bandha ikat motifs -- shankha, chakra, "
            "and phula -- tie-dyed into the yarn before weaving, giving every "
            "genuine piece naturally occurring small irregularities that a "
            "printed imitation won't have."
        ),
    },
    "bandhani": {
        "display_name": "Bandhani",
        "tamil_name": "பந்தனி",
        "state": "Gujarat & Rajasthan",
        "gi_status": "GI Registered (2016)",
        "signature_motif": "Fine tie-and-dye dots forming bandhej patterns",
        "fallback_note": (
            "Made by pinching and tying thousands of tiny points across the fabric "
            "before dyeing, leaving each released dot with a faint, organic ring -- "
            "machine-printed fakes show perfectly uniform, flat dots instead."
        ),
    },
}
