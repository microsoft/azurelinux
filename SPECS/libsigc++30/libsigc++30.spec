Summary:        Library that Implements a typesafe callback system for standard C++.
Name:           libsigc++30
Version:        3.4.0
Release:        1%{?dist}
License:        LGPLv2+
URL:            https://github.com/libsigcplusplus/libsigcplusplus
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://github.com/libsigcplusplus/libsigcplusplus/releases/download/%{version}/libsigc++-%{version}.tar.xz
BuildRequires:  docbook-style-xsl
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  graphviz
BuildRequires:  libxslt
BuildRequires:  m4
BuildRequires:  meson

%description
libsigc++ implements a typesafe callback system for standard C++. It
allows you to define signals and to connect those signals to any
callback function, either global or a member function, regardless of
whether it is static or virtual.
 
libsigc++ is used by gtkmm to wrap the GTK+ signal system. It does not
depend on GTK+ or gtkmm.

%package        doc
Summary:        Documentation for %{name}, includes full API docs
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
 
%description    doc
This package contains the full API documentation for %{name}.

%prep
%setup -qn libsigc++-%{version}

%build
%meson -Dbuild-documentation=true
%meson_build

%install
%meson_install

%files
%defattr(-,root,root)
%license COPYING
%doc AUTHORS README.md NEWS
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/sigc++-3.0/include/*.h
%{_includedir}/*

%files doc
%doc %{_datadir}/doc/libsigc++-3.0/
%doc %{_datadir}/devhelp/

%changelog
* Mon Nov 06 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.4.0-1
- Auto-upgrade to 3.4.0 - Azure Linux 3.0 - package upgrades

* Thu Feb 03 2022 Cameron Baird <cameronbaird@microsoft.com> - 3.2.0-1
- Update to v3.2.0
- Add doc package

* Fri Sep 10 2021 Thomas Crain <thcrain@microsoft.com> - 2.10.0-7
- Remove libtool archive files from final packaging

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.10.0-6
- Added %%license line automatically

* Wed Apr 29 2020 Emre Girgin <mrgirgin@microsoft.com> 2.10.0-5
- Renaming libsigc++ to libsigc++20

* Thu Apr 09 2020 Joe Schmitt <joschmit@microsoft.com> 2.10.0-4
- Fix Source0 comment.

* Tue Apr 07 2020 Joe Schmitt <joschmit@microsoft.com> 2.10.0-3
- Update Source0 with valid URL.
- Update URL.
- Remove sha1 macro.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.10.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu May 25 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.10.0-1
- Revert back to the stable version 2.10.0-1

* Wed Apr 12 2017 Danut Moraru <dmoraru@vmware.com> 2.99.8-1
- Updated to version 2.99.8

* Tue Apr 04 2017 Kumar Kaushik <kaushikk@vmware.com> 2.10.0-1
- Updated to version 2.10.0

* Tue Sep 06 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.8.0-1
- Updated to version 2.8.0-1

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.6.2-2
- GA - Bump release of all rpms

* Mon Feb 22 2016 XIaolin Li <xiaolinl@vmware.com> 2.6.2-1
- Updated to version 2.6.2

* Wed Nov 12 2014 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.4.0-1
- Initial version
