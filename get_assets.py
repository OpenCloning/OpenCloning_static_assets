import json
import shutil
import subprocess
from pathlib import Path


def run(cmd, cwd=None):
    subprocess.run(cmd, check=True, cwd=cwd)


def copy_item(src: Path, dst: Path) -> None:
    if src.is_dir():
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def main() -> None:
    project_root = Path.cwd()
    assets_dir = project_root / "assets"
    temp_dir = project_root / "temp"

    assets_dir.mkdir(parents=True, exist_ok=True)
    if temp_dir.exists():
        shutil.rmtree(temp_dir)

    # Copy top-level files
    shutil.copyfile(project_root / "index.html", assets_dir / "index.html")
    shutil.copyfile(project_root / "_headers", assets_dir / "_headers")

    # Load versions.json
    with open(project_root / "versions.json", "r", encoding="utf-8") as f:
        versions = json.load(f)

    for dir_name, info in versions.items():
        target_base = assets_dir / dir_name
        target_base.mkdir(parents=True, exist_ok=True)

        repo_url = info.get("repository")
        commit_hash = info.get("commit")
        paths = info.get("paths", [])

        print("--------------------------------")
        print(f"Repository: {repo_url}")
        print(f"Commit: {commit_hash}")

        # Clone and checkout
        repo_temp_dir = temp_dir
        if repo_temp_dir.exists():
            shutil.rmtree(repo_temp_dir)
        run(["git", "clone", repo_url, str(repo_temp_dir)])
        run(["git", "checkout", commit_hash], cwd=repo_temp_dir)

        # Copy listed paths preserving structure
        for path_str in paths:
            print(f"Copying {path_str}")
            src_path = repo_temp_dir / path_str
            dst_path = target_base / path_str
            copy_item(src_path, dst_path)

        # Clean up temp repo
        shutil.rmtree(repo_temp_dir, ignore_errors=True)

    # In the index.html, replace the <!-- tree --> section with the new dirlist
    dirlist = subprocess.run(
        ["tree", assets_dir], capture_output=True, text=True
    ).stdout
    with open(assets_dir / "index.html", "r", encoding="utf-8") as f:
        html = f.read()
    html = html.replace("<!-- tree -->", f"<!-- tree -->\n{dirlist}")
    with open(assets_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    main()
