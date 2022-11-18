Summary:        TensorFlow is an open source machine learning framework for everyone.
Name:           tensorflow
Version:        2.8.3
Release:        1%{?dist}
License:        #####
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://www.tensorflow.org/
Source0:        https://github.com/tensorflow/tensorflow/archive/refs/tags/v%{Version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-cache-full.tar.gz
BuildRequires:  build-essential
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-requests
BuildRequires:  python3-packaging
BuildRequires:  python3-wheel
BuildRequires:  python3-numpy
BuildRequires:  bazel = 4.2.1
BuildRequires:  binutils
BuildRequires:  which
BuildRequires:  tar
BuildRequires:  git
BuildRequires:  python3-pip
BuildRequires:  libstdc++-devel

%description
TensorFlow is an open source machine learning framework for everyone.

%package -n     python3-tensorflow
Summary:        python-tensorflow
Requires:       python3

%description -n python3-tensorflow
Python 3 version.

%prep
%autosetup -p1


%build
#unload the cache
tar -xf %{SOURCE1} -C /root/

# numpy distutil
# rm -rf /usr/lib/python3.9/site-packages/numpy/core/include/numpy
# tar -xvf %{SOURCE2} -C /usr/lib/python3.9/site-packages/numpy/core/include/

ln -s /usr/bin/python3 /usr/bin/python
# bazel clean 
# pushd /root
# tar -czvf cacheroot.tar.gz .cache
# popd
# mv /root/cacheroot.tar.gz /usr/
# sleep 180

bazel build //tensorflow/tools/pip_package:build_pip_package


# sleep 43200
# ---------
./bazel-bin/tensorflow/tools/pip_package/build_pip_package pyproject-wheeldir/
# --------


%install
%pyproject_install


 
%check
pip3 install nose pytest
mkdir -pv test
cd test
#PYTHONPATH=%{buildroot}%{python3_sitelib} PATH=$PATH:%{buildroot}%{_bindir} %python3 -c "import numpy; numpy.test()"

%files -n python3-tensorflow
%license LICENSE
%{python3_sitelib}/*
%{_bindir}/estimator_ckpt_converter
%{_bindir}/import_pb_to_tensorboard
%{_bindir}/saved_model_cli
%{_bindir}/tensorboard
%{_bindir}/tf_upgrade_v2
%{_bindir}/tflite_convert
%{_bindir}/toco
%{_bindir}/toco_from_protos


%changelog
* Thu Sep 22 2022 Riken Maharjan <rmaharjan@microsoft> - 2.8.3-1
- License verified
- Original version for CBL-Mariner
