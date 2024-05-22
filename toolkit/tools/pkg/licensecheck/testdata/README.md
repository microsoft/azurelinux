# Test data for the license checker

The `licensecheck` package uses a heuristic to identify license files, the input data to this tool comes from the
packages currently in the distro.

The test data is generated from all the files packaged into `/usr/share/licenses/<pkg>/*` and is gathered via `repoquery`.

## Generating new test data

In a AzureLinux environment (specifically an environment with access the the package repos) run:

```bash
cd ./testdata
rm *.json
tdnf -y install dnf-utils python3 ca-certificates
./generate_test_data.py
```

This will query the available repos and generate two files: `all_licenses_<date>.json`, `all_docs_<date>.json`, and
`all_other_files_<date>.json` containing lists of all files that are either `%license` or `%doc` respectively, and all
other files (but not directories).

** Note: `all_other_files_*.json` is marked to be ignored by git, it is a very large file and is less important to
validate against than `all_docs_<date>.json`.

## Quick validation of the test data

This will read the files from above and report false positive/negative results, and generate a set of files containing
all "incorrect" findings.

```bash
cd ./testdata
find . -name 'all_other_files_*.json' | grep -q . || echo "**** Generate test data first! ****"
go run . --licenses ./all_licenses_*.json --licenses-output ./_tmp_bad_licenses.json --docs ./all_docs_*.json --docs-output ./_tmp_bad_docs.json --other-files ./all_other_files_*.json --other-files-output ./_tmp_bad_other_files.json --exception-file ../../../../resources/manifests/package/license_file_exceptions.json
# Check ./_tmp_bad_licenses.json, _tmp_bad_docs.json, _tmp_bad_other_files.json for any files that fail the classification
```

As of 2024-05-22 the results are:

- `1.9%` false negative (licenses)
- `0.25%` false positive (docs)
- `0.47%` false positive (all other files)
