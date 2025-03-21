import torch
import streamlit as st
import os
import qrcode
import tempfile
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from diffusers import StableDiffusionInstructPix2PixPipeline
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get the API key from .env
CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")

if not CLIENT_ID:
    raise ValueError("IMGUR_CLIENT_ID is missing! Add it to the .env file.")

# Set device (Use GPU if available)
device = "cuda" if torch.cuda.is_available() else "cpu"
st.write(f"Using device: {device}")

# Load model
MODEL_NAME = "instruction-tuning-sd/cartoonizer"
try:
    pipeline = StableDiffusionInstructPix2PixPipeline.from_pretrained(
        MODEL_NAME, torch_dtype=torch.float16 if device == "cuda" else torch.float32
    ).to(device)
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

st.title("📸 Live Image Cartoonizer 🎨")

# Webcam input
captured_image = st.camera_input("Take a photo")

def upload_to_imgur(image):
    """Uploads image to Imgur and returns the public URL."""
    CLIENT_ID = "d86bc4bc36bd909"  # Replace with your Imgur client ID

    # Save image temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        image.save(temp_file.name, format="PNG")
        temp_file_path = temp_file.name

    # Upload to Imgur
    headers = {"Authorization": f"Client-ID {CLIENT_ID}"}
    with open(temp_file_path, "rb") as img:
        response = requests.post(
            "https://api.imgur.com/3/upload",
            headers=headers,
            files={"image": img},
        )
    
    # Parse response
    if response.status_code == 200:
        return response.json()["data"]["link"]  # Return the public Imgur link
    else:
        st.error("Failed to upload image to Imgur. Try again.")
        return None

def generate_qr_code(url):
    """Generates a QR code for the given URL."""
    qr = qrcode.make(url)

    # Convert QR code to bytes
    qr_io = BytesIO()
    qr.save(qr_io, format="PNG")
    return qr_io.getvalue()

def add_text_to_image(image):
    """Adds 'AVS ENGINEERING COLLEGE' (Top-Centered) and 'ALGOVERSE' (Bottom-Centered) with background labels."""
    image = image.convert("RGB")  # Ensure it's in RGB mode
    draw = ImageDraw.Draw(image)

    # Font Paths
    FONT_DIR = "fonts"
    AVS_FONT_PATH = os.path.join(FONT_DIR, "times.ttf")
    ALGOVERSE_FONT_PATH = os.path.join(FONT_DIR, "impact.ttf")

    # Load fonts
    avs_font = ImageFont.truetype(AVS_FONT_PATH, 30)
    algoverse_font = ImageFont.truetype(ALGOVERSE_FONT_PATH, 20)

    # Image size
    img_width, img_height = image.size

    # 🎯 **AVS ENGINEERING COLLEGE (Top-Center)**
    text_avs = "AVS ENGINEERING COLLEGE"
    padding = 15  # Padding around text

    # Get text bounding box
    text_bbox = draw.textbbox((0, 0), text_avs, font=avs_font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    x_avs = (img_width - text_width) // 2  # Center horizontally
    y_avs = 10  # Top margin

    box_x1 = x_avs - padding
    box_y1 = y_avs - padding
    box_x2 = x_avs + text_width + padding
    box_y2 = y_avs + text_height + padding

    # Draw background rectangle
    draw.rectangle([box_x1, box_y1, box_x2, box_y2], fill="white", outline="black", width=2)
    # Draw text over the background
    draw.text((x_avs, y_avs), text_avs, fill="navy", font=avs_font)

    # 🎯 **ALGOVERSE (Bottom-Center)**
    text_algoverse = "ALGOVERSE'25"  # Using curly apostrophe


    # Get text bounding box
    text_bbox = draw.textbbox((0, 0), text_algoverse, font=algoverse_font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    x_algoverse = (img_width - text_width) // 2  # Center horizontally
    y_algoverse = img_height - text_height - 10  # Move up slightly

    box_x1 = x_algoverse - padding
    box_y1 = y_algoverse - padding
    box_x2 = x_algoverse + text_width + padding
    box_y2 = y_algoverse + text_height + padding

    # Draw background rectangle
    draw.rectangle([box_x1, box_y1, box_x2, box_y2], fill="white", outline="black", width=1)
    # Draw text over the background
    draw.text((x_algoverse, y_algoverse), text_algoverse, fill="navy", font=algoverse_font)

    return image

if captured_image:
    image = Image.open(captured_image).convert("RGB")

    if st.button("Cartoonize"):
        with st.spinner("Processing..."):
            try:
                # Apply Cartoonization
                cartoonized_image = pipeline("Cartoonize the following image", image=image).images[0]

                # 🖌️ **Add Text to Cartoonized Image**
                cartoonized_image_with_text = add_text_to_image(cartoonized_image)

                # Upload to Imgur
                img_url = upload_to_imgur(cartoonized_image_with_text)

                if img_url:
                    # Generate QR code for the Imgur URL
                    qr_code_bytes = generate_qr_code(img_url)

                    # Display cartoonized image with text
                    st.image(cartoonized_image_with_text, caption="Cartoonized Image with Text", use_container_width=True)

                    # Display QR code
                    st.image(qr_code_bytes, caption="Scan to Download", use_container_width=False)

                    st.success(f"Done! Scan the QR code or click [here]({img_url}) to download your image.")

            except Exception as e:
                st.error(f"Error during cartoonization: {e}")
