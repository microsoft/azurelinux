Summary:       Device Tree Compiler
Name:          dtc
Version:       1.5.1
Release:       3%{?dist}
License:       BSD or GPLv2+
URL:           https://devicetree.org/
Group:         Development/Tools
Vendor:        Microsoft Corporation
Distribution:  Mariner
Source0:       https://kernel.org/pub/software/utils/%{name}/%{name}-%{version}.tar.gz
Patch0:        dtc-disable-warning.patch

BuildRequires: gcc make
BuildRequires: flex bison swig

%description
Devicetree is a data structure for describing hardware. Rather than hard coding
every detail of a device into an operating system, many aspects of the hardware
can be described in a data structure that is passed to the operating system at
boot time. The devicetree is used by OpenFirmware, OpenPOWER Abstraction Layer
(OPAL), Power Architecture Platform Requirements (PAPR) and in the standalone
Flattened Device Tree (FDT) form.

%package devel
Summary: Development headers for device tree library
Requires: %{name} = %{version}-%{release}

%description devel
This package provides development files for libfdt

%prep
%autosetup -p1
sed -i 's/python2/python3/' pylibfdt/setup.py
sed -i 's/SUBLEVEL = 0/SUBLEVEL = 1/' Makefile


%build
make %{?_smp_mflags} V=1 CC="gcc $RPM_OPT_FLAGS $RPM_LD_FLAGS"

%install
make install DESTDIR=%{buildroot} PREFIX=%{buildroot}/usr \
                            LIBDIR=%{_libdir} BINDIR=%{_bindir} INCLUDEDIR=%{_includedir} V=1

%clean
rm -rf %{buildroot}/*

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
* Mon Apr 12 2021 Henry Li <lihl@microsoft.com> 1.5.1-3
- Apply patch to disable treating cast-qual and missing-prototypes as errors
- Add %{python3_sitearch}/

* Thu Apr 09 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.5.1-2
- Fixed "Source0" tag.
- License verified and "License" tag updated.
- Removed "%%define sha1".

* Thu Sep 26 2019 Henry Beberman <hebeberm@microsoft.com> - 1.5.1-1
- Original version for CBL-Mariner.
