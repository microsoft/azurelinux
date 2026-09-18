# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libfyaml
Version:        0.8
Release:        8%{?dist}
Summary:        Complete YAML parser and emitter

# All files MIT except
# GPL-2.0-only 
# src/lib/fy-list.h
# BSD-2-clause
# src/xxhash/xxhash.c
# src/xxhash/xxhash.h
License:        MIT and GPL-2.0-only and BSD-2-Clause
URL:            https://github.com/pantoniou/libfyaml
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        LICENSE-GPL-2.0
Source2:        LICENSE-BSD-2-Clause
Patch0:         obsolete-macros-update.patch

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: check
BuildRequires: gcc
BuildRequires: libtool
BuildRequires: libtool-ltdl-devel
BuildRequires: libyaml-devel
BuildRequires: make
BuildRequires: python3-sphinx
#BuildRequires: xxhash-devel
# Needed to update macro
BuildRequires: sed
# Bundled modified old version of xxhash (https://xxhash.com/) is used
# Unclear exact old version it is derived from
# Issue to update to newer version:
# https://github.com/pantoniou/libfyaml/issues/92
Provides: bundled(libxxhash)

%description
A fancy 1.2 YAML and JSON parser/writer.

Fully feature complete YAML parser and emitter, supporting
the latest YAML spec and passing the full YAML testsuite.

It is designed to be very efficient, avoiding copies of data,
and has no artificial limits like the 1024 character limit for
implicit keys.

%package devel
Summary:  Complete YAML parser and emitter
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for libfyaml

%prep
%autosetup

%build
cp %{SOURCE1} .
cp %{SOURCE2} .

autoreconf -fi
%configure --disable-static
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
%make_build

%install
%make_install

%check
# Run basic tests
make check

%files
%license LICENSE
%license LICENSE-GPL-2.0
%license LICENSE-BSD-2-Clause
%doc README.md
%doc AUTHORS
%{_bindir}/fy-compose
%{_bindir}/fy-dump
%{_bindir}/fy-filter
%{_bindir}/fy-join
%{_bindir}/fy-testsuite
%{_bindir}/fy-tool
%{_bindir}/fy-ypath
%{_libdir}/libfyaml.so.0
%{_libdir}/libfyaml.so.0.0.0
%{_mandir}/man1/fy-compose.1.gz
%{_mandir}/man1/fy-dump.1.gz
%{_mandir}/man1/fy-filter.1.gz
%{_mandir}/man1/fy-join.1.gz
%{_mandir}/man1/fy-testsuite.1.gz
%{_mandir}/man1/fy-tool.1.gz
%{_mandir}/man1/fy-ypath.1.gz

%files devel
%{_includedir}/libfyaml.h
%{_libdir}/libfyaml.so
%{_libdir}/pkgconfig/libfyaml.pc

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Benson Muite <benson_muite@emailplus.org> - 0.8-2
- Add license files
- Replace obsolete AC_PROG_TOOL with LT_INIT
- Indicate libxxhash is bundled

* Sat Jul 08 2023 Benson Muite <benson_muite@emailplus.org> - 0.8-1
- Initial packaging

