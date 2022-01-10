%define debug_package %{nil}

Summary:	Autoconf macro archive
Name:		autoconf-archive
Version:	2021.02.19
Release:    1%{?dist}
License:	GPLv3+
URL:		https://www.gnu.org/software/autoconf-archive
Group:		System Environment/Base
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:	https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz

BuildArch:  noarch
Requires:	autoconf

%description
The package contains programs for producing shell scripts that can
automatically configure source code.
%prep
%setup -q
%build
%configure
make
%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
rm -rf %{buildroot}%{_infodir}
rm -frv %{buildroot}%{_datadir}/%{name}

%files
%doc AUTHORS NEWS README TODO COPYING*
%license COPYING*
%{_datadir}/aclocal/*.m4

%changelog
*   Thu Jan 06 2022 Nicolas Guibourge <nicolasg@microsoft.com> 2021.02.19-1
-   Upgrade to 2021.02.19
-   License verified
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2018.03.13-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Sep 10 2018 Anish Swaminathan <anishs@vmware.com> 2018.03.13-1
-   Initial build
