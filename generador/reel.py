"""Reel 9:16 (1080x1920) a partir del render de Gemini + láminas del carrusel. Sin música (evita derechos).
Uso: python3 generador/reel.py <render.jpg> <lamina_planta.jpg> <lamina_ficha.jpg> <kicker> <titulo1> <titulo2> <bajada> <salida.mp4>"""
import os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from slides3 import BG, INK, MUTED, ORANGE, T, logo

W, H = 1080, 1920


def svg(body, bg=None):
    r = f'<rect width="{W}" height="{H}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{r}{body}</svg>'


def png(s, path):
    open(path + ".svg", "w").write(s)
    subprocess.run(["rsvg-convert", path + ".svg", "-o", path], check=True)


def main(render, planta, ficha, kicker, t1, t2, bajada, out):
    d = tempfile.mkdtemp()
    # overlay portada: degradé claro arriba para legibilidad + textos + leyenda abajo
    grad = ('<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F5F3EF" stop-opacity="0.92"/>'
            '<stop offset="1" stop-color="#F5F3EF" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#000" stop-opacity="0.55"/></linearGradient></defs>'
            f'<rect width="{W}" height="760" fill="url(#g)"/><rect y="1620" width="{W}" height="300" fill="url(#b)"/>')
    png(svg(grad + logo(72, 150, 84) + T(72, 360, kicker, 24, 600, ORANGE, ls=6)
            + T(66, 470, t1, 96, 300, INK) + T(66, 575, t2, 96, 300, INK) + T(72, 640, bajada, 30, 400, MUTED)
            + T(72, 1830, "Render ilustrativo · diseño original DPRO", 26, 500, "#FFFFFF")), f"{d}/ov1.png")
    png(svg("", BG), f"{d}/bg2.png")
    png(svg("", BG), f"{d}/bg3.png")
    png(svg(logo(390, 560, 300) + T(W / 2, 1040, "¿La querés en tu terreno?", 56, 300, INK, "middle")
            + T(W / 2, 1160, "Escribí PLANO", 84, 500, ORANGE, "middle") + T(W / 2, 1240, "por WhatsApp", 44, 300, INK, "middle")
            + T(W / 2, 1420, "Capiatá · Central · Paraguay", 28, 400, MUTED, "middle"), BG), f"{d}/end.png")
    A, B, C, D, X = 7, 5, 5, 3.5, 0.5
    fc = (
        f"[0:v]scale=-2:1920,crop=1080:1920:'(iw-1080)*t/{A}':0,fps=30[a0];[a0][1:v]overlay=0:0,format=yuv420p,setsar=1[a];"
        f"[2:v]scale=2160:-2,zoompan=z='1+0.04*on/({B}*30)':d=1:x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':s=1080x1350:fps=30[p];"
        f"[3:v][p]overlay=0:285:shortest=1,format=yuv420p,setsar=1[b];"
        f"[4:v]scale=2160:-2,zoompan=z='1+0.04*on/({C}*30)':d=1:x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':s=1080x1350:fps=30[f];"
        f"[5:v][f]overlay=0:285:shortest=1,format=yuv420p,setsar=1[c];"
        f"[6:v]fps=30,format=yuv420p,setsar=1[e];"
        f"[a][b]xfade=transition=fade:duration={X}:offset={A-X}[ab];"
        f"[ab][c]xfade=transition=fade:duration={X}:offset={A+B-2*X}[abc];"
        f"[abc][e]xfade=transition=fade:duration={X}:offset={A+B+C-3*X}[v]")
    total = A + B + C + D - 3 * X
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-loop", "1", "-framerate", "30", "-t", str(A), "-i", render, "-loop", "1", "-framerate", "30", "-t", str(A), "-i", f"{d}/ov1.png",
           "-loop", "1", "-framerate", "30", "-t", str(B), "-i", planta, "-loop", "1", "-framerate", "30", "-t", str(B), "-i", f"{d}/bg2.png",
           "-loop", "1", "-framerate", "30", "-t", str(C), "-i", ficha, "-loop", "1", "-framerate", "30", "-t", str(C), "-i", f"{d}/bg3.png",
           "-loop", "1", "-framerate", "30", "-t", str(D), "-i", f"{d}/end.png",
           "-f", "lavfi", "-t", str(total), "-i", "anullsrc=r=44100:cl=stereo",
           "-filter_complex", fc, "-map", "[v]", "-map", "7:a", "-c:v", "libx264", "-preset", "slow", "-crf", "20",
           "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    print(out)


if __name__ == "__main__":
    main(*sys.argv[1:9])
