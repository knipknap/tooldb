import os
import glob
from .. import Library, Tool

LIBRARY_EXT='.tbl'

class LinuxCNCSerializer():
    def __init__(self, path, *args, **kwargs):
        self.path = path
        self._init_tool_dir()

    def _init_tool_dir(self):
        if os.path.exists(self.path) and not os.path.isdir(self.path):
            raise ValueError(repr(self.path) + ' is not a directory')

        # Create subdir if it does not yet exist.
        os.makedirs(self.path, exist_ok=True)

    def _library_filename_from_id(self, id):
        return os.path.join(self.path, id+LIBRARY_EXT)

    def _get_library_ids(self):
        files = glob.glob(os.path.join(self.path, '*'+LIBRARY_EXT))
        return sorted(os.path.basename(os.path.splitext(f)[0])
                      for f in files if os.path.isfile(f))

    def _remove_library_by_id(self, id):
        filename = self._library_filename_from_id(id)
        os.remove(filename)

    def serialize_libraries(self, libraries):
        existing = set(self._get_library_ids())
        for library in libraries:
            self.serialize_library(library)
            if library.id in existing:
                existing.remove(library.id)
        for id in existing:
            self._remove_library_by_id(id)

    def deserialize_libraries(self):
        return [] # Not implemented

    def serialize_library(self, library):
        filename = self._library_filename_from_id(library.id)
        with open(filename, 'w') as fp:
            for tool in library.tools:
                fp.write("T{} P{} D{} ;{}\n".format(
                    tool.pocket,
                    tool.pocket,
                    tool.diameter,
                    tool.label
                ))

    def deserialize_library(self, id):
        raise NotImplemented()

    def deserialize_shapes(self):
        # In LinuxCNC, shapes cannot exist on their own outside a library.
        # So nothing to be done here.
        return []

    def serialize_shape(self, shape):
        # In LinuxCNC, shapes cannot exist on their own outside a library.
        # So nothing to be done here.
        return

    def deserialize_shape(self, attrs):
        # In LinuxCNC, shapes cannot exist on their own outside a library.
        # So nothing to be done here.
        return

    def deserialize_tools(self):
        # In LinuxCNC, tools cannot exist on their own outside a library.
        # So nothing to be done here.
        return []

    def serialize_tool(self, tool):
        # In LinuxCNC, tools cannot exist on their own outside a library.
        # So nothing to be done here.
        return

    def deserialize_tool(self, attrs):
        # In LinuxCNC, tools cannot exist on their own outside a library.
        # So nothing to be done here.
        return