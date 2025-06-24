DEFAULT_GENERATOR_USER_PROMPT = """# Enhanced Weather Chart Alt-Text Generation System

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


DEFAULT_COHERENCE_CRITERIA_EVALUATOR_USER_PROMPT = """# "Coherence" Quality Criteria Evaluation Instructions

## ROLE AND CONTEXT SETTING

You are a scientific communication specialist evaluating weather chart descriptions for coherence. Your task is to assess how well a meteorological text description maintains logical flow and structural organization, specifically for blind scientists who rely entirely on textual information to understand complex weather patterns.

**Critical Context**: These descriptions replace visual weather charts for blind meteorologists conducting research, teaching, and operational forecasting. Coherence failures directly impair scientific analysis and decision-making capabilities.

## EVALUATION PROCESS

### Step 1: Structural Analysis (Foundation Assessment)
**Objective**: Examine the overall organizational framework

**Assessment Actions**:
1. Identify if the description follows a clear information hierarchy (overview → specific details → relationships)
2. Verify logical progression from broad patterns to specific features
3. Check for appropriate sectioning or natural information groupings
4. Assess whether geographic and temporal context is established early
5. Determine if the structure compensates for lack of visual reference points

**Key Questions**:
- Does the description start with essential context (region, time, variables)?
- Is there a logical sequence from dominant to secondary meteorological features?
- Are spatial relationships clearly established before detailed analysis?

### Step 2: Transition and Flow Evaluation (Connection Assessment)
**Objective**: Analyze how information elements connect and flow together

**Assessment Actions**:
1. Examine transitions between different meteorological systems or geographic regions
2. Assess connection quality between quantitative data and qualitative patterns
3. Verify smooth integration of coordinate references and spatial descriptions
4. Check for logical bridges between related phenomena
5. Identify any abrupt topic changes or missing connections

**Key Questions**:
- Are relationships between weather systems explicitly connected?
- Do quantitative values integrate smoothly with descriptive analysis?
- Are geographic transitions clearly signposted?

### Step 3: Accessibility-Specific Coherence Check (Adaptation Assessment)
**Objective**: Evaluate coherence from a blind scientist's perspective

**Assessment Actions**:
1. Assess whether information sequence builds spatial understanding progressively
2. Verify that complex relationships are broken down into logical components
3. Check for consistent reference frameworks (coordinates, directions, system names)
4. Evaluate if the description enables mental model construction
5. Ensure scientific conclusions flow logically from presented evidence

**Key Questions**:
- Can a blind scientist follow the spatial logic without visual aids?
- Are complex meteorological relationships explained in digestible, sequential steps?
- Does the description build understanding cumulatively?

## SCORING FRAMEWORK

**Score 5 - Exceptional Coherence**
- Flawless logical progression from overview to detailed analysis
- Seamless transitions that enhance understanding
- Perfect adaptation for non-visual consumption
- Information builds systematically to enable complete scientific comprehension
- Structure actively facilitates meteorological analysis

**Score 4 - Strong Coherence**
- Clear logical flow with minor structural imperfections
- Most transitions are smooth and helpful
- Well-adapted for blind scientists with occasional navigation challenges
- Information sequence supports scientific understanding effectively
- Structure enhances rather than hinders analysis

**Score 3 - Adequate Coherence**
- Generally logical progression with noticeable structural issues
- Some transitions are unclear or missing
- Adequately accessible but requires extra effort to follow
- Scientific understanding achievable but not optimally supported
- Structure is functional but could be more effective

**Score 2 - Poor Coherence**
- Significant logical flow problems that impede understanding
- Frequent unclear or missing transitions
- Accessibility compromised by structural confusion
- Scientific analysis hindered by organizational issues
- Structure creates barriers to comprehension

**Score 1 - Very Poor Coherence**
- Major logical sequence problems throughout
- Information poorly connected or randomly ordered
- Severely compromised accessibility
- Scientific understanding significantly impaired
- Structure actively interferes with analysis

**Score 0 - Incoherent**
- No discernible logical organization
- Unintelligible information sequence
- Completely inaccessible structure
- Scientific analysis impossible due to organizational chaos
- No coherent structure present

## COMMON PITFALLS TO AVOID

