# Place rpm-macros into proper location.
%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; /bin/echo $d)
Summary:        Finds duplicate files in a given set of directories
Name:           fdupes
Version:        2.2.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/adrianlopezroche/%{name}
Source0:        https://github.com/adrianlopezroche/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1:        macros.%{name}
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  pcre2-devel

%description
FDUPES is a program for identifying duplicate files residing within specified
directories.

%prep
%autosetup -p 1

# From README.
cat << EOF > LICENSE
FDUPES Copyright (c) 1999-2019 Adrian Lopez

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
EOF

autoreconf -fiv


%build
%configure
%make_build


%install
%make_install
install -Dpm 0644 %{SOURCE1} %{buildroot}%{macrosdir}/macros.%{name}


%check
./%{name} testdir
./%{name} --omitfirst testdir
./%{name} --recurse testdir
./%{name} --size testdir


%files
%license CONTRIBUTORS LICENSE
%doc CHANGES README
%{_mandir}/man1/%{name}.1*
%{_mandir}/man7/%{name}*.7*
%{_bindir}/%{name}
%{macrosdir}/macros.fdupes

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.2.1-1
- Auto-upgrade to 2.2.1 - Azure Linux 3.0 - package upgrades

* Tue Jan 25 2022 Cameron Baird <cameronbaird@microsoft.com> - 2.1.2-1
- Update source to 2.1.2

* Thu Jun 10 2021 Henry Li <lihl@microsoft.com> - 2.1.1-3
- Initial CBL-Mariner import from Fedora 34 (license: MIT)
- License Verified
- Remove epoch field, which is not supported in CBL-Mariner

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Aug 13 2020 Richard Shaw <hobbes1069@gmail.com> - 1:2.1.1-1
- Update to 2.1.1.

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 02 2020 Richard Shaw <hobbes1069@gmail.com> - 1:2.1.0-1
- Update to 2.1.0.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 05 2020 Björn Esser <besser82@fedoraproject.org> - 1:2.0.0-1
- Update to 2.0.0 (#1787848)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Apr 09 2017 Björn Esser <besser82@fedoraproject.org> - 1:1.6.1-1
- Updated to new upstream-release
- Upstream changed versioning-scheme, Epoch is needed
- Drop old patches, applied upstream
- Update spec-file to recent guidelines
- Drop el5-bits

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.51-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.51-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Jon Schlueter <jschluet@redhat> - 1.51-10
- Rebaseline using github which is new home of fdupes
- source tarball has unusual folder naming of fdupes-fdupes-1.51 instead of normal fdupes-1.51

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.51-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.51-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.51-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 18 2014 Björn Esser <bjoern.esser@gmail.com> - 1.51-6
- remove duplicated `macros.d`-dir (#1088566)

* Tue Mar 18 2014 Björn Esser <bjoern.esser@gmail.com> - 1.51-5
- Add needed bits for el5
- Fix `mixed use of spaces-and tabs`
- Minor cleanup and improved readability

* Tue Mar 18 2014 Björn Esser <bjoern.esser@gmail.com> - 1.51-4
- Place rpm-macros into proper location using %%global macrosdir
- Apply proper LDFLAGS
- Fix offset in Patch1 and renamed it to match current version

* Sun Jan 19 2014 Ville Skyttä <ville.skytta@iki.fi> - 1.51-3
- Move macros to %%{_rpmconfigdir}/macros.d.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.51-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Richard Shaw <hobbes1069@gmail.com> - 1.51-1
- Update to latest upstream release.
- Fixes security bugs BZ#865591 & 865592.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.50-0.7.PR2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.50-0.6.PR2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Richard Shaw <hobbes1069@gmail.com> - 1.50-0.5.PR2
- Add RPM macro.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.50-0.4.PR2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.50-0.3.PR2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.50-0.2.PR2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Feb 01 2009 Debarshi Ray <rishi@fedoraproject.org> - 1.50-0.1.PR2
- Version bump to 1.50 PR2.
  * Added --noprompt, --recurse and --summarize options
  * Now sorts duplicates (old to new) for consistent order when listing or
    deleting duplicate files.
  * Now tests for early matching of files, which should help speed up the
    matching process when large files are involved.
  * Added warning whenever a file cannot be deleted.
  * Fixed bug where some files would not be closed after failure.
  * Fixed bug where confirmmatch() function wouldn't always deal properly with
    zero-length files.
  * Fixed bug where progress indicator would not be cleared when no files were
    found.
- Inclusion of string.h now added by upstream.
- Added patch to fix file comparisons from Debian. (Debian BTS #213385)
- Added patch to enable large file support on 32-bit systems from Debian.
  (Debian BTS #447601)
- Added patch to fix typo in the online manual page from Debian. (Debian BTS
  #353789)

* Tue Feb 19 2008 Release Engineering <rel-eng@fedoraproject.org> - 1.40-12
- Autorebuild for gcc-4.3.

* Thu Dec 27 2007 Debarshi Ray <rishi@fedoraproject.org> - 1.40-11
- Fixed Makefile to preserve timestamps using 'cp -p'.

* Thu Nov 29 2007 Debarshi Ray <rishi@fedoraproject.org> - 1.40-10
- Release bumped to overcome spurious build.

* Sun Nov 25 2007 Debarshi Ray <rishi@fedoraproject.org> - 1.40-9
- Initial build. Imported SPEC from Rawhide.
- Fixed Makefile to use DESTDIR correctly.
- Fixed sources to include string.h.
