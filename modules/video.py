from pathlib import Path
import re
from moviepy import (
    ImageClip, AudioFileClip, CompositeVideoClip, TextClip, concatenate_videoclips
)

media_path = Path().cwd()
audio_path = media_path / "media" / "audio"
image_path = media_path / "media" / "images"
font_path = media_path / "fonts" / "font.otf"

audio_indices = {
    int(re.search(r"output_(\d+).mp3", f.name).group(1))
    for f in audio_path.glob("output_*.mp3")
    if re.search(r"output_(\d+).mp3", f.name)
}

image_indices = {
    int(re.search(r"image_(\d+).png", f.name).group(1))
    for f in image_path.glob("image_*.png")
    if re.search(r"image_(\d+).png", f.name)
}

print("Audio found:", sorted(audio_indices))
print("Image found:", sorted(image_indices))
common_indices = sorted(audio_indices & image_indices)

if not common_indices:
    raise RuntimeError("No matching audio/image pairs found.")

clips = []

for i in common_indices:
    audio_file = audio_path / f"output_{i}.mp3"
    image_file = image_path / f"image_{i}.png"

    print(f"Using image_{i}.png + output_{i}.mp3")

    audio = AudioFileClip(str(audio_file))
    image = ImageClip(str(image_file)).with_duration(audio.duration).with_audio(audio)
    image = image.resized(height=1920).with_position("center").resized(width=1080)

    subtitle = TextClip(
        text=f"Clip {i}",
        font=str(font_path),
        color="white",
        bg_color="black",
        size=(1080, None),
        method="label",
    ).with_position(("center", "bottom")).with_duration(audio.duration)
    
    video = CompositeVideoClip([image, subtitle], size=(1080, 1920))
    clips.append(video)

final_video = concatenate_videoclips(clips, method="compose")
final_video.write_videofile("final_video.mp4", fps=50, audio_codec="aac")
