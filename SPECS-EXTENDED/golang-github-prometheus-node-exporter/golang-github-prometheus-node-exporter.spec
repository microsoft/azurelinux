%global shortname prometheus-node-exporter

# https://github.com/prometheus/node_exporter
%global goipath         github.com/prometheus/node_exporter

%gometa

%global common_description %{expand:
Prometheus exporter for hardware and OS metrics exposed by *NIX kernels, written
in Go with pluggable metric collectors.}

%global golicenses      LICENSE NOTICE

%global godocs          docs examples CHANGELOG.md CODE_OF_CONDUCT.md\\\
                        CONTRIBUTING.md MAINTAINERS.md SECURITY.md README.md

Summary:        Exporter for machine metrics
Name:           %{goname}
Version:        1.3.1
Release:        6%{?dist}
# Upstream license specification: Apache-2.0
License:        ASL 2.0 AND MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            %{gourl}
Source0:        https://github.com/prometheus/node_exporter/archive/refs/tags/v%{version}.tar.gz#/%{shortname}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using vendored Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/prometheus/node_exporter/archive/refs/tags/v%{version}.tar.gz -O %%{shortname}-%%{version}.tar.gz
#   2. tar -xf %%{shortname}-%%{version}.tar.gz
#   3. cd %%{shortname}-%%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{shortname}-%%{version}-vendor.tar.gz vendor
#
Source1:        %{name}-%{version}-vendor.tar.gz
Source2:        %{shortname}.sysusers
Source3:        %{shortname}.service
Source4:        %{shortname}.conf
Source5:        %{shortname}.logrotate
# Replace defaults paths for config files
Patch0:         defaults-paths.patch
# https://github.com/prometheus/node_exporter/pull/2190
Patch1:         0001-Refactor-perf-collector.patch

BuildRequires:  go-rpm-macros
BuildRequires:  systemd-rpm-macros

Requires(pre):  shadow-utils

%description
%{common_description}

%{gopkg}

%prep
%{goprep}
%patch0 -p1
%patch1 -p1

%build
export BUILDTAGS="netgo osusergo static_build"
LDFLAGS="-X github.com/prometheus/common/version.Version=%{version}  \
         -X github.com/prometheus/common/version.Revision=%{release} \
         -X github.com/prometheus/common/version.Branch=tarball      \
         -X github.com/prometheus/common/version.BuildDate=$(date -u -d@$SOURCE_DATE_EPOCH +%%Y%%m%%d)"
%{gobuild} -o %{gobuilddir}/bin/node_exporter %{goipath}

%install
%{gopkginstall}
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/
mv %{buildroot}%{_bindir}/node_exporter %{buildroot}%{_bindir}/%{shortname}
pushd %{buildroot}%{_bindir}
ln -s %{shortname} node_exporter
popd

install -Dpm0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{shortname}.conf
install -Dpm0644 %{SOURCE3} %{buildroot}%{_unitdir}/%{shortname}.service
install -Dpm0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/default/%{shortname}
install -Dpm0644 example-rules.yml %{buildroot}%{_datadir}/prometheus/node-exporter/example-rules.yml
install -Dpm0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/%{shortname}
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus/node-exporter

# Build man pages.
mkdir -vp %{buildroot}/%{_mandir}/man1/
%{buildroot}%{_bindir}/%{shortname} --help-man > \
    %{buildroot}/%{_mandir}/man1/%{shortname}.1
sed -i '/^  /d; /^.SH "NAME"/,+1c.SH "NAME"\nprometheus-node-exporter \\- The Prometheus Node-Exporter' \
    %{buildroot}/%{_mandir}/man1/%{shortname}.1

%check
%{gocheck} -d collector

%pre
%{sysusers_create_compat} %{SOURCE1}

%post
%systemd_post %{shortname}.service

%preun
%systemd_preun %{shortname}.service

%postun
%systemd_postun_with_restart %{shortname}.service

%files
%license LICENSE NOTICE
%doc docs examples CHANGELOG.md CODE_OF_CONDUCT.md CONTRIBUTING.md
%doc MAINTAINERS.md SECURITY.md README.md
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/default/%{shortname}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{shortname}
%{_sysusersdir}/%{shortname}.conf
%{_unitdir}/%{shortname}.service
%{_mandir}/man1/%{shortname}.1*
%{_datadir}/prometheus/node-exporter/example-rules.yml
%dir %attr(0755,prometheus,prometheus) %{_sharedstatedir}/prometheus
%dir %attr(0755,prometheus,prometheus) %{_sharedstatedir}/prometheus/node-exporter

%{gopkgfiles}

%changelog
* Mon Jan 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.1-6
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Jan 16 2022 Robert-André Mauchin <zebob.m@gmail.com> 1.3.1-4
- Add logrotate file

* Sat Jan 15 2022 Robert-André Mauchin <zebob.m@gmail.com> 1.3.1-3
- Add LDFLAGS

* Fri Jan 14 2022 Robert-André Mauchin <zebob.m@gmail.com> 1.3.1-2
- Fix home directory permissions

* Fri Jan 14 2022 Robert-André Mauchin <zebob.m@gmail.com> 1.3.1-1
- Update to 1.3.1 Close: rhbz#2024811 Close: rhbz#2039257

* Thu Aug 12 2021 Robert-André Mauchin <zebob.m@gmail.com> 1.2.2-1
- Update to 1.2.2 Close: rhbz#1945422

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Mar 28 18:14:35 CEST 2021 Robert-André Mauchin <zebob.m@gmail.com> - 1.1.1-2
- Fix binary location

* Wed Feb 17 22:48:22 CET 2021 Robert-André Mauchin <zebob.m@gmail.com> - 1.1.1-1
- Initial package
