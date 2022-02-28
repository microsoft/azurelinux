Vendor:         Microsoft Corporation
Distribution:   Mariner
%bcond_without vmguestlib

Name: spausedd
Summary: Utility to detect and log scheduler pause
Version: 20201112
Release: 3%{?dist}
License: ISC
URL: https://github.com/jfriesse/spausedd
Source0: https://github.com/jfriesse/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz

# VMGuestLib exists only for x86 architectures
%if %{with vmguestlib}
%ifarch %{ix86} x86_64
%global use_vmguestlib 1
%endif
%endif

BuildRequires: gcc
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
make \
%if %{defined use_vmguestlib}
    WITH_VMGUESTLIB=1 \
%else
    WITH_VMGUESTLIB=0 \
%endif
    %{?_smp_mflags}

%install
make DESTDIR="%{buildroot}" PREFIX="%{_prefix}" install

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
* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20201112-3
- Removing the explicit %%clean stage.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20201112-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Nov 12 2020 Jan Friesse <jfriesse@redhat.com> - 20201112-1
- Add ability to move process into root cgroup
- Rebase to new version

* Tue Nov 10 2020 Jan Friesse <jfriesse@redhat.com> - 20201110-1
- Fix log_perror
- Enhance man page
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
