user_prompt = """# Enhanced Weather Chart Alt-Text Generation System

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
