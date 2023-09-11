# Doxygen HTML help is not suitable for packaging due to a minified JavaScript
# bundle inserted by Doxygen itself. See discussion at
# https://bugzilla.redhat.com/show_bug.cgi?id=2006555.
#
# We can enable the Doxygen PDF documentation as a substitute.
%global so_version 1
%bcond_with doc_pdf
%bcond_without autoreconf
Summary:        Library to extract data from within an Excel spreadsheet
Name:           freexl
Version:        1.0.6
Release:        19%{?dist}
# The entire source is triply-licensed as (MPL-1.1 OR GPL-2.0-or-later OR
# LGPL-2.1-or-later), except for some build-system files that do not contribute
# to the license of the binary RPMs:
#   - aclocal.m4, m4/ltoptions.m4, m4/ltsugar.m4, m4/ltversion.m4, and
#     m4/lt~obsolete.m4 are FSFULLR
#   - compile, config.guess, config.sub, depcomp, ltmain.sh, missing, and
#     test-driver are GPL-2.0-or-later
#   - configure is FSFUL, or, more likely,
#     (FSFUL AND (MPL-1.1 OR GPL-2.0-or-later OR LGPL-2.1-or-later))
#   - install-sh is X11
#   - m4/libtool.m4 is (FSFULLR AND GPL-2.0-or-later)
License:        MPL-1.1 OR GPL-2.0-or-later OR LGPL-2.1-or-later
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.gaia-gis.it/FreeXL
Source0:        https://www.gaia-gis.it/gaia-sins/freexl-sources/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
%if %{with autoreconf}
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
%endif

%description
FreeXL is a library to extract valid data from within spreadsheets.

Design goals:
  • to be simple and lightweight
  • to be stable, robust and efficient
  • to be easily and universally portable
  • completely ignoring any GUI-related oddity

%package doc
Summary:        Documentation and examples for FreeXL
BuildArch:      noarch
%if %{with doc_pdf}
BuildRequires:  doxygen
BuildRequires:  doxygen-latex
%endif

%description doc
%{summary}.

%package devel
Summary:        Development Libraries for FreeXL
Requires:       freexl%{?_isa} = %{version}-%{release}

%description devel
The freexl-devel package contains libraries and header files for
developing applications that use freexl.

%prep
%autosetup

# We want to install a “clean” version of the examples
mkdir -p clean
cp -rp examples clean/
# Automake files don’t work without a configure.ac; don’t bother installing
# them.
rm -vf clean/examples/Makefile.*

%if %{with doc_pdf}
# We enable the Doxygen PDF documentation as a substitute. We must enable
# GENERATE_LATEX and LATEX_BATCHMODE; the rest are precautionary and should
# already be set as we like them. We also disable GENERATE_HTML, since we will
# not use it.
sed -r -i \
    -e "s/^([[:blank:]]*(GENERATE_LATEX|LATEX_BATCHMODE|USE_PDFLATEX|\
PDF_HYPERLINKS)[[:blank:]]*=[[:blank:]]*)NO[[:blank:]]*/\1YES/" \
    -e "s/^([[:blank:]]*(LATEX_TIMESTAMP|GENERATE_HTML)\
[[:blank:]]*=[[:blank:]]*)YES[[:blank:]]*/\1NO/" \
    Doxyfile.in
%endif


%build
%if %{with autoreconf}
autoreconf --force --install --verbose
%endif
%configure --disable-static
%make_build

%if %{with doc_pdf}
doxygen Doxyfile
%make_build -C latex
mv latex/refman.pdf latex/FreeXL.pdf
%endif


%check
%make_build check


%install
%make_install
# Delete undesired libtool archives
find '%{buildroot}' -type f -name '*.la' -print -delete


%files
%license COPYING
%{_libdir}/libfreexl.so.%{so_version}
%{_libdir}/libfreexl.so.%{so_version}.*

%files devel
%{_includedir}/freexl.h
%{_libdir}/libfreexl.so
%{_libdir}/pkgconfig/freexl.pc

%files doc
%license COPYING
%doc AUTHORS
%doc README
%doc clean/examples
%if %{with doc_pdf}
%doc latex/FreeXL.pdf
%endif

%changelog
* Wed Aug 09 2023 Archana Choudhary <archana1@microsoft.com> - 1.0.6-19
- Initial CBL-Mariner import from Fedora 37 (license: MIT).
- Disable doc_pdf
- License verified

* Mon Aug 01 2022 Benjamin A. Beasley <code@musicinmybrain.net> 1.0.6-18
- Update License field to SPDX

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> 1.0.6-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> 1.0.6-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 16 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.0.6-4
- Modernize and clean up the spec file
- Make it harder to miss any .so version change
- Properly install the license file
- Remove an obsolete sed-patch
- Move documentation and examples to a -doc subpackage
- Build PDF instead of HTML documentation

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Aug 02 2020 Volker Fröhlich <volker27@gmx.at> - 1.0.6-1
- New upstream release

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 22 2018 Volker Fröhlich <volker27@gmx.at> - 1.0.5-1
- New upstream release

* Thu Feb 08 2018 Volker Fröhlich <volker27@gmx.at> - 1.0.4-3
- Remove Group keyword

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 08 2017 Volker Fröhlich <volker27@gmx.at> - 1.0.4-1
- New release

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 23 2017 Volker Fröhlich <volker27@gmx.at> 1.0.3-1
- New release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 28 2015 Volker Froehlich <volker27@gmx.at> - 1.0.2-2
- Release bump to work around the f23 build being wrongly tagged for f24

* Wed Jul 15 2015 Volker Fröhlich <volker27@gmx.at> 1.0.2-1
- New release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar 22 2015 Volker Fröhlich <volker27@gmx.at> 1.0.1-1
- New release

* Fri Mar  6 2015 Volker Fröhlich <volker27@gmx.at> 1.0.0i-1
- New release with security fixes

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0f-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0f-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Nov 30 2013 Volker Fröhlich <volker27@gmx.at> 1.0.0f-1
- Drop obsolete patch for aarch64

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0d-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr  2 2013 Volker Fröhlich <volker27@gmx.at> 1.0.0d-4
- Add patch for aarch64

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0d-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0d-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Volker Fröhlich <volker27@gmx.at> 1.0.0d-1
- New upstream bugfix release

* Fri Jan 13 2012 Volker Fröhlich <volker27@gmx.at> 1.0.0a-3
- Remove coverage tests and BR for lcov (fail in Rawhide)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jan 08 2012 Volker Fröhlich <volker27@gmx.at> 1.0.0a-1
- Correct versioning scheme to post-release
- Correct Source and setup macro accordingly

* Fri Nov 18 2011 Volker Fröhlich <volker27@gmx.at> 1.0.0-0.1.a
- Move development lib symlink to devel
- Don't build static lib
- Add README
- Build with enable-gcov
- BR lcov and doxygen
- Shorten description and summary
- Use macros in Source tag
- Add check section
- Change version and release
- Correct URL
- Correct to multiple licensing scenario
- Drop defattr
- Add pkgconfig and isa macro to devel's BR
- Use upstream tarball, as file size is different
- Remove EPEL 5 specific elements

* Fri Nov 26 2010 Peter Hopfgartber <peter.hopfgartner@r3-gis.com> 1.0.0a-0.1
- Initial packaging
