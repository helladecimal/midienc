import hashlib, math, struct
from pathlib import Path
import argparse
import random
import zlib

MIDI_HEADER = b"MThd"
MIDI_TRK = b"MTrk"

def event_enc(data, chan, delta):
    event_data = bytearray()

    event_data.extend([0x00, 0xC0 | chan, random.randint(0, 119)]) 
    
    for i in range(0, len(data)):

        pitch = (data[i]) & 0x7f
        vel = (data[i] >> 7) & 0x01

        vel = vel if vel == 1 else 32

        event_data.extend([
            1,
            0x90 | chan,
            pitch,
            vel * 64 if vel == 1 else vel
        ])
        

        event_data.extend([
            delta,
            0x80 | chan,
            pitch,
            0x00
        ])

        print(f"encoding track {chan+1}: {int( (i/len(data)) * 100)}% done", end="\r")
    
    print("")
    event_data.extend([0x00, 0xFF, 0x2F, 0x00])

    event_data = bytes(event_data)

    event_len = len(event_data)
    return event_data, event_len


def decode(file_data):
    # 4 byte header + 4 length + 2 format + 2 tracks + 2 div + 4 ascii + 4 byte
    tracks = int.from_bytes(file_data[10:12], "big", signed=False)
    #event_data = file_data[22:]
    #event_data = event_data[3:len(event_data)-4] # program change, 4 byte eof
    event_data = bytearray()
    decoded_data = bytearray()

    trk_start = 14
    for i in range(tracks):
        length = int.from_bytes(file_data[trk_start+4:trk_start+8], "big", signed=False)
        event_data.extend(
            file_data[trk_start+11:trk_start+4+length]
        )
        trk_start += 8+length



    for i in range(0, len(event_data), 4):

        if i+3 >= len(event_data):
            break

        note_stat = (event_data[i+1])
        pitch = (event_data[i+2])
        vel = (event_data[i+3])

        bit8 = 1 if vel > 32 else 0

        if (note_stat & 0xF0) == 0x90: # note on for any channel
            decoded_data.append((pitch | (bit8 << 7)))

        print(f"decoding: {int((i/len(file_data)) * 100)}% done", end="\r")
    print("")
    decoded_data = bytes(decoded_data)

    #decoded_data = zlib.decompress(decoded_data)
    try:
        decoded_data = zlib.decompress(decoded_data)
    except zlib.error:
        decoded_data = decoded_data
    return decoded_data

def encode(file_data, inst, delta):

    header_chunk = (
        MIDI_HEADER +
        (6).to_bytes(4, "big", signed=False) + # length
        (0 if inst <= 1 else 1).to_bytes(2, "big", signed=False) + # format
        (inst).to_bytes(2, "big", signed=False) + # tracks
        (200).to_bytes(2, "big", signed=False) # ticks per beat
    )

    file_data = zlib.compress(file_data, 9)

    total_track = b""

    split_data = []

    if inst > 1:
        div = len(file_data) // inst
        for i in range(0, inst):
            end = (i+1)*div if i < inst-1 else len(file_data)
            split_data.append(file_data[i*div:end])
    else:
        split_data.append(file_data)

    for i in range(len(split_data)):

        data_seg = split_data[i]

        event_data, event_len = event_enc(data_seg, i, delta)
        
        track_chunk = (
            MIDI_TRK +
            (event_len).to_bytes(4, "big", signed=False) +
            event_data 
        )

        total_track += track_chunk

    return header_chunk + total_track

def convert(file, output, inst, delta):
    midi = encode(file.read_bytes(), inst, delta)
    if not output:
        new = file.name
    else:
        new = output.name

    with open(f"{new}.mid", "wb") as f:
        f.write(midi)
    print("done converting")

def revert(file, output):
    data = decode(file.read_bytes())

    if not output:
        new = file.name[:-4] # remove .mid
    else:
        new = output.name

    with open(f"{new}", "wb") as f:
        f.write(data)
    print("done reverting")

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("file", type=Path)
    parser.add_argument("-e", "--encode", action="store_true")
    parser.add_argument("-d", "--decode", action="store_true")
    parser.add_argument("-o", "--output", type=Path)
    parser.add_argument("-I", "--inst", type=int)
    parser.add_argument("-l", "--delta", type=int)

    args = parser.parse_args()

    if args.file and args.file.exists():
        if args.encode:
            inst = args.inst if args.inst else 1
            delta = args.delta if args.delta else 5

            inst = 65535 if inst > 65535 else inst

            convert(args.file, args.output, inst, delta)
        if args.decode:
            if args.file.name[-4:] == ".mid":
                revert(args.file, args.output)
            else:
                print("file is not a midi file")
    else:
        print("invalid file")

if __name__ == "__main__":
    main()