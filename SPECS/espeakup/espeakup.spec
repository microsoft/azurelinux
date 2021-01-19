Summary:        Connector for espeak and speakup
Name:           espeakup
Version:        0.80
Release:        1%{?dist}
License:        GPLv3
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/williamh/espeakup
#Source0:       https://github.com/williamh/%{name}/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.conf
Source2:        %{name}.service
BuildRequires:  espeak-ng-devel
BuildRequires:  gcc
BuildRequires:  make
Requires:       espeak-ng

%description
espeakup is a light weight connector for espeak and speakup.

%prep
%autosetup

%build
make

%install
make DESTDIR=%{buildroot} PREFIX=%{_prefix} install
install -m755 %{SOURCE1} %{buildroot}%{_libdir}/modules-load.d/%{name}.conf
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
* Thu Jan 07 2021 Thomas Crain <thcrain@microsoft.com> - 0.80-1
- Initial version for CBL-Mariner (license: MIT)
