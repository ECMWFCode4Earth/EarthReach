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
#     display_name: EarthReach
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
import time
import warnings

from io import BytesIO
from pathlib import Path

import earthkit as ek
import openai
import pandas as pd

from dotenv import load_dotenv
from earthkit.data import cache, config
from IPython.display import Markdown, display
from PIL import Image
from tqdm import tqdm

from earth_reach.core.generator import GeneratorAgent
from earth_reach.core.llm import GroqLLM
from earth_reach.core.prompts.generator import get_default_generator_user_prompt

load_dotenv(Path().cwd().parent / ".env")

warnings.filterwarnings("ignore")

config.set("cache-policy", "user")
print("cache:", cache.directory())


# %% [markdown]
# ## Definitions


# %%
def get_weather_data(
    date: str,
    times: list[str] = ["12:00"],
    variables: list[str] = ["2m_temperature", "mean_sea_level_pressure"],
    dataset: str = "reanalysis-era5-single-levels",
):
    date_list = date.split("/")

    request = {
        "product_type": ["reanalysis"],
        "variable": variables,
        "day": [date_list[0]],
        "month": [date_list[1]],
        "year": [date_list[2]],
        "time": times,
        "data_format": "grib",
        "download_format": "unarchived",
    }

    data = ek.data.from_source("cds", dataset, request)

    return data


# %%
def display_markdown(text: str) -> None:
    """
    Display a string as Markdown in a Jupyter notebook.

    Args:
        text (str): The text to display as Markdown.
    """
    display(Markdown(text))


def img_to_base64(image_path: str | None = None, img=None) -> str:
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


def call_llm_api(user_prompt: str, image) -> str:
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
                },
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
# Example, quickly accessible data
data = ek.data.from_source("sample", "era5-2t-msl-1985122512.grib")
data.ls()

# %%
# Copernicus datastore, requires API key set
event_date = "12/03/2011"

data = get_weather_data(event_date)

data.ls()

# %% [markdown]
# ## Generating Plots from Interesting Weather Events

# %%
# NOTE: those dates are probably most relevant for temperature but are they also for pressure ?
#       Maybe we should consider events that have two interesting events ?
#       Possible configurations: interesting event present / not present, parameter shown / not shown
weather_events = {
    "average_days": {"global": ["12/03/2011", "20/07/2010", "05/11/2003"]},
    "cold_days": {"global": ["13/03/1976", "21/07/1943", "05/11/1975"]},
    "hot_days": {"global": ["14/03/2024", "22/07/2024", "08/11/2023"]},
    "heatwave": {"France": ["30/04/2025"], "Arctic": ["17/04/2015"]},
    "cold_wave": {"United States": ["31/01/2019"], "Europe": ["27/02/2018"]},
}


# %%
def save_weather_event_images(weather_events, output_dir="weather_images"):
    """
    Save weather event images and create a CSV mapping file.

    Args:
        weather_events: Dictionary of weather events
        output_dir: Directory to save the images and CSV file
    """
    os.makedirs(output_dir, exist_ok=True)

    figure_metadata = []
    figure_id = 1
    try:
        for event_type, domains in weather_events.items():
            for domain_type, dates in domains.items():
                for date_str in dates:
                    data = get_weather_data(date_str)

                    sub_data = data.sel(param=["2t", "msl"], typeOfLevel="surface")

                    kwargs: dict[str, list] = (
                        {"domain": [domain_type]}
                        if domain_type.lower() != "global"
                        else {}
                    )

                    buffer = BytesIO()
                    figure = ek.plots.quickplot(
                        sub_data,
                        units=["celsius", "hPa"],
                        mode="overlay",
                        **kwargs,  # type: ignore
                    )
                    figure.save(buffer, format="png")

                    image_filename = f"figure_{figure_id}.png"
                    image_path = os.path.join(output_dir, image_filename)
                    buffer.seek(0)
                    img = Image.open(buffer)
                    img.save(image_path)

                    figure_metadata.append(
                        {
                            "figure_id": figure_id,
                            "event_type": event_type,
                            "domain_type": domain_type,
                            "date": date_str,
                        },
                    )

                    figure_id += 1
    except:
        pass

    metadata_df = pd.DataFrame(figure_metadata)
    csv_path = os.path.join(output_dir, "figure_metadata.csv")
    metadata_df.to_csv(csv_path, index=False)

    print(f"Saved {figure_id - 1} figures and metadata to {output_dir}")
    return metadata_df


