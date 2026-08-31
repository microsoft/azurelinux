# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global debug_package %{nil}
%global test_data_version 3.1.0
%global bundled_hedley_version 15

Name:           json
Version:        3.11.3
Release:        4%{?dist}

# The entire source is MIT except
# include/nlohmann/thirdparty/hedley/hedley.hpp, which is CC0-1.0
License:        MIT AND CC0-1.0
Summary:        JSON for Modern C++
URL:            https://github.com/nlohmann/%{name}
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/nlohmann/json_test_data/archive/v%{test_data_version}/json_test_data-%{test_data_version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build

# Build requirements for the tests.
BuildRequires:  doctest-devel
BuildRequires:  gawk

%description
This is a packages version of the nlohmann/json header-only C++
library available at Github.

%package devel
Summary:        Development files for %{name}
Provides:       %{name}-static = %{?epoch:%{epoch}:}%{version}-%{release}
# This package is also known as nlohmann-json, provide some alternate names
# to make it easier to find
Provides:       nlohmann-json-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       nlohmann-json-static = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       nlohmann_json-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       nlohmann_json-static = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       bundled(hedley) = %{bundled_hedley_version}
Requires:       libstdc++-devel%{?_isa}

%description devel
The %{name}-devel package contains C++ header files for developing
applications that use %{name}.

%prep
%autosetup -p1
%setup -q -D -T -a1

# Unbundle doctest. Used only in tests.
ln -svf %{_includedir}/doctest/doctest.h ./tests/thirdparty/doctest/doctest.h

%build
%cmake -G Ninja \
    -DJSON_BuildTests:BOOL=ON \
    -DJSON_Install:BOOL=ON \
    -DJSON_MultipleHeaders:BOOL=ON \
    -DJSON_TestDataDirectory:STRING=json_test_data-%{test_data_version} \
%cmake_build

%check
%ctest --label-exclude 'git_required' --timeout 3600

# Verify version of virtual Provides for bundled Hedley matches actual header
[ "$(awk '
/^[[:blank:]]*#[[:blank:]]*define[[:blank:]]+JSON_HEDLEY_VERSION[[:blank:]]/ {
  print $NF }' include/nlohmann/thirdparty/hedley/hedley.hpp
)" = '%{bundled_hedley_version}' ]

%install
%cmake_install

%files devel
%doc README.md
%license LICENSE.MIT
%{_includedir}/nlohmann/
%{_datadir}/cmake/nlohmann_json/
%{_datadir}/pkgconfig/nlohmann_json.pc

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 13 2024 Jonathan Steffan <jsteffan@fedoraproject.org> - 3.11.3-1
- Update to 3.11.3

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Dec 23 2023 Davide Cavalca <dcavalca@fedoraproject.org> - 3.11.2-5
- Add provides for nlohmann-json and nlohmann_json as alternate names

* Mon Oct 09 2023 Carl George <carlwgeorge@fedoraproject.org> - 3.11.2-4
- Add patches to fix test failures under GCC 13

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Aug 14 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 3.11.2-1
- Updated to version 3.11.2.

* Wed Aug 03 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 3.11.1-1
- Updated to version 3.11.1.

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 04 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 3.10.5-1
- Updated to version 3.10.5.

* Sat Oct 23 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 3.10.4-1
- Updated to version 3.10.4.

* Fri Oct 08 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 3.10.3-1
- Updated to version 3.10.3.

* Thu Aug 26 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 3.10.2-1
- Updated to version 3.10.2.

* Wed Aug 25 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 3.10.1-1
- Updated to version 3.10.1.

* Wed Aug 18 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 3.10.0-1
- Updated to version 3.10.0.
- Switched to multi-headers version.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Mar 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 3.9.1-4
- Handle bundled Hedley: add virtual Provides and commentary, and incorporate
  its license in the License field

* Fri Mar 26 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 3.9.1-3
- Unbundle doctest

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Aug 06 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 3.9.1-1
- Updated to version 3.9.1.

* Mon Jul 27 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 3.9.0-1
- Updated to version 3.9.0.

* Wed Jun 24 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 3.8.0-2
- Backported upstream patches with build and tests fixes.

* Mon Jun 15 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 3.8.0-1
- Updated to version 3.8.0.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 20 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 3.7.3-1
- Updated to version 3.7.3.

* Mon Nov 11 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 3.7.2-1
- Updated to version 3.7.2.

* Thu Nov 07 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 3.7.1-1
- Updated to version 3.7.1.

* Sat Aug 17 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 3.7.0-1
- Updated to version 3.7.0.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 21 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 3.6.1-1
- Updated to version 3.6.1.

* Wed Mar 20 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 3.6.0-1
- Updated to version 3.6.0.

* Mon Feb 04 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 3.5.0-3
- Fixed FTBFS on Fedora 30.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 07 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 3.5.0-1
- Updated to version 3.5.0.

* Mon Nov 05 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 3.4.0-1
- Updated to version 3.4.0.

* Mon Oct 08 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 3.3.0-1
- Updated to version 3.3.0.

* Thu Oct 04 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 3.2.0-3
- Fixed build under RHEL/CentOS 7 due to missing ctest executable.

* Thu Oct 04 2018 Simone Caronni <negativo17@gmail.com> - 3.2.0-2
- Add support for RHEL/CentOS 7.
- Remove unneeded build requirement.
- Remove obsolete group tag.

* Tue Aug 21 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 3.2.0-1
- Updated to version 3.2.0.

* Wed Jul 25 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 3.1.2-2
- Added symlink to legacy path.

* Tue Jul 17 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 3.1.2-1
- Updated to version 3.1.2.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug 02 2016 Daniel Kopecek <dkopecek@redhat.com> - 2.0.2-1
- update to latest upstream release v2.0.2

* Thu Jul 07 2016 Daniel Kopecek <dkopecek@redhat.com> - 2.0.1-1
- update to latest upstream release v2.0.1

* Mon May 16 2016 Daniel Kopecek <dkopecek@redhat.com> - 1.1.0-1
- update to latest upstream release v1.1.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0-7.20151110git3948630
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Daniel Kopecek <dkopecek@redhat.com> - 0-6.20151110git3948630
- update to rev 3948630

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-5.20150410gitd7d0509
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 30 2015 Daniel Kopecek <dkopecek@redhat.com> - 0-4.20150410gitd7d0509
- don't build the base package
- removed a dot from the release tag
- corrected -devel subpackage description

* Tue Apr 14 2015 Daniel Kopecek <dkopecek@redhat.com> - 0-3.20150410git.d7d0509
- added patch to fix compilation of json_unit with gcc-5.x

* Tue Apr 14 2015 Daniel Kopecek <dkopecek@redhat.com> - 0-2.20150410git.d7d0509
- run json_unit target from the check section
- document catch.hpp license
- don't build the debuginfo subpackage
- don't generate a distribution specific pkg-config file

* Fri Apr 10 2015 Daniel Kopecek <dkopecek@redhat.com> - 0-1.20150410git.d7d0509
- Initial package
