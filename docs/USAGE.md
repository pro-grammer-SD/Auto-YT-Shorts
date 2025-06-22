## 🚀 Command Line Usage Guide

| Flag               | Alias | Description                                                                 |
|--------------------|-------|-----------------------------------------------------------------------------|
| `-make <TOPIC>`    | —     | Generate a short video from the given topic text.                          |
| `-d`               | —     | Delete the existing `media/` folder before generating new content.         |
| `-ow`              | —     | Overwrite the final video output if it already exists.                     |
| `-fr`              | —     | Force render the final video using existing audio/image without regenerating them. |
| `-c`               | —     | Cleanup both `media/` and `output/` directories and exit immediately.      |
| `-h`               | —     | Show help and available commands.                                          |

---

### 💡 Examples

```bash
# Generate a new video for the topic "Importance of Water"
python main.py -make "Importance of Water"

# Force rendering from existing media, skip regeneration
python main.py -make "Importance of Water" -fr

# Delete old media before generating new
python main.py -make "AI vs Humans" -d

# Overwrite the final video even if it exists
python main.py -make "Benefits of Yoga" -ow

# Clean all media and output, then exit
python main.py -c
```

> 📝 Tip: Combine `-ow` and `-d` if you want a completely fresh build every time.
