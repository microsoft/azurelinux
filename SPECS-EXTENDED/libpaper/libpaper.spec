Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#%%global nmu +nmu4

Name:		libpaper
Version:	1.1.28
Release:	2%{?dist}
Summary:	Library and tools for handling papersize
License:	GPLv2
URL:		https://packages.qa.debian.org/libp/libpaper.html
Source0:	https://ftp.debian.org/debian/pool/main/libp/libpaper/%{name}_%{version}.tar.gz


# Filed upstream as:
# https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=481213
Patch2:		libpaper-useglibcfallback.patch
# Memory leak
Patch3:   libpaper-file-leak.patch
# memory leak found by covscan, reported to debian upstream
#Patch4: libpaper-covscan.patch


# gcc is no longer in buildroot by default
BuildRequires:  gcc
# use git for autosetup
BuildRequires:  git-core
# uses make
BuildRequires:  make
BuildRequires:	libtool, gettext, gawk

%description
The paper library and accompanying files are intended to provide a 
simple way for applications to take actions based on a system- or 
user-specified paper size. This release is quite minimal, its purpose 
being to provide really basic functions (obtaining the system paper name 
and getting the height and width of a given kind of paper) that 
applications can immediately integrate.

%package devel
Summary:	Headers/Libraries for developing programs that use libpaper
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains headers and libraries that programmers will need 
to develop applications which use libpaper.

%prep
%autosetup -S git
libtoolize

%build
touch AUTHORS NEWS
aclocal
autoheader
autoconf
automake -a
%configure --disable-static
# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build

%install
%make_install
rm $RPM_BUILD_ROOT%{_libdir}/*.la
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
echo '# Simply write the paper name. See papersize(5) for possible values' > $RPM_BUILD_ROOT%{_sysconfdir}/papersize
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/libpaper.d
for i in cs da de es fr gl hu it ja nl pt_BR sv tr uk vi; do
	mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/$i/LC_MESSAGES/;
	msgfmt debian/po/$i.po -o $RPM_BUILD_ROOT%{_datadir}/locale/$i/LC_MESSAGES/%{name}.mo;
done
%find_lang %{name}

%ldconfig_scriptlets

%files -f %{name}.lang
%doc ChangeLog README
%license COPYING
%config(noreplace) %{_sysconfdir}/papersize
%dir %{_sysconfdir}/libpaper.d
%{_bindir}/paperconf
%{_libdir}/libpaper.so.1.1.2
%{_libdir}/libpaper.so.1
%{_sbindir}/paperconfig
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files devel
%{_includedir}/paper.h
%{_libdir}/libpaper.so
%{_mandir}/man3/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.28-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

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
