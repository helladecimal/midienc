import hashlib, math, struct
from pathlib import Path

MIDI_HEADER = b"MThd"
MIDI_TRK = b"MTrk"

def event_enc(data):
    event_data = b""

    for i in range(0, len(data)-1):
        print(hex(data[i]))
        event_data = event_data + (1).to_bytes(2, "big", signed=False) + b"\x90" + int(data[i]).to_bytes(2, "big", signed=False) + int(data[i+1]).to_bytes(2, "big", signed=False)
        event_data = event_data + (1).to_bytes(2, "big", signed=False) + b"\x80" + int(data[i]).to_bytes(2, "big", signed=False) + b"\x00"

    return event_data

def encode(file_data):

    event_data = event_enc(file_data)

    header_chunk = MIDI_HEADER + (6).to_bytes(4, "big", signed=False) + (0).to_bytes(2, "big", signed=False) + (1).to_bytes(2, "big", signed=False) + (0).to_bytes(2, "big", signed=False) + (100).to_bytes(2, "big", signed=False)

    track_chunk = MIDI_TRK + len(event_data).to_bytes(4, "big", signed=False) + event_data

    return header_chunk + track_chunk



file = Path("test.txt")
midi = encode(file.read_bytes())

with open(f"{file.name}.mid", "wb") as f:
    f.write(midi)