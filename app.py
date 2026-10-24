import streamlit as st
from moviepy.editor import *
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os, tempfile

st.set_page_config(page_title="KIOVID by kIORAX", page_icon="🔱", layout="wide")

# --- PREMIUM GOLDEN CSS ---
st.markdown("""
<style>
.stApp {background: radial-gradient(ellipse at top, #1e1e3f 0%, #0f0c29 100%) !important; color: white !important}
h1 {font-size: 60px !important; font-weight: 900 !important; background: linear-gradient(90deg, #FFD700, #FF8C00, #FF512F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center}
.gold-card {background: rgba(255,255,255,0.06); border: 1px solid rgba(255,215,0,0.3); border-radius: 18px; padding: 20px; backdrop-filter: blur(10px); margin-bottom: 15px}
.stButton>button {background: linear-gradient(90deg, #FFD700, #FF512F) !important; color: black !important; font-weight: 900 !important; font-size: 19px !important; border-radius: 30px !important; height: 60px !important; width: 100%; border: none !important; box-shadow: 0 0 25px rgba(255,215,0,0.5)}
</style>
<h1>🔱 KIOVID</h1>
<p style='text-align:center; color:gold; letter-spacing:6px'>PREMIUM EDITION by kIORAX • 2026 • FREE</p>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🎨 Style")
    style = st.selectbox("", ["Gold Glow ✨ Premium", "Sanatan Warm 🔥", "Original"])
    st.markdown("### 🏷️ Title")
    title = st.text_input("", "॥ KIOVID by kIORAX ॥")
    st.markdown("### 📝 Bangla Script")
    script = st.text_area("", "হরে কৃষ্ণ, KIOVID by kIORAX থেকে স্বাগতম, সনাতন ধর্মের জয় হোক", height=120)

# --- MAIN ---
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="gold-card">', unsafe_allow_html=True)
    st.markdown("#### 📁 Upload Images / Videos")
    files = st.file_uploader("", type=["png","jpg","jpeg","webp","mp4","mov"], accept_multiple_files=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    generate = st.button("⚡ GENERATE PREMIUM VIDEO")

with col2:
    st.markdown('<div class="gold-card">', unsafe_allow_html=True)
    st.markdown("#### 🎬 Output")
    video_placeholder = st.empty()
    thumb_placeholder = st.empty()
    seo_placeholder = st.empty()
    st.markdown('</div>', unsafe_allow_html=True)

# --- ENGINE ---
def add_title_func(frame, title_text):
    pil = Image.fromarray(frame)
    draw = ImageDraw.Draw(pil)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 55)
    except:
        font = ImageFont.load_default()
    draw.text((643,83), title_text, font=font, fill="black", anchor="mm")
    draw.text((640,80), title_text, font=font, fill=(255,215,0), anchor="mm", stroke_width=2, stroke_fill="black")
    return np.array(pil)

if generate:
    if not files:
        st.error("⚠️ আগে ছবি/ভিডিও আপলোড করো!")
    else:
        with st.spinner("🎬 KIOVID Premium ভিডিও বানানো হচ্ছে..."):
            clips = []
            temp_dir = tempfile.mkdtemp()
            for f in files:
                path = os.path.join(temp_dir, f.name)
                with open(path, "wb") as out:
                    out.write(f.getbuffer())
                if path.lower().endswith(('.png','.jpg','.jpeg','.webp')):
                    clips.append(ImageClip(path).set_duration(3).resize((1280,720)).set_position('center'))
                else:
                    clips.append(VideoFileClip(path).resize((1280,720)))
            
            base = concatenate_videoclips(clips, method="compose")

            # Voice
            if script.strip():
                try:
                    gTTS(text=script, lang='bn').save(os.path.join(temp_dir, "voice.mp3"))
                    audio = AudioFileClip(os.path.join(temp_dir, "voice.mp3"))
                    base = base.set_duration(audio.duration+1).set_audio(audio)
                except:
                    base = base.set_duration(6)
            else:
                base = base.set_duration(6)

            if "Gold" in style:
                base = base.fl_image(lambda f: np.clip(f*1.25, 0, 255).astype('uint8'))

            if title.strip():
                base = base.fl_image(lambda frame: add_title_func(frame, title))

            out_path = os.path.join(temp_dir, "KIOVID_FINAL.mp4")
            base.write_videofile(out_path, fps=24, codec='libx264', preset='ultrafast', logger=None)
            
            # Thumbnail
            thumb_path = os.path.join(temp_dir, "thumb.jpg")
            Image.fromarray(base.get_frame(0.5)).save(thumb_path)

            video_placeholder.video(out_path)
            thumb_placeholder.image(thumb_path, caption="Thumbnail")
            seo_placeholder.code(f"TITLE: {title}\nSCRIPT: {script}\nTAGS: #KIOVID #kIORAX #Sanatan", language="text")
            
            with open(out_path, "rb") as v:
                st.download_button("📥 DOWNLOAD FULL HD VIDEO", v, file_name="KIOVID_PREMIUM.mp4", mime="video/mp4")
