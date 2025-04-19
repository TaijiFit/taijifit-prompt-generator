# Streamlit AI Image Prompt Generator with Vibe Presets and Randomizer

import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="🎨 AI Image Prompt Generator", layout="centered")

st.title("🎨 AI Image Prompt Generator")
st.markdown("Choose a Vibe Preset, or click 🎲 to generate random prompt ingredients!")

# --- Vibe Preset List with Visual Grouping ---
vibe_options = [
    "TaijiFit Style",
    "None",
    "--- Retro-Futurism ---",
    "Admen of Tomorrow",
    "Saturday Space Age",
    "--- Atmospheric Worlds ---",
    "Cyberdreams",
    "Mystic Forest",
    "Desert Future",
    "--- Stylized Characters ---",
    "Noir Detective"
]

# --- Dropdown ---
vibe = st.selectbox("Choose a Vibe Preset (optional)", vibe_options)
randomize = st.button("🎲 Randomize Fields")

# --- Preset Definitions ---
def get_preset_values(vibe):
    presets = {
        "TaijiFit Style": {
            "subject_quantity": "a single",
            "subject_adjectives": ["fluid", "empowered", "glowing"],
            "subject_noun": "Tai Chi practitioner",
            "subject_action": "mid-form with one hand extended and eyes focused",
            "env_adjectives": ["serene", "open", "flowing"],
            "env_noun": "natural studio or oceanside setting",
            "env_mood": "with soft glow and grounded presence",
            "medium": "photorealistic",
            "style": "professional photography – natural light, soft bokeh, Hasselblad quality",
            "lighting": "cinematic lighting",
            "color_scheme": "pastel palette with chrome accents",
            "composition": "close-up",
            "quality": ["sharp focus", "hyperreal detail", "soft depth of field"],
            "negative": "blurry, low quality, distorted, flat light",
            "aspect_ratio": "16:9",
            "seed": "",
            "style_strength": 600
        },
        # ... presets dictionary (already defined previously)
    }
    return presets.get(vibe, {})

# --- Helper Function ---
def get_value(key, default=""):
    return preset.get(key) or random_values.get(key) or default

# --- Determine whether to load preset or random values ---
valid_presets = {
    "TaijiFit Style",
    "Admen of Tomorrow",
    "Saturday Space Age",
    "Cyberdreams",
    "Mystic Forest",
    "Desert Future",
    "Noir Detective"
}

if randomize:
    preset = {}
    random_values = get_preset_values(random.choice(list(valid_presets)))
elif vibe in valid_presets:
    preset = get_preset_values(vibe)
    random_values = {}
else:
    preset = {}
    random_values = {}

# --- UI Input Fields ---
subject_quantity = st.selectbox("Quantity", ["a single", "a pair of", "three", "many", "a cartoon"], index=0)
subject_adjectives = st.multiselect("Adjectives (for subject)", ["ethereal", "massive", "elegant", "armored", "floating", "chrome-plated", "stylized", "jet-finned", "bold-lined", "midcentury-styled", "animated", "neon-lit", "glitchy", "holographic", "shadowy", "gritty", "trench-coated", "fluid", "empowered", "glowing"], get_value("subject_adjectives", []))
subject_noun = st.text_input("Noun (for subject)", get_value("subject_noun", "dancer"))
subject_action = st.text_input("Action or Pose", get_value("subject_action", "twirling midair"))

env_adjectives = st.multiselect("Environment Adjectives", ["misty", "futuristic", "glowing", "foggy", "lush", "whimsical", "color-blocked", "ozone-clear", "carefully manicured", "retro-futuristic", "pastel-toned", "serene", "open", "flowing"], get_value("env_adjectives", []))
env_noun = st.text_input("Environment Noun", get_value("env_noun", "forest clearing"))
env_mood = st.text_input("Atmosphere or Mood", get_value("env_mood", "at dawn"))

medium = st.selectbox("Medium/Format", ["photorealistic", "oil painting", "3D render", "sketch", "digital illustration", "animated cel illustration", "glossy magazine illustration", "black and white sketch"], index=0)
style = st.selectbox("Style or Artist", [
    "TaijiFit Style – natural light, photorealistic, Hasselblad-quality professional look",
    "Studio Ghibli – whimsical, nature-focused anime with soft lighting",
    "Moebius – surreal, flowing sci-fi landscapes in fine line art",
    "Norman Rockwell – nostalgic Americana, highly detailed realism",
    "Hayao Miyazaki – fantastical creatures with emotional storytelling",
    "H.R. Giger – biomechanical, dark, surreal horror fusion",
    "Salvador Dalí – dreamlike surrealism, melting reality"
], index=0)
lighting = st.selectbox("Lighting", ["cinematic lighting", "soft daylight", "volumetric rays", "flat lighting with bold shadows", "cinematic Kodachrome lighting", "harsh shadows"], index=0)
color_scheme = st.selectbox("Color Scheme", ["vibrant colors", "monochromatic", "pastel palette", "neon tones", "bold primaries", "pastel palette with chrome accents", "sun-bleached warm tones"], index=0)
composition = st.selectbox("Composition / Camera Angle", ["wide angle shot", "close-up", "low angle", "over-the-shoulder", "tilted cartoon action shot"], index=0)

quality = st.multiselect("Quality Boosters", ["hyperdetailed", "8k", "sharp focus", "clean lines", "exaggerated poses", "ad-perfect styling", "cartoon clarity", "hyper-clean", "digital grain", "soft textures", "painterly detail", "vintage textures", "hyperreal detail", "soft depth of field"], get_value("quality", []))
negative = st.text_area("Negative Prompts", get_value("negative", "ugly, deformed, blurry, watermark, text"))
aspect_ratio = st.selectbox("Aspect Ratio", ["16:9", "1:1", "9:16", "3:2"], index=0)
seed = st.text_input("Optional Seed", get_value("seed", ""))
style_strength = st.slider("Stylization Parameter (--s)", 0, 1000, int(get_value("style_strength", 500)))

# --- Generate Prompt ---
if st.button("🎨 Generate Image Prompt"):
    prompt = (
        f"{subject_quantity} {' '.join(subject_adjectives)} {subject_noun}, {subject_action}, "
        f"in a {' '.join(env_adjectives)} {env_noun} {env_mood}, {medium}, "
        f"in the style of {style}, with {lighting}, {color_scheme}, {composition}, "
        f"{', '.join(quality)} --no {negative} --ar {aspect_ratio}"
    )
    if seed:
        prompt += f" --seed {seed}"
    prompt += f" --s {style_strength}"

    st.markdown("### ✨ Your Prompt:")
    st.code(prompt, language="text")

    components.html(f"""
        <textarea id='promptBox' style='width:100%; height:100px;'>{prompt}</textarea>
        <button onclick="navigator.clipboard.writeText(document.getElementById('promptBox').value)">Copy to Clipboard</button>
    """, height=150)

    st.info("✅ Click the button above to copy your prompt to the clipboard!")
