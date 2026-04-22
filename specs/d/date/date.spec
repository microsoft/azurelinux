# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# .so library version
%global abiver  3

Name:           date
Version:        3.0.4
Release: 2%{?dist}
Summary:        Date and time library based on the C++11/14/17 <chrono> header

License:        MIT
URL:            https://github.com/HowardHinnant/date
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
# add pkg-config support to make the package compatible with meson
# https://github.com/HowardHinnant/date/pull/538
Patch0:         output-date-pc-for-pkg-config.patch
# Adjust default value of USE_OS_TZDB macro to match Fedora build.
Patch1:         date-macro.patch

BuildRequires:  cmake >= 3.7
BuildRequires:  gcc-c++
# required for test suite
BuildRequires:  tzdata

%global _description %{expand:
This is actually several separate C++11/C++14/C++17 libraries:
 - "date.h" is a header-only library which builds upon <chrono>.
   It adds some new duration types, and new time_point types. It
   also adds "field" types such as year_month_day which is a
   struct {year, month, day}. And it provides convenient means
   to convert between the "field" types and the time_point types.
 - "tz.h" / "tz.cpp" are a timezone library built on top of the
   "date.h" library. This timezone library is a complete parser
   of the IANA timezone database. It provides for an easy way to
   access all of the data in this database, using the types from
   "date.h" and <chrono>. The IANA database also includes data
   on leap seconds, and this library provides utilities to compute
   with that information as well.
Slightly modified versions of "date.h" and "tz.h" were voted into
the C++20 standard.}

%description %{_description}


# only timezone libary has binary part
%package -n     libdate-tz
Summary:        Timezone library built on top of the date library
Requires:       tzdata

%description -n libdate-tz
Timezone library built on top of the date library. This timezone library
is a complete parser of the IANA timezone database. It provides for
an easy way to access all of the data in this database, using the types
from "date.h" and <chrono>. The IANA database also includes data on leap
seconds, and this library provides utilities to compute with that
information as well.


%package        devel
Summary:        Date and time library based on the C++11/14/17 <chrono> header
Requires:       libdate-tz%{?_isa} = %{version}-%{release}
# virtual Provide for header-only parts of the library
Provides:       %{name}-static = %{version}-%{release}

%description    devel %{_description}

%prep
%autosetup -p1 %{?date:-n %{name}-%{commit}}
# remove broken tests
# fails due to gcc std::locale bugs (gcc#86976, HowardHinnant/date#388)
rm -f test/date_test/parse.pass.cpp
# fails in fedora-rawhide-i386 due to missing timezone configuration
rm -f test/tz_test/zoned_time_deduction.pass.cpp
# one more test that depends on localtime. we don't even install this header
rm -rf test/solar_hijri_test/


%build
%cmake \
    -DBUILD_TZ_LIB=ON     \
    -DUSE_SYSTEM_TZ_DB=ON \
    -DENABLE_DATE_TESTING=ON
%cmake_build


%install
%cmake_install


%check
export CTEST_OUTPUT_ON_FAILURE=ON
%cmake_build -t testit


%files -n libdate-tz
%license LICENSE.txt
%{_libdir}/libdate-tz.so.%{abiver}*

%files devel
%license LICENSE.txt
%doc README.md
%{_includedir}/%{name}/
%{_libdir}/libdate-tz.so
%{_libdir}/cmake/%{name}/
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Sun Dec 28 2025 Aleksei Bavshin <alebastr@fedoraproject.org> - 3.0.4-1
- Update to 3.0.4

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1^20221213gitc9169ea-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1^20221213gitc9169ea-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1^20221213gitc9169ea-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1^20221213gitc9169ea-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1^20221213gitc9169ea-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1^20221213gitc9169ea-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1^20221213gitc9169ea-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 13 2022 Aleksei Bavshin <alebastr@fedoraproject.org> - 3.0.1^20221213gitc9169ea-1
- Update to new snapshot
- Convert License tag to SPDX
- Drop outdated Obsoletes: libtz

* Tue Dec 13 2022 Jonathan Wakely <jwakely@redhat.com> - 3.0.1^20210518git052eeba-5
- Add patch to set USE_OS_TZDB so it matches the Fedora package

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1^20210518git052eeba-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1^20210518git052eeba-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1^20210518git052eeba-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 15 2021 Aleksei Bavshin <alebastr@fedoraproject.org> - 3.0.1^20210518git052eeba-1
- Upstream release 3.0.1 (+ 2 fixes from git master)
- Apply new versioning guidelines for snapshots

* Tue Mar 30 2021 Jonathan Wakely <jwakely@redhat.com> - 3.0.0-5.20200708git6952fb5
- Rebuilt for removed libstdc++ symbol (#1937698)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-4.20200708git6952fb5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-3.20200708git6952fb5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-2.20200708git6952fb5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 08 2020 Aleksei Bavshin <alebastr89@gmail.com> - 3.0.0-1
- Upstream release 3.0.0 (+4 commits from git master)
- Rename libtz subpackage to libdate-tz according to upstream change
- Use new cmake_build macros with out-of-tree build

* Fri Feb 07 2020 Aleksei Bavshin <alebastr89@gmail.com> - 2.4.1-1.20200207git9a0ee254
- Initial import (#1801013)