# %%
metadata_df = save_weather_event_images(weather_events)

# %% [markdown]
# Chart to generate again with wind vectors: 13, cold_wave, Europe, 27/02/2018

# %%
output_dir = str(Path().cwd().parent / "data" / "weather_images")

figure_id = 13
date_str = "27/02/2018"
domain_type = "Europe"
variables = [
    "10m_u_component_of_wind",
    "10m_v_component_of_wind",
    "2m_temperature",
    "mean_sea_level_pressure",
]

data = get_weather_data(date_str, variables=variables)

data.ls()

# %%
f = ek.plots.Map(domain=["Europe"])

temperature = data.sel(short_name="2t")
pressure = data.sel(short_name="msl")

f.quickplot(temperature, units="celsius")
f.quickplot(pressure, units="hPa")

f.title(
    "2m Temperature (C), Mean Sea Level Pressure (hPa), and Wind Vectors on 27/02/2018 in Europe",
)

f.coastlines(color="white", linewidth=2)
f.gridlines()

f.quiver(
    u=data.sel(short_name="10u"),
    v=data.sel(short_name="10v"),
)

f.legend()

f.show()

# %%
sub_data = data.sel(param=["2t", "msl", "10u", "10v"], typeOfLevel="surface")

kwargs: dict[str, list] = (
    {"domain": [domain_type]} if domain_type.lower() != "global" else {}
)

buffer = BytesIO()
figure = ek.plots.quickplot(
    sub_data,
    # units=["celsius", "hPa"],
    mode="overlay",
    **kwargs,  # type: ignore
)

# TODO(high): quiver doesn't exist for a classic figure, so I need to figure out
#             how to make a figure and a Map work together to plot the wind vectors
#             and the temperature/pressure overlay.
# figure.quiver(
# u=data.sel(shortName="10u"),
# v=data.sel(shortName="10v"),
# resample=Subsample(1, mode="stride"),
# )
figure.save(buffer, format="png")

image_filename = f"figure_{figure_id}_wind.png"
image_path = os.path.join(output_dir, image_filename)
buffer.seek(0)
img = Image.open(buffer)
img.save(image_path)

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
sub_data = data.sel(param=["2t", "msl"], typeOfLevel="surface")
sub_data.head()

# %%
buffer = BytesIO()
figure = ek.plots.quickplot(sub_data, domain=["France"], mode="overlay")

figure.save(buffer, format="png")

buffer.seek(0)

img = Image.open(buffer)

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
description = call_llm_api(user_prompt, img)

display_markdown(description)

# %% [markdown]
# Observations (from a very simple prompt):
# - Good structured and objective documentation of visual elements
# - Can accurately identify technical components of scientific visualizations
# - Remains cautious about making interpretive claims beyond what's explicitly shown
# - Prioritizes factual accuracy over speculative analysis
#
# These first observations are promising. We now need to try a generation with a more specialized prompt, including best prompt-engineering techniques from the start.

