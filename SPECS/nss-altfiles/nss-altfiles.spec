Summary:        NSS module to read passwd/group files from alternate locations
Name:           nss-altfiles
Version:        2.23.0
Release:        4%{?dist}
License:        LGPLv2+
URL:            https://github.com/aperezdc/nss-altfiles
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
#Source0:       https://github.com/aperezdc/nss-altfiles/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  glibc-devel

%description
NSS module to read passwd/group files from alternate locations.

%prep
%setup -q

%build
env CFLAGS='%{optflags}' ./configure --prefix=%{_prefix} --libdir=%{_libdir}

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%doc README.md
%{_libdir}/*.so.*

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.23.0-4
- Added %%license line automatically

*   Tue Apr 07 2020 Paul Monson <paulmon@microsoft.com> 2.23.0-3
-   Add #Source0.  License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.23.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*	Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.23.0-1
-	Update to 2.23.0
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.19.1-2
-	GA - Bump release of all rpms
*   Sat Jul 11 2015 Touseef Liaqat <tliaqat@vmware.com> 2.19.1-2
-   Initial version
