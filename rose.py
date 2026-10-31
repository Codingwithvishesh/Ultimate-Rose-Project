"""
A Rose For You - 3D math rose animation (Python + Matplotlib)

Run:
    pip install numpy matplotlib
    python rose.py            # live window (slow/atak sakta hai)
    python rose.py --save     # rose.mp4 banayega - YE RECOMMENDED HAI (ffmpeg chahiye)
    python rose.py --png      # sirf ek image rose.png save karega
"""
import sys
import numpy as np
import matplotlib
if "--save" in sys.argv or "--png" in sys.argv:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

# ---------------- Settings ----------------
FPS = 30
DURATION = 16            # seconds
TOTAL_FRAMES = FPS * DURATION
GROW_FRAMES = FPS * 5    # pehle 5 sec me rose khulti hai

N_THETA = 481            # petal direction me resolution
N_R = 28                 # center se edge tak resolution
THETA_MAX = 20 * np.pi   # kitne "turns" tak petals bante hain

PINK = "#ff2d55"
YELLOW = "#f5c542"
TEXT_RED = "#e8344f"
TEXT_GOLD = "#e0a96d"


# ---------------- Rose maths ----------------
def build_rose(theta_max):
    """Rose surface ke X, Y, Z points return karta hai (theta 0 -> theta_max)."""
    n = max(int(N_THETA * theta_max / THETA_MAX), 8)
    theta = np.linspace(0, theta_max, n)[:, None]        # (n, 1)
    r = np.linspace(0, 1, N_R)[None, :]                  # (1, N_R)

    phi = (np.pi / 2) * np.exp(-theta / (8 * np.pi))
    X = 1 - 0.5 * ((5 / 4) * (1 - (3.6 * theta % (2 * np.pi)) / np.pi) ** 2 - 0.25) ** 2

    # petal ki profile (x = r, y = petal curve)
    y = 1.95653 * r**2 * (1.27689 * r - 1) ** 2
    R = X * (r * np.sin(phi) + y * np.cos(phi))

    xs = R * np.sin(theta)
    ys = R * np.cos(theta)
    zs = X * (r * np.cos(phi) - y * np.sin(phi))
    return xs, ys, zs


# ---------------- Figure setup ----------------
fig = plt.figure(figsize=(7.2, 12.8), dpi=100, facecolor="black")
ax = fig.add_axes([0.0, 0.22, 1.0, 0.62], projection="3d", facecolor="black")
ax.set_axis_off()
LIM = 0.8
ax.set_xlim(-LIM, LIM)
ax.set_ylim(-LIM, LIM)
ax.set_zlim(-LIM, LIM)
ax.set_box_aspect((1, 1, 1))

fig.text(0.5, 0.91, "A Rose For You", ha="center", va="center",
         fontsize=36, color=TEXT_RED, family="serif")
fig.text(0.5, 0.17, r"$\varphi(\theta)=\frac{\pi}{2}\,e^{-\theta/8\pi},$",
         ha="center", color=TEXT_GOLD, fontsize=15)
fig.text(0.5, 0.115,
         r"$X(\theta)=1-\frac{1}{2}\left(\frac{5}{4}\left(1-\frac{\theta\ \mathrm{mod}\ 2\pi}{\pi}\right)^{2}-\frac{1}{4}\right)^{2},$",
         ha="center", color=TEXT_GOLD, fontsize=15)
fig.text(0.5, 0.06,
         r"$(x,y,z)=(r\sin\theta,\ r\cos\theta,\ X(x\cos\varphi-y\sin\varphi))$",
         ha="center", color=TEXT_RED, fontsize=15)


def shaded_colors(xs, ys, zs, alpha):
    """Halki lighting: petals ke beech depth dikhane ke liye."""
    P = np.stack([xs, ys, zs], axis=-1)
    du = np.gradient(P, axis=0)
    dv = np.gradient(P, axis=1)
    nrm = np.cross(du, dv)
    nrm /= (np.linalg.norm(nrm, axis=-1, keepdims=True) + 1e-9)
    light = np.array([0.4, 0.3, 0.85])
    light /= np.linalg.norm(light)
    k = 0.72 + 0.28 * np.abs(nrm @ light)
    base = np.array(matplotlib.colors.to_rgb(PINK))
    rgb = np.clip(base * k[..., None] * 1.05, 0, 1)
    a = np.full(k.shape + (1,), alpha)
    return np.concatenate([rgb, a], axis=-1)


def draw_axes():
    """Simple white 3D axes (video jaisa)."""
    L = 0.8
    for vec in ([L, 0, 0], [0, L, 0], [0, 0, L]):
        ax.plot([-vec[0], vec[0]], [-vec[1], vec[1]], [-vec[2], vec[2]],
                color="#bbbbbb", lw=0.8, zorder=0)


def draw(frame):
    ax.clear()
    ax.set_axis_off()
    ax.set_xlim(-LIM, LIM)
    ax.set_ylim(-LIM, LIM)
    ax.set_zlim(-LIM, LIM)
    ax.set_box_aspect((1, 1, 1))
    draw_axes()

    # growth: 0 -> 1 (ease-out)
    t = min(frame / GROW_FRAMES, 1.0)
    grow = 1 - (1 - t) ** 3
    theta_max = max(grow * THETA_MAX, 0.6 * np.pi)
    scale = 0.25 + 0.75 * grow

    xs, ys, zs = build_rose(theta_max)
    xs, ys, zs = xs * scale, ys * scale, zs * scale

    # shuru me yellow wireframe, baad me pink surface
    if grow < 0.55:
        ax.plot_wireframe(xs, ys, zs, color=YELLOW, linewidth=0.4,
                          rstride=2, cstride=2)
    ax.plot_surface(xs, ys, zs,
                    facecolors=shaded_colors(xs, ys, zs, min(1.0, grow * 1.6)),
                    edgecolor="#ff8a5c", linewidth=0.2,
                    rstride=1, cstride=1, shade=False, antialiased=True)

    # camera: upar-neeche tilt + ghoomta hua
    elev = 28 + 40 * np.sin(2 * np.pi * frame / TOTAL_FRAMES)
    azim = 25 + 360 * frame / TOTAL_FRAMES
    ax.view_init(elev=elev, azim=azim)
    return []


if "--png" in sys.argv:
    draw(GROW_FRAMES)
    fig.savefig("rose.png", facecolor="black")
    print("Saved rose.png")
elif "--save" in sys.argv:
    anim = FuncAnimation(fig, draw, frames=TOTAL_FRAMES, blit=False)
    anim.save("rose.mp4", writer=FFMpegWriter(fps=FPS, bitrate=6000),
              progress_callback=lambda i, n: print(f"\rRendering {i + 1}/{n}", end="", flush=True))
    print()
    print("Saved rose.mp4")
else:
    anim = FuncAnimation(fig, draw, frames=TOTAL_FRAMES, interval=1000 / FPS,
                         blit=False, repeat=True)
    plt.show()
