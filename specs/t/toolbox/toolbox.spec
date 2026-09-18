# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global __brp_check_rpaths %{nil}

%if 0%{?rhel}
%if 0%{?rhel} <= 9
%{!?bash_completions_dir: %global bash_completions_dir %{_datadir}/bash-completion/completions}
%{!?fish_completions_dir: %global fish_completions_dir %{_datadir}/fish/vendor_completions.d}
%{!?zsh_completions_dir: %global zsh_completions_dir %{_datadir}/zsh/site-functions}
%endif
%endif


Name:          toolbox
Version:       0.3

%global goipath github.com/containers/%{name}

%if 0%{?fedora}
%gometa -f
%endif

%if 0%{?rhel}
%if 0%{?rhel} <= 9
%gometa
%else
%gometa -f
%endif
%endif

%global toolbx_go 1.22

%if 0%{?fedora}
%global toolbx_go 1.24.7
%endif

%if 0%{?rhel}
%if 0%{?rhel} == 9
%global toolbx_go 1.22.5
%elif 0%{?rhel} == 10
%global toolbx_go 1.22.5
%elif 0%{?rhel} > 10
%global toolbx_go 1.24.4
%endif
%endif

Release:       1%{?dist}
Summary:       Tool for interactive command line environments on Linux

License:       Apache-2.0
URL:           https://containertoolbx.org/
Source0:       https://github.com/containers/%{name}/releases/download/%{version}/%{name}-%{version}-vendored.tar.xz

# RHEL specific
Source1:       %{name}.conf

# Fedora specific
Patch100:      toolbox-Make-the-build-flags-match-Fedora.patch

# RHEL specific
Patch200:      toolbox-Make-the-build-flags-match-RHEL-9.patch
Patch201:      toolbox-Make-the-build-flags-match-RHEL-10.patch
Patch202:      toolbox-Add-migration-paths-for-coreos-toolbox-users.patch

BuildRequires: gcc
BuildRequires: go-md2man
BuildRequires: golang >= %{toolbx_go}
BuildRequires: meson >= 0.58.0
BuildRequires: pkgconfig(bash-completion)
BuildRequires: shadow-utils-subid-devel >= 4.16.0
BuildRequires: systemd
BuildRequires: systemd-rpm-macros
%if ! 0%{?rhel}
BuildRequires: pkgconfig(fish)
# for tests
# BuildRequires: codespell
# BuildRequires: ShellCheck
%endif

Recommends:    p11-kit-server
Recommends:    skopeo
%if ! 0%{?rhel}
Recommends:    fuse-overlayfs
%endif

Requires:      containers-common
Requires:      flatpak-session-helper
Requires:      podman >= 1.6.4
Requires:      shadow-utils-subid%{?_isa} >= 4.16.0


%description
Toolbx is a tool for Linux, which allows the use of interactive command line
environments for software development and troubleshooting the host operating
system, without having to install software on the host. It is built on top of
Podman and other standard container technologies from OCI.

Toolbx environments have seamless access to the user's home directory, the
Wayland and X11 sockets, networking (including Avahi), removable devices (like
USB sticks), systemd journal, SSH agent, D-Bus, ulimits, /dev and the udev
database, etc..


%package       tests
Summary:       Tests for %{name}

Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      coreutils
Requires:      diffutils
# for gdbus(1)
Requires:      glib2
Requires:      grep
# for htpasswd(1)
Requires:      httpd-tools
Requires:      openssl
Requires:      python3
Requires:      skopeo
%if ! 0%{?rhel}
Requires:      bats >= 1.10.0
%endif


%description   tests
The %{name}-tests package contains system tests for %{name}.


%prep
%setup -q

%if 0%{?fedora}
%patch -P100 -p1
%endif

%if 0%{?rhel}
%if 0%{?rhel} == 9
%patch -P200 -p1
%endif

%if 0%{?rhel} >= 10
%patch -P201 -p1
%endif

%if 0%{?rhel} <= 9
%patch -P202 -p1
%endif
%endif

%gomkdir -s %{_builddir}/%{extractdir}/src -k


%build
export CGO_CFLAGS="%{optflags} -D_GNU_SOURCE -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"

%meson \
%if 0%{?rhel}
    -Dfish_completions_dir=%{fish_completions_dir} \
%if 0%{?rhel} <= 9
    -Dmigration_path_for_coreos_toolbox=true \
