from PIL import Image, ExifTags
from tqdm import tqdm
import os
import json

def resize_images(source_dir, dest_dir, target_width, target_height, compression_quality):
    # Create the destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Get a list of all files in the source directory
    files = os.listdir(source_dir)

    # Create a tqdm progress bar
    progress_bar = tqdm(files, desc="Resizing Images", unit="image")

    for file in progress_bar:
        # Check if the file is an image (you can add more image extensions if needed)
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            # Construct the full file paths
            source_path = os.path.join(source_dir, file)
            dest_path = os.path.join(dest_dir, file)

            # Open the image using Pillow
            image = Image.open(source_path)

            # Check and rotate the image based on its EXIF orientation
            try:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = dict(image._getexif().items())
                if exif[orientation] == 3:
                    image = image.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    image = image.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    image = image.rotate(90, expand=True)
            except (AttributeError, KeyError, IndexError):
                # Ignore if there is no EXIF information or if there is an error
                pass

            # Resize the image while preserving the aspect ratio
            aspect_ratio = image.width / image.height
            new_width = target_width
            new_height = int(new_width / aspect_ratio)
            resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

            # Save the resized image to the destination directory with compression quality
            resized_image.save(dest_path, quality=compression_quality)

    # Close the tqdm progress bar
    progress_bar.close()

if __name__ == "__main__":
    # Read configuration from setup.json
    with open('setup.json', 'r') as config_file:
        config = json.load(config_file)

    # Set the source and destination directories
    source_directory = config["source_directory"]
    destination_directory = config["destination_directory"]

    # Set the desired width and height for resizing
    target_width = config["width"]
    target_height = config["height"]

    # Set the compression quality
    compression_quality = config["compression_quality"]

    # Call the function to resize images
    resize_images(source_directory, destination_directory, target_width, target_height, compression_quality)

    print("Image resizing completed.")
