import hashlib, math, struct
from pathlib import Path

data = Path("test.txt").name.encode()

print(len(data), data[:8])

MIDI_HEADER = b"MThd"
MIDI_TRK = b"MTrk"

header_chunk = MIDI_HEADER + (6).to_bytes(4, "big", signed=False) + (0).to_bytes(2, "big", signed=False) + (1).to_bytes(2, "big", signed=False) + (0).to_bytes(2, "big", signed=False) + (100).to_bytes(2, "big", signed=False)

track_chunk = MIDI_TRK

print(header_chunk)