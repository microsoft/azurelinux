%global proton_datadir %{_datadir}/proton
%global __cmake_in_source_build 1
 
%global __provides_exclude_from ^%{proton_datadir}/examples/.*$
%global __requires_exclude_from ^%{proton_datadir}/examples/.*$
 
%undefine __brp_mangle_shebangs
 
Name:           qpid-proton
Version:        0.40.0
Release:        15%{?dist}
Summary:        A high performance, lightweight messaging library
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
URL:            http://qpid.apache.org/proton/
 
Source0:        https://archive.apache.org/dist/qpid/proton/%{version}/%{name}-%{version}.tar.gz
Patch0:         proton.patch
Source1:        licenses.xml
 
%global proton_licensedir %{_licensedir}/proton
%{!?_licensedir:%global license %doc}
%{!?_licensedir:%global proton_licensedir %{proton_datadir}}
 
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  cmake
BuildRequires:  libuuid-devel
BuildRequires:  openssl-devel
BuildRequires:  cyrus-sasl-devel
BuildRequires:  cyrus-sasl-plain
BuildRequires:  cyrus-sasl-md5
BuildRequires:  doxygen
BuildRequires:  jsoncpp-devel
BuildRequires:  python3-devel
BuildRequires:  python3-build
BuildRequires:  python3-cffi
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx
BuildRequires:  python3-wheel
BuildRequires:  pkgconfig
BuildRequires:  python3-pyproject-hooks
 
 
%description
Proton is a high performance, lightweight messaging library. It can be used in
the widest range of messaging applications including brokers, client libraries,
routers, bridges, proxies, and more. Proton is based on the AMQP 1.0 messaging
standard. Using Proton it is trivial to integrate with the AMQP 1.0 ecosystem
from any platform, environment, or language.
 
 
%package c
Summary:   C libraries for Qpid Proton
Requires:  cyrus-sasl-lib
Obsoletes: qpid-proton
Obsoletes: perl-qpid-proton
 
%description c
%{summary}.
 
 
%files c
%dir %{proton_datadir}
%license %{proton_licensedir}/LICENSE.txt
%license %{proton_licensedir}/licenses.xml
%doc %{proton_datadir}/README*
%{_libdir}/libqpid-proton.so.*
%{_libdir}/libqpid-proton-core.so.*
%{_libdir}/libqpid-proton-proactor.so.*
 
%ldconfig_scriptlets c
 
 
%package   cpp
Summary:   C++ libraries for Qpid Proton
Requires:  qpid-proton-c%{?_isa} = %{version}-%{release}
Requires:  jsoncpp
#Requires:  opentelemetry-cpp
 
%description cpp
%{summary}.
 
%files cpp
%dir %{proton_datadir}
%doc %{proton_datadir}/README*
%{_libdir}/libqpid-proton-cpp.so.*
 
%ldconfig_scriptlets cpp
 
 
%package c-devel
Requires:  qpid-proton-c%{?_isa} = %{version}-%{release}
Summary:   Development libraries for writing messaging apps with Qpid Proton
Obsoletes: qpid-proton-devel
 
%description c-devel
%{summary}.
 
%files c-devel
%{_includedir}/proton
%exclude %{_includedir}/proton/*.hpp
%exclude %{_includedir}/proton/**/*.hpp
%{_libdir}/libqpid-proton.so
%{_libdir}/libqpid-proton-core.so
%{_libdir}/libqpid-proton-proactor.so
%{_libdir}/pkgconfig/libqpid-proton.pc
%{_libdir}/pkgconfig/libqpid-proton-core.pc
%{_libdir}/pkgconfig/libqpid-proton-proactor.pc
%{_libdir}/cmake/Proton
 
 
%package cpp-devel
Requires:  qpid-proton-cpp%{?_isa} = %{version}-%{release}
Requires:  qpid-proton-c-devel%{?_isa} = %{version}-%{release}
Summary:   Development libraries for writing messaging apps with Qpid Proton
 
%description cpp-devel
%{summary}.
 
