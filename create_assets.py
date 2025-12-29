from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    size = (192, 192)
    img = Image.new('RGBA', size, (46, 125, 50, 255))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([10, 10, 182, 182], outline=(212, 175, 55, 255), width=8)
    draw.rectangle([18, 18, 174, 174], outline=(255, 215, 0, 255), width=4)
    
    try:
        font_large = ImageFont.truetype("arial.ttf", 60)
        font_small = ImageFont.truetype("arial.ttf", 30)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    text = "24"
    bbox = draw.textbbox((0, 0), text, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) / 2
    y = (size[1] - text_height) / 2 - 10
    draw.text((x, y), text, font=font_large, fill=(255, 255, 255, 255))
    
    subtext = "点"
    bbox2 = draw.textbbox((0, 0), subtext, font=font_small)
    text_width2 = bbox2[2] - bbox2[0]
    text_height2 = bbox2[3] - bbox2[1]
    x2 = (size[0] - text_width2) / 2
    y2 = y + text_height + 5
    draw.text((x2, y2), subtext, font=font_small, fill=(255, 194, 7, 255))
    
    img.save('data/icon.png')
    print("图标已创建: data/icon.png")

def create_presplash():
    size = (480, 800)
    img = Image.new('RGBA', size, (46, 125, 50, 255))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([20, 20, 460, 780], outline=(212, 175, 55, 255), width=10)
    draw.rectangle([30, 30, 450, 770], outline=(255, 215, 0, 255), width=5)
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 80)
        font_subtitle = ImageFont.truetype("arial.ttf", 40)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
    
    title = "24点"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) / 2
    y = size[1] / 3
    draw.text((x, y), title, font=font_title, fill=(255, 255, 255, 255))
    
    subtitle = "扑克牌游戏"
    bbox2 = draw.textbbox((0, 0), subtitle, font=font_subtitle)
    text_width2 = bbox2[2] - bbox2[0]
    text_height2 = bbox2[3] - bbox2[1]
    x2 = (size[0] - text_width2) / 2
    y2 = y + text_height + 30
    draw.text((x2, y2), subtitle, font=font_subtitle, fill=(255, 194, 7, 255))
    
    loading = "正在加载..."
    bbox3 = draw.textbbox((0, 0), loading, font=font_subtitle)
    text_width3 = bbox3[2] - bbox3[0]
    text_height3 = bbox3[3] - bbox3[1]
    x3 = (size[0] - text_width3) / 2
    y3 = size[1] * 2 / 3
    draw.text((x3, y3), loading, font=font_subtitle, fill=(255, 255, 255, 179))
    
    img.save('data/presplash.png')
    print("启动画面已创建: data/presplash.png")

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    create_icon()
    create_presplash()
