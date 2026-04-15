from dataclasses import dataclass, field
from typing import List, Any

@dataclass
class DependencyData:
    sublayers: List[Any] = field(default_factory=list)
    references: List[Any] = field(default_factory=list)
    payloads: List[Any] = field(default_factory=list)
    textures: List[Any] = field(default_factory=list)

    def __str__(self) -> str:
        return f"DependencyData(sublayers={len(self.sublayers)}, references={len(self.references)}, " \
               f"payloads={len(self.payloads)}, textures={len(self.textures)})"

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        return self.total_count

    @property
    def total_count(self) -> int:
        return self.sublayers_count + self.references_count + self.payloads_count + self.textures_count

    @property
    def layer_count(self) -> int:
        return self.sublayers_count + self.references_count + self.payloads_count

    @property
    def summary(self) -> dict:
        return {
            "sublayers": self.sublayers_count,
            "references": self.references_count,
            "payloads": self.payloads_count,
            "textures": self.textures_count,
        }

    @property
    def sublayers_count(self) -> int:
        return len(self.sublayers)

    @property
    def references_count(self) -> int:
        return len(self.references)

    @property
    def payloads_count(self) -> int:
        return len(self.payloads)

    @property
    def textures_count(self) -> int:
        return len(self.textures)

    @property
    def sublayers_summary(self) -> dict:
        return {
            "sublayers": self.sublayers_count,
            "sublayer_paths": self.sublayers,
        }

    @property
    def references_summary(self) -> dict:
        return {
            "references": self.references_count,
            "reference_paths": self.references,
        }

    @property
    def payloads_summary(self) -> dict:
        return {
            "payloads": self.payloads_count,
            "payload_paths": self.payloads,
        }

    @property
    def textures_summary(self) -> dict:
        return {
            "textures": self.textures_count,
            "texture_paths": self.textures,
        }
