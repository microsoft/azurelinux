Summary:        Voikko is a library for spellcheckers and hyphenators
Name:           libvoikko
Version:        4.3
Release:        1%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://voikko.puimula.org
# The usual format of stable release URLs
Source0:        http://www.puimula.org/voikko-sources/%{name}/%{name}-%{version}.tar.gz
# The usual format of test release URLs
#Source0:        http://www.puimula.org/htp/testing/%%{name}-%%{version}rc1.tar.gz
BuildRequires:  gcc-c++
BuildRequires:  python3-devel
# Require the Finnish morphology because Finnish is currently the only language
# supported by libvoikko in Fedora.
Requires:       malaga-suomi-voikko

%description
This is libvoikko, library for spellcheckers and hyphenators using Malaga
natural language grammar development tool. The library is written in C.

Currently only Finnish is supported, but the API of the library has been
designed to allow adding support for other languages later. Note however that
Malaga is rather low level tool that requires implementing the whole morphology
of a language as a left associative grammar. Therefore languages that have
simple or even moderately complex morphologies and do not require morphological
analysis in their hyphenators should be implemented using other tools such as
Hunspell.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkg-config

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n     voikko-tools
Summary:        Test tools for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n voikko-tools
This package contains voikkospell and voikkohyphenate, small command line
tools for testing libvoikko. These tools may also be useful for shell
scripts.

%package -n python3-libvoikko
%{?python_provide:%python_provide python3-libvoikko}
Summary:        Python interface to %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description -n python3-libvoikko
Python interface to libvoikko, library of Finnish language tools.
This module can be used to perform various natural language analysis
tasks on Finnish text.

%prep
%setup -q


%build
# The dictionary path must be the same where malaga-suomi-voikko is installed
# Use malaga for now, no hfst or vfst. We need to package foma for the vfst dictionaries.
%configure --with-dictionary-path=%{_libdir}/voikko --disable-hfst --disable-vfst --disable-buildtools --enable-malaga
# Remove rpath,
# https://fedoraproject.org/wiki/Packaging/Guidelines#Removing_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags} CXXFLAGS="$CXXFLAGS"


%install
make install INSTALL="install -p" DESTDIR=%{buildroot}
find %{buildroot} -type f -name "*.la" -delete -print
# Remove static archive
find %{buildroot} -name '*.a' -exec rm -f {} ';'
# Install the Python interface
install -d %{buildroot}%{python3_sitelib}
install -pm 0644 python/libvoikko.py %{buildroot}%{python3_sitelib}/

%ldconfig_scriptlets


