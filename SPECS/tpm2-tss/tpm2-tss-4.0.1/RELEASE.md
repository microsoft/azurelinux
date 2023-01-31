# Release Process:
This document describes the general process that maintainers must follow when making a release of the `tpm2-tss` libraries.

# Milestones
All releases should have a milestone used to track the release. If the release version is not known, as covered in [Version Numbers](#Version Numbers),
then an "x" may be used for the unknown number, or the generic term "next" may be used. The description field of the milestone will be used to record
the CHANGELOG for that release. See [CHANGELOG Update](#CHANGELOG Update) for details.

# Version Numbers
Our releases will follow the semantic versioning scheme.
You can find a thorough description of this scheme here: [http://semver.org/](http://semver.org/)
In short, this scheme has 3 parts to the version number: A.B.C

* A is the 'major' version, incremented when an API incompatible change is made
* B is the 'minor' version, incremented when an API compatible change is made
* C is the 'micro' version, incremented for bug fix releases
Please refer to the [Semantic Versioning](http://semver.org/) website for the authoritative description.

## Version String
The version string is set for the rest of the autotools bits by autoconf.
Autoconf gets this string from the `AC_INIT` macro in the configure.ac file.
Once you decide on the next version number (using the scheme above) you must set it manually in configure.ac.
The version string must be in the form `A.B.C` where `A`, `B` and `C` are integers representing the major, minor and micro components of the version number.

## Release Candidates
In the run up to a release the maintainers may create tags to identify progress toward the release.
In these cases we will append a string to the release number to indicate progress using the abbreviation `rc` for 'release candidate'.
This string will take the form of `_rcX`.
We append an incremental digit `X` in case more than one release candidate is necessary to communicate progress as development moves forward.

# Static Analysis
Before a release is made the `coverity_scan` branch must be updated to the point in git history where the release will be made from.
This branch must be pushed to github which will cause the CI infrastructure to run an automated coverity scan.
The results of this scan must be dispositioned by the maintainers before the release is made.

# CHANGELOG Update
Before tagging the repository with the release version, the maintainer MUST update the CHANGELOG file with the contents from the description field
from the corresponding release milestone and update any missing version string details in the CHANGELOG and milestone entry.

# Git Tags
When a release is made a tag is created in the git repo identifying the release by the [version string](#Version String).
The tag should be pushed to upstream git repo as the last step in the release process.
**NOTE** tags for release candidates will be deleted from the git repository after a release with the corresponding version number has been made.
**NOTE** release (not release candidate) tags should be considered immutable.

## Signed tags
Git supports GPG signed tags and for releases after the `1.1.0` release will have tags signed by a maintainer.
For details on how to sign and verify git tags see: https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work.

# Release tarballs
We use the git tag as a way to mark the point of the release in the projects history.
We do not however encourage users to build from git unless they intend to modify the source code and contribute to the project.
For the end user we provide release "tarballs" following the GNU conventions as closely as possible.

To make a release tarball use the `distcheck` make target.
This target includes a number of sanity checks that are extremely helpful.
For more information on `automake` and release tarballs see: https://www.gnu.org/software/automake/manual/html_node/Dist.html#Dist

## Hosting Releases on Github
Github automagically generates a page in their UI that maps git tags to 'releases' (even if the tag isn't for a release).
Additionally they support hosting release tarballs through this same interface.
The release tarball created in the previous step must be posted to github using the release interface.
Additionally this tarball must be accompanied by a detached GPG signature.
The Debian wiki has an excellent description of how to post a signed release to Github here: https://wiki.debian.org/Creating%20signed%20GitHub%20releases
**NOTE** release candidates must be taken down after a release with the corresponding version number is available.

## Signing Release Tarballs
Signatures must be generated using the `--detach-sign` and `--armor` options to the `gpg` command:
```
$ gpg --detach-sign --armor tpm2-tss-X.Y.Z.tar.gz
```

## Verifying Signatures
Verifying the signature on a release tarball requires the project maintainers public keys be installed in the GPG keyring of the verifier.
With both the release tarball and signature file in the same directory the following command will verify the signature:
```
$ gpg --verify tpm2-tss-X.Y.Z.tar.gz.asc
```

## Signing Keys
The GPG keys used to sign a release tag and the associated tarball must be the same.
Additionally they must:
* belong to a project maintainer
* be discoverable using a public GPG key server
* be associated with the maintainers github account (https://help.github.com/articles/adding-a-new-gpg-key-to-your-github-account/)

# Announcements
Release candidates and proper releases should be announced on the 01.org TPM2 mailing list:
  - https://lists.linuxfoundation.org/mailman/listinfo/tpm2

This announcement should be accompanied by a link to the release page on Github as well as a link to the CHANGELOG.md accompanying the release.

# Maintenance
The most recent minor releases will receive bug fixes and bug fix releases.
Additionally the latest major release will receive bug fixes for another year after release.

# Release schedule
The project aims for 3 releases per year; early spring, summer, late fall.
Whether a release is a major or minor release depends on whether an API/ABI break occurs (see [Semantic Versioning](http://semver.org/)).
