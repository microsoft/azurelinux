## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 7;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond bootstrap 0

Name:           dola
Version:        1.3.2
Release:        %autorelease
Summary:        Declarative system for Java RPM packaging
License:        Apache-2.0
URL:            https://github.com/mizdebsk/dola
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source:         https://github.com/mizdebsk/dola/releases/download/%{version}/dola-%{version}.tar.zst

# https://github.com/mizdebsk/dola/pull/30
Patch:          0001-Update-to-XMvn-5.1.0.patch
# https://github.com/mizdebsk/dola/pull/32
Patch:          0002-Ensure-os_install_post-commands-are-NL-terminated.patch
# https://github.com/mizdebsk/dola/pull/33
Patch:          0003-Switch-to-OpenJDK-for-runtime.patch

Requires:       %{name}-bsx = %{version}-%{release}
Requires:       %{name}-generator = %{version}-%{release}
Requires:       dola-gleaner
Requires:       dola-transformer
Requires:       xmvn5-minimal
Requires:       xmvn5-mojo
Requires:       xmvn5-tools

BuildSystem:    maven
BuildOption:    usesJavapackagesBootstrap
BuildOption:    singletonPackaging
BuildOption:    xmvnToolchain "openjdk25"
BuildOption:    buildRequires {
BuildOption:        version "org.apache.maven:" "4.0.0-rc-4"
BuildOption:        version "org.fedoraproject.xmvn:" "5.1.0"
BuildOption:    }

%description
Dola is a modern, declarative system for RPM packaging of Maven-based
Java projects.  It enables package maintainers to entirely avoid
writing `%%prep`, `%%build`, or `%%install` scriptlets in RPM spec files.
Instead, all build configuration is expressed using BuildOption tags
(introduced in RPM 4.20), resulting in cleaner, more maintainable spec
files.

%package bsx
Summary:        Runtime layer for running Dola inside RPM builds
Requires:       java-25-openjdk-headless
Requires:       lujavrite
Requires:       rpm-build

%description bsx
Dola BSX is a minimal execution layer that bridges the gap between
rpmbuild and high-level packaging logic implemented in Java via Dola.
Acting as a microkernel, BSX exposes a structured API for I/O, macro
evaluation, logging, and event handling.

%package generator
Summary:        RPM dependency generator for Java
Requires:       %{name}-bsx = %{version}-%{release}

%description generator
Dola Generator is a dependency generator for RPM Package Manager
written in Java and Lua, that uses LuJavRite library to call Java code
from Lua.

%install -a
# BSX
install -D -p -m 644 dola-bsx/src/main/lua/dola-bsx.lua %{buildroot}%{_rpmluadir}/dola-bsx.lua
install -D -p -m 644 dola-bsx/src/main/rpm/macros.dola-bsx %{buildroot}%{_rpmmacrodir}/macros.dola-bsx
install -D -p -m 644 dola-bsx/src/main/conf/dola-bsx.conf %{buildroot}%{_javaconfdir}/dola/classworlds/00-dola-bsx.conf
install -D -p -m 644 dola-bsx-api/src/main/conf/dola-bsx-api.conf %{buildroot}%{_javaconfdir}/dola/classworlds/01-dola-bsx-api.conf
# DBS
install -D -p -m 644 dola-dbs/src/main/lua/dola-dbs.lua %{buildroot}%{_rpmluadir}/dola-dbs.lua
install -D -p -m 644 dola-dbs/src/main/rpm/macros.dola-dbs %{buildroot}%{_rpmmacrodir}/macros.zzz-dola-dbs
install -D -p -m 644 dola-dbs/src/main/conf/dola-dbs.conf %{buildroot}%{_javaconfdir}/dola/classworlds/04-dola-dbs.conf
# Generator
install -D -p -m 644 dola-generator/src/main/lua/dola-generator.lua %{buildroot}%{_rpmluadir}/dola-generator.lua
install -D -p -m 644 dola-generator/src/main/rpm/macros.dola-generator %{buildroot}%{_rpmmacrodir}/macros.dola-generator
install -D -p -m 644 dola-generator/src/main/rpm/macros.dola-generator-etc %{buildroot}%{_sysconfdir}/rpm/macros.dola-generator-etc
install -D -p -m 644 dola-generator/src/main/rpm/dolagen.attr %{buildroot}%{_fileattrsdir}/dolagen.attr
install -D -p -m 644 dola-generator/src/main/conf/dola-generator.conf %{buildroot}%{_javaconfdir}/dola/classworlds/03-dola-generator.conf

%files bsx -f .mfiles-dola-bsx -f .mfiles-dola-bsx-api
%{_rpmluadir}/dola-bsx.lua
%{_rpmmacrodir}/macros.dola-bsx
%dir %{_javaconfdir}/dola
%dir %{_javaconfdir}/dola/classworlds
%{_javaconfdir}/dola/classworlds/00-dola-bsx.conf
%{_javaconfdir}/dola/classworlds/01-dola-bsx-api.conf
%license LICENSE NOTICE

%files -f .mfiles-dola-dbs -f .mfiles-dola-parent
%{_rpmluadir}/dola-dbs.lua
%{_rpmmacrodir}/macros.zzz-dola-dbs
%{_javaconfdir}/dola/classworlds/04-dola-dbs.conf
%doc README.md

%files generator -f .mfiles-dola-generator
%{_rpmluadir}/dola-generator.lua
%{_rpmmacrodir}/macros.dola-generator
%{_sysconfdir}/rpm/macros.dola-generator-etc
%{_fileattrsdir}/dolagen.attr
%{_javaconfdir}/dola/classworlds/03-dola-generator.conf

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 1.3.2-7
- test: add initial lock files

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 13 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.2-5
- Switch to OpenJDK 25 for runtime

* Sat Jul 12 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.2-4
- Ensure os_install_post commands are NL-terminated

* Sat Jul 12 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.2-1
- Update to upstream version 1.3.2

* Wed Jul 09 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.1-1
- Update to upstream version 1.3.1

* Tue Jul 08 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.0-1
- Update to upstream version 1.3.0
- Singleton packaging

* Fri Jul 04 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2.0-3
- Configure smoke tests for gating

* Thu Jul 03 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2.0-2
- Switch to declarative build

* Thu Jul 03 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2.0-1
- Update to upstream version 1.2.0

* Wed Jun 25 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1.0-1
- Update to upstream version 1.1.0

* Fri Jun 13 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.0-2
- Implement bootstrap mode

* Wed Jun 11 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.0-1
- Update to upstream version 1.0.0

* Thu May 22 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 0^20250521.183244.git.7d6a2aa-2
- Onboard package into gating

* Thu May 22 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 0^20250521.183244.git.7d6a2aa-1
- Initial packaging
## END: Generated by rpmautospec
