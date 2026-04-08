# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# git ls-remote https://github.com/roc-streaming/roc-toolkit.git
#global git_commit 127cfc645d0a807a33506001367b6d9a9d46f23e
#global git_date 20230110

#global git_short_commit %%(echo %%{git_commit} | cut -c -8)
#global git_suffix %%{git_date}git%%{git_short_commit}

Name:		roc-toolkit
#Version:	0.2.1^%%{git_suffix}
Version:	0.4.0
Release:	3%{?dist}
Summary:	Real-time audio streaming
License:	MPL-2.0 AND LGPL-2.1-or-later AND CECILL-C
URL:		https://github.com/roc-streaming/roc-toolkit
#Source0:	%%{url}/archive/%%{git_commit}/%%{name}-%%{git_suffix}.tar.gz
Source0:	%{url}/archive/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	python3-devel
BuildRequires:	python3-scons
BuildRequires:	python3-sphinxemoji
BuildRequires:	python3-setuptools
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	pkgconf-pkg-config
BuildRequires:	gengetopt
BuildRequires:	ragel
BuildRequires:	libuv-devel
BuildRequires:	libunwind-devel
BuildRequires:	sox-devel
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	openfec-devel
BuildRequires:	cpputest-devel
BuildRequires:	python3-sphinx
BuildRequires:	python3-breathe
BuildRequires:	speexdsp-devel
BuildRequires:	openssl-devel
BuildRequires:	doxygen
BuildRequires:	libsndfile-devel
# https://github.com/roc-streaming/roc-toolkit/issues/481
Patch0:		roc-toolkit-0.3.0-no-explicit-cpp98.patch

%description
Roc is a toolkit for real-time audio streaming over the network.

%package devel
Summary: Development libraries for roc-toolkit
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The roc-toolkit-devel package contains header files necessary for
developing programs using roc-toolkit.

%package utils
Summary: Utilities for roc-toolkit
Requires: %{name}%{?_isa} = %{version}-%{release}

%description utils
Utilities for roc-toolkit.

%package doc
Summary: Documentation for roc-toolkit

%description doc
Documentation for roc-toolkit.

%prep
#autosetup -p1 -n %{name}-%{git_commit}
%autosetup -p1 -n %{name}-%{version}

%build
scons %{?_smp_mflags} --with-openfec-includes=%{_includedir}/openfec \
  CFLAGS="%{build_cflags}" CXXFLAGS="%{build_cxxflags}" LDFLAGS="%{build_ldflags}"
scons docs --enable-doxygen --enable-sphinx

%install
scons install --with-openfec-includes=%{_includedir}/openfec --prefix=%{buildroot}%{_prefix} \
  --libdir=%{buildroot}%{_libdir}

# temporal dirty workaround for https://github.com/roc-streaming/roc-toolkit/issues/744
%ifnarch s390x
%check
scons test --with-openfec-includes=%{_includedir}/openfec --enable-tests
%endif

%files
%license LICENSE
%doc README.md
%{_libdir}/libroc.so.0*

%files devel
%{_includedir}/roc
%{_libdir}/libroc.so
%{_libdir}/pkgconfig/roc.pc

%files utils
%{_bindir}/roc-copy
%{_bindir}/roc-recv
%{_bindir}/roc-send
%{_mandir}/man1/*.1.gz

%files doc
%doc docs/html

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Aug  6 2024 Jaroslav Škarvada <jskarvad@redhat.com> - 0.4.0-1
- New version

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Feb  1 2024 Jaroslav Škarvada <jskarvad@redhat.com> - 0.3.0-1
- New version
- Fixed FTBFS
  Resolves: rhbz#2261654

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Aug  8 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 0.2.1-4
- Fixed FTBFS
  Resolves: rhbz#2226398

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 10 2023 Wim Taymans <wtaymans@redhat.com> - 0.2.1-1
- Update to 0.2.1

* Sat Dec 24 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 0.1.5^20221224git2017450a-1
- New snapshot

* Tue Oct 11 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 0.1.5^20220829git863a0227-3
- Disabled tests on 32 bit architectures (code is broken, use on own risk)

* Mon Oct 10 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 0.1.5^20220829git863a0227-2
- Switched license tag to SPDX format

* Sat Aug 20 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 0.1.5^20220829git863a0227-1
- Initial version
