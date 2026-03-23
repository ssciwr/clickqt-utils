from __future__ import annotations

import os
from collections.abc import Iterable, Mapping
from typing import Callable, Any

import click


class PathWithExtensions(click.Path):
    """A ``click.Path`` variant that restricts accepted file extensions."""

    def __init__(
        self,
        *args: Any,
        file_extensions: Iterable[str] | Mapping[Iterable[str], str] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.file_extension_groups = self._normalize_extension_groups(file_extensions)
        self.file_extensions = tuple(
            dict.fromkeys(
                extension
                for extension_group, _group_name in self.file_extension_groups
                for extension in extension_group
            )
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

    def _normalize_extension_groups(
        self,
        file_extensions: Iterable[str] | Mapping[Iterable[str], str] | None,
    ) -> tuple[tuple[tuple[str, ...], str], ...]:
        if file_extensions is None:
            return ()

        if isinstance(file_extensions, Mapping):
            return tuple(
                (self._normalize_extensions(extensions), group_name)
                for extensions, group_name in file_extensions.items()
            )

        normalized_extensions = self._normalize_extensions(file_extensions)
        if not normalized_extensions:
            return ()
        return ((normalized_extensions, "Allowed Files"),)

    @staticmethod
    def _normalize_extensions(file_extensions: Iterable[str]) -> tuple[str, ...]:
        return tuple(
            extension.lower() if extension.startswith(".") else f".{extension.lower()}"
            for extension in file_extensions
        )
