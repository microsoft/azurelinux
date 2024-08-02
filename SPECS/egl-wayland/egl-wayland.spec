Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           egl-wayland
Version:        1.1.6
Release:        3%{?dist}
Summary:        Wayland EGL External Platform library

License:        MIT
URL:            https://github.com/NVIDIA/%{name}
Source0:        %url/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        10_nvidia_wayland.json

BuildRequires:  meson
BuildRequires:  libtool
BuildRequires:  eglexternalplatform-devel

BuildRequires:  libglvnd-devel



BuildRequires:  wayland-devel

# Required for directory ownership
Requires:       libglvnd-egl%{?_isa}

%description
Wayland EGL External Platform library

%package devel
Summary:        Wayland EGL External Platform library development package
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Wayland EGL External Platform library development package

%prep
%autosetup -p1
%if 0%{?rhel}
sed -i -e 's@>= 0.50@>= 0.47@g'  meson.build
%endif

%build
%meson
%meson_build


%install
%meson_install
install -m 0755 -d %{buildroot}%{_datadir}/egl/egl_external_platform.d/
install -pm 0644 %{SOURCE1} %{buildroot}%{_datadir}/egl/egl_external_platform.d/
find %{buildroot} -name '*.la' -exec rm -f {} ';'


%ldconfig_scriptlets


%files
%doc README.md
%license COPYING
%{_libdir}/*.so.*
%{_datadir}/egl/egl_external_platform.d/10_nvidia_wayland.json

%files devel
%{_libdir}/libnvidia-egl-wayland.so
%{_libdir}/pkgconfig/wayland-eglstream.pc
%{_datadir}/pkgconfig/wayland-eglstream-protocols.pc
%{_datadir}/wayland-eglstream/

%changelog
* Wed Jul 10 2024 Hideyuki Nagase <hideyukn@microsoft.com> - 1.1.6-3
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.6-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Thu Jan  7 2021 Leigh Scott <leigh123linux@gmail.com> - 1.1.6-1
- Update to 1.1.6

* Fri Aug 14 2020 Leigh Scott <leigh123linux@gmail.com> - 1.1.5-3
- Add upstream patch to address rhbz#1842473

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 01 2020 Leigh Scott <leigh123linux@gmail.com> - 1.1.5-1
- Update to 1.1.5

* Mon Mar 30 2020 leigh123linux <leigh123linux@googlemail.com> - 1.1.4-4
- Use upstream commit to address missing mesa includes

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 16 2019 Leigh Scott <leigh123linux@gmail.com> - 1.1.4-2
- Add patch to add missing mesa includes

* Sun Sep 15 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.1.4-1
- Update to 1.1.4

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.1.3-1
- Update to 1.1.3

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 1.1.2-3
- Rebuild with Meson fix for #1699099

* Sat Mar 30 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.1.2-2
- Switch to upstream fix

* Fri Feb 01 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.1.2-1
- Update to 1.1.2

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec 06 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.1-3
- Fix the same crappy warning f28 generates

* Thu Dec 06 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.1-2
- Fix the crappy warning epel7 generates

* Thu Dec 06 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.1-1
- Update to 1.1.1

* Mon Nov 26 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.0-0.2.20181015git0eb29d4
- Update to latest git snapshot (rhbz#1653118)

* Mon Aug 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.0-0.1.20180916git1676d1d
- Update to 1.1.0 snapshot

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-0.2.20180626git395ce9f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.0.5-0.1.20180626git395ce9f
- Update to 1.0.5 snapshot

* Sat Jun 16 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.0.4-0.1.20180602git4ab0873
- Update to 1.0.4 snapshot

* Tue Feb 06 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.0.3-2.20180201git6f5f7d0
- Update to latest git snapshot
- Switch to meson
- Install .so file to -devel as it's listed in wayland-eglstream.pc
- Fix directory ownership

* Wed Jan 31 2018 Jonas Ådahl <jadahl@redhat.com> - 1.0.3-1.20180111gitb283689
- Update to 1.0.3
- Add -devel package

* Thu Aug 03 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.2-0.4.20170802git1f4b1fd
- Update to latest git snapshot

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-0.3.20170628git818b613
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-0.2.20170628git818b613
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 28 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.2-0.1.20170628git818b613
- Update to 1.0.2 git

* Wed Mar 08 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.1-0.1.20170308git582fbf3
- Update to 1.0.1 git

* Tue Feb 07 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.0-0.7.20170207git05eb000
- Add license file

* Thu Feb 02 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.0-0.6.20170120git743d702
- Add requires libglvnd-egl
- Make review changes

* Wed Feb 01 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.0-0.5.20170120git743d702
- Drop devel sub-package

* Wed Feb 01 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.0-0.4.20170120git743d702
- Add 10_nvidia_wayland.json to libs sub-package

* Wed Feb 01 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.0-0.3.20170120git743d702
- Add loader directory to common sub-package
- Move libs to sub-package

* Fri Jan 20 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.0-0.2.20170120git743d702
- Add date to release

* Fri Jan 20 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.0-0.1.git743d702
- First build

