# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# defining macros needed by SELinux
%global selinuxtype targeted
%global selinux_policyver 3.14.3-22
%global moduletype contrib
%global modulename tabrmd

Name: tpm2-abrmd-selinux
Version: 2.3.1
Release: 15%{?dist}
Summary: SELinux policies for tpm2-abrmd

License: BSD-2-Clause
URL:     https://github.com/tpm2-software/tpm2-abrmd
Source0: https://github.com/tpm2-software/tpm2-abrmd/archive/%{version}/tpm2-abrmd-%{version}.tar.gz

Patch0: selinux-allow-fwupd-to-communicate-with-tpm2-abrmd.patch

BuildArch: noarch
Requires: selinux-policy >= %{selinux_policyver}
BuildRequires: make
BuildRequires: git
BuildRequires: pkgconfig(systemd)
BuildRequires: selinux-policy
BuildRequires: selinux-policy-devel
BuildRequires: selinux-policy-%{selinuxtype}
Requires(post): selinux-policy-base >= %{selinux_policyver}
Requires(post): libselinux-utils
Requires(post): policycoreutils
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires(post): policycoreutils-python-utils
%else
Requires(post): policycoreutils-python
%endif

%description
SELinux policy modules for tpm2-abrmd.

%prep
%autosetup -p1 -n tpm2-abrmd-%{version}

%build
pushd selinux
make %{?_smp_mflags} TARGET="tabrmd" SHARE="%{_datadir}"
popd

%pre
%selinux_relabel_pre -s %{selinuxtype}

%install
# install policy modules
pushd selinux
install -d %{buildroot}%{_datadir}/selinux/packages
install -d -p %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}
install -p -m 644 %{modulename}.if %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}
install -m 0644 %{modulename}.pp.bz2 %{buildroot}%{_datadir}/selinux/packages
popd

%check

%post
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{modulename}.pp.bz2

%postun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename}
fi

%posttrans
%selinux_relabel_post -s %{selinuxtype}

%files
%license LICENSE
%{_datadir}/selinux/*
%{_datadir}/selinux/packages/%{modulename}.pp.bz2
%{_datadir}/selinux/devel/include/%{moduletype}/%{modulename}.if

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Feb 19 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 2.3.1-11
- Fix policycoreutils-python-utils dependency for RHEL 8+

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 26 2023 Štěpán Horáček <shoracek@redhat.com> - 2.3.1-9
- Migrate license to SPDX

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 12 2020 Javier Martinez Canillas <javierm@redhat.com> - 2.3.1-1
- Update to 2.3.1 release

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 08 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.1.0-2
- selinux: allow tpm2-abrmd to communicate with fwupd
  Resolves: rhbz#1665701

* Fri Feb 22 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.1.0-1
- Update to 2.1.0 release
- Add selinux-policy-%{selinuxtype} BuildRequires

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 04 2018 Javier Martinez Canillas <javierm@redhat.com> - 2.0.0-1
- Initial import (rhbz#1550595)
