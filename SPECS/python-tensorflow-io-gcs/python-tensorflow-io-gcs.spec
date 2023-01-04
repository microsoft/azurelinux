%global pypi_name tensorflow-io-gcs
%global _description %{expand:
TensorFlow I/O is a collection of file systems and file formats that are not available in TensorFlow's built-in support}
%define _enable_debug_package 0
%global debug_package %{nil}

Summary:        TensorFlow I/O is a collection of file systems and file formats that are not available in TensorFlow's built-in support
Name:           python-%{pypi_name}
Version:        0.29.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/tensorflow/io
Source0:        https://github.com/tensorflow/io/archive/refs/tags/v%{version}.tar.gz#/%{pypi_name}-%{version}.tar.gz
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  python3-six


%description %{_description}

%package -n python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name} %{_description}

%prep
%autosetup -p1 -n io-%{version}

%build
ln -s /usr/bin/python3 /usr/bin/python
python3 setup.py -q bdist_wheel --project tensorflow_io_gcs_filesystem 
mkdir -p pyproject-wheeldir/ && cp ./dist/*.whl pyproject-wheeldir/

%install
%{pyproject_install}


%files -n python3-%{pypi_name} 
%doc README.md
%license LICENSE
%{python3_sitelib}/*

%changelog
* Mon Dec 19 2022 Riken Maharjan <rmaharjan@microsoft.com> - 0.29.0-1
- Original version for CBL-Mariner. License Verified.

