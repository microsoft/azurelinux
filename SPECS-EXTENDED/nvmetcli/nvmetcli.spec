Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           nvmetcli
License:        Apache-2.0
Summary:        An adminstration shell for NVMe storage targets
Version:        0.7
Release:        1%{?dist}
URL:            ftp://ftp.infradead.org/pub/nvmetcli/
Source:         ftp://ftp.infradead.org/pub/nvmetcli/%{name}-%{version}.tar.gz
Patch00:        0001-nvmetcli-don-t-remove-ANA-Group-1-on-clear.patch
Patch01:        0002-README-Update-URL-for-configshell-fb.patch
Patch02:        0003-nvmetcli-Improve-IOError-handling-on-restore.patch
Patch03:        0004-nvme.py-Explicit-close-is-redundant.patch
Patch04:        0005-nvme.py-Sync-the-containing-directory.patch
Patch05:        0006-nvme.py-Make-modprobe-work-for-kmod-lib-too.patch
Patch06:        0007-test_nvmet.py-test_invalid_input-fails-for-py3.patch
Patch07:        0008-nvmetcli-Report-save-name-correctly.patch
Patch08:        0009-nvmetcli-Allow-different-devices-for-make-test.patch
Patch09:        0010-nvmetcli-Correct-xrange-usage-for-py3.patch
Patch10:        0011-nvmetcli-add-a-tcp-example-json.patch
Patch11:        0012-Documentation-fix-typo.patch
BuildArch:      noarch
BuildRequires: make
BuildRequires:  python3-devel python3-setuptools systemd-units asciidoc xmlto
Requires:       python3-configshell python3-kmod
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
This package contains the command line interface to the NVMe over Fabrics
nvmet in the Linux kernel.  It allows configuring the nvmet interactively
as well as saving / restoring the configuration to / from a json file.

%prep
%autosetup -p1

%build
%{__python3} setup.py build
cd Documentation
make
gzip --stdout nvmetcli.8 > nvmetcli.8.gz

%install
%{__python3} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/nvmet
install -m 644 nvmet.service %{buildroot}%{_unitdir}/nvmet.service
mkdir -p %{buildroot}%{_mandir}/man8/
install -m 644 Documentation/nvmetcli.8.gz %{buildroot}%{_mandir}/man8/

%post
%systemd_post nvmet.service

%preun
%systemd_preun nvmet.service

%postun
%systemd_postun_with_restart nvmet.service

%files
%{python3_sitelib}/*
%dir %{_sysconfdir}/nvmet
%{_sbindir}/nvmetcli
%{_unitdir}/nvmet.service
%doc README
%license COPYING
%{_mandir}/man8/nvmetcli.8.gz

%changelog
* Thu Dec 19 2024 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 0.7-1
- Update to 0.7
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.4-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4-9
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4-8
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.4-4
- Rebuilt for Python 3.7

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 9 2017 Andy Grover <agrover@redhat.com> - 0.4-1
- Update for new upstream release
- Remove fix-setup.patch

* Tue Feb 21 2017 Andy Grover <agrover@redhat.com> - 0.3-1
- Update for new upstream release

* Wed Oct 12 2016 Andy Grover <agrover@redhat.com> - 0.2-1
- Initial packaging
