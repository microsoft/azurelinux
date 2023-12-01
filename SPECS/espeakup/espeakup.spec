Summary:        Connector for espeak and speakup
Name:           espeakup
Version:        0.80
Release:        2%{?dist}
License:        GPLv3
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/williamh/espeakup
#Source0:       https://github.com/williamh/%{name}/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.conf
Source2:        %{name}.service
Patch0:         unicode-device.patch
Patch1:         speaking-spaces.patch
Patch2:         support-pauses.patch
Patch3:         default-voice.patch
Patch4:         missing-mutex-calls.patch
BuildRequires:  espeak-ng-devel
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  systemd
Requires:       espeak-ng
Requires:       kernel-drivers-accessibility
Requires:       systemd

%description
espeakup is a light weight connector for espeak and speakup.

%prep
%autosetup

%build
make %{_smp_mflags}

%install
make DESTDIR=%{buildroot} PREFIX=%{_prefix} install
mkdir -p %{buildroot}%{_libdir}/modules-load.d
install -m755 %{SOURCE1} %{buildroot}%{_libdir}/modules-load.d/%{name}.conf
mkdir -p %{buildroot}%{_libdir}/systemd/system
install -m755 %{SOURCE2} %{buildroot}%{_libdir}/systemd/system/%{name}.service

# %check
# This package has no check section as of version 0.80

%files
%defattr(-,root,root)
%license COPYING
%doc ChangeLog README
%{_bindir}/%{name}
%{_libdir}/systemd/system/%{name}.service
%{_libdir}/modules-load.d/%{name}.conf
%{_mandir}/man8/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 0.80-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Jan 07 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.80-1
- Original version for CBL-Mariner (license: MIT)
- License verified
