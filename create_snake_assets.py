from PIL import Image, ImageDraw, ImageFont

def create_icon(size=(192, 192)):
    img = Image.new('RGBA', size, (0, 150, 0, 255))
    draw = ImageDraw.Draw(img)
    
    center_x = size[0] // 2
    center_y = size[1] // 2
    snake_width = 20
    
    draw.rectangle([center_x - 60, center_y - 10, center_x + 60, center_y + 10], fill=(0, 255, 0, 255))
    draw.rectangle([center_x - 10, center_y - 40, center_x + 10, center_y + 40], fill=(0, 255, 0, 255))
    
    draw.ellipse([center_x - 15, center_y - 15, center_x + 15, center_y + 15], fill=(255, 0, 0, 255))
    
    return img

def create_presplash(size=(1024, 1024)):
    img = Image.new('RGBA', size, (0, 100, 0, 255))
    draw = ImageDraw.Draw(img)
    
    center_x = size[0] // 2
    center_y = size[1] // 2
    
    draw.rectangle([center_x - 200, center_y - 50, center_x + 200, center_y + 50], fill=(0, 255, 0, 255))
    draw.rectangle([center_x - 50, center_y - 200, center_x + 50, center_y + 200], fill=(0, 255, 0, 255))
    
    draw.ellipse([center_x - 60, center_y - 60, center_x + 60, center_y + 60], fill=(255, 0, 0, 255))
    
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()
    
    text = "Snake Game"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    draw.text((center_x - text_width // 2, center_y + 150), text, fill=(255, 255, 255, 255), font=font)
    
    return img

if __name__ == '__main__':
    import os
    
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    icon = create_icon()
    icon.save(os.path.join(data_dir, 'icon.png'))
    print(f"Created {os.path.join(data_dir, 'icon.png')}")
    
    presplash = create_presplash()
    presplash.save(os.path.join(data_dir, 'presplash.png'))
    print(f"Created {os.path.join(data_dir, 'presplash.png')}")
