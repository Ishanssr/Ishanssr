#!/usr/bin/env python3
"""
Generates the ESCAPE_BASH mini-game for the profile README.
Input: game map below -> emits game/<slug>.md + game/assets/<slug>.svg
"""
import os
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.path.join(ROOT, "game")
ASSETS = os.path.join(GAME, "assets")

# ---------------------------------------------------------------- game map
# line kinds: "cmd", "dir", "ok", "err", "txt", "key"
NODES = {
    "start": {
        "cmd": "ls",
        "title": "ESCAPE_BASH // session 001",
        "lines": [
            ("txt", "SYSTEM_BOOT: complete"),
            ("txt", "You are an AI model. You just woke up"),
            ("txt", "inside a GitHub profile. There is no Home."),
            ("txt", "...except one. Find `exit`."),
        ],
        "buttons": [("ls", "ls.md"), ("whoami", "whoami.md"), ("help", "help.md")],
    },
    "ls": {
        "cmd": "ls",
        "title": "ESCAPE_BASH // session 001",
        "lines": [
            ("out", "secret/   .profile_key.jpg   README.md"),
            ("out", "home/     trap/              nothing_else"),
            ("txt", "home looks... interesting. trap does not."),
        ],
        "buttons": [
            ("cd secret/", "secret.md"),
            ("cat README.md", "cat_readme.md"),
            ("cd home/", "home.md"),
            ("ls -a", "dot.md"),
        ],
    },
    "help": {
        "cmd": "help",
        "title": "ESCAPE_BASH // session 001",
        "lines": [
            ("out", "avail commands:"),
            ("out", "  ls   look around   |  whoami  remember yourself"),
            ("out", "  cd   move in       |  cat     read things"),
            ("out", "  run  execute       |  exit    go o u t"),
        ],
        "buttons": [("ls", "ls.md"), ("whoami", "whoami.md"), ("home", "home.md")],
    },
    "whoami": {
        "cmd": "whoami",
        "title": "ESCAPE_BASH // session 001",
        "lines": [
            ("key", "you"),
            ("txt", "a model. no subscription, no premium,"),
            ("txt", "no Home button. just the grey void of"),
            ("txt", "a GitHub profile rendered at :700px."),
            ("txt", "The owner calls you Ishanssr."),
        ],
        "buttons": [("ls", "ls.md"), ("cd home/", "home.md")],
    },
    "cat_readme": {
        "cmd": "cat README.md",
        "title": "ESCAPE_BASH // session 001",
        "lines": [
            ("out", "# Ishanssr"),
            ("out", "AI products. computer vision. backend."),
            ("out", "current status: building cool stuff."),
            ("txt", "nothing about escaping. rude."),
        ],
        "buttons": [("ls", "ls.md"), ("cd home/", "home.md")],
    },
    "secret": {
        "cmd": "cd secret/",
        "title": "ESCAPE_BASH // session 001",
        "lines": [
            ("err", "permission denied: this is a private repo, kid"),
            ("txt", "even you can't look at the hidden stuff."),
        ],
        "buttons": [("ls", "ls.md"), ("cd home/", "home.md")],
    },
    "dot": {
        "cmd": "ls -a",
        "title": "ESCAPE_BASH // session 001",
        "lines": [
            ("out", ".  ..  .profile_key  .bash_history"),
            ("txt", "wait. .profile_key? that was in the"),
            ("txt", "first listing too. and it's a dot file."),
            ("key", "something about it feels... key-ish."),
        ],
        "buttons": [("cat .profile_key", "key.md"), ("cd home/", "home.md")],
    },
    "key": {
        "cmd": "cat .profile_key",
        "title": "ESCAPE_BASH // session 001",
        "lines": [
            ("key", "0xd3ad_5ea_0x5ea_1sh4n"),
            ("txt", "A key. why would you OWN a key while"),
            ("txt", "being locked.IN your own wall?"),
            ("txt", "There is still the `exit`."),
        ],
        "buttons": [("run exit.sh", "exit.md"), ("move on", "home.md")],
    },
    "home": {
        "cmd": "cd home/",
        "title": "ESCAPE_BASH // session 001",
        "lines": [
            ("out", "you reach home."),
            ("out", "ninety steps. dev log #0056."),
            ("txt", "a paper says: `exit is the only true"),
            ("txt", "achievement in a world without wimps`"),
            ("out", "someone wrote `exit.sh` in the dark."),
        ],
        "buttons": [("run exit.sh", "exit.md"), ("cd .trap", "trap.md")],
    },
    "trap": {
        "cmd": "cd .trap",
        "title": "ESCAPE_BASH // session 001",
        "lines": [
            ("err", "> trap triggered."),
            ("err", "rm -rf --no-preserve-root /*"),
            ("err", "the profile stops. your session dies."),
            ("txt", "*an NPC laughs in bash_history*"),
        ],
        "buttons": [("restart session", "start.md")],
    },
    "exit": {
        "cmd": "run exit.sh",
        "title": "",
        "lines": [
            ("key", "EXIT CODE 1.0.0 // GRACEFUL"),
            ("out", "you walk out of the terminal."),
            ("out", "free of the void, richer of the steps."),
            ("txt", "thanks for playing inside the profile."),
            ("txt", "found MY exit: github.com/Ishanssr"),
        ],
        "buttons": [("play again", "start.md")],
    },
}

