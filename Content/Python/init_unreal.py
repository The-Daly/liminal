import sys
from pathlib import Path

import unreal

project_dir = Path(unreal.Paths.project_dir())
scripts_dir = project_dir / "scripts"
content_python_dir = project_dir / "Content" / "Python"

for path in (str(scripts_dir), str(content_python_dir)):
    if path not in sys.path:
        sys.path.insert(0, path)

import ld_datatable_rows  # noqa: E402,F401
import ld_menu_runtime  # noqa: E402
import ld_playable_loop_runtime  # noqa: E402


ld_menu_runtime.register()
ld_playable_loop_runtime.register()
