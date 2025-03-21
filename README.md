# 🎨 AI Cartoon Image Generator

## 📌 Overview
The **AI Cartoon Image Generator** is a Streamlit-based web application that converts real-world images into high-quality cartoonized versions using **Stable Diffusion InstructPix2Pix**. This project allows users to capture or upload an image, apply a cartoon filter, and download the transformed output with additional text overlays.

## ✨ Features
- 🖼️ **Real-time image capture** – Use your webcam to take a photo.
- 🎭 **AI-powered Cartoonization** – Converts images into cartoon versions using Stable Diffusion.
- 📝 **Custom Text Overlays** – Adds institute branding (`AVS ENGINEERING COLLEGE`) and event name (`ALGOVERSE'25`).
- ☁️ **Cloud Upload & QR Code Generation** – Images are uploaded to Imgur, and a QR code is generated for easy downloads.
- ⚡ **Optimized for Speed** – Uses **GPU acceleration** if available.

## 🚀 Tech Stack
- **Python**
- **Streamlit** (Web UI)
- **Stable Diffusion InstructPix2Pix** (Image transformation)
- **PyTorch** (Deep Learning)
- **Imgur API** (Image hosting)
- **QR Code Generation** (For download link)

## 🛠 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/ai-cartoon-image-generator.git
cd ai-cartoon-image-generator


2️⃣ Install Dependencies
Make sure you have Python 3.8+ installed, then run:

bash
Copy
Edit
pip install -r requirements.txt
3️⃣ Set Up Environment Variables
Create a .env file and add your Imgur Client ID:

ini
Copy
Edit
IMGUR_CLIENT_ID=your_client_id_here
4️⃣ Run the Application
bash
Copy
Edit
streamlit run ui.py
🖥️ Usage
Launch the app in your browser.
Take a photo or upload an image.
Click "Cartoonize" to process the image.
Download the final image or scan the QR code.
📷 Sample Output

🏆 Credits
Developed by: Your Name
Model Used: Stable Diffusion InstructPix2Pix
Inspiration: Enhancing AI-powered digital art
🤝 Contributing
Pull requests are welcome! If you'd like to add new features, open an issue first to discuss your idea.

📜 License
This project is licensed under the MIT License.

🔥 Transform your images into cartoons instantly with AI! 🚀
