%define debug_package %{nil}

Summary:	Autoconf macro archive
Name:		autoconf-archive
Version:	2018.03.13
Release:        2%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/autoconf-archive
Group:		System Environment/Base
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:	http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
%define sha1 autoconf-archive=6177513edcf3998e07684cf65fbb7470acc72997

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
%doc AUTHORS NEWS README TODO
%license COPYING*
%{_datadir}/aclocal/*.m4

%changelog
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2018.03.13-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Sep 10 2018 Anish Swaminathan <anishs@vmware.com> 2018.03.13-1
-   Initial build
