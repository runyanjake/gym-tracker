# generate_readme_table.py
import os
from utilities import safe_filename

folders = {
    "Volume": "output/volume",
    "Reps": "output/reps",
    "Weight": "output/weight_stats"
}

# Map normalized exercise name -> chart files by type
exercise_files = {}

for chart_type, folder in folders.items():
    if not os.path.exists(folder):
        continue
    for f in os.listdir(folder):
        if not f.endswith(".svg"):
            continue
            
        name = f[:-4]  # strip .svg

        name = safe_filename(name)
        if name not in exercise_files:
            exercise_files[name] = {}
        exercise_files[name][chart_type] = os.path.join(folder, f)

# Helper for HTML img with width
def img_tag(path, width=200):
    return f'<img src="{path}" width="{width}"/>' if path else ""

# Build table rows
rows = []
for ex in sorted(exercise_files.keys()):
    files = exercise_files[ex]
    display_name = ex.replace("_", " ").title()
    rows.append(
        f"<tr><td>{display_name}</td>"
        f"<td>{img_tag(files.get('Volume'))}</td>"
        f"<td>{img_tag(files.get('Reps'))}</td>"
        f"<td>{img_tag(files.get('Weight'))}</td></tr>"
    )

# Full HTML table
table_html = (
    "<table>\n"
    "<tr><th>Exercise</th><th>Volume (total lbs)</th><th>Reps</th><th>Weight Stats (lbs)</th></tr>\n"
    + "\n".join(rows)
    + "\n</table>"
)

# Inject into README.md
readme_path = "README.md"
with open(readme_path, "r") as f:
    readme_content = f.read()

import re
pattern = r"<!-- CHARTS_TABLE_START -->.*<!-- CHARTS_TABLE_END -->"
replacement = f"<!-- CHARTS_TABLE_START -->\n{table_html}\n<!-- CHARTS_TABLE_END -->"

readme_content = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)

with open(readme_path, "w") as f:
    f.write(readme_content)

print("README.md updated with charts table.")