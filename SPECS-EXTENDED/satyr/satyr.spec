Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%if 0%{?fedora} || 0%{?rhel} > 7
# Enable python3 build by default
%bcond_without python3
%else
%bcond_with python3
%endif
 
%if 0%{?suse_version}
  %define libdw_devel libdw-devel
  %define libelf_devel libelf-devel
%else
  %define libdw_devel elfutils-devel
  %define libelf_devel elfutils-libelf-devel
%endif
 
%define glib_ver 2.43.4
 
Name: satyr
Version: 0.43
Release: 1%{?dist}
Summary: Tools to create anonymous, machine-friendly problem reports
License: GPL-2.0-or-later
URL: https://github.com/abrt/satyr
Source0: https://github.com/abrt/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz
%if %{with python3}
BuildRequires: python3-devel
%endif
BuildRequires: %{libdw_devel}
BuildRequires: %{libelf_devel}
BuildRequires: binutils-devel
BuildRequires: rpm-devel
BuildRequires: libtool
BuildRequires: doxygen
BuildRequires: pkgconfig
BuildRequires: make
BuildRequires: automake
BuildRequires: gcc-c++
BuildRequires: gdb
BuildRequires: gperf
BuildRequires: json-c-devel
BuildRequires: glib2-devel
%if %{with python3}
BuildRequires: python3-sphinx
%endif
Requires: json-c%{?_isa}
Requires: glib2%{?_isa} >= %{glib_ver}
 
%description
Satyr is a library that can be used to create and process microreports.
Microreports consist of structured data suitable to be analyzed in a fully
automated manner, though they do not necessarily contain sufficient information
to fix the underlying problem. The reports are designed not to contain any
potentially sensitive data to eliminate the need for review before submission.
Included is a tool that can create microreports and perform some basic
operations on them.
 
%package devel
Summary: Development libraries for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
 
%description devel
Development libraries and headers for %{name}.
 
%if %{with python3}
%package -n python3-satyr
%{?python_provide:%python_provide python3-satyr}
Summary: Python 3 bindings for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
 
%description -n python3-satyr
Python 3 bindings for %{name}.
%endif
 
%prep
%setup -q
 
%build
autoreconf
 
%configure \
%if %{without python3}
        --without-python3 \
%endif
        --disable-static \
        --enable-doxygen-docs
 
%make_build
%install
%make_install
# Remove all libtool archives (*.la) from modules directory.
find %{buildroot} -name "*.la" -delete
 
%check
make check|| {
    # find and print the logs of failed test
    # do not cat tests/testsuite.log because it contains a lot of bloat
    cat tests/test-suite.log
    find tests/testsuite.dir -name "testsuite.log" -print -exec cat '{}' \;
    exit 1
}
 
%if 0%{?fedora} > 27
# ldconfig is not needed
%else
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%endif
 
%files
%doc README.md NEWS
%license COPYING
%{_bindir}/satyr
%{_mandir}/man1/%{name}.1*
%{_libdir}/lib*.so.*
 
%files devel
# The complex pattern below (instead of simlpy *) excludes Makefile{.am,.in}:
%doc apidoc/html/*.{html,png,css,js}
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
 
%if 0%{?with_python3}
%files -n python3-satyr
%dir %{python3_sitearch}/%{name}
%{python3_sitearch}/%{name}/*
%endif

%changelog
* Tue Nov 12 2024 Sumit Jena <v-sumitjena@microsoft.com> - 0.43-1
- Update to version 0.43

* Tue Jan 12 2021 Joe Schmitt <joschmit@microsoft.com> - 0.30-3
- Initial CBL-Mariner import from Fedora 31 (license: MIT).
- Build with python3

* Fri Feb 07 2020 Ernestas Kulik <ekulik@redhat.com> - 0.30-2
- Bump for side tag rebuild

* Thu Feb 06 2020 Michal Fabik <mfabik@redhat.com> - 0.30-1
- Fix registers being parsed as modules in kernel oopses in some cases
- Use Nettle for cryptographic calculations

* Thu Jan 30 2020 Martin Kutlak <mkutlak@redhat.com> - 0.29-3
- Add patch to fix build failure with gcc -fno-common
- Resolves: #1796384

* Mon Nov 11 2019 Ernestas Kulik <ekulik@redhat.com> - 0.29-2
- Add patch for https://bugzilla.redhat.com/show_bug.cgi?id=1518943

* Fri Oct 11 2019 Matěj Grabovský <mgrabovs@redhat.com> 0.29-1
- spec: Switch sources tarball compression from xz to gzip
- spec: Replace xargs rm with delete
- spec: Remove provides for satyr-python3
- spec: Replace make with rpm macros
- Replace bundled JSON parser with json-c
- lib: normalize: Hash removable function names
- rpm: Fix typo in a static function name
- json: Improve error messages on EOF
- json: Use backticks consistently in error messages
- json,style: Improve code style consistency slightly
- json: Update to latest upstream version
- core: Document unknown core frame address
- style: Correct parenthesization for bitfield tests
- style: Use specific integer types instead of the generic int
- style: Use *_MAX constants instead of -1 in unsigned comparisons

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.28-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.28-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 21 2019 Ernestas Kulik <ekulik@redhat.com> - 0.28-1
- New version 0.28

* Mon Jun 10 22:13:23 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.27-4
- Rebuild for RPM 4.15

* Mon Jun 10 15:42:05 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.27-3
- Rebuild for RPM 4.15

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 8 2018 Martin Kutlak <mkutlak@redhat.com> 0.27-1
- New upstream version
 - Improve format of truncated backtrace for Python and core

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Matej Habrnal <mhabrnal@redhat.com> 0.26-3
- Anonymize paths in frames
- Test fix: correct syntax for gdb backtrace command

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.26-2
- Rebuilt for Python 3.7

* Tue Apr 17 2018 Matej Habrnal <mhabrnal@redhat.com> 0.26-1
- spec: fix Allow python2 to be optional at build time
- Allow python2 to be optional at build time
- normalization: actualize list of functions
- Append Python interpreter as related package
- makefile: create .tar.xz with make release

* Thu Jan 18 2018 Martin Kutlak <mkutlak@redhat.com> 0.25-1
- New upstream version
 - Normalization: actualize list of functions
 - Fix some compilation warnings
 - Allow to build python3 for rhel8
 - Makefile: add make release-* subcommands
 - Elfutils: Add missing stubs from earlier commit

* Wed Nov 1 2017 Julius Milan <jmilan@redhat.com> 0.24-1
- New upstream version
  - Allow to report unpackaged problems
  - apidoc: generate html docs using doxygen
  - Fix parsing of subset of arm kernel oopses

* Mon Mar 13 2017 Matej Habrnal <mhabrnal@redhat.com> 0.23-1
- New upstream version
  - Allow rpm to be optional at build time
  - Do not use deprecated fedorahosted.org

* Thu Dec 1 2016 Jakub Filak <jakub@thefilaks.net> 0.22-1
- New upstream version
  - Added support fof JavaScript (V8) stack traces
  - Most parts of the in-hook core unwinder callable under unprivileged user
  - GDB core unwinder limits number of unwound frames
  - Fixed a pair of compile warnings - Chris Redmon <credmonster@gmail.com>

* Wed May 18 2016 Matej Habrnal <mhabrnal@redhat.com> 0.21-1
- New upstream version
  - Introduce 'serial' field in uReport
  - normalization: actualize list of functions
