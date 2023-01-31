# Guidelines for submitting bugs:
All non security bugs should be filed on the Issues tracker:
https://github.com/tpm2-software/tpm2-tss/issues

Security sensitive bugs should be handled per the instructions in the
[SECURITY](SECURITY.md) file.

# Guideline for submitting changes:
All changes to the source code must follow the coding standard used in the
surrounding source and documented [here](doc/coding_standard_c.md).

All changes should be introduced via github pull requests. This allows anyone to
comment and provide feedback in lieu of having a mailing list. For pull requests
opened by non-maintainers, any maintainer may review and merge that pull
request. For maintainers, they either must have their pull request reviewed by
another maintainer if possible, or leave the PR open for at least 24 hours, we
consider this the window for comments.

## Patch requirements
* All tests must pass on the CI system for the merge to occur with the exception of
  Cirrus. Cirrus failures should be manually evaluated by the maintainer to determine
  if it's a blocking failure or intermittent CI issues with Cirrus.
* All changes must not introduce superfluous changes or whitespace errors.
* All commits should adhere to the git commit message guidelines described
here: https://chris.beams.io/posts/git-commit/ with the following exceptions.
 * We allow commit subject lines up to 80 characters.
 * Commit subject lines should be prefixed with a string identifying the
effected subsystem. If the change is spread over a number of
subsystems then the prefix may be omitted. The general guidelines for prefix is to use the
top level directory name, a colon and space. For example, a change to `doc/logging.md`
would be "doc: ". Additional, more specific recommended prefixes are below for files in:
  - src/tss2-sys use prefix "sys: "
  - src/tss2-esys use prefix "esys: "
  - src/tss2-fapi use prefix "fapi: "
  - src/tss2-mu use prefix "mu: "
  - src/tss2-rc use prefix "rc: "
  - src/tss2-tcti use prefix "tcti: ".
    - However, "tcti-<subtcti>" should be used to indicate
      changes to a specific tcti vs the generic tcti layer.
  - to src/util is "util: "

* All contributions must adhere to the Developers Certificate of Origin. The
full text of the DCO is here: https://developercertificate.org/. Contributors
must add a 'Signed-off-by' line to their commits. This indicates the
submitters acceptance of the DCO.

## Guideline for merging changes

Pull Requests MUST be assigned to an upcoming release tag. If a release milestone does
not exist, the maintainer SHALL create it per the [RELEASE.md](RELEASE.md) instructions.
When accepting and merging a change, the maintainer MUST edit the description field for
the release milestone to add the CHANGELOG entry.

Changes must be merged with the "rebase" option on github to avoid merge commits.
This provides for a clear linear history.
