%bcond_with docs
Summary:        Module manipulating metadata files
Name:           libmodulemd
Version:        2.13.0
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://github.com/fedora-modularity/libmodulemd
Source0:        https://github.com/fedora-modularity/libmodulemd/releases/download/%{version}/modulemd-%{version}.tar.xz
Patch1:         test_import_headers_timeout.patch
BuildRequires:  clang-devel
BuildRequires:  gcc
BuildRequires:  glib
BuildRequires:  gobject-introspection-devel
BuildRequires:  libyaml-devel
BuildRequires:  meson
BuildRequires:  python3-gobject
BuildRequires:  python3-pycodestyle
BuildRequires:  valgrind
%if %{with docs}
BuildRequires:  gtk-doc
%endif
Requires:       libyaml

%description
C Library for manipulating module metadata files

%package        devel
Summary:        Header and development files for libmodulemd
Requires:       %{name} = %{version}-%{release}
Requires:       libyaml-devel

%description    devel
It contains the libraries and header files.

%prep
%autosetup -p1 -n modulemd-%{version}

%build
%meson \
%if %{with docs}
    -Dwith_docs=true \
%else
    -Dwith_docs=false \
%endif
    -Dwith_manpages=disabled
%meson_build

%install
%meson_install

%check
export LC_CTYPE=C.utf8
%meson_test

%ldconfig_scriptlets

%files
%license COPYING
%doc README.md
%{_bindir}/modulemd-validator
%{_libdir}/girepository-1.0/Modulemd-2.0.typelib
%{_libdir}/libmodulemd.so.2*
%{_datadir}/gir-1.0/Modulemd-2.0.gir
%if %{with docs}
%{_datadir}/gtk-doc/html/modulemd-1.0/*
%endif
%{python3_sitelib}/*

%files devel
%{_libdir}/libmodulemd.so
%{_libdir}/pkgconfig/modulemd-2.0.pc
%{_includedir}/modulemd-2.0/*

%changelog
* Sun Dec 12 2021 Chris Co <chrco@microsoft.com> - 2.13.0-2
- Fix build options with new meson

* Tue Sep 14 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.13.0-1
- Upgrade to latest version
- Use updated source URL

* Fri Apr 02 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.5.0-6
- Merge the following releases from dev to 1.0 spec
- joschmit@microsoft.com, 2.5.0-4: Replace python3-pygobject requires with python3-gobject.

*   Tue Jan 05 2021 Andrew Phelps <anphel@microsoft.com> 2.5.0-5
-   Improve test reliability by increasing timeout.

*   Thu Nov 19 2020 Andrew Phelps <anphel@microsoft.com> 2.5.0-4
-   Fix check test.

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 2.5.0-3
-   Added %%license line automatically

*   Tue Apr 07 2020 Nicolas Ontiveros <niontive@microsoft.com> 2.5.0-2
-   Remove python3-autopep8 from BuildRequires.

*   Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> 2.5.0-1
-   Update to 2.5.0. Source0 URL Fixed. License verified.

*   Wed Sep 25 2019 Saravanan Somasundaram <sarsoma@microsoft.com> 2.4.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Wed May 15 2019 Ankit Jain <ankitja@vmware.com> 2.4.0-1
-   Initial build. First version
