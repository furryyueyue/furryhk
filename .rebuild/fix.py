#!/usr/bin/env python3
import hashlib, os, re, subprocess, sys

BASE = "127aedc"
WANT = "2c5eca6a007a016e663a1cc1fc1586b31bd3f6bc3b71ba18e1088674c7af5103"
WANT_BYTES = 148721

def sh(cmd, check=True):
    return subprocess.run(cmd, check=check, capture_output=True, text=True)

def git_config():
    sh(["git", "config", "user.name", "github-actions[bot]"])
    sh(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"])

def fail(msg):
    os.makedirs(".rebuild", exist_ok=True)
    with open(".rebuild/STATUS.txt", "w", encoding="utf-8") as f:
        f.write("FAIL: " + msg + "\n")
    git_config()
    sh(["git", "add", "-A", ".rebuild"], check=False)
    sh(["git", "commit", "-m", "chore: footer fix reported failure [skip ci]"], check=False)
    sh(["git", "push"], check=False)
    print("FAILED:", msg)
    sys.exit(1)

def main():
    orig = subprocess.run(["git", "show", BASE + ":index.html"],
                          check=True, capture_output=True).stdout
    d = orig
    pat = re.compile(rb'(yy-footer-filings">)<span>.*?</span>(<a class="yy-icp-link")')
    d, n = pat.subn(rb"\1\2", d, count=1)
    if n != 1:
        fail("remove-old-span count=%d" % n)
    anchor = b'yy-footer-filings">'
    gui = ('<a class="yy-icp-link" href="http://beian.miit.gov.cn/" target="_blank" '
           'rel="noopener noreferrer"><span>桂ICP备2026023237号</span></a>').encode("utf-8")
    if d.count(anchor) != 1:
        fail("anchor count=%d" % d.count(anchor))
    d = d.replace(anchor, anchor + gui, 1)
    got = hashlib.sha256(d).hexdigest()
    if len(d) != WANT_BYTES or got != WANT:
        fail("hash-mismatch len=%d sha=%s" % (len(d), got))
    with open("index.html", "wb") as f:
        f.write(d)
    git_config()
    sh(["git", "rm", "-r", "--quiet", ".rebuild"], check=False)
    sh(["git", "add", "index.html"], check=True)
    c = sh(["git", "commit", "-m",
            "chore: footer filings inline; restore full index [skip ci]"], check=False)
    if c.returncode != 0:
        print("nothing to commit")
        sys.exit(0)
    p = sh(["git", "push"], check=False)
    if p.returncode != 0:
        print(p.stdout)
        print(p.stderr)
        sys.exit(1)
    print("SUCCESS: index.html restored and pushed")

if __name__ == "__main__":
    main()
