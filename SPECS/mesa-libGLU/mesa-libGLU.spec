Summary:        Mesa libGLU library
Name:           mesa-libGLU
Version:        9.0.1
Release:        4%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://mesa3d.org/
Source0:        https://mesa.freedesktop.org/archive/glu/glu-%{version}.tar.xz
Source1:        LICENSE.PTR
Source2:        make-git-snapshot.sh
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  mesa-libGL-devel
Provides:       libGLU = %{version}-%{release}

%description
Mesa implementation of the standard GLU OpenGL utility API.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       libGLU-devel = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n glu-%{version}
cp %{SOURCE1} .

%build
autoreconf -v -i -f
%configure --disable-static
%make_build
make %{?_smp_mflags}

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print
rm -rf %{buildroot}%{_mandir}/man3/gl[A-Z]*

%ldconfig_scriptlets

%files
%license LICENSE.PTR
%{_libdir}/libGLU.so.1
%{_libdir}/libGLU.so.1.3.*

%files devel
%{_includedir}/GL/glu*.h
%{_libdir}/libGLU.so
%{_libdir}/pkgconfig/glu.pc

%changelog
* Wed Jul 21 2021 Vinicius Jarina <vinja@microsoft.com> - 9.0.1-4
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- Added a "LICENSE.PTR" source clarifying the project's license.
- License verified.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Peter Robinson <pbrobinson@fedoraproject.org> 9.0.1-1
- libGLU 9.0.1

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Adam Jackson <ajax@redhat.com> - 9.0.0-15
- Use ldconfig scriptlet macros

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 9.0.0-8
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Adam Jackson <ajax@redhat.com> 9.0.0-5
- Always autoreconf to pick up patch changes (#1070602)

* Mon Dec 09 2013 Adam Jackson <ajax@redhat.com> 9.0.0-4
- Sync with git (#1011823)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 18 2012 Adam Jackson <ajax@redhat.com> 9.0.0-1
- libGLU 9.0

* Mon Sep 10 2012 Dave Airlie <airlied@redhat.com> 9.0-0.2
- add back libGLU provides for now

* Tue Sep 04 2012 Adam Jackson <ajax@redhat.com> 9.0-0.1
- Initial packaging for split libGLU
