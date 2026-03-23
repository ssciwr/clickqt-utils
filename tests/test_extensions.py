import click
import pytest

from click.testing import CliRunner
from clickqt_utils.extensions import PathWithExtensions


def test_path_with_extensions_stores_file_extensions():
    path_type = PathWithExtensions(file_extensions=["txt", ".csv"])

    assert path_type.file_extensions == (".txt", ".csv")
    assert path_type.file_extension_groups == (((".txt", ".csv"), "Allowed Files"),)
    assert path_type.validation_callbacks[1] == path_type._validate_file_extension


def test_path_with_extensions_stores_extension_groups_for_dialog():
    path_type = PathWithExtensions(
        file_extensions={
            ("png", ".JPEG"): "Images",
            ("txt",): "Text Files",
        }
    )

    assert path_type.file_extensions == (".png", ".jpeg", ".txt")
    assert path_type.file_extension_groups == (
        ((".png", ".jpeg"), "Images"),
        ((".txt",), "Text Files"),
    )


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


def test_path_with_extensions_accepts_grouped_extensions(tmp_path):
    image_file = tmp_path / "photo.JPEG"
    image_file.write_text("img", encoding="utf-8")
    text_file = tmp_path / "readme.txt"
    text_file.write_text("txt", encoding="utf-8")

    path_type = PathWithExtensions(
        file_extensions={
            ("png", ".jpeg"): "Images",
            ("txt",): "Text Files",
        },
        exists=True,
    )

    assert path_type.convert(str(image_file), None, None) == str(image_file)
    assert path_type.convert(str(text_file), None, None) == str(text_file)


def test_path_with_extensions_rejects_directories(tmp_path):
    input_dir = tmp_path / "folder.txt"
    input_dir.mkdir()

    path_type = PathWithExtensions(file_extensions=[".txt"], exists=True)

    with pytest.raises(click.BadParameter, match="directory"):
        path_type.convert(str(input_dir), None, None)


@click.command()
@click.argument(
    "path",
    type=PathWithExtensions(file_extensions=[".txt"], exists=True),
)
def cli(path):
    click.echo(path)


def test_path_with_extensions_click_cli_system(tmp_path):
    runner = CliRunner()

    valid_file = tmp_path / "valid.txt"
    valid_file.write_text("ok", encoding="utf-8")
    valid_result = runner.invoke(cli, [str(valid_file)])
    assert valid_result.exit_code == 0
    assert str(valid_file) in valid_result.output

    invalid_file = tmp_path / "invalid.csv"
    invalid_file.write_text("no", encoding="utf-8")
    invalid_result = runner.invoke(cli, [str(invalid_file)])
    assert invalid_result.exit_code != 0
    assert "required extensions" in invalid_result.output

    invalid_dir = tmp_path / "folder.txt"
    invalid_dir.mkdir()
    dir_result = runner.invoke(cli, [str(invalid_dir)])
    assert dir_result.exit_code != 0
    assert "is a directory" in dir_result.output


def test_path_with_extensions_grouped_extensions_click_cli_system(tmp_path):
    @click.command()
    @click.argument(
        "path",
        type=PathWithExtensions(
            file_extensions={
                ("png", ".jpeg"): "Images",
                ("txt",): "Text Files",
            },
            exists=True,
        ),
    )
    def grouped_cli(path):
        click.echo(path)

    runner = CliRunner()

    image_file = tmp_path / "photo.png"
    image_file.write_text("image", encoding="utf-8")
    image_result = runner.invoke(grouped_cli, [str(image_file)])
    assert image_result.exit_code == 0

    invalid_file = tmp_path / "archive.zip"
    invalid_file.write_text("zip", encoding="utf-8")
    invalid_result = runner.invoke(grouped_cli, [str(invalid_file)])
    assert invalid_result.exit_code != 0
    assert "required extensions" in invalid_result.output
