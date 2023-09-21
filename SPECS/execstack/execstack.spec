%global commit 4c79120bcdbde0616f592458ccde7035e92ca3d8
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Summary:        Utility to set/clear/query executable stack bit
Name:           execstack
Version:        0.5.0
Release:        21%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
# work around for missing upstream tarball with latest checkin
URL:            https://github.com/keszybz/prelink
Source0:        https://github.com/keszybz/prelink/archive/%{commit}.tar.gz#/prelink-%{shortcommit}.tar.gz
Patch0:         Add-PL_ARCH-for-AArch64.patch
BuildRequires:  elfutils-libelf-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  libselinux-devel
BuildRequires:  libselinux-utils

Requires:       coreutils
Requires:       findutils
Requires:       gawk
Requires:       glibc >= 2.2.4-18
Requires:       grep
Requires:       util-linux

%description
This package is built from prelink sources but contains just the
execstack binary. It can be used manipulate ELF binaries to run
with or without executable stack.

%prep
%autosetup -n prelink-%{commit} -p1 -Sgit

%build
sed -i -e '/^prelink_LDADD/s/$/ -lpthread/' src/Makefile.{am,in}
%configure
make %{?_smp_mflags} -C gelf
make %{?_smp_mflags} -C gelfx
make %{?_smp_mflags} -C gelfx32
make %{?_smp_mflags} -C src execstack

%check
cp src/execstack test
src/execstack -q test | grep '^-'
src/execstack -s test
src/execstack -q test | grep '^X'
src/execstack -c test
src/execstack -q test | grep '^-'

%install
install -D src/execstack %{buildroot}%{_bindir}/execstack
install -Dm0644 doc/execstack.8 %{buildroot}%{_mandir}/man8/execstack.8

%files
%license COPYING
%doc ChangeLog NEWS README TODO THANKS
%{_bindir}/execstack
%{_mandir}/man8/execstack.8.*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 0.5.0-21
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Apr 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.5.0-20
- Cleaning-up spec. License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.5.0-19
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Aug 21 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.5.0-9
- Add support for aarch64 (#1251165)

* Mon Jul 27 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.5.0-8
- Kill off most of prelink package
