import numpy as np


def print_structure_shape(obj, depth=0, max_depth=None, name="root"):
    spacer = "  " * depth

    # Stop recursion and do NOT print anything if max_depth reached
    if max_depth is not None and depth >= max_depth:
        return

    if isinstance(obj, dict):
        print(f"{spacer}{name}: dict, len={len(obj)}")
        for key, value in obj.items():
            print_structure_shape(value, depth + 1, max_depth, name=repr(key))

    elif isinstance(obj, list):
        print(f"{spacer}{name}: list, len={len(obj)}")
        for idx, item in enumerate(obj):
            print_structure_shape(item, depth + 1, max_depth, name=f"[{idx}]")

    elif isinstance(obj, np.ndarray):
        print(f"{spacer}{name}: ndarray, shape={obj.shape}")

    else:
        print(f"{spacer}{name}: {type(obj).__name__}")
