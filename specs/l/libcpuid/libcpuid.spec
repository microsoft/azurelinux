# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libcpuid
Version:        0.8.1
Release:        4%{?dist}
Summary:        Provides CPU identification for x86 and ARM
License:        BSD-2-Clause
URL:            https://github.com/anrieff/libcpuid
Source0:        https://github.com/anrieff/libcpuid/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
ExcludeArch:    ppc64le s390x

BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  python3-devel
BuildRequires:  python3-pytest

%description
Libcpuid provides CPU identification for the x86 (x86_64) and ARM architectures.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
For details about the programming API, please see the docs
on the project's site (http://libcpuid.sourceforge.net/)

%package static
Summary:        Static development files for %{name}
Requires:       %{name}-devel%{_isa} = %{version}-%{release}

%description static
The %{name}-static package contains a library for developing applications
that need to use %{name} statically.

%package -n python3-%{name}
Summary:        Python bindings for the libcpuid library
Requires:       %{name}%{_isa} = %{version}-%{release}

%description -n python3-%{name}
The python3-%{name} package contains Python bindings for the libcpuid library.

%prep
%autosetup -p1 -n %{name}-%{version}

%generate_buildrequires
cd python
# CFFI tries to compile the bindings when get_requires_for_build_wheel is called
# https://github.com/python-cffi/cffi/issues/190
mv setup.py{,.ignore}
%pyproject_buildrequires
mv setup.py{.ignore,}

%build
autoreconf -vfi
%configure
%make_build

pushd python
%pyproject_wheel
popd

%install
%make_install
# WARNING: empty dependency_libs variable. remove the pointless .la
rm %{buildroot}%{_libdir}/*.la

%ldconfig_scriptlets

pushd python
%pyproject_install
popd

%pyproject_save_files -L %{name}

%check
LD_LIBRARY_PATH=%{buildroot}%{_libdir} %pytest python/tests

%files
%doc Readme.md
%license COPYING
%{_libdir}/%{name}.so.*

%files devel
%{_bindir}/cpuid_tool
%{_includedir}/%{name}
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/*.3.*

%files static
%{_libdir}/%{name}.a

%files -n python3-%{name} -f %{pyproject_files}
%doc python/README.md


%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.8.1-3
- Rebuilt for Python 3.14.0rc3 bytecode

* Tue Aug 26 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 0.8.1-2
- Use pyproject macros for dependencies

* Wed Aug 20 2025 Martin Gansser <martinkg@fedoraproject.org> - 0.8.1-1
- Update to 0.8.1

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.8.0-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 0.8.0-4
- Drop unused wheel dependency

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.8.0-2
- Rebuilt for Python 3.14

* Sun May 04 2025 Martin Gansser <martinkg@fedoraproject.org> - 0.8.0-1
- Update to 0.8.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Dec 01 2024 Martin Gansser <martinkg@fedoraproject.org> - 0.7.1-1
- Update to 0.7.1

* Tue Sep 03 2024 Martin Gansser <martinkg@fedoraproject.org> - 0.7.0-3
- Add BR pyproject-rpm-macros

* Sun Sep 01 2024 Pavol Žáčik <pzacik@redhat.com> - 0.7.0-2
- Build for aarch64
- Add Python bindings as a subpackage

* Wed Aug 28 2024 Martin Gansser <martinkg@fedoraproject.org> - 0.7.0-1
- Update to 0.7.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 04 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 0.6.5-4
- Enable static library for cpu-x flatpaks

* Thu May 23 2024 Pavol Žáčik <pzacik@redhat.com> - 0.6.5-3
- Patch bugs found by static analysis tools
- Add %%{name}-fix-handle-leaks-in-rdmsr-c.patch
- Add %%{name}-fix-cpuid_get_hypervisor.patch
- Add %%{name}-prevent-intel_fn11-array-overruns.patch

* Thu May 09 2024 Pavol Žáčik <pzacik@redhat.com> - 0.6.5-2
- Specify license using an SPDX identifier

* Tue Apr 30 2024 Martin Gansser <martinkg@fedoraproject.org> - 0.6.5-1
- Update to 0.6.5

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 09 2023 Martin Gansser <martinkg@fedoraproject.org> - 0.6.4-1
- Update to 0.6.4

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May 03 2023 Martin Gansser <martinkg@fedoraproject.org> - 0.6.3-1
- Update to 0.6.3

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Nov 12 2022 Martin Gansser <martinkg@fedoraproject.org> - 0.6.2-1
- Update to 0.6.2

* Sat Oct 22 2022 Martin Gansser <martinkg@fedoraproject.org> - 0.6.0-1
- Update to 0.6.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Sep 02 2021 Martin Gansser <martinkg@fedoraproject.org> - 0.5.1-1
- Update to 0.5.1

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 22 2020 Martin Gansser <martinkg@fedoraproject.org> - 0.5.0-1
- Update to 0.5.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Martin Gansser <martinkg@fedoraproject.org> - 0.4.1-1
- Update to 0.4.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-8.20171023git2f10315
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-7.20171023git2f10315
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-6.20171023git2f10315
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-5.20171023git2f10315
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct 23 2017 Martin Gansser <martinkg@fedoraproject.org> - 0.4.0-4.20171023git2f10315
- Update to 0.4.0-4.20171023git2f10315
- Dropped %%{name}-not-use-4m-macro.patch
- Add ExcludeArch: aarch64 %%arm ppc64le ppc64 s390x

* Mon Oct 23 2017 Martin Gansser <martinkg@fedoraproject.org> - 0.4.0-3.20170504git57298c6
- Add BR doxygen
- disable build of static lib
- don't remove %%exclude %%{_libdir}/%%{name}.so
- Add %%{name}-not-use-4m-macro.patch

* Mon Oct 23 2017 Martin Gansser <martinkg@fedoraproject.org> - 0.4.0-2.20170504git57298c6
- Add BR gcc-c++
- replace libtoolize and autoreconf --install with autoreconf -vfi
- remove %%exclude %%{_libdir}/%%{name}.so.* not needed

* Sun Oct 22 2017 Martin Gansser <martinkg@fedoraproject.org> - 0.4.0-1.20170504git57298c6
- Initial build.