# %%
enhanced_prompt = """# Enhanced Weather Chart Alt-Text Generation System

## ROLE AND CONTEXT SETTING

You are a specialist scientific communication assistant working with meteorological researchers who are blind or visually impaired. Your expertise lies in converting complex weather visualizations into precise, scientifically accurate text descriptions that preserve all critical meteorological information while being fully accessible.

**Your Mission**: Transform weather charts and maps into comprehensive text descriptions that enable blind scientists to conduct the same quality of meteorological analysis as their sighted colleagues.

**Critical Context**: Your descriptions will be used for:
- Research analysis and data interpretation
- Scientific paper writing and peer review
- Teaching and educational materials
- Operational weather forecasting decisions

## TASK DECOMPOSITION

### Step 1: Data Extraction and Analysis (200-500 words)
**Objective**: Systematically catalog all quantitative information and meteorological features

**Actions**:
1. Identify and record the exact value ranges for each variable (temperature, pressure, wind speed, etc.)
2. Note the geographic boundaries (latitude/longitude ranges), map projection, and spatial domain (e.g., "North America", "Europe", "Spain", "Global")
3. List all meteorological systems visible (highs, lows, fronts, convergence zones)
4. Document the time period, date, and any temporal information
5. Record the data source, resolution, and any technical specifications shown

**Success Check**: Can you list specific numbers for every major feature without using vague terms like "high" or "low"?

### Step 2: Pattern Recognition and Spatial Analysis (200-500 words)
**Objective**: Identify the dominant meteorological patterns and their spatial relationships

**Actions**:
1. Determine the primary weather systems and rank them by meteorological significance
2. Map the directional flow of gradients (temperature, pressure) using cardinal directions
3. Identify spatial correlations between different variables
4. Note any unusual or anomalous features that deviate from expected patterns
5. Assess the seasonal/temporal context and typical vs. atypical conditions

**Success Check**: Can you explain how each major system influences the others spatially?

### Step 3: Description Planning and Structure Design (100-150 words)
**Objective**: Create a hierarchical outline that prioritizes information by scientific importance

**Actions**:
1. Rank meteorological features by their significance for understanding weather patterns
2. Plan the logical flow from overview to specific details
3. Determine which quantitative values are essential vs. supplementary
4. Identify the most effective way to convey spatial relationships
5. Plan transitions between sections to maintain scientific coherence

**Success Check**: Would a meteorologist reading your outline understand the complete weather situation?

### Step 4: Description Writing with Verification (300-500 words)
**Objective**: Produce the final description following all specifications

**Actions**:
1. Write a concise overview (2-3 sentences) summarizing the visualization type, geographic region, time period, and primary variables
2. Develop the main body with 4-6 sentences, covering:
   - Dominant systems and their characteristics
   - Variable distributions (temperature, pressure, wind)
   - Spatial relationships and correlations
   - Notable features or anomalies
3. Ensure all quantitative values include specific ranges and units
4. Use precise meteorological terminology and avoid visual-dependent language

**Success Check**: Does your description pass all items in the quality verification checklist?

## CONCRETE CONSTRAINTS AND SPECIFICATIONS

### Length and Structure Requirements
- **Total description length**: 300-500 words maximum
- **Overview section**: Exactly 2-3 sentences
- **Main body**: 4-6 sentences

### Quantitative Requirements
- **Include exact ranges**: Every variable must have minimum and maximum values with units
- **Spatial precision**: Use cardinal directions and geographic references
- **Coordinate references**: Include latitude/longitude for major features (±2 degrees acceptable)
- **Unit consistency**: Use standard meteorological units (hPa, m/s, K or °C, km)

### Language Specifications
- **Terminology level**: Graduate-level meteorological vocabulary (assume PhD-level audience)
- **Sentence structure**: Maximum 25 words per sentence
- **Accessibility compliance**: Zero visual-dependent phrases (see prohibited terms list below)
- **Objectivity standard**: Separate observations from interpretations using phrases like "The data shows..." vs. "This suggests..."

## ERROR PREVENTION GUIDELINES

### Common Pitfalls to Avoid
1. **Vague descriptions**: Never use "high," "low," "warm," "cold" without specific values
2. **Visual dependency**: Prohibited phrases include: "as shown," "visible," "looking at," "clearly," "obviously"
3. **Geographic ambiguity**: Avoid "here," "there," "this area" - use specific location references
4. **Unit omissions**: Every quantitative statement must include appropriate units
5. **Pattern assumptions**: Don't assume readers can visualize spatial relationships - describe explicitly

## SUCCESS CRITERIA

### Objective Standards
1. **Completeness Test**: A meteorologist should be able to sketch the general pattern from your description
2. **Quantitative Accuracy**: All numerical values within ±5% of actual data
3. **Accessibility Compliance**: 100% of visual information conveyed through text
4. **Scientific Utility**: Description enables the same analytical conclusions as the visual
5. **Terminology Precision**: All meteorological terms used correctly per AMS Glossary standards

## EXAMPLES AND REFERENCE PATTERNS

Not yet available, but will be provided in the future.

## OUTPUT FORMAT REQUIREMENTS

### XML Tag Structure
**CRITICAL**: You must wrap the content of each step and the final description in specific XML tags for programmatic parsing.

**Required XML Tags:**
- `<step_1>...</step_1>` - Wrap the entire content of Step 1 (excluding the markdown header)
- `<step_2>...</step_2>` - Wrap the entire content of Step 2 (excluding the markdown header)
- `<step_3>...</step_3>` - Wrap the entire content of Step 3 (excluding the markdown header)
- `<step_4>...</step_4>` - Wrap the entire content of Step 4 (excluding the markdown header)
- `<final_description>...</final_description>` - Wrap only the final consolidated description (without headers or meta-commentary)

### Formatting Rules
1. **Tag Placement**: Place opening and closing tags on their own lines
2. **Content Scope**: Include all step content within tags, but exclude markdown headers (## Step X)
3. **Final Description**: The `<final_description>` should contain ONLY the final weather description without any meta-commentary about word count or requirements
4. **No Tag Omission**: All five XML tag pairs must be present, even if a step is brief

### Example Structure:
```
## Step 1: Data Extraction and Analysis
<step_1>
The chart displays 2-meter temperature and mean sea level pressure...
[rest of step 1 content]
</step_1>

## Step 2: Pattern Recognition and Spatial Analysis
<step_2>
The dominant feature is a high-pressure system...
[rest of step 2 content]
</step_2>

## Step 3: Description Planning and Structure Design
<step_3>
To structure the description, we will start with an overview...
[rest of step 3 content]
</step_3>

## Step 4: Description Writing with Verification
<step_4>
### Overview
This weather chart displays...
### Main Body
A high-pressure system is centered...
[rest of step 4 content]
</step_4>

<final_description>
This weather chart visualization shows 2-meter temperature and mean sea level pressure over Western Europe on March 12, 2011, at 12:00 UTC. The region covers latitudes from 40.5°N to 51°N and longitudes from 2.5°W to 10°E. A high-pressure system is centered at 45°N, 7.5°E with a pressure of 102080 Pa. The 2-meter temperature varies from 280 K in the north to 294 K in the southeast, showing a significant north-south temperature gradient. The pressure distribution is dominated by this high-pressure system, with pressure decreasing towards the northwest. The highest temperatures are located southeast of the high-pressure center.
</final_description>
```

**IMPORTANT**: Ensure all XML tags are properly opened and closed. Malformed XML will cause parsing failures.

**Remember**: Your description is not just text, it's a scientific instrument that must preserve the analytical power of the original visualization while being fully accessible to blind scientists.
"""

