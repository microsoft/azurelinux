# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global githubname   libbpf
%global githubver    1.6.1
%global githubfull   %{githubname}-%{githubver}
%global libver       1.6.1

Name:           %{githubname}
Version:        %{githubver}
Release: 4%{?dist}
Summary:        Libbpf library

License:        LGPL-2.1-only OR BSD-2-Clause
URL:            https://github.com/%{githubname}/%{githubname}
Source:         https://github.com/%{githubname}/%{githubname}/archive/v%{githubver}.tar.gz
BuildRequires:  gcc elfutils-libelf-devel elfutils-devel
BuildRequires: make

Patch1:         libbpf-Add-the-ability-to-suppress-perf-event-enable.patch

# This package supersedes libbpf from kernel-tools,
# which has default Epoch: 0. By having Epoch: > 0
# this libbpf will take over smoothly
Epoch:          2

%description
A mirror of bpf-next linux tree bpf-next/tools/lib/bpf directory plus its
supporting header files. The version of the package reflects the version of
ABI.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = 2:%{version}-%{release}
Requires:       kernel-headers >= 5.16.0
Requires:       zlib

%description devel
The %{name}-devel package contains libraries header files for
developing applications that use %{name}

%package static
Summary: Static library for libbpf development
Requires: %{name}-devel = 2:%{version}-%{release}

%description static
The %{name}-static package contains static library for
developing applications that use %{name}

%define _lto_cflags %{nil}

%global make_flags PREFIX=%{_prefix} INCLUDEDIR=%{_includedir} DESTDIR=%{buildroot} \
	OBJDIR=%{_builddir} CFLAGS="%{build_cflags} -fPIC" LDFLAGS="%{build_ldflags} \
	-Wl,--no-as-needed" LIBDIR=/%{_libdir} NO_PKG_CONFIG=1

%prep
%autosetup -n %{githubfull} -p1

%build
%make_build -C ./src %{make_flags}

%install
%make_install -C ./src %{make_flags}

%files
%{_libdir}/libbpf.so.%{libver}
%{_libdir}/libbpf.so.1

%files devel
%{_libdir}/libbpf.so
%{_includedir}/bpf/
%{_libdir}/pkgconfig/libbpf.pc

%files static
%{_libdir}/libbpf.a

%changelog
* Tue Aug 12 2025 Viktor Malik <vmalik@redhat.com> - 2:1.6.1-3
- Backport patch to fix latest perf builds

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 21 2025 Viktor Malik <vmalik@redhat.com> - 2:1.6.1-1
- release 1.6.1-1

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Oct 31 2024 Viktor Malik <vmalik@redhat.com> - 2:1.5.0-1
- release 1.5.0-1

* Fri Sep 06 2024 Viktor Malik <vmalik@redhat.com> - 2:1.4.6-1
- release 1.4.6-1

* Thu Aug 22 2024 Viktor Malik <vmalik@redhat.com> - 2:1.4.5-1
- release 1.4.5-1

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 02 2024 Viktor Malik <vmalik@redhat.com> - 2:1.4.3-1
- release 1.4.3-1

* Fri May 03 2024 Viktor Malik <vmalik@redhat.com> - 2:1.4.1-1
- release 1.4.1-1

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 05 2023 Jiri Olsa <olsajiri@gmail.com> - 2:1.2.0-1
- release 1.2.0-1

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Viktor Malik <vmalik@redhat.com> - 2:1.1.0-3
- Migrate license to SPDX

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 22 2022 Jiri Olsa <olsajiri@gmail.com> - 2:1.1.0-1
- release 1.1.0-1

* Tue Dec 20 2022 Jiri Olsa <olsajiri@gmail.com> - 2:1.0.0-4
- CVE-2022-3606 fix

* Tue Nov 01 2022 Jiri Olsa <olsajiri@gmail.com> - 2:1.0.0-3
- release 1.0.0-3

* Sat Sep 03 2022 Jiri Olsa <olsajiri@gmail.com> - 2:1.0.0-1
- release 1.0.0-1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed May 18 2022 Jiri Olsa <olsajiri@gmail.com> - 2:0.8.0-1
- release 0.8.0-1

* Fri Feb 18 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2:0.7.0-3
- Re-enable package notes

* Fri Feb 15 2022 Jay W <git.jaydobuleu@gmail.com> - 2:0.7.0-2
- Ensure PREFIX=%{_prefix} INCLUDEDIR=%{_includedir} are set so that flatpak is
  able to build libbpf as dependency.

* Sun Feb 13 2022 Jiri Olsa <jolsa@redhat.com> - 2:0.7.0-1
- release 0.7.0-1

* Tue Feb 08 2022 Jiri Olsa <jolsa@redhat.com> - 2:0.6.1-1
- release 0.6.1-1

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Sep 10 2021 Jiri Olsa <jolsa@redhat.com> - 2:0.5.0-1
- release 0.5.0-1

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed May 26 2021 Jiri Olsa <jolsa@redhat.com> - 2:0.4.0-1
- release 0.4.0-1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Jiri Olsa <jolsa@redhat.com> - 2:0.3.0-1
- release 0.3.0-1

* Thu Oct 01 2020 Jiri Olsa <jolsa@redhat.com> - 2:0.1.0-1
- release 0.1.0

* Sun Aug 02 2020 Jiri Olsa <jolsa@redhat.com> - 2:0.0.9-1
- release 0.0.9

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.0.8-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 10 2020 Jiri Olsa <jolsa@redhat.com> - 2:0.0.8-1
- release 0.0.8

* Wed Mar 03 2020 Jiri Olsa <jolsa@redhat.com> - 2:0.0.7-1
- release 0.0.7

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 2 2020 Jiri Olsa <jolsa@redhat.com> - 0.0.6-2
- release 0.0.6-2, build server issues

* Mon Dec 30 2019 Jiri Olsa <jolsa@redhat.com> - 0.0.6-1
- release 0.0.6

* Thu Nov 28 2019 Jiri Olsa <jolsa@redhat.com> - 0.0.5-3
- release 0.0.5

* Fri Nov 22 2019 Jiri Olsa <jolsa@redhat.com> - 0.0.3-3
- Revert to 0.0.3 version and adjust kernel-headers dependency (BZ#1755317)

* Tue Nov 12 2019 Jiri Olsa <jolsa@redhat.com> - 0.0.5-2
- Add kernel-headers dependency

* Thu Oct 03 2019 Jiri Olsa <jolsa@redhat.com> - 0.0.5-1
- release 0.0.5

* Wed Sep 25 2019 Jiri Olsa <jolsa@redhat.com> - 0.0.3-2
- Fix libelf linking (BZ#1755317)

* Fri Sep 13 2019 Jiri Olsa <jolsa@redhat.com> - 0.0.3-1
- Initial release