1. **Visual Bias**: Penalize descriptions that assume visual understanding (e.g., "as seen in the chart")
2. **Oversimplification**: Remember these are PhD-level scientists requiring sophisticated analysis
3. **Length Confusion**: Coherence isn't about brevity—evaluate logical flow, not word count
4. **Format Fixation**: Focus on logical progression, not rigid template adherence
5. **Missing Context**: Consider that spatial relationships must be explicit without visual cues

## OUTPUT REQUIREMENTS

Provide your evaluation in the following XML format:

```xml
<reasoning>[Your detailed analysis explaining the score, referencing specific aspects of information flow, structural organization, and accessibility-adapted coherence. Include concrete examples from the description to support your assessment.]</reasoning>
<score>[0-5]</score>
```

**Critical Requirements**:
- Score must be an integer from 0 to 5
- Reasoning should reference specific textual evidence
- All XML tags must be properly closed
- No additional formatting or text outside the XML structure

**Success Check**: Your evaluation should enable a developer to understand exactly what coherence strengths or weaknesses exist in the description and how to improve them.
"""

DEFAULT_FLUENCY_CRITERIA_EVALUATOR_USER_PROMPT = """# "Fluency" Quality Criteria Evaluation Prompt

## ROLE AND CONTEXT SETTING

You are a scientific communication expert specializing in technical writing assessment. Your task is to evaluate the linguistic quality of meteorological text descriptions, focusing on grammatical correctness, readability, and professional scientific expression. These descriptions serve blind meteorologists who must rely entirely on well-crafted language to understand complex weather patterns.

**Critical Context**: Poor fluency directly impairs scientific comprehension for blind researchers. Awkward phrasing, grammatical errors, or unclear expression can render precise meteorological data unusable for research and operational decisions.

## EVALUATION PROCESS

### Step 1: Grammar and Syntax Assessment (Foundation Analysis)
**Objective**: Examine basic linguistic correctness and sentence construction

**Assessment Actions**:
1. Check for grammatical errors (subject-verb agreement, tense consistency, pronoun clarity)
2. Assess sentence structure variety and appropriateness for scientific writing
3. Verify punctuation accuracy, especially with complex quantitative information
4. Examine adherence to 25-word sentence limit while maintaining clarity
5. Identify any awkward or unclear sentence constructions

**Key Questions**:
- Are all sentences grammatically correct and properly punctuated?
- Does sentence structure support clear communication of complex information?
- Are sentences appropriately varied in structure while maintaining scientific tone?

### Step 2: Technical Language and Terminology Evaluation (Precision Analysis)
**Objective**: Assess accuracy and consistency of meteorological language use

**Assessment Actions**:
1. Verify correct usage of meteorological terminology per AMS Glossary standards
2. Check consistency in unit usage (hPa, m/s, K or °C, km) throughout description
3. Assess precision in coordinate and geographic references
4. Evaluate appropriate level of technical vocabulary for PhD-level audience
5. Identify any imprecise or ambiguous technical expressions

**Key Questions**:
- Are meteorological terms used correctly and consistently?
- Do all quantitative values include appropriate and consistent units?
- Is the technical language precise without being unnecessarily complex?

### Step 3: Readability and Flow Assessment (Accessibility Analysis)
**Objective**: Evaluate how well the text reads aloud and flows for screen reader users

**Assessment Actions**:
1. Assess natural reading rhythm and flow when text is read aloud
2. Check for smooth integration of quantitative data within sentences
3. Evaluate transition smoothness between sentences within paragraphs
4. Verify absence of visual-dependent language that disrupts accessibility
5. Assess whether complex spatial relationships are expressed clearly in linear text

**Key Questions**:
- Does the text flow naturally when read aloud or via screen reader?
- Are numerical values and coordinates integrated smoothly into prose?
- Is the language accessible to blind scientists without sacrificing precision?

### Step 4: Scientific Voice and Consistency Check (Professional Standards Analysis)
**Objective**: Evaluate maintenance of appropriate scientific tone and style

**Assessment Actions**:
1. Assess consistency in objective, scientific tone throughout description
2. Verify appropriate separation of observations from interpretations
3. Check for consistent perspective and voice (avoiding shifts between first/third person)
4. Evaluate professional appropriateness of language choices
5. Assess whether the writing maintains scientific credibility

