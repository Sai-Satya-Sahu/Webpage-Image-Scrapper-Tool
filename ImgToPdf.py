import os
from PIL import Image
import re

# Folder where images are saved
IMAGE_FOLDER = "downloaded_images"
OUTPUT_PDF = "document.pdf"

# Main Functions
def extract_number(filename):
    match = re.search(r'image_(\d+)', filename)
    return int(match.group(1)) if match else float('inf')

def convert_images_to_pdf():
    if not os.path.exists(IMAGE_FOLDER):
        print(f"❌ Folder '{IMAGE_FOLDER}' not found.")
        return

    image_files = sorted(
        [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".bmp"))],
        key=extract_number
    )

    if not image_files:
        print("❌ No image files found to convert.")
        return

    print(f"🖼 Found {len(image_files)} images. Converting to PDF...")

    image_list = []
    for idx, file in enumerate(image_files):
        img_path = os.path.join(IMAGE_FOLDER, file)
        img = Image.open(img_path).convert("RGB")
        image_list.append(img)

    pdf_path = os.path.join(IMAGE_FOLDER, OUTPUT_PDF)
    image_list[0].save(pdf_path, save_all=True, append_images=image_list[1:])
    print(f"✅ PDF saved as '{pdf_path}'")

if __name__ == "__main__":
    convert_images_to_pdf()
