# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Drop google-benchmark, gtest on RHEL
%bcond gbench %[ !0%{?rhel} ]
%bcond gtest %[ !0%{?rhel} ]

%global __cmake_in_source_build 1
Name:           snappy
Version:        1.2.2
Release: 3%{?dist}
Summary:        Fast compression and decompression library

License:        BSD-3-Clause
URL:            https://github.com/google/snappy
Source0:        https://github.com/google/snappy/releases/download/%{version}/%{name}-%{version}.tar.gz

# Remove dependency on bundled gtest and google-benchmark.
Patch0:         %{name}-thirdparty.patch

# Do not forcibly disable RTTI
Patch1:         %{name}-do-not-disable-rtti.patch

BuildRequires:  make
BuildRequires:  cmake
BuildRequires:  gcc-c++
%{?with_gbench:BuildRequires:  google-benchmark-devel}
%{?with_gtest:BuildRequires:  gtest-devel}

%description
Snappy is a compression/decompression library. It does not aim for maximum 
compression, or compatibility with any other compression library; instead, it 
aims for very high speeds and reasonable compression. For instance, compared to 
the fastest mode of zlib, Snappy is an order of magnitude faster for most 
inputs, but the resulting compressed files are anywhere from 20% to 100% 
bigger. 


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       cmake-filesystem
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup


%build
# gtest 1.13.0 requires C++14 or later
%cmake -DCMAKE_CXX_STANDARD=14 %{!?with_gbench:-DSNAPPY_BUILD_BENCHMARKS=OFF} %{!?with_gtest:-DSNAPPY_BUILD_TESTS=OFF} .
%make_build

# create pkgconfig file
cat << EOF >snappy.pc
prefix=%{_prefix}
exec_prefix=%{_exec_prefix}
includedir=%{_includedir}
libdir=%{_libdir}

Name: %{name}
Description: A fast compression/decompression library
Version: %{version}
Cflags: -I\${includedir}
Libs: -L\${libdir} -lsnappy
EOF


%install
rm -rf %{buildroot}
chmod 644 *.txt AUTHORS COPYING NEWS README.md
%make_install
install -m644 -D snappy.pc %{buildroot}%{_libdir}/pkgconfig/snappy.pc
rm -rf %{buildroot}%{_datadir}/doc/snappy/
rm -rf %{buildroot}%{_datadir}/doc/snappy-devel/

%check
ctest -V %{?_smp_mflags}


%ldconfig_scriptlets


%files
%license COPYING
%doc AUTHORS NEWS README.md
%{_libdir}/libsnappy.so.*

%files devel
%doc format_description.txt framing_format.txt
%{_includedir}/snappy*.h
%{_libdir}/libsnappy.so
%{_libdir}/pkgconfig/snappy.pc
%{_libdir}/cmake/Snappy/


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Mar 27 2025 Martin Gieseking <martin.gieseking@uos.de> - 1.2.2-1
- Updated to version 1.2.2

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Aug 15 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.2.1-3
- Disable google-benchmark on RHEL

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed May 22 2024 Martin Gieseking <martin.gieseking@uos.de> - 1.2.1-1
- Updated to version 1.2.1.

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 22 2023 Jiri Kucera <jkucera@redhat.com> - 1.1.10-2
- Drop gtest on RHEL, migrate to SPDX license identifier

* Thu Mar 09 2023 Martin Gieseking <martin.gieseking@uos.de> - 1.1.10-1
- Updated to version 1.1.10.
- Removed snappy-inline.patch as it's no longer required.

* Tue Jan 31 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.9-7
- Build with C++14 instead of C++11; gtest 1.13.0 requires it

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 08 2021 Davide Cavalca <dcavalca@fedoraproject.org> - 1.1.9-2
- Do not forcibly disable RTTI

* Sat May 15 2021 Martin Gieseking <martin.gieseking@uos.de> - 1.1.9-1
- Updated to new release.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 24 2020 Jeff Law <law@redhat.com> - 1.1.8-3
- Use __cmake_in_source_build

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 15 2020 Martin Gieseking <martin.gieseking@uos.de> - 1.1.8-1
- Updated to new release.
- Dropped version-related patch which has been applied upstream (BZ #1527850).

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 25 2019 Martin Gieseking <martin.gieseking@uos.de> - 1.1.7-8
- Moved cmake files to proper directory (BZ #1679727).

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 19 2018 Martin Gieseking <martin.gieseking@uos.de> - 1.1.7-5
- Added BR: gcc-c++ according to new packaging guidelines.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.1.7-3
- Switch to %%ldconfig_scriptlets

* Wed Dec 20 2017 Martin Gieseking <martin.gieseking@uos.de> - 1.1.7-2
- Fixed https://bugzilla.redhat.com/show_bug.cgi?id=1527850

* Fri Aug 25 2017 Martin Gieseking <martin.gieseking@uos.de> - 1.1.7-1
- Updated to new release.
- Build with CMake since autotool support is deprecated.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 28 2017 Martin Gieseking <martin.gieseking@uos.de> - 1.1.4-2
- Rebuilt with https://github.com/google/snappy/archive/1.1.4.tar.gz since
  %%{source0} contains different and buggy code.
  https://groups.google.com/forum/#!topic/snappy-compression/uhELq553TrI

* Sat Jan 28 2017 Martin Gieseking <martin.gieseking@uos.de> - 1.1.4-1
- Updated to new release.
- Added pkgconfig file now coming with the sources.

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 14 2015 Martin Gieseking <martin.gieseking@uos.de> 1.1.3-1
- Updated to new release.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.1.1-5
- Rebuilt for GCC 5 C++11 ABI change

* Wed Feb 25 2015 Martin Gieseking <martin.gieseking@uos.de> 1.1.1-4
- Rebuilt for new GCC 5.0 ABI.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 24 2014 Martin Gieseking <martin.gieseking@uos.de> 1.1.1-1
- Updated to new release.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 06 2013 Martin Gieseking <martin.gieseking@uos.de> 1.1.0-1
- updated to new release

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 24 2012 Martin Gieseking <martin.gieseking@uos.de> 1.0.5-1
- updated to release 1.0.5
- made dependency of devel package on base package arch dependant

* Tue Jan 17 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.0.4-3
- Add in buildroot stuff for EL5 build

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 16 2011 Martin Gieseking <martin.gieseking@uos.de> 1.0.4-1
- updated to release 1.0.4

* Sat Jun 04 2011 Martin Gieseking <martin.gieseking@uos.de> 1.0.3-1
- updated to release 1.0.3
- added format description to devel package

* Fri Apr 29 2011 Martin Gieseking <martin.gieseking@uos.de> 1.0.2-1
- updated to release 1.0.2
- changed License to BSD
- dropped the patch as it has been applied upstream

* Thu Mar 24 2011 Martin Gieseking <martin.gieseking@uos.de> 1.0.0-3
- added file COPYING from the upstream repo

* Thu Mar 24 2011 Martin Gieseking <martin.gieseking@uos.de> 1.0.0-2
- replaced $CXXFLAGS with %%{optflags} in %%build section
- removed empty %%doc entry from %%files devel

* Thu Mar 24 2011 Martin Gieseking <martin.gieseking@uos.de> 1.0.0-1
- initial package

