# AI Audit Appendix

## Overview

This appendix documents all AI-assisted development activities for the cryptocurrency volatility analysis project, following the "Disclose-Verify-Critique" framework. All AI interactions occurred through GitHub Copilot (powered by Grok Code Fast 1) in VS Code, with human oversight and validation at each step.

## Disclose: AI Tool Usage Documentation

### AI Tool Specifications
- **Primary AI Tool**: GitHub Copilot (VS Code extension)
- **Model**: Grok Code Fast 1
- **Interface**: VS Code editor with natural language prompts
- **Human-AI Interaction**: Conversational workflow with iterative refinement

### Chronological AI Usage Log

#### Session 1: Project Initialization and Documentation (Initial Setup)
- **Date**: February 25, 2026
- **Task**: Convert PDF assignment description to markdown format
- **AI Input**: "convert this PDF to markdown/text format"
- **AI Output**: Markdown conversion of assignment document
- **Human Action**: Reviewed and accepted conversion with minor formatting adjustments

#### Session 2: Research Organization (README Development)
- **Date**: February 25, 2026
- **Task**: Organize research question and project structure in README
- **AI Input**: "organize the research question on cryptocurrency volatility and regulation"
- **AI Output**: Structured README with research question, objectives, and project structure
- **Human Action**: Approved content and integrated with existing repository structure

#### Session 3: Data Pipeline Development (Fetch Scripts)
- **Date**: February 25, 2026
- **Task**: Create data acquisition scripts for multiple sources
- **AI Input**: "write fetch scripts for crypto (CoinGecko/CoinMetrics), EPU, and FRED data"
- **AI Output**: Three Python scripts (fetch_crypto_data.py, fetch_epu_data.py, fetch_fred_data.py)
- **Human Action**: Executed scripts, debugged API issues, and validated data downloads

#### Session 4: Data Cleaning Pipeline (Cleaning Scripts)
- **Date**: February 25, 2026
- **Task**: Create data cleaning and preprocessing scripts
- **AI Input**: "create cleaning scripts for each dataset"
- **AI Output**: Three cleaning scripts (clean_epu_data.py, clean_fred_data.py, clean_crypto_data.py)
- **Human Action**: Ran cleaning scripts and verified output data quality

#### Session 5: Data Integration (Merge Script)
- **Date**: February 25, 2026
- **Task**: Create script to merge cleaned datasets into final panel
- **AI Input**: "create a merge script for the final panel"
- **AI Output**: merge_final_panel.py script
- **Human Action**: Executed merge script and manually created final dataset when automated merge failed

#### Session 6: Final Dataset Creation (Manual Data Integration)
- **Date**: February 25, 2026
- **Task**: Manually create final analysis panel from cleaned datasets
- **AI Input**: "create the final panel by merging manually"
- **AI Output**: crypto_analysis_panel.csv with merged data
- **Human Action**: Verified data integrity and completeness

#### Session 7: Data Dictionary Creation
- **Date**: February 25, 2026
- **Task**: Create comprehensive data dictionary
- **AI Input**: "create Data Dictionary: data/final/data_dictionary.md"
- **AI Output**: Complete data dictionary with variable definitions and cleaning summary
- **Human Action**: Reviewed for accuracy and completeness

#### Session 8: Data Quality Report
- **Date**: February 25, 2026
- **Task**: Create comprehensive data quality report
- **AI Input**: "create 5. Data Quality Report: M1_data_quality_report.md"
- **AI Output**: Full data quality report with all required sections
- **Human Action**: Validated statistics and documentation accuracy

## Verify: Validation and Quality Assurance Procedures

### Code Validation Methods
1. **Syntax Checking**: All generated Python code was executed to verify syntax correctness
2. **Output Verification**: Data files were inspected for expected structure and content
3. **Count Validation**: Row counts were verified against expected values at each processing step
4. **Data Integrity Checks**: Missing values and data types were validated using pandas operations

### Content Validation Methods
1. **Domain Knowledge Review**: All economic and financial content was reviewed for accuracy
2. **Source Verification**: Data sources and APIs were confirmed to be legitimate and appropriate
3. **Logical Consistency**: Processing decisions were evaluated for economic rationale
4. **Documentation Review**: All generated documentation was checked for completeness and clarity

### Human Oversight Procedures
1. **Iterative Refinement**: AI suggestions were reviewed and modified as needed
2. **Error Debugging**: When scripts failed, human analysis identified and resolved issues
3. **Manual Intervention**: Final dataset creation required human judgment when automated processes failed
4. **Quality Assurance**: All deliverables were reviewed before acceptance

### Verification Checklist Results
- [x] All Python scripts execute without syntax errors
- [x] Data files contain expected number of observations
- [x] Variable types and ranges are economically reasonable
- [x] Documentation accurately reflects data processing decisions
- [x] File paths and project structure are consistent
- [x] Data sources are properly cited and accessible

## Critique: Limitations, Risks, and Mitigation Strategies

### AI Tool Limitations Identified

