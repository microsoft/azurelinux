# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# SPDX-License-Identifier: MIT
# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>

%bcond tests 1

Name:           forge-srpm-macros
Version:        0.4.0
Release:        3%{?dist}
Summary:        Macros to simplify packaging of forge-hosted projects

License:        GPL-1.0-or-later
URL:            https://git.sr.ht/~gotmax23/forge-srpm-macros
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  make
%if %{with tests}
BuildRequires:  python3-pytest
BuildRequires:  python3-pyyaml
# For %%pytest definition
BuildRequires:  python3-rpm-macros
%endif

# We require macros and lua defined in redhat-rpm-config
# We constrain this to the version released after the code was split out that
# doesn't contain the same files.
%if (0%{?fedora} >= 40 || 0%{?rhel} >= 10)
Requires:       redhat-rpm-config >= 266-1
%elif 0%{?fedora} == 39
Requires:       redhat-rpm-config >= 265-1
%else
# For testing purposes on older releases,
# we can depend on any version of redhat-rpm-config.
Requires:       redhat-rpm-config
%endif


%description
%{summary}.


%prep
%autosetup -n %{name}-v%{version}


%build
%if %{defined el9}
%make_build epel9-build
%endif


%install
%make_build \
    DESTDIR=%{buildroot} \
    RPMMACRODIR=%{_rpmmacrodir} RPMLUADIR=%{_rpmluadir} %{?el9:epel9-}install


%check
%if %{with tests}
export MACRO_DIR=%{buildroot}%{_rpmmacrodir}
export MACRO_LUA_DIR="%{buildroot}%{_rpmluadir}"
%pytest
%endif


%files
%license LICENSES/GPL-1.0-or-later.txt
%doc README.md NEWS.md
%if %{undefined el9}
%{_rpmluadir}/fedora/srpm/forge.lua
%{_rpmmacrodir}/macros.forge
%else
%{_rpmluadir}/fedora/srpm/forge_epel.lua
%{_rpmmacrodir}/macros.zzz-forge_epel
%endif
%{_rpmluadir}/fedora/srpm/_forge_util.lua


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Sep 27 2024 Maxwell G <maxwell@gtmx.me> - 0.4.0-1
- Update to 0.4.0.
- Fixes: rhbz#2303884

* Wed Aug 7 2024 Maxwell G <maxwell@gtmx.me> - 0.3.2-1
- Update to 0.3.2.

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Apr 10 2024 Maxwell G <maxwell@gtmx.me> - 0.3.1-1
- Update to 0.3.1.

* Sat Mar 2 2024 Maxwell G <maxwell@gtmx.me> - 0.3.0-1
- Update to 0.3.0.

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Dec 7 2023 Maxwell G <maxwell@gtmx.me> - 0.2.0-1
- Update to 0.2.0.

* Mon Sep 4 2023 Maxwell G <maxwell@gtmx.me> - 0.1.0-1
- Initial package. Closes rhbz#2237933.
