import logging as _logging

from pxr import Usd as _Usd, Sdf as _Sdf, UsdShade as _UsdShade, UsdUtils as _UsdUtils, Ar as _Ar
from tqdm import tqdm as _tqdm

from stageship.helpers.dependency_data import DependencyData


logger = _logging.getLogger(__name__)


def analyse(file):
    logger.info(f"Analysing {file}...")

    stage = _Usd.Stage.Open(file)

    # dependencies = _UsdUtils.ComputeAllDependencies(file)
    # logger.debug("Dependencies: {}".format(dependencies))

    dependencies = {
        "sublayers": find_sublayers(stage),
        "references": find_references(stage),
        "payloads": find_payloads(stage),
        "textures": find_texture_dependencies(stage),
    }

    dependencies = DependencyData(**dependencies)
    logger.info(f"Found {dependencies.total_count()} dependencies")
    logger.info(f"Dependencies: {dependencies.summary()}")

    return dependencies

def find_sublayers(stage: _Usd.Stage) -> list:
    dependencies = []

    root = stage.GetRootLayer()
    for layer in root.subLayerPaths:
        if not layer: continue
        path = _Sdf.Layer.FindRelativeToLayer(root, layer)
        if path:
            dependencies.append(path)
            logger.debug(f"Found sublayer {path}")

    logger.info(f"Found {len(dependencies)} sublayers")
    return dependencies

def find_references(stage: _Usd.Stage) -> list:
    dependencies = []

    prims = list(stage.TraverseAll())

    for prim in _tqdm(prims, total=len(prims), desc="Searching for References"):
        for spec in prim.GetPrimStack():
            reference_list = spec.referenceList

            all_references = []
            all_references.extend(reference_list.prependedItems)
            all_references.extend(reference_list.explicitItems)
            all_references.extend(reference_list.orderedItems)

            for reference in all_references:
                dependencies.append(reference.assetPath)
                logger.debug(f"Reference Found: {reference.assetPath} on {prim.GetPath()}")

    logger.info(f"Found {len(dependencies)} references")
    return dependencies

def find_payloads(stage: _Usd.Stage) -> list:
    dependencies = []

    prims = list(stage.TraverseAll())

    for prim in _tqdm(prims, total=len(prims), desc="Searching for Payloads"):
        for spec in prim.GetPrimStack():
            payload_list = spec.payloadList

            all_payloads = []
            all_payloads.extend(payload_list.prependedItems)
            all_payloads.extend(payload_list.explicitItems)
            all_payloads.extend(payload_list.orderedItems)

            for payload in all_payloads:
                dependencies.append(payload.assetPath)
                logger.debug(f"Payload Found: {payload.assetPath} on {prim.GetPath()}")

    logger.info(f"Found {len(dependencies)} payloads")
    return dependencies

def find_texture_dependencies(stage: _Usd.Stage) -> list:
    dependencies = []

    material_prims = [prim for prim in stage.TraverseAll() if prim.IsA(_UsdShade.Material)]

    def find_texture_inputs(prim):
        for child in prim.GetChildren():
            if child.IsA(_UsdShade.Shader):
                file_input = child.GetProperty("inputs:file").Get() if child.HasProperty("inputs:file") else None
                if not (file_input and hasattr(file_input, "path")):
                    continue
                dependencies.append(file_input.path)
            elif child.IsA(_UsdShade.NodeGraph):
                find_texture_inputs(child)

    for prim in material_prims:
        find_texture_inputs(prim)

    logger.info(f"Found {len(dependencies)} texture dependencies")
    return dependencies
