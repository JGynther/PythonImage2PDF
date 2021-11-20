"""

(c) Joona Gynther
    joona@gynther.xyz
    https://github.com/JGynther

Simple python script to convert images into a pdf file.
Very much made for simply my own needs.

"""
from PIL import Image as PIL
from typing import List
from random import choice
import string
from os import system, name, path


# Set the default save path variable here
DEFAULT_SAVE_PATH = f"{path.expanduser('~')}/Downloads/"


# Convert PIL-modules default Image-class to a more readable format
# (To avoid using Image.Image everywhere!)
class Image:
    PIL.Image


# Parse raw input string into usable file paths.
def parse_file_paths(file_path_string: str) -> List[str]:
    file_paths: List[str] = []

    for path in file_path_string.split(" /"):
        if not path[0] == "/":
            path = "/" + path
        # On osx when dragging files to the terminal, system already tries to escape spaces in file names.
        # Which causes python to not be able to open said files. Hence need to remove backslashes.
        path = path.replace("\\", "").strip()
        file_paths.append(path)

    return file_paths


def get_file_paths_by_user_input(default_str: str = "Enter (or drag) file paths (then enter): ") -> List[str]:
    print(f"\n{default_str}")

    raw_input_string: str = ""

    while True:
        if raw_input_string != "":
            print("Press enter again to continue, or enter more files!")

        user_input: str = input("  -->  ")
        if user_input == "" and raw_input_string != "":
            break

        raw_input_string += user_input

    print("")

    return parse_file_paths(raw_input_string)


def convert_image(image: Image, format: str = "RGB") -> Image:
    return image.convert(format)


def create_image_list(file_paths: List[str]) -> List[Image]:
    images: List[Image] = []

    for path in file_paths:
        image: Image = PIL.open(path)
        image = convert_image(image)
        images.append(image)

    return images


def generate_random_file_name(size: int = 10) -> str:
    # Simple random string generator for file names
    # https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
    return "".join(choice(string.ascii_letters + string.digits) for _ in range(size))


def convert_images_to_pdf(images: List[Image], save_path: str = DEFAULT_SAVE_PATH) -> None:
    file_name: str = input("Enter file name (*.pdf): ").strip()

    if file_name == "":
        # If no file name is given, generate a random one
        file_name = generate_random_file_name()
        print(f"-- Generated random file name: {file_name}.pdf --")

    if not file_name[-4:] == ".pdf":
        # If file name is lacking the pdf extension, add it
        file_name += ".pdf"

    if input("Use default save path? (y/n): ") in ["y", "Y", ""]:
        file_name = save_path + file_name

    try:
        images[0].save(file_name, save_all=True, append_images=images[1:])
        print(f"\nImages saved to {file_name}\n")
    except OSError:
        print("Error: could not save images as pdf.")


def clear_screen():
    # Clear terminal screen
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")


def print_start_message():
    print("\n"+56*"=")
    print(" PythonImage2PDF v1.0 by JGynther (github.com/JGynther)")
    print(56*"="+"\n")


def main():
    clear_screen()
    print_start_message()

    file_paths: List[str] = get_file_paths_by_user_input()
    images: List[Image] = create_image_list(file_paths)
    convert_images_to_pdf(images)


if __name__ == "__main__":
    main()