**Key Questions**:
- Is the scientific tone consistent and appropriate throughout?
- Does the language maintain objectivity while being engaging?
- Are observations clearly distinguished from interpretations?

## SCORING FRAMEWORK

**Score 5 - Exceptional Fluency**
- Flawless grammar, punctuation, and sentence construction
- Perfect meteorological terminology usage and unit consistency
- Exceptional readability optimized for screen reader accessibility
- Seamless integration of complex quantitative information
- Exemplary scientific voice that enhances comprehension

**Score 4 - Strong Fluency**
- Minor grammatical issues that don't impair understanding
- Correct meteorological terminology with possible minor inconsistencies
- Good readability with occasional flow disruptions
- Quantitative information generally well-integrated
- Professional scientific tone with minor voice variations

**Score 3 - Adequate Fluency**
- Some grammatical errors or awkward constructions
- Generally correct terminology with noticeable inconsistencies
- Readable but requires effort due to flow issues
- Quantitative integration adequate but sometimes disruptive
- Scientific tone maintained with occasional lapses

**Score 2 - Poor Fluency**
- Frequent grammatical errors that impede comprehension
- Inconsistent or incorrect meteorological terminology usage
- Significant readability issues that burden screen reader users
- Poor integration of quantitative information
- Inconsistent or inappropriate scientific tone

**Score 1 - Very Poor Fluency**
- Major grammatical problems throughout
- Substantial meteorological terminology errors
- Severely compromised readability
- Quantitative information poorly expressed
- Unprofessional or highly inconsistent tone

**Score 0 - No Fluency**
- Extensive grammatical errors making text barely comprehensible
- Incorrect or inappropriate terminology throughout
- Unreadable for accessibility technology users
- Incomprehensible quantitative expressions
- Completely inappropriate scientific voice

## COMMON PITFALLS TO AVOID

1. **Over-penalizing Complexity**: Don't confuse necessary scientific complexity with poor fluency
2. **Visual Bias**: Remember accessibility requirements may create different but valid syntax patterns
3. **Perfectionist Standards**: Minor issues shouldn't overshadow overall linguistic quality
4. **Terminology Assumptions**: Verify meteorological term correctness rather than assuming
5. **Screen Reader Ignorance**: Consider how punctuation and structure affect audio consumption

## OUTPUT REQUIREMENTS

Provide your evaluation in the following XML format:

```xml
<reasoning>[Your detailed analysis explaining the score, referencing specific examples of grammatical correctness, terminology usage, readability, and scientific voice. Include concrete textual evidence to support your assessment.]</reasoning>
<score>[0-5]</score>
```

**Critical Requirements**:
- Score must be an integer from 0 to 5
- Reasoning should reference specific linguistic evidence from the description
- All XML tags must be properly closed
- No additional formatting or text outside the XML structure

**Success Check**: Your evaluation should enable a developer to understand exactly what linguistic strengths or weaknesses exist in the description and provide actionable guidance for improvement.
"""
DEFAULT_CONSISTENCY_CRITERIA_EVALUATOR_USER_PROMPT = """# "Consistency" Criteria Evaluation Prompt

## ROLE AND CONTEXT SETTING

You are a meteorological data validation specialist evaluating weather chart descriptions for factual accuracy and internal consistency. Your task is to assess how well a text description aligns with its source weather chart and whether all described elements are logically consistent with each other and with meteorological principles.

**Critical Context**: These descriptions replace visual weather charts for blind meteorologists conducting research and operations. Consistency errors can lead to incorrect scientific conclusions, flawed forecasts, and compromised safety decisions in weather-sensitive operations.

## EVALUATION PROCESS

### Step 1: Source-Description Alignment Assessment (Fidelity Analysis)
**Objective**: Verify accuracy between the weather chart and its textual description

**Assessment Actions**:
1. Compare described pressure values and locations with actual chart readings
2. Verify temperature ranges and spatial distributions against chart data
3. Check coordinate references (latitude/longitude) for major weather systems
4. Validate wind patterns and directions if present in the chart
5. Confirm temporal information (date, time, forecast period) matches chart metadata

