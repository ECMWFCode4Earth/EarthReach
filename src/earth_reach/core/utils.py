"""
Utility functions module.

Provides utility functions for image processing, file path operations,
and data format conversions.
"""

import base64

from io import BytesIO
from pathlib import Path

from PIL.ImageFile import ImageFile


def img_to_base64(image_path: str | None = None, img: ImageFile | None = None) -> str:
    """
    Convert an image to a base64 string.

    Args:
        image_path (str): The path to the image file. Either this or img must be provided.
        img (ImageFile | None): The image object. Either this or image_path must be provided.

    Returns:
        str: The base64 string representation of the image.
    """
    if image_path is None and img is None:
        raise ValueError("Either image_path or img must be provided.")

    if img is not None:
        bytes_io = BytesIO()
        img.save(bytes_io, format="PNG")
        return base64.b64encode(bytes_io.getvalue()).decode("utf-8")

    with open(image_path, "rb") as img_file:  # type: ignore
        return base64.b64encode(img_file.read()).decode("utf-8")


def img_to_bytes(img: ImageFile) -> bytes:
    """
    Convert a PIL Image to bytes for Gemini API.

    Args:
        img: ImageFile object

    Returns:
        bytes: Image as bytes
    """
    if img is None:
        raise ValueError("Image cannot be None")

    bytes_io = BytesIO()
    img.save(bytes_io, format="PNG")
    return bytes_io.getvalue()


def get_root_dir_path() -> Path:
    """Get the root directory path of the project."""

    return Path(__file__).parent.parent.parent.resolve()
