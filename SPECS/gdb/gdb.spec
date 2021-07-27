Summary:        C debugger
Name:           gdb
Version:        8.3
Release:        5%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://www.gnu.org/software/gdb
Source0:        https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
Patch0:         gdb-7.12-pstack.patch
# 8.3 contains a partial fix in the form of a warning when this bug is triggered
# The complete fix is not easily backported from 9.1
Patch1:         CVE-2019-1010180.nopatch
BuildRequires:  expat-devel
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  ncurses-devel
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  xz-devel
Requires:       expat
Requires:       ncurses
Requires:       python3
Requires:       xz-libs
Provides:       %{name}-headless = %{version}-%{release}
Provides:       %{name}-gdbserver = %{version}-%{release}
%if %{with_check}
BuildRequires:  dejagnu
BuildRequires:  systemtap-sdt-devel
%endif

%description
GDB, the GNU Project debugger, allows you to see what is going on
`inside' another program while it executes -- or what
another program was doing at the moment it crashed.

%prep
%autosetup -p1

%build
%configure --with-python=%{python3}
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print
rm %{buildroot}%{_infodir}/dir

# following files conflicts with binutils-2.24-1.x86_64
rm %{buildroot}%{_includedir}/ansidecl.h
rm %{buildroot}%{_includedir}/bfd.h
rm %{buildroot}%{_includedir}/bfdlink.h
rm %{buildroot}%{_includedir}/dis-asm.h
rm %{buildroot}%{_libdir}/libbfd.a
rm %{buildroot}%{_libdir}/libopcodes.a
# following files conflicts with binutils-2.25-1.x86_64
rm %{buildroot}%{_datadir}/locale/de/LC_MESSAGES/opcodes.mo
rm %{buildroot}%{_datadir}/locale/fi/LC_MESSAGES/bfd.mo
rm %{buildroot}%{_datadir}/locale/fi/LC_MESSAGES/opcodes.mo
%ifarch aarch64
rm %{buildroot}%{_libdir}/libaarch64-unknown-linux-gnu-sim.a
%endif
%find_lang %{name} --all-name

%check
# disable security hardening for tests
rm -f $(dirname $(gcc -print-libgcc-file-name))/../specs
%make_build check TESTS="gdb.base/default.exp"

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
%exclude %{_datadir}/locale
%exclude %{_includedir}/*.h
%{_includedir}/gdb/*.h
%{_libdir}/*.so
%{_infodir}/*.gz
%{_datadir}/gdb/python/*
%{_datadir}/gdb/syscalls/*
%{_datadir}/gdb/system-gdbinit/*
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Fri Jul 23 2021 Thomas Crain <thcrain@microsoft.com> - 8.3-5
- Add compatibility provides for gdbserver subpackage
- Use make macros throughout

* Fri Mar 26 2021 Thomas Crain <thcrain@microsoft.com> - 8.3-4
- Merge the following releases from 1.0 to dev branch
- thcrain@microsoft.com, 8.3-3: Patch CVE-2019-1010180
- anphel@microsoft.com, 8.3-4: Only run gdb.base/default.exp tests

* Wed Mar 03 2021 Henry Li <lihl@microsoft.com> - 8.3-3
- Add gcc-c++ and gcc-gfortran as dependencies
- Provides gdb-headless

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 8.3-2
- Added %%license line automatically

* Mon Mar 16 2020 Henry Beberman <henry.beberman@microsoft.com> - 8.3-1
- Update to 8.3. URL fixed. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 8.2-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> - 8.2-1
- Update to version 8.2

* Thu Dec 07 2017 Alexey Makhalov <amakhalov@vmware.com> - 7.12.1-8
- Enable LZMA support

* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 7.12.1-7
- Aarch64 support

* Mon Sep 11 2017 Rui Gu <ruig@vmware.com> - 7.12.1-6
- Enable make check in docker with part of checks disabled

* Thu Aug 10 2017 Alexey Makhalov <amakhalov@vmware.com> - 7.12.1-5
- Make check improvements

* Fri Jul 21 2017 Rui Gu <ruig@vmware.com> - 7.12.1-4
- Add pstack wrapper which will invoke gdb.

* Wed Jul 12 2017 Alexey Makhalov <amakhalov@vmware.com> - 7.12.1-3
- Get tcl, expect and dejagnu from packages

* Thu May 18 2017 Xiaolin Li <xiaolinl@vmware.com> - 7.12.1-2
- Build gdb with python3.

* Wed Mar 22 2017 Alexey Makhalov <amakhalov@vmware.com> - 7.12.1-1
- Version update

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 7.8.2-3
- GA - Bump release of all rpms

* Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> - 7.8.2-2
- Handled locale files with macro find_lang

* Wed Apr 08 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 7.8.2-1
- Initial build. First version
