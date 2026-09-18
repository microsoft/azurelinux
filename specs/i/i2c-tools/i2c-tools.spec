# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Copyright (c) 2007 SUSE LINUX Products GmbH, Nuernberg, Germany.
# Copyright (c) 2007 Hans de Goede <j.w.r.degoede@hhs>, the Fedora project.
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

Name:           i2c-tools
Version:        4.4
Release:        3%{?dist}
Summary:        A heterogeneous set of I2C tools for Linux
# Note: py-symbus/ is GPL-2.0-only, lib/ is LGPL-2.1-or-later
# and the rest is GPL-2.0-or-later
License:        GPL-2.0-or-later
URL:            https://i2c.wiki.kernel.org/index.php/I2C_Tools

Source0:        https://www.kernel.org/pub/software/utils/i2c-tools/%{name}-%{version}.tar.xz

# for /etc/udev/makedev.d resp /usr/lib/modprobe.d ownership
Requires:       systemd-udev kmod
Requires:       libi2c%{?_isa} = %{version}-%{release}
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
ExcludeArch:    s390 s390x
Obsoletes:      i2c-tools-eepromer < 4.2-2

%description
This package contains a heterogeneous set of I2C tools for Linux: a bus
probing tool, a chip dumper, register-level access helpers, EEPROM
decoding scripts, and more.


%package -n python3-i2c-tools
Summary:        Python 3 bindings for Linux SMBus access through i2c-dev
License:        GPL-2.0-only
%{?python_provide:%python_provide python3-i2c-tools}
Requires:       libi2c%{?_isa} = %{version}-%{release}
%if %{without python2}
# Remove before F30
Obsoletes: %{name}-python < 4.0-4
# Remove before F31
Obsoletes: python2-i2c-tools < 4.0-5
%endif

%description -n python3-i2c-tools
Python 3 bindings for Linux SMBus access through i2c-dev

%package perl
Summary:        i2c tools written in Perl
License:        GPL-2.0-or-later
Requires:       libi2c%{?_isa} = %{version}-%{release}

%description perl
A collection of tools written in perl for use with i2c devices.

%package -n libi2c
Summary:        I2C/SMBus bus access library
License:        LGPL-2.1-or-later

%description -n libi2c
libi2c offers a way for applications to interact with the devices
connected to the I2C or SMBus buses of the system.

%package -n libi2c-devel
Summary:        Development files for the I2C library
License:        LGPL-2.1-or-later
Requires:       libi2c%{?_isa} = %{version}-%{release}
# Remove in F30
Obsoletes:      i2c-tools-devel < 4.0-1

%description -n libi2c-devel
%{summary}.

%prep
%autosetup -p1

%build
make CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS" BUILD_STATIC_LIB=0 EXTRA=eeprog
pushd py-smbus
CFLAGS="$RPM_OPT_FLAGS -I../include" LDFLAGS="$RPM_LD_FLAGS" \
  %{__python3} setup.py build -b build-py3
popd


%install
make install DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix} BUILD_STATIC_LIB=0 \
  EXTRA=eeprog libdir=%{_libdir} bindir=%{_bindir} sbindir=%{_sbindir}
pushd py-smbus
%{__python3} setup.py build -b build-py3 install --skip-build --root=$RPM_BUILD_ROOT
popd

# cleanup
rm -f $RPM_BUILD_ROOT%{_bindir}/decode-edid.pl
# Remove unpleasant DDC tools.  KMS already exposes the EDID block in sysfs,
# and edid-decode is a more complete tool than decode-edid.
rm -f $RPM_BUILD_ROOT%{_bindir}/{ddcmon,decode-edid}

# for i2c-dev ondemand loading through kmod
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/modprobe.d 
echo "alias char-major-89-* i2c-dev" > \
  $RPM_BUILD_ROOT%{_prefix}/lib/modprobe.d/i2c-dev.conf
