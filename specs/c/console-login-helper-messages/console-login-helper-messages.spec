# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global github_owner    coreos
%global github_project  console-login-helper-messages

Name:           console-login-helper-messages
Version:        0.21.3
Release: 12%{?dist}
Summary:        Combines motd, issue, profile features to show system information to the user before/on login
License:        BSD-3-Clause
URL:            https://github.com/%{github_owner}/%{github_project}
Source0:        https://github.com/%{github_owner}/%{github_project}/archive/v%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  systemd make
%{?systemd_requires}
Requires:       bash systemd

%description
%{summary}.

%package motdgen
Summary:        Message of the day generator script showing system information
Requires:       console-login-helper-messages
# sshd reads /run/motd.d, where the generated MOTD message is written.
Recommends:     openssh
# bash: bash scripts are included in this package
# systemd: systemd service units, and querying for failed units
# (the above applies to the issuegen and profile subpackages too)
Requires:       bash systemd
# setup: filesystem paths need setting up.
#   * https://pagure.io/setup/pull-request/14
#   * https://pagure.io/setup/pull-request/15
#   * https://pagure.io/setup/pull-request/16
# Make exception for fc29 - soft requires as we will create /run/motd.d
# ourselves if it doesn't already exist.
%if 0%{?fc29}
Requires:       setup
%else
Requires:       setup >= 2.12.7-1
%endif
# pam: to display motds in /run/motd.d.
#   * https://github.com/linux-pam/linux-pam/issues/47
#   * https://github.com/linux-pam/linux-pam/pull/69
#   * https://github.com/linux-pam/linux-pam/pull/76
Requires:       ((pam >= 1.3.1-15) if openssh)
# selinux-policy: to apply pam_var_run_t contexts:
#   * https://github.com/fedora-selinux/selinux-policy/pull/244
# Make exception for fc29, as PAM will create the tmpfiles. (In Fedora 30 and
# above, setup is responsible for this).
%if 0%{?fc29}
Requires:       ((selinux-policy >= 3.14.2-50) if openssh)
%else
Requires:       ((selinux-policy >= 3.14.3-23) if openssh)
%endif
# Needed to display MOTDs in `/run/motd.d` before upon login through 
# the serial console.
Requires:       util-linux >= 2.36-1

%description motdgen
%{summary}.

%package issuegen
Summary:        Issue generator scripts showing SSH keys and IP address
Requires:       console-login-helper-messages
Requires:       bash systemd setup
# NetworkManager: for displaying IP info using NetworkManager dispatcher script
Requires:       (NetworkManager)
Requires:       /etc/issue.d
# Needed to display issues in /etc/issue.d before login through the serial console.
Requires:       util-linux >= 2.36-1

%description issuegen
%{summary}.

%package profile
Summary:        Profile script showing systemd failed units
Requires:       console-login-helper-messages
Requires:       bash systemd setup

%description profile
%{summary}.

%prep
%autosetup -p1

%build

%install
make install DESTDIR=%{buildroot}
# /run/motd.d is now provided by the setup package on Fedora
rm %{buildroot}/%{_tmpfilesdir}/%{name}-motdgen.conf

%post issuegen
%systemd_post %{name}-gensnippet-ssh-keys.service

%preun issuegen
%systemd_preun %{name}-gensnippet-ssh-keys.service

%postun issuegen
%systemd_postun_with_restart %{name}-gensnippet-ssh-keys.service

%post motdgen
%systemd_post %{name}-gensnippet-os-release.service

%preun motdgen
%systemd_preun %{name}-gensnippet-os-release.service

%postun motdgen
%systemd_postun_with_restart %{name}-gensnippet-os-release.service

# TODO: %%check

%files
%doc README.md
%doc doc/manual.md
%license LICENSE
%dir %{_libexecdir}/%{name}
%dir %{_prefix}/lib/%{name}
%dir %{_prefix}/share/%{name}
%{_prefix}/lib/%{name}/libutil.sh
%{_tmpfilesdir}/%{name}.conf

%files issuegen
%{_unitdir}/%{name}-gensnippet-ssh-keys.service
%{_sysconfdir}/NetworkManager/dispatcher.d/90-%{name}-gensnippet_if
%{_prefix}/lib/%{name}/issue.defs
%{_tmpfilesdir}/%{name}-issuegen.conf
%{_libexecdir}/%{name}/gensnippet_ssh_keys
%{_libexecdir}/%{name}/gensnippet_if
%{_libexecdir}/%{name}/gensnippet_if_udev

%files motdgen
%{_unitdir}/%{name}-gensnippet-os-release.service
%{_prefix}/lib/%{name}/motd.defs
%{_libexecdir}/%{name}/gensnippet_os_release

