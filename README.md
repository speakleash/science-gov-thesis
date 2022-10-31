# science-gov-thesis
Text extraction from large public pdf files (>50 pages) e.g. PhD theses, government reports, strategy description, etc.

The main script, based on the data/files.json file, retrieves the PDF files extracts the text from them and generates one aggregate jsonl file compressed with Zstandard (zstd)