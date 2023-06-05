%bcond_with tests
Vendor:         Microsoft Corporation
Distribution:   Mariner
## START: Set by rpmautospec
## (rpmautospec version 0.3.5)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%global pypi_version 23.5

Name:           python-virt-firmware
Version:        %{pypi_version}
Release:        2%{?dist}
Summary:        Tools for virtual machine firmware volumes

License:        GPLv2
URL:            https://pypi.org/project/virt-firmware/
Source0:        https://files.pythonhosted.org/packages/c2/f8/204dc513d2d3f0f3d3aead03600f7db1b763cf02998ad7b35e7ac5ef6849/virt-firmware-%{pypi_version}.tar.gz#/python-virt-firmware-%{pypi_version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(cryptography)
BuildRequires:  python3dist(setuptools)
BuildRequires:  make help2man

%description
Tools for ovmf / armvirt firmware volumes This is a small collection of tools
for edk2 firmware images. They support decoding and printing the content of
firmware volumes. Variable stores (OVMF_VARS.fd) can be modified, for example
to enroll secure boot certificates.

%package -n     python3-virt-firmware
Summary:        %{summary}
%{?python_provide:%python_provide python3-virt-firmware}
Provides:       virt-firmware
Requires:       python3dist(cryptography)
Requires:       python3dist(setuptools)
%description -n python3-virt-firmware
Tools for ovmf / armvirt firmware volumes This is a small collection of tools
for edk2 firmware images. They support decoding and printing the content of
firmware volumes. Variable stores (OVMF_VARS.fd) can be modified, for example
to enroll secure boot certificates.

%package -n     python3-virt-firmware-peutils
Summary:        %{summary} - peutils
Requires:       python3dist(pefile)
Conflicts:      python3-virt-firmware < 1.6
%description -n python3-virt-firmware-peutils
Some utilities to inspect efi (pe) binaries.

%if %{with tests}
%package -n     python3-virt-firmware-tests
Summary:        %{summary} - test cases
Requires:       python3-virt-firmware
Requires:       python3dist(pytest)
Requires:       edk2-ovmf
%description -n python3-virt-firmware-tests
test cases
%endif

%prep
%autosetup -n virt-firmware-%{pypi_version}

%build
%py3_build

%install
%py3_install
# manpages
install -m 755 -d      %{buildroot}%{_mandir}/man1
install -m 644 man/*.1 %{buildroot}%{_mandir}/man1

# tests
%if %{with tests}
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -ar tests %{buildroot}%{_datadir}/%{name}
%endif

%files -n python3-virt-firmware
%license LICENSE
%doc README.md experimental
%{_bindir}/host-efi-vars
%{_bindir}/virt-fw-dump
%{_bindir}/virt-fw-vars
%{_bindir}/virt-fw-sigdb
%{_bindir}/migrate-vars
%{_mandir}/man1/virt-*.1*
%{python3_sitelib}/virt/firmware
%{python3_sitelib}/virt_firmware-%{pypi_version}-py%{python3_version}.egg-info

%files -n python3-virt-firmware-peutils
%{python3_sitelib}/virt/peutils
%{_bindir}/pe-dumpinfo
%{_bindir}/pe-listsigs
%{_bindir}/pe-addsigs

%if %{with tests}
%files -n python3-virt-firmware-tests
%{_datadir}/%{name}/tests
%endif

%changelog
* Fri Jun 02 2023 Vince Perri <viperri@microsoft.com> - 23.5-2
- License verified.
- Initial CBL-Mariner import from Fedora 39 (license: MIT).

* Thu May 04 2023 Gerd Hoffmann <kraxel@redhat.com> - 23.5-1
- update to version 23.5

* Fri Apr 14 2023 Gerd Hoffmann <kraxel@redhat.com> - 23.4-1
- update to version 23.4

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Gerd Hoffmann <kraxel@redhat.com> - 1.8-1
- update to version 1.8

* Fri Dec 02 2022 Gerd Hoffmann <kraxel@redhat.com> - 1.7-1
- update to version 1.7

* Thu Nov 10 2022 Gerd Hoffmann <kraxel@redhat.com> - 1.6-2
- add conflict declaration

* Thu Nov 10 2022 Gerd Hoffmann <kraxel@redhat.com> - 1.6-1
- update to version 1.6
- split peutils to subpackage

* Wed Oct 05 2022 Gerd Hoffmann <kraxel@redhat.com> - 1.5-1
- update to version 1.5

* Wed Oct 05 2022 Gerd Hoffmann <kraxel@redhat.com> - 1.4-5
- turn on gating

* Wed Oct 05 2022 Gerd Hoffmann <kraxel@redhat.com> - 1.4-4
- more test dependency tweaks

* Wed Oct 05 2022 Gerd Hoffmann <kraxel@redhat.com> - 1.4-3
- tweak test dependencies

* Wed Oct 05 2022 Gerd Hoffmann <kraxel@redhat.com> - 1.4-2
- add tests

* Tue Sep 27 2022 Gerd Hoffmann <kraxel@redhat.com> - 1.4-1
- update to version 1.4
- add man-pages
- add tests sub-package

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 18 2022 Gerd Hoffmann <kraxel@redhat.com> - 1.2-1
- update to version 1.2

* Fri Jul 01 2022 Gerd Hoffmann <kraxel@redhat.com> - 1.1-1
- update to version 1.1

* Wed Jun 22 2022 Gerd Hoffmann <kraxel@redhat.com> - 1.0-1
- update to version 1.0

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.98-2
- Rebuilt for Python 3.11

* Tue May 24 2022 Gerd Hoffmann <kraxel@redhat.com> - 0.98-1
- update to version 0.98

* Mon Apr 11 2022 Gerd Hoffmann <kraxel@redhat.com> - 0.95-1
- Initial package.

