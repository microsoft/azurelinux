# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# enable asm implementations by default
%bcond_without asm

# enable .lz4 support by default
%bcond_without lz4

# enable .xz/.lzma support by default
%bcond_without lzma

# enable .gz support by default
%bcond_without zlib

# enable pzstd support by default
%bcond_without pzstd

# Disable gtest on RHEL
%bcond gtest %[ !0%{?rhel} ]

Name:           zstd
Version:        1.5.7
Release:        2%{?dist}
Summary:        Zstd compression library

License:        BSD-3-Clause AND GPL-2.0-only
URL:            https://github.com/facebook/zstd
Source0:        https://github.com/facebook/zstd/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

Patch1:         man-pages-1.5.7.patch

BuildRequires:  make
BuildRequires:  gcc %{?with_gtest:gtest-devel}
%if %{with lz4}
BuildRequires:  lz4-devel
%endif
%if %{with lzma}
BuildRequires:  xz-devel
%endif
%if %{with pzstd}
BuildRequires:  gcc-c++
%endif
%if %{with zlib}
BuildRequires:  zlib-devel
%endif
BuildRequires:  execstack

%description
Zstd, short for Zstandard, is a fast lossless compression algorithm,
targeting real-time compression scenarios at zlib-level compression ratio.

%package -n lib%{name}
Summary:        Zstd shared library

%description -n lib%{name}
Zstandard compression shared library.

%package -n lib%{name}-devel
Summary:        Header files for Zstd library
Requires:       lib%{name}%{?_isa} = %{version}-%{release}

%package -n lib%{name}-static
Summary:        Static variant of the Zstd library
Requires:       lib%{name}-devel = %{version}-%{release}

%description -n lib%{name}-devel
Header files for Zstd library.

%description -n lib%{name}-static
Static variant of the Zstd library.

%prep
%setup -q
find -name .gitignore -delete
%patch 1 -p1

%build
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="$RPM_LD_FLAGS"
export PREFIX="%{_prefix}"
export LIBDIR="%{_libdir}"
%make_build -C lib lib-mt %{!?with_asm:ZSTD_NO_ASM=1}
%make_build -C programs %{!?with_asm:ZSTD_NO_ASM=1}
%if %{with pzstd}
export CXXFLAGS="$RPM_OPT_FLAGS"
%make_build -C contrib/pzstd %{!?with_asm:ZSTD_NO_ASM=1}
%endif

%check
execstack lib/libzstd.so.1

export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="$RPM_LD_FLAGS"
make -C tests test-zstd
%if %{with pzstd} && %{with gtest}
export CXXFLAGS="$RPM_OPT_FLAGS"
make -C contrib/pzstd test
%endif

%install
%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir}
%if %{with pzstd}
install -D -m755 contrib/pzstd/pzstd %{buildroot}%{_bindir}/pzstd
install -D -m644 programs/%{name}.1 %{buildroot}%{_mandir}/man1/p%{name}.1
%endif

%files
%doc CHANGELOG README.md
%{_bindir}/%{name}
%if %{with pzstd}
%{_bindir}/p%{name}
%{_mandir}/man1/p%{name}.1*
%endif
%{_bindir}/%{name}mt
%{_bindir}/un%{name}
%{_bindir}/%{name}cat
%{_bindir}/%{name}grep
%{_bindir}/%{name}less
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/un%{name}.1*
%{_mandir}/man1/%{name}cat.1*
%{_mandir}/man1/%{name}grep.1*
%{_mandir}/man1/%{name}less.1*
%license COPYING LICENSE

%files -n lib%{name}
%{_libdir}/libzstd.so.*
%license COPYING LICENSE

%files -n lib%{name}-devel
%{_includedir}/zdict.h
%{_includedir}/zstd.h
%{_includedir}/zstd_errors.h
%{_libdir}/pkgconfig/libzstd.pc
%{_libdir}/libzstd.so

%files -n lib%{name}-static
%{_libdir}/libzstd.a

%ldconfig_scriptlets -n lib%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Feb 20 2025 Pádraig Brady <P@draigBrady.com> - 1.5.7-1
- latest upstream

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Mar 29 2024 Pádraig Brady <P@draigBrady.com> - 1.5.6-1
- latest upstream

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 22 2023 Jiří Kučera <jkucera@redhat.com> - 1.5.5-3
- Drop gtest on RHEL (c9s backport)

* Thu Apr 13 2023 Lukáš Zaoral <lzaoral@redhat.com> - 1.5.5-2
- migrate to SPDX license format

