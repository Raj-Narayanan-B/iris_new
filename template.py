import os

dirs = [
    os.path.join("data","raw"),
    os.path.join("data","processed"),
    "data_source",
    "saved_models",
    "notebooks",
    "src"
]

for i in dirs:
    os.makedirs(i,exist_ok=True)
    with open(os.path.join(i,".gitkeep"),"w"):
        pass

files = [
    "dvc.yaml",
    "params.yaml",
    ".gitignore",
    os.path.join("src","__init__.py")
]

for i in files:
    with open(i,"w"):
        pass