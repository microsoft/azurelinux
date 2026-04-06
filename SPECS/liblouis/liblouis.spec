# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           liblouis
Version:        3.33.0
Release:        6%{?dist}
Summary:        Braille translation and back-translation library

# LGPL-2.1-or-later: the project as a whole
# LGPL-2.0-or-later: parts of gnulib
# - gnulib/_Noreturn.h
# - gnulib/arg-nonnull.h
# - gnulib/c++defs.h
# - gnulib/warn-on-use.h
License:        LGPL-2.1-or-later AND LGPL-2.0-or-later
URL:            https://liblouis.io
Source0:        https://github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  hardlink
BuildRequires:  help2man
BuildRequires:  libyaml-devel
BuildRequires:  m4
BuildRequires:  make
BuildRequires:  texinfo
BuildRequires:  texinfo-tex
BuildRequires:  texlive-eurosym
BuildRequires:  texlive-xetex
BuildRequires:  python3-devel

Provides:       bundled(gnulib)

Requires:       %{name}-tables = %{version}-%{release}

%description
Liblouis is an open-source braille translator and back-translator named in
honor of Louis Braille. It features support for computer and literary braille,
supports contracted and uncontracted translation for many languages and has
support for hyphenation. New languages can easily be added through tables that
support a rule- or dictionary based approach. Liblouis also supports math
braille (Nemeth and Marburg).

Liblouis has features to support screen-reading programs. This has led to its
use in two open-source screen readers, NVDA and Orca. It is also used in some
commercial assistive technology applications for example by ViewPlus.

Liblouis is based on the translation routines in the BRLTTY screen reader for
Linux. It has, however, gone far beyond these routines.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
License:        LGPL-2.1-or-later

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        tables
Summary:        Data tables
# LGPL-2.1-or-later: most of the tables
# LGPL-3.0-or-later:
# - tables/Es-Es-G0.utb
# - tables/et-g0.utb
# - tables/is-chardefs6.cti
# - tables/is-chardefs8.cti
# - tables/pt-pt-g2.ctb
# - tables/sr-chardefs.cti
# - tables/sr-g1.ctb
License:        LGPL-2.1-or-later AND LGPL-3.0-or-later
BuildArch:      noarch

%description    tables
Data tables for liblouis, containing attributes and dot patterns.


%package        utils
Summary:        Command-line utilities to test %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
# GPL-3.0-or-later: the source code in tools
# LGPL-2.0-or-later AND LGPL-2.1-or-later: tools/gnulib
# LGPL-3.0-or-later: tools/gnulib/version-etc.{c,h}
# LGPL-3.0-or-later OR GPL-2.0-or-later:
# - tools/gnulib/unistr/u16-mbtoucr.c
# - tools/gnulib/unistr/u16-to-u8.c
License:        GPL-3.0-or-later AND LGPL-3.0-or-later AND LGPL-2.1-or-later AND LGPL-2.0-or-later AND (LGPL-3.0-or-later OR GPL-2.0-or-later)

%description    utils
Six test programs are provided as part of the liblouis package. They
are intended for testing liblouis and for debugging tables. None of
them is suitable for braille transcription.


%package -n python3-louis
Summary:        Python 3 language bindings for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
License:        LGPL-2.1-or-later

%description -n python3-louis
This package provides Python 3 language bindings for %{name}.


%package doc
Summary:        Documentation for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
# See doc/liblouis.texi
License:        LGPL-3.0-or-later

%description doc
This package provides the documentation for liblouis.


