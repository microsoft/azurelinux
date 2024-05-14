Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: Convert filename encodings
Name: convmv
Version: 2.05
Release: 7%{?dist}

License: GPLv2 or GPLv3
URL: https://j3e.de/linux/convmv
Source0: https://j3e.de/linux/convmv/convmv-%{version}.tar.gz
Patch0: convmv-2.0-preserve-timestamps.patch
BuildArch: noarch
BuildRequires: perl-generators
BuildRequires: perl(Getopt::Long)
%if 0%{?with_check}
BuildRequires: perl(File::Find)
%endif

%description
This package contains the tool convmv with which you can convert the encodings
of filenames, e.g. from Latin1 to UTF-8.

%prep
%setup -q
%patch 0 -p1 -b .preserve-timestamps
tar -xf testsuite.tar

%build
make %{_smp_mflags}

%check
make test

%install
make PREFIX=%{_prefix} DESTDIR=%{buildroot} install

%files
%doc CREDITS Changes TODO
%license GPL2
%{_bindir}/convmv
%{_mandir}/man*/*

%changelog
* Wed Apr 20 2022 Muhammad Falak <mwani@microsoft.com> - 2.05-7
- Add an explicit BR on `perl(File::Find)` to enable ptest
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.05-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Mar 27 2018 Parag Nemade <pnemade AT redhat DOT com> - 2.05-1
- Update to 2.05 version (#1467456)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Nils Philippsen <nils@tiptoe.de> - 2.01-1
- version 2.01

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Feb 23 2016 Parag Nemade <pnemade AT redhat DOT com> - 2.0-4
- Resolves:rh#1307401: FTBFS in rawhide
- Added %%license tag

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 19 2015 Nils Philippsen <nils@redhat.com> - 2.0-1
- version 2.0
- use patch to patch Makefile instead of sed

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Parag Nemade <pnemade AT redhat DOT com> - 1.15-2
- Follow the recent packaging guideline changes

* Wed Sep 11 2013 Nils Philippsen <nils@redhat.com> - 1.15-1
- version 1.15
- reenable testsuite
- fix bogus dates in changelog

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.14-7
- Perl 5.18 rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 03 2009 Nils Philippsen <nils@redhat.com> - 1.14-1
- version 1.14
- temporarily disable "make test" to work around problems in koji

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 25 2008 Nils Philippsen <nphilipp@redhat.com> - 1.12-1
- version 1.12
- remove obsolete tests patch
- don't run md5sum against MD5sums as it lists a non-existing .MD5sums file
  which causes md5sum to error out
- change license tag to "GPLv2 or GPLv3"

* Thu Sep 27 2007 Nils Philippsen <nphilipp@redhat.com> - 1.10-3
- don't expect find output to be sorted, move "make test" to %%check (#237687,
  patch by Giuseppe Bonacci)
- change license tag to "GPLv2"

* Mon Aug 28 2006 Nils Philippsen <nphilipp@redhat.com> - 1.10-2
- FC6 mass rebuild

* Wed Aug 16 2006 Nils Philippsen <nphilipp@redhat.com> - 1.10-1
- version 1.10
- use dist tag

* Fri Mar 10 2006 Nils Philippsen <nphilipp@redhat.com>
- version 1.09

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Fri Jan 14 2005 Warren Togami <wtogami@redhat.com>
- remove testsuite.tar from doc

* Fri Jan 14 2005 Nils Philippsen <nphilipp@redhat.com>
- version 1.08

* Sat Feb 07 2004 Nils Philippsen <nphilipp@redhat.com>
- version 1.07
- initial build
