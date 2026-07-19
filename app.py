import streamlit as st
from dotenv import load_dotenv
import os
import random  # Task 4: Import random module
import requests
import time
from urllib.parse import quote  # For proper URL encoding
from datetime import datetime

load_dotenv()

# ─────────────────────────────────────────────────────────────────
#  Page Config
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Image Studio",
    page_icon="🎨",
    layout="wide"
)

# ─────────────────────────────────────────────────────────────────
#  Global CSS
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

.main {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.04);
    border-right: 1px solid rgba(255,255,255,0.08);
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 50px;
    font-weight: 700;
    font-size: 16px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    transition: all 0.3s ease;
    letter-spacing: 0.5px;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
}

.hero-title {
    text-align: center;
    font-size: 3.2rem;
    font-weight: 900;
    background: linear-gradient(135deg, #f093fb, #f5576c, #4facfe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
    line-height: 1.1;
}

.hero-subtitle {
    text-align: center;
    color: rgba(255,255,255,0.55);
    font-size: 1.1rem;
    margin-bottom: 2rem;
}

.badge {
    display: inline-block;
    background: linear-gradient(135deg, #667eea33, #764ba233);
    border: 1px solid rgba(102,126,234,0.4);
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 0.78rem;
    color: #a78bfa;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.badge-container {
    text-align: center;
    margin-bottom: 1rem;
}

.footer {
    text-align: center;
    padding-top: 30px;
    color: rgba(255,255,255,0.3);
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
#  Task 4: Surprise Me prompt list (5 crazy creative prompts)
# ─────────────────────────────────────────────────────────────────
surprise_prompts = [
    "An astronaut riding a horse on Mars at golden sunset",
    "A cyberpunk street food vendor in neon-lit Tokyo rain",
    "A dragon made entirely of stained glass in a Gothic cathedral",
    "An underwater city built inside a giant jellyfish",
    "A samurai cat warrior defending a cherry blossom temple from robots"
]

# ─────────────────────────────────────────────────────────────────
#  Art Styles
# ─────────────────────────────────────────────────────────────────
art_styles = [
    "Photorealistic",
    "Anime",
    "Oil Painting",
    "Watercolor",
    "Digital Art",
    "Comic Book",
    "Cyberpunk",
    "Fantasy",
    "Pixel Art",
    "Sketch"
]

# ─────────────────────────────────────────────────────────────────
#  Sidebar Settings
# ─────────────────────────────────────────────────────────────────
st.sidebar.markdown("## ⚙️ Studio Settings")
st.sidebar.markdown("---")

art_style = st.sidebar.selectbox(
    "🎨 Art Style",
    art_styles,
    index=0
)

st.sidebar.markdown("---")

st.sidebar.markdown("**📐 Image Dimensions**")
# Task 1: width and height sliders
width = st.sidebar.slider("Width (px)", min_value=256, max_value=1920, value=1024, step=64)
height = st.sidebar.slider("Height (px)", min_value=256, max_value=1920, value=768, step=64)
st.sidebar.caption(f"📏 Output: {width} × {height} px")

st.sidebar.markdown("---")

# Task 3: Magic Enhance Toggle checkbox
magic_enhance = st.sidebar.checkbox("✨ Enable Magic Enhance")
if magic_enhance:
    st.sidebar.caption("🚀 Boost words will be added to your prompt for stunning quality!")

st.sidebar.markdown("---")
st.sidebar.markdown("**ℹ️ About**")
st.sidebar.caption("Powered by Pollinations AI · Built with Streamlit")

# ─────────────────────────────────────────────────────────────────
#  Hero Header
# ─────────────────────────────────────────────────────────────────
st.markdown('<div class="badge-container"><span class="badge">🎓 MirAI School of Technology</span></div>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">🎨 AI Image Studio</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Transform your imagination into stunning AI-generated artwork</p>', unsafe_allow_html=True)

st.markdown("---")

# ─────────────────────────────────────────────────────────────────
#  Main Input Area
# ─────────────────────────────────────────────────────────────────
col_input, col_style = st.columns([3, 1])

with col_input:
    user_prompt = st.text_area(
        "💭 Describe your image",
        placeholder="e.g. A majestic lion sitting on a throne in a cosmic galaxy...",
        height=120,
        help="Be descriptive! The more detail you give, the better the result."
    )

with col_style:
    st.markdown(f"**Selected Style:** `{art_style}`")
    st.markdown(f"**Size:** `{width} × {height}`")
    if magic_enhance:
        st.success("✨ Magic Enhance ON")
    else:
        st.info("Magic Enhance OFF")

st.markdown("")

btn_col1, btn_col2 = st.columns(2)

with btn_col1:
    generate_clicked = st.button("🚀 Generate Image", key="generate_btn")

with btn_col2:
    # Task 4: Surprise Me! button
    surprise_clicked = st.button("🎲 Surprise Me!", key="surprise_btn")


# ─────────────────────────────────────────────────────────────────
#  Image Generation Function
# ─────────────────────────────────────────────────────────────────
def generate_ai_image(prompt_text, art_style, width, height, magic_enhance, max_retries=3):
    """Fetch AI-generated image from Pollinations API.

    Returns (image_bytes_or_None, full_prompt, error_message_or_None)
    """

    # Build the full prompt with art style (commas are fine — they get encoded below)
    full_prompt = f"{prompt_text}, {art_style} style"

    # Task 3: Magic Enhance — append boost words if checkbox is checked
    if magic_enhance:
        full_prompt += ", masterpiece, 8k resolution, highly detailed, trending on artstation"

    # Encode the entire prompt — spaces → %20, commas → %2C, etc.
    encoded_prompt = quote(full_prompt, safe="")

    # Random seed forces a fresh generation every time
    seed = random.randint(1, 999999)

    # Explicit model + nologo + referrer so requests are correctly identified
    # by Pollinations and don't get treated as anonymous scraping traffic.
    url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?width={width}&height={height}&seed={seed}"
        f"&model=flux&nologo=true&referrer=ai-image-studio"
    )

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    last_error = None

    with st.spinner("🎨 AI is painting your masterpiece... Please wait..."):
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers, timeout=90)

                # Pollinations' free/anonymous tier is rate-limited (~1 request
                # per 15s). Back off and retry instead of failing immediately.
                if response.status_code == 429:
                    last_error = "Rate limited by the image API (too many requests)."
                    time.sleep(2 ** attempt * 3)  # 3s, 6s, 12s
                    continue

                if response.status_code != 200:
                    last_error = f"API returned status {response.status_code}."
                    time.sleep(1.5)
                    continue

                content_type = response.headers.get("Content-Type", "")
                # A 200 response isn't always a real image — the API can
                # return an HTML/JSON error page with a 200 status too.
                if "image" not in content_type or len(response.content) < 1000:
                    last_error = (
                        f"API responded but didn't return a valid image "
                        f"(content-type: {content_type or 'unknown'})."
                    )
                    time.sleep(1.5)
                    continue

                return response.content, full_prompt, None

            except requests.exceptions.Timeout:
                last_error = "Request timed out. The AI is busy."
                time.sleep(1.5)
            except requests.exceptions.RequestException as e:
                last_error = f"Network error: {e}"
                time.sleep(1.5)

    return None, full_prompt, last_error or "Unknown error generating image."


# ─────────────────────────────────────────────────────────────────
#  Handle Generate Click
# ─────────────────────────────────────────────────────────────────
if generate_clicked:
    if not user_prompt.strip():
        st.warning("⚠️ Please enter a prompt before generating!")
    else:
        image_bytes, final_prompt, error = generate_ai_image(
            user_prompt.strip(), art_style, width, height, magic_enhance
        )

        if image_bytes:
            st.markdown("---")
            st.markdown("### 🖼️ Your Generated Masterpiece")

            col_img, col_info = st.columns([2, 1])

            with col_img:
                st.image(image_bytes, use_container_width=True, caption=f"Style: {art_style} | {width}×{height}px")

            with col_info:
                st.markdown("**📋 Generation Details**")
                st.markdown(f"- 🎨 **Style:** {art_style}")
                st.markdown(f"- 📐 **Size:** {width} × {height} px")
                st.markdown(f"- ✨ **Magic Enhance:** {'ON 🟢' if magic_enhance else 'OFF 🔴'}")
                st.markdown(f"- 🕐 **Generated:** {datetime.now().strftime('%H:%M:%S')}")

                if magic_enhance:
                    st.success("✨ Magic Enhance was applied!")

                st.markdown("**🔗 Full Prompt Used:**")
                st.code(final_prompt, language=None)

                # Task 2 FIX + Bonus: Dynamic .png file name using art_style
                st.download_button(
                    label="📥 Download Image",
                    data=image_bytes,
                    file_name=f"{art_style.replace(' ', '_').lower()}_image.png",
                    mime="image/png",
                    use_container_width=True
                )
        else:
            st.error(f"❌ Couldn't generate the image. {error}")
            st.info("💡 Tip: the free Pollinations tier allows about 1 request every 15 seconds — wait a moment and try again.")


# ─────────────────────────────────────────────────────────────────
#  Handle Surprise Me! Click (Task 4)
# ─────────────────────────────────────────────────────────────────
if surprise_clicked:
    # Task 4: Use random.choice() to pick from the list
    random_prompt = random.choice(surprise_prompts)

    st.markdown("---")
    st.info(f"🎲 **Surprise Prompt Selected:** *{random_prompt}*")

    image_bytes, final_prompt, error = generate_ai_image(
        random_prompt, art_style, width, height, magic_enhance
    )

    if image_bytes:
        st.markdown("### 🖼️ Your Surprise Masterpiece!")

        col_img2, col_info2 = st.columns([2, 1])

        with col_img2:
            st.image(image_bytes, use_container_width=True,
                     caption=f"Surprise: {random_prompt[:50]}... | {width}×{height}px")

        with col_info2:
            st.markdown("**📋 Generation Details**")
            st.markdown(f"- 🎲 **Mode:** Surprise Me!")
            st.markdown(f"- 🎨 **Style:** {art_style}")
            st.markdown(f"- 📐 **Size:** {width} × {height} px")
            st.markdown(f"- ✨ **Magic Enhance:** {'ON 🟢' if magic_enhance else 'OFF 🔴'}")
            st.markdown(f"- 🕐 **Generated:** {datetime.now().strftime('%H:%M:%S')}")

            st.markdown("**💭 Surprise Prompt:**")
            st.code(random_prompt, language=None)

            # Task 2 FIX + Bonus: Dynamic .png file name
            st.download_button(
                label="📥 Download Surprise Image",
                data=image_bytes,
                file_name=f"{art_style.replace(' ', '_').lower()}_image.png",
                mime="image/png",
                use_container_width=True,
                key="surprise_download"
            )
    else:
        st.error(f"❌ Couldn't generate the image. {error}")
        st.info("💡 Tip: the free Pollinations tier allows about 1 request every 15 seconds — wait a moment and try again.")


# ─────────────────────────────────────────────────────────────────
#  Pro Tips Section
# ─────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 💡 Pro Tips for Better Images")

tip_col1, tip_col2, tip_col3 = st.columns(3)

with tip_col1:
    st.markdown("""
    **📝 Write Better Prompts**
    - Be specific and descriptive
    - Include lighting details
    - Mention mood and atmosphere
    - Add color preferences
    """)

with tip_col2:
    st.markdown("""
    **🎨 Use Art Styles**
    - "Photorealistic" for real-world looks
    - "Anime" for Japanese animation style
    - "Cyberpunk" for futuristic neon vibes
    - "Watercolor" for soft artistic feel
    """)

with tip_col3:
    st.markdown("""
    **✨ Magic Enhance**
    - Enable for lazy/short prompts
    - Automatically adds quality boosters
    - Great for professional results
    - Works with all art styles
    """)


# ─────────────────────────────────────────────────────────────────
#  Footer
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
<hr style="border-color:rgba(255,255,255,0.1)">
🎓 <b>MirAI School of Technology</b> · Virtual Summer Internship 2026 · AI Builder Track<br>
🎨 <b>AI Image Studio v2.0</b> · Powered by Pollinations AI + Streamlit<br>
Built with ❤️ as part of the Weekend Assignment
</div>
""", unsafe_allow_html=True)