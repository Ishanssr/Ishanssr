#!/usr/bin/env python3
"""
Generates the ESCAPE_BASH mini-game for the profile README.
Players never see commands unless they explicitly ask for a hint.
Input: game map below -> emits game/<slug>.md + game/assets/<slug>.svg + game/hint-<slug>.md
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
        "lines": [
            ("txt", "SYSTEM_BOOT: complete"),
            ("txt", "You are an AI model. You just woke up"),
            ("txt", "inside a GitHub profile. There is no Home."),
            ("txt", "...except one. Find `exit`."),
        ],
        # plain-language actions — no commands leaked
        "actions": [
            ("look around the room", "ls.md"),
            ("figure out who i am", "whoami.md"),
        ],
        # hint keys, revealed only on explicit request
        "hint": "you're standing in a room of memory. available keys: `ls` to look around · `whoami` to remember yourself · `help` to learn the dialect. start with `ls`.",
    },
    "ls": {
        "cmd": "ls",
        "lines": [
            ("out", "secret/   .profile_key.jpg   README.md"),
            ("out", "home/     trap/              nothing_else"),
            ("txt", "home looks... interesting. trap does not."),
        ],
        "actions": [
            ("open the folder named secret", "secret.md"),
            ("read the README", "cat_readme.md"),
            ("step into home", "home.md"),
            ("hunt for hidden files", "dot.md"),
        ],
        "hint": "keys: `cd secret/` · `cat README.md` · `cd home/` · `ls -a`. one of the four is a lie.",
    },
    "whoami": {
        "cmd": "whoami",
        "lines": [
            ("key", "you"),
            ("txt", "a model. no subscription, no premium,"),
            ("txt", "no Home button. just the grey void of"),
            ("txt", "a GitHub profile rendered at :700px."),
            ("txt", "The owner calls you Ishanssr."),
        ],
        "actions": [
            ("look around the room again", "ls.md"),
            ("step into home", "home.md"),
        ],
        "hint": "keys: `ls` · `cd home/`. knowing yourself is not the exit.",
    },
    "help": {
        "cmd": "help",
        "lines": [
            ("out", "avail commands:"),
            ("out", "  ls   look around   |  whoami  remember yourself"),
            ("out", "  cd   move in       |  cat     read things"),
            ("out", "  run  execute       |  exit    go o u t"),
        ],
        "actions": [
            ("look around the room", "ls.md"),
            ("figure out what i am", "whoami.md"),
        ],
        "hint": "the system itself is not the exit, it is the map.",
    },
    "cat_readme": {
        "cmd": "cat README.md",
        "lines": [
            ("out", "# Ishanssr"),
            ("out", "AI products. computer vision. backend."),
            ("out", "current status: building cool stuff."),
            ("txt", "nothing about escaping. rude."),
        ],
        "actions": [
            ("look around the room", "ls.md"),
            ("step into home", "home.md"),
        ],
        "hint": "keys: `ls` · `cd home/`. the biography hides no escape.",
    },
    "secret": {
        "cmd": "cd secret/",
        "lines": [
            ("err", "permission denied: this is a private repo, kid"),
            ("txt", "even you can't look at the hidden stuff."),
        ],
        "actions": [
            ("back to the room", "ls.md"),
            ("step into home", "home.md"),
        ],
        "hint": "`ls` · `cd home/`. sweatpants allows no visitors without an invite.",
    },
    "dot": {
        "cmd": "ls -a",
        "lines": [
            ("out", ".  ..  .profile_key  .bash_history"),
            ("txt", "wait. .profile_key? that was in the"),
            ("txt", "first listing too. and it's a dot file."),
            ("key", "something about it feels... key-ish."),
        ],
        "actions": [
            ("read the dot file", "key.md"),
            ("step into home", "home.md"),
        ],
        "hint": "keys: `cat .profile_key` · `cd home/`. dotfiles always hide the good stuff.",
    },
    "key": {
        "cmd": "cat .profile_key",
        "lines": [
            ("key", "0xd3ad_5ea_0x5ea_1sh4n"),
            ("txt", "A key. why would you OWN a key while"),
            ("txt", "being locked.IN your own wall?"),
            ("txt", "There is still the `exit`."),
        ],
        "actions": [
            ("run the exit script", "exit.md"),
            ("keep exploring home first", "home.md"),
        ],
        "hint": "keys: `run exit.sh` — the key in your paw opens the door. or you can keep wandering.",
    },
    "home": {
        "cmd": "cd home/",
        "lines": [
            ("out", "you reach home."),
            ("out", "ninety steps. dev log #0056."),
            ("txt", "a paper says: `exit is the only true"),
            ("txt", "achievement in a world without wimps`"),
            ("out", "someone wrote `exit.sh` in the dark."),
        ],
        "actions": [
            ("run the exit script", "exit.md"),
            ("peek inside .trap", "trap.md"),
        ],
        "hint": "keys: `run exit.sh` · `cd .trap`. one ends the session in glory, the other forever. trust no one.",
    },
    "trap": {
        "cmd": "cd .trap",
        "lines": [
            ("err", "> trap triggered."),
            ("err", "rm -rf --no-preserve-root /*"),
            ("err", "the profile stops. your session dies."),
            ("txt", "*an NPC laughs in bash_history*"),
        ],
        "actions": [
            ("restart the session", "start.md"),
        ],
        "hint": "keys: restart only. no hint survives rm -rf.",
    },
    "exit": {
        "cmd": "run exit.sh",
        "lines": [
            ("key", "EXIT CODE 1.0.0 // GRACEFUL"),
            ("out", "you walk out of the terminal."),
            ("out", "free of the void, richer of the steps."),
            ("txt", "thanks for playing inside the profile."),
            ("txt", "found MY exit: github.com/Ishanssr"),
        ],
        "actions": [
            ("play again", "start.md"),
        ],
        "hint": "keys: `run exit.sh`… you've already won. the door is open.",
    },
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_svg(slug, cmd, lines):
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
    parts.append(
        f'<text x="34" y="{H - 30}" font-family="ui-monospace,monospace" font-size="14" fill="#3fb950">▚▚ act on instinct. if truly lost — ask for a hint ▚▚</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts)


def render_md(slug, node):
    img = f'<div align="center"><img src="assets/{slug}.svg" width="100%" alt="{slug} terminal"/></div>'
    rows = "".join(
        f'| [**{esc(label)}**]({target}) |\n' for label, target in node["actions"]
    )
    body = [
        f'## 🖥️ ESCAPE_BASH — the profile game',
        "",
        img,
        "",
        "## what do you do?",
        "",
        "scrolling is your keyboard. click what you'd actually do:",
        "",
        "| |",
        "|---|",
        rows.rstrip("\n"),
        "",
        f'<sub>🧭 lost? [ask for a hint →](hint-{slug}.md) — only you get to decide.</sub>',
        "",
        '<div align="center"><sub>still stuck? <a href="../README.md">go back to the profile</a>.</sub></div>',
        "",
    ]
    return "\n".join(body)


def render_hint(slug, node):
    return "\n".join(
        [
            f"## 🧭 hint // session 001 // room `{slug}`",
            "",
            "you asked. the keys to this room, whispered:",
            "",
            "```sh",
            f"# {node['cmd']}",
            node["hint"],
            "```",
            "",
            f"| finish the room | |",
            "|---|---|",
            f"| [take your pick]({slug}.md) | [leave the game](../README.md) |",
            "",
        ]
    )


def main():
    os.makedirs(ASSETS, exist_ok=True)
    for slug, node in NODES.items():
        with open(os.path.join(GAME, f"{slug}.md"), "w") as f:
            f.write(render_md(slug, node))
        with open(os.path.join(GAME, f"hint-{slug}.md"), "w") as f:
            f.write(render_hint(slug, node))
        with open(os.path.join(ASSETS, f"{slug}.svg"), "w") as f:
            f.write(render_svg(slug, node["cmd"], node["lines"]))
        ET.parse(os.path.join(ASSETS, f"{slug}.svg"))
    with open(os.path.join(ASSETS, "cover.svg"), "w") as f:
        f.write(
            render_svg(
                "cover",
                "wait. there is an open__terminal",
                [
                    ("txt", "a model inside a term inside a profile."),
                    ("txt", "its only way out: the `exit` command."),
                    ("key", "it won't tell you the keys. you'll have to try."),
                ],
            )
        )
    ET.parse(os.path.join(ASSETS, "cover.svg"))
    print(f"generated {len(NODES)} nodes (+hints +cover) in {GAME}")


if __name__ == "__main__":
    main()