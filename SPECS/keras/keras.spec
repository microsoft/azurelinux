%define _enable_debug_package 0
%global debug_package %{nil}
Summary:        Keras is a high-level neural networks API, written in Python and capable of running on top of TensorFlow, CNTK, or Theano.
Name:           keras
Version:        2.11.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://keras.io/
Source0:        https://github.com/keras-team/keras/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  bazel = 5.3.0
BuildRequires:  build-essential
BuildRequires:  git
BuildRequires:  libstdc++-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-numpy
BuildRequires:  python3-packaging
BuildRequires:  python3-pip
BuildRequires:  python3-requests
BuildRequires:  python3-wheel
BuildRequires:  tar
BuildRequires:  which
BuildRequires:  python3-tensorflow = 2.11.0
ExclusiveArch:  x86_64

%description
Keras is a deep learning API written in Python, running on top of the machine learning platform TensorFlow. 

%package -n     python3-keras
Summary:        python-keras


%description -n python3-keras
Python 3 version.

%prep
%autosetup -p1


%build
# tar -xf %{SOURCE1} -C /root/

ln -s %{_bindir}/python3 %{_bindir}/python

bazel --batch build  --verbose_explanations //keras/tools/pip_package:build_pip_package
# ---------
# steps to create the cache tar. network connection is required to create the cache.
#----------------------------------
# pushd /root
# tar -czvf cacheroot.tar.gz .cache  #creating the cache using the /root/.cache directory
# popd
# mv /root/cacheroot.tar.gz /usr/

./bazel-bin/keras/tools/pip_package/build_pip_package pyproject-wheeldir/
# --------


%install
%{pyproject_install}


%files -n python3-keras
%license LICENSE
%{python3_sitelib}/*


%changelog
* Mon Dec 12 2022 Riken Maharjan <rmaharjan@microsoft> - 2.11.0-1
- License verified
- Original version for CBL-Mariner
