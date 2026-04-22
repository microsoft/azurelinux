# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# General maintainer notes:
#   Fedora guideliens for packaging of SELinux rules:
#     https://fedoraproject.org/wiki/SELinux/IndependentPolicy
#   RHEL instructions regarding Troubleshooting problems related to SELinux:
#     https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/using_selinux/troubleshooting-problems-related-to-selinux_using-selinux

# defining macros needed by SELinux
%global selinuxtype targeted
%global modulename mysql

Name:           mysql-selinux
Version:        1.0.14
Release: 3%{?dist}

License:        GPL-3.0-only
URL:            https://github.com/devexp-db/mysql-selinux
Summary:        SELinux policy modules for MySQL and MariaDB packages

Source0:        https://github.com/devexp-db/mysql-selinux/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  selinux-policy-devel

%{?selinux_requires}
Requires:       selinux-policy-%{selinuxtype}
Requires(post): selinux-policy-%{selinuxtype}

%description
SELinux policy modules for MySQL and MariaDB packages.


%prep
%setup -q -n %{name}-%{version}

%build
make

%install
# install policy modules
install -d %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}
install -m 0644 %{modulename}.pp.bz2 %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}


%pre
%selinux_relabel_pre -s %{selinuxtype}

%post
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2

%postun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename}
fi

%posttrans
%selinux_relabel_post -s %{selinuxtype}


%files
%defattr(-,root,root,0755)
%attr(0644,root,root) %{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2
%ghost %verify(not mode md5 size mtime) %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{modulename}
%license COPYING

# Note:
#   we do not pack the *.if file as seen in the example:
#     https://fedoraproject.org/wiki/SELinux/IndependentPolicy#The_%prep_and_%install_Section
#   since we do not have any interface to be shared (and even then it is optional)

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 15 2025 Packit <hello@packit.dev> - 1.0.14-1
- Update to version 1.0.14
- Resolves: rhbz#2380217

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 19 2024 Michal Schorm <mschorm@redhat.com> - 1.0.13-1
- Update to version 1.0.13

* Mon Sep 16 2024 Packit <hello@packit.dev> - 1.0.11-1
- Update to version 1.0.11
- Resolves: rhbz#2312549

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Nov 18 2023 Packit <hello@packit.dev> - 1.0.10-1
- 2nd attempt to fix rhbz#2186996 rhbz#2221433 rhbz#2245705 (Michal Schorm)
- Resolves rhbz#2250424

* Fri Nov 17 2023 Packit <hello@packit.dev> - 1.0.9-1
- Revert "Attempt to fix rhbz#2186996 rhbz#2221433 rhbz#2245705" This reverts commit de84778e555b891fd9ea5f3111c87a4990650d6c. (Michal Schorm)
- Resolves rhbz#2250360

* Tue Sep 26 2023 Michal Schorm <mschorm@redhat.com> - 1.0.7-2
- Bump release for rebuild

* Thu Sep 14 2023 Packit <hello@packit.dev> - 1.0.7-1
- Empty commit to test Fedora PACKIT configuration for packaging automation (Michal Schorm)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Adam Dobes <adobes@redhat.com> - 1.0.6-1
- Rebase to 1.0.6

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 09 2022 Michal Schorm <mschorm@redhat.com> - 1.0.5-1
- Rebase to 1.0.5

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Apr 21 2021 Lukas Javorsky <ljavorsk@redhat.com> - 1.0.4-2
- Fix rpm verification it's a ghost file so it should ignore the error

* Fri Mar 19 2021 Lukas Javorsky <ljavorsk@redhat.com> - 1.0.4-1
- Rebase to 1.0.4
- Unintentional removal of semicolon

* Fri Mar 19 2021 Lukas Javorsky <ljavorsk@redhat.com> - 1.0.3-1
- Rebase to 1.0.3
- Remove setuid/setgid capabilities from mysqld_t type.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 02 2020 Michal Schorm <mschorm@redhat.com> - 1.0.2-1
- Rebase to 1.0.2 release
  Added context for "*mariadb*" named executables

* Tue Dec 01 2020 Michal Schorm <mschorm@redhat.com> - 1.0.1-1
- Rebase to 1.0.1 release
  This release is just a sync-up with upstream selinux-policy
- URL changed to a new upstream repository

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 11 2019 Kevin Fenzi <kevin@scrye.com> - 1.0.0-7
- Also make sure posttrans does not fail.

* Thu Jan 10 2019 Kevin Fenzi <kevin@scrye.com> - 1.0.0-6
- Add Requires(post) on policycoreutils for semodule and make sure post/postun cannot fail

* Thu Dec 06 2018 Jakub Janco <jjanco@redhat.com> - 1.0.0-5
- Sync with upstream

* Wed Aug 29 2018 Jakub Janco <jjanco@redhat.com> - 1.0.0-4
- Allow mysqld sys_nice capability

* Mon Aug 20 2018 Jakub Janco <jjanco@redhat.com> - 1.0.0-3
- reflect latest changes of mysql policy

* Fri Jul 27 2018 Jakub Janco <jjanco@redhat.com> - 1.0.0-2
- reflect latest changes of Independent Product Policy

* Wed Jul 18 2018 Jakub Janco <jjanco@redhat.com> - 1.0.0-1
- First Build

