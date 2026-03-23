import click

from clickqt_utils.extensions import PathWithExtensions


@click.command(help="Validate and report extension-restricted input files.")
@click.option(
    "--input",
    "input_path",
    required=True,
    type=PathWithExtensions(
        exists=True,
        dir_okay=True,
        file_extensions={
            ("png", ".jpeg"): "Images",
            ("txt",): "Text Files",
        },
    ),
    help="Input file. Allowed: images (.png/.jpeg) or text (.txt).",
)
@click.option(
    "--mask",
    "mask_path",
    required=False,
    type=PathWithExtensions(
        exists=True,
        dir_okay=True,
        file_extensions=["png", "jpeg"],
    ),
    help="Optional mask image (.png/.jpeg).",
)
def cli(input_path: str, mask_path: str | None) -> None:
    click.echo(f"Input: {input_path}")
    if mask_path is not None:
        click.echo(f"Mask: {mask_path}")


if __name__ == "__main__":
    cli()
