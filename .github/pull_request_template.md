<!--
COMMENT BLOCKS WILL NOT BE INCLUDED IN THE PR.
Feel free to delete sections of the template which do not apply to your PR, or add additional details
-->

###### Merge Checklist  <!-- REQUIRED -->
<!-- You can set them now ([x]) or set them later using the Github UI -->
**All** boxes should be checked before merging the PR *(just tick any boxes which don't apply to this PR)*
- [ ] The toolchain has been rebuilt successfully (or no changes were made to it)
- [ ] The toolchain/worker package manifests are up-to-date
- [ ] Any updated packages successfully build (or no packages were changed)
- [ ] Packages depending on static components modified in this PR (Golang, `*-static` subpackages, etc.) have had their `Release` tag incremented.
- [ ] Package tests (%check section) have been verified with RUN_CHECK=y for existing SPEC files, or added to new SPEC files
- [ ] All package sources are available
- [ ] cgmanifest files are up-to-date and sorted (`./cgmanifest.json`, `./toolkit/scripts/toolchain/cgmanifest.json`, `.github/workflows/cgmanifest.json`)
- [ ] LICENSE-MAP files are up-to-date (`./SPECS/LICENSES-AND-NOTICES/data/licenses.json`, `./SPECS/LICENSES-AND-NOTICES/LICENSES-MAP.md`, `./SPECS/LICENSES-AND-NOTICES/LICENSE-EXCEPTIONS.PHOTON`)
- [ ] All source files have up-to-date hashes in the `*.signatures.json` files
- [ ] `sudo make go-tidy-all` and `sudo make go-test-coverage` pass
- [ ] Documentation has been updated to match any changes to the build system
- [ ] If you are adding/removing a .spec file that has multiple-versions supported, please add [@microsoft/cbl-mariner-multi-package-reviewers](https://github.com/orgs/microsoft/teams/cbl-mariner-multi-package-reviewers) team as reviewer [(Eg. golang has 2 versions 1.18, 1.21+)](https://github.com/microsoft/azurelinux/tree/2.0/SPECS/golang)
- [ ] Ready to merge

---

###### Summary <!-- REQUIRED -->
<!-- Quick explanation of the changes. -->
What does the PR accomplish, why was it needed?

###### Change Log  <!-- REQUIRED -->
<!-- Detail the changes made here. -->
<!-- Please list any packages which will be affected by this change, if applicable. -->
<!-- Please list any CVES fixed by this change, if applicable. -->
- Change
- Change
- Change

###### Does this affect the toolchain?  <!-- REQUIRED -->
<!-- Any packages which are included in the toolchain should be carefully considered. Make sure the toolchain builds with these changes if so. -->
<!-- Update: manifests/package/toolchain_*.txt, pkggen_core_*.txt, update_manifests.sh -->
<!-- To validate: make clean; make workplan REBUILD_TOOLCHAIN=y DISABLE_UPSTREAM_REPOS=y CONFIG_FILE="" ... -->
**YES/NO**

###### Associated issues  <!-- optional -->
<!-- Link to Github issues if possible. -->
<!-- you can use "fixes #xxxx" to auto close an associated issue once the PR is merged -->
- #xxxx

###### Links to CVEs  <!-- optional -->
- https://nvd.nist.gov/vuln/detail/CVE-YYYY-XXXX

###### Test Methodology
<!-- How was this test validated? i.e. local build, pipeline build etc. -->
- Pipeline build id: xxxx
