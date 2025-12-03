# **Ash's Video Converter**  
*A gloriously over-engineered GUI wrapper for FFmpeg, handcrafted in Python with love.*

---

## 🎬 What Is This?

**Ash’s Video Converter** is a slick, dark-themed desktop application built with PyQt5 that lets you:

- Convert *any* video format (as long as FFmpeg can read it, which is basically everything except microwave dinners)
- Change resolution with one click
- Choose your desired output file format  
  *(mp4, mkv, mov, avi, webm—because variety is the spice of life)*
- Give your output file a custom name  
  *(say goodbye to “Untitled_1_FINAL_v3_EDITED_FIXED_REALFINAL.mp4”)*
- Watch the conversion progress with a real progress bar
- Spy on FFmpeg’s inner thoughts with a scrolling log window
- Enjoy a slick, dark navy theme and pretend you're hacker man! 

This is the “I’m too lazy to remember FFmpeg arguments” tool we all need.

---

## ✨ Features

### 🔍 **Accepts Any Input Video Format**
If FFmpeg can read it, this GUI can handle it.  
.avi? .mov? .mk4? .flv? Some obscure container from 2004?  
Yep. Bring it on.

### 🧩 **Pick Your Output Format**
Choose between:

- **mp4**
- **mkv**
- **mov**
- **avi**
- **webm**

Convert your shaky phone video into something your editing software actually likes.

### 🖌️ **Choose Your Resolution**
From glorious Full HD to "why does this look like it was filmed with a potato":

- 1920×1080  
- 1280×720  
- 854×480  
- 640×360  
- 426×240

### ✏️ **Custom Output File Name**
Name it whatever you want.  
You’re in control.  
You’re powerful.  
You’ve always been powerful.

### 📊 **Progress Bar + Status Updates**
No more staring at a terminal wondering whether something is happening or whether FFmpeg has died again.  
This GUI tracks real conversion progress using ffprobe + ffmpeg timecodes.

### 📜 **Full Log Window**
See *everything* FFmpeg says in real time.  
Useful for debugging…  
…or for pretending you’re in a cyberpunk thriller.

### 🎨 **Dark Navy Theme**
Your retinas will thank you.  
Cool, modern, professional, and just a little bit moody.

---

## 🛠️ Requirements

- **Python 3.8+**
- **PyQt5**  
  ```bash
  pip install PyQt5
FFmpeg installed and visible in PATH

Windows users: add ffmpeg/bin to your PATH

macOS users: brew install ffmpeg

Linux users: you know what you’re doing

## 📦 Installation
Clone or download this repository

Install the requirements:

bash
Copy code
pip install PyQt5
Ensure FFmpeg is working:

bash
Copy code
ffmpeg -version
Run the app:

bash
Copy code
python ash_video_converter.py
Boom. You're in.


## ❤️ Final Thoughts
This project exists because manually typing FFmpeg commands is character-building,
but sometimes you just want to press a button and feel like royalty.

If this made your life easier, even once, it has served its noble purpose.

Enjoy converting! 🎥🍿
