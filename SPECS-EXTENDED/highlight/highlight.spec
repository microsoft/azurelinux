Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           highlight
Summary:        Universal source code to formatted text converter
Version:        3.54
Release:        3%{?dist}
License:        GPLv3
URL:            https://www.andre-simon.de/
Source0:        https://www.andre-simon.de/zip/%{name}-%{version}.tar.bz2
BuildRequires:  gcc-c++
BuildRequires:  qt5-qtbase-devel
BuildRequires:  lua-devel, boost-devel
BuildRequires:  desktop-file-utils

%{?filter_setup:
%filter_from_provides /^perl(/d;
%filter_from_requires /^perl(/d;
%filter_from_requires /^\/bin\/lua/d;
%filter_setup
}

%description
A utility that converts sourcecode to HTML, XHTML, RTF, LaTeX, TeX,
XSL-FO, XML or ANSI escape sequences with syntax highlighting.
It supports several programming and markup languages.
Language descriptions are configurable and support regular expressions.
The utility offers indentation and reformatting capabilities.
It is easily possible to create new language definitions and colour themes.

%package gui
Summary:        GUI for the hihghlight source code formatter
Requires:       %{name} = %{version}-%{release}

%description gui
A Qt-based GUI for the highlight source code formatter source.

%prep
%autosetup

%build
CFLAGS="$CFLAGS -fPIC %{optflags}"; export CFLAGS
CXXFLAGS="$CXXFLAGS -fPIC %{optflags}"; export CXXFLAGS
LDFLAGS="$LDFLAGS %{?__global_ldflags}"; export LDFLAGS

# disabled paralell builds to fix FTBFS on rawhide & highlight 3.52+
#make_build all gui           CFLAGS="${CFLAGS}"          \
      make all gui            CFLAGS="${CFLAGS}"          \
                              CXXFLAGS="${CXXFLAGS}"      \
                              LDFLAGS="${LDFLAGS}"        \
                              LFLAGS="-Wl,-O1 ${LDFLAGS}" \
                              PREFIX="%{_prefix}"         \
                              conf_dir="%{_sysconfdir}/highlight/" \
                              QMAKE="%{_qt5_qmake}"       \
                              QMAKE_STRIP=

%install
%make_install PREFIX="%{_prefix}" conf_dir="%{_sysconfdir}/highlight/"

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
make install-gui DESTDIR=$RPM_BUILD_ROOT PREFIX="%{_prefix}" conf_dir="%{_sysconfdir}/highlight/"

rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}/

desktop-file-install \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications \
   highlight.desktop

%files
%{_bindir}/highlight
%{_datadir}/highlight/
%{_mandir}/man1/highlight.1*
%{_mandir}/man5/filetypes.conf.5*
%config(noreplace) %{_sysconfdir}/highlight/

%doc ChangeLog* AUTHORS README* extras/
%license COPYING

%files gui
%{_bindir}/highlight-gui
%{_datadir}/applications/highlight.desktop
%{_datadir}/pixmaps/highlight.xpm


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.54-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Filipe Rosset <rosset.filipe@gmail.com> - 3.54-1
- Update to 3.54

* Mon Aug 05 2019 Filipe Rosset <rosset.filipe@gmail.com> - 3.53-1
- Update to 3.53

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.52-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jul 13 2019 Filipe Rosset <rosset.filipe@gmail.com> - 3.52-2
- Disable paralell builds to fix build failures
- Make it possible to build with different prefix (rpm2flatpak) thanks to Milan Crha
- Fixed rhbz#1728753 and rhbz#1729455

* Sat Jun 15 2019 Filipe Rosset <rosset.filipe@gmail.com> - 3.52-1
- Updated to new 3.52 upstream version

* Sun Mar 31 2019 Filipe Rosset <rosset.filipe@gmail.com> - 3.50-1
- Updated to new 3.50 upstream version

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 18 2018 Filipe Rosset <rosset.filipe@gmail.com> - 3.48-1
- Updated to new 3.48 upstream version, remove upstreamed patch

* Tue Dec 11 2018 Filipe Rosset <rosset.filipe@gmail.com> - 3.47-2
- rebuilt to fix --list-scripts=langs crash fixes rhbz #1656332

* Fri Oct 26 2018 Filipe Rosset <rosset.filipe@gmail.com> - 3.47-1
- Updated to new 3.47 upstream version
- spec cleanup (remove old unused comments)
- Fixes rhbz #1611359 and #1630845 thanks to Milan Crha for all bug reports

* Thu Sep 20 2018 Filipe Rosset <rosset.filipe@gmail.com> - 3.44-2
- attempt to fix and respect build flags rhbz #1563149

* Sat Sep 15 2018 Filipe Rosset <rosset.filipe@gmail.com> - 3.44-1
- Updated to new 3.44 upstream version

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.42-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 09 2018 Filipe Rosset <rosset.filipe@gmail.com> - 3.42-2
- added gcc-c++ as BR

* Thu Mar 29 2018 Filipe Rosset <rosset.filipe@gmail.com> - 3.42-1
- Updated to new 3.42 upstream version

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.39-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.39-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 3.39-2
- Work around RPM bug re: dependency extraction from examples (#1476594)

* Thu Jul 27 2017 Filipe Rosset <rosset.filipe@gmail.com> - 3.39-1
- Updated to new 3.39 upstream version

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.36-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 3.36-2
- Rebuild due to bug in RPM (RHBZ #1468476)

* Fri Apr 14 2017 Filipe Rosset <rosset.filipe@gmail.com> - 3.36-1
- Updated to new 3.36 upstream version

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.33-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 3.33-3
- Rebuilt for Boost 1.63

* Sun Nov 06 2016 Filipe Rosset <rosset.filipe@gmail.com> - 3.33-2
- Updated to new 3.33 upstream version

* Wed Sep 14 2016 Filipe Rosset <rosset.filipe@gmail.com> - 3.31-1
- Updated to new 3.31 upstream version, fixes rhbz #1307617

* Mon Jul 04 2016 Filipe Rosset <rosset.filipe@gmail.com> - 3.30-1
- Updated to new 3.30 upstream version, fixes rhbz #1307617

* Sat May 21 2016 Filipe Rosset <rosset.filipe@gmail.com> - 3.28-3
- Disable paralell builds, atempt to fixes FTBFS rhbz #1307617

* Wed May 18 2016 Filipe Rosset <rosset.filipe@gmail.com> - 3.28-2
- Updated to new 3.28 upstream version
- Build against qt5 instead of qt4
- Attempt to fixes rhbz #1307617

* Wed May 18 2016 Filipe Rosset <rosset.filipe@gmail.com> - 3.28-1
- Updated to new 3.28 upstream version
- Build against qt5 instead of qt4
- Fixes rhbz #1307617

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.22-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb 01 2016 Rex Dieter <rdieter@fedoraproject.org> 3.22-7
- ensure proper link flags (for hardening)

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 3.22-6
- Rebuilt for Boost 1.60

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 3.22-5
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.22-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 3.22-3
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 29 2015 Jochen Schmitt <Jochen herr-schmitt de> - 3.22-1
- New upstream release

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.21-2
- Rebuilt for GCC 5 C++11 ABI change

* Mon Feb  2 2015 Jochen Schmitt <Jochen herr-schmitt de> - 3.21-1
- New upstream release with support for lua-5.3

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 3.20-2
- Rebuild for boost 1.57.0

* Wed Jan 21 2015 Jochen Schmitt <Jochen herr-schmitt de> - 3.20-1
- New upstream release

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 3.18-2
- Rebuild for boost 1.55.0

* Thu May  1 2014 Jochen Schmitt <Jochen herr-schmitt de> - 3.18-1
- New upstream release

* Tue Nov 26 2013 Jochen Schmitt <Jochen herr-schmitt de> - 3.16.1-2
- Use of correct tar ball should fix BZ #10341741)

* Fri Nov  1 2013 Jochen Schmitt <Jochen herr-schmitt de> - 3.16.1-1
- Minor bug fix release from upstream

* Sun Oct 13 2013 Jochen Schmitt <Jochen herr-schmitt de> - 3.16-1
- New upstream release

* Wed Aug 21 2013 Jochen Schmitt <Jochen herr-schmitt de> - 3.15-1
- New upstream release
- Fix FTBFS due changed lua API (#991892)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 3.13-2
- Rebuild for boost 1.54.0

* Tue Feb 19 2013 Jochen Schmitt <Jochen herr-schmitt de> - 3.13-1
- New upstream release
- Clean up sPEC file

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Oct  7 2012 Jochen Schmitt <Jochen herr-schmitt de> - 3.12-1
- New upstream release

* Thu Sep  6 2012 Jochen Schmitt <Jochen herr-schmitt de> - 3.11-0.1
- New upstream release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 24 2012 Jochen Schmitt <Jochen herr-schmitt de> 3.9-1
- New upstream release

* Thu Mar  8 2012 Jochen Schmitt <Jochen herr-schmitt de> 3.8-1
- New upstream release

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7-2
- Rebuilt for c++ ABI breakage

* Mon Jan 16 2012 Jochen Schmitt <Jochen herr-schmitt de> 3.7-1
- New upstream release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 16 2011 Jochen Schmitt <Jochen herr-schmitt de> 3.6-1
- New upstream release

* Wed Jun  8 2011 Jochen Schmitt <Jochen herr-schmitt de> 3.5-1
- New upstream release

* Thu Mar 31 2011 Jochen Schmitt <Jochen herr-schmitt de> 3.4-1
- New upstream release

* Sun Mar 20 2011 Jochen Schmitt <Jochen herr-schmitt de> 3.3-5
- Migrating Req./Prov. filterering to filter rpm macros

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 30 2010 Jochen Schmitt <Jochen herr-schmitt de> 3.3-1
- New upstream release

* Tue Nov 16 2010 Jochen Schmitt <Jochen herr-schmitt de> 3.2-1
- New upstream release

* Tue Sep  7 2010 Jochen Schmitt <Jochen herr-schmitt de> 3.1-2
- Add epoche for qt-devel BR (#631442)

* Mon Aug 30 2010 Jochen Schmitt <Jochen herr-schmitt de> 3.1-1
- New upstream release

* Sun Aug 15 2010 Jochen Schmitt <Jochen herr-schmitt de> 3.1-0.3
- New upstream release

* Thu Jul 15 2010 Jochen Schmitt <Jochen herr-schmitt de> 3.1-0.2
- New upstream release

* Sat Jun 26 2010 Jochen Schmitt <Jochen herr-schmitt de> 3.1-0.1
- New upstream release

* Sat Jun 12 2010 Jochen Schmitt <Jochen herr-schmitt de> 3.0-0.2
- Exclude all perl related req. caused by the examples

* Thu Jun 10 2010 Jochen Schmitt <Jochen herr-schmitt de> 3.0-0.1
- New upstream release (beta)

* Mon Apr  5 2010 Jochen Schmitt <Jochen herr-schmitt de> 2.16-1
- New upstream release

* Sun Mar 14 2010 Jochen Schmitt <Jochen herr-schmitt de> 2.15-2
- Add StartupNotify=true into desktop file

* Mon Mar  1 2010 Jochen Schmitt <Jochen herr-schmitt de> 2.15-1
- New upstream release

* Thu Jan 28 2010 Jochen Schmitt <Jochen herr-schmitt de> 2.14-1
- New upstream release

* Wed Oct 14 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.13-1
- New upstream release

* Thu Sep 10 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.12-1
- New upstream release

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> 2.10-4
- Use bzipped upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.10-2
- License was changed go GPLv3 from upstream

* Mon Jun 29 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.10-1
- New upstream release

* Tue May 12 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.9-1
- New upstream release

* Mon Apr 20 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.8-3
- Adding GUI subpackage

* Mon Apr 20 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.8-1
- New upstream release

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb  3 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.7-2
- Patches for gcc-4.4

* Thu Jan 15 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.7-1
- New upstream release

* Mon Nov  3 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.6.14-1
- New upstream release

* Tue Oct 14 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.6.13-2
- Fix SMP build issue

* Wed Oct  8 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.6.13-1
- New upstream release

* Thu Sep 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.12-2
- don't package broken examples, causes bogus perl provides/requires
- don't claim to Provide: perl(highlight_pipe)
- don't claim to Requires: perl(IPC::Open3)

* Mon Aug 18 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.6.12-1
- New upstream release
- Fix for gcc-4.3 issue on highlight-2.6.13

* Thu Jul 17 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.6.11-1
- New upstream release

* Mon May 12 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.6.10-1
- New upstream release

* Mon Mar 31 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.6.9-2
- New upstream release

* Sun Feb 10 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.6.8-1
- New upstream release

* Mon Jan 21 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.6.7-2
- New upstream release
- Fix gcc-4.3 issues

* Tue Dec 11 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.6.6-1
- New upstream release

* Mon Oct 29 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.6.5-1
- New upstream release

* Sun Sep 16 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.6.4-1
- New upstream release

* Tue Sep 11 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.6.3-1
- New upstream release

* Thu Aug  9 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.6.2-1
- New upstream release

* Wed Aug  8 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.6.1-2
- Changing license tag

* Tue Jul 10 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.6.1-1
- New upstream release

* Tue Feb  6 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.4.8-2
- fir rpmopt bug (#227292)

* Mon Oct 23 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.4.8-1
- New upstream release

* Sun Sep  3 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.4.7-2
- Rebuilt for FC-6

* Tue Jul  4 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.4.7-1
- New upstream release

* Wed Mar 22 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.4.5-2
- New upstream relase
- Add gcc41 patch

* Wed Mar 15 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.4.4-2
- Add fixcodegen patch from Eric Hopper #184245

* Sun Mar 12 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.4.4-1
- New upstream release
- Adapt rpmopt patch to new upstream release

* Sun Feb 12 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.4.3-2
- Rebuilt for FC5

* Tue Nov  1 2005 Jochen Schmitt <Jochen herr-schmitt de> 2.4.3-1
- New upstream release

* Tue Oct 11 2005 Jochen Schmitt <Jochen herr-schmitt de> 2.4.2-3
- Fix typo in highlight-2.4-rpmoptflags.patch

* Mon Oct 10 2005 Jochen Schmitt <Jochen herr-schmitt de> 2.4.2-2
- Use -DUSE_FN_MATCH

* Sun Oct  9 2005 Jochen Schmitt <Jochen herr-schmitt de> 2.4.2-1
- New upstream release

* Wed Aug 10 2005 Jochen Schmitt <Jochen herr-schmitt de> 2.4.1-6
- Rebuilt for FC-4/FC-3

* Tue Aug  9 2005 Jochen Schmitt <Jochen herr-schmitt de> 2.4-1-5
- Fix #165302

* Mon Aug  8 2005 Jochen Schmitt <Jochen herr-schmitt de> 2.4.1-4
- Move extension.conf and scriptre.conf to /etc/highlight

* Wed Aug  3 2005 Jochen Schmitt <Jochen herr-schmitt de> 2.4.1-3
- Remove leading 'A' from summary line

* Wed Aug  3 2005 Jochen Schmitt <Jochen herr-schmitt de> 2.4.1-2
- Add rpmoptflags patch from Tom Callaway

* Wed Aug  3 2005 Jochen Schmitt <Jochen herr-schmitt de> 2.4.1-1
- Change versioning schema
- Add suggested changes from Oliver

* Sun Jul 24 2005 Jochen Schmitt <Jochen herr-schmitt de> 2.4-1
- Initial build

