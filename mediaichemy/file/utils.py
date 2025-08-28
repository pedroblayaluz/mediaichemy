import os


def get_next_available_path(base_path):
    if not os.path.exists(base_path):
        return base_path
    directory, filename = os.path.split(base_path)
    name, extension = split_name_extension(filename)
    counter = 1
    while True:
        new_filename = f"{name}({counter}){extension}"
        new_path = os.path.join(directory, new_filename)
        if not os.path.exists(new_path):
            return new_path
        counter += 1


def split_name_extension(filename):
    if '.' in filename and not filename.startswith('.'):
        name, extension = os.path.splitext(filename)
        return name, extension
    else:
        return filename, ""


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def delete_dir(path):
    os.rmdir(path)
