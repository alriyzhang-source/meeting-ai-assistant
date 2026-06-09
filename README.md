# Meeting AI Assistant

A real-time AI assistant for online meetings (Tencent Meeting). It captures audio, recognizes speech, detects questions, and generates answers based on your reference materials.

## Features

- Real-time audio capture from Tencent Meeting via VB-Cable
- Chinese speech recognition using Vosk
- Automatic question detection
- AI-powered answer generation using MiMo API
- Private display window (visible only to you during screen sharing)

## Requirements

- Windows 10/11
- Python 3.8+
- NVIDIA GPU (optional, for faster processing)
- VB-Audio Virtual Cable
-  API key

## Installation

1. Install VB-Audio Virtual Cable from https://vb-audio.com/Cable/

2. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/meeting-ai-assistant.git
cd meeting-ai-assistant
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Download the Vosk Chinese model:
```bash
python -c "
import urllib.request, zipfile, os
url = 'https://alphacephei.com/vosk/models/vosk-model-small-cn-0.22.zip'
urllib.request.urlretrieve(url, 'vosk-model-small-cn.zip')
with zipfile.ZipFile('vosk-model-small-cn.zip', 'r') as z:
    z.extractall('.')
os.rename('vosk-model-small-cn-0.22', 'vosk-model-cn')
os.remove('vosk-model-small-cn.zip')
"
```

5. Configure your API key in `config.py`:
```python
CLAUDE_API_KEY = "your-mimo-api-key"
```

6. Place your reference materials (PDF, DOCX, PPTX, TXT) in the `materials/` folder.

## Audio Setup

1. Open Tencent Meeting settings
2. Set Speaker to **CABLE Input**
3. Set Microphone to your built-in microphone (not AirPods)
4. In Windows Sound Settings:
   - Go to Recording devices
   - Right-click **CABLE Output** → Properties
   - Enable **Listen** and set output to your headphones/speakers

## Usage

```bash
python main.py
```

A floating window will appear showing:
- Detected questions from the meeting
- AI-generated answers based on your materials

Press `Ctrl+C` to stop.

## Project Structure

```
meeting-ai-assistant/
├── main.py              # Entry point
├── config.py            # Configuration
├── audio_capture.py     # Audio capture module
├── transcriber.py       # Speech recognition (Vosk)
├── ai_responder.py      # AI answer generation
├── ui.py                # GUI display
├── requirements.txt     # Python dependencies
└── materials/           # Your reference documents
```

## License

MIT
