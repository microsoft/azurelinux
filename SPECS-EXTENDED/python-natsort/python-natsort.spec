Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname natsort

Name:           python-%{srcname}
Version:        8.4.0
Release:        1%{?dist}
Summary:        Simple yet flexible natural sorting in Python

License:        MIT
URL:            https://github.com/SethMMorton/natsort
Source0:        https://files.pythonhosted.org/packages/e2/a9/a0c57aee75f77794adaf35322f8b6404cbd0f89ad45c87197a937764b7d0/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros

%global _description %{expand:
natsort provides a simple yet flexible way to sort strings "naturally", i.e.
ordering embedded numbers by value rather than lexicographically (so that, for
example, "file2" sorts before "file10"). It handles real numbers, signs,
locale-aware ordering, and version-style strings, and ships a command-line
utility for sorting input naturally.}

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
%pyproject_save_files %{srcname}

%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.rst
%{_bindir}/natsort

%changelog
* Wed Jun 03 2026 Andy Zaugg <azaugg@linkedin.com> - 8.4.0-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.
