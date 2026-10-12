"""Build the bento-grid profile tiles.

Each tile is its own SVG so every tile can link somewhere different.
Every tile is written twice, assets/bento/<name>-light.svg and -dark.svg;
the README picks one with <picture> + prefers-color-scheme.
Fonts (subset woff2) and the CleanIQ icon are embedded as data URIs,
because GitHub renders SVGs as images and blocks external resources.
"""
import base64
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "src"
OUT = ROOT / "assets" / "bento"
OUT.mkdir(parents=True, exist_ok=True)


def b64(p):
    return base64.b64encode((SRC / p).read_bytes()).decode()


FONT_CSS = (
    "@font-face{font-family:BG;font-weight:800;src:url(data:font/woff2;base64,%s) format('woff2')}"
    "@font-face{font-family:DM;font-weight:400;src:url(data:font/woff2;base64,%s) format('woff2')}"
    "@font-face{font-family:DM;font-weight:700;src:url(data:font/woff2;base64,%s) format('woff2')}"
    % (b64("bricolage-800.woff2"), b64("dmsans-400.woff2"), b64("dmsans-700.woff2"))
)
CLEANIQ = "data:image/png;base64," + b64("cleaniq-icon.png")
NICETABLE = "data:image/png;base64," + b64("nicetable-icon.png")
ZENITH = "data:image/png;base64," + b64("zenith-icon.png")

INK = "#141414"
WHITE = "#FFFFFF"
COBALT = "#2F5BFF"
LIME = "#C8F55A"
PINK = "#FF6FA8"
ORANGE = "#FF8A1F"
VIOLET = "#7B5CFF"
YELLOW = "#FFD43B"
TEAL = "#2DD4BF"

THEMES = {
    "light": dict(
        grey=("#F1F1ED", INK, "#55554F"),
        tool=("#EEF2FF", INK, COBALT, WHITE),
        name=(INK, WHITE, LIME, "#D9D9D9", "#BDBDBD"),
    ),
    "dark": dict(
        grey=("#1C2128", "#F0F3F6", "#9AA4B2"),
        tool=("#161B33", "#E8ECFF", "#8FA6FF", "#252D52"),
        name=("#F4F4EF", INK, COBALT, "#3A3A3A", "#55554F"),
    ),
}

M = 7          # transparent margin; two neighbours give a 14px gap
X0 = 29        # content inset (margin + 22px padding)
DISPLAY = "BG, 'Bricolage Grotesque', 'Segoe UI', sans-serif"
BODY = "DM, 'DM Sans', 'Segoe UI', sans-serif"


def text(x, y, s, size, fill, family=BODY, weight=400, anchor="start", ls=0, opacity=1):
    extra = f' letter-spacing="{ls}"' if ls else ""
    extra += f' text-anchor="{anchor}"' if anchor != "start" else ""
    extra += f' opacity="{opacity}"' if opacity != 1 else ""
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-weight="{weight}" '
            f'font-size="{size}" fill="{fill}"{extra}>{escape(s)}</text>')


def label(x, y, s, fill, size=12):
    return text(x, y, s, size, fill, weight=700, ls=1.3)


def arrow(x, y, stroke):
    return (f'<g transform="translate({x} {y})" fill="none" stroke="{stroke}" stroke-width="2.2" '
            f'stroke-linecap="round" stroke-linejoin="round"><path d="M5 19 19 5M8 5h11v11"/></g>')


def svg(name, theme, w, h, bg, body, title):
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
           f'role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>'
           f'<style>{FONT_CSS}</style>'
           f'<rect x="{M}" y="{M}" width="{w - 2 * M}" height="{h - 2 * M}" rx="24" fill="{bg}"/>'
           f'{body}</svg>')
    (OUT / f"{name}-{theme}.svg").write_text(doc, encoding="utf-8")


