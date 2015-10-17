import os

def get_graphviz_path():
    options = [
        r"C:\Program Files (x86)\Graphviz2.38\bin\dot.exe",
        '/usr/bin/dot',
        ]
    for path in options:
        if os.path.exists(path):
            return path
    raise Exception("Couldn't find GraphViz")


