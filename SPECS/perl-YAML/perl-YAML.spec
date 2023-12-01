# Got the intial spec from Fedora and modified it
Summary:        YAML Ain't Markup Language (tm)
Name:           perl-YAML
Version:        1.30
Release:        2%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/YAML/
Source0:        https://cpan.metacpan.org/authors/id/T/TI/TINITA/YAML-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildArch:      noarch
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
%if %{with_check}
BuildRequires:  perl(CPAN)
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
BuildRequires:  perl-debugger
%endif

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(B::Deparse)
Requires:       perl(Carp)
Provides:       perl(YAML) = %{version}-%{release}
Provides:       perl(YAML::Any) = %{version}-%{release}
Provides:       perl(YAML::Dumper) = %{version}-%{release}
Provides:       perl(YAML::Dumper::Base) = %{version}-%{release}
Provides:       perl(YAML::Error) = %{version}-%{release}
Provides:       perl(YAML::Loader) = %{version}-%{release}
Provides:       perl(YAML::Loader::Base) = %{version}-%{release}
Provides:       perl(YAML::Marshall) = %{version}-%{release}
Provides:       perl(YAML::Mo) = %{version}-%{release}
Provides:       perl(YAML::Node) = %{version}-%{release}
Provides:       perl(YAML::Tag) = %{version}-%{release}
Provides:       perl(YAML::Type::blessed) = %{version}-%{release}
Provides:       perl(YAML::Type::code) = %{version}-%{release}
Provides:       perl(YAML::Type::glob) = %{version}-%{release}
Provides:       perl(YAML::Type::ref) = %{version}-%{release}
Provides:       perl(YAML::Type::regexp) = %{version}-%{release}
Provides:       perl(YAML::Type::undef) = %{version}-%{release}
Provides:       perl(YAML::Types) = %{version}-%{release}
Provides:       perl(YAML::Warning)
# Filter private provides:
# perl(yaml_mapping) perl(yaml_scalar) perl(yaml_sequence)
%global __provides_exclude ^perl\\(yaml_

%description
The YAML.pm module implements a YAML Loader and Dumper based on the
YAML 1.0 specification. http://www.yaml.org/spec/
YAML is a generic data serialization language that is optimized for
human readability. It can be used to express the data structures of
most modern programming languages, including Perl.
For information on the YAML syntax, please refer to the YAML
specification.

%prep
%setup -q -n YAML-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name 'perllocal.pod' -delete

%check
export PERL_MM_USE_DEFAULT=1
cpan local::lib
cpan Test::YAML
make %{?_smp_mflags} test

%files
%license LICENSE
%dir %{perl_vendorlib}/YAML/
%dir %{perl_vendorlib}/YAML/Dumper/
%dir %{perl_vendorlib}/YAML/Loader/
%doc %{perl_vendorlib}/YAML.pod
%doc %{perl_vendorlib}/YAML/Any.pod
%doc %{perl_vendorlib}/YAML/Dumper.pod
%doc %{perl_vendorlib}/YAML/Dumper/Base.pod
%doc %{perl_vendorlib}/YAML/Error.pod
%doc %{perl_vendorlib}/YAML/Loader.pod
%doc %{perl_vendorlib}/YAML/Loader/Base.pod
%doc %{perl_vendorlib}/YAML/Marshall.pod
%doc %{perl_vendorlib}/YAML/Node.pod
%doc %{perl_vendorlib}/YAML/Tag.pod
%doc %{perl_vendorlib}/YAML/Types.pod
%{perl_vendorlib}/YAML.pm
%{perl_vendorlib}/YAML/Any.pm
%{perl_vendorlib}/YAML/Dumper.pm
%{perl_vendorlib}/YAML/Dumper/Base.pm
%{perl_vendorlib}/YAML/Error.pm
%{perl_vendorlib}/YAML/Loader.pm
%{perl_vendorlib}/YAML/Loader/Base.pm
%{perl_vendorlib}/YAML/Marshall.pm
%{perl_vendorlib}/YAML/Mo.pm
%{perl_vendorlib}/YAML/Node.pm
%{perl_vendorlib}/YAML/Tag.pm
%{perl_vendorlib}/YAML/Types.pm
%{_mandir}/man3/YAML.3*
%{_mandir}/man3/YAML::Any.3*
%{_mandir}/man3/YAML::Dumper.3*
%{_mandir}/man3/YAML::Dumper::Base.3*
%{_mandir}/man3/YAML::Error.3*
%{_mandir}/man3/YAML::Loader.3*
%{_mandir}/man3/YAML::Loader::Base.3*
%{_mandir}/man3/YAML::Marshall.3*
%{_mandir}/man3/YAML::Node.3*
%{_mandir}/man3/YAML::Tag.3*
%{_mandir}/man3/YAML::Types.3*

%changelog
* Fri Jul 29 2022 Muhammad Falak <mwani@microsoft.com> - 1.30-2
- Add BR on `perl(ExtUtils::MakeMaker)` & `cpan` to enable ptest

* Thu Apr 14 2022 Mateusz Malisz <mateusz.malisz@microsoft.com> - 1.30-1
- Updated to 1.30

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.26-6
- Adding 'BuildRequires: perl-generators'.
- License verified.

* Fri Apr 02 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.26-5
- Merge the following releases from 1.0 to dev branch
- pawelwi@microsoft.com, 1.26-4: Adding 'local::lib' perl5 library to fix test dependencies.

*   Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 1.26-4
-   Use new perl package names.
-   Provide perl(YAML::*).

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.26-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.26-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.26-1
-   Update to version 1.26
*   Wed Apr 05 2017 Robert Qi <qij@vmware.com> 1.23-1
-   Update version to 1.23
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 1.15-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.15-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.15-1
-   Updated to version 1.15
*   Mon Feb 01 2016 Anish Swaminathan <anishs@vmware.com> 1.14-2
-   Fix for multithreaded perl
*   Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.14-1
-   Initial version.