%prep
%autosetup
chmod 664 tables/*


%generate_buildrequires
cd python
%pyproject_buildrequires


%build
%configure --disable-static --enable-ucs4

# Get rid of undesirable hardcoded rpaths; workaround libtool reordering
# -Wl,--as-needed after all the libraries.
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|CC="\(.*g..\)"|CC="\1 -Wl,--as-needed"|' \
    -i libtool

# parallel builds fail
%if 0%{?rhel}
LD_LIBRARY_PATH=$PWD/liblouis/.libs \
%endif
make
cd doc; xetex %{name}.texi
cd ../python
%pyproject_wheel


%check
LD_LIBRARY_PATH=%{buildroot}%{_libdir} make check


%install
%make_install
rm -f %{buildroot}/%{_infodir}/dir
rm -f %{buildroot}/%{_libdir}/%{name}.la
rm -rf %{buildroot}/%{_bindir}/lou_maketable*
rm -rf %{buildroot}/%{_defaultdocdir}/%{name}/

# Install internal.h for MuseScore
install -pm 0644 liblouis/internal.h %{buildroot}%{_includedir}/%{name}

# Hardlink table files with identical content
hardlink -t %{buildroot}%{_datadir}/%{name}/tables/

cd python
%pyproject_install
%pyproject_save_files louis
cd -


%files
%doc README AUTHORS NEWS ChangeLog TODO
%license COPYING.LESSER
%{_libdir}/%{name}.so.*
%{_infodir}/%{name}.info*

%files devel
%doc HACKING
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/%{name}.so

%files tables
%{_datadir}/%{name}/

%files utils
%license COPYING
%{_bindir}/lou_*
%{_mandir}/man1/lou_*.1*

%files -n python3-louis -f %{pyproject_files}

%files doc
%doc doc/%{name}.{html,txt,pdf}


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.33.0-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.33.0-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.33.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 3.33.0-3
- Rebuilt for Python 3.14

* Fri May 23 2025 Martin Gieseking <martin.gieseking@uos.de> - 3.33.0-2
- Updated URL of upstream website.

* Sun May 18 2025 Martin Gieseking <martin.gieseking@uos.de> - 3.33.0-1
- Update to 3.33.0
- Added missing BR m4

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.28.0-6
- Rebuilt for Python 3.13

* Mon Feb 12 2024 Jerry James <loganjerry@gmail.com> - 3.28.0-5
- Hardlink, rather than symlink, duplicate table files

* Mon Feb 12 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 3.28.0-4
- Fix RHEL build after RPATH removal

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan  3 2024 Jerry James <loganjerry@gmail.com> - 3.28.0-1
- Update to 3.28.0
- Install internal.h for MuseScore
- Drop ancient obsoletes
- Build the python package with dist-info
- Add tables subpackage for the noarch data
- Complete and correct SPDX migration
- Remove need for chrpath
- Minor spec file cleanups

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.25.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 3.25.0-2
- Rebuilt for Python 3.12

* Tue Mar 07 2023 Martin Gieseking <martin.gieseking@uos.de> - 3.25.0-1
- Update to 3.25.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.24.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 06 2022 Martin Gieseking <martin.gieseking@uos.de> - 3.24.0-1
- Update to 3.24.0

* Mon Sep 12 2022 Martin Gieseking <martin.gieseking@uos.de> - 3.23.0-1
- Update to 3.23.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.22.0-2
- Rebuilt for Python 3.11

* Thu Jun 09 2022 Martin Gieseking <martin.gieseking@uos.de> - 3.22.0-1
- Update to 3.22.0

* Wed Mar 09 2022 Martin Gieseking <martin.gieseking@uos.de> - 3.21.0-1
- Update to 3.21.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.20.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 20 2021 Martin Gieseking <martin.gieseking@uos.de> - 3.20.0-1
- Update to 3.20.0

* Thu Sep 16 2021 Martin Gieseking <martin.gieseking@uos.de> - 3.19.0-1
- Update to 3.19.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 09 2021 Martin Gieseking <martin.gieseking@uos.de> - 3.18.0-1
- Update to 3.18.0

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.17.0-2
- Rebuilt for Python 3.10

* Thu Mar 11 2021 Martin Gieseking <martin.gieseking@uos.de> - 3.17.0-1
- Update to 3.17.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 02 2020 Martin Gieseking <martin.gieseking@uos.de> - 3.16.1-1
- Update to 3.16.1

* Tue Dec 01 2020 Martin Gieseking <martin.gieseking@uos.de> - 3.16.0-1
- Update to 3.16.0

* Mon Sep 07 2020 Martin Gieseking <martin.gieseking@uos.de> - 3.15.0-2
- Use make_install macro.

* Tue Sep 01 2020 Martin Gieseking <martin.gieseking@uos.de> - 3.15.0-1
- Updated to 3.15.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.12.0-3
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Martin Gieseking <martin.gieseking@uos.de> - 3.12.0-1
- Updated to 3.12.0.
- Dropped date from Provides(gnulib).

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.10.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.10.0-3
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 03 2019 Martin Gieseking <martin.gieseking@uos.de> - 3.10.0-1
- Updated to 3.10.0.
- Use %%license tag to add the file containing the license text.

* Mon Mar 04 2019 Martin Gieseking <martin.gieseking@uos.de> - 3.9.0-1
- Updated to 3.9.0.
- Dropped GCC 9 related patch since changes have been applied upstream.

* Fri Feb 08 2019 Martin Gieseking <martin.gieseking@uos.de> - 3.8.0-3
- Fixed memory issue introduced with GCC 9 (changed semantics of block scope compound literals).

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 10 2018 Martin Gieseking <martin.gieseking@uos.de> - 3.8.0-1
- Updated to 3.8.0

* Sat Oct 13 2018 Martin Gieseking <martin.gieseking@uos.de> - 3.7.0-2
- Dropped Python 2 language bindings according to
  https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal
- Dropped Python dependency from utils package because it doesn't contain Python scripts any longer
- Added BR:libyaml-devel to enable YAML support

* Wed Sep 26 2018 Martin Gieseking <martin.gieseking@uos.de> - 3.7.0-1
- Updated to 3.7.0, fixes CVE-2018-17294 (BZ #1632834).

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 3.6.0-4
- Rebuild with fixed binutils

* Sat Jul 28 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.6.0-3
- Replace obsolete scriptlets

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Martin Gieseking <martin.gieseking@uos.de> - 3.6.0-1
- Updated to 3.6.0.
- Added patch to fix CVE-2018-12085.
- Create liblouis.pdf with XeTeX rather than texi2pdf to prevent build errors.

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.6.2-16
- Rebuilt for Python 3.7

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.6.2-14
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sun Dec 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.6.2-13
- Python 2 binary package renamed to python2-louis
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Fri Nov 03 2017 Martin Gieseking <martin.gieseking@uos.de> - 2.6.2-12
- Applied security fixes from EL 7.4 (CVE-2014-8184, CVE-2017-13738, CVE-2017-13740, CVE-2017-13741, CVE-2017-13742, CVE-2017-13743, CVE-2017-13744)
- Dropped redundant parts of the spec file.
- Updated URL.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Feb 15 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.6.2-9
- Rebuild for brp-python-bytecompile

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.6.2-7
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.2-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sun Aug 23 2015 Kalev Lember <klember@redhat.com> - 2.6.2-3
- Rename liblouis-python3 to python3-louis, as per latest packaging guidelines
- Fix the build with texinfo 6.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 08 2015 Martin Gieseking <martin.gieseking@uos.de> 2.6.2-1
- Updated to new upstream release.

* Tue Sep 16 2014 Martin Gieseking <martin.gieseking@uos.de> 2.6.0-1
- Updated to new upstream release.

* Mon Aug 18 2014 Martin Gieseking <martin.gieseking@uos.de> 2.5.4-5
- Fixed check for ELF binaries to prevent chrpath from failing.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 2.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue May 13 2014 Martin Gieseking <martin.gieseking@uos.de> 2.5.4-1
- Updated to new upstream release.
- Activated the bundled test suite which has been adapted to work correctly with the recent release. 
- Remove Rpaths from the utility programs.
- Updated the description according to the upstream website.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Martin Gieseking <martin.gieseking@uos.de> - 2.5.3-1
- Update to new upstream release.

* Thu Jul 18 2013 Matthias Clasen <mclasen@redhat.com> - 2.5.2-7
- Tighten dependencies between subpackages (pointed out by rpmdiff)

* Tue Apr 16 2013 Martin Gieseking <martin.gieseking@uos.de> 2.5.2-6
- Restrict exclusion of Python 3 packages to RHEL <= 7.

* Mon Apr 15 2013 Martin Gieseking <martin.gieseking@uos.de> 2.5.2-5
- Restrict exclusion of Python 3 packages to RHEL < 7.

* Mon Apr 15 2013 Rui Matos <rmatos@redhat.com> - 2.5.2-4
- Don't depend on python3 in RHEL.

* Tue Feb 26 2013 Martin Gieseking <martin.gieseking@uos.de> 2.5.2-3
- Added Python 3 language bindings.

* Fri Feb 22 2013 Martin Gieseking <martin.gieseking@uos.de> 2.5.2-2
- Moved documentation to doc subpackage.

* Wed Feb 06 2013 Martin Gieseking <martin.gieseking@uos.de> 2.5.2-1
- Updated to new upstream release.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 10 2012 Martin Gieseking <martin.gieseking@uos.de> 2.4.1-1
- Updated to upstream release 2.4.1.
- Made the devel package's dependency on the base package arch specific.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 12 2011 Martin Gieseking <martin.gieseking@uos.de> 2.4.0-1
- Updated to upstream release 2.4.0.

* Fri May 20 2011 Martin Gieseking <martin.gieseking@uos.de> 2.3.0-1
- Updated to upstream release 2.3.0.

* Mon Feb 28 2011 Martin Gieseking <martin.gieseking@uos.de> - 2.2.0-2
- Added release date of bundled gnulib to Provides.
- Use %%{name} macro consistently.

* Tue Feb 15 2011 Martin Gieseking <martin.gieseking@uos.de> - 2.2.0-1
- Updated to upstream release 2.2.0.
- Added Python bindings.

* Mon Jul 5 2010 Lars Bjørndal <lars.bjorndal@broadpark.no> - 1.9.0-2
- In advice from Martin Gieseking: Removed some garbage from the file section, and added a PDF version of the liblouis documentation. See <https://bugzilla.redhat.com/show_bug.cgi?id=597597>.

* Wed Jun 30 2010 Lars Bjørndal <lars.bjorndal@broadpark.no> - 1.9.0-1
- A new version was up to day. At the same time, fixed a minor spec issue according to a comment from Martin Gieseking, see <https://bugzilla.redhat.com/show_bug.cgi?id=597597>.

* Sun Jun 20 2010 Lars Bjørndal <lars.bjorndal@broadpark.no> - 1.8.0-3
- Fixed some small problems, among them wrong destination directory for documentation. See <https://bugzilla.redhat.com/show_bug.cgi?id=597597> for further details.

* Thu Jun 17 2010 Lars Bjørndal <lars.bjorndal@broadpark.no> 1.8.0-2
- Created the tools sub package and did a lot of clean ups, see <https://bugzilla.redhat.com/show_bug.cgi?id=597597>.

* Sat May 29 2010 Lars Bjørndal <lars.bjorndal@broadpark.no> 1.8.0-1
- Create the RPM for Fedora.
