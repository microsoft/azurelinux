# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%undefine __cmake_in_source_build
%{?rhel: %global cmake %cmake3}

# Bootstrap may be needed to break circular dependencies between
# codec2 and lpcnetfreedv
%bcond_with     bootstrap

Name:           codec2
Version:        1.2.0
Release:        7%{?dist}
Summary:        Next-Generation Digital Voice for Two-Way Radio
License:        LGPL-2.1-only

URL:            http://rowetel.com/codec2.html
Source0:        https://github.com/drowe67/codec2/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake%{?rhel:3}
BuildRequires:  gcc gcc-c++
BuildRequires:  libsamplerate-devel
%if %{without bootstrap}
BuildRequires:  lpcnetfreedv-devel
%endif
BuildRequires:  speex-devel
%if ! 0%{?rhel} < 8
BuildRequires:  speexdsp-devel
%endif


%description
Codec 2 is an open source (LGPL licensed) speech codec for 2400 bit/s
and below. This is the runtime library package.


%package devel
Summary:        Development files for Codec 2 
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Codec 2 is an open source (LGPL licensed) speech codec for 2400 bit/s
and below. This package contains the development files required to 
compile programs that use codec2.


%package devel-examples
Summary:        Example code for Codec 2
Requires:       %{name}-devel = %{version}-%{release}
BuildArch:      noarch

%description devel-examples
Example code for Codec 2


%prep
%autosetup -p1


%build
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo \
%if %{without bootstrap}
       -DLPCNET=ON
%endif

%cmake_build


%install
%cmake_install

# Create and install pkgconfig file
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cat > %{buildroot}%{_libdir}/pkgconfig/codec2.pc << EOF
prefix=%{_prefix}
exec_prefix=\${prefix}
includedir=\${prefix}/include/%{name}
libdir=\${exec_prefix}/%{_lib}

Name: codec2
Description: Next-Generation Digital Voice for Two-Way Radio
Version: 1.2.0
Cflags: -I\${includedir}
Libs: -L\${libdir} -l%{name}
EOF


%ldconfig_scriptlets


%files
%license COPYING
%doc README.md
%{_libdir}/*.so.*

%files devel
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}/


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Aug 05 2023 Richard Shaw <hobbes1069@gmail.com> - 1.2.0-2
- Rebuild after bootstrap for lpcnetfreedv.

* Sat Aug 05 2023 Richard Shaw <hobbes1069@gmail.com> - 1.2.0-1
- Update to 1.2.0

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 07 2022 Richard Shaw <hobbes1069@gmail.com> - 1.0.5-1
- Update to 1.0.5.

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jul 16 2022 Richard Shaw <hobbes1069@gmail.com> - 1.0.4-1.1
- Add patch to deal with unintentional API change.

* Sat Jul 09 2022 Richard Shaw <hobbes1069@gmail.com> - 1.0.4-1
- Update to 1.0.4.

* Thu Mar 03 2022 Richard Shaw <hobbes1069@gmail.com> - 1.0.3-1
- Update to 1.0.3.

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Dec 05 2021 Richard Shaw <hobbes1069@gmail.com> - 1.0.1-1
- Update to 1.0.1.

* Mon Aug 09 2021 Richard Shaw <hobbes1069@gmail.com> - 1.0.0-1.2
- Rebuild codec2 with lpcnetfreedv post bootstrap.

* Mon Aug 09 2021 Richard Shaw <hobbes1069@gmail.com> - 1.0.0-1.1
- Rebuild codec2 without lpcnetfreedv to break circular depdendency.

* Sun Aug 08 2021 Richard Shaw <hobbes1069@gmail.com> - 1.0.0-1
- Update to 1.0.0.

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Dec 20 2020 Richard Shaw <hobbes1069@gmail.com> - 0.9.2-6
- Re-enable normal build after bootstrapping lpcnetfreedv.

* Sun Dec 20 2020 Richard Shaw <hobbes1069@gmail.com> - 0.9.2-5
- Rebuild for updated lpcnetfreedv.

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Richard Shaw <hobbes1069@gmail.com> - 0.9.2-2
- Rebuild with lpcnetfreedv.

* Thu Apr 16 2020 Richard Shaw <hobbes1069@gmail.com> - 0.9.2-1
- Update to 0.9.2.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 03 2018 Richard Shaw <hobbes1069@gmail.com> - 0.8.1-1
- Update to 0.8.1

* Tue May 29 2018 Richard Shaw <hobbes1069@gmail.com> - 0.8-1
- Update to 0.8.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Richard Shaw <hobbes1069@gmail.com> - 0.7-1
- Update to latest upstream release.

* Sun Feb 19 2017 Richard Shaw <hobbes1069@gmail.com> - 0.6-1
- Update to latest upstream release.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Apr 25 2016 Richard Shaw <hobbes1069@gmail.com> - 0.5.1-1
- Update to latest upstream release.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct 29 2015 Richard Shaw <hobbes1069@gmail.com> - 0.5-1
- Update to latest upstream release.

* Sat Aug  8 2015 Richard Shaw <hobbes1069@gmail.com> - 0.4-2
- Update to latest bugfix release.

* Thu Jul  2 2015 Richard Shaw <hobbes1069@gmail.com> - 0.4-1
- Update to latest upstream release.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-6.20150317svn2080
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 17 2015 Richard Shaw <hobbes1069@gmail.com> - 0.3-5.svn2080
- Update to later checkout.

* Mon Mar 16 2015 Richard Shaw <hobbes1069@gmail.com> - 0.3-4.svn1914
- Fixup spec file per review request comments.

* Sun Jul 27 2014 Richard Shaw <hobbes1069@gmail.com> - 0.3-2.svn1771
- Fix executable permissions on scripts.
- Move example package to devel-examples.
- Move binaries to devel package as they are not useful elsewere.
- Fix package name to include svn checkout date.

* Mon Jun 16 2014 Richard Shaw <hobbes1069@gmail.com> - 0.3-1.svn1657
- Updated for ABI incompatible change in freedv.

* Mon Jun 16 2014 Richard Shaw <hobbes1069@gmail.com> - 0.2-9
- Update to newer svn checkout.

* Mon May  5 2014 Richard Shaw <hobbes1069@gmail.com> - 0.2-8
- Update to newer checkout.

* Fri Mar 28 2014 Richard Shaw <hobbes1069@gmail.com> - 0.2-6
- Update to newer checkout.

* Wed Mar 27 2013 Richard Shaw <hobbes1069@gmail.com> - 0.2.0-5
- Make the package more Fedora compliant.
- Add patch to make sure fdmdv.h is installed.
- Strip rpath from binaries.
- Create pkgconfig file to deal with non-standard header location.
- Move examples to a separate sub-package.

* Sun Dec 30 2012 Mike Heitmann <mheitmann@n0so.net> 0.2.0-2
- Fixed ldconfig path error

* Sun Dec 30 2012 Mike Heitmann <mheitmann@n0so.net> 0.2.0-1
- Fixed ldconfig errors, corrected version number

* Sun Dec 23 2012 Mike Heitmann <mheitmann@n0so.net> 0.0.1-1
- Initial SPEC
- Split out from FreeDV to compile separately
