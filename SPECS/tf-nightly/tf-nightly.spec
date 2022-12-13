Summary:        TensorFlow nightly is an open source machine learning framework for everyone.
Name:           tf-nightly
Version:        2.11.0
Release:        2%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://www.tensorflow.org/
Source0:        https://github.com/tensorflow/tensorflow/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-cache.tar.gz
BuildRequires:  bazel = 5.3.0
BuildRequires:  binutils
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
ExclusiveArch:  x86_64

%description
TensorFlow is an open source machine learning framework for everyone.

%package -n     python3-tf-nightly
Summary:        python-tf-nightly
Requires:       python3-six
Requires:  python3-absl-py
Requires:  numpy
BuildRequires:  python3-wrapt
BuildRequires:  python3-typing-extensions
BuildRequires:  python3-packaging
BuildRequires:  python3-opt-einsum
BuildRequires:  python3-gast
BuildRequires:  python3-astunparse
BuildRequires:  python3-termcolor
BuildRequires:  python3-flatbuffers
BuildRequires:  python3-requests


%description -n python3-tensorflow
Python 3 version.

%prep
%autosetup -p1


%build
tar -xf %{SOURCE1} -C /root/

ln -s %{_bindir}/python3 %{_bindir}/python

bazel --batch build  --verbose_explanations //tensorflow/tools/pip_package:build_pip_package
# ---------
# steps to create the cache tar. network connection is required to create the cache.
#----------------------------------
# pushd /root
# tar -czvf cacheroot.tar.gz .cache  #creating the cache using the /root/.cache directory
# popd
# mv /root/cacheroot.tar.gz /usr/

./bazel-bin/tensorflow/tools/pip_package/build_pip_package pyproject-wheeldir/
# --------


%install
%{pyproject_install}


%files -n python3-tensorflow
%license LICENSE
%{python3_sitelib}/*
%{_bindir}/estimator_ckpt_converter
%{_bindir}/import_pb_to_tensorboard
%{_bindir}/saved_model_cli
%{_bindir}/tf_upgrade_v2
%{_bindir}/tflite_convert
%{_bindir}/toco
%{_bindir}/toco_from_protos


%changelog
* Thu Dec 08 2022 Riken Maharjan <rmaharjan@microsoft> - 2.11.0-2
- correct markupsafe package name. 

* Sun Dec 04 2022 Riken Maharjan <rmaharjan@microsoft> - 2.11.0-1
- update to 2.11.0

* Thu Sep 22 2022 Riken Maharjan <rmaharjan@microsoft> - 2.8.3-1
- License verified
- Original version for CBL-Mariner
