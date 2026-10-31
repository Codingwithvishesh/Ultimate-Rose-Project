# A Rose For You 🌹

Python + Matplotlib se bana 3D math-rose animation. Rose dheere-dheere khulti hai
(yellow wireframe → pink surface) aur camera uske around ghoomta hai.

## Formulas

- φ(θ) = (π/2) · e^(−θ / 8π)
- X(θ) = 1 − ½ · ( (5/4) · (1 − (θ mod 2π) / π)² − ¼ )²
- (x, y, z) = ( r sinθ, r cosθ, X(θ) · (x cosφ − y sinφ) )

## Requirements

- Python 3.8+
- numpy, matplotlib
- ffmpeg (sirf video save karne ke liye)

## Install

```bash
pip install numpy matplotlib
```

ffmpeg install:

- Windows: `winget install ffmpeg` (ya https://ffmpeg.org se download)
- Mac: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

## Run

**Recommended (smooth):** pehle video banao, phir `rose.mp4` ko play karo.

```bash
python rose.py --save     # rose.mp4 banayega (720x1280, 16 sec, 30 FPS)
```

Render me kuch minute lagte hain (progress dikhta rahega). Video hamesha smooth chalegi
aur seedha Reels me use ho sakti hai.

Dusre options:

```bash
python rose.py            # live window (Matplotlib 3D slow hai, atak sakta hai)
python rose.py --png      # rose.png (ek image)
```

## Settings badalna

`rose.py` ke upar ye values change kar sakte ho:

| Setting | Matlab |
|---|---|
| `FPS` | frames per second |
| `DURATION` | video ki length (seconds) |
| `GROW_FRAMES` | rose kitni der me khulegi |
| `PINK`, `YELLOW` | colors |
| `N_THETA`, `N_R` | surface ki quality (zyada = smooth, par slow) |
