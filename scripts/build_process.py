"""從 log.md 與 WORKFLOW.md 產生 docs/process.html（不手動轉寫紀錄）。"""
import html, re, sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")

def mermaid_blocks(md):
    return re.findall(r"```mermaid\n(.*?)```", md, re.S)

def pill(result):
    r = result.strip()
    if r.startswith("PASS") and "FAIL" not in r:
        cls = "pass"
    elif r.startswith("FAIL") and "PASS" not in r:
        cls = "fail"
    elif r in ("—", "-", ""):
        return "—"
    else:
        cls = "mix"
    return f'<span class="pill {cls}">{html.escape(r)}</span>'

def inline_md(s):
    s = html.escape(s)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", s)

def log_rows(md):
    rows = []
    for line in md.splitlines():
        if not line.startswith("| 20"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
        if len(cells) != 5:
            raise SystemExit(f"bad log row: {line}")
        t, node, res, why, act = cells
        rows.append(f'      <tr><td class="t">{html.escape(t)}</td><td><b>{inline_md(node)}</b></td>'
                    f"<td>{pill(res)}</td><td>{inline_md(why)}</td><td>{inline_md(act)}</td></tr>")
    return rows

def main():
    tpl = (ROOT / "work" / "process.template.html").read_text(encoding="utf-8")
    wf = (ROOT / "WORKFLOW.md").read_text(encoding="utf-8")
    blocks = mermaid_blocks(wf)
    if len(blocks) < 2:
        raise SystemExit("WORKFLOW.md needs v1 and v2 mermaid blocks")
    rows = log_rows((ROOT / "log.md").read_text(encoding="utf-8"))
    out = (tpl.replace("{{MERMAID_V1}}", blocks[0].strip())
              .replace("{{MERMAID_V2}}", blocks[1].strip())
              .replace("{{LOG_ROWS}}", "\n".join(rows))
              .replace("{{LOG_COUNT}}", str(len(rows))))
    assert "{{" not in out, "unfilled placeholder"
    (ROOT / "docs" / "process.html").write_text(out, encoding="utf-8")
    print(f"process.html built: {len(rows)} log rows, {len(blocks)} mermaid blocks")

if __name__ == "__main__":
    main()
