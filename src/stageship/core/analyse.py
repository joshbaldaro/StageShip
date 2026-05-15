import logging as _logging

from pxr import Usd as _Usd, Sdf as _Sdf, UsdShade as _UsdShade
from tqdm import tqdm as _tqdm

from stageship.helpers.dependency_data import DependencyData


logger = _logging.getLogger(__name__)


def analyse(file: str) -> DependencyData:
    """
    Analyse a USD file for external dependencies, including sublayers, references, payloads, and texture dependencies.

    :param file: The USD file to analyse
    :return: A DependencyData object containing the dependencies found in the USD file
    """
    logger.info(f"Analysing {file}...")

    stage = _Usd.Stage.Open(file)

    # Note: UsdUtils.ComputeAllDependencies can be used to find all dependencies, but provides less control and
    # visibility into the types of dependencies found. The custom functions below allow for more detailed logging and
    # categorization of dependencies.

    # dependencies = _UsdUtils.ComputeAllDependencies(file)
    # logger.debug("Dependencies: {}".format(dependencies))

    dependencies = {
        "sublayers": find_sublayers(stage),
        "references": find_references(stage),
        "payloads": find_payloads(stage),
        "textures": find_texture_dependencies(stage),
    }

    # Convert the dependency dictionary into a DependencyData object for easier handling and summary
    dependencies = DependencyData(**dependencies)
    logger.info(f"Found {dependencies.total_count} dependencies")
    logger.info(f"Dependencies: {dependencies.summary}")

    return dependencies


def find_sublayers(stage: _Usd.Stage) -> list:
    """
    Get the sublayers from the root layer of the stage. This only checks the root layer, as sublayers can themselves
    have sublayers, and we want to avoid infinite recursion. The dependencies found here will be included in the
    final dependency count, but we won't check for references or payloads in these sublayers, as they will be included
    in the final flattened stage if flattening is chosen.

    :param stage: The USD stage to analyse for sublayers
    :return: A list of sublayer paths found in the root layer of the stage
    """
    dependencies = []

    root = stage.GetRootLayer()
    for layer in root.subLayerPaths:
        if not layer: continue
        # FindRelativeToLayer will resolve the sublayer path relative to the root layer, which is important for
        # correctly indentifying whether the sublayer is an internal or external reference
        path = _Sdf.Layer.FindRelativeToLayer(root, layer)
        if path:
            dependencies.append(path)
            logger.debug(f"Found sublayer {path}")

    logger.info(f"Found {len(dependencies)} sublayers")

    return dependencies


def find_references(stage: _Usd.Stage) -> list:
    """
    Get the references from all prims in the stage. This checks all prims and their prim stacks for references.

    :param stage: The USD stage to analyse for references
    :return: A list of reference paths found in the stage
    """
    dependencies = []

    prims = list(stage.TraverseAll())

    for prim in _tqdm(prims, total=len(prims), desc="Searching for References"):
        for spec in prim.GetPrimStack():
            reference_list = spec.referenceList

            # The reference list can contain prepended, explicit, and ordered items, so we need to check all of them
            # for references
            all_references = []
            all_references.extend(reference_list.prependedItems)
            all_references.extend(reference_list.explicitItems)
            all_references.extend(reference_list.orderedItems)

            for reference in all_references:
                # Some references may not have an asset path, such as references to other prims in the same stage,
                # which we need to filter out to avoid false positives in our dependency count
                if not reference.assetPath:
                    continue
                if reference.assetPath not in dependencies:
                    dependencies.append(reference.assetPath)
                logger.debug(f"Reference Found: {reference.assetPath} on {prim.GetPath()}")

    logger.info(f"Found {len(dependencies)} references")
    return dependencies


def find_payloads(stage: _Usd.Stage) -> list:
    """
    Get the payloads from all prims in the stage. This checks all prims and their prim stacks for payloads.

    :param stage: The USD stage to analyse for payloads
    :return: A list of payload paths found in the stage
    """
    dependencies = []

    prims = list(stage.TraverseAll())

    for prim in _tqdm(prims, total=len(prims), desc="Searching for Payloads"):
        for spec in prim.GetPrimStack():
            payload_list = spec.payloadList

            # The payload list can contain prepended, explicit, and ordered items, so we need to check all of them
            # for payloads
            all_payloads = []
            all_payloads.extend(payload_list.prependedItems)
            all_payloads.extend(payload_list.explicitItems)
            all_payloads.extend(payload_list.orderedItems)

            for payload in all_payloads:
                # Some payloads may not have an asset path, such as payloads to other prims in the same stage,
                # which we need to filter out to avoid false positives in our dependency count
                if not payload.assetPath:
                    continue
                if payload.assetPath not in dependencies:
                    dependencies.append(payload.assetPath)
                logger.debug(f"Payload Found: {payload.assetPath} on {prim.GetPath()}")

    logger.info(f"Found {len(dependencies)} payloads")
    return dependencies


def find_texture_dependencies(stage: _Usd.Stage) -> list:
    """
    Get the texture dependencies from all materials in the stage. This checks all materials and their shader networks
    for file inputs that point to texture files. This is a more complex process than finding sublayers, references,
    and payloads, as there is no single API call to get all texture dependencies, and we need to traverse the shader
    networks of all materials to find them.

    :param stage: The USD stage to analyse for texture dependencies
    :return: A list of texture file paths found in the shader networks of all materials in the stage
    """
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

    for prim in _tqdm(material_prims, total=len(material_prims), desc="Searching for Texture Dependencies"):
        find_texture_inputs(prim)

    logger.info(f"Found {len(dependencies)} texture dependencies")
    return dependencies
