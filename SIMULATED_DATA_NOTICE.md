# Simulated Data Notice

## Status

**Dataset status: SIMULATED / INVENTED EDUCATIONAL EXAMPLES**

The file `data/sample_mic_data.csv` supplied with the mini-project was created by the student as sample data. It was not downloaded from NCBI, and no external accession or original laboratory source is claimed.

## What the records contain

The CSV has eight illustrative rows and these columns:

- `Sample_ID`: example record identifier
- `Strain`: descriptive example label
- `Zone_mm`: invented example inhibition-zone diameter in millimetres
- `MIC_ug_per_ml`: invented example MIC value in micrograms per millilitre
- `Notes`: explanatory text written for the exercise

Labels such as `Patient1` and `Clinical` are only names in the invented examples. They do not refer to real people, patient samples, or clinical isolates.

## What can and cannot be concluded

This dataset can be used to practise reading a CSV, checking column types, making simple tables, and drawing educational plots.

It cannot establish the prevalence of resistance, verify that any bacterium is resistant, validate a diagnostic method, or support treatment decisions. No clinical breakpoint interpretation should be presented as validated for these invented records.

## Reporting language

Use wording such as:

> “We used eight simulated example records to demonstrate how inhibition-zone and MIC measurements can be organised and visualised in Python.”

Do not say:

- “NCBI data showed…”
- “Our clinical isolates showed…”
- “This program verified resistance…”
- “The results recommend an antibiotic…”

unless the project is redesigned around traceable, appropriately documented data and reviewed methods. Even then, a student website should not be presented as a clinical decision tool.

## Reproducibility checklist

- [x] Clearly label the records as simulated.
- [x] Do not claim NCBI provenance.
- [x] Remove resistance verdicts and treatment language from the website's interactive tool.
- [ ] Keep the CSV file alongside the code when sharing the full project.
- [ ] If replacing these examples with public data later, record the database, accession identifiers, download date, licence/terms, processing steps, and any exclusions before analysing it.
