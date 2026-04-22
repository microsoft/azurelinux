# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global debug_package %{nil}

Name:           eglexternalplatform
Version:        1.2.1
Release: 3%{?dist}
Summary:        EGL External Platform Interface headers
License:        MIT
URL:            https://github.com/NVIDIA
BuildArch:      noarch

Source0:        %url/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  meson

%description
%summary

%package        devel
Summary:        Development files for %{name}

%description    devel
The %{name}-devel package contains the header files for
developing applications that use %{name}.

%prep
%autosetup

%build
%meson

%install
%meson_install

%files devel
%doc README.md samples
%license COPYING
%{_includedir}/*
%{_datadir}/pkgconfig/eglexternalplatform.pc

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Mar 27 2025 Simone Caronni <negativo17@gmail.com> - 1.2.1-1
- Update to 1.2.1.
- Trim changelog.

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Simone Caronni <negativo17@gmail.com> - 1.2-2
- Adjust path of generated pkg-config file so it's still considered noarch.

* Thu Aug 08 2024 Simone Caronni <negativo17@gmail.com> - 1.2-1
- Update to 1.2.

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
