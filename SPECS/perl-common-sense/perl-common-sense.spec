# Got the intial spec from Fedora and modified it
# This arch-specific package has no binaries and generates no debuginfo
%global debug_package %{nil}

Summary:        "Common sense" Perl defaults
Name:           perl-common-sense
Version:        3.75
Release:        1%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/common-sense
Source0:        http://search.cpan.org/CPAN/authors/id/M/ML/MLEHMANN/common-sense-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl-generators

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Provides:       perl(common::sense) = %{version}-%{release}

Patch1:         common-sense-3.71-podenc.patch

%description
This module implements some sane defaults for Perl programs, as defined
by two typical (or not so typical - use your common sense) specimens of
Perl coders:

It's supposed to be mostly the same, with much lower memory usage, as:

        use utf8;
        use strict qw(vars subs);
        use feature qw(say state switch);
        use feature qw(unicode_strings unicode_eval current_sub fc evalbytes);
        no feature qw(array_base);
        no warnings;
        use warnings qw(FATAL closed threads internal debugging pack
                        portable prototype inplace io pipe unpack malloc
                        deprecated glob digit printf layer
                        reserved taint closure semicolon);
        no warnings qw(exec newline unopened);

%prep
%setup -q -n common-sense-%{version}

# Specify POD encoding
%patch1

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

# Have a non-empty manpage too
pod2man sense.pod > %{buildroot}%{_mandir}/man3/common::sense.3pm

%check
make test

%files
%license LICENSE
%dir %{perl_vendorarch}/common/
%{perl_vendorarch}/common/sense.pm
%doc %{perl_vendorarch}/common/sense.pod
%{_mandir}/man3/common::sense.3*

%changelog
* Tue Apr 26 2022 Mateusz Malisz <mamalisz@microsoft.com> - 3.75-1
- Update to 3.75

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.74-8
- Adding 'BuildRequires: perl-generators'.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.74-7
- Removing the explicit %%clean stage.
- License verified.

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 3.74-6
- Use new perl package names.
- Provide perl(common::sense).

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.74-5
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.74-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 3.74-3
- Consuming perl version upgrade of 5.28.0

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.74-2
- GA - Bump release of all rpms

* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.74-1
- Upgraded to version 3.74

* Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 3.73-1
- Initial version.
