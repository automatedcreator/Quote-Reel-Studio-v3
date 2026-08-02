# 🎬 Quote Reel Studio v1.0

Generate beautiful Instagram quote reels automatically using an Excel sheet and background videos.

---

## ✨ Features

- 📄 Read quotes from an Excel file
- 🎥 Use one or multiple background videos
- 🖼️ Automatically create quote images
- 🎬 Generate multiple vertical reels
- 📦 Download all generated reels as a ZIP
- 🖥️ Simple Gradio web interface

---

## 📂 Project Structure

```
Quote-Reel-Studio/
│
├── app/
│   ├── ui.py
│   ├── renderer.py
│   ├── typography.py
│   ├── quotes.py
│   ├── config.py
│   ├── animations.py
│   └── themes.py
│
├── quotes/
├── videos/
├── output/
├── assets/
├── main.py
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

```bash
git clone <your-repository-url>
cd Quote-Reel-Studio
pip install -r requirements.txt
```

---

## ▶️ Run

```bash
python -m app.ui
```

---

## 📋 How to Use

1. Launch the application.
2. Upload your Excel file containing quotes.
3. Upload one or more background videos.
4. Click **Submit**.
5. Wait for rendering to finish.
6. Download `reels.zip`.

---

## 📦 Output

Generated reels are saved in:

```
output/
```

A ZIP file containing all reels is also created.

---

## 🛠 Tech Stack

- Python
- MoviePy
- OpenCV
- Pillow
- Pandas
- Gradio

---

## 🔖 Version

**Quote Reel Studio v1.0**

---

## 📄 License

For personal and educational use.