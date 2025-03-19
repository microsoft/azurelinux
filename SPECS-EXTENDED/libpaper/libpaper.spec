Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:		libpaper
Version:	2.1.1
Release:	1%{?dist}
# Needed to replace separate paper package
Epoch:		1
Summary:	Library and tools for handling papersize
# libpaper is LGPL-2.1+
# bundled libgnu is LGPL-2.1+, LGPL-2+ and GPL-3+
# paperspecs is Public Domain
# localepaper.c is FSFAP
License:	LGPL-2.1-or-later AND LicenseRef-Fedora-Public-Domain AND GPL-3.0-or-later AND LGPL-2.0-or-later AND FSFAP
URL:		https://github.com/rrthomas/libpaper/
Source0:	https://github.com/rrthomas/libpaper/archive/v%{version}/%{name}-%{version}.tar.gz
# Pulled from paper
Source1:	localepaper.c
# from libpaper-1.x
Source2:        paperconf.1
 
# gcc is no longer in buildroot by default
BuildRequires:  gcc
# use git for autosetup
BuildRequires:  git-core
# uses make
BuildRequires:  make
BuildRequires:	libtool, gettext, gawk, autoconf, automake
BuildRequires:	help2man, tar, gnupg2, perl-interpreter, gzip
 
Provides: bundled(gnulib)
 
%description
The libpaper package enables users to indicate their preferred paper
size and specifies system-wide and per-user paper size catalogues, which can
also be used directly (see paperspecs(5)).
 
%package devel
Summary:	Headers/Libraries for developing programs that use libpaper
Requires:	%{name}%{?_isa} = %{epoch}:%{version}-%{release}
 
%description devel
This package contains headers and libraries that programmers will need
to develop applications which use libpaper.
 
%package -n paper
Summary:	Print paper size information
Requires:	%{name}%{?_isa} = %{epoch}:%{version}-%{release}
# This is licensed differently from libpaper.
# paper.c is GPL-3.0-or-later
# paperconf.c is GPL 2.0 only
# localepaper.c is FSFAP (except it is missing the warranty disclaimer... but the intent is clear)
License:	GPL-3.0-or-later AND FSFAP AND GPL-2.0-only
 
%description -n paper
The paper(1) utility can be used to find the user's preferred
default paper size and give information about known sizes.
 
%prep
%autosetup -S git
cp %{SOURCE1} src/
 
%if 0
sed -i 's|gnulib_tool=$gnulib_path/gnulib-tool|gnulib_tool=%{_bindir}/gnulib-tool|g' bootstrap
sed -i 's|./gnulib/gnulib-tool|%{_bindir}/gnulib-tool|g' bootstrap.conf
sed -i '/doc\/INSTALL/d' bootstrap
./bootstrap --gnulib-srcdir=%{_datadir}/gnulib/ --skip-git
%endif
 
%build
%configure --disable-static
%make_build
# localepaper
pushd src
%{__cc} %{optflags} -I.. -Ilibgnu -o localepaper localepaper.c libgnu/.libs/libgnupaper.a %{_hardening_ldflags}
popd
 
%check
# No upstream tests
echo "Testing localepaper tool"
locale width height > expected
./src/localepaper | tr ' ' "\n" > got
diff -u expected got
# No real way to test the paper tool
 
