Summary:        zip-3.0
Name:           zip
Version:        3.0
Release:        6%{?dist}
License:        BSD
URL:            https://infozip.sourceforge.net/
Source0:        https://downloads.sourceforge.net/infozip/zip30.tar.gz
Patch:          CVE-2018-13410.patch
Group:          SystemUtilities
Vendor:         Microsoft Corporation
Distribution:   Azure Linux

%description
The Zip package contains Zip utilities.

%prep
%autosetup -p1 -n %{name}30

%build
make -f unix/Makefile generic_gcc %{?_smp_mflags}

%install
install -v -m755 -d %{buildroot}%{_bindir}
make prefix=%{buildroot}/%{_prefix} MANDIR=%{buildroot}/usr/share/man/man1 -f unix/Makefile install

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/*
%{_mandir}/*

%changelog
*   Thu Feb 15 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0-6
-   Updated patch application macros.

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 3.0-5
-   Added %%license line automatically
*   Mon May 04 2020 Emre Girgin <mrgirgin@microsoft.com> 3.0-4
-   Fix CVE-2018-13410.
-   Update Source0 and URL.
-   License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.0-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0-2
-   GA - Bump release of all rpms
*   Fri May 29 2015 Alexey Makhalov <amakhalov@vmware.com> 3.0-1
-   Initial build. First version
