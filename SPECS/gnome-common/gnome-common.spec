Summary:        Common development macros for GNOME
Name:           gnome-common
Version:        3.18.0
Release:        6%{?dist}
License:        GPLv2+
URL:            https://github.com/GNOME/gnome-common
Source0:        https://ftp.gnome.org/pub/GNOME/sources/%{name}/3.18/%{name}-%{version}.tar.xz
Group:          System Environment/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildArch:      noarch

%description
This provides Common development macros for GNOME.

%prep
%setup -q
./autogen.sh

%build
./configure \
        --prefix=%{_prefix}
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/gnome-autogen.sh
%{_datadir}/aclocal/*.m4

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.18.0-6
- Added %%license line automatically

*   Mon Apr 27 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 3.18.0-5
-   Fixed 'Source0' and 'URL' tags.
-   License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.18.0-4
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.18.0-3
-   Fix arch
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.18.0-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  3.18.0-1
-   Upgrade to 3.18.0
*   Tue Aug 11 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.14.0-1
-   Add gnome-common v3.14.0
