%global srcname menuinst

Distribution:   Azure Linux
Name:           python-%{srcname}
Vendor:         Microsoft Corporation
Version:        2.2.0
Release:        7%{?dist}
Summary:        Cross platform menu item installation

License:        BSD-3-Clause
URL:            https://github.com/conda/menuinst
Source:         %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
BuildRequires:  python3-wheel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
#BuildRequires:  python3-pydantic

%global _description %{expand:
This package provides cross platform menu item installation for conda packages.

If a conda package ships a menuinst JSON document under $PREFIX/Menu, conda
will invoke menuinst to process the JSON file and install the menu items in
your operating system. The menu items are removed when the package is
uninstalled.

The following formats are supported:

   Windows: .lnk files in the Start menu. Optionally, also in the Desktop and
            Quick Launch.
   macOS: .app bundles in the Applications folder.
   Linux: .desktop files as defined in the XDG standard.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %_description


%prep
%autosetup -p1 -n %{srcname}-%{version}
# apipkg is only needed on Windows
rm -r menuinst/_vendor
# remove Windows only components not needed and with some different licenses
rm -r menuinst/_legacy/win32.py menuinst/platforms/win*
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
# Ensure pretend_version is set to true in pyproject.toml



%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_wheel


%install
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_install
%pyproject_save_files %{srcname}


%check
# Upstream does not support pydantic 2.X
# https://github.com/conda/menuinst/issues/166
%pytest || :


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.*


%changelog
* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 29 2024 Python Maint <python-maint@redhat.com> - 2.0.0-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 05 2023 Orion Poplawski <orion@nwra.com> - 2.0.0-1
- Initial import
