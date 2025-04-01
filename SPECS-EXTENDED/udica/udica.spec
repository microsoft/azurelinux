Summary:        A tool for generating SELinux security policies for containers
Name:           udica
Version:        0.2.8
Release:        1%{?dist}
License:        GPLv3+
BuildArch:      noarch
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/containers/udica
Source0:        https://github.com/containers/udica/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

#git format-patch -N v0.2.8 -- . ':!.cirrus.yml' ':!.github'
Patch0001: 0001-Add-option-to-generate-custom-policy-for-a-confined-.patch
Patch0002: 0002-Add-tests-covering-confined-user-policy-generation.patch
Patch0003: 0003-confined-make-l-non-optional.patch
Patch0004: 0004-confined-allow-asynchronous-I-O-operations.patch

BuildRequires: python3 
BuildRequires: python3-devel
BuildRequires: python3-setuptools
Requires:      python3
Requires:      python3-libsemanage 
Requires:      python3-libselinux

%description
Tool for generating SELinux security profiles for containers based on
inspection of container JSON file.

%prep
%autosetup -p 1

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --single-version-externally-managed --root=%{buildroot}
install --directory %{buildroot}%{_datadir}/udica/macros
install --directory %{buildroot}%{_mandir}/man8
install -m 0644 udica/man/man8/udica.8 %{buildroot}%{_mandir}/man8/udica.8

%files
%{_mandir}/man8/udica.8*
%{_bindir}/udica
%dir %{_datadir}/udica
%dir %{_datadir}/udica/ansible
%dir %{_datadir}/udica/macros
%{_datadir}/udica/ansible/*
%{_datadir}/udica/macros/*
%license LICENSE
%{python3_sitelib}/udica/
%{python3_sitelib}/udica-*.egg-info


%changelog
* Thu Mar 06 2025 Jyoti Kanase <v-jykanase@microsoft.com> - 0.2.8-1
- Upgrade to 0.2.8
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.2.1-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 25 2019 Lukas Vrabec <lvrabec@redhat.com> - 0.2.1-1
- New rebase https://github.com/containers/udica/releases/tag/v0.2.1

* Wed Sep 25 2019 Lukas Vrabec <lvrabec@redhat.com> - 0.2.0-1
- New rebase https://github.com/containers/udica/releases/tag/v0.2.0

* Wed Aug 28 2019 Lukas Vrabec <lvrabec@redhat.com> - 0.1.9-1
- Update tests test_basic.podman.cil, test_basic.docker.cil. Round 2
- New rebase https://github.com/containers/udica/releases/tag/v0.1.9

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.1.8-3
- Rebuilt for Python 3.8

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 11 2019 Lukas Vrabec <lvrabec@redhat.com> - 0.1.8-1
- New rebase https://github.com/containers/udica/releases/tag/v0.1.8

* Wed Jun 12 2019 Lukas Vrabec <lvrabec@redhat.com> - 0.1.7-1
- New rebase with upstream adding new param --ansible, to generate ansible playbook for deploying policies. https://github.com/containers/udica/releases/tag/v0.1.7

* Thu May 16 2019 Lukas Vrabec <lvrabec@redhat.com> - 0.1.6-1
- New rebase with upstream adding new tests

* Tue Apr 30 2019 Lukas Vrabec <lvrabec@redhat.com> - 0.1.5-2
- Add allow rules for container_runtime_t to base_container.cil, Podman version 1.2.0 requires new allow rules.
* Fri Apr 19 2019 Lukas Vrabec <lvrabec@redhat.com> - 0.1.5-1
- Create mock selinux and semanage module
- Update testing section in README
- Add travis file for Travis CI
- Grammar fixes in the udica.8 manpage file
- Support port ranges (Resolves: #16)
- Test port ranges

* Mon Mar 11 2019 Lukas Vrabec <lvrabec@redhat.com> - 0.1.4-1
- Fix minor problems reported by pylint #11
- Catch FileNotFoundError when inspecting containers #12
- Create basic tests #13
- Restore working directory #14
- udica cannot use the container ID once it is provided #10

* Mon Feb 25 2019 Lukas Vrabec <lvrabec@redhat.com> - 0.1.3-4
- Update manpage with the latest known bug described in https://github.com/containers/udica/issues/8
- Add check if runtimes are installed on the system

* Sun Feb 17 2019 Lukas Vrabec <lvrabec@redhat.com> - 0.1.3-3
- Improve capability parsing for docker containers
- Update small changes in manpage, like issue with mandatory option '-c' for docker containers
- Fix parsing Mountpoints in docker inspect JSON file

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Lukas Vrabec <lvrabec@redhat.com> - 0.1.3-1
- Fix capability allow rules when capabilities are specified in JSON file
- Add additional SELinux allow rules to base container template to allow container to read proc_type types.

* Fri Jan 04 2019 Lukas Vrabec <lvrabec@redhat.com> - 0.1.2-1
- Fix invalid syntax output when policy is using just one template
Resolves: #6

* Tue Oct 23 2018 Lukas Vrabec <lvrabec@redhat.com> - 0.1.1-2
- Fix small issues in spec file like improve description and change files section.

* Mon Oct 22 2018 Lukas Vrabec <lvrabec@redhat.com> - 0.1.1-1
- Add proper shebang to all source files
- Add License to all source files

* Sat Oct 13 2018 Lukas Vrabec <lvrabec@redhat.com> - 0.1.0-1
- Add support for docker containers

* Mon Oct 08 2018 Lukas Vrabec <lvrabec@redhat.com> - 0.0.5-1
- Update x_container template based on testing container related to Nvidia Cuda operations

* Mon Oct 08 2018 Lukas Vrabec <lvrabec@redhat.com> - 0.0.4-2
- Build udica on Red Hat Enterprise Linux 7 with python version 2

* Mon Oct 08 2018 Lukas Vrabec <lvrabec@redhat.com> - 0.0.4-1
- Add manpages
- Add support for communicating with libvirt daemon
- Add support for communicating with X server.
- Add support for read/write to the controlling terminal

* Sun Oct 07 2018 Lukas Vrabec <lvrabec@redhat.com> - 0.0.3-1
- Remove required parameters -i or -j and added support for reading json file from stdin.
- Remove "-n" or "--name" parameter. Name of the container will be required for this tool

* Tue Sep 25 2018 Lukas Vrabec <lvrabec@redhat.com> - 0.0.2-1
- Use subprocess.Popen instead of subprocess.run for inspecting to support also python2

* Thu Sep 20 2018 Lukas Vrabec <lvrabec@redhat.com> - 0.0.1-3
- Update readme and setup.py files after migration to github

* Sun Sep 16 2018 Lukas Vrabec <lvrabec@redhat.com> - 0.0.1-2
- Update LICENSE
- Improve %%files section

* Sun Sep 16 2018 Lukas Vrabec <lvrabec@redhat.com> - 0.0.1-1
- Initial build
