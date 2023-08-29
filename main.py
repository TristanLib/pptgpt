import gradio as gr
import openai
import requests
from pptx import Presentation
from pptx.util import Inches
from io import BytesIO

# OpenAI API密钥
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Unsplash API的URL
UNSPLASH_URL = "https://api.unsplash.com/photos/random?query={}&client_id=YOUR_UNSPLASH_API_KEY"

def generate_ppt(prompt):
    # 使用OpenAI API获取提纲
    response = openai.Completion.create(
      engine="davinci",
      prompt=prompt,
      max_tokens=150
    )
    outline = response.choices[0].text.strip().split('\n')

    # 创建PPT
    prs = Presentation()
    for point in outline:
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        title = slide.shapes.title
        title.text = point

        # 从Unsplash获取图片
        response = requests.get(UNSPLASH_URL.format(point))
        image_url = response.json()["urls"]["small"]
        image = requests.get(image_url).content
        image_stream = BytesIO(image)

        # 添加图片到PPT
        slide.shapes.add_picture(image_stream, Inches(1), Inches(1), width=Inches(4))

    # 保存PPT到文件
    ppt_file = "generated_ppt.pptx"
    prs.save(ppt_file)

    return ppt_file

# 创建gradio界面
interface = gr.Interface(
    fn=generate_ppt, 
    inputs=gr.Textbox(lines=5, placeholder="请输入你的提示语..."), 
    outputs=gr.File(),
    live=False
)

interface.launch()
