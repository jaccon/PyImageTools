import os
from tqdm import tqdm

def generate_html_gallery(directory, output_file="gallery.html"):
    # Get all image files recursively in the specified directory
    image_files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # Create the HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Image Gallery</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                background-color: #000;
            }
            #gallery-container {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-around;
                align-items: flex-start;
                padding: 20px;
            }
            .gallery-item {
                position: relative;
                flex: 0 0 30%;
                margin: 10px;
            }
            .gallery-item img {
                width: 100%;
                height: auto;
                cursor: pointer;
            }
            #modal {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.8);
                z-index: 1;
                justify-content: center;
                align-items: center;
            }
            #modal img {
                max-width: 80%;
                max-height: 80%;
                width: auto;
            }
        </style>
    </head>
    <body>
        <div id="gallery-container">
    """

    # Add image elements to the HTML content
    for i, image_file in enumerate(tqdm(image_files, desc="Creating HTML Gallery", unit="image")):
        image_path = os.path.join(directory, image_file)
        html_content += f'<div class="gallery-item" onclick="openModal(\'{image_path}\')" tabindex="{i + 1}" onkeydown="handleImageNavigation(event)"><img src="{image_path}" alt="{image_file}"></div>\n'

    # Close the HTML content
    html_content += """
        </div>
        <div id="modal" onclick="closeModal()">
            <img id="modal-img" alt="Modal Image">
        </div>
        <script>
            var currentIndex = 0;
            var images = document.getElementsByClassName('gallery-item');
            var modalImg = document.getElementById('modal-img');
            var modal = document.getElementById('modal');

            function openModal(imagePath) {
                modalImg.src = imagePath;
                modal.style.display = 'flex';
                currentIndex = Array.from(images).findIndex(item => item.contains(document.activeElement));
                document.addEventListener('keydown', handleKeyPress);
            }

            function closeModal() {
                modal.style.display = 'none';
                document.removeEventListener('keydown', handleKeyPress);
                currentIndex = 0;  // Reset currentIndex when closing the modal
            }

            function handleKeyPress(event) {
                if (event.key === 'Escape') {
                    closeModal();
                } else if (event.key === 'ArrowLeft') {
                    navigate('prev');
                } else if (event.key === 'ArrowRight') {
                    navigate('next');
                }
            }

            function handleImageNavigation(event) {
                if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
                    navigate(event.key === 'ArrowLeft' ? 'prev' : 'next');
                    event.preventDefault();
                }
            }

            function navigate(direction) {
                if (direction === 'prev') {
                    currentIndex = (currentIndex - 1 + images.length) % images.length;
                } else if (direction === 'next') {
                    currentIndex = (currentIndex + 1) % images.length;
                }

                modalImg.src = images[currentIndex].getElementsByTagName('img')[0].src;
            }
        </script>
    </body>
    </html>
    """

    # Write the HTML content to the output file
    with open(output_file, "w") as html_file:
        html_file.write(html_content)

if __name__ == "__main__":
    # Specify the source directory (e.g., "Photos")
    source_directory = "Photos"
    
    # Specify the output HTML file
    output_html_file = "gallery.html"

    # Generate the HTML gallery
    generate_html_gallery(source_directory, output_html_file)

    print(f"Image gallery generated successfully. Open '{output_html_file}' in a web browser.")
