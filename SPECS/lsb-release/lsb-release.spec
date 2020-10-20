%define LICENSE_PATH LICENSE.PTR
Summary:       lsb_release script
Name:          lsb-release
Version:       1.4
Release:       1%{?dist}
License:       GPLv2+
URL:           https://wiki.linuxfoundation.org/lsb/start
Vendor:        Microsoft
Distribution:  Mariner
BuildArch:     noarch
Source0:       https://downloads.sourceforge.net/lsb/%{name}-%{version}.tar.gz
Source1:       %{LICENSE_PATH}
BuildRequires: coreutils
BuildRequires: gzip
Requires:      mariner-release

%description
lsb_release prints certain LSB (Linux Standard Base) and Distribution information.

%prep
%setup -q
cp %{SOURCE1} .

%install
./help2man -N --include ./lsb_release.examples --alt_version_key=program_version ./lsb_release > lsb_release.1
gzip -9f lsb_release.1
install -D -m 644 lsb_release.1.gz %{buildroot}%{_mandir}/man1/lsb_release.1.gz
install -D -m 755 lsb_release %{buildroot}%{_bindir}/lsb_release

%files
%license %{LICENSE_PATH}
%{_bindir}/lsb_release
%{_mandir}/man1/lsb_release.1.gz

%changelog
*   Wed Aug 26 2020 Thomas Crain <thcrain@microsoft.com> - 1.4-1
-   Original version for Mariner.
