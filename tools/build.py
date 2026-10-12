"""Generates the SVG assets used by the profile README.

Run:  python tools/build.py
Writes into ./assets/. Every graphic is plain SVG with inline CSS so GitHub
renders it (including the animations) without any external service.
"""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

BG0, BG1 = "#070B14", "#0B1324"
LINE = "#1B2740"
TEXT = "#F4F7FB"
MUTED = "#93A3BC"
DIM = "#5D6E8A"
BLUE = "#3B82F6"
BLUE_L = "#7AB0FF"
GREEN = "#34D399"


def write(name, svg):
    (OUT / name).write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", name)


# ---------------------------------------------------------------- header ----
def header():
    w, h = 1200, 420
    grid = "".join(
        f'<line x1="{x}" y1="0" x2="{x}" y2="{h}"/>' for x in range(0, w + 1, 40)
    ) + "".join(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}"/>' for y in range(0, h + 1, 40))

    # "eval log" lines on the right, revealed one after another
    log = [
        ("$", "eval --models gpt claude gemini", MUTED),
        ("✓", "structured output      validated", GREEN),
        ("✓", "cost per turn          logged", GREEN),
        ("✓", "refusals & latency     compared", GREEN),
        ("→", "route on the numbers. ship.", BLUE_L),
    ]
    log_svg = ""
    for i, (mark, txt, col) in enumerate(log):
        y = 150 + i * 34
        log_svg += (
            f'<g class="ln" style="animation-delay:{0.6 + i * 0.55:.2f}s">'
            f'<text x="770" y="{y}" fill="{col}" font-family="{MONO}" font-size="17">{escape(mark)}</text>'
            f'<text x="796" y="{y}" fill="{TEXT if mark=="$" else MUTED}" font-family="{MONO}" font-size="17">{escape(txt)}</text>'
            f"</g>"
        )

    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Omar Albarghouthi — AI Engineer. LLM apps, RAG and evaluation. Amman, Jordan.">
  <title>Omar Albarghouthi — AI Engineer</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/>
    </linearGradient>
    <radialGradient id="orb" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{BLUE}" stop-opacity="0.55"/>
      <stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#fff" stop-opacity="1"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <mask id="gridmask"><rect width="{w}" height="{h}" fill="url(#fade)"/></mask>
    <clipPath id="r"><rect width="{w}" height="{h}" rx="22"/></clipPath>
  </defs>
  <style>
    .orb {{ animation: drift 14s ease-in-out infinite alternate; transform-origin: center; }}
    @keyframes drift {{ from {{ transform: translate(0,0) scale(1); }} to {{ transform: translate(-60px,30px) scale(1.15); }} }}
    .ln {{ opacity: 0; animation: in .5s ease-out forwards; }}
    @keyframes in {{ from {{ opacity: 0; transform: translateX(-8px); }} to {{ opacity: 1; transform: none; }} }}
    .caret {{ animation: blink 1.05s steps(1) infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    .pulse {{ animation: pulse 2.2s ease-out infinite; transform-origin: 92px 352px; }}
    @keyframes pulse {{ from {{ opacity: .7; transform: scale(1); }} to {{ opacity: 0; transform: scale(2.8); }} }}
    .scan {{ animation: scan 6s linear infinite; }}
    @keyframes scan {{ from {{ transform: translateY(-40px); }} to {{ transform: translateY({h}px); }} }}
  </style>
  <g clip-path="url(#r)">
    <rect width="{w}" height="{h}" fill="url(#bg)"/>
    <g stroke="{LINE}" stroke-width="1" opacity="0.55" mask="url(#gridmask)">{grid}</g>
    <circle class="orb" cx="1020" cy="80" r="320" fill="url(#orb)"/>
    <rect class="scan" x="0" y="0" width="{w}" height="2" fill="{BLUE}" opacity="0.12"/>

    <!-- left: identity -->
    <text x="80" y="96" fill="{BLUE_L}" font-family="{MONO}" font-size="16" letter-spacing="3">AI ENGINEER  ·  AMMAN, JORDAN</text>
    <text x="78" y="168" fill="{TEXT}" font-family="{FONT}" font-size="60" font-weight="800" letter-spacing="-1.5">Omar Albarghouthi</text>
    <text x="80" y="216" fill="{MUTED}" font-family="{FONT}" font-size="24">I build LLM apps and <tspan fill="{TEXT}" font-weight="700">measure</tspan> whether they work.</text>
    <text x="80" y="252" fill="{DIM}" font-family="{FONT}" font-size="18">LLM applications · RAG · evaluation · guardrails · Python / FastAPI / React</text>

    <g font-family="{FONT}" font-size="15" font-weight="600">
      <rect x="80" y="288" width="118" height="34" rx="17" fill="none" stroke="{LINE}"/>
      <text x="139" y="310" fill="{TEXT}" text-anchor="middle">العربية</text>
      <rect x="208" y="288" width="96" height="34" rx="17" fill="none" stroke="{LINE}"/>
      <text x="256" y="310" fill="{TEXT}" text-anchor="middle">English</text>
      <rect x="314" y="288" width="196" height="34" rx="17" fill="none" stroke="{LINE}"/>
      <text x="412" y="310" fill="{TEXT}" text-anchor="middle">Gulf · Jordan · Remote</text>
    </g>

    <circle class="pulse" cx="92" cy="352" r="6" fill="{GREEN}"/>
    <circle cx="92" cy="352" r="6" fill="{GREEN}"/>
    <text x="108" y="358" fill="{GREEN}" font-family="{FONT}" font-size="16" font-weight="600">Open to AI &amp; software engineering roles</text>

    <!-- right: terminal -->
    <rect x="740" y="92" width="400" height="236" rx="14" fill="#0A1222" stroke="{LINE}"/>
    <circle cx="762" cy="112" r="5" fill="#2A3A58"/><circle cx="780" cy="112" r="5" fill="#2A3A58"/><circle cx="798" cy="112" r="5" fill="#2A3A58"/>
    {log_svg}
    <rect class="caret" x="796" y="296" width="10" height="20" fill="{BLUE_L}"/>
  </g>
</svg>"""


# ----------------------------------------------------------- project card ----
def card(name, file, kicker, title, lines, tags, foot, accent=BLUE):
    w, h = 560, 280
    body = "".join(
        f'<text x="32" y="{132 + i * 26}" fill="{MUTED}" font-family="{FONT}" font-size="16">{escape(t)}</text>'
        for i, t in enumerate(lines)
    )
    x = 32
    tag_svg = ""
    for t in tags:
        tw = 14 + len(t) * 7.6
        tag_svg += (
            f'<rect x="{x}" y="212" width="{tw:.0f}" height="26" rx="13" fill="{accent}" fill-opacity="0.12" stroke="{accent}" stroke-opacity="0.35"/>'
            f'<text x="{x + tw / 2:.0f}" y="230" fill="{BLUE_L}" font-family="{MONO}" font-size="12.5" text-anchor="middle">{escape(t)}</text>'
        )
        x += tw + 8
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">
  <title>{escape(title)}</title>
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG0}"/></linearGradient>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></linearGradient>
  </defs>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="18" fill="url(#g)" stroke="{LINE}"/>
  <rect x="24" y="0.5" width="200" height="3" rx="1.5" fill="url(#edge)"/>
  <text x="32" y="50" fill="{BLUE_L}" font-family="{MONO}" font-size="13" letter-spacing="2">{escape(kicker)}</text>
  <text x="32" y="92" fill="{TEXT}" font-family="{FONT}" font-size="30" font-weight="800" letter-spacing="-0.5">{escape(title)}</text>
  {body}
  {tag_svg}
  <text x="{w-32}" y="50" fill="{DIM}" font-family="{FONT}" font-size="14" text-anchor="end">{escape(foot)} →</text>
</svg>"""
    write(file, svg)


# ------------------------------------------------------------ numbers row ----
def numbers():
    w, h = 1200, 180
    items = [
        ("2,000+", "contributions on GitHub", "in the last 12 months"),
        ("500K+", "organic visits", "Arabic tech blog I built"),
        ("15 hrs/week", "manual work removed", "UiPath automations, internship"),
        ("5", "LLM providers", "benchmarked side by side"),
    ]
    col = w / len(items)
    out = ""
    for i, (big, a, b) in enumerate(items):
        cx = col * i + col / 2
        out += (
            f'<text x="{cx:.0f}" y="76" fill="{TEXT}" font-family="{FONT}" font-size="46" font-weight="800" text-anchor="middle" letter-spacing="-1">{escape(big)}</text>'
            f'<text x="{cx:.0f}" y="112" fill="{BLUE_L}" font-family="{FONT}" font-size="19" font-weight="600" text-anchor="middle">{escape(a)}</text>'
            f'<text x="{cx:.0f}" y="140" fill="{DIM}" font-family="{FONT}" font-size="17" text-anchor="middle">{escape(b)}</text>'
        )
        if i:
            out += f'<line x1="{col*i:.0f}" y1="40" x2="{col*i:.0f}" y2="136" stroke="{LINE}"/>'
    write("numbers.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="2,000+ GitHub contributions in 12 months; 500K+ organic blog visits; 15 hours a week of manual work automated; 5 LLM providers benchmarked">
  <title>Numbers</title>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="18" fill="{BG0}" stroke="{LINE}"/>
  {out}
</svg>""")


# ------------------------------------------------------------- principles ----
def principles():
    w, h = 1200, 260
    rows = [
        ("01", "Tests before prompts", "Write the cases first. A prompt that worked once is not a prompt that works."),
        ("02", "Measure, then route", "Cost per turn, latency, refusals, valid-output rate. Pick models on numbers, not hype."),
        ("03", "Ship to real users", "Every project here is live or open source. Feedback beats a perfect plan."),
    ]
    col = w / 3
    out = ""
    for i, (n, t, d) in enumerate(rows):
        x = col * i + 36
        words, line, lines = d.split(), "", []
        for wd in words:
            if len(line) + len(wd) > 32:
                lines.append(line.strip()); line = ""
            line += wd + " "
        lines.append(line.strip())
        out += f'<text x="{x:.0f}" y="64" fill="{BLUE}" font-family="{MONO}" font-size="15" letter-spacing="2">{n}</text>'
        out += f'<text x="{x:.0f}" y="100" fill="{TEXT}" font-family="{FONT}" font-size="26" font-weight="700">{escape(t)}</text>'
        for j, l in enumerate(lines):
            out += f'<text x="{x:.0f}" y="{140 + j*28}" fill="{MUTED}" font-family="{FONT}" font-size="20">{escape(l)}</text>'
        if i:
            out += f'<line x1="{col*i:.0f}" y1="40" x2="{col*i:.0f}" y2="{h-40}" stroke="{LINE}"/>'
    write("principles.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="How I work: tests before prompts; measure, then route; ship to real users">
  <title>How I work</title>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="18" fill="{BG0}" stroke="{LINE}"/>
  {out}
</svg>""")


# ------------------------------------------------------------------ stack ----
def stack():
    w, h = 1200, 290
    groups = [
        ("LLM & AI", ["OpenAI", "Claude", "Gemini", "DeepSeek", "Ollama", "LangChain", "RAG", "Tool calling"]),
        ("Backend", ["Python", "FastAPI", "Flask", "Node.js", "SQL", "Docker"]),
        ("Frontend", ["React", "Next.js", "TypeScript", "Vite", "HTML/CSS"]),
        ("Ship & automate", ["Vercel", "Cloudflare", "GitHub Actions", "n8n", "UiPath", "SEO / GEO"]),
    ]
    out = ""
    for i, (g, items) in enumerate(groups):
        y = 48 + i * 58
        out += f'<text x="36" y="{y+24}" fill="{DIM}" font-family="{MONO}" font-size="15" letter-spacing="2">{escape(g.upper())}</text>'
        x = 260
        for it in items:
            tw = 26 + len(it) * 10.2
            out += (
                f'<rect x="{x:.0f}" y="{y}" width="{tw:.0f}" height="38" rx="9" fill="#0F1A2E" stroke="{LINE}"/>'
                f'<text x="{x + tw/2:.0f}" y="{y+25}" fill="{TEXT}" font-family="{FONT}" font-size="17.5" font-weight="500" text-anchor="middle">{escape(it)}</text>'
            )
            x += tw + 10
    write("stack.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Tech stack">
  <title>Tech stack</title>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="18" fill="{BG0}" stroke="{LINE}"/>
  {out}
</svg>""")


# ------------------------------------------------------------- section bar ---
def section(file, label):
    w, h = 1200, 56
    write(file, f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">
  <title>{escape(label)}</title>
  <rect x="0" y="26" width="6" height="22" rx="3" fill="{BLUE}"/>
  <text x="20" y="44" fill="#4C7DD9" font-family="{MONO}" font-size="18" font-weight="600" letter-spacing="3">{escape(label.upper())}</text>
  <line x1="{24 + len(label)*13.5:.0f}" y1="38" x2="{w}" y2="38" stroke="#4C7DD9" stroke-opacity="0.3"/>
</svg>""")


if __name__ == "__main__":
    write("header.svg", header())
    card("nicetable", "card-nicetable.svg", "LIVE PRODUCT", "NiceTable",
         ["Paste messy text, get a clean, styled table.",
          "Reliable structured output from LLMs, a per-session",
          "cost cap, and no sign-up needed."],
         ["React", "FastAPI", "LLM APIs", "Vercel"], "nice-table.vercel.app")
    card("cleaniq", "card-cleaniq.svg", "OPEN SOURCE · MIT", "CleanIQ",
         ["A local LLM reads each file and tells you what it is",
          "before you delete it. Nothing leaves your machine.",
          "Recovered 74.5 GB on my own laptop."],
         ["Python", "FastAPI", "Ollama", "Local AI"], "repo")
    card("guardrails", "card-guardrails.svg", "LLM SAFETY RESEARCH", "Anatomy of LLM Guardrails",
         ["How guardrail layers behave under multi-turn",
          "pressure: a defensive case study on GLM-4.6,",
          "with a taxonomy and builder recommendations."],
         ["LLM safety", "Red teaming", "EN / AR"], "repo")
    card("usage", "card-usage-hack.svg", "AUTOMATION", "claude-usage-hack",
         ["Starts your Claude Pro/Max 5-hour window at a",
          "time you choose, via a scheduled routine or a",
          "GitHub Actions cron hitting the Routines API."],
         ["GitHub Actions", "Shell", "API"], "repo")
    numbers()
    principles()
    stack()
    section("sec-work.svg", "Selected work")
    section("sec-numbers.svg", "In numbers")
    section("sec-how.svg", "How I work")
    section("sec-stack.svg", "Toolbox")
    section("sec-now.svg", "Right now")
