# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Upstream actually uses a post-release snapshot of commit
# df4d68c09cdef73e023b8838a8bc7ca4dff1d1de “that addresses a missing include
# directive needed in more recent Visual Studio releases;” we should be able to
# get by with the release.
%global antl4_ver 4.13.2

Name:		adobe-afdko
Version:	4.0.3
Release:	1%{?dist}
Summary:	Adobe Font Development Kit for OpenType
# Everything is Apache-2.0 except:
#
# The following would affect the license of a python3-afdko subpackage, which
# we currently don’t have.
#
# - License of afdko-3.6.1/python/afdko/pdflib/pdfgen.py is said to be “same as
#   the Python license,” which would seem to suggest Python-2.0.1, but the
#   license text matches MIT-CMU.
# - Contents of python/afdko/resources/ are derived from adobe-mappings-cmap
#   and share its BSD-3-Clause license.
#
# The following do not affect the licenses of the binary RPMs.
#
# - ExternalAntlr4Cpp.cmake is BSD-3-Clause, as noted in LICENSE.md, but this
#   is a build-system file and does not affect the licenses of the binary RPMs
# - Various fonts and other test data files are OFL-1.1 (and/or
#   OFL-1.0-RFN/OFL-1.0-no-RFN?), but do not contribute to the licenses of the
#   binary RPMs
License:	Apache-2.0
URL:		https://github.com/adobe-type-tools/afdko
Source0:	%{url}/releases/download/%{version}/afdko-%{version}.tar.gz
Source1:	https://www.antlr.org/download/antlr4-cpp-runtime-%{antl4_ver}-source.zip
BuildRequires:	gcc g++
BuildRequires:	cmake
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-devel
BuildRequires:	utf8cpp-devel
Provides: bundled(antlr4-project) = %{antl4_ver}
%description
Adobe Font Development Kit for OpenType (AFDKO).
The AFDKO is a set of tools for building OpenType font files
from PostScript and TrueType font data.

%prep
%autosetup -p1 -n afdko-%{version}

%build
%set_build_flags
export XFLAGS="${CFLAGS} ${LDFLAGS}"
%cmake \
  -DANTLR4_ZIP_REPOSITORY:PATH=%{SOURCE1}
%cmake_build

%install
%cmake_install

%files
%license LICENSE.md
%doc docs/ README.md NEWS.md
%{_bindir}/detype1
%{_bindir}/makeotfexe
%{_bindir}/mergefonts
%{_bindir}/rotatefont
%{_bindir}/sfntdiff
%{_bindir}/sfntedit
%{_bindir}/spot
%{_bindir}/tx
%{_bindir}/type1

%changelog
* Tue Dec 09 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 4.0.3-1
- Updated to 4.0.3 release
- Bundled antlr4-cpp-runtime-4.13.2
- List packaged executables explicitly
- Correct/update and better document the License expression

* Tue Dec 09 2025 Cristian Le <git@lecris.dev> - 4.0.2-1
- Updated to 4.0.2 release
- Bundled antlr4-cpp-runtime-4.12.0
- Allow to build with CMake 4.0

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 25 2024 Manish Tiwari <matiwari@redhat.com> - 4.0.1-1
- Updated to 4.0.1 release
- Switched to CMake build system 
- Bundled antlr4-cpp-runtime-4.9.3

* Thu Jan 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.6.1-10
- Fix a typo in the License expression
- Fix build not respecting distribution compiler flags; this means executables
  are now PIE, and the debuginfo package is now useful

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 05 2024 Florian Weimer <fweimer@redhat.com> - 3.6.1-7
- Fix C compatibility issues

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Feb 02 2021 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 3.6.1-1
- Build for latest 3.6.1 release

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Oct 16 2020 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 3.5.1-1
- Build for latest release 3.5.1

* Fri Jul 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 3.4.0-1
- Build for latest release 3.4.0

* Mon May 18 2020 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 3.3.0-1
- Build for latest release 3.3.0

* Sat May 09 2020 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 3.2.0-2
- undo the change 'Rename makeotfexe to makeotf'

* Fri Apr 3 2020 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 3.2.0-1
- Build for latest release

* Mon Mar 23 2020 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 3.0.1-4
- rename package name afdko to adobe-afdko

* Mon Mar 9 2020 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 3.0.1-3
- Added %%set_build_flags
- Updated install script

* Mon Mar 2 2020 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 3.0.1-2
- Added build dependency gcc, make
- Removed unused build dependency
- Rename makeotfexe to makeotf

* Fri Dec 13 2019 Peng Wu <pwu@redhat.com> - 3.0.1-1
- Initial Version
