import traceback
import sys

print("Python version:", sys.version)
try:
    from faster_whisper import WhisperModel
    print("Imported WhisperModel successfully.")
    m = WhisperModel("tiny", device="cpu", compute_type="int8")
    print("Loaded tiny model successfully!")
except Exception as e:
    print("Caught Exception:", type(e), e)
    traceback.print_exc()
