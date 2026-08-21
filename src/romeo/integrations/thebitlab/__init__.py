"""Official TheBitLab runtime plugin entry point."""

from romeo.integrations.thebitlab.plugin import RomeoRuntimePlugin


def create_plugin() -> RomeoRuntimePlugin:
    """Create the zero-argument plugin instance required by TheBitLab discovery."""

    return RomeoRuntimePlugin()


__all__ = ["RomeoRuntimePlugin", "create_plugin"]
