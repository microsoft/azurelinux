# Got the intial spec from Fedora and modified it
Summary:        SQLite DBI Driver
Name:           perl-DBD-SQLite
Version:        1.74
Release:        1%{?dist}
Group:          Development/Libraries
License:        (GPL+ or Artistic) and Public Domain
URL:            http://search.cpan.org/dist/DBD-SQLite/
Source0:        https://cpan.metacpan.org/authors/id/I/IS/ISHIGAKI/DBD-SQLite-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  sqlite-devel >= 3.22.0
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl-DBI
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
%if %{with_check}
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Time::HiRes)
%endif

Requires:       perl-DBI
Requires:       perl-libs

Provides:       perl(DBD::SQLite) = %{version}-%{release}
Provides:       perl(DBD::SQLite::Constants) = %{version}-%{release}
Provides:       perl(DBD::SQLite::GetInfo) = %{version}-%{release}
Provides:       perl(DBD::SQLite::VirtualTable) = %{version}-%{release}
Provides:       perl(DBD::SQLite::VirtualTable::Cursor) = %{version}-%{release}
Provides:       perl(DBD::SQLite::VirtualTable::FileContent) = %{version}-%{release}
Provides:       perl(DBD::SQLite::VirtualTable::FileContent::Cursor) = %{version}-%{release}
Provides:       perl(DBD::SQLite::VirtualTable::PerlData) = %{version}-%{release}
Provides:       perl(DBD::SQLite::VirtualTable::PerlData::Cursor) = %{version}-%{release}

%description
SQLite is a public domain RDBMS database engine that you can find at
http://www.hwaci.com/sw/sqlite/.

This module provides a SQLite RDBMS module that uses the system SQLite
libraries.

%prep
%setup -q -n DBD-SQLite-%{version}

%build
CFLAGS="%{optflags}" perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags} OPTIMIZE="%{optflags}"

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name '*.bs' -size 0 \) -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license LICENSE
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/DBD/
%{_mandir}/man3/*

%changelog
* Mon Nov 27 2023 Andrew Phelps <anphel@microsoft.com> - 1.74-1
- Upgrade to version 1.74

* Mon Aug 01 2022 Muhammad Falak <mwani@microsoft.com> - 1.70-2
- Add BR on `perl(Test::More)` & `perl(Digest::MD5)` to fix ptest

* Tue Apr 26 2022 Mateusz Malisz <mamalisz@microsoft.com> - 1.70-1
- Update to 1.70

* Tue Feb 08 2022 Thomas Crain <thcrain@microsoft.com> - 1.62-6
- Remove unused `%%define sha1` lines

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.62-5
- Adding 'BuildRequires: perl-generators'.
- License verified.

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 1.62-4
- Use new perl package names.
- Provide perl(DBD::SQLite::*).

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.62-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.62-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Jan 22 2019 Michelle Wang <michellew@vmware.com> 1.62-1
- Update to version 1.62.

* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.58-1
- Update to version 1.58.

* Tue Feb 20 2018 Xiaolin Li <xiaolinl@vmware.com> 1.54-2
- Build perl-DBD-SQLite with sqlite-autoconf-3.22.0.

* Mon Apr 3 2017 Robert Qi <qij@vmware.com> 1.54-1
- Upgraded to 1.54.

* Wed Nov 16 2016 Alexey Makhalov <ppadmavilasom@vmware.com> 1.50-3
- Use sqlite-devel as a BuildRequires.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.50-2
- GA - Bump release of all rpms.

* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.50-1
- Upgraded to version 1.50.

* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.48-1
- Upgrade version.

* Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.46-1
- Initial version.