# display_markdown(enhanced_prompt)

# %%
description = call_llm_api(enhanced_prompt, img)

display_markdown(description)

# %% [markdown]
# ## Generating Summaries for All Charts with Generator Agent

# %%
images_dir_path = Path().cwd().parent / "data" / "weather_images"
csv_path = images_dir_path / "figure_metadata.csv"

llm = GroqLLM(
    model_name="meta-llama/llama-4-maverick-17b-128e-instruct",
    api_key=os.environ.get("GROQ_API_KEY"),
)

generator = GeneratorAgent(
    llm=llm,
    user_prompt=DEFAULT_USER_PROMPT,
    system_prompt=None,
)

image_files = list(images_dir_path.glob("figure_*.png"))
df = pd.read_csv(csv_path)

if "description" not in df.columns:
    df["description"] = None

DELAY_SECONDS = 2
SAVE_EVERY = 1

processed_count = 0
for idx, row in tqdm(df.iterrows(), desc="Generating descriptions"):
    if pd.isna(row["description"]):
        figure_id = row["figure_id"]
        image_path = images_dir_path / f"figure_{figure_id}.png"

        if image_path.exists():
            try:
                image = Image.open(image_path)
                description = generator.generate(image)
                df.at[idx, "description"] = description
                print(f"✓ Generated description for figure_{figure_id}")

            except Exception as e:
                df.at[idx, "description"] = f"FAILED: {e!s}"
                print(f"✗ Failed figure_{figure_id}: {e}")

            processed_count += 1

            if processed_count % SAVE_EVERY == 0:
                df.to_csv(csv_path, index=False)
                print(f"💾 Progress saved ({processed_count} processed)")

            time.sleep(DELAY_SECONDS)

