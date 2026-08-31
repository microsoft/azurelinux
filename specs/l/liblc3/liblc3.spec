# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:          liblc3
Version:       1.1.3
Release:       5%{?dist}
Summary:       Low Complexity Communication Codec (LC3)

License:       Apache-2.0
URL:           https://github.com/google/liblc3
Source0:       %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:        0001-Revert-build-fix-rpath-issue.patch

BuildRequires: gcc
BuildRequires: meson
BuildRequires: python3-devel

%description
The Low Complexity Communication Codec (LC3) is used by
Bluetooth as the codec for LE Audio. It enables high
quality audio over the low bandwidth connections provided
by Bluetooth LE.

%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with %{name}.

%package -n python3-lc3
Summary: Python3 bindings for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description -n python3-lc3
Python3 bindings for %{name}.

%package utils
Summary: Utility package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description utils
Uitlities for command line use of and testing
the %{name} library.

%prep
%autosetup -p1

%build
%meson -Dtools=true -Dpython=true
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license LICENSE
%{_libdir}/liblc3.so.1{,.*}

%files devel
%{_includedir}/lc3*
%{_libdir}/pkgconfig/lc3.pc
%{_libdir}/liblc3.so

%files -n python3-lc3
%{python3_sitelib}/*

%files utils
%{_bindir}/dlc3
%{_bindir}/elc3

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.1.3-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.1.3-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.1.3-2
- Rebuilt for Python 3.14

* Thu Feb 13 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 1.1.3-1
- Update to 1.1.3

* Mon Feb 03 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.1.1-2
- Rebuilt for Python 3.13

* Sun Apr 21 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1

* Sat Mar 30 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0
- Enable new python bindings

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 13 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.4-2
- Review fixes

* Fri Aug 04 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4
- Review updates
- Split utils out to subpackage

* Thu Jun 22 2023 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.3-1
- Initial package
