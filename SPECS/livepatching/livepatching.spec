%define livepatching_lib_path %{_libdir}/livepatching

Summary:        Set of core livepatching packages for Mariner.
Name:           livepatching
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

%description
%{summary}

%package filesystem
Summary:        Basic directory layout for livepatching packages.

%description filesystem
%{summary}

%package subscription
Summary:        Retain livepatches across kernel upgrades.

Requires:       %{name}-filesystem = %{version}-%{release}
Requires:       coreutils
Requires:       grep
Requires:       inotify-tools
Requires:       kpatch
Requires:       systemd
Requires:       tdnf

Requires(post): grep
Requires(post): inotify-tools
Requires(post): kpatch
Requires(post): systemd
Requires(post): tdnf

Requires(postun): systemd

Requires(preun): systemd

%description subscription
This package allows your system to retain livepatches across kernel upgrades.
Once a livepatch for the new kernel is installed, it does NOT automatically
pull newer versions of the livepatch for that kernel.

%prep

%install
install -vdm755 %{buildroot}%{_libdir}/systemd/system-preset
echo "enable livepatching.service" > %{buildroot}%{_libdir}/systemd/system-preset/50-livepatching.preset

install -vdm755 %{buildroot}%{_unitdir}
install -D -m 644 %{SOURCE0} %{buildroot}%{_unitdir}/livepatching.service

install -vdm755 %{buildroot}%{livepatching_lib_path}
install -D -m 744 %{SOURCE1} %{buildroot}%{livepatching_lib_path}/livepatching.systemd

%post subscription
%systemd_post livepatching.service
# Only start on initial installation. Upgrade restarts handled by %%postun.
if [ $1 -eq 1 ]
then
    systemctl start livepatching.service >/dev/null 2>&1 || :
fi

%preun subscription
%systemd_preun livepatching.service

%postun subscription
%systemd_postun_with_restart livepatching.service
systemctl try-restart livepatching.service >/dev/null 2>&1 || :

%files filesystem
%defattr(-,root,root)
%dir %{livepatching_lib_path}

%files subscription
%defattr(-,root,root)
%{_libdir}/systemd/system-preset/50-livepatching.preset
%{_unitdir}/livepatching.service
%{livepatching_lib_path}/livepatching.systemd

%changelog
* Fri Sep 02 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.0-1
- Original version for CBL-Mariner.
- License verified.
