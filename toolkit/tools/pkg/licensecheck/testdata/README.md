# Test data for the license checker

The `licensecheck` package uses a heuristic to identify license files, the input data to this tool comes from the
packages currently in the distro.

The test data is generated from all the files packaged into `/usr/share/licenses/<pkg>/*` and is gathered via `repoquery`.

## Generating new test data

In a AzureLinux environment (specifically an environment with access the the package repos) run:

```bash
cd ./testdata
rm *.txt
tdnf -y install dnf-utils python3 ca-certificates
./generate_test_data.py
```

This will query the available repos and generate two files: `all_licenses_<date>.txt`, `all_docs_<date>.txt`, and
`all_other_files_<date>.txt` containing lists of all files that are either `%license` or `%doc` respectively, and all
other files (but not directories).

** Note: `all_other_files_*.txt` is marked to be ignored by git, it is a very large file and is less important to
validate against than `all_docs_<date>.txt`.

## Quick validation of the test data

This will read the files from above and report false positive/negative results, and generate a set of files containing
all "incorrect" findings.

```bash
cd ./testdata
find . -name 'all_other_files_*.txt' | grep -q . || echo "**** Generate test data first! ****"
go run . --licenses ./all_licenses_*.txt --licenses-output ./_tmp_bad_licenses.txt --docs ./all_docs_*.txt --docs-output ./_tmp_bad_docs.txt --other-files ./all_other_files_*.txt --other-files-output ./_tmp_bad_other_files.txt --exception-file ../../../../resources/manifests/package/license_file_exceptions.json
# Check ./_tmp_bad_licenses.txt, _tmp_bad_docs.txt, _tmp_bad_other_files.txt for any files that fail the classification
```

The test expects `< 1%` fail rate, i.e. `< 56 / 5615` files. As of `2024-04-25` there are `19` false positives in the
test set.
