"""Generate an HTML supply-chain disruption report.

Usage:
    python generate_report.py
    python generate_report.py --input report.json --output disruption_report.html
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any


DEFAULT_OUTPUT = "disruption_report.html"


SAMPLE_REPORT: dict[str, Any] = {
    "report_id": "SCR-001",
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "news_headline": "Port disruption delays inbound component shipments",
    "risk_assessment": {
        "risk_type": "Port congestion",
        "severity": "High",
        "affected_country": "India",
        "confidence_score": 0.86,
    },
    "affected_suppliers": [
        {
            "supplier_name": "Global Components Ltd.",
            "country": "India",
            "tier": 1,
            "parts_affected": ["Semiconductor modules", "Control boards"],
        },
        {
            "supplier_name": "Precision Metals Co.",
            "country": "Vietnam",
            "tier": 2,
            "parts_affected": ["Stamped brackets", "Heat sinks"],
        },
    ],
    "alternative_suppliers": [
        {
            "supplier_name": "RapidSource Manufacturing",
            "country": "Malaysia",
            "parts_available": ["Control boards", "Heat sinks"],
            "lead_time_days": 12,
            "reliability_score": 0.91,
        },
        {
            "supplier_name": "NorthStar Electronics",
            "country": "Thailand",
            "parts_available": ["Semiconductor modules"],
            "lead_time_days": 18,
            "reliability_score": 0.84,
        },
    ],
    "recovery_time_days": 21.5,
    "executive_summary": (
        "The disruption is expected to create short-term delays for Tier-1 and "
        "Tier-2 suppliers. Alternative suppliers are available, but lead times "
        "should be monitored closely until port throughput stabilizes."
    ),
}


def safe_text(value: Any) -> str:
    """Convert a value to escaped HTML text."""
    if value is None:
        return ""
    return escape(str(value))


def format_percent(value: Any) -> str:
    try:
        return f"{float(value) * 100:.0f}%"
    except (TypeError, ValueError):
        return safe_text(value)


def format_list(values: Any) -> str:
    if not values:
        return "<span class=\"muted\">None listed</span>"

    if not isinstance(values, list):
        return safe_text(values)

    items = "".join(f"<li>{safe_text(item)}</li>" for item in values)
    return f"<ul>{items}</ul>"


def load_report(input_path: str | None) -> dict[str, Any]:
    if not input_path:
        return SAMPLE_REPORT

    path = Path(input_path)
    with path.open("r", encoding="utf-8") as file:
        report = json.load(file)

    if not isinstance(report, dict):
        raise ValueError("Input JSON must contain one report object.")

    return report


def normalize_report(report: Any) -> dict[str, Any]:
    if isinstance(report, dict):
        return report

    if hasattr(report, "model_dump"):
        return report.model_dump()

    if hasattr(report, "dict"):
        return report.dict()

    raise TypeError("Report must be a dictionary or a Pydantic model.")


def render_affected_suppliers(suppliers: list[dict[str, Any]]) -> str:
    if not suppliers:
        return "<tr><td colspan=\"4\" class=\"muted\">No affected suppliers listed.</td></tr>"

    rows = []
    for supplier in suppliers:
        rows.append(
            "<tr>"
            f"<td>{safe_text(supplier.get('supplier_name'))}</td>"
            f"<td>{safe_text(supplier.get('country'))}</td>"
            f"<td>Tier {safe_text(supplier.get('tier'))}</td>"
            f"<td>{format_list(supplier.get('parts_affected'))}</td>"
            "</tr>"
        )
    return "".join(rows)


def render_alternative_suppliers(suppliers: list[dict[str, Any]]) -> str:
    if not suppliers:
        return "<tr><td colspan=\"5\" class=\"muted\">No alternative suppliers listed.</td></tr>"

    rows = []
    for supplier in suppliers:
        rows.append(
            "<tr>"
            f"<td>{safe_text(supplier.get('supplier_name'))}</td>"
            f"<td>{safe_text(supplier.get('country'))}</td>"
            f"<td>{format_list(supplier.get('parts_available'))}</td>"
            f"<td>{safe_text(supplier.get('lead_time_days'))}</td>"
            f"<td>{format_percent(supplier.get('reliability_score'))}</td>"
            "</tr>"
        )
    return "".join(rows)


def render_html(report: dict[str, Any]) -> str:
    risk = report.get("risk_assessment") or {}
    affected_suppliers = report.get("affected_suppliers") or []
    alternative_suppliers = report.get("alternative_suppliers") or []

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Supply Chain Disruption Report</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #18202f;
      --muted: #667085;
      --line: #d8dee9;
      --panel: #ffffff;
      --page: #f5f7fa;
      --accent: #0f766e;
      --accent-soft: #d9f4ef;
      --danger: #b42318;
      --warning: #b54708;
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      background: var(--page);
      color: var(--ink);
      font-family: Arial, Helvetica, sans-serif;
      line-height: 1.5;
    }}

    .page {{
      width: min(1120px, calc(100% - 32px));
      margin: 32px auto;
    }}

    header {{
      display: grid;
      gap: 12px;
      padding: 28px;
      background: #102033;
      color: #ffffff;
      border-radius: 8px;
    }}

    h1, h2, h3, p {{
      margin: 0;
    }}

    h1 {{
      font-size: clamp(28px, 4vw, 44px);
      line-height: 1.1;
      letter-spacing: 0;
    }}

    h2 {{
      margin-bottom: 16px;
      font-size: 22px;
    }}

    .meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      color: #d9e7f7;
      font-size: 14px;
    }}

    .grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 16px;
      margin: 18px 0;
    }}

    .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 20px;
    }}

    .metric {{
      min-height: 112px;
    }}

    .label {{
      color: var(--muted);
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: .04em;
    }}

    .value {{
      margin-top: 8px;
      font-size: 26px;
      font-weight: 700;
    }}

    .badge {{
      display: inline-flex;
      align-items: center;
      min-height: 30px;
      padding: 4px 10px;
      border-radius: 999px;
      background: var(--accent-soft);
      color: var(--accent);
      font-weight: 700;
    }}

    .badge.high,
    .badge.critical {{
      background: #fee4e2;
      color: var(--danger);
    }}

    .badge.medium {{
      background: #fef0c7;
      color: var(--warning);
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      table-layout: fixed;
    }}

    th, td {{
      padding: 12px;
      border-top: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
      overflow-wrap: anywhere;
    }}

    th {{
      color: var(--muted);
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: .04em;
    }}

    ul {{
      margin: 0;
      padding-left: 18px;
    }}

    .section {{
      margin-top: 18px;
    }}

    .muted {{
      color: var(--muted);
    }}

    @media (max-width: 820px) {{
      .grid {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }}
    }}

    @media (max-width: 560px) {{
      .page {{
        width: min(100% - 20px, 1120px);
        margin: 16px auto;
      }}

      header,
      .panel {{
        padding: 16px;
      }}

      .grid {{
        grid-template-columns: 1fr;
      }}

      table,
      thead,
      tbody,
      tr,
      th,
      td {{
        display: block;
      }}

      thead {{
        display: none;
      }}

      tr {{
        border-top: 1px solid var(--line);
        padding: 10px 0;
      }}

      td {{
        border: 0;
        padding: 6px 0;
      }}
    }}
  </style>
</head>
<body>
  <main class="page">
    <header>
      <p class="badge">Report {safe_text(report.get("report_id"))}</p>
      <h1>{safe_text(report.get("news_headline"))}</h1>
      <div class="meta">
        <span>Generated: {safe_text(report.get("timestamp"))}</span>
        <span>Country: {safe_text(risk.get("affected_country"))}</span>
      </div>
    </header>

    <section class="grid" aria-label="Report metrics">
      <article class="panel metric">
        <p class="label">Risk Type</p>
        <p class="value">{safe_text(risk.get("risk_type"))}</p>
      </article>
      <article class="panel metric">
        <p class="label">Severity</p>
        <p class="value">
          <span class="badge {safe_text(risk.get("severity")).lower()}">{safe_text(risk.get("severity"))}</span>
        </p>
      </article>
      <article class="panel metric">
        <p class="label">Confidence</p>
        <p class="value">{format_percent(risk.get("confidence_score"))}</p>
      </article>
      <article class="panel metric">
        <p class="label">Recovery Time</p>
        <p class="value">{safe_text(report.get("recovery_time_days"))} days</p>
      </article>
    </section>

    <section class="panel section">
      <h2>Executive Summary</h2>
      <p>{safe_text(report.get("executive_summary"))}</p>
    </section>

    <section class="panel section">
      <h2>Affected Suppliers</h2>
      <table>
        <thead>
          <tr>
            <th>Supplier</th>
            <th>Country</th>
            <th>Tier</th>
            <th>Parts Affected</th>
          </tr>
        </thead>
        <tbody>
          {render_affected_suppliers(affected_suppliers)}
        </tbody>
      </table>
    </section>

    <section class="panel section">
      <h2>Alternative Suppliers</h2>
      <table>
        <thead>
          <tr>
            <th>Supplier</th>
            <th>Country</th>
            <th>Parts Available</th>
            <th>Lead Time</th>
            <th>Reliability</th>
          </tr>
        </thead>
        <tbody>
          {render_alternative_suppliers(alternative_suppliers)}
        </tbody>
      </table>
    </section>
  </main>
</body>
</html>
"""


def write_report(report: Any, output_path: str) -> Path:
    path = Path(output_path)
    path.write_text(render_html(normalize_report(report)), encoding="utf-8")
    return path


def save_report(report: Any, output_path: str | None = None) -> str:
    report_data = normalize_report(report)
    report_id = report_data.get("report_id", "disruption_report")
    path = output_path or f"{report_id}.html"
    return str(write_report(report_data, path))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an HTML disruption report.")
    parser.add_argument("--input", help="Path to a JSON file containing report data.")
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Path for the generated HTML file. Defaults to {DEFAULT_OUTPUT}.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = load_report(args.input)
    output_path = write_report(report, args.output)
    print(f"HTML report generated: {output_path.resolve()}")


if __name__ == "__main__":
    main()
