# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#global candidate rc0
%global with_python 1

Name:          libgpiod
Version:       2.2.3
Release: 2%{?candidate:.%{candidate}}%{?dist}
Summary:       C library and tools for interacting with linux GPIO char device

License:       LGPL-2.1-or-later
URL:           https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/
Source0:       https://mirrors.edge.kernel.org/pub/software/libs/%{name}/%{name}-%{version}%{?candidate:-%{candidate}}.tar.xz
Source1:       gpiod-sysusers.conf

BuildRequires: doxygen
BuildRequires: gcc gcc-c++
BuildRequires: gi-docgen
BuildRequires: glib2-devel
BuildRequires: gobject-introspection-devel
BuildRequires: help2man
BuildRequires: kernel-headers
BuildRequires: kmod-devel
BuildRequires: libgudev-devel
BuildRequires: libstdc++-devel
BuildRequires: make
BuildRequires: pkgconf
%if 0%{?with_python}
BuildRequires: python3-devel
BuildRequires: python3-packaging
BuildRequires: python3-pip
BuildRequires: python3-setuptools
BuildRequires: (python3-wheel if python3-setuptools < 71)
%endif
BuildRequires: systemd

%description
libgpiod is a C library and tools for interacting with the linux GPIO character 
device (gpiod stands for GPIO device) The new character device interface 
guarantees all allocated resources are freed after closing the device file 
descriptor and adds several new features that are not present in the obsolete 
sysfs interface (like event polling, setting/reading multiple values at once or 
open-source and open-drain GPIOs).

%package manager
Summary: DBus manager for GPIO
License: GPL-2.0-or-later
Requires: %{name}%{?_isa} = %{version}-%{release}

%description manager
DBus manager for interacting with GPIO character devices.

%package utils
Summary: Utilities for GPIO
License: GPL-2.0-or-later
Requires: %{name}%{?_isa} = %{version}-%{release}

%description utils
Utilities for interacting with GPIO character devices.

%package c++
Summary: C++ bindings for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description c++
C++ bindings for use with %{name}.

%package glib
Summary: GLib2 bindings for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description glib
GLib2 bindings for use with %{name}.

%if 0%{?with_python}
%package -n python3-%{name}
Summary: Python 3 bindings for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}
Python 3 bindings for development with %{name}.
%endif

%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-c++ = %{version}-%{release}
%if 0%{?with_python}
Requires: python3-%{name} = %{version}-%{release}
%endif

%description devel
Files for development with %{name}.

%prep
%autosetup -p1
%if 0%{?with_python}
# python bindings build is set to use isolation. Remove this for distro build so it uses the
# system installed dependencies instead of trying to use pip to install from the network
sed -i 's/-m build/-m pip wheel --wheel-dir dist --no-build-isolation ./' bindings/python/Makefile*
# Once the following commit is merged, replace the above line with the command below:
# https://lore.kernel.org/linux-gpio/20250407181116.1070816-1-yselkowi@redhat.com/T/#u
#sed -i 's/-m pip wheel/& --no-build-isolation/' bindings/python/Makefile*
%endif

%build
%configure \
	--enable-tools \
	--enable-dbus \
	--enable-systemd \
	--disable-static \
	--enable-bindings-cxx \
	--enable-bindings-glib \
%if 0%{?with_python}
	--enable-bindings-python \
%endif
	%{nil}

%make_build

%install
%make_install

# Install sysusers file
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/gpiod.conf
# Fix udev rule location
%ifnarch %{ix86}
mkdir -p %{buildroot}/%{_udevrulesdir}/
mv -f %{buildroot}/%{_libdir}/udev/rules.d/90-gpio.rules %{buildroot}/%{_udevrulesdir}/90-gpio.rules
%endif
# Remove libtool archives.
find %{buildroot} -name '*.la' -delete

%ldconfig_scriptlets


%post manager
%systemd_post gpio-manager.service

%preun manager
%systemd_preun gpio-manager.service

%postun manager
%systemd_postun_with_restart gpio-manager.service

%files
%license COPYING
%doc README.md
%{_libdir}/libgpiod.so.3*
%{_libdir}/libgpiodbus.so.1*
%{_sysusersdir}/gpiod.conf
%{_udevrulesdir}/90-gpio.rules

%files manager
%{_bindir}/gpio-manager
%{_bindir}/gpiocli
%{_sysconfdir}/dbus-1/system.d/io.gpiod1.conf
%{_datadir}/dbus-1/interfaces/io.gpiod1.xml
%{_unitdir}/gpio-manager.service

%files utils
%{_bindir}/gpiodetect
%{_bindir}/gpioget
%{_bindir}/gpioinfo
%{_bindir}/gpiomon
%{_bindir}/gpionotify
%{_bindir}/gpioset
%{_mandir}/man*/gpio*

%files c++
%{_libdir}/libgpiodcxx.so.2*

%files glib
%{_libdir}/libgpiod-glib.so.1*
%{_libdir}/girepository-1.0/Gpiodglib-1.0.typelib

%if 0%{?with_python}
%files -n python3-%{name}
%{python3_sitearch}/gpiod/
%{python3_sitearch}/gpiod-2.2.0.dist-info
%endif

