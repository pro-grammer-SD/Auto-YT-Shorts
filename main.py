import os
import argparse
from pathlib import Path
from shutil import rmtree
from rich.console import Console
from rich.panel import Panel

from modules.audio import make_audio
from modules.image import make_image
from modules.text import make_text
from modules.video import make_video

console = Console()

def build_audio(lines):
    audio_dir = Path("audio")
    audio_dir.mkdir(exist_ok=True)
    os.chdir(audio_dir)
    index_count = 1
    for line in lines:
        while True:
            try:
                make_audio(line, index_count)
                index_count += 1
                break
            except Exception as e:
                console.print(f"[red]Audio error:[/red] {e}")
    os.chdir("..")

def build_images(lines):
    images_dir = Path("images")
    images_dir.mkdir(exist_ok=True)
    os.chdir(images_dir)
    index_count = 1
    for line in lines:
        while True:
            try:
                make_image(line, index_count)
                index_count += 1
                break
            except Exception as e:
                console.print(f"[red]Image error:[/red] {e}")
    os.chdir("..")

def cleanup_and_exit():
    for folder in ["media", "output"]:
        path = Path(folder)
        if path.exists():
            rmtree(path)
            console.print(f"[red]🧹 Deleted: {folder}/[/red]")
    console.print("[bold green]✅ Cleanup complete. Exiting...[/bold green]")
    exit()

def main():
    parser = argparse.ArgumentParser(description="Auto YT Shorts Generator", add_help=False)
    parser.add_argument("-make", metavar="TOPIC", type=str, help="Generate short for a given topic")
    parser.add_argument("-d", "--delete", action="store_true", help="Delete existing media folder")
    parser.add_argument("-ow", "--overwrite", action="store_true", help="Overwrite final output video if exists")
    parser.add_argument("-fr", "--forcerender", action="store_true", help="Force render without regenerating media")
    parser.add_argument("-c", "--cleanup", action="store_true", help="Clean up media and output folders and quit")
    parser.add_argument("-h", "--help", action="help", help="Show this help message and exit")

    args = parser.parse_args()

    if args.cleanup:
        cleanup_and_exit()

    if not args.make:
        console.print("[bold yellow]💡 Use:[/bold yellow] python main.py -make \"Your topic here\" [-d] [-ow] [-fr] [-c]")
        return

    media_dir = Path("media")
    if args.delete and media_dir.exists():
        console.print("[bold red]🗑️ Deleting existing media folder...[/bold red]")
        rmtree(media_dir)

    media_dir.mkdir(exist_ok=True)
    os.chdir(media_dir)

    topic = args.make

    audio_ready = Path("audio").exists() and any(Path("audio").glob("*.mp3"))
    images_ready = Path("images").exists() and any(Path("images").glob("*.png"))

    if not (args.forcerender or args.overwrite):
        lines = make_text(topic)
        console.print(Panel.fit("\n".join(lines), title=f"📜 Generated Lines for: {topic}", border_style="cyan"))
    else:
        lines = []

    if not audio_ready and not args.forcerender:
        build_audio(lines)

    if not images_ready and not args.forcerender:
        build_images(lines)

    final_output = Path("..") / "output" / "final_video.mp4"

    if final_output.exists() and not args.overwrite:
        console.print(f"[yellow]⚠️ Final video exists: '{final_output}'. Use --overwrite to regenerate.[/yellow]")
        return

    if Path("audio").exists() and Path("images").exists():
        audio_indices = {
            int(f.stem.split("_")[1])
            for f in Path("audio").glob("output_*.mp3")
            if f.stem.split("_")[1].isdigit()
        }

        image_indices = {
            int(f.stem.split("_")[1])
            for f in Path("images").glob("image_*.png")
            if f.stem.split("_")[1].isdigit()
        }

        matched = sorted(audio_indices & image_indices)

        if matched:
            console.print("[bold green]🎬 Rendering final video...[/bold green]")
            success = make_video(subtitle_text=topic, overwrite=args.overwrite)
            if success:
                console.print("[bold green]✅ Build successful![/bold green]")
            else:
                console.print("[bold red]❌ Build failed during video rendering.[/bold red]")
        else:
            console.print("[bold red]❌ No matching audio/image pairs found. Cannot render.[/bold red]")
    else:
        console.print("[bold red]❌ Audio or images folder is missing.[/bold red]")

if __name__ == "__main__":
    main()