%files cpp-devel
%{_includedir}/proton/*.hpp
%{_includedir}/proton/**/*.hpp
%{_libdir}/pkgconfig/libqpid-proton-cpp.pc
%{_libdir}/libqpid-proton-cpp.so
%{_libdir}/cmake/ProtonCpp
 
 
%package c-docs
Summary:   Documentation for the C development libraries for Qpid Proton
BuildArch: noarch
Obsoletes: qpid-proton-c-devel-doc
Obsoletes: qpid-proton-c-devel-docs
 
%description c-docs
%{summary}.
 
%files c-docs
%license %{proton_licensedir}/LICENSE.txt
%doc %{proton_datadir}/docs/api-c
%doc %{proton_datadir}/examples/README.md
%doc %{proton_datadir}/examples/c/ssl-certs
%doc %{proton_datadir}/examples/c/*.c
%doc %{proton_datadir}/examples/c/*.h
%doc %{proton_datadir}/examples/c/README.dox
%doc %{proton_datadir}/examples/c/CMakeLists.txt
 
 
%package   cpp-docs
Summary:   Documentation for the C++ development libraries for Qpid Proton
BuildArch: noarch
Obsoletes: qpid-proton-cpp-devel-doc
Obsoletes: qpid-proton-cpp-devel-docs
 
%description cpp-docs
%{summary}.
 
%files cpp-docs
%license %{proton_licensedir}/LICENSE.txt
%doc %{proton_datadir}/docs/api-cpp
%doc %{proton_datadir}/examples/cpp/*.cpp
%doc %{proton_datadir}/examples/cpp/*.hpp
%doc %{proton_datadir}/examples/cpp/README.dox
%doc %{proton_datadir}/examples/cpp/CMakeLists.txt
%doc %{proton_datadir}/examples/cpp/ssl-certs
%doc %{proton_datadir}/examples/cpp/tutorial.dox
 
 
%package -n python3-qpid-proton
Summary:  Python language bindings for the Qpid Proton messaging framework
Requires: qpid-proton-c%{?_isa} = %{version}-%{release}
Requires: python3
Provides: python%{python3_version}dist(python-%name)
%description -n python3-qpid-proton
%{summary}.
 
%files -n python3-qpid-proton
%{python3_sitearch}/__pycache__/*
%{python3_sitearch}/*.so
%{python3_sitearch}/*.py*
%{python3_sitearch}/proton
%{python3_sitearch}/python_qpid_proton-%{version}.dist-info
 
 
%package -n python-qpid-proton-docs
Summary:   Documentation for the Python language bindings for Qpid Proton
BuildArch: noarch
Obsoletes:  python-qpid-proton-doc
 
%description -n python-qpid-proton-docs
%{summary}.
 
%files -n python-qpid-proton-docs
%license %{proton_licensedir}/LICENSE.txt
%doc %{proton_datadir}/docs/api-py
%doc %{proton_datadir}/examples/python
 
 
%package tests
Summary:   Qpid Proton Tests
BuildArch: noarch
 
%description tests
%{summary}.
 
%files tests
%doc %{proton_datadir}/tests
 
 
%prep
%setup -q -n %{name}-%{version}
%patch -p1 0
# Buildroot provides Python 3.12; keep CMake minimum compatible after patching.
sed -i 's/find_package(Python 3.13/find_package(Python 3.9/' CMakeLists.txt
 
%build
mkdir -p BLD
cd BLD
%cmake \
    -DCMAKE_SKIP_RPATH:BOOL=OFF \
   "-DCMAKE_C_FLAGS=$CFLAGS -Wno-deprecated-declarations" \
    -DENABLE_FUZZ_TESTING=NO \
    -DENABLE_PYTHON_ISOLATED=NO \
    ..
make all docs %{?_smp_mflags}
 
 
%install
rm -rf %{buildroot}
 
cd BLD
%make_install
# Install the pre-built Python wheel using pip
if [ -f python/dist/*.whl ]; then
  %{__python3} -m pip install --no-deps --no-build-isolation --root %{buildroot} python/dist/*.whl
fi
# Strip the build extension to avoid buildroot references in debug info
strip %{buildroot}%{python3_sitearch}/cproton*.so 2>/dev/null || true
 
# clean up files that are not shipped
rm -rf %{buildroot}%{_exec_prefix}/bindings
rm -rf %{buildroot}%{_libdir}/java
rm -rf %{buildroot}%{_libdir}/libproton-jni.so
rm -rf %{buildroot}%{_datarootdir}/java
rm -rf %{buildroot}%{_libdir}/proton.cmake
rm -fr %{buildroot}%{proton_datadir}/examples/CMakeFiles
rm -f  %{buildroot}%{proton_datadir}/examples/Makefile
rm -f  %{buildroot}%{proton_datadir}/examples/*.cmake
rm -fr %{buildroot}%{proton_datadir}/examples/c/CMakeFiles
rm -f  %{buildroot}%{proton_datadir}/examples/c/*.cmake
rm -f  %{buildroot}%{proton_datadir}/examples/c/Makefile
rm -f  %{buildroot}%{proton_datadir}/examples/c/Makefile.pkgconfig
rm -f  %{buildroot}%{proton_datadir}/examples/c/broker
rm -f  %{buildroot}%{proton_datadir}/examples/c/direct
rm -f  %{buildroot}%{proton_datadir}/examples/c/receive
rm -f  %{buildroot}%{proton_datadir}/examples/c/send
rm -f  %{buildroot}%{proton_datadir}/examples/c/send-abort
rm -f  %{buildroot}%{proton_datadir}/examples/c/send-ssl
rm -f  %{buildroot}%{proton_datadir}/examples/c/raw_connect
rm -f  %{buildroot}%{proton_datadir}/examples/c/raw_echo
rm -fr %{buildroot}%{proton_datadir}/examples/cpp/CMakeFiles
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/*.cmake
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/Makefile
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/Makefile.pkgconfig
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/broker
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/client
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/connection_options
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/direct_recv
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/direct_send
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/encode_decode
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/flow_control
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/helloworld
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/helloworld_direct
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/queue_browser
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/scheduled_send_03
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/scheduled_send
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/selected_recv
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/server
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/server_direct
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/service_bus
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/simple_connect
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/simple_recv
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/simple_send
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/ssl
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/ssl_client_cert
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/message_properties
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/multithreaded_client
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/multithreaded_client_flow_control
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/reconnect_client
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/colour_send
rm -fr %{buildroot}%{proton_datadir}/examples/engine/java
rm -fr %{buildroot}%{proton_datadir}/examples/go
rm -fr %{buildroot}%{proton_datadir}/examples/java
rm -fr %{buildroot}%{proton_datadir}/examples/javascript
rm -fr %{buildroot}%{proton_datadir}/examples/perl
rm -fr %{buildroot}%{proton_datadir}/examples/php
rm -f  %{buildroot}%{proton_datadir}/CMakeLists.txt
 
install -dm 755 %{buildroot}%{proton_licensedir}
install -pm 644 %{SOURCE1} %{buildroot}%{proton_licensedir}
install -pm 644 %{buildroot}%{proton_datadir}/LICENSE.txt %{buildroot}%{proton_licensedir}
rm -f %{buildroot}%{proton_datadir}/LICENSE.txt
 
%check
 
%changelog
* Sat Apr 4 2026 Akarsh Chaudhary <v-akarshc@microsoft.com> - 0.40.0-15
- Initial CBL-Mariner import from Fedora 44 (license: MIT).
- License verified

* Sun Mar 22 2026 Björn Esser <besser82@fedoraproject.org> - 0.40.0-14
- Rebuild (jsoncpp)
 
* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild
 
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.40.0-12
- Rebuilt for Python 3.14.0rc3 bytecode
 
* Thu Aug 28 2025 Hirotaka Wakabayashi <hiwkby@yahoo.com> - 0.40.0-11
- Migrated the old macro
 
* Thu Aug 28 2025 Hirotaka Wakabayashi <hiwkby@yahoo.com> - 0.40.0-10
- Migrated the old macro
 
* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.40.0-9
- Rebuilt for Python 3.14.0rc2 bytecode
 
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild
 
* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.40.0-7
- Rebuilt for Python 3.14
 
* Thu Feb 27 2025 Björn Esser <besser82@fedoraproject.org> - 0.40.0-6
- Rebuild (jsoncpp)
 
* Fri Jan 24 2025 Hirotaka Wakabayashi <hiwkby@yahoo.com> - 0.40.0-5
- Add the warning workaround for std=++17 build flag.
 
* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild
 
* Thu Jan 16 2025 Hirotaka Wakabayashi <hiwkby@yahoo.com> - 0.40.0-3
- Fix Automatic Python Provides(rhbz#2243262)
 
* Wed Dec 04 2024 Hirotaka Wakabayashi <hiwkby@yahoo.com> - 0.40.0-2
- Update licenses.xml
 
* Fri Nov 29 2024 Hirotaka Wakabayashi <hiwkby@yahoo.com> - 0.40.0-1
- Rebased to 0.40.0
 
* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 0.38.0-10
- convert license to SPDX
 
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild
 
* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.38.0-8
- Rebuilt for Python 3.13
 
* Thu Mar 14 2024 Hirotaka Wakabayashi <hiwkby@yahoo.com> - 0.38.0-7
- Fixes the "machine-readable provides" bug
 
* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild
 
* Mon Jul 10 2023 Lukáš Zaoral <lzaoral@redhat.com> - 0.38.0-3
- Fix compatibility with Python 3.12 (rhbz#2220586)
 
* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 0.38.0-2
- Rebuilt for Python 3.12
 
* Fri Mar 31 2023 Kim van der Riet <kvanderr@redhat.com> - 0.38.0-1
- Rebased to 0.38.0, opentelemetry-cpp not included as no pkgs in Fedora yet.
 
* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.37.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild
 
* Wed Jan 04 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.37.0-4
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.2
 
* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.37.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild
 
* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.37.0-2
- Rebuilt for Python 3.11
 
* Tue Mar 22 2022 Kim van der Riet <kvanderr@redhat.com> - 0.37.0-1
- Rebased to 0.37.0
 
* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.36.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild
 
* Thu Jan 13 2022 Irina Boverman <iboverma@redhat.com> - 0.36.0-2
- Removed no longer needed code
 
* Tue Jan  4 2022 Irina Boverman <iboverma@redhat.com> - 0.36.0-1
- Rebased to 0.36.0
 
* Wed Nov 03 2021 Björn Esser <besser82@fedoraproject.org> - 0.35.0-4
- Rebuild (jsoncpp)
 
* Mon Oct 25 2021 Irina Boverman <iboverma@redhat.com> - 0.35.0-3
- Rebuilt with OpenSSL 3.0.0
 
* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.35.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild
 
* Fri Jul 16 2021 Kim van der Riet <kvanderr@redhat.com> - 0.35.0-1
- Rebased to 0.35.0
 
* Tue May  4 2021 Irina Boverman <iboverma@redhat.com> - 0.34.0-1
- Rebased to 0.34.0
 
* Tue Jan 19 2021 Irina Boverman <iboverma@redhat.com> - 0.33.0-1
- Rebased to 0.33.0
 
* Fri Oct  2 2020 Irina Boverman <iboverma@redhat.com> - 0.32.0-2
- Added temp fix to allow building c/cpp examples
 
* Thu Sep 24 2020 Irina Boverman <iboverma@redhat.com> - 0.32.0-1
- Rebased to 0.32.0
 
* Tue Jul 28 2020 Irina Boverman <iboverma@redhat.com> - 0.31.0-5
- Added rubygem-qpid_proton subpackage
 
* Mon Jun  1 2020 Irina Boverman <iboverma@redhat.com> - 0.31.0-4
- Corrected cmake for c/cpp examples
- Resolved PROTON-2228
 
* Sat May 30 2020 Björn Esser <besser82@fedoraproject.org> - 0.31.0-3
- Rebuild (jsoncpp)
 
* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.31.0-2
- Rebuilt for Python 3.9
 
* Thu May 14 2020 Irina Boverman <iboverma@redhat.com> - 0.30.0-1
- Rebased to 0.31.0
 
* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
 
* Mon Jan 20 2020 Irina Boverman <iboverma@redhat.com> - 0.30.0-1
- Rebased to 0.30.0
- Removed python2--qpid-proton
- Replaced epydoc with python3-sphinx
 
* Thu Nov 14 2019 Björn Esser <besser82@fedoraproject.org> - 0.29.0-2
- Rebuild (jsoncpp)
 
* Tue Oct  1 2019 Irina Boverman <iboverma@redhat.com> - 0.29.0-1
- Rebased to 0.29.0
 
* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.28.0-4
- Rebuilt for Python 3.8
 
* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.28.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
 
* Wed Jul 03 2019 Björn Esser <besser82@fedoraproject.org> - 0.28.0-2
- Rebuild (jsoncpp)
 
* Tue May 14 2019 Irina Boverman <iboverma@redhat.com> - 0.28.0-1
- Rebased to 0.28.0
 
* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
 
* Mon Jan  7 2019 Irina Boverman <iboverma@redhat.com> - 0.26.0-1
- Rebased to 0.26.0
 
* Tue Jul 31 2018 Irina Boverman <iboverma@redhat.com> - 0.24.0-4
- Added cmake arguments for python3 build
 
* Tue Jul 31 2018 Irina Boverman <iboverma@redhat.com> - 0.24.0-3
- Updated spec for %{python3_sitearch}/_cproton.so
 
* Thu Jul 26 2018 Irina Boverman <iboverma@redhat.com> - 0.24.0-2
- Updated to build both python2- and python3-qpid-proton packages
 
* Tue Jul 24 2018 Irina Boverman <iboverma@redhat.com> - 0.24.0-1
- Rebased to 0.24.0
 
* Wed Mar 14 2018 Irina Boverman <iboverma@redhat.com> - 0.21.0-2
- Updated per changes on master
 
* Tue Mar 13 2018 Irina Boverman <iboverma@redhat.com> - 0.21.0-1
- Rebased to 0.21.0
 
* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
 
* Mon Jan 29 2018 Merlin Mathesius <mmathesi@redhat.com> - 0.18.1-3
- Cleanup spec file conditionals
 
* Sun Dec 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.18.1-2
- Python 2 binary package renamed to python2-qpid-proton
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3
 
* Thu Nov 16 2017 Irina Boverman <iboverma@redhat.com> - 0.18.1-1
- Rebased to 0.18.1
 
* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.17.0-8
- Python 2 binary package renamed to python2-qpid-proton
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3
 
* Wed Aug  9 2017 Irina Boverman <iboverma@redhat.com> - 0.17.0-7
- Resolves: PROTON-1526
 
* Tue Aug  8 2017 Irina Boverman <iboverma@redhat.com> - 0.17.0-6
- Added missing *.hpp files in qpid-proton-cpp-devel package
 
* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.17.0-5
- Rebuild due to bug in RPM (RHBZ #1468476)
 
* Fri Jun 23 2017 Irina Boverman <iboverma@redhat.com> - 0.17.0-4
- Excluded *.hpp files from qpid-proton-c-devel
 
* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.17.0-3
- Perl 5.26 rebuild
 
* Wed May 10 2017 Irina Boverman <iboverma@redhat.com> - 0.17.0-2
- Added 0001-PROTON-1466-proton-c-mixing-up-links-with-names-that.patch
 
* Tue Feb 21 2017 Irina Boverman <iboverma@redhat.com> - 0.17.0-1
- Rebased to 0.17.0
- Added *cpp* packages
 
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild
 
* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.14.0-3
- Rebuild for Python 3.6
 
* Wed Nov  9 2016 Irina Boverman <iboverma@redhat.com> - 0.14.0-2
- Renamed sub-packages qpid-proton-c-devel-docs/qpid-proton-cpp-devel-docs
  to qpid-proton-c-docs/qpid-proton-cpp-docs
- Removed binary and derived files from qpid-proton-cpp-docs package
 
* Tue Sep 6  2016 Irina Boverman <iboverma@redhat.com> - 0.14.0-1
- Added "-std=c++11" flag
- Rebased to 0.14.0
 
* Mon Aug 1  2016 Irina Boverman <iboverma@redhat.com> - 0.13.1-1
- Rebased to 0.13.1
 
* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages
 
* Wed Jun 22 2016 Irina Boverman <iboverma@redhat.com> - 0.13.0-1
- Rebased to 0.13.0
- Changed *doc to *docs, moved examples to *docs
 
* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.12.1-2
- Perl 5.24 rebuild
 
* Wed Mar 23 2016 Irina Boverman <iboverma@redhat.com> - 0.12.1-1
- Rebased to 0.12.1
- Added python3 installation
 
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
 
* Tue Sep  8 2015 Irina Boverman <iboverma@redhat.com> - 0.10-2
- Added dependency on cyrus-sasl-devel and cyrus-sasl-lib
- Added 0001-PROTON-974-Accept-a-single-symbol-in-SASL-mechs-fram.patch
 
* Wed Sep  2 2015 Irina Boverman <iboverma@redhat.com> - 0.10-1
- Rebased to 0.10
 
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild
 
* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.9-4
- Perl 5.22 rebuild
 
* Wed Apr  8 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.9-3
- Added a global excludes macro to fix EL6 issues with example Perl modules.
 
* Wed Apr  8 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.9-2
- Marked the examples in -c-devel as doc.
- Turned off the executable flag on all files under examples.
 
* Mon Apr  6 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.9-1
- Rebased on Proton 0.9.
- Removed the proton binary from qpid-proton-c.
- Added the perl-qpid-proton subpackage.
 
* Tue Nov 18 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.8-1
- Rebased on Proton 0.8.
 
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild
 
* Tue Jul  8 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.7-3
- Removed intra-package comments which cause error messages on package uninstall.
 
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild
 
* Tue Apr 29 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.7-1
- Rebased on Proton 0.7
- Added new CMake modules for Proton to qpid-proton-c-devel.
 
* Mon Feb 24 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.6-2
- Reorganized the subpackages.
- Merged up branches to get things back into sync.
 
* Thu Jan 16 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.6-1
- Rebased on Proton 0.6.
- Update spec to delete ruby and perl5 directories if Cmake creates them.
- Removed Java sub-packages - those will be packaged separate in future.
 
* Fri Sep  6 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.5-2
- Made python-qpid-proton-doc a noarch package.
- Resolves: BZ#1005058
 
* Wed Aug 28 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.5-1
- Rebased on Proton 0.5.
- Resolves: BZ#1000620
 
* Mon Aug 26 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.4-4
- Created the qpid-proton-c-devel-doc subpackage.
- Resolves: BZ#1000615
 
* Wed Jul 24 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.4-3
- Provide examples for qpid-proton-c
- Resolves: BZ#975723
 
* Fri Apr  5 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.4-2.2
- Added Obsoletes and Provides for packages whose names changed.
- Resolves: BZ#948784
 
* Mon Apr  1 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.4-2.1
- Fixed the dependencies for qpid-proton-devel and python-qpid-proton.
 
* Thu Mar 28 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.4-2
- Moved all C libraries to the new qpid-proton-c subpackage.
 
* Tue Feb 26 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.4-1
- Rebased on Proton 0.4.
 
* Thu Feb 21 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.3-4
- Fixes copying nested data.
- PROTON-246, PROTON-230
 
* Mon Jan 28 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.3-3
- Fixes build failure on non-x86 platforms.
- Resolves: BZ#901526
 
* Fri Jan 25 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.3-2
- Fixes build failure on non-x86 platforms.
- Resolves: BZ#901526
 
* Wed Jan 16 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.3-1
- Rebased on Proton 0.3.
 
* Fri Dec 28 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.2-2.4
- Moved ownership of the docs dir to the docs package.
 
* Wed Dec 19 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.2-2.3
- Fixed package dependencies, adding the release macro.
 
* Mon Dec 17 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.2-2.2
- Fixed subpackage dependencies on main package.
- Removed accidental ownership of /usr/include.
 
* Thu Dec 13 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.2-2.1
- Remove BR for ruby-devel.
- Removed redundant package name from summary.
- Removed debugging artifacts from specfile.
- Moved unversioned library to the -devel package.
- Added dependency on main package to -devel.
- Fixed directory ownerships.
 
* Fri Nov 30 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.2-2
- Removed BR on help2man.
- Added patch for generated manpage.
 
* Mon Nov  5 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.2-1
- Initial packaging of the Qpid Proton.