# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: Library for producing small, fast columnar storage for Hadoop workloads
Name:    liborc
Version: 2.1.4
Release: 2%{?dist}
License: Apache-2.0
URL:     http://orc.apache.org/
Source:  https://downloads.apache.org/orc/orc-%{version}/orc-%{version}.tar.gz
Source1: https://downloads.apache.org/orc/orc-format-1.1.0/orc-format-1.1.0.tar.gz
Patch0001:	0001-cmake.patch
Patch0002:	0002-c++-src-CpuInfoUtil.cc.patch
# Apache ORC has numerous compile errors and apparently assumes a 64-bit
# build and runtime environment. The only consumer of this package is 
# Ceph (by way of Apache Arrow) which is also 64-bit only
ExcludeArch:   i686 armv7hl
BuildRequires: gnupg2
BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: protobuf-devel
BuildRequires: zlib-devel
BuildRequires: libzstd-devel
BuildRequires: lz4-devel
BuildRequires: snappy-devel

%description
ORC is a self-describing type-aware columnar file format designed
for Hadoop workloads. It is optimized for large streaming reads,
but with integrated support for finding required rows quickly.
Storing data in a columnar format lets the reader read, decompress,
and process only the values that are required for the current query.
Because ORC files are type-aware, the writer chooses the most
appropriate encoding for the type and builds an internal index as
the file is written. Predicate pushdown uses those indexes to
determine which stripes in a file need to be read for a particular
query and the row indexes can narrow the search to a particular set
of 10,000 rows. ORC supports the complete set of types in Hive,
including the complex types: structs, lists, maps, and unions.

%package -n %{name}2
Summary: Library for producing small, fast columnar storage for Hadoop workloads
Provides: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: %{name}1 < %{version}-%{release}

%description -n %{name}2
ORC is a self-describing type-aware columnar file format designed
for Hadoop workloads. It is optimized for large streaming reads,
but with integrated support for finding required rows quickly.
Storing data in a columnar format lets the reader read, decompress,
and process only the values that are required for the current query.
Because ORC files are type-aware, the writer chooses the most
appropriate encoding for the type and builds an internal index as
the file is written. Predicate pushdown uses those indexes to
determine which stripes in a file need to be read for a particular
query and the row indexes can narrow the search to a particular set
of 10,000 rows. ORC supports the complete set of types in Hive,
including the complex types: structs, lists, maps, and unions.

%package devel
Summary:  Header files, libraries and development documentation for %{name}
Requires: %{name}2 = %{version}-%{release}

%description devel
ORC is a self-describing type-aware columnar file format designed
for Hadoop workloads. It is optimized for large streaming reads,
but with integrated support for finding required rows quickly.
Storing data in a columnar format lets the reader read, decompress,
and process only the values that are required for the current query.
Because ORC files are type-aware, the writer chooses the most
appropriate encoding for the type and builds an internal index as
the file is written. Predicate pushdown uses those indexes to
determine which stripes in a file need to be read for a particular
query and the row indexes can narrow the search to a particular set
of 10,000 rows. ORC supports the complete set of types in Hive,
including the complex types: structs, lists, maps, and unions.

Contains header files for developing applications that use the %{name}
library.

%prep
%autosetup -p1 -n orc-%{version}

%build

echo "RPM_OPT_FLAGS: $RPM_OPT_FLAGS"
# https://src.fedoraproject.org/rpms/protobuf/pull-request/26#comment-183002
export CXXFLAGS="$RPM_OPT_FLAGS -Wno-error=dangling-reference -Wno-error=stringop-overflow"

%cmake \
    -DOVERRIDE_INSTALL_PREFIX=/usr \
    -DCMAKE_COLOR_MAKEFILE:BOOL=OFF \
    -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \
    -DINSTALL_LIBDIR:PATH=%{_libdir} \
    -DBUILD_SHARED_LIBS:BOOL=on \
    -DBUILD_LIBHDFSPP:BOOL=off \
    -DSNAPPY_HOME="$(pkg-config --variable=prefix snappy)" \
    -DLZ4_HOME="$(pkg-config --variable=prefix liblz4)" \
    -DZLIB_HOME="$(pkg-config --variable=prefix zlib)" \
    -DZSTD_HOME="$(pkg-config --variable=prefix libzstd)" \
    -DGTEST_HOME="$(pkg-config --variable=prefix gtest)" \
    -DPROTOBUF_HOME="$(pkg-config --variable=prefix protobuf)" \
    -Dorc_VERSION="%{version}" \
    -DBUILD_CPP_TESTS=off \
    -DBUILD_TOOLS=off \
    -DBUILD_JAVA=off \
    -DANALYZE_JAVA=off \
    "-GUnix Makefiles"
