from dataclasses import dataclass, field
from typing import List, Any

@dataclass
class DependencyData:
    sublayers: List[Any] = field(default_factory=list)
    references: List[Any] = field(default_factory=list)
    payloads: List[Any] = field(default_factory=list)
    textures: List[Any] = field(default_factory=list)

    def total_count(self) -> int:
        return len(self.sublayers) + len(self.references) + len(self.payloads) + len(self.textures)

    def summary(self) -> dict:
        return {
            "sublayers": len(self.sublayers),
            "references": len(self.references),
            "payloads": len(self.payloads),
            "textures": len(self.textures),
        }