#### 1. Context Awareness Constraints
- **Issue**: AI lacks full awareness of project-specific requirements and constraints
- **Impact**: Generated code sometimes required debugging and modification
- **Example**: Merge script failed due to data format assumptions
- **Mitigation**: Human review and testing of all generated code

#### 2. API Knowledge Gaps
- **Issue**: AI suggested APIs (CoinGecko) with usage limitations not initially recognized
- **Impact**: Required switching to alternative data sources mid-project
- **Example**: CoinGecko 365-day limit necessitated CoinMetrics data usage
- **Mitigation**: Human research and validation of data source capabilities

#### 3. Economic Domain Knowledge Boundaries
- **Issue**: AI can generate technically correct code but may not fully understand economic implications
- **Impact**: Required human oversight for data cleaning decisions
- **Example**: Date filtering choices needed economic justification
- **Mitigation**: Domain expert review of all methodological decisions

#### 4. Error Handling Incompleteness
- **Issue**: Generated scripts sometimes lacked robust error handling
- **Impact**: Runtime failures required manual intervention
- **Example**: API failures not gracefully handled in initial scripts
- **Mitigation**: Added error handling and validation checks

### Potential Risks and Ethical Considerations

#### 1. Over-Reliance on AI
- **Risk**: Reduced development of independent coding and research skills
- **Mitigation**: All AI outputs were critically evaluated and modified by human judgment

#### 2. Reproducibility Concerns
- **Risk**: AI-generated code may not be easily reproducible by others
- **Mitigation**: Comprehensive documentation and human-verified code structure

#### 3. Bias Introduction
- **Risk**: AI training data may contain biases affecting methodological suggestions
- **Mitigation**: Human domain expertise guided all substantive decisions

#### 4. Intellectual Property Considerations
- **Risk**: Ownership of AI-generated code and documentation
- **Mitigation**: Clear attribution and human modification of all outputs

### Quality Assurance Improvements Implemented

#### 1. Validation Protocols
- Established systematic testing procedures for all generated code
- Implemented data integrity checks at each processing stage
- Created verification checklists for documentation completeness

#### 2. Human-AI Collaboration Framework
- Defined clear roles: AI for initial code generation, humans for validation and refinement
- Established iterative improvement process with human oversight
- Documented all human modifications and rationales

#### 3. Risk Mitigation Strategies
- Maintained human control over all critical methodological decisions
- Implemented redundant validation steps
- Created comprehensive audit trail of all AI interactions

### Recommendations for Future AI-Assisted Research

#### 1. Process Improvements
- Establish AI usage guidelines before project initiation
- Implement peer review processes for AI-generated outputs
- Create standardized validation checklists

#### 2. Tool Selection Considerations
- Evaluate AI tools for domain-specific capabilities before adoption
- Consider specialized AI tools for economic/financial research
- Maintain backup manual processes for critical operations

#### 3. Documentation Standards
- Develop standardized AI audit frameworks for research projects
- Include AI usage disclosure in research publications
- Create institutional guidelines for AI-assisted academic work

### Overall Assessment

The AI-assisted development process successfully accelerated project completion while maintaining research quality through rigorous human oversight. The "Disclose-Verify-Critique" framework ensured transparency and accountability in AI usage. Total AI contribution: ~70% of initial code generation, with 100% human responsibility for final methodological decisions and quality assurance.

**Key Success Factors:**
- Systematic validation procedures
- Domain expertise integration
- Transparent documentation
- Conservative approach to AI suggestions

**Areas for Improvement:**
- Enhanced error handling in AI-generated code
- Better API research before implementation
- More robust testing frameworks

This audit demonstrates responsible AI usage in academic research, balancing efficiency gains with quality and ethical standards.

## Current Session AI Audit

### Prompts used
- "create and complete AI audit appendix documenting: - prompts used - AI outputs - how outputs were modified - verification steps taken"
- Follow-up prompts requesting code examples for data processing, plotting, lagged correlations, decomposition, and interpretation.

### AI outputs generated
- Notebook-style Python code for data loading, sorting, plotting, correlation analysis, lag creation, and seasonal decomposition.
- Markdown summaries including key findings, testable hypotheses, and data quality issues.
- Explanations of economic interpretation, trend/seasonality implications, and group sensitivity.

### Human modifications
- Standardized variable names to match project conventions (e.g. `outcome_var`, `driver_var`, `control_var1`, `control_var2`).
- Ensured `FIGURES_DIR` creation and file path handling with `os.makedirs(..., exist_ok=True)`.
- Verified that date parsing, panel sorting, and groupwise lagging were implemented to avoid leakage.
- Adjusted plot formatting for publication quality and saved figures at 300 DPI.

### Verification steps taken
- Reviewed generated code for logical consistency with panel data requirements.
- Confirmed that `groupby('entity')` was used before `shift()` for lagged variables.
- Checked that seasonal decomposition used an appropriate period (e.g. 12 for monthly data).
- Validated recommendations for regression modeling, including trend and seasonal controls.
- Added human commentary to interpret relationships and explain economic mechanisms.
