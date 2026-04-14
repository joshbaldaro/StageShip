import logging as _logging
import os as _os

from pxr import UsdUtils as _UsdUtils


logger = _logging.getLogger(__name__)


def package(file: str, output: str = None, dependencies: list[str] = None):

    if not output:
        output = file.replace(".usd", ".usdz")

    if not dependencies:
        _UsdUtils.CreateNewUsdzPackage(file, output)
        logger.info(f"Created new Usdz package {output}")
        return

    absolute = True
    for dependency in dependencies:
        if not _os.path.isabs(dependency) or not _os.path.exists(dependency):
            absolute = False
            logger.warning("Found dependency that is not an absolute path or does not exist, packaging unavailable")
            break

    if absolute:
        _UsdUtils.CreateNewUsdzPackage(file, output)
        logger.info(f"Created new Usdz package {output} with dependencies {dependencies}")