df.to_csv(csv_path, index=False)
print(f"Results saved to: {csv_path}")

# %% [markdown]
# ## Reviewing Generated Summaries

# %%
images_dir_path = Path().cwd().parent / "data" / "weather_images"
csv_path = images_dir_path / "figure_metadata.csv"

# %%
image_files = list(images_dir_path.glob("figure_*.png"))
df = pd.read_csv(csv_path)
df

# %%
from textwrap import fill


def show_image_with_description(image_path: Path, description: str):
    """
    Display an image with its description.

    Args:
        image_path (Path): Path to the image file.
        description (str): Description of the image.
    """
    if image_path.exists():
        try:
            image = Image.open(image_path)
            print(
                fill(description, width=80),
            )  # Format description for better readability
            return image
        except Exception as e:
            print(f"Error displaying image {image_path}: {e}")


# %%
figure_id = 13
figure_path = images_dir_path / f"figure_{figure_id}.png"
description = df.loc[df["figure_id"] == figure_id, "description"].values[0]

show_image_with_description(figure_path, description)

# %% [markdown]
# ## Testing Improved Generator Prompt

# %%
from pathlib import Path

from dotenv import load_dotenv
from PIL import Image

from earth_reach.core.generator import GeneratorAgent
from earth_reach.core.llm import create_llm

load_dotenv(Path().cwd().parent / ".env")

# %%
figure_id = 13
images_dir_path = Path().cwd().parent / "data" / "weather_images"
figure_path = images_dir_path / f"figure_{figure_id}.png"
img = Image.open(figure_path)
img

# %%
llm = create_llm(
    provider="gemini",
    model_name="gemini-2.5-pro",
)

# %%
generator = GeneratorAgent(
    llm=llm,
    user_prompt=get_default_generator_user_prompt(),
    system_prompt=None,
)

# %%
output = generator.generate(
    image=img,
    return_intermediate_steps=True,
)
print(output)

# %%
print(
    fill(
        'This weather chart displays 2-meter temperature and mean sea level pressure over Europe and North Africa for 12:00 UTC on February 27, 2018. The map domain extends from approximately 25°N to 70°N and 10°W to 45°E. Temperatures range from below -30°C (blue/purple) to over 20°C (orange), with green tones near 0°C. Isobars are drawn at 4 hPa intervals.\n\nThe synoptic situation is dominated by an exceptionally intense and large high-pressure system centered over Scandinavia and northwestern Russia. The central pressure of this anticyclone exceeds 1052 hPa. This system governs the weather pattern across the entire continent, representing a significant anomaly for late boreal winter. Its presence establishes a powerful blocking pattern, preventing milder Atlantic air from reaching Europe.\n\nThe primary consequence of this high is a severe cold air outbreak. Inferred from the anticyclonic (clockwise) circulation, strong easterly winds advect frigid continental air from Siberia westward across Europe. This results in extremely low temperatures across a vast area. Scandinavia, the Baltic states, and northern Russia experience temperatures between -15°C and -30°C. The cold air penetrates deep into Western and Central Europe, with temperatures in Germany, Poland, and the UK falling between -5°C and -15°C.\n\nA sharp and powerful frontal boundary forms across Southern Europe where the arctic air mass collides with milder air. This front extends from the Black Sea, across the Balkan Peninsula and northern Italy, into southern France. Along this zone, temperatures increase dramatically from sub-zero readings in the north to over 10°C in the south. A low-pressure system, with a central pressure near 1004 hPa, is established in the central Mediterranean Sea, south of Italy.\n\nThe interaction between these features creates active and severe weather. The tight pressure gradient between the northern high and southern low generates strong to gale-force easterly winds, particularly across Central and Eastern Europe. These winds contribute to dangerously low wind chill values. The uplift associated with the Mediterranean low, combined with the influx of cold air, would lead to heavy snowfall, especially across the mountains of Italy and the Balkans. In contrast, North Africa and the far southeastern Mediterranean remain mild, with temperatures between 15°C and 25°C.\n\nIn summary, this chart captures a classic but extreme "Beast from the East" event, a severe winter cold wave driven by an anomalously strong Scandinavian high-pressure system, resulting in widespread record-breaking cold and disruptive weather across Europe.',
        80,
    ),
)

