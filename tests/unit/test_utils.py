import logging
import zipfile
from pathlib import Path

from gerador_readme_ia_web.utils import extract_project_data_from_zip


def test_extract_project_data_from_zip_returns_content(tmp_path: Path) -> None:
    zip_path = tmp_path / "project.zip"
    with zipfile.ZipFile(zip_path, "w") as zip_file:
        zip_file.writestr("README.md", "# Demo")
        zip_file.writestr("src/main.py", "print('hello')")

    output = extract_project_data_from_zip(str(zip_path), logging.getLogger("test"))

    assert output is not None
    assert "README.md" in output
    assert "src/main.py" in output


def test_extract_project_data_from_zip_handles_bad_zip(tmp_path: Path) -> None:
    invalid_zip_path = tmp_path / "invalid.zip"
    invalid_zip_path.write_text("not-a-zip", encoding="utf-8")

    output = extract_project_data_from_zip(str(invalid_zip_path), logging.getLogger("test"))

    assert output is None