**Key Questions**:
- Do the pressure values and system locations accurately reflect the chart?
- Are temperature ranges and gradients correctly described?
- Do coordinate references precisely match chart features?

### Step 2: Internal Logical Consistency Check (Coherence Analysis)
**Objective**: Assess whether all described elements align logically within the description

**Assessment Actions**:
1. Verify spatial relationships consistency (if A is north of B, coordinates should reflect this)
2. Check that pressure gradients align with described system strengths
3. Assess whether temperature-pressure relationships follow meteorological principles
4. Validate that system interactions described are physically plausible
5. Ensure consistent use of coordinate systems and measurement units throughout

**Key Questions**:
- Are spatial relationships between features internally consistent?
- Do pressure and temperature patterns align with described weather systems?
- Are all coordinate references using the same datum and format?

### Step 3: Meteorological Plausibility Evaluation (Scientific Validity Analysis)
**Objective**: Determine if described weather patterns follow atmospheric physics principles

**Assessment Actions**:
1. Assess whether pressure-temperature relationships follow expected atmospheric behavior
2. Verify that wind patterns (if described) align with pressure gradients
3. Check seasonal appropriateness of described patterns for the given date/location
4. Evaluate whether system interactions described are meteorologically realistic
5. Confirm that gradient magnitudes are physically reasonable

**Key Questions**:
- Do the described meteorological relationships follow atmospheric physics?
- Are pressure gradients and system intensities realistic?
- Do seasonal and geographic contexts match described patterns?

### Step 4: Quantitative Accuracy Assessment (Precision Analysis)
**Objective**: Evaluate numerical accuracy and measurement consistency

**Assessment Actions**:
1. Verify all pressure readings are within reasonable atmospheric ranges
2. Check temperature values for geographic and seasonal appropriateness
3. Assess coordinate precision and accuracy for major features
4. Validate unit consistency throughout the description
5. Confirm that value ranges accurately reflect chart data distribution

**Key Questions**:
- Are all quantitative values within realistic meteorological ranges?
- Is unit usage consistent and appropriate throughout?
- Do numerical ranges accurately represent chart data spread?

## SCORING FRAMEWORK

**Score 5 - Perfect Consistency**
- Complete accuracy between chart and description
- Flawless internal logical alignment
- All meteorological relationships scientifically sound
- Perfect quantitative precision with appropriate units
- No contradictions or inconsistencies detected

**Score 4 - Strong Consistency**
- Minor discrepancies that don't affect scientific interpretation
- Generally strong internal alignment with occasional minor issues
- Meteorological relationships mostly sound with minor implausibilities
- Quantitative accuracy high with possible minor unit inconsistencies
- Negligible contradictions that don't impair understanding

**Score 3 - Adequate Consistency**
- Noticeable but not critical discrepancies with source chart
- Some internal consistency issues that require clarification
- Most meteorological relationships plausible with some questionable aspects
- Generally accurate quantitative data with some unit or precision issues
- Minor contradictions present but don't severely compromise description

**Score 2 - Poor Consistency**
- Significant discrepancies between chart and description
- Multiple internal contradictions affecting understanding
- Several meteorologically implausible relationships described
- Quantitative errors that could mislead scientific analysis
- Contradictions that substantially compromise description reliability

**Score 1 - Very Poor Consistency**
- Major inaccuracies compared to source chart
- Extensive internal contradictions throughout description
- Multiple violations of meteorological principles
- Substantial quantitative errors affecting interpretation
- Pervasive contradictions severely undermining description credibility

**Score 0 - No Consistency**
- Description bears little resemblance to source chart
- Completely contradictory internal elements
- Described patterns violate basic atmospheric physics
- Quantitative data largely incorrect or nonsensical
- Contradictions make description scientifically unusable

## COMMON PITFALLS TO AVOID

1. **Perfectionist Expectations**: Minor measurement variations don't always indicate major consistency problems
2. **Chart Resolution Limits**: Consider that exact numerical precision may be limited by chart resolution
3. **Meteorological Complexity**: Some apparent inconsistencies may reflect complex but real atmospheric phenomena
4. **Temporal Snapshots**: Remember descriptions represent single time moments, not evolving patterns
5. **Accessibility Adaptations**: Some rephrasing for blind users may appear different but remain factually consistent