%install
%make_install
rm $RPM_BUILD_ROOT%{_libdir}/*.la
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
# maybe someday the translations will return
%if 0
for i in cs da de es fr gl hu it ja nl pt_BR sv tr uk vi; do
	mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/$i/LC_MESSAGES/;
	msgfmt debian/po/$i.po -o $RPM_BUILD_ROOT%{_datadir}/locale/$i/LC_MESSAGES/%{name}.mo;
done
%find_lang %{name}
%endif
 
mkdir %{buildroot}%{_libexecdir}
install -m0755 src/localepaper %{buildroot}%{_libexecdir}
 
gzip -c %{SOURCE2} > paperconf.1.gz
install -m0644 paperconf.1.gz %{buildroot}%{_mandir}/man1/paperconf.1
 
%ldconfig_scriptlets
%files
%doc ChangeLog README
%license COPYING
%config(noreplace) %{_sysconfdir}/paperspecs
%{_libdir}/libpaper.so.2*
 
%files devel
%{_includedir}/paper.h
%{_libdir}/libpaper.so
 
%files -n paper
%{_bindir}/paper
%{_bindir}/paperconf
%{_libexecdir}/localepaper
%{_mandir}/man1/paper.*
%{_mandir}/man1/paperconf.*
%{_mandir}/man5/paperspecs.*
 
%changelog
* Tue Mar 18 2025 Akarsh Chaudhary <v-akarshc@microsoft.com> - 2.1.1-1
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild
 
* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild
 
* Mon May 13 2024 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.1.1-6
- remove gnulib dependency and use bundled one
 
* Thu Apr 25 2024 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.1.1-5
- add paperconf manpage
 
* Tue Apr 23 2024 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.1.1-4
- apply hardening ldflags for localepaper
 
* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Tue Jul 25 2023 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.1.1-1
- 2.1.1
 
* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild
 
* Fri Apr 14 2023 Tom Callaway <spot@fedoraproject.org> - 1:2.1.0-1
- update to 2.1.0
 
* Fri Mar  3 2023 Tom Callaway <spot@fedoraproject.org> - 1:2.0.10-1
- update to 2.0.10
 
* Thu Feb 23 2023 Tom Callaway <spot@fedoraproject.org> - 1:2.0.9-1
- update to 2.0.9
 
* Tue Feb 14 2023 Tom Callaway <spot@fedoraproject.org> - 1:2.0.8-1
- update to 2.0.8
 
* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild
 
* Mon Jan 9 2023 Tom Callaway <spot@fedoraproject.org> - 2.0.4-2
- move /etc/paperspecs to libpaper to ensure proper functionality in cases where paper subpackage
  is not installed
- fix Requires to include epoch
 
* Sun Jan  8 2023 Tom Callaway <spot@fedoraproject.org> - 2.0.4-1
- update to 2.0.4
 
* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.28-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild
 
* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild
 
* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild
 
* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild
 
* Thu Nov 05 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.1.28-1
- 1.1.28
 
* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.24-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
 
* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 1.1.24-27
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro
 
* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.24-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
 
* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.24-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
 
* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.24-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
 
* Mon Dec 03 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.1.24-23
- fixing covscan issue - memory leak
 
* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.24-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
 
* Fri Mar 09 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.1.24-21
- remove nmu5 from .gitignore and sources
- fixed memory leak
 
* Wed Feb 21 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.1.24-20
- gcc is no longer in buildroot by default
 
* Thu Feb 08 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.1.24-19
- remove old stuff https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/MRWOMRZ6KPCV25EFHJ2O67BCCP3L4Y6N/
 
* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.24-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
 
* Mon Feb 05 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.1.24-17
- Switch to %%ldconfig_scriptlets
* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.24-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild
 
* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.24-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild
 
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.24-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild
 
* Fri Nov 11 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1.1.24-13
- bump to nmu4
 
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.24-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
 
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.24-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild
 
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.24-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild
 
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.24-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild
 
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.24-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild
 
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.24-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild
 
* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.24-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild
 
* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
 
* Tue May 17 2011 Tom Callaway <spot@fedoraproject.org> - 1.1.24-3
- bump to nmu1
 
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild
 
* Sat Apr 24 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.24-1
- update to 1.1.24
 
* Thu Mar  4 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.23-7
- update to 1.1.23+nmu2
 
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild
 
* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild
 
* Mon Feb 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.23-4
- run libtoolize to fix build with newer libtool
- disable rpath
 
* Fri Aug 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.23-3
- update to nmu1
- apply patch to fix imprecise definition of DL format
- apply patch so that when no config is present, libpaper will fallback through
  LC_PAPER before giving up and using Letter
 
* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.23-2
- Autorebuild for GCC 4.3
 
* Tue Feb 19 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.23-1
- 1.1.23
 
* Fri Aug 24 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.22-1.1
- missing BR: gawk
 
* Thu Aug 23 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.22-1
- bump, no real changes of note, rebuild for ppc32
- license fix, v2 only
 
* Mon Jul 09 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.21-1.1
- BR: libtool
 
* Mon Jul 09 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.21-1
- bump to 1.1.21
- fix automake bug (bz 247458)
 
* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 1.1.20-5
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21
 
* Sat Sep 23 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.20-4
- remove aclocal call
 
* Sat Sep 23 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.20-3
- fix FC-4 with aclocal call
- move man3 pages to -devel
- don't set default, just put comment in conf file
- own /etc/libpaper.d
- use debian/NEWS
- include the meager translations
- use --disable-static
 
* Sat Sep 23 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.20-2
- nuke static lib
- own /etc/papersize
- fix mixed spaces/tabs rpmlint warning
 
* Sat Sep 23 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.20-1
- initial package for Fedora Extras