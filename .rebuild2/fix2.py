#!/usr/bin/env python3
import hashlib, os, subprocess, sys

WANT = "1e537f147dbb72676e14f8e354f1059822033866d4184641fae4f2ff15055bc4"
WANT_BYTES = 148955

def sh(cmd, check=True):
    return subprocess.run(cmd, check=check, capture_output=True, text=True)

def git_config():
    sh(["git", "config", "user.name", "github-actions[bot]"])
    sh(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"])

def fail(msg):
    os.makedirs(".rebuild2", exist_ok=True)
    with open(".rebuild2/STATUS.txt", "w", encoding="utf-8") as f:
        f.write("FAIL: " + msg + "\n")
    git_config()
    sh(["git", "add", "-A", ".rebuild2"], check=False)
    sh(["git", "commit", "-m", "chore: friends-apply fix failed [skip ci]"], check=False)
    sh(["git", "push"], check=False)
    print("FAILED:", msg)
    sys.exit(1)

def main():
    with open("index.html", "rb") as f:
        d = f.read()
    old_css = b'    #yueyue-preview .yy-friends-heading{display:flex;align-items:center;gap:8px}\n'
    add_css = (b'    #yueyue-preview .yy-friends-section .yy-friends-heading{flex-wrap:wrap}\n'
               b'    #yueyue-preview .yy-friends-apply{font-size:11px;font-weight:400;letter-spacing:0;opacity:.55}\n')
    old_html = '</svg>友情链接</h2>'.encode("utf-8")
    new_html = '</svg>友情链接<span class="yy-friends-apply">友链申请请联系</span></h2>'.encode("utf-8")
    if d.count(old_css) != 1:
        fail("old_css count=%d" % d.count(old_css))
    d = d.replace(old_css, old_css + add_css, 1)
    if d.count(old_html) != 1:
        fail("old_html count=%d" % d.count(old_html))
    d = d.replace(old_html, new_html, 1)
    got = hashlib.sha256(d).hexdigest()
    if len(d) != WANT_BYTES or got != WANT:
        fail("hash-mismatch len=%d sha=%s" % (len(d), got))
    with open("index.html", "wb") as f:
        f.write(d)
    git_config()
    sh(["git", "rm", "-r", "--quiet", ".rebuild2"], check=False)
    sh(["git", "add", "index.html"], check=True)
    c = sh(["git", "commit", "-m",
            "feat: add faint friends-apply note beside links heading [skip ci]"], check=False)
    if c.returncode != 0:
        print("nothing to commit")
        sys.exit(0)
    p = sh(["git", "push"], check=False)
    if p.returncode != 0:
        print(p.stdout)
        print(p.stderr)
        sys.exit(1)
    print("SUCCESS: friends-apply note added and pushed")

if __name__ == "__main__":
    main()