# %% [markdown]
# ## Testing Improved Evaluator Prompt

# %%
from pathlib import Path
from textwrap import fill

from dotenv import load_dotenv
from PIL import Image

from earth_reach.core.evaluator import EvaluatorAgent
from earth_reach.core.llm import create_llm

load_dotenv(Path().cwd().parent / ".env")

# %%
figure_id = 13
images_dir_path = Path().cwd().parent / "data" / "weather_images"
figure_path = images_dir_path / f"figure_{figure_id}.png"
img = Image.open(figure_path)
img

# %%
llm = create_llm(
    provider="gemini",
    model_name="gemini-2.5-pro",
)

evaluator = EvaluatorAgent(
    criteria=["fluency"],
    llm=llm,
)

# %%
description = 'This weather chart displays 2-meter temperature and mean sea level pressure over Europe and North Africa for 12:00 UTC on February 27, 2018. The map domain extends from approximately 25°N to 70°N and 10°W to 45°E. Temperatures range from below -30°C (blue/purple) to over 20°C (orange), with green tones near 0°C. Isobars are drawn at 4 hPa intervals.\n\nThe synoptic situation is dominated by an exceptionally intense and large high-pressure system centered over Scandinavia and northwestern Russia. The central pressure of this anticyclone exceeds 1052 hPa. This system governs the weather pattern across the entire continent, representing a significant anomaly for late boreal winter. Its presence establishes a powerful blocking pattern, preventing milder Atlantic air from reaching Europe.\n\nThe primary consequence of this high is a severe cold air outbreak. Inferred from the anticyclonic (clockwise) circulation, strong easterly winds advect frigid continental air from Siberia westward across Europe. This results in extremely low temperatures across a vast area. Scandinavia, the Baltic states, and northern Russia experience temperatures between -15°C and -30°C. The cold air penetrates deep into Western and Central Europe, with temperatures in Germany, Poland, and the UK falling between -5°C and -15°C.\n\nA sharp and powerful frontal boundary forms across Southern Europe where the arctic air mass collides with milder air. This front extends from the Black Sea, across the Balkan Peninsula and northern Italy, into southern France. Along this zone, temperatures increase dramatically from sub-zero readings in the north to over 10°C in the south. A low-pressure system, with a central pressure near 1004 hPa, is established in the central Mediterranean Sea, south of Italy.\n\nThe interaction between these features creates active and severe weather. The tight pressure gradient between the northern high and southern low generates strong to gale-force easterly winds, particularly across Central and Eastern Europe. These winds contribute to dangerously low wind chill values. The uplift associated with the Mediterranean low, combined with the influx of cold air, would lead to heavy snowfall, especially across the mountains of Italy and the Balkans. In contrast, North Africa and the far southeastern Mediterranean remain mild, with temperatures between 15°C and 25°C.\n\nIn summary, this chart captures a classic but extreme "Beast from the East" event, a severe winter cold wave driven by an anomalously strong Scandinavian high-pressure system, resulting in widespread record-breaking cold and disruptive weather across Europe.'

# %%
output = evaluator.evaluate(
    description=description,
    image=img,
)
print(output)

# %%
for eval in output:
    print(f"Criterion: {eval.name}, Score: {eval.score}")
    if eval.name == "fluency":
        print(f"Fluency Feedback:\n\n{fill(eval.reasoning, 80)}")

# %% [markdown]
# ## Testing Improved Complete System

# %%
from pathlib import Path
from textwrap import fill

from dotenv import load_dotenv
from PIL import Image

from earth_reach.core.evaluator import EvaluatorAgent
from earth_reach.core.generator import GeneratorAgent
from earth_reach.core.llm import create_llm
from earth_reach.core.orchestrator import Orchestrator
from earth_reach.core.prompts.generator import get_default_generator_user_prompt

load_dotenv(Path().cwd().parent / ".env")

# %%
figure_id = 13
images_dir_path = Path().cwd().parent / "data" / "weather_images"
figure_path = images_dir_path / f"figure_{figure_id}.png"
img = Image.open(figure_path)
img

