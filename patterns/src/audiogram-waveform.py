"""Podcast audiogram: still card + live waveform from the audio. The demo synthesises a speech-like test signal
(amplitude-modulated noise with pauses) so the renderer needs no recording and no network."""
import tempfile
from pathlib import Path

from lib import ffmpeg, from_spec, ph


def render(out: Path) -> Path:
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "voice.wav"
        # syllable-rate (~4 Hz) envelope, phrase gaps every ~1.7 s, band-limited like a voice
        ffmpeg("-f", "lavfi", "-i", "anoisesrc=d=4:c=pink:a=1",
               "-af", "volume='0.25+0.75*abs(sin(2*PI*4.1*t))*gt(sin(2*PI*0.6*t),-0.5)':eval=frame,"
                      "highpass=f=120,lowpass=f=3200", str(wav))
        spec = {"kind": "audiogram", "theme": "faceless-story", "show": "Low Tide Radio · ep. 31",
                "title": "Why the harbour bell still rings at noon", "speaker": "with R. Okafor (fictional)",
                "audio": str(wav), "photo": ph("rain"), "focus": [0.5, 0.3], "duration": 4}
        return from_spec("audiogram-waveform", spec, out)
