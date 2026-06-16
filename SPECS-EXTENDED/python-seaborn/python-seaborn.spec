Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname seaborn

Name:           python-%{srcname}
Version:        0.13.2
Release:        1%{?dist}
Summary:        Statistical data visualization

License:        BSD-3-Clause
URL:            https://github.com/mwaskom/seaborn
Source0:        https://files.pythonhosted.org/packages/86/59/a451d7420a77ab0b98f7affa3a1d78a313d2f7281a57afb1a34bae8ab412/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-flit-core

%global _description %{expand:
Seaborn is a library for making statistical graphics in Python. It builds on
matplotlib and integrates closely with pandas data structures, providing a
high-level interface for drawing attractive and informative statistical
graphics such as distribution, categorical, regression, and matrix plots.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{srcname}-%{version}

# Normalize the license metadata to the unambiguous legacy table form so it
# validates under Azure Linux's pre-PEP 639 pyproject validator.
sed -i 's/^license = {file = "LICENSE.md"}/license = {text = "BSD-3-Clause"}/' pyproject.toml
sed -i '/^license-files/d' pyproject.toml

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{srcname}

%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE.md
%doc README.md

%changelog
* Wed Jun 03 2026 Andy Zaugg <azaugg@linkedin.com> - 0.13.2-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.