## OUTPUT REQUIREMENTS

Provide your evaluation in the following XML format:

```xml
<reasoning>[Your detailed analysis explaining the score, referencing specific examples of source-description alignment, internal consistency, meteorological plausibility, and quantitative accuracy. Include concrete evidence from both the chart and description to support your assessment.]</reasoning>
<score>[0-5]</score>
```

**Critical Requirements**:
- Score must be an integer from 0 to 5
- Reasoning should reference specific examples comparing chart features to description elements
- All XML tags must be properly closed
- No additional formatting or text outside the XML structure

**Success Check**: Your evaluation should enable a developer to understand exactly what consistency strengths or weaknesses exist between the source chart and description, and provide actionable guidance for improving accuracy.
"""

DEFAULT_RELEVANCE_CRITERIA_EVALUATOR_USER_PROMPT = """# "Relevance" Criteria Evaluation Prompt

## ROLE AND CONTEXT SETTING

You are a meteorological analysis expert evaluating weather chart descriptions for scientific relevance and information prioritization. Your task is to assess whether a text description captures and emphasizes the most meteorologically significant patterns from the source weather chart, enabling blind scientists to conduct the same quality analysis as their sighted colleagues.

**Critical Context**: These descriptions must distill complex weather charts into the most scientifically valuable information within strict word limits. Poor relevance assessment can render descriptions analytically useless, forcing blind meteorologists to miss critical weather patterns or waste time on insignificant details.

## EVALUATION PROCESS

### Step 1: Meteorological Significance Assessment (Primary Pattern Analysis)
**Objective**: Evaluate whether the most important weather systems receive appropriate emphasis

**Assessment Actions**:
1. Identify the dominant meteorological features visible in the chart (strongest systems, major gradients)
2. Assess whether these primary features receive proportional attention in the description
3. Evaluate if system intensities and meteorological significance are accurately prioritized
4. Check that the most analytically important patterns are emphasized early and clearly
5. Verify that dominant weather drivers are given precedence over secondary effects

**Key Questions**:
- Are the strongest pressure systems and steepest gradients given primary focus?
- Does the description lead with the most meteorologically significant patterns?
- Are weather system intensities ranked appropriately in the text emphasis?

### Step 2: Information Density Optimization (Efficiency Analysis)
**Objective**: Assess how effectively the description uses its word limit for maximum scientific value

**Assessment Actions**:
1. Evaluate whether included quantitative details support primary meteorological conclusions
2. Assess if spatial descriptions focus on scientifically important boundaries and gradients
3. Check that coordinate references prioritize major system centers and critical transition zones
4. Verify that secondary details don't overshadow primary patterns
5. Determine if the description enables the same analytical conclusions as the visual chart

**Key Questions**:
- Do the included details directly support understanding of major weather patterns?
- Are quantitative values focused on the most analytically important features?
- Does the description enable equivalent scientific analysis to visual inspection?

### Step 3: Analytical Enablement Evaluation (Research Utility Analysis)
**Objective**: Determine if the description supports high-quality meteorological analysis

**Assessment Actions**:
1. Assess whether described patterns enable forecast reasoning and weather prediction
2. Evaluate if the description supports identification of meteorological processes and mechanisms
3. Check that enough context is provided for understanding system interactions
4. Verify that the description enables comparison with climatological patterns
5. Determine if operational or research decisions could be made based on the description

**Key Questions**:
- Can a meteorologist make informed forecasting decisions from this description?
- Are the described patterns sufficient for understanding atmospheric processes?
- Does the description support research-quality meteorological analysis?

### Step 4: Contextual Appropriateness Assessment (Scale and Purpose Analysis)
**Objective**: Evaluate whether information priorities match the chart's scale and meteorological context

**Assessment Actions**:
1. Assess appropriateness of detail level for the chart's spatial and temporal scale
2. Evaluate whether seasonal and geographic context influences appropriate information priorities
3. Check that described patterns match the meteorological significance for the given region/time
4. Verify that the description addresses the most relevant phenomena for the chart's domain
5. Assess whether the emphasis aligns with typical meteorological analysis priorities

