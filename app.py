import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np

st.set_page_config(page_title="KIOVID Image by kIORAX", page_icon="🖼️", layout="wide")

# --- PREMIUM UI CSS ---
st.markdown("""
<style>
.stApp {background: radial-gradient(ellipse at top, #1a1a2e 0%, #0f0c29 100%) !important}
h1 {font-size: 58px !important; font-weight: 900 !important; background: linear-gradient(90deg, #FFD700, #FF8C00, #FF512F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center}
.gold-card {background: rgba(255,255,255,0.06); border: 1px solid rgba(255,215,0,0.3); border-radius: 18px; padding: 18px; margin-bottom: 12px}
.stButton>button {background: linear-gradient(90deg, #FFD700, #FF512F) !important; color: black !important; font-weight: 900 !important; font-size: 18px !important; border-radius: 30px !important; height: 55px !important; width: 100%}
</style>
<h1>🖼️ KIOVID IMAGE</h1>
<p style='text-align:center; color:gold; letter-spacing:5px'>PREMIUM POSTER & THUMBNAIL MAKER by kIORAX</p>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### ✍️ Title")
    title = st.text_input("", "॥ KIOVID by kIORAX ॥")
    sub = st.text_input("Subtitle", "হরে কৃষ্ণ - Sanatan Dharma")
    st.markdown("### 🎨 Style")
    style = st.selectbox("", ["Gold Glow ✨", "Sanatan Warm 🔥", "Divine Blur 💫", "Cinematic Dark 🎬"])
    font_size = st.slider("Font Size", 40, 120, 75)
    st.markdown("### 📍 Position")
    pos = st.selectbox("", ["Top Center", "Center", "Bottom Center"])

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="gold-card">', unsafe_allow_html=True)
    uploaded = st.file_uploader("📁 Base Image Upload করো", type=["png","jpg","jpeg","webp"])
    st.markdown('</div>', unsafe_allow_html=True)
    gen = st.button("⚡ GENERATE PREMIUM IMAGE")

with col2:
    st.markdown('<div class="gold-card">', unsafe_allow_html=True)
    st.markdown("#### 🎨 Output")
    out_place = st.empty()
    st.markdown('</div>', unsafe_allow_html=True)

def make_premium_image(base_img, title, sub, style, font_size, pos):
    W, H = 1280, 720
    img = base_img.convert("RGB").resize((W,H))
    
    # Style Filters
    if "Gold" in style:
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.4)
        enhancer2 = ImageEnhance.Brightness(img)
        img = enhancer2.enhance(1.15)
    elif "Sanatan" in style:
        # Warm filter
        arr = np.array(img, dtype=np.float32)
        arr[:,:,0] *= 1.2
        arr[:,:,1] *= 1.05
        arr = np.clip(arr, 0, 255)
        img = Image.fromarray(arr.astype('uint8'))
    elif "Blur" in style:
        img = img.filter(ImageFilter.GaussianBlur(1))
    elif "Cinematic" in style:
        # Darken edges
        overlay = Image.new('RGB', (W,H), (0,0,20))
        img = Image.blend(img, overlay, 0.25)

    draw = ImageDraw.Draw(img)
    try:
        font_main = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
        font_sub = ImageFont.truetype("DejaVuSans.ttf", 32)
    except:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Position logic
    if "Top" in pos: y = 120
    elif "Bottom" in pos: y = H-120
    else: y = H//2

    x = W//2

    # Premium Title with Shadow + Gold Stroke
    # Shadow
    draw.text((x+4, y+4), title, font=font_main, fill="black", anchor="mm", stroke_width=4, stroke_fill="black")
    # Gold Main
    draw.text((x, y), title, font=font_main, fill=(255,215,0), anchor="mm", stroke_width=2, stroke_fill="black")
    
    # Subtitle
    if sub.strip():
        draw.text((x+2, y+font_size//2+42), sub, font=font_sub, fill="black", anchor="mm")
        draw.text((x, y+font_size//2+40), sub, font=font_sub, fill="white", anchor="mm")

    return img

if gen:
    if not uploaded:
        st.error("আগে একটা ছবি আপলোড করো!")
    else:
        base = Image.open(uploaded)
        result = make_premium_image(base, title, sub, style, font_size, pos)
        out_place.image(result, use_container_width=True)
        
        # Download
        result.save("KIOVID_PREMIUM.jpg", quality=95)
        with open("KIOVID_PREMIUM.jpg", "rb") as f:
            st.download_button("📥 DOWNLOAD HD IMAGE", f, "KIOVID_PREMIUM_HD.jpg", "image/jpeg")
