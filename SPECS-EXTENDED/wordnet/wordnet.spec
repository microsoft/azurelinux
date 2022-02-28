Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           wordnet
Version:        3.0
Release:        38%{?dist}
Summary:        A lexical database for the English language

License:        MIT and GPLv2+
URL:            http://wordnet.princeton.edu/
Source0:        http://wordnetcode.princeton.edu/%{version}/WordNet-%{version}.tar.bz2
# Updated database
Source1:        http://wordnetcode.princeton.edu/wn3.1.dict.tar.gz
Patch0:         wordnet-3.0-CVE-2008-2149.patch
Patch1:         wordnet-3.0-CVE-2008-3908.patch
Patch2:         wordnet-3.0-fix_man.patch
Patch3:         wordnet-3.0-fix_resourcedir_path.patch
Patch4:         wordnet-3.0-src_stubs_c.patch
# wordnet-3.0-wishwn_manpage.patch is GPLv2+
Patch5:         wordnet-3.0-wishwn_manpage.patch
Patch6:         wordnet-3.0-use_system_tk_headers.patch
Patch7:         wordnet-3.0-libtool.patch
# Bug #585206
Patch8:         wordnet-3.0-error_message.patch
# Bug #1037386
Patch9:         wordnet-3.0-Pass-compilation-with-Werror-format-security.patch
BuildRequires:  automake >= 1.8
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  gzip
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  tar
BuildRequires:  tcl-devel
BuildRequires:  tk-devel

%description
WordNet is a large lexical database of English, developed under the direction
of George A. Miller. Nouns, verbs, adjectives and adverbs are grouped into sets
of cognitive synonyms (synsets), each expressing a distinct concept. Synsets
are interlinked by means of conceptual-semantic and lexical relations. The
resulting network of meaningfully related words and concepts can be navigated
with the browser. WordNet is also freely and publicly available for download.
WordNet's structure makes it a useful tool for computational linguistics and
natural language processing.


%package browser
Summary:    Tk browser for WordNet
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   font(:lang=en)

%description browser
This package contains graphical browser for WordNet database.


%package devel
Summary:    The development libraries and header files for WordNet
Requires:   %{name} = %{version}-%{release}

%description devel
This package contains the libraries and header files required to create
applications based on WordNet.


%package doc
Summary:    Manual pages for WordNet in alternative formats
BuildArch:  noarch

%description doc
This package contains manual pages for WordNet package in HTML, PDF,
and PostScript format.


%prep
%setup -q -n WordNet-%{version}
%patch0 -p1 -b .cve-2008-2149
%patch1 -p1 -b .cve-2008-3908
%patch2 -p1 -b .fix_man
%patch3 -p1 -b .fix_resourcedir_path
%patch4 -p1 -b .src_stubs_c
%patch5 -p1 -b .wishwn_manpage
sed -e '/man_MANS/ s/$/ wishwn.1/' -i doc/man/Makefile.am
%patch6 -p1 -b .use_system_tk_headers
%patch7 -p1 -b .libtool
%patch8 -p1 -b .error_message
%patch9 -p1 -b .format
# delete the include/tk dir, since we do not use the included tk headers
rm -rf include/tk
# Update a database
tar -xozf %{SOURCE1}
# Remove database byproducts brought by the database update
rm -rf dict/dbfiles


%build
libtoolize && aclocal
autoupdate
autoreconf -i

export CFLAGS="%{?optflags} -DUSE_INTERP_RESULT"
export CXXFLAGS="%{?optflags} -DUSE_INTERP_RESULT"

%configure --enable-static=no --prefix=%{_datadir}/wordnet-%{version}/
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
# delete the libWN.la files (reasoning in the packaging guidelines)
rm -f  $RPM_BUILD_ROOT%{_libdir}/libWN.la
# Remove duplicate copies of docs installed by make install
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/doc
# Remove useless Makefiles installed by %%doc
rm -rf doc/{html,ps,pdf}/Makefile*


%ldconfig_scriptlets

