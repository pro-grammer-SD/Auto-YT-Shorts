import os
from pathlib import Path
import re
from moviepy import (
    ImageClip, AudioFileClip, CompositeVideoClip, TextClip, concatenate_videoclips
)
from rich.console import Console
from rich.progress import track

console = Console()

def make_video(subtitle_text="Clip", overwrite=False):
    root_dir = Path(__file__).resolve().parent
    if Path("audio").exists() and Path("images").exists():
        root_dir = Path.cwd().parent
    media_path = root_dir / "media"
    audio_path = media_path / "audio"
    image_path = media_path / "images"
    video_path = media_path / "video"
    output_path = root_dir / "output"
    font_path = root_dir / "fonts" / "font.otf"

    video_path.mkdir(parents=True, exist_ok=True)
    output_path.mkdir(parents=True, exist_ok=True)

    audio_indices = {
        int(re.search(r"output_(\d+)\.mp3", f.name).group(1))
        for f in audio_path.glob("output_*.mp3")
        if re.search(r"output_(\d+)\.mp3", f.name)
    }

    image_indices = {
        int(re.search(r"image_(\d+)\.png", f.name).group(1))
        for f in image_path.glob("image_*.png")
        if re.search(r"image_(\d+)\.png", f.name)
    }
    
    common_indices = sorted(audio_indices & image_indices)
    if not common_indices:
        console.print("[bold red]❌ No matching audio/image pairs found.[/bold red]")
        return

    clips = []
    for i in track(common_indices, description="🎞️ Creating test clips"):
        try:
            audio = AudioFileClip(str(audio_path / f"output_{i}.mp3"))
            img = ImageClip(str(image_path / f"image_{i}.png")).resized(height=1920)
            img = img.with_background_color(size=(1080, 1920), color=(0, 0, 0), pos="center")
            img = img.with_audio(audio).with_duration(audio.duration)

            subtitle = TextClip(
                text=subtitle_text,
                font=str(font_path),
                font_size=60,
                color="white",
                method="caption",
                size=(1000, None)
            ).with_duration(audio.duration).with_position(("center", "bottom"))
            
            clip = CompositeVideoClip([img, subtitle], size=(1080, 1920))
            clip.write_videofile(str(video_path / f"clip_{i}.mp4"), fps=30, audio_codec="aac", threads=4, preset="ultrafast", logger=None)
            clips.append(clip)
        except Exception as e:
            console.print(f"[red]Error on clip {i} → {e}[/red]")

    final_path = output_path / "final_video.mp4"
    if final_path.exists() and not overwrite:
        console.print(f"[yellow]⚠️ Output already exists: {final_path}. Skipping final merge.[/yellow]")
        return

    if clips:
        final = concatenate_videoclips(clips, method="compose")
        final.write_videofile(str(final_path), fps=30, audio_codec="aac", threads=4, preset="ultrafast")
        console.print(f"[green]✅Final video saved at {final_path}. Opening it...[/green]")
        os.startfile(final_path)
    else:
        console.print("[red]❌ No clips were created.[/red]")

if __name__ == "__main__":
    make_video()
