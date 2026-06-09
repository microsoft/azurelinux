Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname pillow
%global module  PIL

Name:           python-%{srcname}
Version:        10.4.0
Release:        1%{?dist}
Summary:        Python Imaging Library (Fork)

License:        HPND
URL:            https://python-pillow.github.io
Source0:        https://files.pythonhosted.org/packages/cd/74/ad3d526f3bf7b6d3f408b73fde271ec69dfac8b81341a318ce825f2b3812/%{srcname}-%{version}.tar.gz

# Compiled (C) package built with setuptools. In addition to the toolchain it
# needs the system image libraries below. Pinned to 10.4.0, the latest release
# that builds with Azure Linux's setuptools (newer Pillow requires setuptools
# >= 77 for its PEP 639 metadata, which is not available here).
BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  zlib-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  freetype-devel

%global _description %{expand:
Pillow is the friendly PIL fork. The Python Imaging Library adds image
processing capabilities to the Python interpreter, providing extensive file
format support, an efficient internal representation, and powerful image
processing tools. It is a dependency of matplotlib for raster image support.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{module}

%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.md

%changelog
* Wed Jun 03 2026 Andy Zaugg <azaugg@linkedin.com> - 10.4.0-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.