%files
%license COPYING
%doc ChangeLog README
%{_libdir}/*.so.*

%files -n voikko-tools
%{_bindir}/voikkospell
%{_bindir}/voikkohyphenate
%{_bindir}/voikkogc
%{_mandir}/man1/voikkohyphenate.1.gz
%{_mandir}/man1/voikkospell.1.gz
%{_mandir}/man1/voikkogc.1.gz

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libvoikko.pc

%files -n python3-libvoikko
%{python3_sitelib}/%{name}.py*
%{python3_sitelib}/__pycache__/*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.3-1
- Auto-upgrade to 4.3 - Azure Linux 3.0 - package upgrades

* Fri Sep 16 2022 Osama Esmail <osamaesmail@microsoft.com> - 4.1.1-8
- Moved from SPECS-EXTENDED to SPECS
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.1.1-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 4.1.1-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 4.1.1-4
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Aug 3 2018 Ville-Pekka Vainio <vpvainio AT iki.fi> - 4.1.1-1
- New upstream release.
- Provide only python3-libvoikko, remove python2-libvoikko
- Use malaga for now, foma is not packaged for Fedora yet.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.8-10
- Rebuilt for Python 3.7

* Wed May 23 2018 Mike FABIAN <mfabian@redhat.com> - 3.8-9
- Add python3-devel to BuildRequires.
- Resolves: rhbz#1580782

* Thu Apr 19 2018 Mike FABIAN <mfabian@redhat.com> - 3.8-8
- Build Python 2 subpackage only for Fedora
- Resolves: rhbz#1566121

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.8-6
- Python 2 binary package renamed to python2-libvoikko
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jul 14 2016 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.8-1
- New upstream release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.7.1-2
- Rebuilt for GCC 5 C++11 ABI change

* Sat Oct 25 2014 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.7.1-1
- New upstream release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jan 26 2014 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.7-1
- New upstream release

* Fri Oct 18 2013 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.6.1-1
- New upstream release
- Remove voikkovfstc from the package, it is not built by default anymore
- Update upstream URLs

* Mon Jul 29 2013 Parag <paragn AT fedoraproject DOT org> - 3.6-2
- Ah don't add %%{?_isa} for noarch packages

* Mon Jul 29 2013 Parag <paragn AT fedoraproject DOT org> - 3.6-2
- Fix spec file to follow packaging guidelines

* Sun Apr 14 2013 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.6-1
- New upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 01 2012 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.5-1
- New upstream release

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.1-2
- Rebuilt for c++ ABI breakage

* Sat Feb 04 2012 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.4.1-1
- New upstream release, fixes build with GCC 4.7

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 27 2011 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.4-1
- Update to the latest upstream release:
- A crash bug affecting grammar checker has been fixed.
- New grammar checker rule for missing verbs has been added.

* Sun Sep 25 2011 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.3.1-0.3.rc1
- Remove the isa macro from the malaga-suomi-voikko dependency,
  malaga-suomi-voikko is not a library and is thus not multilib'd. The previous
  change was a misunderstanding.

* Sat Sep 24 2011 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.3.1-0.2.rc1
- Add the isa macro to the malaga-suomi-voikko dependency and drop the version.

* Sat Sep 24 2011 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.3.1-0.1.rc1
- New upstream release candidate, fixes a bug which crashed Firefox when
  using Finnish spell checking.

* Fri Sep 16 2011 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.3-1
- New upstream release

* Sun Jun 12 2011 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.2.1-1
- New upstream release
- Fixes handling of embedded null characters in input strings entered through
  Python or Java interfaces.

* Fri Mar 25 2011 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.2-1
- New upstream release

* Tue Feb 15 2011 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.1-3
- Add patch to fix build with GCC 4.6

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 22 2010 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.1-1
- New upstream release
- Remove the unneeded %%clean section, not needed in Fedora >= 13

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu May 27 2010 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.0-1
- 3.0 final

* Thu May 13 2010 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.0-0.1.rc1
- New upstream release candidate with multithread support
- Remove unneeded BuildRoot tag

* Thu Feb 18 2010 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.3.1-1
- Version 2.3.1 contains fixes for bugs found in version 2.3

* Sun Jan 31 2010 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.3-0.1.rc1
- New release candidate
- Dependency on glib has been removed

* Wed Nov 11 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.2.2-1
- Version 2.2.2 fixes a crash found in version 2.2.1 that can occur when the
  APIs that use wchar_t strings as arguments are used.

* Mon Oct 26 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.2.1-2
- Add Python interface (package python-libvoikko, noarch)

* Fri Oct 09 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.2.1-1
- New upstream release, fixes bugs found in 2.2

* Fri Sep 18 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.2-0.3.rc2
- 2.2rc2
- Remove getcwd() value check patch, accepted upstream

* Wed Sep 16 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.2-0.2.rc1
- Remove rpath which was set for the voikko-tools binaries in 64 bit
  architechtures

* Tue Sep 15 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.2-0.1.rc1
- New release candidate
- Improvements to spelling suggestions, grammar checker etc.
- Libvoikko now uses its own internal implementation of malaga.
- This prevents symbol conflicts such as https://bugzilla.redhat.com/502546
- BuildRequires malaga removed and glib2-devel added.
- Require malaga-suomi-voikko >= 1.4, libvoikko 2.2 expects the newer
  dictionary format
- Add a patch to make it compile on Fedora with -Werror

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 2 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.1-1
- 2.1 final, including fixes to grammar checking

* Fri Apr 17 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.1-0.5.rc4
- 2.1rc4:
  - Fix invalid use of delete vs. delete[]
  - Limit the scope of some variables

* Mon Apr 13 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.1-0.4.rc3
- 2.1rc3, remove patch

* Sat Apr 11 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.1-0.3.rc2
- Patch to current SVN HEAD, includes a fix for a memory leak in the grammar
  checker

* Mon Apr 6 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.1-0.2.rc2
- New release candidate
- Both patches applied upstream

* Mon Apr 6 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.1-0.1.rc1
- New release candidate
- Improvements on grammar checking and dictionary loading
- Raise malaga-suomi-voikko dependency to 1.3-10, which has the new dictionary
  data directory layout needed by this version of libvoikko
- Add BuildRequires python for running the trie compiler during build
- Add patch for GCC 4.4 and glibc 2.90 compliance
- Add patch to fix warn_unused_result errors

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug 28 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.0-1
- libvoikko 2.0

* Sat Aug 23 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.0-0.1.rc1
- New release candidate, including the new voikkogc tool in voikko-tools
- Add defattr to voikko-tools
- Drop upstreamed pkg-config patch

* Fri May 30 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 1.7-3
- Add Requires pkgconfig to -devel

* Mon May 26 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 1.7-2
- Add patch which makes a libvoikko.pc file for pkg-config

* Sat May 24 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 1.7-1
- libvoikko 1.7

* Thu May 22 2008 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.7-0.2.rc2
- Don't BuildRequire the Finnish data files, this should make Koji builds a bit
  quicker

* Sun May 11 2008 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.7-0.1.rc2
- New release candidate

* Sun Mar 02 2008 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.6-3
- Put voikkospell and voikkohyphenate into a separate voikko-tools
  subpackage to decrease the size of the binary libvoikko package

* Sat Feb 16 2008 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.6-2
- Rebuild for GCC 4.3

* Tue Dec 04 2007 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.6-1
- libvoikko 1.6
- Add versioned BuildRequires and Requires as per the Voikko release notes
  at http://voikko.sourceforge.net/releases.html

* Mon Dec 03 2007 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.6-0.4.rc4
- Upstream released a new release candidate

* Wed Nov 28 2007 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.6-0.3.rc3
- Upstream released a new release candidate

* Wed Nov 28 2007 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.6-0.2.rc2
- Upstream released a new release candidate

* Tue Nov 27 2007 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.6-0.1.rc1
- Upstream released a new release candidate

* Thu Nov 08 2007 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.5-1
- Bump Release for the first Fedora build

* Wed Nov 07 2007 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.5-0.3
- libvoikko-devel: remove unneeded Requires: malaga-devel
- install with -p so that timestamps are preserved

* Wed Nov 07 2007 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.5-0.2
- Requires only malaga-suomi-voikko, BR malaga-devel and malaga-suomi-voikko
- Remove static archive

* Wed Oct 24 2007 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.5-0.1
- Initial package