%cmake_build

%check

%install
%cmake_install
mkdir %{buildroot}%{_docdir}/%{name}2
mv %{buildroot}%{_docdir}/orc/NOTICE %{buildroot}%{_docdir}/%{name}2/
mkdir -p %{buildroot}/%{_defaultlicensedir}/%{name}2
mv %{buildroot}%{_docdir}/orc/LICENSE %{buildroot}/%{_defaultlicensedir}/%{name}2/
rm -f %{buildroot}/%{_includedir}/orc/._*.hh
rm -f %{buildroot}/%{_includedir}/orc/sargs/._*.hh

%ldconfig_scriptlets

%files -n %{name}2
%license LICENSE
%doc README.md NOTICE
%{_libdir}/liborc.so.*
%{_libdir}/cmake/orc/orcConfig*
%exclude %{_libdir}/cmake/orc/*
%exclude %{_libdir}/orcTargets*

%files devel
%dir %{_includedir}/orc
     %{_includedir}/orc/*.hh
%dir %{_includedir}/orc/sargs
     %{_includedir}/orc/sargs/*.hh
     %{_libdir}/liborc.so

%changelog
* Mon Jan 12 2026  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 2.1.4-1
- Apache ORC 2.1.4 GA

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 15 2025  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 2.1.3-1
- Apache ORC 2.1.3 GA

* Thu May 8 2025  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 2.1.2-1
- Apache ORC 2.1.2 GA

* Fri Apr 18 2025  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 2.1.1-2
- Apache ORC 2.1.1, with orc-format-1.1.0

* Thu Mar 13 2025  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 2.1.1-1
- Apache ORC 2.1.1 GA

* Thu Feb 6 2025  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 2.1.0-1
- Apache ORC 2.1.0

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Nov 20 2024  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 2.0.3-1
- Apache ORC 2.0.3

* Wed Oct 2 2024  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 2.0.2-1
- Apache ORC 2.0.2

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 18 2024  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 2.0.0-3
- 2.0.0, Obsoletes: liborc1

* Tue Jun 18 2024  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 2.0.0-2
- 2.0.0, liborc1 -> liborc2

* Fri Mar 15 2024  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 2.0.0-1
- 2.0.0 GA

* Wed Feb 14 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9.2-5
- Add -Wno-error=stringop-overflow

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 15 2023  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 1.9.2-2
- 1.9.2, rebuild for f40-build-side-76708

* Wed Nov 15 2023  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 1.9.2-1
- 1.9.2 GA

* Thu Aug 17 2023  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 1.9.1-1
- 1.9.1 GA

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 1.9.0-1
- 1.9.0 GA

* Wed Jun 14 2023  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 1.8.4-1
- 1.8.4 GA

* Thu Mar 16 2023  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 1.8.3-1
- 1.8.3 GA

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 1.8.2-1
- 1.8.2 GA (w/ gcc-13 -Wno-error=dangling-references)

* Mon Dec 5 2022  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 1.8.1-1
- 1.8.1 GA

* Fri Nov 11 2022  Kaleb S. KEITHLEY <kkeithle [at] redhat.com>
- SPDX migration

* Sun Sep 4 2022  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 1.8.0-1
- 1.8.0 GA

* Sun Sep 4 2022  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 1.7.6-2
- 1.7.6, fix shlib name

* Thu Aug 18 2022  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 1.7.6-1
- 1.7.6 GA

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 21 2022  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 1.7.5-1
- 1.7.5 GA

* Sun May 1 2022  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 1.7.4-1
- 1.7.4 GA

* Tue Feb 15 2022  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 1.7.3-2
- 1.7.3, fix SO_NAME

* Thu Feb 10 2022  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 1.7.3-1
- 1.7.3 GA

* Fri Aug 27 2021  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 1.6.6-1
- New upstream release.

