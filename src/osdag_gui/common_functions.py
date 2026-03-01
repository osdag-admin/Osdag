import os
import sys
import shutil
import subprocess
from importlib import resources

def design_examples(self):
    try:
        resource_dir = resources.files(
            "osdag_core.data.ResourceFiles.design_example._build.html"
        )

        with resources.as_file(resource_dir) as temp_path:

            app_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
            target_dir = os.path.join(app_dir, "design_examples")

            # Copy once
            if not os.path.exists(target_dir):
                shutil.copytree(temp_path, target_dir, dirs_exist_ok=True)

            index_file = os.path.join(target_dir, "index.html")

            if sys.platform.startswith("win"):
                os.startfile(index_file)
            elif sys.platform == "darwin":
                subprocess.call(["open", index_file])
            else:
                subprocess.call(["xdg-open", index_file])

    except Exception as e:
        print("Error opening design examples:", e)
