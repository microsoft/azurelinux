# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           open-vmdk
Version:        0.3.12
Release:        1%{?dist}
Summary:        Tools to create OVA files from raw disk images
License:        Apache-2.0
URL:            https://github.com/vmware/open-vmdk
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  python3-devel
BuildRequires:  zlib-devel
Requires:       coreutils
Requires:       grep
Requires:       python3-PyYAML
Requires:       python3-lxml
Requires:       sed
Requires:       tar
Requires:       util-linux

%description
Open VMDK is an assistant tool for creating Open Virtual Appliance (OVA).
An OVA is a tar archive file with Open Virtualization Format (OVF) files
inside, which is composed of an OVF descriptor with extension .ovf,
one or more virtual machine disk image files with extension .vmdk,
and a manifest file with extension .mf.

%files
%{_bindir}/mkova.sh
%{_bindir}/ova-compose
%{_bindir}/vmdk-convert
%{_datadir}/%{name}/
%config(noreplace) %{_sysconfdir}/open-vmdk.conf

%dnl ---------------------------------------------------------------------

%package -n ovfenv
Summary:       Tools to get or set OVF environment variables
Requires:      open-vm-tools
Requires:      python3-libxml2
BuildArch:     noarch

%description -n ovfenv
Show the value of an OVF property, whether the properties
were presented to this VM in guestinfo or on a cdrom.
Optionally, allows a property value to be modified.

%files -n ovfenv
%{_bindir}/ovfenv
%dir %{_sharedstatedir}/ovfenv


%dnl ---------------------------------------------------------------------

%prep
%autosetup -p1


%build
%{!?_auto_set_build_flags:%{set_build_flags}}
%make_build


%install
%make_install

# Fix shebang for ovfenv
%py3_shebang_fix %{buildroot}%{_bindir}/ovfenv

install -m0644 templates/*.ovf %{buildroot}%{_datadir}/%{name}
install -d -m 755 %{buildroot}%{_sharedstatedir}/ovfenv


%changelog
* Tue Jan 20 2026 Neal Gompa <ngompa@fedoraproject.org> - 0.3.12-1
- Update to 0.3.12

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Mar 08 2024 İsmail Dönmez <ismail@i10z.com> - 0.3.8-1
- Bump to version 0.3.8

* Sat Feb 03 2024 İsmail Dönmez <ismail@i10z.com> - 0.3.7-1
- Bump to version 0.3.7
  Drop honor-build-flags.patch, merged upstream

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 28 2023 Ismail Doenmez <ismail@i10z.com> - 0.3.6-1
- Initial build for 0.3.6
