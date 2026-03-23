import click
import pytest

from clickqt_utils.extensions import PathWithExtensions


def test_path_with_extensions_stores_file_extensions():
    path_type = PathWithExtensions(file_extensions=["txt", ".csv"])

    assert path_type.file_extensions == (".txt", ".csv")
    assert path_type.validation_callbacks[1] == path_type._validate_file_extension


def test_path_with_extensions_accepts_matching_extension(tmp_path):
    input_file = tmp_path / "input.TXT"
    input_file.write_text("data", encoding="utf-8")

    path_type = PathWithExtensions(file_extensions=[".txt"], exists=True)

    assert path_type.convert(str(input_file), None, None) == str(input_file)


def test_path_with_extensions_rejects_wrong_extension(tmp_path):
    input_file = tmp_path / "input.csv"
    input_file.write_text("data", encoding="utf-8")

    path_type = PathWithExtensions(file_extensions=["txt"], exists=True)

    with pytest.raises(click.BadParameter, match="required extensions"):
        path_type.convert(str(input_file), None, None)


def test_path_with_extensions_rejects_directories(tmp_path):
    input_dir = tmp_path / "folder.txt"
    input_dir.mkdir()

    path_type = PathWithExtensions(file_extensions=[".txt"], exists=True)

    with pytest.raises(click.BadParameter, match="directory"):
        path_type.convert(str(input_dir), None, None)
