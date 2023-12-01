Summary:        A fast and lightweight key/value database library by Google
Name:           leveldb
Version:        1.23
Release:        3%{?dist}
License:        BSD
URL:            https://github.com/google/leveldb
Vendor:         Microsoft Corporation
Distribution:   Mariner

# leveldb git repo contains submodules that must be part of source tarball (adapt version number)
# 1) clone git repo                           => 'git clone https://github.com/google/leveldb.git'
# 2) checkout tag corresponding to version    => 'git checkout 1.23'
# 3) get submodule                            => 'git submodule init' then 'git submodule update'
# 4) create source tarball                    => 'tar --sort=name \
#                                                     --mtime="2021-04-26 00:00Z" \
#                                                     --owner=0 --group=0 --numeric-owner \
#                                                     --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#                                                     -czf leveldb-1.23.tar.gz leveldb'
Source0:        https://github.com/google/leveldb/archive/%{version}.tar.gz#//%{name}-%{version}.tar.gz

# available in https://github.com/fusesource/leveldbjni/blob/leveldb.patch
Patch0001:      0001-Allow-leveldbjni-build.patch
# https://github.com/fusesource/leveldbjni/issues/34
# https://code.google.com/p/leveldb/issues/detail?id=184
# Add DB::SuspendCompactions() and DB:: ResumeCompactions() methods
Patch0002:      0002-Added-a-DB-SuspendCompations-and-DB-ResumeCompaction.patch
# Cherry-picked from Basho's fork
Patch0003:      0003-allow-Get-calls-to-avoid-copies-into-std-string.patch
# https://groups.google.com/d/topic/leveldb/SbVPvl4j4vU/discussion
Patch0004:      0004-bloom_test-failure-on-big-endian-archs.patch
# -fno-rtti breaks ABI compatibility
Patch0006:      0006-revert-no-rtti.patch
# use installed gtest/gmock (if any)
Patch0007:      0007-detect-system-gtest.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gmock-devel
BuildRequires:  gtest-devel
BuildRequires:  make
BuildRequires:  snappy-devel
BuildRequires:  sqlite-devel

%description
LevelDB is a fast key-value storage library written at Google that provides an
ordered mapping from string keys to string values.

%package devel
Summary:        Development files for %{name}
Requires:       cmake
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -p1 -n %{name}

cat > %{name}.pc << EOF
prefix=%{_prefix}
exec_prefix=${prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: %{name}
Description: %{summary}
Version: %{version}
Libs: -l%{name}
EOF

%build
%cmake
%make_build

%install
%make_install
# remove 'benchmark' related files/folders
rm -f  %{buildroot}%{_libdir}/libbenchmark*.*
rm -f  %{buildroot}%{_libdir}/pkgconfig/benchmark.pc
rm -rf %{buildroot}%{_libdir}/cmake/benchmark
rm -rf %{buildroot}%{_includedir}/benchmark

mkdir -p %{buildroot}%{_libdir}/pkgconfig
cp -a %{name}.pc %{buildroot}%{_libdir}/pkgconfig/

%check
ctest -V %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc AUTHORS README.md NEWS
%{_libdir}/lib%{name}.so.*

%files devel
%doc doc/ CONTRIBUTING.md TODO
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}/

%changelog
* Thu Apr 06 2023 Bala <balakumaran.kannan@microsoft.com> 1.23.3
- Remove __cmake_in_source_build macro undefine to match make_build with cmake

* Wed Mar 23 2022 Nicolas Guibourge <nicolasg@microsoft.com> 1.23-2
- Address gmock-devel/snappy-devel incompatibility

* Mon Mar 21 2022 Nicolas Guibourge <nicolasg@microsoft.com> 1.23-1
- Upgrade to 1.23

* Fri Aug 21 2020 Olivia Crain <oliviacrain@microsoft.com> 1.22-3
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
- License verified

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Mar 29 2020 Kefu Chai <tchaikov@gmail.com> - 1.22-1
- Update to 1.22

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 09 2019 Peter Lemenkov <lemenkov@gmail.com> - 1.21-1
- Update to 1.21

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct 23 2017 Stephen Gallagher <sgallagh@redhat.com> - 1.20-1
- Update to 1.20
- Disable parallel make invocation to prevent build failures

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Aug 07 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.18-1
- Update to 1.18 (RHBZ #1306611)
- Cleanups and fixes in spec

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Tomas Hozza <thozza@redhat.com> - 1.12.0-9
- rebuild with newer gcc to resolve linking issues with Ceph

* Sun Mar  1 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.12.0-8
- F-23: rebuild for gcc5 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 25 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.12.0-5
- Don't build with assertions

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 10 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.12.0-3
- Backported Basho's patch (see rhbz#982980)

* Mon Jul 01 2013 gil cattaneo <puntogil@libero.it> 1.12.0-2
- add SuspendCompactions and ResumeCompactions methods for allow leveldbjni build

* Sat Jun 29 2013 gil cattaneo <puntogil@libero.it> - 1.12.0-1
- update to 1.12.0

* Wed Feb 27 2013 gil cattaneo <puntogil@libero.it> - 1.9.0-1
- update to 1.9.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Feb 07 2013 Karsten Hopp <karsten@redhat.com> 1.7.0-5
- temporarily ignore result of self checks on PPC* (rhbz #908800)

* Thu Nov 29 2012 gil cattaneo <puntogil@libero.it> - 1.7.0-4
- Applied patch for allow leveldbjni build

* Sat Oct 27 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.7.0-3
- Dirty workarounds for failed tests on ARM

* Sat Oct 27 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.7.0-2
- Restored patch no.2

* Sat Oct 27 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.7.0-1
- Ver. 1.7.0 (API/ABI compatible bugfix release)

* Tue Aug 21 2012 Dan Horák <dan[at]danny.cz> - 1.5.0-4
- add workaround for big endians eg. s390(x)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.5.0-2
- Cleaned up spec by removing EL5-related stuff
- Added notes about the patches

* Fri Jun 15 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.5.0-1
- Ver. 1.5.0

* Thu May 17 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.4.0-1
- Initial package