%files profile
%{_prefix}/share/%{name}/profile.sh
%{_tmpfilesdir}/%{name}-profile.conf
%ghost %{_sysconfdir}/profile.d/%{name}-profile.sh

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 01 2023 Dusty Mabe <dusty@dustymabe.com> - 0.21.3-5
- Switch License tags to SPDX

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Sep 13 2022 Timothée Ravier <tim@siosm.fr> - 0.21.3-3
- Remove tpmfiles config for /run/motd.d (now provided by the setup package)
  (fedora#2120544)

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Dusty Mabe <dusty@dustymabe.com> - 0.21.3-1
- Update to 0.21.3

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 29 2021 Kelvin Fan <kfan@redhat.com> - 0.21.2-3
- Remove requirement for `fedora-release` and require `/etc/issue.d`

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 30 2021 Kelvin Fan <kfan@redhat.com> - 0.21.2-1
- Update to 0.21.2

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.21.1-3
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Thu Feb 18 2021 Kelvin Fan <kfan@redhat.com> - 0.21.1-2
- Make scripts subpackage-specific, addresses #1929844

* Fri Feb 5 2021 Kelvin Fan <kfan@redhat.com> - 0.21.1-1
- Update to 0.21.1

* Thu Feb 4 2021 Kelvin Fan <kfan@redhat.com> - 0.21-1
- Update to 0.21
- Require util-linux >= 2.36-1
- Remove files related to the issuegen and motdgen executables

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 23 2020 Kelvin Fan <kfan@redhat.com> - 0.20.3-1
- Update to 0.20.3

* Fri Oct 30 2020 Kelvin Fan <kfan@redhat.com> - 0.20.2-1
- Update to 0.20.2

* Fri Oct 2 2020 Kelvin Fan <kfan@redhat.com> - 0.20.1-1
- Update to 0.20.1

* Fri Sep 25 2020 Kelvin Fan <kfan@redhat.com> - 0.2-1
- Update to 0.2
- Add presets for `.service` units
- %%ghost symlinks defined in tmpfiles.d directory

* Fri Sep 18 2020 Kelvin Fan <kfan@redhat.com> - 0.19-2
- BuildRequire `make`
- Remove preinstall scripts

* Tue Sep 08 2020 Kelvin Fan <kfan@redhat.com> - 0.19-1
- Update to 0.19
- Invoke make install
- Remove -motdgen.service, -issuegen.service presets
- Require NetworkManager or systemd-udev

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 06 2020 Robert Fairley <rfairley@redhat.com> - 0.18.2-1
- Update to 0.18.2

* Thu Apr 30 2020 Robert Fairley <rfairley@redhat.com> - 0.18.1-1
- Update to 0.18.1

* Tue Apr 28 2020 Robert Fairley <rfairley@redhat.com> - 0.18-1
- Update to 0.18
- Change github_owner to coreos

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 16 2019 Robert Fairley <rfairley@redhat.com> - 0.17-1
- Update to 0.17
- Add manual.md to package docs
- Use tmpfiles_create_pkg macro

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 21 2019 Robert Fairley <rfairley@redhat.com> - 0.16-3
- Specfile tidyups (comments, formatting), and remove fc28 conditionals

* Fri Mar 22 2019 Robert Fairley <rfairley@redhat.com> - 0.16-2
- Add condition for f28 setup Requires

* Thu Mar 21 2019 Robert Fairley <rfairley@redhat.com> - 0.16-1
- relax setup dependency for f29
- general upstream source/tidiness improvements
- house executable scripts in /usr/libexec
- change Source0 to use GitHub-generated archive link
- drop .path units for motdgen and issuegen

* Fri Mar 15 2019 Robert Fairley <rfairley@redhat.com> - 0.15-1
- make motdgen generate motd in /run with no symlink

* Fri Mar 15 2019 Robert Fairley <rfairley@redhat.com> - 0.14-1
- issuegen.service: rely on sshd-keygen.target
- issuegen: don't show kernel version

* Thu Jan 24 2019 Robert Fairley <rfairley@redhat.com> - 0.13-4
- update reviewers.md and manual.md with correct paths

* Wed Jan 23 2019 Robert Fairley <rfairley@redhat.com> - 0.13-3
- change generated issue to be scoped in private directory

* Wed Jan 23 2019 Robert Fairley <rfairley@redhat.com> - 0.13-2
- change generated motd to be scoped in private directory

* Wed Jan 23 2019 Robert Fairley <rfairley@redhat.com> - 0.13-1
- add a symlink for motdgen (quick solution until upstream pam_motd.so changes propagate)

* Fri Jan 18 2019 Robert Fairley <rfairley@redhat.com> - 0.12-2
- fix Requires for selinux-policy, add missing Requires for systemd-udev and fedora-release

* Wed Jan 16 2019 Robert Fairley <rfairley@redhat.com> - 0.12-1
- fix specfile Source0 to correct github URL

* Wed Jan 16 2019 Robert Fairley <rfairley@redhat.com> - 0.11-1
- add reviewers.md, specfile fixes

* Wed Jan 16 2019 Robert Fairley <rfairley@redhat.com> - 0.1-12
- add move README.md sections out into a manual, update specfile

* Wed Jan 09 2019 Robert Fairley <rfairley@redhat.com> - 0.1-11
- specfile cleanup, go through git commit history to write changelog

* Wed Jan 09 2019 Robert Fairley <rfairley@redhat.com> - 0.1-10
- Add license, tidyups

* Mon Dec 10 2018 Robert Fairley <rfairley@redhat.com> - 0.1-9
- Add tmpfiles_create_package usage to reproduce coredump

* Mon Dec 10 2018 Robert Fairley <rfairley@redhat.com> - 0.1-8
- Remove tmpfiles_create_package usage

* Mon Dec 10 2018 Robert Fairley <rfairley@redhat.com> - 0.1-7
- Fix usage of tmpfiles_create_package macro in specfile

* Fri Dec 07 2018 Robert Fairley <rfairley@redhat.com> - 0.1-6
- Fix tmpfile symlink paths

* Fri Dec 07 2018 Robert Fairley <rfairley@redhat.com> - 0.1-5
- Add [systemd] label to failed units message in profile script

* Tue Dec 04 2018 Robert Fairley <rfairley@redhat.com> - 0.1-4
- Minor formatting edits to generated issue and motd

* Tue Dec 04 2018 Robert Fairley <rfairley@redhat.com> - 0.1-3
- Remove printing package manager info (rpm-ostree, dnf)

* Tue Dec 04 2018 Robert Fairley <rfairley@redhat.com> - 0.1-2
- Add CI with copr
- Drop requirement on specifc SELinux version
- Various tidyups including filenames

* Tue Sep 25 2018 Robert Fairley <rfairley@redhat.com> - 0.1-1
- Initial Package
