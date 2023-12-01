Summary:        The package automatically configure source code
Name:           autoconf
Version:        2.71
Release:        3%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://www.gnu.org/software/autoconf/
Source0:        https://ftp.gnu.org/gnu/autoconf/%{name}-%{version}.tar.xz
BuildRequires:  m4
BuildRequires:  perl

# Dependency on "gtk-doc" regardless of the project's need to build documentation introduced in 2.70.
# Still an open issue as of 15th of March 2022: https://savannah.gnu.org/support/?110503.
Requires:       gtk-doc

%if %{with_check}
BuildRequires:  perl(File::Find)
%endif
Requires:       m4
Requires:       perl-libs
BuildArch:      noarch

%description
The package contains programs for producing shell scripts that can
automatically configure source code.

%prep
%setup -q

%build
%configure \
    --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}

%check
make -k check %{?_smp_mflags}

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_mandir}/*/*
%{_datarootdir}/autoconf/*

%changelog
* Thu Mar 17 2022 Muhammad Falak <mwani@microsoft.com> - 2.71-3
- Drop TESTSUITEFLAGS and run all tests cases
- Add an explicit BR on `perl(File::Find)` to enable ptest

* Tue Mar 15 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.71-2
- Adding run-time dependency on "gtk-doc".

* Mon Nov 22 2021 Andrew Phelps <anphel@microsoft.com> - 2.71-1
- Update to version 2.71
- License verified
- Remove unneeded autoconf-make-check.patch

* Fri Mar 26 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.69-11
- Merge the following releases from 1.0 to dev branch
- anphel@microsoft.com, 2.69-10: Fix check tests

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> - 2.69-10
- Use new perl package names.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.69-9
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.69-8
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Oct 17 2018 Dweep Advani <dadvani@vmware.com> - 2.69-7
- Build section is changed to used %configure

* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.69-6
- Fix arch

* Tue Dec 6 2016 Dheeraj Shetty <dheerajs@vmware.com> - 2.69-5
- Fixed Bug 1718089 make check failure

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.69-4
- GA - Bump release of all rpms

* Fri Jun 5 2015 Divya Thaluru <dthaluru@vmware.com> - 2.69-3
- Adding m4 package to build and run time required package

* Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> - 2.69-2
- Adding perl packages to required packages

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> - 2.69-1
- Initial build. First version
