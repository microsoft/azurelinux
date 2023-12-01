Summary:        Device Tree Compiler
Name:           dtc
Version:        1.6.1
Release:        1%{?dist}
License:        BSD OR GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://devicetree.org/
Source0:        https://kernel.org/pub/software/utils/%{name}/%{name}-%{version}.tar.gz
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  swig
Provides:       libfdt = %{name}-%{version}
Provides:       python3-libfdt = %{name}-%{version}

%description
Devicetree is a data structure for describing hardware. Rather than hard coding
every detail of a device into an operating system, many aspects of the hardware
can be described in a data structure that is passed to the operating system at
boot time. The devicetree is used by OpenFirmware, OpenPOWER Abstraction Layer
(OPAL), Power Architecture Platform Requirements (PAPR) and in the standalone
Flattened Device Tree (FDT) form.

%package        devel
Summary:        Development headers for device tree library
Requires:       %{name} = %{version}-%{release}
Provides:       libfdt-devel = %{version}-%{release}
Provides:       libfdt-static = %{version}-%{release}

%description devel
This package provides development files for libfdt

%prep
%autosetup -p1
sed -i 's/python2/python3/' pylibfdt/setup.py
sed -i 's/SUBLEVEL = 0/SUBLEVEL = 1/' Makefile

%build
make %{?_smp_mflags} V=1 CC="gcc %{optflags} $LDFLAGS -Wno-error=missing-prototypes -Wno-error=cast-qual" NO_PYTHON=1

%install
%make_install \
    PREFIX=%{buildroot}%{_prefix} \
    LIBDIR=%{_libdir} \
    BINDIR=%{_bindir} \
    INCLUDEDIR=%{_includedir}

%files
%license GPL
%doc Documentation/manual.txt
%{_bindir}/*
%{_libdir}/libfdt-%{version}.so
%{_libdir}/libfdt.so.*
%{python3_sitearch}/

%files devel
%{_libdir}/libfdt.so
%{_libdir}/libfdt.a
%{_includedir}/*

%changelog
* Tue Nov 09 2021 Andrew Phelps <anphel@microsoft.com> - 1.6.1-1
- Update to version 1.6.1
- Remove dtc-disable-warning.patch

* Fri Jul 23 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.5.1-4
- Add compatibility provides for libfdt, libfdt-static, libfdt-devel, python3-libfdt packages
- Use make macros throughout, lint spec

* Mon Apr 12 2021 Henry Li <lihl@microsoft.com> - 1.5.1-3
- Apply patch to disable treating cast-qual and missing-prototypes as errors
- Add %{python3_sitearch}/

* Thu Apr 09 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.1-2
- Fixed "Source0" tag.
- License verified and "License" tag updated.
- Removed "%%define sha1".

* Thu Sep 26 2019 Henry Beberman <hebeberm@microsoft.com> - 1.5.1-1
- Original version for CBL-Mariner.
