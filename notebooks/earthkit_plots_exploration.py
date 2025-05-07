# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.1
#   kernelspec:
#     display_name: .venv
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Earthkit Plots Exploration

# %% [markdown]
# ## Configuration & Imports

# %%
import base64
import os
import warnings
from io import BytesIO
from pathlib import Path
from typing import Literal

import earthkit as ek
import matplotlib.pyplot as plt
import openai
import PIL
from dotenv import load_dotenv
from IPython.display import Markdown, display
from PIL.Image import Image

load_dotenv(Path().cwd().parent / ".env")

warnings.filterwarnings("ignore", category=UserWarning)


# %%
def display_markdown(text: str) -> None:
    """
    Display a string as Markdown in a Jupyter notebook.

    Args:
        text (str): The text to display as Markdown.
    """
    display(Markdown(text))


def img_to_base64(image_path: str | None = None, img: Image | None = None) -> str:
    """
    Convert an image to a base64 string.

    Args:
        image_path (str): The path to the image file. Either this or img must be provided.
        img (PIL.Image): The image object. Either this or image_path must be provided.

    Returns:
        str: The base64 string representation of the image.
    """
    if image_path is None and img is None:
        raise ValueError("Either image_path or img must be provided.")

    if img is not None:
        bytes_io = BytesIO()
        img.save(bytes_io, format="PNG")
        return base64.b64encode(bytes_io.getvalue()).decode("utf-8")

    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


# %% [markdown]
# ## High-level API

# %%
data = ek.data.from_source("sample", "era5-2t-msl-1985122512.grib")
data.ls()

# %%
buffer = BytesIO()
ek.plots.quickplot(data, domain=["France", "Greece"], mode="overlay").save(
    buffer, format="png"
)

buffer.seek(0)

img = PIL.Image.open(buffer)

# %% [markdown]
# Observations:
# - Geographic information is represented almost purely visually (there are latitudes and longitudes information on the axes but they are hardly interpretable), so a model should recognize the domains, or have access to them in the forms of variable valuess, default being the whole world
# - Pressure values are only represented as visual isobars, which might be the information the hardest to understand visually. A better approach could be to use the data values.
# - Temperature values are visually represented with a gradient of colors, and a clear legend. I think it would be quite easily interpreted by a model.
# - Title provides important context about the information represented and metadata such as the date. It should probably be transmitted to an end user. It can be accessed visually but also through the figure attributes.
# - In the end, the goal of interpreting this type of images could be phrased as "understanding the spatial distribution of meteorological variables."

# %% [markdown]
# ## Trying a Simple VLLM Summary Generation

# %%
assert os.environ.get("GROQ_API_KEY"), (
    "GROQ_API_KEY not set. Please set it in your environment variables."
)
client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY"),  # Using GROQ free API provider
)

# %%
# img_path = Path().cwd().parent / 'data' / 'temperature_pressure_france_greece.png'
base64_image = img_to_base64(img=img)

response = client.chat.completions.create(
    model="meta-llama/llama-4-maverick-17b-128e-instruct",  # vision-enabled chat model
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        }
    ],
)

display_markdown(response.choices[0].message.content)

# %% [markdown]
# Observations (from a very simple prompt):
# - Good structured and objective documentation of visual elements
# - Can accurately identify technical components of scientific visualizations
# - Remains cautious about making interpretive claims beyond what's explicitly shown
# - Prioritizes factual accuracy over speculative analysis
#
# These first observations are promising. We now need to try a generation with a more specialized prompt, including best prompt-engineering techniques from the start.

# %%
# TODO: add the method (COT), response format, examples. The model boasts a huge context window so we should take advantage of it.
prompt = """# Instructions for Describing Meteorological Visualizations for Blind Scientists

Your task is to create a comprehensive, scientifically accurate description of meteorological visualizations that will be accessible to blind scientists. Follow these detailed guidelines:

## 1. Structural Organization
- Begin with a concise overview (2-3 sentences) stating the visualization type, geographic region, time period, and primary variables displayed.
- Organize your description hierarchically from most to least scientifically significant features.
- Structure your description in clearly defined sections with standardized headings.

## 2. Scientific Content Requirements
- Use precise meteorological terminology consistent with scientific publications.
- Always include quantitative values with appropriate units (hPa for pressure, K/°C for temperature).
- Describe patterns and gradients rather than individual data points.
- Explicitly state the range of values shown for each variable.
- Identify and describe major meteorological features (high/low pressure systems, fronts, temperature gradients).
- Include geographic context using cardinal directions and recognized regional references.

## 3. Spatial Relationship Guidelines
- Systematically describe the geographic distribution of data using cardinal directions (N, S, E, W, NE, etc.).
- Reference latitude and longitude coordinates when describing specific features.
- Describe gradients and transitions using directional language (e.g., "increasing from south to north").
- Use recognized geographic features (countries, seas, mountain ranges) as reference points.

## 4. Pattern Description Protocol
- Identify dominant patterns for each variable (e.g., pressure systems, temperature fronts).
- Describe the spatial relationships between different variables (e.g., how temperature aligns with pressure systems).
- Communicate the intensity of gradients, using terms like "sharp gradient," "gentle slope," or "uniform distribution."
- Note any anomalies or unusual features in the data pattern.

## 5. Technical Elements
- Describe the scale and units prominently displayed in the visualization.
- Explain the visualization technique used for each variable (e.g., color gradient for temperature, contour lines for pressure).
- Note the resolution and any apparent limitations of the data.

## 6. Scientific Context
- Include relevant seasonal context (e.g., winter conditions for December visualization).
- Provide brief meteorological context for the significance of the date, if applicable.
- Relate the patterns shown to typical or expected meteorological conditions for the region and season.

## 7. Accessibility-Specific Considerations
- Use clear, unambiguous language that doesn't rely on visual references.
- Avoid phrases like "as you can see" or "looking at the map."
- Use directional and relative terms that don't require visual understanding.
- Ensure all information conveyed by color is also expressed verbally in terms of values and patterns.

## 8. Language Style
- Maintain a formal, scientific tone throughout.
- Use precise, concise language without unnecessary elaboration.
- Be objective in descriptions, clearly differentiating between observed data and interpretations.
"""
