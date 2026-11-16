"""Reel 9:16 (1080x1920) a partir de 2 clips de video generados en Gemini (Veo).
Une los clips con fundido, suma portada (título), leyenda "Render ilustrativo" y cierre "Escribí PLANO".
Conserva el audio ambiente de Gemini (sin música).
Uso: python3 generador/reel_gemini.py <clip1.mp4> <clip2.mp4> <kicker> <titulo> <bajada> <salida.mp4>"""
import os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from slides3 import BG, INK, MUTED, ORANGE, T, logo

W, H = 1080, 1920
L1, L2, X, END = 9.5, 10.0, 0.7, 3.0  # duración clip1, clip2, fundido, cierre


def svg(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{body}</svg>'


def png(s, path):
    open(path + ".svg", "w").write(s)
    subprocess.run(["rsvg-convert", path + ".svg", "-o", path], check=True)


def main(c1, c2, kicker, titulo, bajada, out):
    d = tempfile.mkdtemp()
    defs = ('<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F5F3EF" stop-opacity="0.94"/>'
            '<stop offset="1" stop-color="#F5F3EF" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#000" stop-opacity="0.55"/></linearGradient>'
            '<linearGradient id="e" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F5F3EF" stop-opacity="0"/>'
            '<stop offset="0.35" stop-color="#F5F3EF" stop-opacity="0.93"/><stop offset="1" stop-color="#F5F3EF" stop-opacity="0.97"/></linearGradient></defs>')
    # leyenda permanente
    png(svg(defs + f'<rect y="1640" width="{W}" height="280" fill="url(#b)"/>'
            + T(72, 1840, "Render ilustrativo · diseño original DPRO", 26, 500, "#FFFFFF")), f"{d}/ley.png")
    # portada (primeros segundos)
    png(svg(defs + f'<rect width="{W}" height="720" fill="url(#g)"/>' + logo(72, 140, 84)
            + T(72, 340, kicker, 24, 600, ORANGE, ls=6) + T(66, 450, titulo, 96, 300, INK)
            + T(72, 520, bajada, 30, 400, MUTED)), f"{d}/tit.png")
    # cierre
    png(svg(defs + f'<rect y="960" width="{W}" height="960" fill="url(#e)"/>' + logo(420, 1130, 240)
            + T(W / 2, 1420, "¿La querés en tu terreno?", 52, 300, INK, "middle")
            + T(W / 2, 1530, "Escribí PLANO", 84, 500, ORANGE, "middle")
            + T(W / 2, 1605, "por WhatsApp", 42, 300, INK, "middle")
            + T(W / 2, 1720, "Render ilustrativo · Capiatá · Central · Paraguay", 26, 400, MUTED, "middle")), f"{d}/end.png")
    total = L1 + L2 - X
    t_end = total - END
    fc = (
        f"[0:v]trim=0:{L1},setpts=PTS-STARTPTS,scale={W}:{H}:flags=lanczos,fps=30,format=yuv420p,setsar=1[v1];"
        f"[1:v]trim=0:{L2},setpts=PTS-STARTPTS,scale={W}:{H}:flags=lanczos,fps=30,format=yuv420p,setsar=1[v2];"
        f"[v1][v2]xfade=transition=fade:duration={X}:offset={L1-X}[v];"
        f"[2:v]format=rgba[ley];[3:v]format=rgba,fade=t=in:st=0.3:d=0.6:alpha=1,fade=t=out:st=3.4:d=0.6:alpha=1[tit];"
        f"[4:v]format=rgba,fade=t=in:st={t_end}:d=0.7:alpha=1[end];"
        f"[v][ley]overlay=0:0:enable='lt(t,{t_end+0.4})'[a];[a][tit]overlay=0:0[b];[b][end]overlay=0:0,format=yuv420p[vo];"
        f"[0:a]atrim=0:{L1},asetpts=PTS-STARTPTS[a1];[1:a]atrim=0:{L2},asetpts=PTS-STARTPTS[a2];"
        f"[a1][a2]acrossfade=d={X},volume=2.0,afade=t=in:d=0.4,afade=t=out:st={total-1.5}:d=1.5[ao]")
    loop = lambda p: ["-loop", "1", "-framerate", "30", "-t", f"{total}", "-i", p]
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", c1, "-i", c2, *loop(f"{d}/ley.png"), *loop(f"{d}/tit.png"), *loop(f"{d}/end.png"),
           "-filter_complex", fc, "-map", "[vo]", "-map", "[ao]", "-t", f"{total}",
           "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p", "-r", "30",
           "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    print(out, f"{total:.1f}s")


if __name__ == "__main__":
    main(*sys.argv[1:7])
