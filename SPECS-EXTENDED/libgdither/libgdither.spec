Summary:        Library for applying dithering to PCM audio sources
Name:           libgdither
Version:        0.6
Release:        27%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://plugin.org.uk/libgdither/README
Source0:        https://plugin.org.uk/libgdither/libgdither-%{version}.tar.gz
Patch0:         libgdither-0.6-default.patch
Patch1:         libgdither-0.6-gavl.patch
Patch2:         libgdither-0.6-ldflags.patch
BuildRequires:  fftw-devel >= 3.0.0
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Libgdither is a GPL'd library library for performing audio dithering on
PCM samples. The dithering process should be carried out before reducing
the bit width of PCM audio data (eg. float to 16 bit int conversions) to
preserve audio quality.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch 0 -p1 -b .default
%patch 1 -p1 -b .gavl_fix
%patch 2 -p1 -b .ldflags


%build
export INIT_CFLAGS="%{optflags}"
export LDFLAGS="%{build_ldflags}"
export PREFIX="%{_prefix}"
%make_build


%install
%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir}
find %{buildroot} -type f -name "*.la" -delete -print

sed -i -e 's|%{_prefix}/local|%{_prefix}|g' \
   %{buildroot}%{_libdir}/pkgconfig/libgdither.pc
sed -i -e 's|%{_prefix}/lib|%{_libdir}|' \
  %{buildroot}%{_libdir}/pkgconfig/libgdither.pc

%check
make test CFLAGS="%{optflags} -Werror --std=c99 -I%{_builddir}/%{?buildsubdir}"


%ldconfig_scriptlets


%files
%doc README
%license COPYING
%{_libdir}/*.so.*

%files devel
%{_includedir}/libgdither/
%{_libdir}/*.so
%{_libdir}/pkgconfig/libgdither.pc

%changelog
* Thu Jan 05 2023 Suresh Thelkar <sthelkar@microsoft.com> - 0.6-27
- Initial CBL-Mariner import from Fedora 36 (license: MIT)
- License verified

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun May 26 2019 David King <amigadave@amigadave.com> - 0.6-20
- Pass through PREFIX to build system

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 17 2018 Nicolas Chauvet <kwizart@gmail.com> - 0.6-18
- Refresh spec file

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 10 2018 Rafael Santos <rdossant@redhat.com> - 0.6-16
- Use Fedora standard linker flags (bug #1548657)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 27 2008 kwizart < kwizart at gmail.com > - 0.6-1
- Backport patch from gavl

* Mon Jun 16 2008 kwizart < kwizart at gmail.com > - 0.6-0
- Initial package
