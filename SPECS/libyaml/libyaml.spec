Summary:        Implementation of a YAML 1.1 parser and emitter
Name:           libyaml
Version:        0.2.5
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries
URL:            https://pyyaml.org/wiki/LibYAML
Source0:        https://pyyaml.org/download/libyaml/yaml-%{version}.tar.gz

%description
LibYAML is a C library implementation of a YAML 1.1 parser and emitter.
It includes a Python language binding.

%package devel
Summary:        Header files, libraries and development documentation for %{name}.
Group:          Development/Libraries
Requires:       %{name}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q -n yaml-%{version}

%build
%configure --disable-static
make %{?_smp_mflags} AM_CFLAGS=""

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -type f -name "*.la" -delete -print

%check
make %{?_smp_mflags} check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%license License
%doc ReadMe.md
%{_libdir}/libyaml-0.so.*

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/yaml.h
%{_libdir}/libyaml.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.2.5-3
- Removing the explicit %%clean stage.
- License verified.

* Fri Sep 10 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.2.5-2
- Remove libtool archive files from final packaging

* Fri Jan 29 2021  Joe Schmitt <joschmit@microsoft.com> - 0.2.5-1
- Upgrade to v0.2.5.
- Update license and readme file names.
- Update Source0 to use https.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.2.1-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.2.1-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*       Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 0.2.1-1
-       Update to version 0.2.1

*       Fri Apr 14 2017 Kumar Kaushik <kaushikk@vmware.com> 0.1.7-1
-       Updating version to 0.1.7

*       Mon Oct 03 2016 Chang Lee <changlee@vmware.com> 0.1.6-4
-       Modified check

*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.1.6-3
-	GA - Bump release of all rpms

*       Fri Aug 14 2015 Vinay Kulkarni <kulkarniv@vmware.com> 0.1.6-2
-       Fix cve-2014-9130.

*       Mon Apr 6 2015 Divya Thaluru <dthaluru@vmware.com> 0.1.6-1
-       Initial package for Photon.
