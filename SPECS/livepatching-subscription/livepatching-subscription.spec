%define livepatching_lib_path %{_libdir}/livepatching

Summary:        Retain livepatches across kernel upgrades
Name:           livepatching-subscription
Version:        1.0.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Text
URL:            https://aka.ms/cbl-mariner
Source0:        livepatching.service
Source1:        livepatching.systemd

ExclusiveArch:  x86_64

BuildRequires:  systemd

Requires:       coreutils
Requires:       grep
Requires:       inotify-tools
Requires:       systemd
Requires:       tdnf
Requires(post): grep
Requires(post): inotify-tools
Requires(post): systemd
Requires(post): tdnf
Requires(postun): systemd

%description
This package allows your system to retain livepatching across kernel upgrades.
Once a livepatch for the new kernel is installed, it does NOT automatically
pull newer versions of the livepatch for that kernel.

%prep

%install
install -vdm755 %{buildroot}/lib/systemd/system-preset
echo "enable livepatching.service" > %{buildroot}%{_libdir}/systemd/system-preset/50-livepatching.preset

install -vdm755 %{buildroot}%{_unitdir}
install -D -m 644 %{SOURCE0} %{buildroot}%{_unitdir}/livepatching.service

install -vdm755 %{buildroot}%{livepatching_lib_path}
install -D -m 644 %{SOURCE1} %{buildroot}%{livepatching_lib_path}/livepatching.systemd

%post
%systemd_post livepatching.service

%postun
%systemd_postun livepatching.service

%files
%defattr(-,root,root)
%{_libdir}/systemd/system-preset/50-livepatching.preset
%{_unitdir}/livepatching.service
%{livepatching_lib_path}/livepatching.systemd

%changelog
* Fri Sep 02 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.0-1
- Original version for CBL-Mariner.
- License verified.
