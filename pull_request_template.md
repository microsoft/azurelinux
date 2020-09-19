Updating Microsoft trusted root CAs.

###### Merge Checklist
**All** boxes should be checked before merging the PR *(just tick any boxes which don't apply to this PR)*
- [X] The toolchain has been rebuilt successfully (or no changes were made to it)
- [X] The toolchain/worker package manifests are up-to-date
- [X] Any updated packages successfully build (or no packages were changed)
- [X] All package sources are available
- [X] cgmanifest files are up-to-date and sorted (`./cgmanifest.json`, `./toolkit/tools/cgmanifest.json`, `./toolkit/scripts/toolchain/cgmanifest.json`)
- [X] All source files have up-to-date hashes in the `*.signatures.json` files
- [X] `sudo make go-tidy-all` and `sudo make go-test-coverage` pass
- [X] Documentation has been updated to match any changes to the build system
- [X] Ready to merge

---

###### Summary
**This is an automatically generated pull request.**

A change to the Microsoft trusted root CAs has been detected and to this pull request
has been created to address that change.

###### Change Log
- Updated the 'certdata.microsoft.txt' file containing the Microsoft trusted root CAs.

###### Does this affect the toolchain?
**NO**

###### Test Methodology
- Tested manually by building an image with the updated certificates and verifying access to PCM repository and Azure Watson servers.