%files
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/wn
%{_mandir}/man1/grind.1.gz
%{_mandir}/man1/wn.1.gz
%{_mandir}/man1/wnintro.1.gz
%{_mandir}/man5/*.5.gz
%{_mandir}/man7/*.7.gz
%{_datadir}/%{name}-%{version}/
%exclude %{_datadir}/%{name}-%{version}/lib/wnres/
%{_libdir}/libWN.so.*

%files browser
%{_bindir}/wishwn
%{_bindir}/wnb
%{_mandir}/man1/wishwn.1.gz
%{_mandir}/man1/wnb.1.gz
%{_datadir}/%{name}-%{version}/lib/wnres/

%files devel
%{_mandir}/man3/*.3.gz
%{_includedir}/wn.h
%{_libdir}/libWN.so

%files doc
%doc COPYING doc/{html,ps,pdf}


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0-38
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 23 2018 Petr Pisar <ppisar@redhat.com> - 3.0-33
- Modernize spec file
- Update database to version 3.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Merlin Mathesius <mmathesi@redhat.com> - 3.0-31
- Cleanup spec file conditionals

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 31 2014 Björn Esser <bjoern.esser@gmail.com> - 3.0-23
- fix build with tcl-8.6 (#1102111)
- append `-DUSE_INTERP_RESULT` to C[XX]FLAGS on Fedora >= 21

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0-22
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Wed Dec 04 2013 Petr Pisar <ppisar@redhat.com> - 3.0-21
- Pass compilation with -Werror=format-security (bug #1037386)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep 06 2012 Petr Pisar <ppisar@redhat.com> - 3.0-18
- wnb requires a font to start
- Move Tk browser to sub-package wordnet-browser
- Move alternative manual pages to wordnet-doc package
- Do not package INSTALL instructions and correct URL
- Modernize spec file

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 29 2010 Petr Pisar <ppisar@redhat.com> - 3.0-14
- Remove Makefiles from documentation clashing in multiarch installation
  (#658118).

* Fri Apr 30 2010 Petr Pisar <ppisar@redhat.com> - 3.0-13
- Add GPLv2+ license tag because wishwn(1) manual page is GPLv2+-licensed.

* Wed Apr 28 2010 Petr Pisar <ppisar@redhat.com> - 3.0-12
- Devel subpackages requires tcl-devel and tk-devel.
- Install wishwn(1) manual page

* Mon Apr 26 2010 Petr Pisar <ppisar@redhat.com> - 3.0-11
- Fix error message printing (#585206)
- Fix Source0 URL and Summary typo
- Remove libX11-devel and libXft-devel BuildRequires as they are inherited
  from tk-devel. Keep tcl-devel as tcl.h is included directly.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Caolan McNamara <caolanm@redhat.com> - 3.0-9
- Fixed fedora BZ 504957 - references to non-existing dirs in wnb

* Wed May 27 2009 Steven Fernandez <steve@lonetwin.net> - 3.0-8
- Fixed issues with the doc files duplication and ownership

* Wed May 27 2009 Steven Fernandez <steve@lonetwin.net> - 3.0-7
- Modified the %%files sections for both packages to only include the link in
  the devel package and the .so in the main package.
- Added %%pre and %%post sections

* Wed May 27 2009 Steven Fernandez <steve@lonetwin.net> - 3.0-6
- Added commands to build only shared libs and remove libtool's .la files
  before packaging

* Tue May 19 2009 Steven Fernandez <steve@lonetwin.net> - 3.0-5
- Added the libtool patch to build libWN.so dynamic lib

* Wed Feb 18 2009 Steven Fernandez <steve@lonetwin.net> - 3.0-4
- Added Tom 'spot' Callaway's patch to not include the tk.h and tkDecls.h from
  the upstream source, but instead rely on system tk headers

* Sun Jan 18 2009 Steven Fernandez <steve@lonetwin.net> - 3.0-3
- renamed rpm from WordNet to wordnet to be more consistent with other distos
- split the devel package
- borrowed more patches from the debian package

* Tue Jan 13 2009 Steven Fernandez <steve@lonetwin.net> - 3.0-2
- patch to fix CVE-2008-3908
- Added the wishwn man page from the debian wordnet package

* Sat Nov 29 2008 Steven Fernandez <steve@lonetwin.net> - 3.0-1
- First build for Fedora 10

