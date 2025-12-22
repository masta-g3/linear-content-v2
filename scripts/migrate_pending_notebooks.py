import json
import shutil
import re
from pathlib import Path


def slugify(text: str) -> str:
    """Simple slugify: lowercase, replace non-alnum with hyphen, collapse repeats."""
    text = text.lower()
    # Replace non-alphanumeric with hyphen
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text


def build_yaml_front_matter(fm: dict) -> str:
    """Return a YAML front-matter block (including --- separators) as a single string."""
    lines = ["---"]
    for key in ("title", "date", "description", "categories", "slug"):
        if key in fm and fm[key] not in (None, ""):
            value = fm[key]
            # Properly quote strings, format lists
            if isinstance(value, str):
                # Use json.dumps for robust quoting/escaping
                value = json.dumps(value)
            elif isinstance(value, list):
                # Format list for YAML inline list
                value = "[" + ", ".join(map(str, value)) + "]"
            else:
                # Assume other types are okay as is (e.g., dates)
                value = str(value)
            lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines)


def migrate_notebooks(pending_dir: Path = Path("pending"), posts_dir: Path = Path("posts")) -> None:
    if not pending_dir.exists():
        print(f"Pending directory '{pending_dir}' does not exist. Nothing to migrate.")
        return

    posts_dir.mkdir(exist_ok=True)

    for nb_path in pending_dir.glob("*.ipynb"):
        print(f"Processing {nb_path} …")
        # Load notebook JSON (avoid heavy nbformat dependency)
        with nb_path.open(encoding="utf-8") as fp:
            nb = json.load(fp)

        fm = nb.get("metadata", {}).get("front-matter", {})
        if not fm:
            print(f"  Warning: No front-matter found in {nb_path}. Skipping.")
            continue

        # Extract required metadata
        title = fm.get("title") or nb_path.stem.replace("_", " ")
        date = fm.get("date")
        if not date:
            print(f"  Warning: No date in front-matter for {nb_path}. Skipping.")
            continue

        # Build slug
        slug = slugify(fm.get("slug", title))
        date_compact = date.replace("-", "")
        # If slug already begins with date, drop it to avoid duplication
        if slug.startswith(date_compact):
            slug = slug[len(date_compact) :].lstrip("-_")

        # Quarto prefers categories over tags for blog listings
        if "categories" not in fm:
            tags = fm.get("tags", [])
            if isinstance(tags, str):
                tags = [tags]
            fm["categories"] = tags
        # Remove legacy fields if desired
        fm.pop("tags", None)

        # Update slug in front-matter
        fm["slug"] = slug

        # Ensure updated front-matter saved back
        nb.setdefault("metadata", {})["front-matter"] = fm

        # Destination directory e.g. 20240322_slug
        dest_dir = posts_dir / f"{date_compact}_{slug}"
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest_nb = dest_dir / "index.ipynb"

        # Ensure YAML front-matter cell exists (at cell[0])
        cells = nb.get("cells", [])
        if cells and cells[0].get("cell_type") == "markdown" and cells[0]["source"][0].lstrip().startswith("---"):
            # Replace existing YAML cell
            cells[0]["source"] = [build_yaml_front_matter(fm) + "\n"]
        else:
            # Insert new markdown cell at top
            yaml_cell = {
                "cell_type": "markdown",
                "metadata": {},
                "source": [build_yaml_front_matter(fm) + "\n"],
            }
            nb["cells"] = [yaml_cell] + cells

        # Write updated notebook to destination
        with dest_nb.open("w", encoding="utf-8") as fp:
            json.dump(nb, fp, ensure_ascii=False, indent=1)
            fp.write("\n")

        print(f"  → Moved to {dest_nb}")

        # Remove original notebook
        nb_path.unlink()


def fix_existing_posts(posts_dir: Path = Path("posts")) -> None:
    """Rename directories with duplicate dates and ensure YAML front-matter cell exists."""
    for dir_path in posts_dir.iterdir():
        if not dir_path.is_dir():
            continue

        m = re.match(r"(?P<date>\d{8})_(?P<slug>.+)", dir_path.name)
        if not m:
            continue

        date_part = m.group("date")
        slug_part = m.group("slug")
        if slug_part.startswith(date_part):
            new_slug = slug_part[len(date_part) :].lstrip("-_")
            new_dir = posts_dir / f"{date_part}_{new_slug}"
            if not new_dir.exists():
                dir_path.rename(new_dir)
                dir_path = new_dir  # update reference

        nb_file = dir_path / "index.ipynb"
        if not nb_file.exists():
            continue
        with nb_file.open(encoding="utf-8") as fp:
            nb = json.load(fp)

        fm = nb.get("metadata", {}).get("front-matter", {})
        if not fm:
            continue

        # Insert / replace YAML cell same as in migrate
        cells = nb.get("cells", [])
        if cells and cells[0].get("cell_type") == "markdown" and cells[0]["source"][0].lstrip().startswith("---"):
            cells[0]["source"] = [build_yaml_front_matter(fm) + "\n"]
        else:
            yaml_cell = {
                "cell_type": "markdown",
                "metadata": {},
                "source": [build_yaml_front_matter(fm) + "\n"],
            }
            nb["cells"] = [yaml_cell] + cells

        with nb_file.open("w", encoding="utf-8") as fp:
            json.dump(nb, fp, ensure_ascii=False, indent=1)
            fp.write("\n")


if __name__ == "__main__":
    migrate_notebooks()
    fix_existing_posts() 