Summary:        Light-weight cryptographic and SSL/TLS library
Name:           mbedtls
Version:        2.28.3
Release:        1%{?dist}
Summary:        Light-weight cryptographic and SSL/TLS library
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.trustedfirmware.org/projects/mbed-tls
Source:         https://github.com/Mbed-TLS/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz
BuildRequires: cmake
BuildRequires: doxygen
BuildRequires: gcc-c++
BuildRequires: graphviz
BuildRequires: make
BuildRequires: perl-interpreter
BuildRequires: python3
Obsoletes: mbedtls-utils < 2.28.0-1
Obsoletes: mbedtls-static < 2.28.0-1
 

%description
Mbed TLS is a light-weight open source cryptographic and SSL/TLS
library written in C. Mbed TLS makes it easy for developers to include
cryptographic and SSL/TLS capabilities in their (embedded)
applications with as little hassle as possible.

 
%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

 
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
 

%package        doc
Summary:        Documentation files for %{name}
BuildArch:      noarch
 

%description    doc
The %{name}-doc package contains documentation.

 
%prep
%autosetup
sed -i 's|//\(#define MBEDTLS_HAVEGE_C\)|\1|' include/mbedtls/config.h
sed -i 's|//\(#define MBEDTLS_THREADING_C\)|\1|' include/mbedtls/config.h
sed -i 's|//\(#define MBEDTLS_THREADING_PTHREAD\)|\1|' include/mbedtls/config.h
 

%build
export CFLAGS="%{optflags} -Wno-stringop-overflow -Wno-maybe-uninitialized"
export CXXLAGS="%{optflags} -Wno-stringop-overflow -Wno-maybe-uninitialized"
 
%cmake \
	-DCMAKE_BUILD_TYPE=Release \
	-DLINK_WITH_PTHREAD=ON \
	-DINSTALL_MBEDTLS_HEADERS=ON \
	-DENABLE_PROGRAMS=OFF \
	-DUSE_SHARED_MBEDTLS_LIBRARY=ON \
	-DUSE_STATIC_MBEDTLS_LIBRARY=OFF \
	-DGEN_FILES=OFF
 
%cmake_build
make apidoc
 

