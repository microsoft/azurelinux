Summary:	The package automatically configure source code
Name:		autoconf
Version:	2.69
Release:        9%{?dist}
License:	GPLv2
URL:		http://www.gnu.org/software/autoconf
Group:		System Environment/Base
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:	http://ftp.gnu.org/gnu/autoconf/%{name}-%{version}.tar.xz
%define sha1 autoconf=e891c3193029775e83e0534ac0ee0c4c711f6d23
Patch0:		autoconf-make-check.patch

Requires:	perl
BuildRequires:	m4
Requires:	m4
BuildArch:      noarch

%description
The package contains programs for producing shell scripts that can
automatically configure source code.
%prep
%setup -q
%patch0 -p1
%build
%configure \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}

%check
make -k check %{?_smp_mflags}  TESTSUITEFLAGS="1-500"

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_mandir}/*/*
%{_datarootdir}/autoconf/*
%changelog
* Sat May 09 00:21:00 PST 2020 Nick Samson <nisamson@microsoft.com> - 2.69-9
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.69-8
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Wed Oct 17 2018 Dweep Advani <dadvani@vmware.com> 2.69-7
-   Build section is changed to used %configure
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.69-6
-   Fix arch
*   Tue Dec 6 2016 Dheeraj Shetty <dheerajs@vmware.com> 2.69-5
-   Fixed Bug 1718089 make check failure
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.69-4
-   GA - Bump release of all rpms
*   Fri Jun 5 2015 Divya Thaluru <dthaluru@vmware.com> 2.69-3
-   Adding m4 package to build and run time required package
*   Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> 2.69-2
-   Adding perl packages to required packages
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.69-1
-   Initial build.	First version
