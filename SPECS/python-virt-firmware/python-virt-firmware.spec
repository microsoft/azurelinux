%bcond_with tests
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
## START: Set by rpmautospec
## (rpmautospec version 0.3.5)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%global pypi_version 24.4

Name:           python-virt-firmware
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:        Tools for virtual machine firmware volumes

License:        GPL-2.0-only
URL:            https://pypi.org/project/virt-firmware/
Source0:        https://files.pythonhosted.org/packages/ea/8d/b3417567c9b532879357fb2b6b6fc50a6b0b311f95b16b4845054852e062/virt-firmware-%{pypi_version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(cryptography)
BuildRequires:  python3dist(setuptools)
BuildRequires:  make help2man
BuildRequires:  systemd systemd-rpm-macros

%description
Tools for ovmf / armvirt firmware volumes This is a small collection of tools
for edk2 firmware images. They support decoding and printing the content of
firmware volumes. Variable stores (OVMF_VARS.fd) can be modified, for example
to enroll secure boot certificates.

%package -n     python3-virt-firmware
Summary:        %{summary}
%{?python_provide:%python_provide python3-virt-firmware}
Provides:       virt-firmware
Conflicts:      python3-virt-firmware-peutils < 23.9
Obsoletes:      python3-virt-firmware-peutils < 23.9
Requires:       python3dist(cryptography)
Requires:       python3dist(setuptools)
Requires:       python3dist(pefile)
%description -n python3-virt-firmware
Tools for ovmf / armvirt firmware volumes This is a small collection of tools
for edk2 firmware images. They support decoding and printing the content of
firmware volumes. Variable stores (OVMF_VARS.fd) can be modified, for example
to enroll secure boot certificates.

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
%{_bindir}/pe-dumpinfo
%{_bindir}/pe-listsigs
%{_bindir}/pe-addsigs
%{_bindir}/pe-inspect
%{_mandir}/man1/virt-*.1*
%{python3_sitelib}/virt/firmware
%{python3_sitelib}/virt/peutils
%{python3_sitelib}/virt_firmware-%{pypi_version}-py%{python3_version}.egg-info

%if %{with tests}
%files -n python3-virt-firmware-tests
%{_datadir}/%{name}/tests
%endif

%changelog
* Mon May 13 2024 Elaine Zhao <elainezhao@microsoft.com> - 24.4-1
- update to version 24.4

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

