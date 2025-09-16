import os, sys, subprocess

def design_examples(self):
    root_path = os.path.join('osdag_core','data','ResourceFiles', 'design_example', '_build', 'html')
    for html_file in os.listdir(root_path):
        if os.path.splitext(html_file)[1].lower() == '.html':
            full_path = os.path.join(root_path, html_file)
            if sys.platform.startswith("win"):
                os.startfile(full_path)
            elif sys.platform == "darwin":  # macOS
                subprocess.call(["open", full_path])
            else:  # Linux and others
                subprocess.call(["xdg-open", full_path])
