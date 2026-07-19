# 🎨 AI Image Studio

An AI-powered image generation app built with Streamlit and the Pollinations AI API.
Built as part of the **MirAI School of Technology — Virtual Summer Internship 2026, AI Builder Track**.

## 🚀 Live Demo

Run locally with:
```bash
pip install -r requirements.txt
streamlit run app.py
```
Then open `http://localhost:8501` in your browser.

## ✨ Features

This version upgrades the original prototype with the following fixes and features:

### 1. Fixed Broken Sliders (URL Parameters)
The width and height sliders in the sidebar now actually control the output image size. Previously the values were captured in the UI but never sent to the API — the generation URL now includes `?width=...&height=...` so the sliders work as expected.

### 2. Fixed Download File Extension
Downloaded images now save with a proper `.png` extension so the OS recognizes and opens them correctly. The filename is also dynamic, based on the selected art style (e.g. `cyberpunk_image.png`).

### 3. ✨ Magic Enhance Toggle
A sidebar checkbox that, when enabled, automatically appends quality-boosting keywords (`masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render`) to the prompt — helpful for users who write short or simple descriptions.

### 4. 🎲 Surprise Me!
A one-click button that picks a random, creative prompt from a curated list (using Python's `random.choice()`) and instantly generates an image — great for beating writer's block.

## 🛠️ Tech Stack

- **[Streamlit](https://streamlit.io/)** — UI framework
- **[Pollinations AI](https://pollinations.ai/)** — free image generation API
- **Python** `requests` — API calls
- **python-dotenv** — environment variable management

## 📂 Project Structure

```
.
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (not committed)
├── .gitignore
└── README.md
```

## ⚙️ Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## 📋 Pre-Submission Checklist

- [x] Width and height sliders control the generated image's dimensions
- [x] Downloaded images open correctly as `.png` files
- [x] "Surprise Me" button generates a random image on click
- [x] "Magic Enhance" toggle appends quality-boost keywords to the prompt

## 🎓 Credit

Built during the **MirAI School of Technology** Virtual Summer Internship 2026 — AI Builder Track.