* Wed Apr 05 2023 Pádraig Brady <P@draigBrady.com> - 1.5.5-1
- Latest upstream

* Mon Feb 13 2023 Pádraig Brady <P@draigBrady.com> - 1.5.4-1
- Latest upstream

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu May 19 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 1.5.2-2
- ThreadPool segfault fixed so build pzst everywhere

* Sat Jan 22 2022 Pádraig Brady <P@draigBrady.com> - 1.5.2-1
- Latest upstream

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 11 2022 Pádraig Brady <P@draigBrady.com> - 1.5.1-6
- Re-enable CET protections (#2039353)

* Fri Jan 07 2022 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.5.1-5
- Enable gz, .xz/.lzma and .lz4 support

* Mon Jan 03 2022 Pádraig Brady <P@draigBrady.com> - 1.5.1-4
- Use correct prefix for pkgconfig.

* Wed Dec 29 2021 Pádraig Brady <P@draigBrady.com> - 1.5.1-3
- Avoid executable stack on i686 also.

* Tue Dec 28 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.5.1-2
- Disable amd64 assembly on non-intel architectures (#2035802):
  this should avoid the issue where an executable stack is created.

* Wed Dec 22 2021 Pádraig Brady <P@draigBrady.com> - 1.5.1-1
- Latest upstream

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 16 2021 Pádraig Brady <P@draigBrady.com> - 1.5.0-2
- Latest upstream

* Fri Mar 05 2021 Pádraig Brady <P@draigBrady.com> - 1.4.9-1
- Latest upstream

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 17 2020 Pádraig Brady <P@draigBrady.com> - 1.4.7-1
- Latest upstream

* Wed Aug 26 2020 Jeff Law <law@redhat.com> - 1.4.5-6
- Do not force C++11 mode

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.4.5-4
- Build libzstd with multi-threading support

* Mon May 25 2020 Pádraig Brady <P@draigBrady.com> - 1.4.5-3
- Build shared library with correct compiler flags

* Fri May 22 2020 Pádraig Brady <P@draigBrady.com> - 1.4.5-1
- Latest upstream

* Fri May 22 2020 Avi Kivity <avi@scylladb.com> - 1.4.4-3
- Added static library subpackage

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 15 2020 Pádraig Brady <P@draigBrady.com> - 1.4.4-1
- Latest upstream

* Wed Jul 31 2019 Pádraig Brady <P@draigBrady.com> - 1.4.2-1
- Latest upstream

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 29 2019 Pádraig Brady <P@draigBrady.com> - 1.4.0-1
- Latest upstream

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 31 2018 Pádraig Brady <P@draigBrady.com> - 1.3.8-1
- Latest upstream

* Mon Oct 08 2018 Pádraig Brady <P@draigBrady.com> - 1.3.6-1
- Latest upstream

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Pádraig Brady <P@draigBrady.com> - 1.3.5.1
- Latest upstream

* Wed Mar 28 2018 Pádraig Brady <P@draigBrady.com> - 1.3.4-1
- Latest upstream

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.3-2
- Switch to %%ldconfig_scriptlets

* Thu Dec 21 2017 Pádraig Brady <P@draigBrady.com> - 1.3.3-1
- Latest upstream

* Fri Nov 10 2017 Pádraig Brady <P@draigBrady.com> - 1.3.2-1
- Latest upstream

* Mon Aug 21 2017 Pádraig Brady <P@draigBrady.com> - 1.3.1-1
- Latest upstream

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 16 2017 Pádraig Brady <P@draigBrady.com> - 1.3.0-1
- Latest upstream

* Mon May 08 2017 Pádraig Brady <P@draigBrady.com> - 1.2.0-1
- Latest upstream

* Mon Mar 06 2017 Pádraig Brady <P@draigBrady.com> - 1.1.3-1
- Latest upstream

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 02 2016 Pádraig Brady <pbrady@redhat.com> - 1.1.1-1
- Latest upstream

* Thu Oct 6  2016 Pádraig Brady <pbrady@fb.com> 1.1.0-2
- Add pzstd(1)

* Thu Sep 29 2016 Pádraig Brady <pbrady@fb.com> 1.1.0-1
- New upstream release
- Remove examples and static lib

* Mon Sep 12 2016 Pádraig Brady <pbrady@fb.com> 1.0.0-2
- Adjust various upstream links
- Parameterize various items in spec file

* Mon Sep 5 2016 Pádraig Brady <pbrady@fb.com> 1.0.0-1
- Initial release