%endif
%endif
    -Dprofile_dir=%{_sysconfdir}/profile.d \
    -Dtmpfiles_dir=%{_tmpfilesdir} \
    -Dzsh_completions_dir=%{zsh_completions_dir}

%meson_build


# %%check
# %%meson_test


%install
%meson_install

%if 0%{?rhel}
%if 0%{?rhel} <= 9
install -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/containers/%{name}.conf
%endif
%endif


%files
%doc CODE-OF-CONDUCT.md CONTRIBUTING.md GOALS.md NEWS README.md SECURITY.md
%license COPYING src/vendor/modules.txt
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}-*.1*
%{_mandir}/man5/%{name}.conf.5*
%config(noreplace) %{_sysconfdir}/containers/%{name}.conf
%{_sysconfdir}/profile.d/%{name}.sh
%{_tmpfilesdir}/%{name}.conf
%{bash_completions_dir}/%{name}.bash
%{fish_completions_dir}/%{name}.fish
%{zsh_completions_dir}/_%{name}


%files tests
%{_datadir}/%{name}


%changelog
* Wed Sep 17 2025 Debarshi Ray <rishi@fedoraproject.org> - 0.3-1
- Update to 0.3

* Fri Aug 15 2025 Maxwell G <maxwell@gtmx.me> - 0.2-2
- Rebuild for golang-1.25.0

* Sat Aug 09 2025 Debarshi Ray <rishi@fedoraproject.org> - 0.2-1
- Update to 0.2
- Fix CVE-2025-23266, CVE-2025-23267, and GHSA-fv92-fjc5-jj9h or GO-2025-3787

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Debarshi Ray <rishi@fedoraproject.org> - 0.1.2-1
- Update to 0.1.2

* Wed Jan 22 2025 Debarshi Ray <rishi@fedoraproject.org> - 0.1.1-3
- Use RPM macros for shell completions and clean up directory ownership

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Nov 04 2024 Debarshi Ray <rishi@fedoraproject.org> - 0.1.1-1
- Update to 0.1.1

* Tue Oct 22 2024 Debarshi Ray <rishi@fedoraproject.org> - 0.1.0-1
- Update to 0.1.0

* Wed Oct 16 2024 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.6-6
- Recommend fuse-overlayfs because old containers created with it need it

* Mon Oct 07 2024 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.6-5
- Don't use slirp4netns(1) in tests to work around bug in pasta(1)

* Fri Oct 04 2024 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.6-4
- Use the fedora-toolbox:40 image for Fedora Asahi Remix hosts

* Thu Oct 03 2024 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.6-3
- Unbreak the downstream Fedora CI

* Wed Oct 02 2024 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.6-2
- Silence 'rpminspect --tests=elf'

* Mon Sep 30 2024 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.6-1
- Update to 0.0.99.6

* Thu Sep 12 2024 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.5-18
- Rebuild against shadow-utils-subid ABI version 5.0.0

* Thu Aug 08 2024 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.5-17
- Ensure slirp4netns(1) is installed

* Wed Jul 31 2024 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.5-16
- Avoid running out of storage space when running the tests

* Fri Jul 26 2024 Adam Williamson <awilliam@redhat.com> - 0.0.99.5-15
- Fix CI test (hopefully)

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.99.5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 11 2024 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.5-13
- Silence 'rpminspect --tests=stack-prot'

* Thu Jul 11 2024 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.5-12
- Silence 'rpminspect --tests=annocheck' (part 2)

* Tue May 07 2024 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.5-11
- Unbreak the tests with Podman 5.0

* Tue Mar 26 2024 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.5-10
- Specify the golang versions for RHEL 9 and 10

* Tue Mar 05 2024 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.5-9
- Conditionalize the BuildRequires on golang

* Tue Feb 27 2024 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.5-8
- Unbreak Podman's downstream Fedora CI (part 2)
- Backport some new upstream tests

* Tue Feb 13 2024 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.5-7
- Unbreak Podman's downstream Fedora CI
- Update the BuildRequires on golang to reflect reality

* Sun Feb 11 2024 Maxwell G <maxwell@gtmx.me> - 0.0.99.5-6
- Rebuild for golang 1.22.0

* Wed Feb 07 2024 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.5-5
- Migrate to SPDX license

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.99.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 11 2024 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.5-3
- Drop 'Recommends: subscription-manager'

* Tue Dec 19 2023 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.5-2
- Drop the experience and support subpackages

