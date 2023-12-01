Vendor:         Microsoft Corporation
Distribution:   Mariner
%global __cmake_in_source_build 1

Name: libipt
Version: 2.0.5
Release: 1%{?dist}
Summary: Intel Processor Trace Decoder Library
License: BSD
URL: https://github.com/intel/libipt
Source0: https://github.com/intel/libipt/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0: libipt-gcc11.patch
# c++ is required only for -DPTUNIT test "ptunit-cpp".
BuildRequires: gcc-c++ cmake
%if 0%{?_with_docs:1}
# pandoc is for -DMAN.
BuildRequires: pandoc
%endif
BuildRequires: make
ExclusiveArch: %{ix86} x86_64

%description
The Intel Processor Trace (Intel PT) Decoder Library is Intel's reference
implementation for decoding Intel PT.  It can be used as a standalone library
or it can be partially or fully integrated into your tool.

%ldconfig_scriptlets 

%package devel
Summary: Header files and libraries for Intel Processor Trace Decoder Library
Requires: %{name}%{?_isa} = %{version}-%{release}
ExclusiveArch: %{ix86} x86_64

%description devel
The %{name}-devel package contains the header files and libraries needed to
develop programs that use the Intel Processor Trace (Intel PT) Decoder Library.

%prep
%setup -q -n libipt-%{version}
%patch0 -p1

%build
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DPTUNIT:BOOL=ON \
%if 0%{?_with_docs:1}
       -DMAN:BOOL=ON \
%endif
       -DDEVBUILD:BOOL=ON \
       .
%make_build

%install
%make_install
%global develdocs howto_libipt.md
(cd doc;cp -p %{develdocs} ..)

%check
ctest -V %{?_smp_mflags}

%files
%doc README
%license LICENSE
%{_libdir}/%{name}.so.*

%files devel
%doc %{develdocs}
%{_includedir}/*
%{_libdir}/%{name}.so
%if 0%{?_with_docs:1}
%{_mandir}/*/*.gz
%endif

%changelog
* Fri Mar 04 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.5-1
- Updating to version 2.0.5 using Fedora 36 spec (license: MIT) for guidance.
- License verified.

* Thu Jun 17 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.0.1-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Conditionalize building of documentation

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 16 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 2.0.1-1
- Release v2.0.1.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Aug  8 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 2.0-1
- Release v2.0.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar  5 2018 Jan Kratochvil <jan.kratochvil@redhat.com> - 1.6.1-8
- Enable tests (PTUNIT) and man pages (MAN).
- Change BuildRequires: gcc -> gcc-c++ as PTUNIT tests require C++.

* Sat Mar  3 2018 Jan Kratochvil <jan.kratochvil@redhat.com> - 1.6.1-7
- Add: BuildRequires: gcc
  https://fedoraproject.org/wiki/Packaging:C_and_C%2B%2B#BuildRequires_and_Requires

* Fri Mar  2 2018 Jan Kratochvil <jan.kratochvil@redhat.com> - 1.6.1-6
- Fix v1.6.1-implicit-fallthrough.patch compatibility with gcc < 7.
- Use %%ldconfig_scriptlets.
  https://fedoraproject.org/wiki/Packaging:Scriptlets#Shared_Libraries

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun  9 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 1.6.1-2
- Fix [-Werror=implicit-fallthrough=] with gcc-7.1.1.

* Fri Jun  9 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 1.6.1-1
- Rebase to upstream 1.6.1.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Apr 11 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 1.5-1
- Rebase to upstream 1.5.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 1.4.4-1
- Rebase to upstream 1.4.4.

* Wed Oct 14 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 1.4.3-1
- Rebase to upstream 1.4.3.

* Mon Aug 31 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 1.4.2-1
- Initial Fedora packaging.
