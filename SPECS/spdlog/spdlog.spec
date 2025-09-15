Summary:        Super fast C++ logging library
Name:           spdlog
Version:        1.15.2
Release:        2%{?dist}
License:        MIT
URL:            https://github.com/gabime/%{name}
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Patch0:         %{name}-fmt_external.patch
BuildRequires:  catch-devel >= 3.0.0
BuildRequires:  fmt-devel >= 10.0.0
BuildRequires:  systemd-devel
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ninja-build

%description
This is a packaged version of the gabime/spdlog C++ logging
library available at Github.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       libstdc++-devel
Requires:       fmt-devel

%description devel
The %{name}-devel package contains C++ header files for developing
applications that use %{name}.

%prep
%autosetup -p1
find . -name '.gitignore' -delete
sed -e "s,\r,," -i README.md
rm -f tests/catch.hpp

%build
%cmake -G Ninja \
    -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DCMAKE_BUILD_TYPE=Release \
    -DSPDLOG_BUILD_SHARED=ON \
    -DSPDLOG_BUILD_EXAMPLE=OFF \
    -DSPDLOG_BUILD_BENCH=OFF \
    -DSPDLOG_BUILD_TESTS=ON \
    -DSPDLOG_INSTALL=ON \
    -DSPDLOG_FMT_EXTERNAL=ON
%cmake_build

%check
%ctest

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_libdir}/lib%{name}.so.1.15*

%files devel
%doc example
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/cmake/%{name}
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Fri April 11 2025 Riken Maharjan <rmaharjan@microsoft.com> - 1.12.0-5
- Initial Azure Linux import from Fedora 43 (license: MIT)
- License Verified

* Fri Apr 26 2024 Frantisek Zatloukal <fzatlouk@redhat.com> - 1.12.0-4
- Flag that we use an external fmt

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jul 08 2023 Vitaly Zaitsev <vitaly@easycoding.org> - 1.12.0-1
- Updated to version 1.12.0.

* Mon May 29 2023 Vitaly Zaitsev <vitaly@easycoding.org> - 1.11.0-6
- Rebuilt due to fmt library update.

* Wed Mar 01 2023 Vitaly Zaitsev <vitaly@easycoding.org> - 1.11.0-5
- Ported to catch v3. Fixed FTBFS in ELN.

* Tue Feb 28 2023 Vitaly Zaitsev <vitaly@easycoding.org> - 1.11.0-4
- Fixed FTBFS in EPEL/ELN due to catch v3 update.

* Tue Feb 28 2023 Vitaly Zaitsev <vitaly@easycoding.org> - 1.11.0-3
- Fixed FTBFS due to catch v3 update.

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Nov 03 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 1.11.0-1
- Updated to version 1.11.0.

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 10 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 1.10.0-2
- Rebuilt due to fmt library update.

* Mon Apr 18 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 1.10.0-1
- Updated to version 1.10.0.

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Sep 15 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 1.9.2-2
- Rebuilt due to google-benchmark 1.6.0 update.

* Fri Aug 13 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 1.9.2-1
- Updated to version 1.9.2.

* Tue Jul 27 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 1.9.1-1
- Updated to version 1.9.1.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 1.9.0-1
- Updated to version 1.9.0.

* Sun Jul 04 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 1.8.5-2
- Rebuilt due to fmt library update.

* Fri Apr 02 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 1.8.5-1
- Updated to version 1.8.5.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Dec 12 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 1.8.2-1
- Updated to version 1.8.2.

* Tue Oct 13 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 1.8.1-1
- Updated to version 1.8.1.

* Sat Sep 05 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 1.8.0-1
- Updated to version 1.8.0.

* Tue Jul 21 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 1.7.0-1
- Updated to version 1.7.0.

* Tue Jun 02 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 1.6.1-1
- Updated to version 1.6.1.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 27 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 1.5.0-1
- Updated to version 1.5.0.

* Wed Dec 18 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 1.4.2-1
- Updated to version 1.4.2.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jan 20 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 1.3.1-1
- Updated to version 1.3.1.

* Mon Nov 05 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.1-1
- Updated to version 1.2.1.

* Sun Sep 02 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.0-1
- Updated to version 1.1.0.

* Thu Aug 09 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.0-1
- Updated to version 1.0.0.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.17.0-1
- Updated to version 0.17.0.
- Added tests support.
- Added cmake and pkg-config support.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Sep 04 2016 Daniel Kopecek <dkopecek@redhat.com> - 0.10.0-1
- Update to 0.10.0

* Fri Jul 08 2016 Daniel Kopecek <dkopecek@redhat.com> - 0-8.20160703git34bb86b
- update to rev 34bb86b

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0-7.20151110gitcbc8ba7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Daniel Kopecek <dkopecek@redhat.com> - 0-6.20151110gitcbc8ba7
- update to rev cbc8ba7

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-5.20150410git211ce99
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 30 2015 Daniel Kopecek <dkopecek@redhat.com> - 0-4.20150410git211ce99
- don't build the base package
- remove a dot from the release tag
- corrected -devel subpackage description

* Mon Apr 20 2015 Daniel Kopecek <dkopecek@redhat.com> - 0-3.20150410git.211ce99
- use the -p option when copying the header files

* Tue Apr 14 2015 Daniel Kopecek <dkopecek@redhat.com> - 0-2.20150410git.211ce99
- don't build the debuginfo subpackage
- require libstdc++-devel
- don't generate a distribution specific pkg-config file

* Fri Apr 10 2015 Daniel Kopecek <dkopecek@redhat.com> - 0-1.20150410git.211ce99
- Initial package
