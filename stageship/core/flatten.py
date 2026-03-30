import logging as _logging
from pathlib import Path as _Path

from pxr import Usd as _Usd


logger = _logging.getLogger(__name__)


def flatten(file, output=None):
    stage = _Usd.Stage.Open(file)

    if not output:
        extension = _Path(file).suffix
        output = _Path(file).with_suffix(f".flattened{extension}")
        _logging.debug(f"No output path provided, using {output} as output path")

    flattened_layer = stage.Flatten()
    flattened_layer.Export(str(output))
