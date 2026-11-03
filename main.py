import hashlib, math, struct
from pathlib import Path

MIDI_HEADER = b"MThd"
MIDI_TRK = b"MTrk"

def event_enc(data):
    event_data = b""
    
    for i in range(0, len(data)-1):
        print(hex(data[i]))
        event_data = event_data + (1).to_bytes(2, "big", signed=False) + b"\x90" + (data[i]).to_bytes(2, "big", signed=False) + int(data[i+1]).to_bytes(2, "big", signed=False)
        event_data = event_data + (1).to_bytes(2, "big", signed=False) + b"\x80" + (data[i]).to_bytes(2, "big", signed=False) + b"\x00"

    event_len = len(event_data)
    print(event_len)
    return event_data, event_len

def encode(file_data):

    event_data, event_len = event_enc(file_data)

    header_chunk = MIDI_HEADER + (6).to_bytes(4, "big", signed=False) + (0).to_bytes(2, "big", signed=False) + (1).to_bytes(2, "big", signed=False) + (0).to_bytes(2, "big", signed=False) + (100).to_bytes(2, "big", signed=False)

    track_chunk = MIDI_TRK + (event_len).to_bytes(4, "big", signed=False) + event_data

    print(track_chunk)

    return header_chunk + track_chunk + b"\xFF" + b"\x2F" + b"\x00"



file = Path("test.txt")
midi = encode(file.read_bytes())

with open(f"{file.name}.mid", "wb") as f:
    f.write(midi)