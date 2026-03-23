from __future__ import annotations

import os
from typing import Iterable, Callable, Any

import click


class PathWithExtensions(click.Path):
    """A ``click.Path`` variant that restricts accepted file extensions."""

    def __init__(
        self,
        *args: Any,
        file_extensions: Iterable[str] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.file_extensions = tuple(
            extension.lower() if extension.startswith(".") else f".{extension.lower()}"
            for extension in (file_extensions or ())
        )

        self.validation_callbacks: tuple[
            Callable[
                [
                    str | bytes | os.PathLike[str] | os.PathLike[bytes],
                    click.Parameter | None,
                    click.Context | None,
                ],
                None,
            ],
            ...,
        ] = (
            self._validate_not_directory,
            self._validate_file_extension,
        )

    def convert(
        self,
        value: str | bytes | os.PathLike[str] | os.PathLike[bytes],
        param: click.Parameter | None,
        ctx: click.Context | None,
    ) -> str | bytes | os.PathLike[str] | os.PathLike[bytes]:
        converted = super().convert(value, param, ctx)

        for validation_callback in self.validation_callbacks:
            validation_callback(converted, param, ctx)

        return converted

    def _validate_not_directory(
        self,
        value: str | bytes | os.PathLike[str] | os.PathLike[bytes],
        param: click.Parameter | None,
        ctx: click.Context | None,
    ) -> None:
        path = os.fspath(value)
        if os.path.isdir(path):
            self.fail(f"{path!r} is a directory.", param, ctx)

    def _validate_file_extension(
        self,
        value: str | bytes | os.PathLike[str] | os.PathLike[bytes],
        param: click.Parameter | None,
        ctx: click.Context | None,
    ) -> None:
        if not self.file_extensions:
            return

        path = os.fspath(value)
        lower_path = os.fsdecode(path).lower()

        if any(lower_path.endswith(extension) for extension in self.file_extensions):
            return

        allowed_extensions = ", ".join(self.file_extensions)
        self.fail(
            f"{path!r} does not have one of the required extensions: {allowed_extensions}",
            param,
            ctx,
        )
