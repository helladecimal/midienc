
<div align="center" style="text-align: center;">
    <h1>midi-enc</h1>
    <div style="display:flex; gap: 10px; align-items:center; justify-content:center;">
        <img src="img/screenshot.png" height="200">
        <video height="200" controls>
            <source src="img/demo.mp4" type="video/mp4">
        </video>
    </div>
    <p>convert any file type into a midi file with one simple trick</p>
</div>

> [!NOTE]  
> midi files generated with this program *may* not run on certain midi players

> [!NOTE]  
> this is not compression by any means.  
> generated files can be way bigger than the original.   
> demo file increased by 9x (1.1 mb -> 8.99 mb)

## how to install

### run file
1. download the `main.py` file
2. run `python main.py` with flags and args

### download executable
1. download the midi-enc executable in releases
2. run `midi-enc` with flags and args

### build
1. clone this repository
2. run `pip install -e .`
2. run `midi-enc` with flags and args

## usage

### file -> .mid
```
midi-enc -e (file)
```

### .mid -> file
```
midi-enc -d (midi)
```

## compatibility

<div align="center">
<h3><i>compatibility does not guarantee fast loading or playback</i></h3>
<p>✅: yes ❔: idk ❌: no</p>

| platform | compatibility |  
|----------|---------------|
| midis2jam2 | ✅ (on the latest version)
| most web players | ✅
| midijam | ❔
| VLC | ❔
|windows media player| ❌|  
</div>


<hr>
<div align="right"><i>made for hack club's <a href="https://crescent.hackclub.com/">crescent</a> </i></div>
