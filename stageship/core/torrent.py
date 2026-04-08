import libtorrent as _lt
import logging as _logging
import os as _os

from pathlib import Path as _Path


logger = _logging.getLogger(__name__)


def create_torrent(file: str, output: str = None) -> str:
    """
    Create a torrent file for the given file. This will create a torrent file that can be used to share the file with
    others.

    :param file: The file to create a torrent for
    :param output: The output file for the torrent (default: <input>.torrent)
    :return: The path to the created torrent file
    """
    if not _os.path.exists(file):
        raise FileNotFoundError(f"File {file} does not exist")

    fs = _lt.file_storage()
    _lt.add_files(fs, file)

    creator = _lt.create_torrent(fs)
    creator.set_creator("stageship")

    _lt.set_piece_hashes(creator, _os.path.dirname(file))

    torrent = creator.generate()
    logger.info(f"Generated torrent...")

    if not output:
        output = _Path(file).with_suffix(".torrent")

    with open(output, "wb") as f:
        f.write(_lt.bencode(torrent))
        logger.info(f"Saved torrent to {output}")

    return str(output)
