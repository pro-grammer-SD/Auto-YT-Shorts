import os
from pathlib import Path
from shutil import rmtree
from modules.audio import make_audio
from modules.image import make_image
from modules.text import make_text

media_dir = Path("media")

if media_dir.exists():
    confirm = input("Delete existing `media` folder and all contents? [y/N]: ").strip().lower()
    if confirm == "y":
        rmtree(media_dir)

media_dir.mkdir(exist_ok=True)
os.chdir(media_dir)

topic = input("Enter a COOL topic of your choice _> ")
lines = make_text(topic)
print(lines)

def build_audio(lines):
    audio_dir = Path("audio")
    audio_dir.mkdir(exist_ok=True)
    os.chdir(audio_dir)

    index_count = 1
    for i in lines:
        while True:
            try:
                make_audio(i, index_count)
                index_count += 1
                break
            except Exception as e:
                print(f"An error occurred (audio): {e}")
    os.chdir("..")

def build_images(lines):
    images_dir = Path("images")
    images_dir.mkdir(exist_ok=True)
    os.chdir(images_dir)

    index_count = 1
    for i in lines:
        while True:
            try:
                make_image(i, index_count)
                index_count += 1
                break
            except Exception as e:
                print(f"An error occurred (image): {e}")
    os.chdir("..")

build_audio(lines)
build_images(lines)
