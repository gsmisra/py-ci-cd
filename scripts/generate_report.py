import os
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone

def parse_junit(junit_path: Path):
    if not junit_path.exists():
        return None
    tree = ET.parse(junit_path)
    root = tree.getroot()

    # supports <testsuite> or <testsuites>
    if root.tag == "testsuite":
        suites = [root]
    else:
        suites = root.findall("testsuite")

    totals = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0, "time": 0.0}
    for s in suites:
        totals["tests"] += int(s.attrib.get("tests", 0))
        totals["failures"] += int(s.attrib.get("failures", 0))
        totals["errors"] += int(s.attrib.get("errors", 0))
        totals["skipped"] += int(s.attrib.get("skipped", 0))
        totals["time"] += float(s.attrib.get("time", 0.0))

    return totals

def main():
    run_id = os.getenv("GITHUB_RUN_ID", "")
    sha = os.getenv("GITHUB_SHA", "")[:7]
    ref = os.getenv("GITHUB_REF_NAME", "")
    actor = os.getenv("GITHUB_ACTOR", "")
    workflow = os.getenv("GITHUB_WORKFLOW", "")
    event = os.getenv("GITHUB_EVENT_NAME", "")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    junit_unit = Path("artifacts/junit-unit.xml")
    junit_ct = Path("artifacts/junit-ct.xml")

    unit = parse_junit(junit_unit)
    ct = parse_junit(junit_ct)

    image = os.getenv("IMAGE_TAG", "n/a")
    deploy_env = os.getenv("DEPLOY_ENV", "n/a")
    deploy_status = os.getenv("DEPLOY_STATUS", "n/a")

    lines = []
    lines.append("# CI/CD/CT Report")
    lines.append("")
    lines.append(f"**Workflow:** {workflow}  ")
    lines.append(f"**Event:** {event}  ")
    lines.append(f"**Branch/Ref:** {ref}  ")
    lines.append(f"**Commit:** `{sha}`  ")
    lines.append(f"**Triggered by:** {actor}  ")
    lines.append(f"**Run ID:** {run_id}  ")
    lines.append(f"**Generated:** {now}  ")
    lines.append("")
    lines.append("## Test Summary")
    lines.append("")
    lines.append("| Suite | Tests | Failures | Errors | Skipped | Time (s) |")
    lines.append("|------:|------:|---------:|-------:|--------:|---------:|")

    def row(name, t):
        if not t:
            return f"| {name} | n/a | n/a | n/a | n/a | n/a |"
        return f"| {name} | {t['tests']} | {t['failures']} | {t['errors']} | {t['skipped']} | {t['time']:.2f} |"

    lines.append(row("Unit", unit))
    lines.append(row("CT (Contract)", ct))
    lines.append("")
    lines.append("## Build / Deploy")
    lines.append("")
    lines.append(f"- **Image Tag:** `{image}`")
    lines.append(f"- **Environment:** `{deploy_env}`")
    lines.append(f"- **Deploy Status:** `{deploy_status}`")
    lines.append("")
    report_md = "\n".join(lines)

    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/stakeholder-report.md").write_text(report_md, encoding="utf-8")

    # Also write to Job Summary if available
    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write(report_md + "\n")

if __name__ == "__main__":
    main()