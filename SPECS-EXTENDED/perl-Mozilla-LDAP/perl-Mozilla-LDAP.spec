Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary: LDAP Perl module that wraps the OpenLDAP C SDK
Name: perl-Mozilla-LDAP
Version: 1.5.3
Release: 33%{?dist}
License: MPLv1.1
URL: https://metacpan.org/dist/perldap
Requires: perl-interpreter >= 2:5.8.0
BuildRequires:  gcc
BuildRequires: perl-interpreter >= 2:5.8.0
BuildRequires: perl-devel
BuildRequires: perl-generators
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: nspr-devel
BuildRequires: nss-devel
BuildRequires: openldap-devel >= 2.4.22
%if %{with_check}
BuildRequires: perl(AutoLoader)
%endif
# Source0: https://metacpan.org/dist/perldap/source
Source0: https://ftp.mozilla.org/pub/mozilla.org/directory/perldap/releases/%{version}/src/perl-mozldap-%{version}.tar.gz
Source1: https://ftp.mozilla.org/pub/mozilla.org/directory/perldap/releases/1.5/src/Makefile.PL.rpm

%description
%{summary}.

%prep
%setup -q -n perl-mozldap-%{version}
# Filter unwanted Provides:
cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} $* |\
  sed -e '/perl(Mozilla::LDAP::Entry)$/d'
EOF

%define __perl_provides %{_builddir}/perl-mozldap-%{version}/%{name}-prov
chmod +x %{__perl_provides}

# Filter unwanted Requires:
cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} $* |\
  sed -e '/perl(Mozilla::LDAP::Entry)/d'
EOF

%define __perl_requires %{_builddir}/perl-mozldap-%{version}/%{name}-req
chmod +x %{__perl_requires}

%build

LDAPPKGNAME=openldap CFLAGS="$RPM_OPT_FLAGS" perl %{SOURCE1} PREFIX=$RPM_BUILD_ROOT%{_prefix} INSTALLDIRS=vendor < /dev/null
make OPTIMIZE="$RPM_OPT_FLAGS" CFLAGS="$RPM_OPT_FLAGS" 

%install
rm -rf $RPM_BUILD_ROOT
eval `perl '-V:installarchlib'`

%makeinstall

# remove files we don't want to package
rm -f `find $RPM_BUILD_ROOT -type f -name perllocal.pod -o -name .packlist`
find $RPM_BUILD_ROOT -name API.bs -a -size 0 -exec rm -f {} \;

# make sure shared lib is correct mode
find $RPM_BUILD_ROOT -name API.so -exec chmod 755 {} \;


# find and run the correct version of brp-compress
if [ -x /usr/lib/rpm/brp-compress ] ; then
    /usr/lib/rpm/brp-compress
elif [ -x %{_libdir}/rpm/brp-compress ] ; then
    %{_libdir}/rpm/brp-compress
fi

# make sure files refer to %{_prefix} instead of buildroot/%prefix
find $RPM_BUILD_ROOT%{_prefix} -type f -print | \
	sed "s@^$RPM_BUILD_ROOT@@g" > %{name}-%{version}-%{release}-filelist
if [ "$(cat %{name}-%{version}-%{release}-filelist)X" = "X" ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit 1
fi

%check
make test

%files -f %{name}-%{version}-%{release}-filelist
%license MPL-1.1.txt
%doc CREDITS ChangeLog README

%changelog
* Thu Jan 13 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.3-33
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.3-32
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.5.3-29
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.5.3-26
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Petr Pisar <ppisar@redhat.com> - 1.5.3-22
- perl dependency renamed to perl-interpreter
  <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.5.3-21
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.5.3-19
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.5.3-16
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.5.3-15
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.5.3-11
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Nathan Kinder <nkinder@redhat.com> - 1.5.3-9
- Corrected upstream source URLs

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 23 2010 Rich Megginson <rmeggins@redhat.com> - 1.5.3-4
- forgot to add -DUSE_SSL -DPRLDAP

* Wed Sep 29 2010 jkeating - 1.5.3-3
- Rebuilt for gcc bug 634757

* Tue Sep 14 2010 Rich Megginson <rmeggins@redhat.com> - 1.5.3-2
- added new sources

* Tue Sep 14 2010 Rich Megginson <rmeggins@redhat.com> - 1.5.3-1
- new version 1.5.3 with openldap support

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.5.2-7.1
- Mass rebuild with perl-5.12.0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar 11 2008 Rich Megginson <rmeggins@redhat.com> - 1.5.2-4.1
- rebuild for perl 5.10

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.5.2-3.1
- Autorebuild for GCC 4.3

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.5.2-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.5.2-2
- Rebuild for selinux ppc32 issue.

* Fri Jul 27 2007 Rich Megginson <richm@stanfordalumni.org> - 1.5.2-1
- Fix bugzilla 389731 - crash when a bad URL is passed

* Wed Jun 20 2007 Rich Megginson <richm@stanfordalumni.org> - 1.5.1-1
- all files have been GPL/LGPL/MPL tri-licensed

* Wed Jan 10 2007 Rich Megginson <richm@stanfordalumni.org> - 1.5-9
- remove only perl(Mozilla::LDAP::Entry) from Provides, leave in 
- perl(Mozilla::LDAP::Entry) = 1.5

* Wed Jan 10 2007 Rich Megginson <richm@stanfordalumni.org> - 1.5-8
- add perl_requires filter for the Entry module
- add the MPL-1.1.txt file to the DOCs

* Wed Jan 10 2007 Rich Megginson <richm@stanfordalumni.org> - 1.5-7
- Incorporate comments from Fedora Extras review - https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=219869
- Remove all Requires except perl - use autogenerated ones
- Remove ExclusiveArch
- Remove files that don't need to be packaged
- add full URL to sources
- set API.so to mode 755

* Tue Oct 17 2006 Rich Megginson <richm@stanfordalumni.org> - 1.5-6
- look for brp-compress first in /usr/lib then _libdir

* Tue Oct 17 2006 Rich Megginson <richm@stanfordalumni.org> - 1.5-5
- there is no TODO file; use custom Makefile.PL

* Mon Oct 16 2006 Rich Megginson <richm@stanfordalumni.org> - 1.5-4
- use pkg-config --variable=xxx instead of --cflags e.g.

* Mon Oct 16 2006 Rich Megginson <richm@stanfordalumni.org> - 1.5-3
- this is not a noarch package

* Mon Oct 16 2006 Rich Megginson <richm@stanfordalumni.org> - 1.5-2
- Use new mozldap6, dirsec versions of nspr, nss

* Tue Feb  7 2006 Rich Megginson <richm@stanfordalumni.org> - 1.5-1
- Based on the perl-LDAP.spec file

