Summary:        The GNU portable thread library.
Name:           pth
Version:        2.0.7
Release:        4%{?dist}
License:        LGPLv2+
URL:            https://www.gnu.org/software/pth/
Group:          System Environment/Libraries.
Source0:        https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Mariner

%description

Pth is a very portable POSIX/ANSI-C based library for Unix platforms which
provides non-preemptive priority-based scheduling for multiple threads of
execution (aka ``multithreading'') inside event-driven applications. All
threads run in the same address space of the server application, but each
thread has it's own individual program-counter, run-time stack, signal
mask and errno variable.

%package devel
Summary:       GNU pth development header and libraries.
Group:         Development/Libraries.
Requires:      pth = %{version}

%description devel
Development package for pth.

%prep
%setup -q

%build
%configure --disable-static \
           --prefix=%{_prefix}
make

%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete

%check
make %{?_smp_mflags} -k check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.so
%{_mandir}/*/*
%{_datadir}/aclocal/*

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.0.7-4
- Added %%license line automatically

*   Mon Apr 27 2020 Nick Samson <nisamson@microsoft.com> 2.0.7-3
-   Updated Source0. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.0.7-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Wed Jul 27 2016 Kumar Kaushik <kaushikk@vmware.com> 2.0.7-1
-   Initial Build.