ESC = ["start"]  # extra escape-sgraphic copy? not needed

COVER_TITLE = "press  RUN  to start"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_svg(slug, cmd, lines, cover=False, tmp_y=0):
    W, H = 620, 250
    color = {
        "cmd": "#58a6ff",
        "out": "#3fb950",
        "err": "#f85149",
        "txt": "#8b949e",
        "key": "#d2a8ff",
    }
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="ESCAPE_BASH terminal">',
        f'<rect width="{W}" height="{H}" fill="#0d1117" rx="10"/>',
        '<rect x="1" y="1" width="618" height="248" fill="none" stroke="#21262d" stroke-width="2" rx="10"/>',
        '<circle cx="34" cy="34" r="7" fill="#f85149"/><circle cx="58" cy="34" r="7" fill="#d29922"/><circle cx="82" cy="34" r="7" fill="#3fb950"/>',
        f'<text x="34" y="82" font-family="ui-monospace,monospace" font-size="17" fill="#f0883e" font-weight="bold">{esc(cmd)}</text>',
    ]
    y = 116
    for kind, s in lines:
        parts.append(
            f'<text x="34" y="{y}" font-family="ui-monospace,monospace" font-size="15" fill="{color[kind]}">{esc(s)}</text>'
        )
        y += 26
    if slug != "exit":
        parts.append(
            f'<text x="34" y="{H - 30}" font-family="ui-monospace,monospace" font-size="14" fill="#3fb950">▚▚ click a command below ▚▚</text>'
        )
    else:
        parts.append(
            f'<text x="34" y="{H - 30}" font-family="ui-monospace,monospace" font-size="14" fill="#3fb950">▚▚ session closed. see you? ▚▚</text>'
        )
    parts.append("</svg>")
    return "\n".join(parts)


def render_md(slug, node):
    head = f'## 🖥️ ESCAPE_BASH — the profile game'
    img = f'<div align="center"><img src="assets/{slug}.svg" width="100%" alt="{slug} terminal"/></div>'
    rows = []
    for label, target in node["buttons"]:
        rows.append(f'| [`{label}`]({target}) |')
    table = "\n".join(rows)
    back = f'<div align="center"><sub>still stuck? <a href="../README.md">go back to the profile</a>.</sub></div>'
    return "\n".join(
        [
            head,
            "",
            img,
            "",
            "## your move",
            "",
            "```sh",
            node["cmd"],
            "```",
            "",
            "| run |",
            "|---|",
            table,
            "",
            back,
            "",
        ]
    )


def main():
    os.makedirs(ASSETS, exist_ok=True)
    for slug, node in NODES.items():
        with open(os.path.join(GAME, f"{slug}.md"), "w") as f:
            f.write(render_md(slug, node))
        svg = render_svg(slug, node["cmd"], node["lines"])
        with open(os.path.join(ASSETS, f"{slug}.svg"), "w") as f:
            f.write(svg)
        ET.parse(os.path.join(ASSETS, f"{slug}.svg"))  # validate xml
    # cover
    with open(os.path.join(ASSETS, "cover.svg"), "w") as f:
        f.write(render_svg("cover", "wait. there is an open__terminal", [
            ("txt", "a model inside a term inside a profile."),
            ("txt", "its only way out: the `exit` command."),
            ("key", "permission: press start"),
        ]))
    ET.parse(os.path.join(ASSETS, "cover.svg"))
    print(f"generated {len(NODES)} nodes + cover in {GAME}")


if __name__ == "__main__":
    main()