* Tue Dec 19 2023 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.5-1
- Update to 0.0.99.5

* Tue Dec 19 2023 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.4-10
- Require openssl(1) for the system tests in the tests subpackage

* Wed Dec 06 2023 Adam Williamson <awilliam@redhat.com> - 0.0.99.4-9
- tests subpackage: require httpd-tools for htpasswd

* Tue Dec 05 2023 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.4-8
- Fix the conditionals for 'if RHEL <= 9'

* Thu Nov 30 2023 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.4-7
- Track the active container on Fedora Linux Asahi Remix

* Thu Nov 09 2023 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.4-6
- Drop the custom /etc/containers/toolbox.conf from RHEL 10 onwards

* Mon Oct 02 2023 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.4-5
- Drop github.com/coreos/toolbox compatibility from RHEL 10 onwards

* Mon Oct 02 2023 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.4-4
- Be aware of security hardened mount points
- Simplify removing the user's password

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.99.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Mar 8 2023 Nieves Montero <nmontero@redhat.com> - 0.0.99.4-2
- Sprinkle a debug log

* Wed Feb 22 2023 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.4-1
- Update to 0.0.99.4

* Wed Feb 22 2023 Martin Jackson <mhjacks@swbell.net> - 0.0.99.3-12
- Fix the ExclusiveArch

* Tue Feb 21 2023 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.3-11
- Add ExclusiveArch to match Podman

* Thu Feb 02 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 0.0.99.3-10
- Sync packaging changes from CentOS Stream

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.99.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 22 2022 Yaakov Selkowitz <yselkowi@redhat.com> - 0.0.99.3-8
- Use vendored dependencies for RHEL/ELN builds

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.99.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Maxwell G <gotmax@e.email> - 0.0.99.3-6
- Rebuild for CVE-2022-{1705,32148,30631,30633,28131,30635,30632,30630,1962} in
  golang

* Sat Jun 18 2022 Robert-André Mauchin <zebob.m@gmail.com> - 0.0.99.3-5
- Rebuilt for CVE-2022-1996, CVE-2022-24675, CVE-2022-28327, CVE-2022-27191,
  CVE-2022-29526, CVE-2022-30629

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.99.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Jan 09 2022 Ondřej Míchal <harrymichal@fedoraproject.org> - 0.0.99.3-3
- Add upstream patch fixing doubled error messages

* Fri Dec 10 2021 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.3-2
- BuildRequire only systemd-rpm-macros as recommended by the Fedora packaging
  guidelines

* Fri Dec 10 2021 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.3-1
- Update to 0.0.99.3

* Mon Oct 25 2021 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.2^3.git075b9a8d2779-9
- Restore backwards compatibility with existing containers

* Fri Oct 22 2021 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.2^3.git075b9a8d2779-8
- Ensure that binaries are run against their build-time ABI

* Mon Sep 13 2021 Oliver Gutiérrez <ogutierrez@fedoraproject.org> - 0.0.99.2^3.git075b9a8d2779-7
- Rebuilt for gating tests

* Thu Sep 09 2021 Oliver Gutiérrez <ogutierrez@fedoraproject.org> - 0.0.99.2^3.git075b9a8d2779-6
- Rebuilt for gating tests

* Mon Aug 23 2021 Oliver Gutiérrez <ogutierrez@fedoraproject.org> - 0.0.99.2^3.git075b9a8d2779-5
- Version bump to build and check fedora gating after fixing ansible playbooks

* Fri Aug 20 2021 Oliver Gutiérrez <ogutierrez@fedoraproject.org> - 0.0.99.2^3.git075b9a8d2779-4
- Version bump to build and check fedora gating

* Wed Aug 18 2021 Oliver Gutiérrez <ogutierrez@fedoraproject.org> - 0.0.99.2^3.git075b9a8d2779-3
- Added Fedora gating

* Wed Aug 18 2021 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.2^3.git075b9a8d2779-2
- Require containers-common for ownership of %%{_sysconfdir}/containers

* Mon Aug 09 2021 Oliver Gutiérrez <ogutierrez@fedoraproject.org> - 0.0.99.2^3.git075b9a8d2779-1
- Updated to 0.0.99.2^3.git075b9a8d2779 snapshot

* Thu Jul 29 2021 Oliver Gutiérrez <ogutierrez@fedoraproject.org> - 0.0.99.2^2.git40fbd377ed0b-1
- Updated to 0.0.99.2^2.git40fbd377ed0b snapshot

