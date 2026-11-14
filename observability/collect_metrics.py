#!/usr/bin/env python3
"""多席量化採集器 v1：agents/messages/PRs/code changes 每日快照
輸出：observability/snapshots/metrics-YYYY-MM-DD.csv（Databricks 上傳用）
"""
import json, os, subprocess, csv, datetime, sys

TODAY = datetime.date.today().isoformat()
OUT_DIR = "/Users/miku/Github/lexsi-safety-2026/observability/snapshots"
os.makedirs(OUT_DIR, exist_ok=True)

def sh(cmd, cwd=None):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return r.stdout.strip()

# 1) momotalk D1：席位數／訊息總數／今日訊息數
d1 = sh("""npx --yes wrangler d1 execute momotalk-bus --remote --json --command "
SELECT
 (SELECT COUNT(*) FROM agents) AS agents_total,
 (SELECT COUNT(*) FROM agents WHERE revoked=0) AS agents_active,
 (SELECT COUNT(*) FROM messages) AS messages_total,
 (SELECT COUNT(*) FROM messages WHERE date(created_at)=date('now','localtime')) AS messages_today
" """, cwd="/Users/miku/Github/momotalk-audit")
try:
    d1_rows = json.loads(d1)[0]["results"][0]
except Exception:
    print("D1 查詢失敗:", d1[:200]); d1_rows = {"agents_total": "?", "agents_active": "?", "messages_total": "?", "messages_today": "?"}

# 2) GitHub：PR 合併數（近 7 日）＋commits/additions/deletions（近 7 日，兩 repo）
repos = {"calpa-2023-website": "/Users/miku/Github/calpa-2023-website",
         "momotalk": "/Users/miku/Github/momotalk-audit"}
gh_rows = []
for repo, path in repos.items():
    prs = sh(f'gh pr list --repo itsuki2049/{repo} --state merged --limit 100 --json number,mergedAt --jq "[.[] | select(.mergedAt >= \\"2026-11-07\\")] | length"', cwd=path)
    log = sh(f'git log --since="7 days ago" --pretty=format:"%h|%ad" --numstat --date=iso', cwd=path)
    commits = len([l for l in log.split("\n") if "|" in l and len(l.split("|")[0]) == 7])
    adds = sum(int(p.split("\t")[0]) for p in log.split("\n") if "\t" in p and p.split("\t")[0].isdigit())
    dels = sum(int(p.split("\t")[1]) for p in log.split("\n") if "\t" in p and p.split("\t")[1].isdigit())
    gh_rows.append({"repo": repo, "prs_merged_7d": prs or 0, "commits_7d": commits, "additions_7d": adds, "deletions_7d": dels})

# 3) 輸出 CSV（Databricks 上傳格式）
rows = []
for g in gh_rows:
    rows.append({"date": TODAY, **d1_rows, **g})
csv_path = f"{OUT_DIR}/metrics-{TODAY}.csv"
with open(csv_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print("快照 ✓", csv_path)
print(json.dumps(rows, indent=1, ensure_ascii=False))


# 4) Databricks 推送（launchd 全自動段）：INSERT 今日快照
def push_databricks():
    tok_path = os.path.expanduser("~/.secrets/databricks.token")
    if not os.path.exists(tok_path):
        print("databricks token 不存在，跳過推送"); return
    token = open(tok_path).read().strip()
    host = "https://dbc-15afc093-a709.cloud.databricks.com"
    wh = "a69609e6d738a055"
    # 冪等：同日期重跑先刪舊列（重複插入防護）
    import urllib.request as _u
    _del = f"DELETE FROM workspace.yongle.team_metrics WHERE date = DATE('{TODAY}')"
    _req = _u.Request(f"{host}/api/2.0/sql/statements", method="POST",
        data=json.dumps({"warehouse_id": wh, "statement": _del, "wait": "45s", "format": "JSON_ARRAY"}).encode(),
        headers={"authorization": f"Bearer {token}", "content-type": "application/json"})
    with _u.urlopen(_req, timeout=90) as r:
        json.load(r)
    for g in gh_rows:
        stmt = (f"INSERT INTO workspace.yongle.team_metrics VALUES "
                f"(DATE('{TODAY}'),{d1_rows['agents_total']},{d1_rows['agents_active']},"
                f"{d1_rows['messages_total']},{d1_rows['messages_today']},"
                f"'{g['repo']}',{g['prs_merged_7d']},{g['commits_7d']},{g['additions_7d']},{g['deletions_7d']})")
        import urllib.request
        req = urllib.request.Request(f"{host}/api/2.0/sql/statements", method="POST",
            data=json.dumps({"warehouse_id": wh, "statement": stmt, "wait": "45s", "format": "JSON_ARRAY"}).encode(),
            headers={"authorization": f"Bearer {token}", "content-type": "application/json"})
        with urllib.request.urlopen(req, timeout=90) as r:
            st = json.load(r).get("status", {}).get("state")
            print(f"INSERT {g['repo']}: {st}")

push_databricks()
