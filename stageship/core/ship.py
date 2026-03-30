import logging as _logging

from stageship.core import analyse as _analyse, flatten as _flatten, torrent as _torrent
from stageship.helpers.dependency_data import DependencyData
from stageship.helpers import confirmation as _confirmation


logger = _logging.getLogger(__name__)


def ship(file: str, flatten: bool = False, torrent: bool = False) -> None:
    logger.info(f"Shipping {file}...")

    dependencies = _analyse.analyse(file)
    if dependencies.total_count() > 0 and not flatten:
        _confirmation.confirm(f"{file} has {dependencies.total_count()} dependencies. Shipping without flattening may "
                              f"result in missing files. Would you like to flatten the stage now?")
        flatten = True

    if flatten:
        _flatten.flatten(file)

    if torrent:
        _torrent.create_torrent(file)

    logger.info(f"Finished shipping {file}...")
