import hashlib, math, struct
from pathlib import Path

MIDI_HEADER = b"MThd"
MIDI_TRK = b"MTrk"

def event_enc(data):
    event_data = b""
    
    for i in range(0, len(data)-1):
        print(hex(data[i]))
        event_data = (
            event_data + 
            (1).to_bytes(1, "big", signed=False) + 
            b"\x90" + 
            (data[i]).to_bytes(1, "big", signed=False) + 
            (data[i+1]).to_bytes(1, "big", signed=False)
        )

        event_data = (
            event_data + 
            (1).to_bytes(1, "big", signed=False) + 
            b"\x80" + 
            (data[i]).to_bytes(1, "big", signed=False) + 
            b"\x00"
        )

    event_data = event_data + b"\xFF\x2F\x00"

    event_len = len(event_data)
    return event_data, event_len

def encode(file_data):

    event_data, event_len = event_enc(file_data)

    header_chunk = (
        MIDI_HEADER + 
        (6).to_bytes(4, "big", signed=False) + 
        (0).to_bytes(2, "big", signed=False) + 
        (1).to_bytes(2, "big", signed=False) + 
        (100).to_bytes(2, "big", signed=False)
    )
    
    track_chunk = (
        MIDI_TRK + 
        (event_len).to_bytes(4, "big", signed=False) + 
        event_data 
    )

    return header_chunk + track_chunk

def decode(file_data):
    # 4 byte header + 4 length + 6 format + 4 ascii + 4 byte
    event_data = file_data[22:]
    print(event_data)


def convert(file):
    file = Path("test.txt")
    midi = encode(file.read_bytes())

    with open(f"{file.name}.mid", "wb") as f:
        f.write(midi)

def revert(file):
    file = Path("test.txt.mid")
    decode(file.read_bytes())