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

warnings.filterwarnings("ignore")


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

    with open(image_path, "rb") as img_file:  # type: ignore
        return base64.b64encode(img_file.read()).decode("utf-8")


# %%
assert os.environ.get("GROQ_API_KEY"), (
    "GROQ_API_KEY not set. Please set it in your environment variables."
)
client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY"),  # Using GROQ free API provider
)

MODEL_NAME = (
    "meta-llama/llama-4-maverick-17b-128e-instruct"  # vision-enabled chat model
)


def call_api(user_prompt: str, image: Image):
    """Call the LLM generation API"""
    base64_image = img_to_base64(img=image)
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
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
        description = response.choices[0].message.content

        if not description:
            raise ValueError("The description generated is empty")

        return description

    except Exception as e:
        print("Encountered unexpected error when calling the api: {e}")
        raise e


# %% [markdown]
# ## Loading Data

# %%
from earthkit.data import cache, config

config.set("cache-policy", "user")
cache.directory()

# %%
# Example, quickly accessible data
data = ek.data.from_source("sample", "era5-2t-msl-1985122512.grib")
data.ls()

# %%
# Copernicus datastore, requires API key set
dataset = "reanalysis-era5-single-levels"
request = {
    "product_type": ["reanalysis"],
    "variable": ["2m_temperature", "mean_sea_level_pressure"],
    "year": ["2024"],
    "month": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"],
    "day": ["01"],
    "time": ["12:00"],
    "data_format": "grib",
    "download_format": "unarchived",
}

data = ek.data.from_source("cds", dataset, request)
data.ls()

# %% [markdown]
# ## Exploring GRIB data

# %% [markdown]
# When loaded through the `.from_source()` method, a GRIB file will yield a `GribFielList` object. Documentation available [here](https://earthkit-data.readthedocs.io/en/latest/guide/data_format/grib.html)
#
# Some information about fields and GRIB data:
# - The fields can be iterated through with for loops
# - A field represents a single meteorological phenomenon (like temperature), measured at a certain time, at a certain height, from a certain center

# %%
len(data)  # Number of fields

# %%
data.head()  # List first 5 fields and "some" metadata for each field

# %%
data.ls()  # List all fields and *some* metadata for each field

# %%
data.describe()  # Describe the fields

# %%
data[0].dump()  # Access different metadata namespaces

# %%
data[0].metadata(namespaces="statistics")

# %%
data.indices()  # List of the metadata and the values they can take

# %% [markdown]
# ## Earthkit-plot Quickplot API

# %%
data.head()

# %%
# Sub-select the data
sub_data = data.sel(param=["2t", "msl"], typeOfLevel="surface", dataDate=20240101)
sub_data.head()

# %%
buffer = BytesIO()
figure = ek.plots.quickplot(sub_data, domain=["France", "Greece"], mode="overlay")

figure.save(buffer, format="png")

buffer.seek(0)

img = PIL.Image.open(buffer)

# %%
figure.title()  # TODO: extract the string title

# %% [markdown]
# Observations:
# - Geographic information is represented almost purely visually (there are latitudes and longitudes information on the axes but they are hardly interpretable), so a model should recognize the domains, or have access to them in the forms of variable valuess, default being the whole world
# - Pressure values are only represented as visual isobars, which might be the information the hardest to understand visually. A better approach could be to use the data values.
# - Temperature values are visually represented with a gradient of colors, and a clear legend. I think it would be quite easily interpreted by a model.
# - Title provides important context about the information represented and metadata such as the date. It should probably be transmitted to an end user. It can be accessed visually but also through the figure attributes.
# - In the end, the goal of interpreting this type of images could be phrased as "understanding the spatial distribution of meteorological variables."

# %% [markdown]
# ## Trying a Simple VLLM Summary Generation

# %% [markdown]
# Observations (from a very simple prompt):
# - Good structured and objective documentation of visual elements
# - Can accurately identify technical components of scientific visualizations
# - Remains cautious about making interpretive claims beyond what's explicitly shown
# - Prioritizes factual accuracy over speculative analysis
#
# These first observations are promising. We now need to try a generation with a more specialized prompt, including best prompt-engineering techniques from the start.

# %%
task_prompt = """# Instructions for Describing Meteorological Visualizations for Blind Scientists

Your task is to create a comprehensive, scientifically accurate description of meteorological visualizations that will be accessible to blind scientists. 

"""

method_prompt = """## Method

To achieve this task, you will work in two three steps. 
1. Understanding the information of the visualization
2. Planning your description
3. Writing your description

First,reflect on the meteorological visualizations and the metadata provided, step by step, critically, and without omitting any detail, to make sure you understand them and the key information they convey.

Once you've completed your full breakdown of the visualization and the metadata, you should be able to write a comprehensive, scientifically accurate description of the visualization. 

So you will once again start a reflection process, to plan what you will convey and how you will convey it in the desciption, in order to respect the requirements established previously 

"""

requirements_prompt = """## Requirements

Here are requirements that you will have to follow rigorously when writing your description.

### 1. Structural Organization
- Begin with a concise overview (2-3 sentences) stating the visualization type, geographic region, time period, and primary variables displayed.
- Organize your description hierarchically from most to least scientifically significant features.
- Structure your description in clearly defined sections with standardized headings.

### 2. Scientific Content Requirements
- Use precise meteorological terminology consistent with scientific publications.
- Always include quantitative values with appropriate units (hPa for pressure, K/°C for temperature).
- Describe patterns and gradients rather than individual data points.
- Explicitly state the range of values shown for each variable.
- Identify and describe major meteorological features (high/low pressure systems, fronts, temperature gradients).
- Include geographic context using cardinal directions and recognized regional references.

### 3. Spatial Relationship Guidelines
- Systematically describe the geographic distribution of data using cardinal directions (N, S, E, W, NE, etc.).
- Reference latitude and longitude coordinates when describing specific features.
- Describe gradients and transitions using directional language (e.g., "increasing from south to north").
- Use recognized geographic features (countries, seas, mountain ranges) as reference points.

### 4. Pattern Description Protocol
- Identify dominant patterns for each variable (e.g., pressure systems, temperature fronts).
- Describe the spatial relationships between different variables (e.g., how temperature aligns with pressure systems).
- Communicate the intensity of gradients, using terms like "sharp gradient," "gentle slope," or "uniform distribution."
- Note any anomalies or unusual features in the data pattern.

### 5. Technical Elements
- Describe the scale and units prominently displayed in the visualization.
- Explain the visualization technique used for each variable (e.g., color gradient for temperature, contour lines for pressure).
- Note the resolution and any apparent limitations of the data.

### 6. Scientific Context
- Include relevant seasonal context (e.g., winter conditions for December visualization).
- Provide brief meteorological context for the significance of the date, if applicable.
- Relate the patterns shown to typical or expected meteorological conditions for the region and season.

### 7. Accessibility-Specific Considerations
- Use clear, unambiguous language that doesn't rely on visual references.
- Avoid phrases like "as you can see" or "looking at the map."
- Use directional and relative terms that don't require visual understanding.
- Ensure all information conveyed by color is also expressed verbally in terms of values and patterns.

### 8. Language Style
- Maintain a formal, scientific tone throughout.
- Use precise, concise language without unnecessary elaboration.
- Be objective in descriptions, clearly differentiating between observed data and interpretations.

"""

format_prompt = """"""

examples_prompt = """"""

user_prompt = (
    task_prompt + method_prompt + requirements_prompt + format_prompt + examples_prompt
)

# %%
description = call_api(user_prompt, img)

display_markdown(description)