# for /dev/i2c-# creation (which are needed for kmod i2c-dev autoloading)
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/makedev.d
for (( i = 0 ; i < 8 ; i++ )) do
  echo "i2c-$i" >> $RPM_BUILD_ROOT%{_sysconfdir}/udev/makedev.d/99-i2c-dev.nodes
done

# auto-load i2c-dev after reboot
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/modules-load.d
echo 'i2c-dev' > $RPM_BUILD_ROOT%{_prefix}/lib/modules-load.d/%{name}.conf


%post
# load i2c-dev after the first install
if [ "$1" = 1 ] ; then
  /usr/sbin/modprobe i2c-dev
fi
exit 0

%ldconfig_post -n libi2c
%ldconfig_postun -n libi2c


%files
%license COPYING
%doc CHANGES README
%config(noreplace) %{_prefix}/lib/modprobe.d/i2c-dev.conf
%config(noreplace) %{_sysconfdir}/udev/makedev.d/99-i2c-dev.nodes
%{_sbindir}/i2c*
%{_sbindir}/eeprog
%exclude %{_sbindir}/i2c-stub*
%{_mandir}/man8/i2c*.8.*
%{_mandir}/man8/eeprog.8.*
%exclude %{_mandir}/man8/i2c-stub-from-dump.8.*
%{_prefix}/lib/modules-load.d/%{name}.conf

