# What's New in GMSC-mapper 0.2.0

## User-visible Improvements

* Add `# GMSC-mapper version ...` comments to generated TSV outputs and
  `summary.txt`
* Add a `citation` subcommand to print the paper citation
* Download xz-compressed FASTA and convert to gzip on the fly
* Use the `requests` library instead of `wget` for database downloads
* Remove auto-download/install of DIAMOND and MMseqs; show an error if the
  tools are not installed
* Add a `--version` option
* Validate the `--mode` argument in the `createdb` subcommand

## Bugfixes

* Fix typo in output filename: `predicted.filterd.smorf.faa` to
  `predicted.filtered.smorf.faa`
* Fix `FutureWarning` from newer pandas in taxonomy mapping
* Fix inverted condition in contig length check
* Fix duplicate sequence filtering in `filter_smorfs()`
* Fix overly broad exception handling in `generate_fasta()`
* Fix resource leak in `predicted_smorf_count()`

## Internal changes

* Convert project packaging from `setup.py` to `pyproject.toml`
* Update testing to use `uv`
* Test in newer versions of Python
* Use the `tmp_path` fixture in tests
* Skip diamond/MMseqs tests when the binaries are not in `PATH`
* Remove outdated installation helpers
