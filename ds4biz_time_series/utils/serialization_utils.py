import json
import os



def serialize(path, obj):
    with open(os.path.join(path, "blueprint.json"), "w") as jf:
        json.dump(obj, jf, indent=2)


def deserialize(path):
    with open(os.path.join(path, "blueprint.json"), "r") as file:
        j = json.load(file)
    return j