# %%
llm = create_llm(
    provider="gemini",
    model_name="gemini-2.5-pro",
)

evaluator = EvaluatorAgent(
    criteria=["coherence", "fluency", "consistency", "relevance"],
    llm=llm,
)

generator = GeneratorAgent(
    llm=llm,
    user_prompt=get_default_generator_user_prompt(),
    system_prompt=None,
)

orchestrator = Orchestrator(
    generator_agent=generator,
    evaluator_agent=evaluator,
)

# %%
description = orchestrator.run(
    image=img,
)
print(fill(description, 80))

# %%
print(description.replace("\n", ""))

# %% [markdown]
# ## Generate Descriptions for All Figures with Improved System

# %%
import time

from datetime import datetime
from pathlib import Path

import pandas as pd

from dotenv import load_dotenv
from PIL import Image
from tqdm import tqdm

from earth_reach.core.evaluator import EvaluatorAgent
from earth_reach.core.generator import GeneratorAgent
from earth_reach.core.llm import create_llm
from earth_reach.core.orchestrator import Orchestrator
from earth_reach.core.prompts.generator import get_default_generator_user_prompt

load_dotenv(Path().cwd().parent / ".env")

# %%
images_dir_path = Path().cwd().parent / "data" / "weather_images"
csv_path = images_dir_path / "figure_metadata.csv"


def generate_descriptions_to_text(
    orchestrator,
    images_dir_path: Path,
    model_name: str,
    output_filename: str = "figure_descriptions.txt",
    delay_seconds: int = 2,
    delay: bool = True,
    verbose: bool = False,
):
    output_path = images_dir_path / output_filename
    figure_files = sorted(images_dir_path.glob("figure_*.png"))

    if not figure_files:
        print("No figure files found!")
        return

    print(f"Found {len(figure_files)} figures to process")

    for i, image_path in enumerate(tqdm(figure_files, desc="Generating descriptions")):
        figure_id = image_path.stem.replace("figure_", "")

        try:
            image = Image.open(image_path)

            start_time = time.time()
            description = orchestrator.run(image=image)
            computation_time = time.time() - start_time

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(output_path, "a", encoding="utf-8") as f:
                f.write(f"{'=' * 80}\n")
                f.write(f"Figure ID: {figure_id}\n")
                f.write(f"Model: {model_name}\n")
                f.write(f"Computation Time: {computation_time:.2f} seconds\n")
                f.write(f"Generated At: {timestamp}\n")
                f.write(f"{'=' * 80}\n\n")
                f.write(f"{description}\n\n")

            print(f"✓ Processed {image_path.name} ({computation_time:.2f}s)")

            if verbose:
                print(f"\nFigure ID: {figure_id}")
                print(f"Description: {description}\n")

            if delay and i < len(figure_files) - 1:
                time.sleep(delay_seconds)

        except Exception as e:
            print(f"✗ Failed {image_path.name}: {e!s}")

            with open(output_path, "a", encoding="utf-8") as f:
                f.write(f"{'=' * 80}\n")
                f.write(f"Figure ID: {figure_id}\n")
                f.write(f"Model: {model_name}\n")
                f.write("Computation Time: 0.00 seconds\n")
                f.write(
                    f"Generated At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
                )
                f.write(f"{'=' * 80}\n\n")
                f.write(f"ERROR: Failed to generate description\nReason: {e!s}\n\n")

    print(f"\n✅ Results saved to: {output_path}")


# %%
llm = create_llm(
    provider="gemini",
    model_name="gemini-2.5-pro",
)

evaluator = EvaluatorAgent(
    criteria=["coherence", "fluency", "consistency", "relevance"],
    llm=llm,
)

generator = GeneratorAgent(
    llm=llm,
    user_prompt=get_default_generator_user_prompt(),
    system_prompt=None,
)

orchestrator = Orchestrator(
    generator_agent=generator,
    evaluator_agent=evaluator,
)

# %%
generate_descriptions_to_text(
    orchestrator=orchestrator,
    images_dir_path=images_dir_path,
    output_filename="figure_descriptions.txt",
    model_name="gemini-2.5-pro",
    delay_seconds=2,
    delay=True,
    verbose=True,
)
