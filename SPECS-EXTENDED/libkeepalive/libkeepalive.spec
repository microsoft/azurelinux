Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:		libkeepalive
Version:	0.3
Release:	13%{?dist}
Summary:	Enable TCP keepalive in dynamic binaries
URL:		https://libkeepalive.sourceforge.net/

BuildRequires:	gcc

License:	MIT
Source0:	https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

# All patches sent to the upstream maintainer directly via email.
Patch1:		0001-Add-vim-modelines-to-source-files.patch
Patch2:		0002-test-test.c-Whitespace-cleanup.patch
Patch3:		0003-test-Implement-self-test-functionality.patch
Patch4:		0004-Makefile-Make-self-test-accessible-by-make-test.patch
Patch5:		0005-Makefile-Allow-setting-custom-compiler-flags.patch

%description
libkeepalive is a library that enables tcp keepalive features in glibc based
binary dynamic executables, without any change in the original program.

%prep
%autosetup -p1

%build
export CFLAGS="%{optflags}"
export LDFLAGS="%{__global_ldflags}"
%make_build

%check
make test

%install
# install the file in src not topdir - the latter is stripped already
install -p -m 0755 -D src/libkeepalive.so %{buildroot}%{_libdir}/libkeepalive.so

%files
%license LICENSE
%doc README
%{_libdir}/libkeepalive.so

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.3-13
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.3-8
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 05 2016 Phil Sutter <psutter@redhat.com> - 0.3-3
- Use %%autosetup flag '-p1' instead of '-S git' to get rid of git dependency.
- Use %%license macro in %%files section.
- Added comment about included patches' upstream status.

* Fri Nov 25 2016 Phil Sutter <psutter@redhat.com> - 0.3-2
- Add missing build requirement: gcc.
- Add source code patches to facilitate following changes.
- Patches managed in git, so add git as another build requirement.
- Respect build system compiler flags.
- Use %%make_build instead of plain make in %%build.
- Add %%check target which performs unattended runtime test.
- Use -D install flag instead of manual mkdir.

* Thu Nov 17 2016 Phil Sutter <psutter@redhat.com> - 0.3-1
- Initial packaging.

