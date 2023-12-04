import os
from pathlib import Path

import multivolumefile
from py7zr import FILTER_CRYPTO_AES256_SHA256, FILTER_ZSTD, SevenZipFile

from util.logging import log


def compress(target: Path, password: str, source: Path, volume: int = 25 * 1024 * 1024):
    filters = [{'id': FILTER_ZSTD}, {'id': FILTER_CRYPTO_AES256_SHA256}]
    with multivolumefile.open(target, mode='wb', volume=volume) as target_archive:
        with SevenZipFile(target_archive, mode='w', filters=filters, password=password) as archive:  # type: ignore
            archive.writeall(source, arcname=source.name)
            log(f'COMPRESSING: {source.name} -> {target.name}',
                *archive.getnames(), indent=True)

    # num_files = len(target_archive._files)  # type: ignore
    # target_files = [target.with_suffix(f".{i+1:04}") for i in range(num_files)]
    # return target_files

    return list(target.parent.glob(f"{target.stem}.*"))


def extract(target: Path, password: str, output: Path):
    filters = [{'id': FILTER_ZSTD}, {'id': FILTER_CRYPTO_AES256_SHA256}]
    with multivolumefile.open(target, mode='rb') as target_archive:
        with SevenZipFile(target_archive, mode='r', filters=filters, password=password) as archive:  # type: ignore
            log(f'EXTRACTING: {target.name} -> {output.name}',
                *archive.getnames(), indent=True)
            archive.extractall(output)


def empty_folder(target: Path):
    for f in Path(target).glob("*"):
        if f.is_file():
            f.unlink()

        elif f.is_dir():
            empty_folder(f)
            f.rmdir()
