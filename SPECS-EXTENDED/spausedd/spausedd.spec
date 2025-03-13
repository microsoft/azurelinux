Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%bcond_without vmguestlib

Name: spausedd
Summary: Utility to detect and log scheduler pause
Version: 20210719
Release: 10%{?dist}
License: ISC
URL: https://github.com/jfriesse/spausedd
Source0: https://github.com/jfriesse/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz

%global use_vmguestlib 0

BuildRequires: gcc
BuildRequires: make
%{?systemd_requires}
BuildRequires: systemd

%if %{defined use_vmguestlib}
BuildRequires: pkgconfig(vmguestlib)
%endif

%description
Utility to detect and log scheduler pause

%prep
%setup -q -n %{name}-%{version}

%build
%set_build_flags
%make_build \
%if %{defined use_vmguestlib}
    WITH_VMGUESTLIB=1 \
%else
    WITH_VMGUESTLIB=0 \
%endif

%install
%make_install PREFIX="%{_prefix}"

mkdir -p %{buildroot}/%{_unitdir}
install -m 644 -p init/%{name}.service %{buildroot}/%{_unitdir}

%files
%doc AUTHORS
%license COPYING
%{_bindir}/%{name}
%{_mandir}/man8/*
%{_unitdir}/spausedd.service

%post
%systemd_post spausedd.service

%preun
%systemd_preun spausedd.service

%postun
%systemd_postun spausedd.service

%changelog
* Fri Jan 10 2025 Archana Shettigar <v-shettigara@microsoft.com> - 20210719-10
- Initial Azure Linux import from Fedora 41 (license: MIT).
- Removing the explicit %%clean stage.
- License verified.

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20210719-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20210719-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20210719-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 06 2023 Jan Friesse <jfriesse@redhat.com> - 20210719-6
- migrated to SPDX license

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20210719-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20210719-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20210719-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20210719-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Jan Friesse <jfriesse@redhat.com> - 20210719-1
- Add mode option for moving to root cgroup functionality

* Thu May 20 2021 Jan Friesse <jfriesse@redhat.com> - 20210520-1
- Document cgroup v2 problems

* Tue May 11 2021 Jan Friesse <jfriesse@redhat.com> - 20210511-1
- Support for cgroup v2

* Fri Mar 26 2021 Jan Friesse <jfriesse@redhat.com> - 20210326-1
- Fix possible memory leak
- Check memlock rlimit

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20201112-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 12 2020 Jan Friesse <jfriesse@redhat.com> - 20201112-1
- Add ability to move process into root cgroup
- Rebase to new version

* Tue Nov 10 2020 Jan Friesse <jfriesse@redhat.com> - 20201110-1
- Fix log_perror
- Rebase to new version

* Tue Sep 22 2020 Jan Friesse <jfriesse@redhat.com> - 20200323-4
- Fix build for ELN

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200323-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Jan Friesse <jfriesse@redhat.com> - 20200323-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Mon Mar 23 2020 Jan Friesse <jfriesse@redhat.com> - 20200323-1
- Enhance man page
- Add CI tests
- Enable gating
- Rebase to new version

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20190807-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Aug 07 2019 Jan Friesse <jfriesse@redhat.com> - 20190807-1
- Enhance makefile
- Rebase to new version

* Tue Aug 06 2019 Jan Friesse <jfriesse@redhat.com> - 20190320-3
- Do not set exec permission for service file

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20190320-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 20 2019 Jan Friesse <jfriesse@redhat.com> - 20190320-1
- Use license macro in spec file

* Tue Mar 19 2019 Jan Friesse <jfriesse@redhat.com> - 20190319-1
- Add AUTHORS and COPYING
- Fix version number in specfile
- Use install -p to preserve timestamps
- Use set_build_flags macro
- Rebase to new version

* Mon Mar 18 2019 Jan Friesse <jfriesse@redhat.com> - 20190318-2
- Initial version for Fedora

* Mon Mar 18 2019 Jan Friesse <jfriesse@redhat.com> - 20190318-1
- Require VMGuestLib only on x86 and x86_64

* Wed Mar 21 2018 Jan Friesse <jfriesse@redhat.com> - 20180321-1
- Remove exlusivearch for VMGuestLib.
- Add copr branch with enhanced spec file which tries to automatically
  detect what build options should be used (systemd/vmguestlib).

* Tue Mar 20 2018 Jan Friesse <jfriesse@redhat.com> - 20180320-1
- Add support for VMGuestLib
- Add more examples

* Mon Feb 19 2018 Jan Friesse <jfriesse@redhat.com> - 20180219-1
- Add support for steal time

* Fri Feb 9 2018 Jan Friesse <jfriesse@redhat.com> - 20180209-1
- Initial version