def build(theme):
    t = THEMES[theme]
    g_bg, g_fg, g_lab = t["grey"]
    tb_bg, tb_fg, tb_lab, tb_chip = t["tool"]
    n_bg, n_fg, n_acc, n_para, n_loc = t["name"]

    # Name (half, 300 tall)
    w = 440
    body = (f'<rect x="{X0}" y="{X0}" width="112" height="30" rx="15" fill="{LIME}"/>'
            + text(X0 + 56, X0 + 20, "Open to work", 13, INK, weight=700, anchor="middle")
            + text(w - X0, X0 + 20, "Amman, Jordan", 13, n_loc, anchor="end")
            + text(X0, 140, "Omar", 52, n_fg, DISPLAY, 800, ls=-0.8)
            + text(X0, 192, "Albarghouthi", 52, n_fg, DISPLAY, 800, ls=-0.8)
            + text(X0, 226, "AI Engineer", 18, n_acc, weight=700)
            + text(X0, 254, "I build LLM apps and measure whether they work.", 14.5, n_para)
            + text(X0, 274, "Arabic + English · Jordan, the Gulf, remote.", 14.5, n_para))
    svg("name", theme, w, 300, n_bg, body, "Omar Albarghouthi, AI Engineer, open to work")

    # NiceTable (half, 300 tall)
    icon = (f'<rect x="{X0}" y="{X0}" width="52" height="52" rx="14" fill="{WHITE}"/>'
            f'<image href="{NICETABLE}" x="{X0 + 9}" y="{X0 + 9}" width="34" height="34"/>')
    body = (icon + label(X0 + 66, X0 + 31, "LIVE PRODUCT", WHITE) + arrow(w - X0 - 24, X0 + 2, WHITE)
            + text(X0, 196, "NiceTable", 38, WHITE, DISPLAY, 800, ls=-0.5)
            + text(X0, 226, "Paste messy text, get a clean table you can", 15, WHITE)
            + text(X0, 246, "restyle and export. No account needed.", 15, WHITE)
            + text(X0, 276, "nice-table.vercel.app", 13, WHITE, weight=700, opacity=0.85))
    svg("nicetable", theme, w, 300, COBALT, body, "NiceTable, live product: messy text to clean tables")

    # Quarter tiles (220 x 220)
    q = 220
    body = (f'<rect x="{X0}" y="{X0}" width="44" height="44" rx="12" fill="{WHITE}"/>'
            f'<image href="{CLEANIQ}" x="{X0 + 5}" y="{X0 + 5}" width="34" height="34"/>'
            + label(X0 + 54, X0 + 27, "OPEN SOURCE", INK, 11)
            + text(X0, 150, "CleanIQ", 26, INK, DISPLAY, 800)
            + text(X0, 176, "Local AI explains each", 13, INK)
            + text(X0, 194, "file before deleting it.", 13, INK))
    svg("cleaniq", theme, q, q, LIME, body, "CleanIQ, open-source local-AI file assistant")

    body = (label(X0, 48, "CASE STUDY", INK)
            + text(X0, 128, "LLM", 26, INK, DISPLAY, 800)
            + text(X0, 156, "Guardrails", 26, INK, DISPLAY, 800)
            + text(X0, 180, "Safety layers under", 13, INK)
            + text(X0, 198, "multi-turn pressure.", 13, INK))
    svg("guardrails", theme, q, q, PINK, body, "Anatomy of LLM Guardrails case study")

    body = (label(X0, 48, "ORGANIC VISITS", g_lab)
            + text(X0, 158, "500K+", 46, g_fg, DISPLAY, 800, ls=-0.5)
            + text(X0, 188, "to my Arabic tech blog", 13, g_fg))
    svg("visits", theme, q, q, g_bg, body, "500K+ organic visits to my Arabic tech blog")

    body = (label(X0, 48, "CONTRIBUTIONS", WHITE)
            + text(X0, 158, "2,000+", 46, WHITE, DISPLAY, 800, ls=-0.5)
            + text(X0, 188, "on GitHub in 12 months", 13, WHITE))
    svg("contributions", theme, q, q, VIOLET, body, "2,000+ GitHub contributions in 12 months")

    body = (label(X0, 48, "TOOL", g_lab)
            + text(X0, 132, "claude-", 23, g_fg, DISPLAY, 800)
            + text(X0, 158, "usage-hack", 23, g_fg, DISPLAY, 800)
            + text(X0, 182, "Pin your Claude usage", 13, g_fg)
            + text(X0, 200, "window to a set time.", 13, g_fg))
    svg("usage-hack", theme, q, q, g_bg, body, "claude-usage-hack: schedule your Claude usage window")

    body = (label(X0, 48, "AUTOMATION", INK)
            + text(X0, 150, "15 h", 46, INK, DISPLAY, 800, ls=-0.5)
            + text(X0, 180, "manual work a week,", 13, INK)
            + text(X0, 198, "removed with UiPath", 13, INK))
    svg("automation", theme, q, q, YELLOW, body, "15 hours of manual work a week removed with UiPath")

    # Zenith (half, 220 tall)
    w2 = 440
    body = (f'<rect x="{X0}" y="{X0}" width="52" height="52" rx="14" fill="{WHITE}"/>'
            f'<image href="{ZENITH}" x="{X0 + 8}" y="{X0 + 8}" width="36" height="36"/>'
            + label(X0 + 66, X0 + 31, "AI APP · OPEN SOURCE", INK)
            + arrow(w2 - X0 - 24, X0 + 2, INK)
            + text(X0, 136, "Zenith", 34, INK, DISPLAY, 800, ls=-0.4)
            + text(X0, 162, "Well-being companion: crisis screen first, HyDE", 14, INK)
            + text(X0, 181, "retrieval over Qdrant, FastAPI + React.", 14, INK)
            + text(X0, 205, "31 tests · CI on every push", 12.5, INK, weight=700, opacity=0.75))
    svg("zenith", theme, w2, 220, TEAL, body, "Zenith: retrieval-grounded well-being companion")

    # Contact (two halves, 220 tall)
    body = (label(X0, 48, "HIRING?", INK)
            + text(X0, 140, "Email me", 32, INK, DISPLAY, 800)
            + text(X0, 176, "omarbarghouti505@gmail.com", 16, INK, weight=700)
            + arrow(w2 - X0 - 24, X0 + 2, INK))
    svg("email", theme, w2, 220, LIME, body, "Email omarbarghouti505@gmail.com")

    body = (label(X0, 48, "CONNECT", WHITE)
            + text(X0, 140, "LinkedIn", 32, WHITE, DISPLAY, 800)
            + text(X0, 176, "in/omar-albarghouthi", 16, WHITE, weight=700)
            + arrow(w2 - X0 - 24, X0 + 2, WHITE))
    svg("linkedin", theme, w2, 220, COBALT, body, "LinkedIn: omar-albarghouthi")

    # Open WebUI (half, 220 tall)
    body = (label(X0, 48, "OPEN-SOURCE CONTRIBUTION", INK)
            + f'<rect x="{w - X0 - 98}" y="{X0}" width="98" height="30" rx="15" fill="{INK}"/>'
            + text(w - X0 - 49, X0 + 20, "PR #32289", 13, ORANGE, weight=700, anchor="middle")
            + text(X0, 140, "463 Arabic strings", 32, INK, DISPLAY, 800, ls=-0.4)
            + text(X0, 176, "for Open WebUI", 32, INK, DISPLAY, 800, ls=-0.4)
            + text(X0, 202, "Completed the ar and ar-BH localisation.", 14, INK))
    svg("openwebui", theme, w, 220, ORANGE, body, "Open WebUI contribution: 463 Arabic strings, PR 32289")

    # Toolbox (half, 220 tall): chips flow into rows
    chips = ["Python", "FastAPI", "LangChain", "RAG", "Ollama", "OpenAI", "Claude", "Gemini",
             "React", "Next.js", "TypeScript", "Docker", "n8n", "UiPath"]
    body = label(X0, 48, "TOOLBOX", tb_lab)
    x, y, right = X0, 66, w - X0
    for c in chips:
        cw = round(len(c) * 7.4 + 24)
        if x + cw > right:
            x, y = X0, y + 40
        body += (f'<rect x="{x}" y="{y}" width="{cw}" height="30" rx="15" fill="{tb_chip}"/>'
                 + text(x + cw / 2, y + 20, c, 13, tb_fg, weight=700, anchor="middle"))
        x += cw + 8
    svg("toolbox", theme, w, 220, tb_bg, body, "Toolbox: " + ", ".join(chips))


for th in THEMES:
    build(th)
print("wrote", len(list(OUT.glob("*.svg"))), "files to", OUT)
