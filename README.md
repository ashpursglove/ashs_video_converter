# Ash’s Video Converter
### A wildly over-engineered GUI wrapper for FFmpeg, built because remembering FFmpeg flags is a form of suffering.

---
![Uploading image.png…]()

## What Is This?

**Ash’s Video Converter** is a dark-themed desktop app built with PyQt5 that lets you convert videos without:
- Googling FFmpeg syntax
- Copy-pasting commands from Stack Overflow
- Whispering “please don’t crash” into a terminal window

It exists for people who:
- Know FFmpeg is powerful
- Know FFmpeg is correct
- Still absolutely refuse to type ffmpeg -i input.mp4 -vf scale=1280:720 -c:v libx264 -preset medium -crf 23 -movflags +faststart output_FINAL_v7_REAL.mp4

This tool is the shortcut you earned.

---

## Yes, There’s Also an EXE

There is a **pre-built Windows EXE** included in this repository.

This is for:
- People who want the tool to just open
- People who are done fighting Python environments
- People on Windows who value their remaining patience

Using the EXE is:
- Technically cheating
- Socially frowned upon by “build it yourself” purists
- Deeply convenient in the real world

**OGs build from source.**  
They will also tell you they built from source.

Everyone else double-clicks the EXE, converts their videos, and moves on with their life.

Both paths work.  
One just comes with fewer opinions.

---

## What It Does

It lets you:

- Convert basically any video format FFmpeg can read  
  (which is everything except maybe cursed files from 1998)
- Change resolution with a single click
- Pick a sane output format
- Rename the output file like a functioning adult
- Watch real progress instead of guessing if FFmpeg died
- See FFmpeg’s internal monologue scrolling past in real time
- Enjoy a dark navy theme and feel like you’re doing serious work

In short:  
All the power of FFmpeg.  
None of the typing.

---

## Features (The Good Stuff)

### Accepts Pretty Much Any Input Video
If FFmpeg can open it, this app will try.

avi, mov, mp4, mkv, webm, flv, something your camera invented in 2006.  
No judgement.  
Just results.

---

### Choose Your Output Format
Pick from:
- mp4
- mkv
- mov
- avi
- webm

Convert your video into a format that:
- Your editor actually likes
- Your phone will play
- Your client won’t complain about

---

### Resolution Presets That Make Sense
From “looks good everywhere” to “why is this so small”:

- 1920×1080
- 1280×720
- 854×480
- 640×360
- 426×240

No aspect-ratio guesswork.  
No calculator required.

---

### Custom Output File Names
You choose the name.

No more:
- Untitled.mp4
- output_final.mp4
- output_final_v2.mp4
- output_final_v2_EDIT.mp4
- output_final_v2_EDIT_REALFINAL.mp4

You’re better than that now.

---

### Real Progress Bar
This is not a fake spinner.

The app uses FFmpeg and ffprobe timecodes to show:
- Actual progress
- Actual status
- Actual reassurance that something is happening

Your anxiety levels will noticeably drop.

---

### Full FFmpeg Log Window
See exactly what FFmpeg is doing in real time.

Useful for:
- Debugging
- Learning
- Pretending you’re in a cyberpunk movie
- Watching walls of text scroll by and feeling productive

---

### Dark Navy Theme
- Easy on the eyes
- Looks professional
- Hides minor life regrets

You can absolutely leave this open during meetings.

---

## Requirements

- Python 3.8+
- PyQt5
- FFmpeg installed and available in PATH

If FFmpeg doesn’t run from your terminal, this app cannot summon it magically.

---

## Installation

- Clone or download the repository
- Install PyQt5
- Make sure FFmpeg works
- Run the app

Or:
- Double-click the EXE
- Ignore the distant screaming of GitHub purists
- Convert your videos

---

## Running the App

Run the Python script.

The window opens.  
You select a video.  
You click convert.  
Things happen.

A truly radical workflow.

---

## Final Thoughts

This project exists because:
- Typing FFmpeg commands builds character
- But pressing a button builds happiness

Also because it’s apparently easier to spend hours building a GUI than to remember a handful of command-line flags.

If this tool saved you even one “why is this upside down and green” moment, then it has fulfilled its purpose.

---

Enjoy converting.  
No terminal trauma required.
