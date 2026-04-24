# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global svn_release 475

Name:           libreplaygain
Version:        0
Release: 1.29.20110810svn%{svn_release}%{?dist}
Summary:        Gain analysis library from Musepack

# Automatically converted from old format: LGPLv2+ - review is highly recommended.
License:        LicenseRef-Callaway-LGPLv2+
URL:            http://www.musepack.net/index.php
Source0:        http://files.musepack.net/source/%{name}_r%{svn_release}.tar.gz

BuildRequires:  cmake gcc

%description
Gain analysis library used by Musepack utilities and libraries


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}_r%{svn_release}

# Correct permissions and end of line
chmod 0644 include/replaygain/*.h src/gain_analysis.c
sed -ibackup 's/\r$//' include/replaygain/*.h src/gain_analysis.c

# Don't let it override the compiler flags
# Don't make the build quiet
sed '5,9d' -ibackup CMakeLists.txt


%build
%cmake .
%cmake_build


%install
%cmake_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
# Remove static lib
rm $RPM_BUILD_ROOT/%{_libdir}/%{name}.a

mkdir -p $RPM_BUILD_ROOT/%{_includedir}/replaygain/
cp -v include/replaygain/*.h $RPM_BUILD_ROOT/%{_includedir}/replaygain/


%files
%{_libdir}/*.so.*

%files devel
%{_includedir}/replaygain
%{_libdir}/*.so


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.29.20110810svn475
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.28.20110810svn475
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 0-0.27.20110810svn475
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.26.20110810svn475
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.25.20110810svn475
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.24.20110810svn475
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.23.20110810svn475
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.22.20110810svn475
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.21.20110810svn475
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.20.20110810svn475
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.19.20110810svn475
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.18.20110810svn475
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 30 2020 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-0.17.20110810svn475
- Fix build using required cmake macros

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.16.20110810svn475
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.15.20110810svn475
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.14.20110810svn475
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.13.20110810svn475
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.12.20110810svn475
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.11.20110810svn475
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Mar 10 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-0.10.20110810svn
- Add gcc to BR

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.9.20110810svn475
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.8.20110810svn475
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.7.20110810svn475
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.6.20110810svn475
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.5.20110810svn475
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.4.20110810svn475
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.3.20110810svn475
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.2.20110810svn475
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Oct 19 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-0.1.20110810svn475
- Update as per review: #1018541
- Update version
- Remove unrequired portions
- File inclusions
- Initial rpmbuild

