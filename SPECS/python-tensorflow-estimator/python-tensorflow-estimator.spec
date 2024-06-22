%global pypi_name tensorflow-estimator
%global _description %{expand:
A high-level TensorFlow API that greatly simplifies machine learning programming}
%define _enable_debug_package 0
%global debug_package %{nil}

Summary:        A high-level TensorFlow API that greatly simplifies machine learning programming
Name:           python-%{pypi_name}
Version:        2.11.0
Release:        2%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/tensorflow/estimator
Source0:        https://github.com/tensorflow/estimator/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-cache.tar.gz
BuildRequires:  bazel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  python3-six
BuildRequires:  python3-tf-nightly
BuildRequires:  python3-keras
BuildRequires:  python3-h5py
ExclusiveArch:  x86_64


%description %{_description}

%package -n python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name} %{_description}

%prep
%autosetup -p1 -n estimator-%{version}

%build
tar -xf %{SOURCE1} -C /root/
ln -s /usr/bin/python3 /usr/bin/python
bazel --batch build //tensorflow_estimator/tools/pip_package:build_pip_package

# ---------
# steps to create the cache tar. network connection is required to create the cache.
#----------------------------------
# bazel clean
# pushd /root
# tar -czvf %{name}-%{version}-cache.tar.gz .cache  #creating the cache using the /root/.cache directory
# popd
# mv /root/%{name}-%{version}-cache.tar.gz /usr/
# sleep 240

./bazel-bin/tensorflow_estimator/tools/pip_package/build_pip_package pyproject-wheeldir/

%install
%{pyproject_install}


%files -n python3-%{pypi_name} 
%doc README.md
%license LICENSE
%{python3_sitelib}/*

%changelog
* Fri May 24 2024 Riken Maharjan <rmaharjan@microsoft.com> - 2.11.0-2
- Explicitly BR python3-h5py.

* Fri Nov 11 2022 Riken Maharjan <rmaharjan@microsoft.com> - 2.11.0-1
- Original version for CBL-Mariner. License Verified.

