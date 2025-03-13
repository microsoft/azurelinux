Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           meanwhile
Version:        1.1.1
Release:        8%{?dist}
Summary:        Lotus Sametime Community Client library
License:        LGPL-3.0
URL:            https://github.com/obriencj/%{name}

Source:         %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         %{name}-file-transfer.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  doxygen
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconfig(glib-2.0) >= 2.0.0

%description
The heart of the %{name} Project is the %{name} library, providing the basic
Lotus Sametime session functionality along with the core services; Presence
Awareness, Instant Messaging, Multi-user Conferencing, Preferences Storage,
Identity Resolution, and File Transfer.

%package devel
Summary:        Header files, libraries and development documentation for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       glib2-devel

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name}, you
will need to install %{name}-devel.

%package doc
Summary:        Documentation for the %{name} library
License:        GFDL
BuildArch:      noarch

%description doc
Documentation for the %{name} library.

%prep
%autosetup -p1

%build
export CFLAGS="%{optflags} -fno-tree-vrp"
autoreconf -vif
%configure --enable-doxygen
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

# Prepare documents for inclusion through %%doc in the %%files section
mkdir docs
mv %{buildroot}%{_datadir}/doc/%{name}-doc-%{version}/{html,samples} docs
rm -rf %{buildroot}%{_datadir}/doc/%{name}-doc-%{version}/

%ldconfig_scriptlets libs

%files
%license COPYING
%doc AUTHORS ChangeLog README TODO LICENSE
%{_libdir}/lib%{name}.so.*

%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%files doc
%doc docs/*

%changelog
* Tue Dec 31 2024 Aninda Pradhan <v-anipradhan@microsoft.com> - 1.1.1-8
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified.

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 28 2022 Simone Caronni <negativo17@gmail.com> - 1.1.1-1
- Update to 1.1.1.
- Clean up SPEC file.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
