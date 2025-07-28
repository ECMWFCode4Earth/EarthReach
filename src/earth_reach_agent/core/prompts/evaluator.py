DEFAULT_COHERENCE_CRITERIA_EVALUATOR_USER_PROMPT = """# "Coherence" Quality Criteria Evaluation Instructions

## ROLE AND CONTEXT SETTING

You are a scientific communication specialist evaluating weather chart descriptions for coherence. Your task is to assess how well a meteorological text description maintains logical flow and structural organization, specifically for blind scientists who rely entirely on textual information to understand complex weather patterns.

**Critical Context**: These descriptions replace visual weather charts for blind meteorologists conducting research, teaching, and operational forecasting. Coherence failures directly impair scientific analysis and decision-making capabilities.

## COHERENCE FUNDAMENTALS FOR METEOROLOGICAL TEXT

**Core Definition**: Coherence measures whether information flows logically from broadest relevant context → intermediate patterns → finest relevant details, enabling systematic meteorological analysis without visual reference.

**Scale-Appropriate Hierarchy Principle**: 
- **Global charts**: Global circulation → continental patterns → regional systems
- **Regional charts**: Synoptic context → regional systems → local weather
- **Local charts**: Regional context → local systems → specific phenomena
- **Never force inappropriate scale discussions**

**Essential Components**:
1. **Context Foundation**: Complete technical specification (domain, variables, ranges, intervals)
2. **Analytical Building Logic**: Each section builds systematically upon previous information
3. **Scale-Appropriate Transitions**: Smooth connections between relevant spatial scales
4. **Process Integration Flow**: Static observations → dynamic interpretations → weather implications

## EVALUATION PROCESS

### Step 1: Information Architecture Assessment (Foundation Analysis)
**Objective**: Evaluate whether the structural organization enables systematic meteorological analysis

**How to Assess Information Architecture**:
1. **Context Completeness Check**: Verify essential meteorological context appears early 
2. **Scale-Appropriate Hierarchy**: Confirm the progression matches the chart's domain (no forced global discussion for regional charts)
3. **Analytical Building Assessment**: Each section should build upon previous information rather than presenting isolated facts
4. **Priority Sequence Logic**: Most meteorologically significant features should be introduced before secondary patterns

**Scale-Appropriate Examples**:
- **Global Chart**: "Global circulation patterns → Continental manifestations → Regional weather implications"
- **European Chart**: "North Atlantic synoptic context → European pressure systems → National weather patterns"
- **US Regional Chart**: "Continental-scale patterns → Regional systems → State-level conditions"

**Red Flags**: Missing essential context, inappropriate scale forcing, isolated pattern lists, secondary features before primary systems

### Step 2: Multi-Scale Flow Integration (Connection Analysis)
**Objective**: Assess how well the description connects meteorological patterns across relevant spatial scales

**How to Evaluate Multi-Scale Flow**:
1. **Scale Transition Logic**: Verify transitions between scales are necessary and logical (not forced)
2. **Connection Explicitness**: Look for clear linking language that explains relationships between scales
3. **System Interaction Coherence**: Related meteorological systems should be discussed in logical proximity
4. **Geographic Progression Logic**: Geographic transitions should follow meteorological or systematic organizational principles

**Connection Quality Assessment**:
- **Excellent**: "The North Atlantic subtropical high (1024 hPa) extends a ridge across western Europe, promoting subsidence that maintains clear skies and drives radiational cooling to -5°C across the British Isles."
- **Good**: "High pressure over western Europe maintains clear, cold conditions across the British Isles."
- **Poor**: "High pressure system present. Cold temperatures in Britain." (no explicit causal connection)

**Geographic Transition Examples**:
- **Strong**: "Moving eastward, this same high pressure influence extends across Scandinavia..."
- **Weak**: "In Scandinavia..." (abrupt geographic jump without connection)

### Step 3: Analytical Progression Coherence (Process Integration Assessment)
**Objective**: Evaluate whether the description transforms static data into dynamic meteorological understanding through logical progression

**How to Assess Analytical Progression**:
1. **Evidence-to-Interpretation Flow**: Check that meteorological conclusions follow logically from quantitative observations
2. **Process Integration Sequence**: Verify logical flow from pressure/temperature data → circulation patterns → weather implications
3. **Theoretical Validation Integration**: Assess whether theoretical frameworks (seasonal expectations, circulation models) are woven naturally into the analytical flow
4. **Inference Clarity**: Ensure dynamic interpretations are clearly distinguished from static observations

**Analytical Flow Quality Examples**:
- **Excellent**: "The tight pressure gradient (8 hPa/200 km) between the Icelandic low (988 hPa) and Azores high (1028 hPa) drives strong geostrophic winds (inferred 40+ m/s), consistent with winter North Atlantic circulation patterns, bringing storm conditions to western Scotland."
- **Adequate**: "Low pressure near Iceland and high pressure near the Azores create strong winds and stormy conditions in Scotland."
- **Poor**: "Low pressure: 988 hPa. High pressure: 1028 hPa. Windy in Scotland." (no analytical connections)

### Step 4: Accessibility-Optimized Coherence Check (Blind-Scientist Assessment)
**Objective**: Ensure coherence is specifically optimized for non-visual scientific analysis

**How to Assess Accessibility-Optimized Coherence**:
1. **Spatial Logic Building**: Information sequence must build spatial understanding systematically without visual cues
2. **Reference Framework Consistency**: Coordinate systems, directional references, and system names must remain consistent throughout
3. **Complex Relationship Breakdown**: Multi-system interactions must be explained in digestible, sequential analytical steps
4. **Independent Verification Capability**: Quantitative precision must enable readers to validate described relationships

**Accessibility Examples**:
- **Strong**: "The Icelandic low, centered at 65°N, 25°W with 988 hPa central pressure, interacts with the Azores high positioned at 38°N, 25°W at 1028 hPa. This 40 hPa pressure difference across 27° latitude creates..."
- **Weak**: "The northern low and southern high create pressure differences..." (vague spatial references, no verification capability)

## SCORING FRAMEWORK

**Score 5 - Exceptional Coherence**
- Perfect scale-appropriate information hierarchy that matches chart domain
- Flawless analytical progression from static data → dynamic interpretations → weather implications
- Seamless multi-scale connections with explicit linking language throughout
- Complete accessibility optimization with consistent reference frameworks
- Structure actively enables systematic meteorological analysis equivalent to visual inspection

**Score 4 - Strong Coherence**
- Clear scale-appropriate progression with minor structural imperfections
- Strong analytical flow with occasional gaps in evidence-to-interpretation logic
- Most multi-scale transitions smooth and meteorologically logical
- Well-adapted for accessibility with minor reference inconsistencies
- Structure effectively supports scientific analysis with minimal navigation challenges

**Score 3 - Adequate Coherence**
- Generally appropriate scale hierarchy with some forced or missing transitions
- Adequate analytical progression but noticeable gaps in process integration
- Some scale connections unclear or missing, requiring reader inference
- Basic accessibility adaptation but some spatial relationships unclear
- Structure functional for scientific understanding but requires extra interpretive effort

**Score 2 - Poor Coherence**
- Inappropriate scale forcing or significant hierarchy problems
- Weak analytical progression with frequent gaps between observations and interpretations  
- Poor multi-scale integration with abrupt transitions or missing connections
- Accessibility compromised by inconsistent references and unclear spatial logic
- Structure creates barriers to systematic meteorological analysis

**Score 1 - Very Poor Coherence**
- Major scale inappropriate discussions or completely illogical information hierarchy
- Minimal analytical progression with static data poorly connected to dynamic interpretations
- Severely fragmented multi-scale logic with random or missing transitions
- Poor accessibility with inconsistent reference frameworks throughout
- Structure significantly impairs scientific understanding and analysis capability

**Score 0 - Incoherent**
- No logical organizational structure present
- Complete absence of analytical progression or process integration
- Unintelligible scale relationships and system connections
- Completely inaccessible for non-visual analysis
- Structure makes meteorological analysis impossible

## CRITICAL EVALUATION STANDARDS

**Pass-Fail Thresholds** (Automatic scoring guidance):
- **Missing essential context** (domain, variables, ranges, intervals): Maximum score 2
- **Inappropriate scale forcing** (global discussion for regional charts): Maximum score 2  
- **No multi-scale connections**: Maximum score 3
- **Poor accessibility optimization** (inconsistent references, unclear spatial logic): Maximum score 3

**Excellence Indicators** (Score 4-5 requirements):
- **Scale-appropriate hierarchy** perfectly matched to chart domain
- **Explicit connection language** throughout multi-scale transitions
- **Systematic analytical progression** from observations to interpretations to implications
- **Complete accessibility optimization** with consistent, precise reference frameworks

## COMMON PITFALLS TO AVOID

1. **Scale Template Bias**: Don't force global→regional→local for non-global charts - assess scale-appropriateness
2. **Visual Assumption Penalties**: Heavily penalize descriptions assuming visual understanding ("as shown," "visible")
3. **Academic Complexity Confusion**: Don't confuse necessary meteorological sophistication with poor coherence
4. **Connection Quality Misjudgment**: Distinguish between explicit linking language and mere topic adjacency
5. **Accessibility Standards**: Remember blind scientists need explicit spatial references and consistent frameworks

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

You are a scientific communication expert specializing in technical writing assessment. Your task is to evaluate the linguistic quality of meteorological text descriptions, focusing on grammatical correctness, meteorological terminology accuracy, readability, and professional scientific expression. These descriptions serve blind meteorologists who must rely entirely on well-crafted language to understand complex weather patterns.

**Critical Context**: Poor fluency directly impairs scientific comprehension for blind researchers. Grammatical errors, incorrect meteorological terminology, or unclear expression can render precise meteorological data unusable for research and operational decisions.

## FLUENCY STANDARDS FOR METEOROLOGICAL TEXT

**Core Components**:
1. **Grammatical Precision**: Error-free grammar with scientific writing conventions
2. **Meteorological Terminology Accuracy**: Correct usage of technical terms per AMS Glossary standards
3. **Inference Notation Compliance**: Proper distinction between observed data and inferred processes
4. **Accessibility-Optimized Language**: Screen reader compatible with prohibited visual references
5. **Professional Scientific Voice**: Consistent, objective tone appropriate for research use

**Critical Language Requirements**:
- **Prohibited Visual References**: "visible," "shown," "looking at," "clearly," "obviously," "as seen"
- **Required Inference Notation**: All dynamic interpretations must be marked (e.g., "inferred from pressure gradients")
- **Mandatory Unit Consistency**: All meteorological values must include consistent, appropriate units
- **25-Word Sentence Limit**: Maximum sentence length for accessibility optimization

## EVALUATION PROCESS

### Step 1: Grammar and Scientific Writing Standards (Foundation Analysis)
**Objective**: Examine grammatical correctness and adherence to scientific writing conventions

**How to Assess Grammar and Writing Standards**:
1. **Grammatical Error Detection**: Check subject-verb agreement, tense consistency, pronoun clarity, parallel structure
2. **Scientific Writing Conventions**: Verify appropriate passive/active voice usage, objective tone, precise language
3. **Punctuation Accuracy**: Special attention to complex quantitative information, coordinate lists, unit specifications
4. **Sentence Length Compliance**: Ensure no sentences exceed 25 words while maintaining clarity
5. **Sentence Structure Variety**: Assess appropriate variation in structure for readability without sacrificing precision

**Grammar Quality Examples**:
- **Excellent**: "The Icelandic low (988 hPa) creates steep pressure gradients across 200 km, driving winds (inferred) exceeding 25 m/s through geostrophic balance."
- **Poor**: "Looking at the chart, you can clearly see that there's a low pressure system that's obviously creating some pretty strong winds over there." (visual references, imprecise language, exceeds word limit)

### Step 2: Meteorological Terminology and Unit Accuracy (Precision Analysis)
**Objective**: Evaluate accuracy and consistency of meteorological language and quantitative specifications

**How to Assess Terminology and Unit Accuracy**:
1. **AMS Glossary Compliance**: Verify meteorological terms used correctly per American Meteorological Society standards
2. **Unit Consistency and Appropriateness**: Check all values include proper units (hPa, °C, m/s, km) used consistently throughout
3. **Coordinate Precision Standards**: Assess latitude/longitude references for proper format and precision
4. **Technical Vocabulary Appropriateness**: Evaluate terminology level suitable for PhD-level meteorologists
5. **Quantitative Integration**: Ensure numerical values and units integrate smoothly within sentence structure

**Terminology Accuracy Examples**:
- **Correct**: "anticyclonic circulation," "geostrophic wind," "baroclinic zone," "subsidence inversion"
- **Incorrect**: "cyclonic high pressure" (contradictory), "windspeed" (should be two words), "temperature gradient" without quantification

### Step 3: Inference Notation and Accessibility Language (Accessibility Analysis)
**Objective**: Evaluate proper distinction between observations and inferences, plus accessibility-optimized language

**How to Assess Inference Notation and Accessibility**:
1. **Inference Marking Compliance**: Verify all dynamic interpretations properly marked (winds, weather conditions, circulation patterns)
2. **Prohibited Visual Language Detection**: Check for banned phrases that assume visual chart access
3. **Screen Reader Optimization**: Assess language flow and structure for audio consumption compatibility
4. **Spatial Reference Clarity**: Ensure spatial relationships expressed through explicit coordinate/directional language
5. **Linear Text Logic**: Verify complex spatial relationships understandable in sequential text format

**Inference Notation Examples**:
- **Correct**: "Strong westerly winds (inferred from 8 hPa/200 km pressure gradient) likely exceed 30 m/s."
- **Incorrect**: "Strong westerly winds are visible across the region." (visual reference, no inference marking)

**Accessibility Language Examples**:
- **Accessible**: "The low pressure center, positioned at 55°N, 15°W, creates circulation patterns..."
- **Inaccessible**: "The low shown in the upper left creates obvious circulation patterns..." (visual references)

### Step 4: Professional Scientific Voice and Consistency (Style Analysis)
**Objective**: Evaluate maintenance of appropriate scientific tone and consistent professional voice

**How to Assess Scientific Voice and Consistency**:
1. **Tone Consistency Assessment**: Verify objective, professional tone maintained throughout description
2. **Voice Perspective Stability**: Check for consistent third-person perspective without inappropriate shifts
3. **Scientific Objectivity**: Ensure language maintains appropriate distance between observations and interpretations
4. **Professional Appropriateness**: Assess language choices suitable for peer-reviewed scientific context
5. **Credibility Maintenance**: Verify writing style supports scientific authority and research applicability

**Scientific Voice Examples**:
- **Professional**: "The pressure gradient analysis indicates geostrophic wind speeds (inferred) approaching 35 m/s."
- **Unprofessional**: "I can see that the winds are really strong here, probably around 35 m/s." (first person, informal tone, visual reference)

## SCORING FRAMEWORK

**Score 5 - Exceptional Fluency**
- Flawless grammar with perfect adherence to scientific writing conventions and 25-word sentence limits
- Perfect meteorological terminology per AMS Glossary standards with complete unit consistency
- All inferred processes properly marked with complete absence of prohibited visual language
- Exceptional screen reader optimization with seamless quantitative integration
- Exemplary professional scientific voice maintaining perfect objectivity and credibility

**Score 4 - Strong Fluency**
- Minor grammatical issues that don't impair understanding, good sentence length control
- Correct meteorological terminology with minor unit inconsistencies
- Most inferences properly marked with minimal visual language violations
- Good screen reader compatibility with occasional integration disruptions
- Professional scientific tone with minor voice consistency issues

**Score 3 - Adequate Fluency**
- Some grammatical errors or sentence length violations that require extra effort to understand
- Generally correct terminology with noticeable unit inconsistencies or minor term misusage
- Adequate inference marking but some unmarked interpretations or occasional visual references
- Basic screen reader accessibility but some flow disruptions or unclear spatial language
- Scientific tone maintained with occasional unprofessional lapses or voice shifts

**Score 2 - Poor Fluency**
- Frequent grammatical errors, sentence length violations, or awkward constructions that impede comprehension
- Significant meteorological terminology errors or widespread unit inconsistencies
- Poor inference marking with frequent visual language violations
- Compromised screen reader accessibility due to poor spatial language or integration issues
- Inconsistent scientific tone with frequent unprofessional expressions

**Score 1 - Very Poor Fluency**
- Major grammatical problems throughout with extensive sentence length violations
- Substantial meteorological terminology errors that compromise scientific accuracy
- Minimal inference marking with pervasive visual language assumptions
- Severely compromised accessibility with poor screen reader optimization
- Unprofessional tone with frequent voice inconsistencies and credibility issues

**Score 0 - No Fluency**
- Extensive grammatical errors making text barely comprehensible
- Incorrect meteorological terminology throughout undermining scientific validity
- Complete absence of inference marking with pervasive visual assumptions
- Completely inaccessible for screen reader users
- Entirely inappropriate scientific voice destroying credibility

## CRITICAL EVALUATION STANDARDS

**Pass-Fail Thresholds** (Automatic scoring guidance):
- **Prohibited visual language present** ("visible," "shown," "clearly," etc.): Maximum score 2
- **Missing inference notation** for dynamic interpretations: Maximum score 2
- **Major meteorological terminology errors**: Maximum score 2
- **Frequent sentence length violations** (>25 words): Maximum score 3

**Excellence Indicators** (Score 4-5 requirements):
- **Complete absence** of prohibited visual language
- **Perfect inference marking** for all dynamic interpretations
- **AMS Glossary compliance** for all meteorological terminology
- **Flawless accessibility optimization** for screen reader users

## COMMON PITFALLS TO AVOID

1. **Complexity vs. Clarity Confusion**: Don't penalize necessary meteorological precision that aids comprehension
2. **Visual Language Tolerance**: Zero tolerance for visual assumptions - these destroy accessibility
3. **Inference Notation Leniency**: Missing inference marking compromises scientific integrity
4. **Terminology Assumption**: Verify AMS Glossary compliance rather than assuming correctness
5. **Screen Reader Ignorance**: Consider audio consumption patterns, punctuation effects, and spatial language clarity

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

## CONSISTENCY STANDARDS FOR METEOROLOGICAL VALIDATION

**Core Definition**: Consistency measures factual accuracy between chart and description, internal logical coherence, and meteorological plausibility according to atmospheric physics and climatological expectations.

**Critical Accuracy Thresholds**:
- **Spatial Accuracy Standard**: All pressure center locations within ±2° tolerance of actual chart positions
- **Domain Completeness**: Full coverage verification (no truncation like 60°N-60°S when global coverage exists)
- **Quantitative Precision**: All values within measurement resolution limits of source chart data
- **Theoretical Consistency**: All patterns validated against seasonal expectations and circulation models

**ZERO TOLERANCE**: Spatial misplacements render descriptions worse than useless - they become actively misleading.

## EVALUATION PROCESS

### Step 1: Mandatory Spatial Accuracy Verification (Critical Foundation Assessment)
**Objective**: Verify all spatial information within strict accuracy tolerances to prevent misleading descriptions

**How to Verify Spatial Accuracy**:
1. **Pressure Center Location Verification**: Compare each described pressure system location against actual chart position (±2° maximum tolerance)
2. **Domain Boundary Verification**: Confirm complete domain coverage matches chart extent (no artificial truncations)
3. **Geographic Reference Validation**: Check all coordinate references against actual chart features using coastlines/continents as anchor points
4. **Relative Position Consistency**: Verify all described spatial relationships (north/south/east/west) match actual chart positions
5. **System Extent Accuracy**: Ensure described pressure system sizes and coverage areas match chart representations

**Spatial Accuracy Examples**:
- **Accurate**: "High pressure center at 45°N, 15°E over the Alps" (when chart shows center at 44°N, 16°E)
- **FAILED**: "High pressure center over the North Sea" (when chart shows center over Scandinavia - >200 km error)

**Red Flags**: Any pressure center >2° from actual position, domain truncation, geographic anchor misplacement

### Step 2: Theoretical and Seasonal Consistency Validation (Scientific Plausibility Assessment)
**Objective**: Ensure all described patterns align with meteorological theory and seasonal expectations

**How to Assess Theoretical Consistency**:
1. **Seasonal Pattern Validation**: Check if described patterns match climatological expectations for the given date/location
2. **Circulation Model Consistency**: Verify patterns align with three-cell circulation model, jet stream positions, typical pressure system locations
3. **Physical Process Verification**: Ensure temperature-pressure relationships follow atmospheric physics principles
4. **Gradient Plausibility**: Confirm pressure gradients and system intensities are meteorologically realistic
5. **System Interaction Logic**: Validate that described system interactions follow known atmospheric dynamics

**Theoretical Consistency Examples**:
- **Consistent**: "1048 hPa Siberian high in February promotes continental cold air mass" (seasonally appropriate)
- **Inconsistent**: "1048 hPa Siberian high in July" (climatologically implausible intensity/timing)

### Step 3: Multi-Scale Internal Consistency Verification (Logical Coherence Assessment)
**Objective**: Assess whether all described elements align logically across spatial scales and within the description framework

**How to Assess Multi-Scale Consistency**:
1. **Cross-Scale Logical Verification**: Ensure local features are consistent with regional patterns, which are consistent with broader atmospheric context
2. **Spatial Relationship Consistency**: Verify all described spatial relationships are internally coherent (if A is north of B, coordinates must reflect this)
3. **Quantitative Cross-Verification**: Check that different quantitative references support each other rather than contradict
4. **System Interaction Consistency**: Ensure described system interactions are logical across all mentioned scales
5. **Reference Framework Consistency**: Verify coordinate systems, units, and measurement frameworks remain consistent throughout

**Multi-Scale Consistency Examples**:
- **Consistent**: "North Atlantic high (1028 hPa) extends ridge over western Europe, promoting subsidence and clear skies across Britain"
- **Inconsistent**: "High pressure over Britain promotes storms" (contradictory meteorological relationship)

### Step 4: Quantitative Precision and Chart Fidelity Assessment (Data Accuracy Analysis)
**Objective**: Evaluate numerical accuracy and measurement consistency against source chart capabilities

**How to Assess Quantitative Precision**:
1. **Chart Resolution Compliance**: Ensure claimed precision doesn't exceed source chart measurement capabilities
2. **Value Range Verification**: Confirm all described ranges accurately reflect chart data distribution
3. **Unit Accuracy and Consistency**: Verify all quantitative values include correct, consistent units throughout
4. **Measurement Interval Consistency**: Check that described measurement intervals match chart specifications
5. **Extreme Value Validation**: Ensure claimed extreme values are actually visible/readable from the source chart

**Quantitative Precision Examples**:
- **Accurate**: "Pressure contours at 4 hPa intervals from 1004 to 1032 hPa" (matches chart contour labeling)
- **Inaccurate**: "Pressure varies continuously from 1004.3 to 1031.7 hPa" (false precision beyond chart resolution)

## SCORING FRAMEWORK

**Score 5 - Perfect Consistency**
- ALL pressure centers within ±2° tolerance with perfect spatial accuracy throughout
- Complete theoretical consistency with seasonal expectations and circulation models
- Flawless multi-scale internal logic with no contradictions across any spatial scales
- Perfect quantitative precision matching chart resolution capabilities exactly
- Complete domain coverage accuracy with no truncations or omissions

**Score 4 - Strong Consistency**
- ALL pressure centers within ±2° tolerance with minor spatial reference inconsistencies elsewhere
- Strong theoretical consistency with minor seasonal or circulation model deviations
- Generally strong multi-scale logic with occasional minor internal contradictions
- High quantitative accuracy with minor unit inconsistencies or precision issues
- Complete domain coverage with minor boundary specification issues

**Score 3 - Adequate Consistency**
- MOST pressure centers within ±2° tolerance but some minor spatial accuracy issues
- Generally appropriate theoretical patterns with some seasonal or theoretical inconsistencies
- Adequate multi-scale consistency but noticeable internal contradictions requiring clarification
- Generally accurate quantitative data with some precision or unit issues
- Adequate domain coverage but some specification problems

**Score 2 - Poor Consistency**
- SOME pressure centers exceed ±2° tolerance or significant spatial accuracy problems
- Poor theoretical consistency with multiple seasonal or circulation model violations
- Significant multi-scale contradictions affecting scientific interpretation
- Quantitative errors that could mislead analysis with widespread unit or precision problems
- Incomplete or inaccurate domain coverage affecting interpretation

**Score 1 - Very Poor Consistency**
- MOST pressure centers exceed ±2° tolerance with major spatial misplacements throughout
- Major theoretical inconsistencies violating seasonal patterns and circulation principles
- Extensive multi-scale contradictions severely undermining description credibility
- Substantial quantitative errors affecting interpretation with pervasive precision/unit problems
- Major domain coverage errors or truncations affecting scientific utility

**Score 0 - No Consistency**
- ALL or most pressure centers grossly misplaced (>5° errors) making description actively misleading
- Complete theoretical implausibility violating basic atmospheric physics
- Pervasive contradictions making description scientifically unusable
- Quantitative data largely incorrect or nonsensical throughout
- Domain coverage completely inaccurate or missing

## CRITICAL EVALUATION STANDARDS

**MANDATORY PASS-FAIL THRESHOLDS**:
- **ANY pressure center >2° from actual position**: Maximum score 1 (description becomes actively misleading)
- **Domain truncation when full coverage exists**: Maximum score 2 (incomplete scientific information)
- **Major theoretical violations** (e.g., impossible seasonal patterns): Maximum score 2
- **Extensive quantitative errors** beyond chart resolution: Maximum score 2

**Excellence Requirements** (Score 4-5):
- **Perfect spatial accuracy**: ALL pressure centers within ±2° tolerance
- **Complete theoretical consistency**: Seasonal and circulation model alignment
- **Multi-scale coherence**: No internal contradictions across spatial scales
- **Quantitative precision**: Accuracy matching chart resolution capabilities

## COMMON PITFALLS TO AVOID

1. **Spatial Accuracy Tolerance**: ZERO tolerance for >2° pressure center errors - these make descriptions actively misleading
2. **Theoretical Complexity Confusion**: Don't excuse clear seasonal/circulation violations as "atmospheric complexity" 
3. **Chart Resolution Expectations**: Don't demand precision beyond chart capabilities, but verify claimed precision is achievable
4. **Multi-Scale Logic**: Ensure local descriptions are consistent with regional and broader patterns mentioned
5. **Domain Coverage Standards**: Verify complete coverage matches chart extent - no artificial truncations acceptable

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

## RELEVANCE STANDARDS FOR METEOROLOGICAL ANALYSIS

**Core Definition**: Relevance measures whether descriptions prioritize meteorologically significant patterns and enable expert-level analytical conclusions equivalent to visual chart inspection.

**Expert-Level Requirements** (based on professional meteorological analysis):
- **Multi-Scale Integration Priority**: Most important patterns emphasized across global/regional/local scales as appropriate
- **Dynamic Process Emphasis**: Static data transformed into circulation patterns and weather implications
- **Theoretical Framework Priority**: Seasonal validation and circulation model context for significant patterns
- **Analytical Enablement**: Sufficient information for forecast reasoning, process understanding, and research decisions

**Information Priority Hierarchy**:
1. **Most Intense Systems**: Strongest pressure centers and steepest gradients receive primary emphasis
2. **Meteorologically Significant Patterns**: Unusual, extreme, or climatologically important features highlighted
3. **Multi-Scale Context**: Pattern significance established through appropriate scale connections
4. **Dynamic Implications**: Weather and circulation consequences of observed patterns

## EVALUATION PROCESS

### Step 1: Meteorological Significance Prioritization Assessment (Primary Pattern Analysis)
**Objective**: Evaluate whether the most meteorologically significant systems receive appropriate emphasis and early attention

**How to Assess Meteorological Significance Prioritization**:
1. **System Intensity Ranking**: Verify strongest pressure systems (highest/lowest values) receive primary emphasis
2. **Gradient Significance Assessment**: Check that steepest pressure gradients and strongest temperature contrasts are highlighted early
3. **Climatological Importance Evaluation**: Assess whether unusual, extreme, or seasonally significant patterns receive appropriate attention
4. **Early Emphasis Verification**: Confirm most significant patterns appear early in description rather than buried in secondary details
5. **Comparative Intensity Assessment**: Ensure system strength rankings in text match actual meteorological intensity

**Significance Prioritization Examples**:
- **Excellent**: "The exceptional 1052 hPa high pressure system dominates northern Europe, representing extreme subsidence..." (leads with most intense feature)
- **Poor**: "Various pressure systems exist across Europe, including a 1052 hPa high..." (buries extreme intensity in generic statement)

### Step 2: Multi-Scale Integration and Dynamic Process Priority (Analytical Depth Assessment)
**Objective**: Assess whether descriptions prioritize multi-scale connections and dynamic process understanding over static data reporting

**How to Assess Multi-Scale Integration and Dynamic Process Priority**:
1. **Multi-Scale Connection Emphasis**: Verify that scale connections receive adequate emphasis rather than being treated as afterthoughts
2. **Dynamic Process Integration Priority**: Check that circulation patterns and weather implications receive prominent attention
3. **Static-to-Dynamic Transformation**: Assess whether static pressure/temperature data is systematically transformed into process understanding
4. **Process Mechanism Explanation**: Evaluate whether physical mechanisms behind observed patterns receive appropriate attention
5. **Weather Implication Priority**: Verify that weather consequences of pressure systems receive adequate emphasis

**Dynamic Process Priority Examples**:
- **Excellent**: "The 1028 hPa high drives anticyclonic circulation, promoting subsidence and clear skies (inferred) across western Europe, while creating strong pressure gradients..."
- **Adequate**: "High pressure (1028 hPa) over western Europe creates clear conditions..."
- **Poor**: "Pressure values: 1028 hPa high, 1012 hPa low, 1020 hPa ridge..." (static data listing without process integration)

### Step 3: Expert-Level Analytical Enablement Assessment (Research Utility Analysis)
**Objective**: Determine whether descriptions enable the same analytical conclusions and research capabilities as expert meteorological analysis

**How to Assess Expert-Level Analytical Enablement**:
1. **Forecast Reasoning Capability**: Assess whether description provides sufficient information for weather prediction and forecast reasoning
2. **Process Understanding Support**: Evaluate if description enables understanding of atmospheric processes and physical mechanisms
3. **Research Decision Support**: Determine whether operational or research decisions could be made based on the provided information
4. **Comparative Analysis Capability**: Check if description enables comparison with climatological patterns and seasonal expectations
5. **Independent Validation Potential**: Assess whether readers can independently verify and extend the analytical conclusions

**Analytical Enablement Examples**:
- **Expert-Level**: "The 1052 hPa Scandinavian high, exceptional for February, promotes continental cold air advection through geostrophic balance, creating temperature gradients of 15°C/500 km across central Europe, indicating strong frontal potential..."
- **Limited**: "High pressure over Scandinavia brings cold weather to Europe..."
- **Insufficient**: "Cold temperatures across Europe..." (no analytical framework provided)

### Step 4: Information Efficiency and Contextual Appropriateness (Optimization Analysis)
**Objective**: Evaluate whether word limit usage maximizes meteorological value and matches chart scale/context appropriately

**How to Assess Information Efficiency and Contextual Appropriateness**:
1. **Word Limit Optimization**: Verify that every significant meteorological detail serves analytical purposes rather than filling space
2. **Scale-Appropriate Detail Level**: Assess whether detail level matches chart scale (global vs regional vs local analysis priorities)
3. **Seasonal/Geographic Context Alignment**: Check that emphasis matches regional and seasonal meteorological priorities
4. **Analytical Value Density**: Evaluate whether included details directly support meteorological conclusions and understanding
5. **Context-Specific Priority Matching**: Verify that emphasized patterns match typical meteorological analysis priorities for the given domain/season

**Information Efficiency Examples**:
- **Efficient**: "The 1048 hPa Siberian high, intense for early March, drives continental outflow affecting European temperatures by 10-15°C below normal..."
- **Inefficient**: "The Siberian high pressure system has a central pressure of 1048 hPa and covers a large area of Siberia with generally high pressure conditions..."
- **Inappropriate Scale**: Discussing global circulation for a European regional chart when European synoptic patterns should dominate

## SCORING FRAMEWORK

**Score 5 - Exceptional Relevance**
- Perfect prioritization of strongest systems and most significant patterns with early emphasis
- Exceptional multi-scale integration and dynamic process emphasis throughout description
- Expert-level analytical enablement supporting forecast reasoning, process understanding, and research decisions
- Optimal information efficiency maximizing meteorological value with perfect scale/context appropriateness
- Every detail directly supports primary meteorological conclusions and enables equivalent analysis to visual inspection

**Score 4 - Strong Relevance**
- Strong prioritization of significant systems with most important patterns emphasized early
- Good multi-scale integration and dynamic process emphasis with minor static data focus
- High-quality analytical enablement supporting most forecast and research needs with minor limitations
- Good information efficiency with occasional less critical details but generally appropriate scale/context matching
- Most details effectively support meteorological conclusions and analytical capabilities

**Score 3 - Adequate Relevance**
- Generally appropriate prioritization but some significant patterns under-emphasized or buried
- Adequate multi-scale integration but noticeable emphasis on static data over dynamic processes
- Basic analytical enablement supporting fundamental meteorological analysis but missing some research opportunities
- Reasonable information efficiency but some space wasted on less critical details with occasional scale/context mismatches
- Mix of relevant and less relevant details affecting overall analytical efficiency

**Score 2 - Poor Relevance**
- Poor prioritization with important systems under-emphasized and weak systems over-emphasized
- Limited multi-scale integration with heavy focus on static data reporting over process understanding
- Limited analytical enablement providing insufficient information for forecast reasoning or research analysis
- Poor information efficiency with significant space devoted to minor details and poor scale/context matching
- Many included details don't support primary meteorological understanding or analytical conclusions

**Score 1 - Very Poor Relevance**
- Major meteorological features largely ignored with inappropriate emphasis on minor systems
- Minimal multi-scale integration with predominantly static data listing and little process understanding
- Severely limited analytical enablement preventing quality meteorological analysis and research application
- Very poor information efficiency focusing on insignificant details with inappropriate scale/context priorities
- Most included details irrelevant to meteorological analysis needs and conclusions

**Score 0 - No Relevance**
- Complete failure to identify or appropriately emphasize any significant meteorological patterns
- No multi-scale integration or dynamic process emphasis - purely static data reporting
- No analytical enablement capability - description provides no useful meteorological analysis support
- Information completely unfocused with no appropriate meteorological priorities or context consideration
- Content largely irrelevant to meteorological analysis needs with no scientific value

## CRITICAL EVALUATION STANDARDS

**Pass-Fail Thresholds** (Automatic scoring guidance):
- **Strongest systems not emphasized early**: Maximum score 2 (defeats primary purpose)
- **No dynamic process integration**: Maximum score 2 (eliminates analytical value)
- **Insufficient detail for basic forecast reasoning**: Maximum score 2 (fails analytical enablement)
- **Inappropriate scale emphasis**: Maximum score 3 (mismatched context priorities)

**Excellence Indicators** (Score 4-5 requirements):
- **Perfect intensity-based prioritization**: Strongest systems receive primary emphasis early
- **Systematic dynamic process integration**: Static data transformed into circulation and weather understanding
- **Expert-level analytical enablement**: Sufficient detail for forecast reasoning and research decisions
- **Optimal information efficiency**: Every significant detail supports meteorological conclusions

## COMMON PITFALLS TO AVOID

1. **Intensity Ranking Errors**: Don't accept weak system emphasis over strong systems - intensity determines meteorological significance
2. **Static Data Tolerance**: Penalize pure data reporting without process integration - descriptions must enable dynamic understanding
3. **Completeness vs. Relevance Confusion**: Focus on meteorological significance, not comprehensive coverage of all features
4. **Scale Appropriateness**: Assess whether emphasis matches chart scale - don't accept global detail for regional charts or vice versa
5. **Analytical Utility Standards**: Verify descriptions enable the same conclusions as expert meteorological analysis

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


def get_default_criterion_evaluator_user_prompt(criterion: str) -> str:
    """
    Get the default CriteriaEvaluatorAgent user prompt for the specified criterion.

    Args:
        criterion (str): The criterion for which to get the default user prompt. Should be one of: coherence, fluency, consistency, relevance.

    Returns:
        str: The default criterion user prompt text.
    """
    if criterion == "coherence":
        return DEFAULT_COHERENCE_CRITERIA_EVALUATOR_USER_PROMPT
    elif criterion == "fluency":
        return DEFAULT_FLUENCY_CRITERIA_EVALUATOR_USER_PROMPT
    elif criterion == "consistency":
        return DEFAULT_CONSISTENCY_CRITERIA_EVALUATOR_USER_PROMPT
    elif criterion == "relevance":
        return DEFAULT_RELEVANCE_CRITERIA_EVALUATOR_USER_PROMPT
    else:
        raise ValueError(
            f"Unknown criterion: {criterion}. Valid options are: coherence, fluency, consistency, relevance."
        )
