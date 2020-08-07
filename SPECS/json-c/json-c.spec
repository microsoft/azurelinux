Summary:        A JSON implementation in C
Name:           json-c
Version:        0.14
Release:        1%{?dist}
License:        MIT
Group:          System Environment/Base
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/json-c/json-c
#Source0:       %{url}/archive/%{name}-%{version}-20200419.tar.gz
Source0:        %{name}-%{name}-%{version}-20200419.tar.gz
Patch0:         CVE-2020-12762.patch

BuildRequires: cmake

%description
JSON-C implements a reference counting object model that allows you to easily construct JSON objects in C, output them as JSON formatted strings and parse JSON formatted strings back into the C representation of JSON objects.

%package devel
Summary:    Development libraries and header files for json-c
Requires:   %{name} = %{version}-%{release}

%description devel
The package contains libraries and header files for
developing applications that use json-c.

%prep
%setup -q -n %{name}-%{name}-%{version}-20200419
%patch0 -p1

%build
mkdir build
pushd build
%cmake ..
make %{?_smp_mflags}
popd

%install
make DESTDIR=%{buildroot} install -C build
rm -r %{buildroot}%{_libdir}/cmake/%{name}

%check
make %{?_smp_mflags} check -C build

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/lib%{name}.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
*   Mon Jun 08 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.14-1
-   Bumping up version and adding a patch to fix CVE-2020-12762.
-   License verified.
-   Removing "sha1" macro.
-   Updated "Source0" tag to use the sources from project's main page instead of Amazon's AWS.
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 0.13.1-3
-   Added %%license line automatically
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.13.1-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Wed Oct 10 2018 Ankit Jain <ankitja@vmware.com> 0.13.1-1
-   Updated package to version 0.13.1
*   Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 0.12.1-1
-   Updated package to version 0.12.1
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.12-2
-   GA - Bump release of all rpms
*   Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 0.12-1
-   Initial build. First version
