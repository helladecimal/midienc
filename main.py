import hashlib, math, struct
from pathlib import Path

MIDI_HEADER = b"MThd"
MIDI_TRK = b"MTrk"

def event_enc(data):
    print(hex(data[1]))
    event_data = b""

    for i in range(0, len(data)-1):
        print(hex(data[i]))
        event_data = event_data + (1).to_bytes(2, "big", signed=False) + b"\x90" + data[i] + data[i+1]
        event_data = event_data + (1).to_bytes(2, "big", signed=False) + b"\x80" + data[i] + b"\x00"

    print(event_data)

def encode(file_data):

    event_data = event_enc(file_data)

    header_chunk = MIDI_HEADER + (6).to_bytes(4, "big", signed=False) + (0).to_bytes(2, "big", signed=False) + (1).to_bytes(2, "big", signed=False) + (0).to_bytes(2, "big", signed=False) + (100).to_bytes(2, "big", signed=False)

    track_chunk = MIDI_TRK + len(file_data).to_bytes(4, "big", signed=False)

file = Path("test.txt").read_bytes()
encode(file)