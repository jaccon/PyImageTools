import os
from PIL import Image, ImageDraw
from tqdm import tqdm
import json

def apply_watermark(source_path, watermark_path, output_path, watermark_width, watermark_position, watermark_transparency):
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    # Load watermark image
    watermark = Image.open(watermark_path)
    watermark = watermark.resize((watermark_width, int(watermark_width * watermark.size[1] / watermark.size[0])), Image.ANTIALIAS)

    # Create a transparent version of the watermark
    watermark = watermark.convert("RGBA")
    watermark_with_transparency = Image.new("RGBA", watermark.size)
    for x in range(watermark.width):
        for y in range(watermark.height):
            r, g, b, a = watermark.getpixel((x, y))
            watermark_with_transparency.putpixel((x, y), (r, g, b, int(a * (1.0 - float(watermark_transparency)))))

    # Iterate through images in the source directory
    images = [f for f in os.listdir(source_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    for image_name in tqdm(images, desc="Applying Watermark", unit="image"):
        image_path = os.path.join(source_path, image_name)
        output_image_path = os.path.join(output_path, image_name)

        # Load image
        image = Image.open(image_path)

        # Calculate watermark position
        if watermark_position == "top-left":
            position = (0, 0)
        elif watermark_position == "top-right":
            position = (image.width - watermark.width, 0)
        elif watermark_position == "bottom-left":
            position = (0, image.height - watermark.height)
        elif watermark_position == "bottom-right":
            position = (image.width - watermark.width, image.height - watermark.height)
        else:
            raise ValueError("Invalid watermark position. Supported positions: top-left, top-right, bottom-left, bottom-right")

        # Create a transparent layer for the watermark
        watermark_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
        watermark_layer.paste(watermark_with_transparency, position, watermark_with_transparency)

        # Composite image and watermark
        watermarked_image = Image.alpha_composite(image.convert("RGBA"), watermark_layer)

        # Save the result
        watermarked_image.save(output_image_path, format="PNG")

if __name__ == "__main__":
    # Read setup parameters from setup.json
    with open("setup.json", "r") as setup_file:
        setup = json.load(setup_file)

    watermark_path = setup["watermark"]
    source_path = setup["source_watermark"]
    watermark_width = setup["watermark_width"]
    watermark_position = setup.get("watermark_position", "bottom-right")
    watermark_transparency = float(setup.get("watermark_transparency", 0.5))

    output_path = "Output"  # You can change this to your desired output directory

    apply_watermark(source_path, watermark_path, output_path, watermark_width, watermark_position, watermark_transparency)
