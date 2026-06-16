Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname fonttools
%global module  fontTools

Name:           python-%{srcname}
Version:        4.63.0
Release:        1%{?dist}
Summary:        Tools to manipulate font files

License:        MIT
URL:            https://github.com/fonttools/fonttools
Source0:        https://files.pythonhosted.org/packages/84/69/c97f2c18e0db87d2c7b15da1974dace76ae938f1cfa22e2727a648b7ed43/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros

%global _description %{expand:
fontTools is a library for manipulating fonts, written in Python. It supports
reading and writing of TrueType/OpenType fonts, reading and writing of AFM
files, reading (and partially writing) of PS Type 1 fonts, and conversion of
fonts to and from an XML-based format (TTX). It is a core dependency of
matplotlib.}

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
%license LICENSE LICENSE.external
%doc README.rst
%{_bindir}/fonttools
%{_bindir}/ttx
%{_bindir}/pyftsubset
%{_bindir}/pyftmerge
%{_mandir}/man1/ttx.1*

%changelog
* Wed Jun 03 2026 Andy Zaugg <azaugg@linkedin.com> - 4.63.0-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.
