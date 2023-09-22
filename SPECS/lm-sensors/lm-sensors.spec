Summary:        The lm_sensors package provides user-space support for the hardware monitoring drivers in the Linux kernel.
Name:           lm-sensors
Version:        3.6.0
Release:        2%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Drivers
URL:            https://github.com/lm-sensors/lm-sensors
#Source0:       https://github.com/lm-sensors/lm-sensors/archive/V3-6-0.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  libgcc-devel
BuildRequires:  make
BuildRequires:  which
Requires:       perl
# The kernel optimized for Hyper-V doesn't have the "CONFIG_I2C_CHARDEV" configuration enabled,
# which is required by this package.
Conflicts:      kernel-hyperv
Provides:       lm_sensors = %{version}-%{release}
Provides:       %{name}-libs = %{version}-%{release}

%description
The lm_sensors package provides user-space support for the hardware monitoring drivers in the Linux kernel.
This is useful for monitoring the temperature of the CPU and adjusting the performance of some hardware (such as cooling fans).

%package   devel
Summary:        lm-sensors devel
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Provides:       lm_sensors-devel = %{version}-%{release}

%description devel
lm-sensors devel

%package   doc
Summary:        lm-sensors docs
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for lm-sensors.

%prep
%setup -q -n %{name}-3-6-0

%build
%make_build all

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_datadir}
make PREFIX=%{buildroot}%{_prefix}        \
     BUILD_STATIC_LIB=0 \
     MANDIR=%{buildroot}%{_mandir} install &&

install -v -m755 -d %{buildroot}%{_docdir}/%{name}-%{version} &&
cp -rv README INSTALL doc/* \
     %{buildroot}%{_docdir}/%{name}-%{version}

%check

%post
/sbin/modprobe i2c-dev

%postun
/sbin/modprobe -r i2c-dev

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_libdir}/libsensors.so.5
%{_libdir}/libsensors.so.5.0.0
%{_sbindir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libsensors.so

%files doc
%defattr(-,root,root)
%{_docdir}/*
%{_mandir}/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 3.6.0-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue Feb 08 2022 Henry Li <lihl@microsoft.com> - 3.6.0-1
- Upgrade to 3.6.0

* Fri Jul 23 2021 Thomas Crain <thcrain@microsoft.com> - 3.5.0-9
- Add provides for libs subpackages from base package

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 3.5.0-8
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Mon Nov 02 2020 Joe Schmitt <joschmit@microsoft.com> - 3.5.0-7
- Provide lm_sensors and lm_sensors-devel.

* Thu Jun 18 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.5.0-6
- Removing runtime dependency on a specific kernel package.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.5.0-5
- Added %%license line automatically

* Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> - 3.5.0-4
- Renaming linux to kernel

* Tue Apr 07 2020 Joe Schmitt <joschmit@microsoft.com> - 3.5.0-3
- Update Source0 with valid URL.
- Remove sha1 macro.
- Fix changelog styling
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 3.5.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Jun 20 2019 Tapas Kundu <tkundu@vmware.com> - 3.5.0-1
- Initial packaging with Photon OS.