%install
%cmake_install
# Library files aren't supposed to be executable, but RPM requires this historically
# for automatic per-file level automatic dependency generation at ELF binaries; see:
# - https://github.com/ARMmbed/mbedtls/commit/280165c9b39091c7c7ffe031430c7cf93ebc4dec
# - https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/PDD6RNQMII472HXM4XAUUWWZKKBGHPTO/
chmod 755 %{buildroot}%{_libdir}/*.so.*
 

%check
%ctest --output-on-failure --force-new-ctest-process --parallel 1
 
%ldconfig_scriptlets
%files
%doc ChangeLog
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_libdir}/*.so.*
 

%files devel
%{_includedir}/mbedtls/
%{_includedir}/psa/
%{_libdir}/*.so
 

%files doc
%doc apidoc/*
 

%changelog
* Mon Jul 10 2023 Saranya R <rsaranya@microsoft.com> - 2.28.3-1
- Initial CBL-Mariner import from Fedora 38 (license: MIT).
- License verified

* Thu Mar 30 2023 Morten Stevens <mstevens@fedoraproject.org> - 2.28.3-1
- Update to 2.28.3
 
* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.28.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild
 
* Fri Dec 16 2022 Benson Muite <benson_muite@emailplus.org> - 2.28.2-1
- Update to 2.28.2
- Update URLs
 
* Sat Oct 22 2022 Morten Stevens <mstevens@fedoraproject.org> - 2.28.1-1
- Update to 2.28.1
 
* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.28.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild
 
* Mon Jan 31 2022 Morten Stevens <mstevens@fedoraproject.org> - 2.28.0-2
- Ensure ELF binary dependency generation and -debug{info,source} packages
- Remove deprecated PolarSSL dependency
 
* Sat Jan 22 2022 Morten Stevens <mstevens@fedoraproject.org> - 2.28.0-1
- Update to 2.28.0
- Dropped support for utils and static subpackage
 
* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild
 
* Sat Jan 01 2022 Morten Stevens <mstevens@fedoraproject.org> - 2.16.12-1
- Update to 2.16.12
 
* Sat Jul 24 2021 Morten Stevens <mstevens@fedoraproject.org> - 2.16.11-1
- Update to 2.16.11
 
* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild
 
* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild
 
* Mon Dec 14 2020 Morten Stevens <mstevens@fedoraproject.org> - 2.16.9-1
- Update to 2.16.9
 
* Thu Oct 15 2020 Morten Stevens <mstevens@fedoraproject.org> - 2.16.8-2
- Drop support for pkcs11 and zlib
 
* Tue Sep 08 2020 Morten Stevens <mstevens@fedoraproject.org> - 2.16.8-1
- Update to 2.16.8
 
* Thu Aug 20 2020 Morten Stevens <mstevens@fedoraproject.org> - 2.16.7-4
- Switch to cmake_build, cmake_install and ctest
- FTBFS in Fedora rawhide/f33 (#1864124)
 
* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.7-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
 
* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
 
* Tue Jul 14 2020 Morten Stevens <mstevens@fedoraproject.org> - 2.16.7-1
- Update to 2.16.7
- Security Advisory 2020-07
 
* Wed May 27 2020 Morten Stevens <mstevens@fedoraproject.org> - 2.16.6-1
- Update to 2.16.6
- Security Advisory 2020-04 (CVE-2020-10932)
 
* Tue Mar 03 2020 Morten Stevens <mstevens@fedoraproject.org> - 2.16.5-1
- Update to 2.16.5
 
* Mon Feb 10 2020 Morten Stevens <mstevens@fedoraproject.org> - 2.16.4-1
- Update to 2.16.4
 
* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
 
* Sat Sep 28 2019 Morten Stevens <mstevens@fedoraproject.org> - 2.16.3-1
- Update to 2.16.3
- Side channel attack on deterministic ECDSA (CVE-2019-16910)
 
* Tue Sep 03 2019 Morten Stevens <mstevens@fedoraproject.org> - 2.16.2-4
- devel package needs pkcs11-helper-devel (#1748468)
 
* Sat Aug 03 2019 Morten Stevens <mstevens@fedoraproject.org> - 2.16.2-3
- Fix building on RHEL8
 
* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
 
* Sat Jul 20 2019 Morten Stevens <mstevens@fedoraproject.org> - 2.16.2-1
- Update to 2.16.2
 
* Thu Mar 28 2019 Morten Stevens <mstevens@fedoraproject.org> - 2.16.1-1
- Update to 2.16.1
 
* Mon Feb 11 2019 Peter Robinson <pbrobinson@fedoraproject.org> 2.16.0-3
- devel package needs zlib-devel
 
* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
 
* Tue Jan 01 2019 Morten Stevens <mstevens@fedoraproject.org> - 2.16.0-1
- Update to 2.16.0
 
* Thu Dec 20 2018 Morten Stevens <mstevens@fedoraproject.org> - 2.14.1-2
- Spec file improvements
- Enabled zlib support
 
* Fri Dec 07 2018 Morten Stevens <mstevens@fedoraproject.org> - 2.14.1-1
- Update to 2.14.1
- CVE-2018-19608 (#1656784)
 
* Mon Dec 03 2018 Morten Stevens <mstevens@fedoraproject.org> - 2.14.0-1
- Update to 2.14.0
 
* Wed Sep 19 2018 Morten Stevens <mstevens@fedoraproject.org> - 2.13.0-1
- Update to 2.13.0
 
* Fri Jul 27 2018 Morten Stevens <mstevens@fedoraproject.org> - 2.12.0-1
- Update to 2.12.0
- Security Advisory 2018-02 (CVE-2018-0497)
 
* Mon Jul 16 2018 Morten Stevens <mstevens@fedoraproject.org> - 2.11.0-3
- BuildRequire gcc-c++ (https://fedoraproject.org/wiki/Packaging:C_and_C%2B%2B)
* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
 
* Mon Jul 09 2018 Morten Stevens <mstevens@fedoraproject.org> - 2.11.0-1
- Update to 2.11.0
 
* Wed May 16 2018 Morten Stevens <mstevens@fedoraproject.org> - 2.9.0-1
- Update to 2.9.0
 
* Fri Apr 06 2018 Morten Stevens <mstevens@fedoraproject.org> - 2.8.0-1
- Update to 2.8.0
 
* Tue Feb 06 2018 Morten Stevens <mstevens@fedoraproject.org> - 2.7.0-1
- Update to 2.7.0
- Enable pthread support (#1533435)
- Security Advisory 2018-01 (CVE-2018-0488)
 
* Tue Aug 29 2017 Morten Stevens <mstevens@fedoraproject.org> - 2.6.0-1
- Update to 2.6.0
 
* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild
 
* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild
 
* Mon Jun 26 2017 Morten Stevens <mstevens@fedoraproject.org> - 2.5.1-3
- Reenable ctest
 
* Fri Jun 23 2017 Morten Stevens <mstevens@fedoraproject.org> - 2.5.1-2
- Disable ctest due a bug on s390x
 
* Wed Jun 21 2017 Morten Stevens <mstevens@fedoraproject.org> - 2.5.1-1
- Update to 2.5.1
 
* Wed Mar 29 2017 David Sommerseth <davids@openvpn.net> - 2.4.2-2
- Enable PKCS#11 support
 
* Sat Mar 11 2017 Morten Stevens <mstevens@fedoraproject.org> - 2.4.2-1
- Update to 2.4.2
 
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild
 
* Mon Oct 31 2016 Morten Stevens <mstevens@fedoraproject.org> - 2.4.0-1
- Update to 2.4.0
 
* Thu Jun 30 2016 Morten Stevens <mstevens@fedoraproject.org> - 2.3.0-1
- Update to 2.3.0
 
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
 
* Sat Jan 09 2016 Morten Stevens <mstevens@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1
 
* Sun Dec 27 2015 Morten Stevens <mstevens@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0
 
* Mon Oct 12 2015 Morten Stevens <mstevens@fedoraproject.org> - 2.1.2-1
- Update to 2.1.2
- CVE-2015-5291
 
* Fri Sep 11 2015 Morten Stevens <mstevens@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0
 
* Wed Jul 22 2015 Morten Stevens <mstevens@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0
 
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild
 
* Fri Jun 05 2015 Morten Stevens <mstevens@fedoraproject.org> - 1.3.11-1
- Update to 1.3.11
 
* Mon Jun 01 2015 Robert Scheck <robert@fedoraproject.org> - 1.3.10-2
- Spec file changes to cover Red Hat Enterprise Linux 5 and 6
 
* Thu May 14 2015 Morten Stevens <mstevens@fedoraproject.org> - 1.3.10-1
- Initial Fedora Package
- Added subpackage for documentation files
- Added subpackage for static files
