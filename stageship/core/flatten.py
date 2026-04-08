import logging as _logging
from pathlib import Path as _Path

from pxr import Usd as _Usd


logger = _logging.getLogger(__name__)


def flatten(file, output=None) -> None:
    """
    Flatten a USD file, which will resolve all sublayers, references, and payloads into a single layer. This is useful
    for shipping a USD file, as it will ensure that all USD file dependencies are collapsed into the final file.

    :param file: The USD file to flatten
    :param output: The output file for the flattened USD (default: <input>_flattened.usd)
    :return: None
    """
    logger.info(f"Flattening {file}...")

    stage = _Usd.Stage.Open(file)

    if not output:
        extension = _Path(file).suffix
        output = _Path(file).with_suffix(f".flattened{extension}")
        _logging.warning(f"No output path provided, using {output} as output path")

    flattened_layer = stage.Flatten()
    flattened_layer.Export(str(output))

    logger.info(f"Flattened {file} to {output}")
