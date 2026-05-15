import logging as _logging
import os as _os

from stageship.core import analyse as _analyse, flatten as _flatten, torrent as _torrent, package as _package
from stageship.helpers import confirmation as _confirmation


logger = _logging.getLogger(__name__)


def ship(file: str, flatten: bool = False, package: bool = False, torrent: bool = False) -> None:
    """
    Ship a USD file and all its dependencies to a target location. This will analyse the USD file for dependencies.
    If flattening is not chosen, it will prompt the user to confirm that they want to ship without flattening, as this
    may result in missing files if the dependencies are not included in the target location. If flattening is chosen, it
    will flatten the USD file, which will resolve all sublayers, references, and payloads into a single layer. If torrent
    is chosen, it will create a torrent file for the USD file, which can be used to share the file with others.

    :param file: The USD file to ship
    :param flatten: Whether to flatten the USD file before shipping (default: False)
    :param package: Whether to create a package (e.g. zip) for the USD file and its dependencies (default: False)
    :param torrent: Whether to create a torrent file for the USD file (default: False)
    :return: None
    """
    logger.info(f"Shipping {file}...")

    dependencies = _analyse.analyse(file)
    if dependencies.layer_count > 0 and not flatten:
        flatten = _confirmation.confirm(f"{file} has {dependencies.total_count} dependencies. Shipping without flattening may "
                              f"result in missing files. Would you like to flatten the stage now?")

    if flatten:
        file = _flatten.flatten(file)

    if dependencies.textures_count > 0:
        package = _confirmation.confirm(f"Flattening does not resolve texture dependencies. Would you like to usd USD Zip to include "
                       f"textures in the shipped file?")

    if package:
        file = _package.package(file, dependencies=dependencies.textures)

    if torrent:
        _torrent.create_torrent(file)

    logger.info(f"Finished shipping {file}...")
