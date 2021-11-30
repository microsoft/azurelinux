Summary:        Virgl Rendering library.
Name:           virglrenderer
Version:        0.9.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://gitlab.freedesktop.org/virgl/virglrenderer
Source0:        %{url}/-/archive/%{name}-%{version}/%{name}-%{name}-%{version}.tar.gz

BuildRequires:  libdrm-devel
BuildRequires:  libepoxy-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  meson
BuildRequires:  python3
BuildRequires:  xorg-x11-util-macros

%description
The virgil3d rendering library is a library used by
qemu to implement 3D GPU support for the virtio GPU.

%package devel
Summary:        Virgil3D renderer development files
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Virgil3D renderer development files, used by
qemu to build against.

%package test-server
Summary:        Virgil3D renderer testing server
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description test-server
Virgil3D renderer testing server is a server
that can be used along with the mesa virgl
driver to test virgl rendering without GL.

%prep
%autosetup -n %{name}-%{name}-%{version}

%build
%meson
%meson_build

%install
%meson_install

%ldconfig_scriptlets

%files
%license COPYING
%{_libdir}/lib*.so.1
%{_libdir}/lib*.so.1.*

%files devel
%dir %{_includedir}/virgl/
%{_includedir}/virgl/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

%files test-server
%{_bindir}/virgl_test_server

%changelog
* Tue Nov 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9.1-1
- Updating to version 0.9.1.
- License verified.
- Updated "Source0" URL, using official release sources.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.8.2-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Feb 12 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.8.2-1.20200212git7d204f39
- Upstream release 0.8.2

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-2.20191220git66c57963
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 20 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.8.1-1.20191220git66c57963
- Upstream release 0.8.1

* Thu Oct 03 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.8.0-1.20191002git4ac3a04c
- Latest upstream git snapshot

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-4.20190424gitd1758cc09
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 24 2019 Dave Airlie <airlied@redhat.com> - 0.7.0-3.20190424gitd1758cc09
- Latest upstream git snapshot

* Wed Apr 10 2019 Dave Airlie <airlied@redhat.com> - 0.7.0-3.20180919git402c22886
- build debug package properly, fix make commands

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-2.20180919git402c22886
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 19 2018 Dave Airlie <airlied@redhat.com> - 0.7.0-1.20180919git402c22886
- upstream 0.7.0 release

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-6.20170210git76b3da97b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Mar 18 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.6.0-5.20170210git76b3da97b
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-4.20170210git76b3da97b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3.20170210git76b3da97b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2.20170210git76b3da97b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Dave Airlie <airlied@redhat.com> - 0.6.0-1.git
- upstream 0.6.0 release

* Mon Apr 11 2016 Dave Airlie <airlied@redhat.com> 0.5.0-1.git
- upstream 0.5.0 release

* Thu Feb 18 2016 Dave Airlie <airlied@redhat.com> 0.4.1-1.git
- fix regression in last build

* Wed Feb 17 2016 Dave Airlie <airlied@redhat.com> 0.4.0-1.git
- latest git snapshot with new API

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-3.20151215gite9d3c0c27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 15 2015 Dave Airlie <airlied@redhat.com> 0.3.0-2.gite9d3c0c27
- latest upstream to fix gnome-shell rendering bugs

* Fri Oct 23 2015 Dave Airlie <airlied@redhat.com> 0.3.0-1.20151023git9ce005e5a
- update to latest upstream to fix shader issue

* Fri Oct 23 2015 Dave Airlie <airlied@redhat.com> 0.2.0-1.20151023git5bfba5190
- update to latest upstream

* Thu Jul 09 2015 Dave Airlie <airlied@redhat.com> 0.0.1-0.20150420gitc4fb40201.2
- fix FTBFS (#1240041)

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-0.20150420gitc4fb40201.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 01 2015 Dave Airlie <airlied@redhat.com> 0.0.1-0.20150401gita9ba2c442
- initial virglrenderer spec