%files devel
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/libgpiod*.pc
%{_libdir}/pkgconfig/gpiod-glib.pc
%{_includedir}/gpiod.*
%{_includedir}/gpiodcxx/
%{_includedir}/gpiod-glib.h
%{_includedir}/gpiod-glib/
%{_datadir}/gir-1.0/Gpiodglib-1.0.gir


%changelog
* Mon Feb 23 2026 Peter Robinson <pbrobinson@fedoraproject.org> - 2.2.3-1
- Update to 2.2.3

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.2.2-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Wed Aug 27 2025 Miro Hrončok <mhroncok@redhat.com> - 2.2.2-4
- Drop unused BuildRequires on python3-wheel

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.2.2-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 25 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 2.2.2-1
- Update to 2.2.2

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.2.1-4
- Rebuilt for Python 3.14

* Thu Apr 24 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 2.2.1-3
- Build with pip, avoid python-build dependency

* Wed Apr 09 2025 Zbigniew Jędrzejewski-Szmek  <zbyszek@in.waw.pl> - 2.2.1-2
- Fix scriptlets for service enablement

* Wed Feb 19 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.2-2
- Drop call to %sysusers_create_compat

* Wed Jan 29 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 2.2-1
- Update to 2.2
- Disable python bindings (temporary)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-0.2.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Oct 17 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 2.2.0-0.1.rc3
- Upgrade to 2.2 RC3
- Enable new gpio-manager dbus service
- Add sysusers for gpio group

* Thu Aug 01 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 2.1.3-1
- Update to 2.1.3

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.1.2-2
- Rebuilt for Python 3.13

* Mon May 13 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 2.1.2-1
- Update to 2.1.2

* Sun Mar 10 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 2.1.1-1
- Update to 2.1.1

* Mon Jan 29 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Nov 03 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 2.1-1
- Update to 2.1

* Fri Aug 25 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 2.0.2-1
- Update to 2.02

* Thu Jul 27 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 2.0.1-5
- migrated to SPDX license

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.0.1-3
- Rebuilt for Python 3.12

* Tue Apr 25 2023 Miro Hrončok <mhroncok@redhat.com> - 2.0.1-2
- Don't install a Python .egg

* Tue Apr 11 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1

* Thu Mar 02 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 2.0-1
- Update to 2.0

* Mon Feb 27 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 2.0-0.4.rc3
- libgpiod 2.0 RC3

* Thu Feb 16 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 2.0-0.3.rc2
- libgpiod 2.0 RC2

* Mon Feb 13 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 2.0-0.2.rc1
- Add deps for man pages build

* Mon Feb 13 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 2.0-0.1.rc1
- Update to libgpiod 2.0 RC1

* Wed Feb 08 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 1.6.4-1
- Update to 1.6.4

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Aug 23 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 1.6.3-7
- Update devel dependencies

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.6.3-5
- Rebuilt for Python 3.11

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.6.3-2
- Rebuilt for Python 3.10

* Mon Mar 22 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 1.6.3-1
- Update to 1.6.3

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec  1 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.6.2-1
- Update to 1.6.2

* Mon Nov  2 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.6.1-1
- Update to 1.6.1

* Thu Oct 01 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.6-1
- Update to 1.6

* Sat Sep 26 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.5.3-1
- Update to 1.5.3

* Wed Aug 26 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.5.2-1
- Update to 1.5.2

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.5.1-2
- Rebuilt for Python 3.9

* Wed Apr 01 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.5.1-1
- Update to 1.5.1

* Tue Jan 28 2020 Peter Robinson <pbrobinson@fedoraproject.org> 1.5-1
- Update to 1.5

* Wed Jan 15 2020 Peter Robinson <pbrobinson@fedoraproject.org> 1.5-0.2-RC2
- Update to 1.5 RC2

* Tue Jan  7 2020 Peter Robinson <pbrobinson@fedoraproject.org> 1.5-0.1-RC1
- Update to 1.5 RC1

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.4.1-2
- Rebuilt for Python 3.8

* Fri Aug  9 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.1-1
- Update to 1.4.1 release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun  9 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.4-1
- Update to 1.4 release

* Tue Mar 26 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.3-1
- Update to 1.3 release

* Sat Feb 16 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.1-1
- Update to 1.2.1 release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Nov 10 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.2-1
- Update to 1.2 release

* Thu Jul 26 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.1-1
- Update to 1.1.1 release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1-2
- Rebuilt for Python 3.7

* Thu May 17 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.1-1
- Update to 1.1 release
- New C++ and Python 3 bindings

* Sun Apr 15 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.1-1
- Update to 1.0.1

* Thu Feb  8 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.0-1
- Update to 1.0.0 with stable API

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov  9 2017 Peter Robinson <pbrobinson@fedoraproject.org> 0.3.2-1
- Update to 0.3.2

* Tue Aug 22 2017 Peter Robinson <pbrobinson@fedoraproject.org> 0.3-2
- Minor review updates

* Sat Jul  1 2017 Peter Robinson <pbrobinson@fedoraproject.org> 0.3-1
- Initial package
