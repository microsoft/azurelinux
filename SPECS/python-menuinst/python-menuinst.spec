%global srcname menuinst

Distribution:   Azure Linux
Name:           python-%{srcname}
Vendor:         Microsoft Corporation
Version:        2.0.0
Release:        %autorelease
Summary:        Cross platform menu item installation

License:        BSD-3-Clause
URL:            https://github.com/conda/menuinst
Source:         %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-pydantic

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


%generate_buildrequires
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_buildrequires


%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{srcname}


%check
# Upstream does not support pydantic 2.X
# https://github.com/conda/menuinst/issues/166
%pytest || :


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.*


%changelog
%autochangelog
