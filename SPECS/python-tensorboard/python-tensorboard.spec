%global pypi_name tensorboard
%global _description %{expand:
TensorBoard is a suite of web applications for inspecting and understanding your TensorFlow runs and graphs}
%define _enable_debug_package 0
%global debug_package %{nil}

Summary:        TensorBoard is a suite of web applications for inspecting and understanding your TensorFlow runs and graphs
Name:           python-%{pypi_name}
Version:        2.11.0
Release:        4%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/tensorflow/tensorboard
Source0:        https://github.com/tensorflow/tensorboard/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-cache.tar.gz
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  python3-six
BuildRequires:  bazel
BuildRequires:  gcc
BuildRequires:  build-essential
BuildRequires:  protobuf
BuildRequires:  zlib
BuildRequires:  python3-virtualenv
ExclusiveArch:  x86_64


%description %{_description}

%package -n python3-%{pypi_name}
Summary:        %{summary}
Requires:   python3-absl-py
Requires:   python3-google-auth-oauthlib
Requires:   python3-google-auth
Requires:   python3-grpcio
Requires:   python3-markdown
Requires:   python3-numpy
Requires:   python3-protobuf
Requires:   python3-requests
Requires:   python3-setuptools
Requires:   python3-werkzeug
Requires:   python3-wheel


%description -n python3-%{pypi_name} %{_description}

%package -n python3-%{pypi_name}-data-server
Summary:        %{summary}


%description -n python3-%{pypi_name}-data-server %{_description}

%prep
%autosetup -p1 -n tensorboard-%{version}

%build
tar -xf %{SOURCE1} -C /root/

ln -s /usr/bin/python3 /usr/bin/python

#tensorboard-data-server
pushd tensorboard/data/server/pip_package
python3 setup.py -q bdist_wheel
popd
mkdir -p pyproject-wheeldir/ && cp tensorboard/data/server/pip_package/dist/*.whl pyproject-wheeldir/

#tensorboard built using bazel
bazel --batch build //tensorboard/pip_package:build_pip_package
#cache
# ---------
# steps to create the cache tar. network connection is required to create the cache.
#----------------------------------
# bazel clean
# pushd /root
# tar -czvf %{name}-%{version}-cache.tar.gz .cache  #creating the cache using the /root/.cache directory
# popd
# mv /root/%{name}-%{version}-cache.tar.gz /usr/

#tensorboard package build script build_pip_package.sh doesn't assign RUNFILES variable successfully.
sed -i 's/output="$1"/output="$1"\n \ RUNFILES="$(CDPATH="" cd -- "$0.runfiles" \&\& pwd)"/' bazel-bin/tensorboard/pip_package/build_pip_package
bazel-bin/tensorboard/pip_package/build_pip_package .
mv %{pypi_name}-%{version}-*.whl pyproject-wheeldir/

%install
%{pyproject_install}


%files -n python3-%{pypi_name}
%doc README.md
%license LICENSE
%{_bindir}/tensorboard
%{python3_sitelib}/tensorboard
%{python3_sitelib}/tensorboard-*

%files -n python3-%{pypi_name}-data-server
%doc README.md
%license LICENSE
%{python3_sitelib}/tensorboard_data_server*

%changelog
* Tue Apr 23 2024 Andrew Phelps <anphel@microsoft.com> - 2.11.0-4
- Remove BR on python3-tf-nightly

* Fri Feb 16 2024 Andrew Phelps <anphel@microsoft.com> - 2.11.0-3
- Relax version requirements

* Tue Aug 01 2023 Riken Maharjan <rmaharjan@microsoft.com> - 2.11.0-2
- Remove bazel version.

* Mon Dec 19 2022 Riken Maharjan <rmaharjan@microsoft.com> - 2.11.0-1
- Original version for CBL-Mariner. License Verified.
