Summary:        Libbpf library
Name:           libbpf
Version:        1.0.1
Release:        1%{?dist}
License:        LGPLv2 OR BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/%{name}/%{name}
Source0:        https://github.com/%{name}/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  elfutils-devel
BuildRequires:  elfutils-libelf-devel
BuildRequires:  gcc
BuildRequires:  make

%description
A mirror of bpf-next linux tree bpf-next/tools/lib/bpf directory plus its
supporting header files. The version of the package reflects the version of
ABI.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       kernel-headers >= 5.9.0
Requires:       zlib

%description    devel
The %{name}-devel package contains libraries header files for
developing applications that use %{name}

%define _lto_cflags %{nil}
%global make_flags DESTDIR=%{buildroot} OBJDIR=%{_builddir} CFLAGS="%{build_cflags} -fPIC" LDFLAGS="%{build_ldflags} -Wl,--no-as-needed" LIBDIR=/%{_libdir} NO_PKG_CONFIG=1

%prep
%autosetup

%build
%make_build -C ./src %{make_flags}

%install
%make_install -C ./src %{make_flags}
find %{buildroot} -type f -name "*.a" -delete -print

%files
%{_libdir}/libbpf.so.%{version}
%{_libdir}/libbpf.so.1

%files devel
%{_libdir}/libbpf.so
%{_includedir}/bpf/
%{_libdir}/pkgconfig/libbpf.pc

%changelog
* Mon Oct 03 2022 Muhammad Falak <mwani@microsoft.com> - 1.0.1-1
- Bump version to 1.0.1

* Fri Sep 09 2022 Muhammad Falak <mwani@microsoft.com> - 1.0.0-1
- Bump version to 1.0.0

* Wed Sep 22 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.4.0-3
- Initial CBL-Mariner import from Fedora 35 (license: MIT)
- Lint spec and remove epoch
- Remove static subpackage
- License verified

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
