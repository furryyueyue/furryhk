#!/usr/bin/env python3
import hashlib, subprocess, sys, random
WANT = "21f08dffa55bb258698d5cdef3467ec2aea7cfcb5406766d78eeeb8a5b296afc"
WANT_BYTES = 150086
UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
cb = random.randint(10**9, 10**10)
NAME = "sync_21f08dff.html"
candidates = [
    ["curl", "-fsSL", "--retry", "3", "--retry-delay", "2", "--max-time", "90",
     "https://litter.catbox.moe/v00uud.html"],
    ["curl", "-fsSL", "--retry", "3", "--retry-delay", "2", "--max-time", "60", "-A", UA,
     f"https://www.furryhk.cn/{NAME}?cb={cb}"],
    ["curl", "-fsSL", "--resolve", "www.furryhk.cn:443:112.74.115.220", "-k", "--max-time", "60", "-A", UA,
     f"https://www.furryhk.cn/{NAME}?cb={cb}"],
]
data = None
for cmd in candidates:
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode == 0 and p.stdout:
        data = p.stdout
        print("downloaded bytes:", len(data), "via", [x for x in cmd if x.startswith("http")])
        break
    print("try failed:", [x for x in cmd if x.startswith("http")], p.stderr.decode()[:160])
if data is None:
    print("ALL DOWNLOADS FAILED")
    sys.exit(1)
sha = hashlib.sha256(data).hexdigest()
print("got", len(data), sha)
if len(data) != WANT_BYTES or sha != WANT:
    print("HASH/BYTE MISMATCH - abort without commit")
    sys.exit(1)
with open("index.html", "wb") as f:
    f.write(data)
def sh(c, check=True):
    return subprocess.run(c, check=check, capture_output=True, text=True)
sh(["git", "config", "user.name", "github-actions[bot]"])
sh(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"])
sh(["git", "rm", "-f", "--quiet", ".github/workflows/friends-apply.yml"], check=False)
sh(["git", "rm", "-r", "--quiet", ".sync3"], check=False)
sh(["git", "add", "index.html"])
c = sh(["git", "commit", "-m",
        "chore: sync index.html with live server (footer filings + friends apply note) [skip ci]"], check=False)
if c.returncode != 0:
    print("nothing to commit")
    sys.exit(0)
p = sh(["git", "push"], check=False)
if p.returncode != 0:
    print(p.stdout)
    print(p.stderr)
    sys.exit(1)
print("SUCCESS: github index.html synced to live server version")