%files -n python3-i2c-tools
%doc py-smbus/README
%{python3_sitearch}/*

%files perl
%doc eeprom/README
%{_bindir}/decode-*
%{_sbindir}/i2c-stub*
%{_mandir}/man1/decode-*.1.*
%{_mandir}/man8/i2c-stub-from-dump.8.*

%files -n libi2c
%license COPYING.LGPL
%{_libdir}/libi2c.so.0*

%files -n libi2c-devel
%dir %{_includedir}/i2c
%{_includedir}/i2c/smbus.h
%{_libdir}/libi2c.so
%{_mandir}/man3/libi2c.3.*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 4.4-2
- Rebuilt for Python 3.14

* Thu Jan 23 2025 Pavol Žáčik <pzacik@redhat.com> - 4.4-1
- Updated to 4.4

* Thu Jan 23 2025 Pavol Žáčik <pzacik@redhat.com> - 4.3-15
- Rebuilt to comply with the bin/sbin merge
- Resolves: rhbz#2340627

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 4.3-12
- Rebuilt for Python 3.13

* Thu May 09 2024 Pavol Žáčik <pzacik@redhat.com> - 4.3-11
- Fix SPDX license identifiers

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 29 2023 Joe Orton <jorton@redhat.com> - 4.3-8
- migrated to SPDX license

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 4.3-6
- Rebuilt for Python 3.12

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.3-3
- Rebuilt for Python 3.11

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jul 24 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 4.3-1
- Update to 4.3

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.2-4
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 16 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 4.2-2
- Move eeprog to i2c-tools (shouldn't have been in eepromer sub package)
- Drop/obsolete eepromer subpackage, deprecated for 6 years
- Drop python2 conditionals
- Minor cleanups

* Thu Jan 07 2021 Artem Egorenkov <aegorenk@redhat.com> - 4.2-1
- Version 4.2

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.1-5
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 4.1-3
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb  4 2019 Peter Robinson <pbrobinson@fedoraproject.org> 4.1-1
- Version 4.1

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 15 2018 Ondřej Lysoněk <olysonek@redhat.com> - 4.0-12
- Ship modprobe.d files in /usr/lib/modprobe.d (rhbz#1195285)

* Mon Aug 13 2018 Peter Robinson <pbrobinson@fedoraproject.org> 4.0-11
- Add requires on libi2c NVR
- Minor spec cleanups, use %%license

* Fri Aug 03 2018 Ondřej Lysoněk <olysonek@redhat.com> - 4.0-10
- Add upstream patch fixing libi2c license headers

* Tue Jul 31 2018 Ondřej Lysoněk <olysonek@redhat.com> - 4.0-9
- Corrected the License tags

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Adam Jackson <ajax@redhat.com> - 4.0-7
- Use ldconfig scriptlets

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 4.0-6
- Rebuilt for Python 3.7

* Thu Mar 22 2018 Ondřej Lysoněk <olysonek@redhat.com> - 4.0-5
- Don't build Python 2 subpackage on EL > 7 and Fedora > 28

* Mon Feb 19 2018 Ondřej Lysoněk <olysonek@redhat.com> - 4.0-4
- Add gcc to BuildRequires

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb  1 2018 Florian Weimer <fweimer@redhat.com> - 4.0-2
- Build with linker flags from redhat-rpm-config

* Tue Nov 21 2017 Ondřej Lysoněk <olysonek@redhat.com> - 4.0-1
- New version
- Dropped i2c-tools-devel, introduced libi2c, libi2c-devel

* Sat Oct 7 2017 Troy Curtis, Jr <troycurtisjr@gmail.com> - 3.1.2-7
- Add Python3 subpackage.

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.1.2-6
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.1.2-5
- Python 2 binary package renamed to python2-i2c-tools
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Ondřej Lysoněk <olysonek@redhat.com> - 3.1.2-2
- Provide i2c-dev.h in /usr/include/i2c-tools/
- Resolves: rhbz#1288823
- Dropped Group: tags as per https://fedoraproject.org/wiki/Packaging:Guidelines#Tags_and_Sections

* Wed Jul 19 2017 Ondřej Lysoněk <olysonek@redhat.com> - 3.1.2-1
- New version
- Updated upstream and source code URL
- Dropped patches accepted by upstream

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-17
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct 08 2015 Jaromir Capik <jcapik@redhat.com> - 3.1.0-15
- Adding i2c-dev auto-load in th %%post and modules-load.d (#913203)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Oct 9  2013 Peter Robinson <pbrobinson@fedoraproject.org> 3.1.0-11
- Split out perl tools to a separate subpackage

* Fri Oct 04 2013 Jaromir Capik <jcapik@redhat.com> - 3.1.0-10
- Making the decode-* man pages installable with Makefile

* Thu Oct 03 2013 Jaromir Capik <jcapik@redhat.com> - 3.1.0-9
- Introducing man pages for decode-* binaries
- Cleaning the spec

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 3.1.0-7
- Perl 5.18 rebuild

* Wed Jul 03 2013 Jaromir Capik <jcapik@redhat.com> - 3.1.0-6
- Installing the man pages and putting them in the files section

* Wed Jul 03 2013 Jaromir Capik <jcapik@redhat.com> - 3.1.0-5
- Introducing man pages for binaries in the eepromer subpackage
- Introducing -r switch in the i2cset help

* Sat Jun  1 2013 Henrik Nordstrom <henrik@henriknordstrom.net> - 3.1.0-4
- Package python interface

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 20 2012 Adam Jackson <ajax@redhat.com> 3.1.0-1
- i2c-tools 3.1.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 05 2011 Adam Jackson <ajax@redhat.com> 3.0.3-1
- i2c-tools 3.0.3

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 13 2009 Adam Jackson <ajax@redhat.com> 3.0.2-3
- mv /etc/modprobe.d/i2c-dev /etc/modprobe.d/i2c-dev.conf (#495455)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 11 2008 Adam Jackson <ajax@redhat.com> 3.0.2-1
- i2c-tools 3.0.2

* Wed Mar  5 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.0-3
- Change /dev/i2c-# creation from /lib/udev/devices to /etc/udev/makedev.d
  usage
- Add an /etc/modprobe.d/i2c-dev file to work around bug 380971

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.0.0-2
- Autorebuild for GCC 4.3

* Tue Nov 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.0-1
- Initial Fedora package, based on Suse specfile

* Mon Oct 15 2007 - jdelvare@suse.de
- Initial release.
