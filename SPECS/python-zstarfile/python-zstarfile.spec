# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Copyright (C) 2024 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT
# License text: https://spdx.org/licenses/MIT

Name:           python-zstarfile
Version:        0.3.0
Release:        4%{?dist}
Summary:        Tarfile extension with additional compression algorithms and PEP 706 by default


License:        MIT
URL:            https://sr.ht/~gotmax23/zstarfile
%global furl    https://git.sr.ht/~gotmax23/zstarfile
Source0:        %{furl}/refs/download/v%{version}/zstarfile-%{version}.tar.gz
Source1:        %{furl}/refs/download/v%{version}/zstarfile-%{version}.tar.gz.asc
Source2:        https://meta.sr.ht/~gotmax23.pgp

BuildArch:      noarch

BuildRequires:  gnupg2
BuildRequires:  python3-devel

# zstandard is part of stdlib on Python 3.14, so no need to pull in pyzstd by default.
# Zstarfile still provides an option pyzstopen method that uses pyzstd.
Recommends:     (%{py3_dist zstarfile[zstandard]} if python(abi) < 3.14)
Recommends:     python3-zstarfile+lz4

%global _description %{expand:
zstarfile is a tarfile extension with additional compression algorithms and
PEP 706 by default.}

%description %_description

%package -n python3-zstarfile
Summary:        %{summary}

%description -n python3-zstarfile %_description


%prep
%gpgverify -d0 -s1 -k2
%autosetup -p1 -n zstarfile-%{version}


%generate_buildrequires
%pyproject_buildrequires -x all,lz4,zstandard,test


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files zstarfile


%check
# ERROR_FOR_MISSING makes it so the tests don't try to use pytest.importorskip
# which doesn't support exc_type on EPEL 9 and 10 (pytest is too old).
%if 0%{?rhel} <= 10
export ERROR_FOR_MISSING=1
%endif
%pytest


%files -n python3-zstarfile -f %{pyproject_files}
%doc README.md
%license LICENSES/*

%pyproject_extras_subpkg -n python3-zstarfile all lz4 zstandard

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.3.0-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.3.0-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 13 2025 Maxwell G <maxwell@gtmx.me> - 0.3.0-1
- Update to 0.3.0.

* Tue Jun 10 2025 Maxwell G <maxwell@gtmx.me> - 0.2.0-6
- Fix build with Python 3.14

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.2.0-5
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 14 2024 Maxwell G <maxwell@gtmx.me> - 0.2.0-2
- Rebuild for Python 3.13

* Sun Apr 07 2024 Maxwell G <maxwell@gtmx.me> - 0.2.0-1
- Initial package (rhbz#2274272).
