import os
import gradio as gr
from PIL import Image, ImageDraw

pro_css = """
.gradio-container{background:#0f0c29!important}
button.primary{background:linear-gradient(90deg,#FFD700,#FF512F)!important; color:black!important; font-weight:900!important; border-radius:30px!important}
"""

def kiovid_turbo(title, script):
    # Fast Thumbnail Only - No heavy video yet
    thumb=Image.new('RGB',(1280,720),color=(20,10,40))
    draw=ImageDraw.Draw(thumb)
    draw.text((640, 300), "KIOVID", fill=(255,215,0), anchor="mm", align="center")
    draw.text((640, 380), title[:60], fill=(255,255,255), anchor="mm", align="center")
    thumb.save("KIOVID_THUMB.jpg")
    # Fast SEO
    seo = f"Title: {title}\nDescription: {script}\nTags: KIOVID, kIORAX, Sanatan\n#KIOVID #kIORAX"
    return "KIOVID_THUMB.jpg", seo

with gr.Blocks(css=pro_css) as demo:
    gr.Markdown("<h1 style='text-align:center; color:#FFD700'>KIOVID TURBO by kIORAX</h1>")
    title=gr.Textbox(label="TITLE", value="॥ KIOVID by kIORAX ॥")
    script=gr.Textbox(label="Script", lines=4, value="হরে কৃষ্ণ, KIOVID থেকে স্বাগতম")
    btn=gr.Button("⚡ GENERATE TURBO (5 sec)", elem_classes="primary")
    out_t=gr.Image(label="Thumbnail - Instant")
    out_s=gr.Textbox(label="SEO Pack")
    btn.click(kiovid_turbo, inputs=[title, script], outputs=[out_t, out_s])

demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
