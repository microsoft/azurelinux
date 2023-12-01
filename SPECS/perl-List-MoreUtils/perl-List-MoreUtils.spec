# Got the intial spec from Fedora and modified it
Summary:        Provide the stuff missing in List::Util
Name:           perl-List-MoreUtils
Version:        0.430
Release:        2%{?dist}
License:        ASL 2.0 AND (GPLv1 OR Artistic)
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/List-MoreUtils/
Source0:        https://cpan.metacpan.org/authors/id/R/RE/REHSACK/List-MoreUtils-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Mariner

BuildArch:      noarch
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl-Exporter-Tiny
BuildRequires:  perl-generators
%if %{with_check}
BuildRequires:  perl(Math::Trig)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Tie::Array)
%endif

Requires:       perl-Exporter-Tiny
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)

Provides:       perl(List::MoreUtils) = %{version}-%{release}
Provides:       perl(List::MoreUtils::PP) = %{version}-%{release}

%description
List::MoreUtils provides some trivial but commonly needed functionality
on lists that is not going to go into List::Util.

%prep
%setup -q -n List-MoreUtils-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PERLLOCAL=1 NO_PACKLIST=1
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name 'perllocal.pod' -delete
%{_fixperms} -c %{buildroot}

%check
# Install required module List::MoreUtils::XS for maketest
export PERL_MM_USE_DEFAULT=1
echo "yes" | cpan -a
cpan local::lib
cpan -i List::MoreUtils::XS
make test

%files
%license ARTISTIC-1.0 GPL-1 LICENSE
%{perl_vendorlib}/List/
%{_mandir}/man3/List::MoreUtils.3*
%{_mandir}/man3/List::MoreUtils::PP.3*
%{_mandir}/man3/List::MoreUtils::Contributing.3pm.gz

%changelog
* Tue Aug 23 2022 Muhammad Falak <mwani@microsoft.com> - 0.430-2
- Add BR on `perl-{(Math::Trig),(Test::More),(Tie::Array)}` to enable ptest

* Fri Apr 22 2022 Mateusz Malisz <mamalisz@microsoft.com> - 0.430-1
- Update to 0.430

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.428-8
- Adding 'BuildRequires: perl-generators'.

* Fri Apr 02 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.428-7
- Merge the following releases from 1.0 to dev branch
- pawelwi@microsoft.com, 1.26-4: Adding 'local::lib' perl5 library to fix test dependencies.
- Removed %%sha1 macro.
- License verified and extended %%license macro to include all license files.

* Fri Nov 13 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.428-5
- Adding 'local::lib' perl5 library to fix test dependencies.
- Removed %%sha1 macro.
- License verified and extended %%license macro to include all license files.

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 0.428-6
- Use new perl package names.
- Provide perl(List::MoreUtils*).

* Mon Sep 28 2020 Joe Schmitt <joschmit@microsoft.com> 0.428-5
- Switch to new perl man page extension.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 0.428-4
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.428-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Dec 03 2018 Dweep Advani <dadvani@vmware.com> 0.428-2
- Fix makecheck tests

* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 0.428-1
- Update to version 0.428

* Wed Apr 05 2017 Robert Qi <qij@vmware.com> 0.418-1
- Update version to 0.418

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.413-2
- GA - Bump release of all rpms

* Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 0.413-1
- Updated to version 0.413

* Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 0.410-1
- Initial version.
