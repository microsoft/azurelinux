# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           package-notes
Version:        0.5
Release: 17%{?dist}
Summary:        Generate LDFLAGS to insert .note.package section
License:        0BSD
URL:            https://github.com/systemd/package-notes

Source0:        redhat-package-notes.in
Source1:        macros.package-notes-srpm

BuildArch:      noarch

%description
This package provides a generator of linker scripts that insert a section with
an ELF note with a JSON payload that describes the package the binary was built
for.

%package srpm-macros
Summary:        %{summary}
Obsoletes:      package-notes < 0.5
# Those are minimum versions that implement --package-metadata
Conflicts:      binutils < 2.37-34
Conflicts:      binutils-gold < 2.37-34
Conflicts:      mold < 1.3.0
Conflicts:      lld < 14.0.5-4

%description srpm-macros
RPM macros to insert a section with an ELF note with a JSON payload that
describes the package the binary was built for via a compiler spec file.

%prep
# nothing to do

%build
sed -e "s|@OSCPE@|cpe:/o:microsoft:azurelinux:4.0|" -e "s|@OS@|azurelinux|" -e "s|@OSVERSION@|4.0|" %{SOURCE0} >redhat-package-notes

# Self-test: fail the build loudly if these overlays did not inject the
# expected .note.package fields into the generated linker spec, rather than
# silently shipping binaries with missing OS / moduleVersion metadata. The
# bare "os" field is added by the same overlay as osVersion and moduleVersion,
# so verifying these three covers it.
for field in osCpe osVersion moduleVersion; do
    grep -qF "$field" redhat-package-notes || { echo "ERROR: generated redhat-package-notes is missing the '$field' field -- package-notes overlay regression" >&2; exit 1; }
done
# moduleVersion's value comes from RPM_MODULE_VERSION, exported by the
# %_generate_package_note_file hook in macros.package-notes-srpm. If a future
# rebase reverts that macro to the upstream %{nil}, moduleVersion would
# silently become empty in every downstream binary -- fail now instead.
grep -q RPM_MODULE_VERSION %{SOURCE1} || { echo "ERROR: macros.package-notes-srpm no longer exports RPM_MODULE_VERSION -- the _generate_package_note_file hook was removed" >&2; exit 1; }

%install
install -Dt %{buildroot}%{_rpmconfigdir}/redhat/ redhat-package-notes
install -m0644 -Dt %{buildroot}%{_rpmmacrodir}/ %{SOURCE1}

%files srpm-macros
%{_rpmconfigdir}/redhat/redhat-package-notes
%{_rpmmacrodir}/macros.package-notes-srpm

%changelog
* Tue Jun 09 2026 Andrew Phelps <anphel@microsoft.com> - 0.5-17
- Embed Azure Linux osCpe, os, osVersion, and 4-part moduleVersion fields in
  the .note.package ELF metadata, and self-test that the overlays applied
