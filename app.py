import os
import gradio as gr
from moviepy.editor import *
from PIL import Image, ImageDraw
from gtts import gTTS

pro_css = """
.gradio-container{background: radial-gradient(circle at top, #1a1a2e, #16213e, #0f0c29)!important}
#brand h1{font-size:52px!important; background:linear-gradient(90deg,#FFD700,#FF512F); -webkit-background-clip:text; color:transparent!important; text-align:center}
#brand h2{text-align:center; color:#aaa!important; letter-spacing:5px}
button.primary{background:linear-gradient(90deg,#FFD700,#FF512F)!important; color:black!important; font-weight:900!important; border-radius:30px!important}
"""

def kiovid_engine(mode, files, voice, script, prompt_ai, motion, vfx, title, cta, export, use_ai_voice, use_ai_image):
    clips=[]
    if files:
        for f in files:
            try:
                if f.name.lower().endswith(('.png','.jpg','.jpeg')):
                    c=ImageClip(f.name).set_duration(4).resize(lambda t:1+0.04*t)
                    size=(1920,1080) if "16:9" in export else (1080,1920)
                    clips.append(c.resize(size).set_position('center'))
                else:
                    clips.append(VideoFileClip(f.name).resize((1920,1080)))
            except: pass
    if not clips: clips=[ColorClip((1920,1080),color=(15,10,40)).set_duration(6)]
    base=concatenate_videoclips(clips, method="compose")

    if voice:
        audio=AudioFileClip(voice.name)
        base=base.set_duration(audio.duration+1).set_audio(audio)
    elif script and use_ai_voice:
        gTTS(script, lang='bn').save("ai_voice.mp3")
        base=base.set_duration(AudioFileClip("ai_voice.mp3").duration+1).set_audio(AudioFileClip("ai_voice.mp3"))

    if vfx=="KIOVID Gold Glow": base=base.fl(lambda gf,t:(gf(t)*1.2).clip(0,255).astype('uint8'))
    if title:
        txt=TextClip(title, fontsize=70, color='yellow', stroke_color='black', stroke_width=3, font='DejaVu-Sans-Bold')
        txt=txt.set_position(('center',80)).set_duration(base.duration)
        base=CompositeVideoClip([base,txt])

    base.write_videofile("KIOVID_FINAL.mp4", fps=24, codec='libx264')
    thumb=Image.new('RGB',(1280,720),color=(20,10,40))
    ImageDraw.Draw(thumb).text((640,360), title[:50], fill=(255,215,0), anchor="mm")
    thumb.save("KIOVID_THUMB.jpg")
    return "KIOVID_FINAL.mp4", "KIOVID_THUMB.jpg", f"KIOVID by kIORAX | {mode} | {title}"

with gr.Blocks(css=pro_css, theme=gr.themes.Soft()) as demo:
    gr.Markdown("<div id='brand'><h1>KIOVID</h1><h2>by kIORAX • AI + CODE STUDIO</h2></div>")
    with gr.Row():
        mode=gr.Dropdown(["YouTube Long - Sanatan","Ads Video - kIORAX","Graphics Promo"], value="YouTube Long - Sanatan")
        export=gr.Dropdown(["YouTube Long (16:9)","Ads/Shorts (9:16)"], value="YouTube Long (16:9)")
    with gr.Row():
        with gr.Column():
            use_ai_image=gr.Checkbox(label="AI Image", value=True)
            prompt_ai=gr.Textbox(label="AI Prompt", value="Lord Krishna divine")
            use_ai_voice=gr.Checkbox(label="AI Voice", value=True)
            script=gr.Textbox(label="Script", value="হরে কৃষ্ণ, KIOVID থেকে স্বাগতম")
        with gr.Column():
            files=gr.File(file_count="multiple", label="Upload Images/Videos")
            voice=gr.File(file_types=["audio"], label="Voice Over")
            motion=gr.Dropdown(["AI Auto Zoom","Slow Zoom"], value="AI Auto Zoom")
            vfx=gr.Dropdown(["KIOVID Gold Glow","No VFX"], value="KIOVID Gold Glow")
    title=gr.Textbox(label="TITLE", value="॥ KIOVID by kIORAX ॥")
    cta=gr.Textbox(label="CTA", value="Order Now")
    btn=gr.Button("⚡ GENERATE WITH KIOVID ENGINE", elem_classes="primary")
    out_v=gr.Video(label="Final Video")
    out_t=gr.Image(label="Thumbnail")
    out_s=gr.Textbox(label="SEO")
    btn.click(kiovid_engine, inputs=[mode, files, voice, script, prompt_ai, motion, vfx, title, cta, export, use_ai_voice, use_ai_image], outputs=[out_v, out_t, out_s])

# Render এর জন্য এই লাইনটা জরুরি
demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
