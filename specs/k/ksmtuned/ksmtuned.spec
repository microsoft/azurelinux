# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: ksmtuned
Version: 0.1.0
Release: 17%{?dist}

Summary: Kernel Samepage Merging services
License: GPL-2.0-or-later
URL: https://github.com/ksmtuned/ksmtuned
Source0: https://github.com/ksmtuned/ksmtuned/archive/v%{version}/ksmtuned-%{version}.tar.gz

# Package was originally 'ksm' as a subpackage of 'qemu'
Obsoletes: ksm < 3.0.0-0.2

BuildRequires: gcc
BuildRequires: meson
%{?systemd_requires}
BuildRequires: systemd


%description
Kernel Samepage Merging (KSM) is a memory-saving de-duplication feature,
that merges anonymous (private) pages (not pagecache ones).

This package provides service files for disabling (ksm) and tuning
(ksmtuned)


%prep
%autosetup -p1


%build
%meson \
    -Dredhat-sysconfig=true
%meson_build


%install
%meson_install


%post
%systemd_post ksm.service
%systemd_post ksmtuned.service
%preun
%systemd_preun ksm.service
%systemd_preun ksmtuned.service
%postun
%systemd_postun_with_restart ksm.service
%systemd_postun_with_restart ksmtuned.service


%files
%license COPYING
%{_libexecdir}/ksmctl
%{_sbindir}/ksmtuned
%{_unitdir}/ksmtuned.service
%{_unitdir}/ksm.service
%config(noreplace) %{_sysconfdir}/ksmtuned.conf
%config(noreplace) %{_sysconfdir}/sysconfig/ksm


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.1.0-7
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 13 2018 Cole Robinson <crobinso@redhat.com> - 0.1.0-1
- Initial package
