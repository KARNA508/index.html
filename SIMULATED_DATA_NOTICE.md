# Dataset Provenance Notice

## Status

**Dataset status: SOURCE UNVERIFIED**

The file `data/sample_mic_data.csv` is included in a mini-project package generated with help from Grok. The student does not know where the CSV values originated. The package does not document a database accession, download URL, publication, or original laboratory source.

The code in `code/resistance_verification.py` reads the local CSV using `pandas.read_csv(filepath)`. It does not itself download data from NCBI or another external source. This only describes the code in the supplied package; it cannot establish what source, if any, was used before the files were generated.

## What the records contain

The CSV has eight rows and these columns:

- `Sample_ID`: record identifier
- `Strain`: descriptive label
- `Zone_mm`: inhibition-zone value in millimetres
- `MIC_ug_per_ml`: MIC value in micrograms per millilitre
- `Notes`: descriptive note

The source and status of the values are not verified. Labels such as `Patient1`, `Clinical`, and `LabMutant` are just text in the CSV; they do not prove the records are real patient samples, clinical isolates, or experimental results.

## What can and cannot be concluded

Until provenance is established, the values should be treated as **unverified sample data for demonstration**, not as verified measurements or confirmed simulated data. They cannot establish the prevalence of resistance, verify that any bacterium is resistant, validate a diagnostic method, or support treatment decisions.

## Reporting language

Use wording such as:

> “The project package includes eight sample records, but their original source could not be verified. We use them only to demonstrate basic data handling and visualisation, and we do not draw clinical conclusions.”

Do not claim the data came from NCBI, a publication, or a clinical laboratory unless a traceable source confirms that claim. Do not present the program as a clinical decision tool.

## How to investigate provenance

1. Ask Grok for the exact source URL, accession numbers, publication, and explanation of whether it generated or copied the CSV values.
2. Review any original prompt, conversation, references, or download instructions from the session that generated the module.
3. Check whether the source actually contains the same records and values.
4. If no traceable source can be found, retain the status **source unverified**. Do not guess a source based on plausible-looking values.

## Reproducibility checklist

- [x] Do not claim NCBI provenance without evidence.
- [x] Avoid presenting the values as verified clinical findings.
- [ ] Record a source URL or accession only if independently confirmed.
- [ ] If replacing the examples with public data later, record database, accession identifiers, download date, licence/terms, processing steps, and exclusions.
