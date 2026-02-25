# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import csv
from pathlib import Path


def build_xray_queries(
    role_title: str,
    required_skills: str,
    locations: str = "Chile OR Miami OR Spain",
    extra_keywords: str = "family office OR shared services",
) -> list[str]:
  """Builds Google X-Ray query templates for talent sourcing.

  Args:
    role_title: The role to source.
    required_skills: Comma-separated required skills.
    locations: Boolean location expression.
    extra_keywords: Optional business keywords.

  Returns:
    A list of query strings to run in Google.
  """
  skills = [skill.strip() for skill in required_skills.split(",") if skill.strip()]
  skill_block = " OR ".join(f'"{skill}"' for skill in skills)

  base = (
      'site:linkedin.com/in ("{role}" OR "Head of Shared Services" '
      'OR "Operations Manager") ({locations}) ({extra})'
  )

  queries = [
      base.format(
          role=role_title,
          locations=locations,
          extra=extra_keywords,
      ),
      (
          f'site:linkedin.com/in ("{role_title}") '
          f'("treasury" OR "back office" OR "middle office") '
          f'({locations}) -jobs -hiring'
      ),
  ]

  if skill_block:
    queries.append(
        f'site:linkedin.com/in ("{role_title}") ({skill_block}) '
        f'({locations}) -jobs -recruiter'
    )

  return queries


def export_candidates_to_csv(
    filename: str,
    headers: str,
    rows: str,
    output_dir: str = "artifacts",
) -> str:
  """Exports candidate rows into an Excel-compatible CSV file.

  Args:
    filename: Output file name (for example `wildsur_xray.csv`).
    headers: Comma-separated headers.
    rows: Newline-separated rows where each row is `|`-separated.
    output_dir: Relative directory for output.

  Returns:
    Absolute path of the generated CSV.
  """
  output_path = Path(output_dir)
  output_path.mkdir(parents=True, exist_ok=True)

  safe_name = Path(filename).name
  if not safe_name.endswith(".csv"):
    safe_name = f"{safe_name}.csv"

  header_values = [value.strip() for value in headers.split(",")]
  parsed_rows = []
  for line in rows.splitlines():
    stripped = line.strip()
    if not stripped:
      continue
    parsed_rows.append([cell.strip() for cell in stripped.split("|")])

  destination = output_path / safe_name
  with destination.open("w", newline="", encoding="utf-8") as file_obj:
    writer = csv.writer(file_obj)
    writer.writerow(header_values)
    writer.writerows(parsed_rows)

  return str(destination.resolve())
