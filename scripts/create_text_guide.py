from PIL import Image, ImageDraw, ImageFont
import os

def create_guide():
    img = Image.new('RGB', (1024, 512), color='white')
    draw = ImageDraw.Draw(img)
    text = 'Sonagi'
    
    # Try to find a bold sans-serif font
    font_paths = [
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf'
    ]
    
    font = None
    for path in font_paths:
        if os.path.exists(path):
            font = ImageFont.truetype(path, 200)
            break
            
    if font is None:
        font = ImageFont.load_default()
        print("Warning: Using default font, text might be small.")

    # Calculate centering
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    
    draw.text(((1024-w)/2, (512-h)/2 - 40), text, fill='#1991b9', font=font)
    
    output_path = '/home/mindulle/comfyui-workspace/input/sonagi_guide.png'
    img.save(output_path)
    print(f"Guide image saved to {output_path}")

if __name__ == "__main__":
    create_guide()
