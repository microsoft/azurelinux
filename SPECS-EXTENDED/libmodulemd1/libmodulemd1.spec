Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           libmodulemd1
Version:        1.8.16
Release:        3%{?dist}
Summary:        Module metadata manipulation library

License:        MIT
URL:            https://github.com/fedora-modularity/libmodulemd
Source0:        %{url}/releases/download/libmodulemd-%{version}/modulemd-%{version}.tar.xz

BuildRequires:  meson >= 0.47
BuildRequires:  pkgconfig
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glib2-doc
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(yaml-0.1)
BuildRequires:  pkgconfig(gtk-doc)
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-gobject-base
%ifarch %{valgrind_arches}
BuildRequires:  valgrind
%endif

Obsoletes: libmodulemd < 1.8.15
Provides: libmodulemd = %{version}-%{release}
Provides: libmodulemd%{?_isa} = %{version}-%{release}

# Patches


%description
C Library for manipulating module metadata files.
See https://github.com/fedora-modularity/libmodulemd/blob/master/README.md for
more details.


%package -n python%{python3_pkgversion}-%{name}
Summary: Python 3.6 bindings for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: python%{python3_pkgversion}-gobject-base
Obsoletes: python3-modulemd < 1.3.4
Obsoletes: python2-%{name} < 1.8.15-3

%description -n python%{python3_pkgversion}-%{name}
Python 3 bindings for %{name}


%package devel
Summary:        Development files for libmodulemd
Requires:       %{name}%{?_isa} = %{version}-%{release}
Conflicts:      libmodulemd-devel

%description devel
Development files for libmodulemd.


%prep
%autosetup -p1 -n modulemd-%{version}


%build
%meson -Ddeveloper_build=false
%meson_build


%check

export LC_CTYPE=C.utf8

%ifarch %{power64} s390x
# Valgrind is broken on ppc64[le] with GCC7:
# https://bugs.kde.org/show_bug.cgi?id=386945
export MMD_SKIP_VALGRIND=1
%endif
%ifnarch %{valgrind_arches}
export MMD_SKIP_VALGRIND=1
%endif

# Don't run tests on ARM for now. There are problems with
# performance on the builders and often these time out.
%ifnarch %{arm} aarch64
%meson_test
%endif


%install
%meson_install


%files
%license COPYING
%doc README.md
%{_bindir}/modulemd-validator-v1
%{_libdir}/libmodulemd.so.1*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/Modulemd-1.0.typelib


%files devel
%{_libdir}/libmodulemd.so
%{_libdir}/pkgconfig/modulemd.pc
%{_includedir}/modulemd/
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Modulemd-1.0.gir
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/modulemd-1.0/


%files -n python%{python3_pkgversion}-%{name}


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.8.16-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 15 2019 Stephen Gallagher <sgallagh@redhat.com> - 1.8.16-1
- Improve the merge logic to handle third-party repos more sanely

* Tue Jul 30 2019 Stephen Gallagher <sgallagh@redhat.com> - 1.8.15-3
- Drop python2 subpackage

* Thu Jul 25 2019 Stephen Gallagher <sgallagh@redhat.com> - 1.8.15-2
- Fix Obsoletes

* Wed Jul 24 2019 Stephen Gallagher <sgallagh@redhat.com> - 1.8.15-1
- First separate release of libmodulemd1

