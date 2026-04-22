# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global         _firmwarepath    /usr/lib/firmware

Name:           wireless-regdb
Version:        2025.10.07
Release: 3%{?dist}
Summary:        Regulatory database for 802.11 wireless networking

License:        ISC
URL:            https://wireless.wiki.kernel.org/en/developers/regulatory/wireless-regdb
BuildArch:      noarch

Requires:       udev, iw
Requires:       systemd >= 190

BuildRequires:  make
BuildRequires:  systemd-devel

Provides:       crda = 3.18_2019.03.01-3
Obsoletes:      crda <= 3.18_2019.03.01-2

Source0:        http://www.kernel.org/pub/software/network/wireless-regdb/wireless-regdb-%{version}.tar.xz
Source1:        setregdomain
Source2:        setregdomain.1
Source3:        85-regulatory.rules


%description
The wireless-regdb package provides the regulatory rules database
used by the kernels 802.11 networking stack in order to comply 
with radio frequency regulatory rules around the world.


%prep
%autosetup -p1


%build
: # Package installs a firmware-like, prebuilt binary from upstream...


%install
make install DESTDIR=%{buildroot} MANDIR=%{_mandir} \
	FIRMWARE_PATH=%{_firmwarepath}

install -D -pm 0755 %SOURCE1 %{buildroot}%{_sbindir}/setregdomain
install -D -pm 0644 %SOURCE2 %{buildroot}%{_mandir}/man1/setregdomain.1
install -D -pm 0644 %SOURCE3 %{buildroot}%{_udevrulesdir}/85-regulatory.rules

rm -rf %{buildroot}/usr/lib/crda


%files
%{_sbindir}/setregdomain
%{_udevrulesdir}/85-regulatory.rules
%{_firmwarepath}/regulatory.db
%{_firmwarepath}/regulatory.db.p7s
%{_mandir}/man1/setregdomain.1*
%{_mandir}/man5/regulatory.db.5*
%{_mandir}/man5/regulatory.bin.5*
%license LICENSE
%doc README


%changelog
* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2025.10.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Sat Oct 11 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 2025.10.07-1
- Update to 2025.10.07

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2025.02.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Apr 22 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 2025.02.20-1
- Update to 2025.02.20

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2024.01.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2024.01.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Feb 01 2024 John W. Linville <linville@redhat.com> - 2024.01.23-1
- Update to version 2024.01.23 from upstream

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2023.09.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 05 2023 John W. Linville <linville@redhat.com> - 2023.09.01-1
- Update to version 2023.09.01 from upstream

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2023.05.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon May 15 2023 John W. Linville <linville@redhat.com> - 2023.05.03-1
- Update to version 2023.05.03 from upstream

* Mon Feb 13 2023 John W. Linville <linville@redhat.com> - 2023.02.13-1
- Update to version 2023.02.13 from upstream

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2022.08.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Aug 31 2022 John W. Linville <linville@redhat.com> - 2022.08.12-1
- Update to version 2022.08.12 from upstream

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2022.06.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 06 2022 John W. Linville <linville@redhat.com> - 2022.06.06-1
- Update to version 2022.06.06 from upstream

* Fri Apr 08 2022 John W. Linville <linville@redhat.com> - 2022.04.08-1
- Update to version 2022.02.18 from upstream

* Mon Feb 21 2022 John W. Linville <linville@redhat.com> - 2022.02.18-1
- Update to version 2022.02.18 from upstream

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2021.08.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Sep 01 2021 John W. Linville <linville@redhat.com> - 2021.08.28-1
- Update to version 2021.08.28 from upstream

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2021.07.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 14 2021 John W. Linville <linville@redhat.com> - 2021.07.14-1
- Update to version 2021.07.14 from upstream

* Tue May 11 2021 John W. Linville <linville@redhat.com> - 2020.04.21-1
- Update to version 2020.04.21 from upstream

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2020.11.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 09 2020 John W. Linville <linville@redhat.com> - 2020.11.20-1
- Update to version 2020.11.20 from upstream

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2020.04.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu May 21 2020 John W. Linville <linville@redhat.com> - 2020.04.29-1
- Update to version 2020.04.29 from upstream

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2019.06.03-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Aug 28 2019 John W. Linville <linville@redhat.com> - 2019.06.03-5
- Remove patch preventing install of regulatory.bin.5 man page
- Include regulatory.bin.5 man page in distributed files

* Mon Aug 26 2019 John W. Linville <linville@redhat.com> - 2019.06.03-4
- Bump crda Provides and Obsoletes to ensure proper upgrades

* Mon Aug 05 2019 John W. Linville <linville@redhat.com> - 2019.06.03-3
- remove Requires for kernel

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2019.06.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 06 2019 John W. Linville <linville@redhat.com> - 2019.06.03-1
- Update to version 2019.06.03 from upstream

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2018.05.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 02 2018 John W. Linville <linville@redhat.com> - 2018.05.31-4
- Enable Provides for crda so as to promote automated upgrades

* Wed Jul 18 2018 John W. Linville <linville@redhat.com> - 2018.05.31-3
- Fix-up changelog typos and bump Release

* Wed Jul 18 2018 John W. Linville <linville@redhat.com> - 2018.05.31-2
- Add BuildRequires for systemd-devel to provide _udevrulesdir definition

* Fri Jul 06 2018 John W. Linville <linville@redhat.com> - 2018.05.31-1
- Initial build
