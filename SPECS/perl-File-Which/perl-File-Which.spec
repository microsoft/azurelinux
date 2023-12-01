Summary:        File-Which
Name:           perl-File-Which
Version:        1.27
Release:        2%{?dist}
License:        GPL+ OR Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/File-Which/
Source0:        https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/File-Which-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl(Env)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl-generators

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(File::Spec) >= 0.60

Provides:       perl(File::Which) = %{version}-%{release}

%description
File::Which finds the full or relative paths to executable programs on
    the system. This is normally the function of which utility. which is
    typically implemented as either a program or a built in shell command.
    On some platforms, such as Microsoft Windows it is not provided as part
    of the core operating system. This module provides a consistent API to
    this functionality regardless of the underlying platform.

    The focus of this module is correctness and portability. As a
    consequence platforms where the current directory is implicitly part of
    the search path such as Microsoft Windows will find executables in the
    current directory, whereas on platforms such as UNIX where this is not
    the case executables in the current directory will only be found if the
    current directory is explicitly added to the path.

    If you need a portable which on the command line in an environment that
    does not provide it, install App::pwhich which provides a command line
    interface to this API.
%prep
%autosetup -n File-Which-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
%make_build

%install
%make_install
find %{buildroot} -name 'perllocal.pod' -delete

%check
%make_build test

%files
%license LICENSE
%{perl_vendorlib}/*
%{perl_vendorlib}/File/Which.pm
%{_mandir}/man3/File::Which.3pm.gz


%changelog
* Wed Jul 27 2022 Muhammad Falak <mwani@microsoft.com> - 1.27-2
- Add BR on `perl(Test::More)`, `perl(Env)` & `perl(ExtUtils::MakeMaker)` to enable ptest

* Tue Apr 22 2022 Mateusz Malisz <mamalisz@microsoft.com> - 1.27-1
- Update to 1.27

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.22-7
- Adding 'BuildRequires: perl-generators'.

* Mon Aug 23 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.22-6
- Bump release to represent package's move to toolchain
- Lint spec
- License verified

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 1.22-5
- Use new perl package names.
- Provide perl(File::Which).

* Mon Sep 28 2020 Joe Schmitt <joschmit@microsoft.com> 1.22-4
- Switch to new perl man page extension.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.22-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.22-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.22-1
- Update to version 1.22

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.21-2
- GA - Bump release of all rpms

* Thu Mar 3 2016 Xiaolin Li <xiaolinl@vmware.com> 1.21-1
- Initial version.
