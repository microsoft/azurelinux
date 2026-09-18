# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:          bcg729
Version:       1.1.1
Release:       13%{?dist}
Summary:       Opensource implementation of the G.729 codec

License:       GPL-3.0-or-later
URL:           https://github.com/BelledonneCommunications/bcg729
Source0:       https://github.com/BelledonneCommunications/bcg729/archive/%{version}/%{name}-%{version}.tar.gz
# Test data is not redistributible
# Source1:       http://www.belledonne-communications.com/downloads/bcg729-patterns.zip

# Fix cmake installation dir
Patch0:        bcg729_cmakedir.patch
# Increase minimum cmake version to 3.5
Patch1:        bcg729_cmakever.patch

BuildRequires: cmake
BuildRequires: gcc
BuildRequires: make


%description
bcg729 is an opensource implementation of both encoder and decoder of the
ITU G729 Annex A speech codec.
The library written in C 99 is fully portable and can be executed on many
platforms including both ARM  processor and x86.
bcg729 supports concurrent channels encoding/decoding for multi call
application such conferencing.


%package       devel
Summary:       Development files for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description   devel
Development files for %{name}.


%prep
%autosetup -p1
# unzip -qq -d test %%{SOURCE1}


%build
%cmake -DENABLE_STATIC=OFF
%cmake_build


%install
%cmake_install

%check
# Test data is not redistributible
# make check


%files
%doc AUTHORS.md README.md CHANGELOG.md
%license LICENSE.txt
%{_libdir}/lib%{name}.so.0*


%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc
%{_libdir}/cmake/Bcg729/


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 16 2025 Sandro Mani <manisandro@gmail.com> - 1.1.1-12
- Increase minimum cmake version to 3.5

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 23 2020 Sandro Mani <manisandro@gmail.com> - 1.1.1-1
- Update to 1.1.1

* Fri Nov 20 2020 Sandro Mani <manisandro@gmail.com> - 1.1.0-1
- Update to 1.1.0

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Sandro Mani <manisandro@gmail.com> - 1.0.4-1
- Update to 1.0.4

* Sat Mar 18 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Feb 28 2017 Sandro Mani <manisandro@gmail.com> - 1.0.3-1
- Update to 1.0.3

* Fri Jan 06 2017 Sandro Mani <manisandro@gmail.com> - 1.0.2-1
- Update to 1.0.2

* Thu Jul 28 2016 Sandro Mani <manisandro@gmail.com> - 1.0.1-2
- Remove OpenSSL BRs

* Thu Jul 28 2016 Sandro Mani <manisandro@gmail.com> - 1.0.1-1
- Update to 1.0.1

* Thu Jul 28 2016 Dominik Mierzejewski <rpm@greysector.net> - 1.0.0-3
- add test data, build (but don't install) static library and enable tests

* Wed Jul 20 2016 Sandro Mani <manisandro@gmail.com> - 1.0.0-2
- Move autoreconf to build
- BR: pkgconfig(ortp)
- License is GPLv2+
- Change command to delete *.la files
- Use %%name in %%files
- Don't fix FSF addresses

* Wed Jul 20 2016 Sandro Mani <manisandro@gmail.com> - 1.0.0-1
- Initial package