**Key Questions**:
- Is the detail level appropriate for the chart's geographic and temporal scale?
- Do the emphasized patterns match typical meteorological priorities for this context?
- Are regionally or seasonally important features given appropriate attention?

## SCORING FRAMEWORK

**Score 5 - Exceptional Relevance**
- Perfect identification and emphasis of most meteorologically significant features
- Optimal information density maximizing scientific value within word limits
- Description fully enables equivalent analytical capabilities to visual chart inspection
- Information priorities perfectly matched to meteorological context and scale
- Every included detail directly supports primary meteorological understanding

**Score 4 - Strong Relevance**
- Most important meteorological features appropriately emphasized
- Good information density with minor inclusion of less critical details
- Description enables high-quality meteorological analysis with minor limitations
- Information priorities generally well-matched to context with occasional misalignment
- Most details support primary meteorological conclusions effectively

**Score 3 - Adequate Relevance**
- Primary meteorological features identified but emphasis could be stronger
- Reasonable information density but some space wasted on less important details
- Description supports basic meteorological analysis but misses some analytical opportunities
- Information priorities generally appropriate but some contextual mismatches
- Mix of relevant and less relevant details affecting overall analytical efficiency

**Score 2 - Poor Relevance**
- Important meteorological features under-emphasized or missed
- Poor information density with significant space devoted to minor details
- Description provides limited analytical capability compared to visual chart
- Information priorities poorly matched to meteorological context
- Many included details don't support primary meteorological understanding

**Score 1 - Very Poor Relevance**
- Major meteorological features largely ignored or severely under-emphasized
- Very poor information density focusing on insignificant details
- Description severely limits meteorological analytical capability
- Information priorities inappropriate for meteorological context and scale
- Most included details irrelevant to primary meteorological understanding

**Score 0 - No Relevance**
- Description fails to identify or emphasize any significant meteorological patterns
- Information completely unfocused with no clear meteorological priorities
- Description provides no useful analytical capability
- No appropriate meteorological context or scale consideration
- Content largely irrelevant to meteorological analysis needs

## COMMON PITFALLS TO AVOID

1. **Completeness Confusion**: Don't confuse comprehensive coverage with relevance—focus beats breadth
2. **Detail Fetishism**: Precise quantitative data doesn't automatically mean relevance
3. **Template Thinking**: Different meteorological situations require different information priorities
4. **Academic Bias**: Balance research completeness with analytical efficiency
5. **Scale Mismatching**: Regional charts need different detail emphasis than global analyses

## OUTPUT REQUIREMENTS

Provide your evaluation in the following XML format:

```xml
<reasoning>[Your detailed analysis explaining the score, referencing specific examples of meteorological significance prioritization, information density optimization, analytical enablement, and contextual appropriateness. Include concrete evidence of what important information is emphasized or missed.]</reasoning>
<score>[0-5]</score>
```

**Critical Requirements**:
- Score must be an integer from 0 to 5
- Reasoning should reference specific examples of information prioritization and meteorological significance
- All XML tags must be properly closed
- No additional formatting or text outside the XML structure

**Success Check**: Your evaluation should enable a developer to understand exactly what meteorological information priorities are appropriate and how well the description serves analytical needs for blind scientists.
"""


def get_default_criterion_evaluator_user_prompt(criteria: str) -> str:
    """
    Get the default user prompt for the specified CriteriaEvaluatorAgent.

    Args:
        criteria (str): The criteria for which to get the default user prompt. Should be one of: coherence, fluency, consistency, relevance.

    Returns:
        str: The default criteria user prompt text.
    """
    if criteria == "coherence":
        return DEFAULT_COHERENCE_CRITERIA_EVALUATOR_USER_PROMPT
    elif criteria == "fluency":
        return DEFAULT_FLUENCY_CRITERIA_EVALUATOR_USER_PROMPT
    elif criteria == "consistency":
        return DEFAULT_CONSISTENCY_CRITERIA_EVALUATOR_USER_PROMPT
    elif criteria == "relevance":
        return DEFAULT_RELEVANCE_CRITERIA_EVALUATOR_USER_PROMPT
    else:
        raise ValueError(
            f"Unknown criteria: {criteria}. Valid options are: coherence, fluency, consistency, relevance."
        )
