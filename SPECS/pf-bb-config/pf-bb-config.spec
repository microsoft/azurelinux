# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           pf-bb-config
Version:        24.07
Release:        3%{?dist}
Summary:        PF BBDEV (baseband device) Configuration Application

License:        Apache-2.0
URL:            https://github.com/intel/pf-bb-config
Source0:        %{url}/archive/v%{version}/pf-bb-config-%{version}.tar.gz

# Currently big endian is not supported due to a bug
ExcludeArch:    s390x

BuildRequires:  gcc
BuildRequires:  make


%description
The PF BBDEV (baseband device) Configuration Application "pf_bb_config"
provides a means to configure the baseband device at the host-level.
The program accesses the configuration space and sets the various parameters
through memory-mapped IO read/writes.


%prep
%autosetup -p1
sed -i "s/#VERSION_STRING#/%{version}/g" config_app.c


%build
%make_build CFLAGS="${RPM_OPT_FLAGS}" LDFLAGS="${RPM_LD_FLAGS}"


%install
for dir in acc100 agx100 fpga_5gnr fpga_lte vrb1 vrb2; do
	install -d -m 755 %{buildroot}%{_datadir}/pf-bb-config/$dir/
	cp -a $dir/*.cfg %{buildroot}%{_datadir}/pf-bb-config/$dir/
done
install -d -m 755 %{buildroot}%{_bindir}
install -p -D -m 755 pf_bb_config %{buildroot}%{_bindir}/pf_bb_config


%files
%license LICENSE
%doc README.md
%{_bindir}/pf_bb_config
%{_datadir}/pf-bb-config/


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 24.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 24.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Sep 27 2024 Timothy Redaelli <tredaelli@redhat.com> - 24.07-1
- Update to 24.07

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 22.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 22.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 22.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 22.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Mar 03 2023 Maxime Coquelin <maxime.coquelin@redhat.com> - 22.11-3
- Add missing ACC200 (VRB1) data files

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 22.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Timothy Redaelli <tredaelli@redhat.com> - 22.11-1
- Update to 22.11

* Mon Oct 03 2022 Timothy Redaelli <tredaelli@redhat.com> - 22.07-1
- Initial import (fedora#2101769)
