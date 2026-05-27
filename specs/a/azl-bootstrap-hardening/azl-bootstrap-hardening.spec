# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           azl-bootstrap-hardening
Version:        1
Release:        1%{?dist}
Summary:        Stage1 BinSkim hardening macros for Azure Linux
License:        MIT
URL:            https://aka.ms/azurelinux
BuildArch:      noarch

Source0:        macros.azl-bootstrap-hardening

# rpm reads /usr/lib/rpm/macros.d/* at startup, so installing this drop-in
# is the only thing we need to do — no scriptlets required.
Requires:       redhat-rpm-config

%description
Layers Azure Linux stage1 compiler/linker hardening defaults on top of
Fedora's redhat-rpm-config via a /usr/lib/rpm/macros.d/ drop-in. Pilot
package used to evaluate distro-wide BinSkim remediation for the
azl4-bootstrap-compliance build target before broader rollout.

%prep
# Nothing to unpack.

%build
# Nothing to build.

%install
install -d %{buildroot}%{_rpmconfigdir}/macros.d
install -m 0644 %{SOURCE0} %{buildroot}%{_rpmconfigdir}/macros.d/macros.azl-bootstrap-hardening

%files
%{_rpmconfigdir}/macros.d/macros.azl-bootstrap-hardening

%changelog
* Tue May 27 2026 Azure Linux Team <azurelinux-pmc@microsoft.com> - 1-1
- Initial package for stage1 hardening flag rollout pilot.
