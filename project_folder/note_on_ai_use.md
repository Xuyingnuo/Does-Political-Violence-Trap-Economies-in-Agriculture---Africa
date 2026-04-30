# Note on AI Use

This project used an AI coding assistant throughout the research workflow to accelerate ideation, coding, data cleaning, visualization, and drafting. The AI-supported parts were always treated as suggestions: I exercised my own judgment to design analyses, validate outputs, and edit text before inclusion in the final deliverables.

## Scope of AI use
- Brainstorming research questions and analysis approaches (causal pathways, thresholds, lag structure).
- Producing and iterating Python code snippets for data ingestion, cleaning, and plotting used in the notebooks under `code/`.
- Generating the HTML conclusion infographic (`docs/assets/conclusion_infographic.html`) and small interactive UI snippets.
- Drafting and copyediting text for the final report and figure captions.

## Validation and verification
All AI-generated code and text were validated manually before being accepted into the project. Validation steps included:

- Running the provided notebooks (`code/01_data_cleaning.ipynb`, `code/02_exploration.ipynb`, `code/03_analysis.ipynb`) to ensure code executed without errors and produced expected intermediate results.
- Inspecting produced datasets in `outputs/cleaned/` and checking shape, variable names, and a few spot-checks of summary statistics against raw sources.
- Reviewing plots and the interactive infographic rendered in `docs/` for accuracy of labels, legends, and numbers.
- Carefully proofreading all AI-drafted text, verifying that citations and data source references (ACLED, World Bank, V-Dem) are correct and consistent with the analyses.

## Limitations and responsibility
AI suggestions can be helpful but are not infallible. I treated the assistant as a productivity tool, not as an authority: the responsibility for all analysis decisions, interpretation of results, and final wording rests with me. Specific limitations I guarded against:

- Hallucinated claims: I verified every factual statement produced by the assistant against the computed results or original data.
- Code correctness: I ran the code end-to-end and inspected outputs; where needed, I refactored or rewrote snippets to ensure clarity and reproducibility.

## Reproducibility and notes for reviewers
The analysis environment (notebooks and scripts) and cleaned data are included in the repository. Key data sources used are listed in the project `docs/` and in the notebooks: ACLED, World Bank, and V-Dem (1996–2023). If you wish to reproduce the exact results, run the notebooks in order, starting with `code/01_data_cleaning.ipynb`, then `02_exploration.ipynb`, and finally `03_analysis.ipynb` which generates the `conclusion_infographic.html` used in the site.

## Summary of AI roles
- Research design ideation: Suggested plausible questions and visual approaches that I adapted and tested.
- Data cleaning code: Provided starter code; I validated and adjusted it for edge cases.
- Visualization & HTML snippets: Generated prototype HTML/CSS and JavaScript for the interactive infographic; I tested and tuned it.
- Draft text & copyediting: Drafted text that I edited for accuracy and clarity.

## Additional AI tools

Beyond the primary coding assistant, I also used other large language models to strengthen specific aspects of the project:

- Deepseek: Used to brainstorm and explore topic insights, alternative framing of research questions, and potential policy implications. Deepseek provided diverse perspectives on how conflict shapes economic structures and suggested angles for the narrative.

- Gemini: Employed for webpage design suggestions and layout optimization for the interactive HTML assets in `docs/`. Gemini offered responsive design recommendations that improved the user experience of the infographic and report visualization. Additionally, Gemini was used as a secondary grammar checker and copy-editor to ensure clarity, consistency, and professional tone across all written text, including figure captions and section introductions.

All suggestions from these tools were carefully reviewed and incorporated only after manual validation. I verified that design recommendations were implemented correctly, that grammar corrections improved readability without changing intended meaning, and that topic insights aligned with the actual data findings.

## Final note
Using an AI assistant significantly sped up routine work and helped generate creative presentation ideas, but all substantive decisions, validation, and final editing were performed by me. I accept full responsibility for the analysis, results, and conclusions presented in this repository.