* Wed Jul 28 2021 Oliver Gutiérrez <ogutierrez@fedoraproject.org> - 0.0.99.2^1.git9820550c82bb-1
- Updated to 0.00.99.2^1.git9820550c82bb snapshot

* Wed Jul 28 2021 Ondřej Míchal <harrymichal@seznam.cz> - 0.0.99.2-3
- Update dependencies of -tests subpackage

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.99.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jun 26 2021 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.2-1
- Update to 0.0.99.2

* Tue Feb 23 2021 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99.1-1
- Update to 0.0.99.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.99-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 2021 Debarshi Ray <rishi@fedoraproject.org> - 0.0.99-1
- Update to 0.0.99

* Mon Jan 11 2021 Debarshi Ray <rishi@fedoraproject.org> - 0.0.98.1-2
- Harden the binary by using the same CGO_CFLAGS as on RHEL 8

* Thu Jan 07 2021 Debarshi Ray <rishi@fedoraproject.org> - 0.0.98.1-1
- Update to 0.0.98.1

* Tue Jan 05 2021 Debarshi Ray <rishi@fedoraproject.org> - 0.0.98-1
- Update to 0.0.98

* Wed Nov 25 2020 Ondřej Míchal <harrymichal@seznam.cz> - 0.0.97-2
- Move krb5-libs from -support to -experience, and update the list of packages
  in -experience

* Tue Nov 03 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.0.97-1
- Update to 0.0.97

* Thu Oct 01 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.0.96-1
- Update to 0.0.96

* Sun Aug 30 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.0.95-1
- Update to 0.0.95

* Mon Aug 24 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.0.94-1
- Update to 0.0.94

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.93-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 25 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.0.93-1
- Update to 0.0.93

* Fri Jul 03 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.0.92-1
- Update to 0.0.92

* Fri Jul 03 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.0.91-2
- Fix the 'toolbox --version' output

* Tue Jun 30 2020 Harry Míchal <harrymichal@seznam.cz> - 0.0.91-1
- Update to 0.0.91

* Sat Jun 27 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.0.18-5
- Remove ExclusiveArch to match Podman

* Wed Jun 10 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.0.18-4
- Sync the "experience" packages with the current Dockerfile
- Make "experience" Require "support"

* Fri Apr 03 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.0.18-3
- Drop compatibility Obsoletes and Provides for fedora-toolbox

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 14 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.0.18-1
- Update to 0.0.18

* Wed Nov 20 2019 Debarshi Ray <rishi@fedoraproject.org> - 0.0.17-1
- Update to 0.0.17

* Tue Oct 29 2019 Debarshi Ray <rishi@fedoraproject.org> - 0.0.16-1
- Update to 0.0.16

* Mon Sep 30 2019 Debarshi Ray <rishi@fedoraproject.org> - 0.0.15-1
- Update to 0.0.15

* Wed Sep 18 2019 Debarshi Ray <rishi@fedoraproject.org> - 0.0.14-1
- Update to 0.0.14

* Thu Sep 05 2019 Debarshi Ray <rishi@fedoraproject.org> - 0.0.13-1
- Update to 0.0.13

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 22 2019 Debarshi Ray <rishi@fedoraproject.org> - 0.0.12-1
- Update to 0.0.12

* Tue Jun 25 2019 Debarshi Ray <rishi@fedoraproject.org> - 0.0.11-2
- Require flatpak-session-helper

* Fri Jun 21 2019 Debarshi Ray <rishi@fedoraproject.org> - 0.0.11-1
- Update to 0.0.11

* Tue May 21 2019 Debarshi Ray <rishi@fedoraproject.org> - 0.0.10-1
- Update to 0.0.10

* Tue Apr 30 2019 Debarshi Ray <rishi@fedoraproject.org> - 0.0.9-1
- Update to 0.0.9

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 0.0.8-2
- Rebuild with Meson fix for #1699099

* Fri Apr 12 2019 Debarshi Ray <rishi@fedoraproject.org> - 0.0.8-1
- Update to 0.0.8

* Thu Mar 14 2019 Debarshi Ray <rishi@fedoraproject.org> - 0.0.7-1
- Update to 0.0.7

* Fri Feb 22 2019 Debarshi Ray <rishi@fedoraproject.org> - 0.0.6-1
- Initial build after rename from fedora-toolbox
