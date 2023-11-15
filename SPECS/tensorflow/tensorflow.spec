Summary:        TensorFlow is an open source machine learning framework for everyone.
Name:           tensorflow
Version:        2.11.1
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://www.tensorflow.org/
Source0:        https://github.com/tensorflow/tensorflow/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-cache.tar.gz
BuildRequires:  bazel
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

%package -n     python3-tensorflow
Summary:        python-tensorflow
Requires:       python3-markupsafe
Requires:       python3-absl-py
Requires:       python3-astunparse
Requires:       python3-cachetools
Requires:       python3-charset-normalizer
Requires:       python3-devel
Requires:       python3-flatbuffers
Requires:       python3-gast
Requires:       python3-google-auth
Requires:       python3-google-pasta
Requires:       python3-google-auth-oauthlib
Requires:       python3-grpcio
Requires:       python3-h5py
Requires:       python3-idna
Requires:       python3-importlib-metadata
Requires:       python3-libclang
Requires:       python3-markdown
Requires:       python3-numpy
Requires:       python3-oauthlib
Requires:       python3-opt-einsum
Requires:       python3-protobuf
Requires:       python3-pyasn1
Requires:       python3-pyasn1-modules
Requires:       python3-requests-oauthlib
Requires:       python3-rsa
Requires:       python3-six
Requires:       python3-termcolor
Requires:       python3-typing-extensions
Requires:       python3-werkzeug
Requires:       python3-wrapt
Requires:       python3-zipp

%description -n python3-tensorflow
Python 3 version.

%package -n python3-tf-nightly
Summary:        python-tensorflow
Requires:       python3-markupsafe
Requires:       python3-absl-py
Requires:       python3-astunparse
Requires:       python3-cachetools
Requires:       python3-charset-normalizer
Requires:       python3-devel
Requires:       python3-flatbuffers
Requires:       python3-gast
Requires:       python3-google-auth
Requires:       python3-google-pasta
Requires:       python3-google-auth-oauthlib
Requires:       python3-grpcio
Requires:       python3-h5py
Requires:       python3-idna
Requires:       python3-importlib-metadata
Requires:       python3-libclang
Requires:       python3-markdown
Requires:       python3-numpy
Requires:       python3-oauthlib
Requires:       python3-opt-einsum
Requires:       python3-protobuf
Requires:       python3-pyasn1
Requires:       python3-pyasn1-modules
Requires:       python3-requests-oauthlib
Requires:       python3-rsa
Requires:       python3-six
Requires:       python3-termcolor
Requires:       python3-typing-extensions
Requires:       python3-werkzeug
Requires:       python3-wrapt
Requires:       python3-zipp

%description -n python3-tf-nightly
Python 3 version.

%prep
%autosetup -p1


%build
tar -xf %{SOURCE1} -C /root/

ln -s %{_bindir}/python3 %{_bindir}/python
# Remove the .bazelversion file so that latest bazel version available will be used to build TensorFlow.
rm .bazelversion
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
%{_bindir}/tensorboard
%{_bindir}/tf_upgrade_v2
%{_bindir}/tflite_convert
%{_bindir}/toco
%{_bindir}/toco_from_protos

%files -n python3-tf-nightly
%license LICENSE
%{python3_sitelib}/*


%changelog
* Wed Oct 11 2023 Mitch Zhu <mitchzhu@microsoft> - 2.11.1-1
- Update to 2.11.1 to fix CVEs

* Tue Aug 01 2023 Riken Maharjan <rmaharjan@microsoft.com> - 2.11.0-4
- Remove .bazelversion file.

* Thu Jan 03 2022 Riken Maharjan <rmaharjan@microsoft> - 2.11.0-3
- Add tf-nightly subpackage. 

* Thu Dec 08 2022 Riken Maharjan <rmaharjan@microsoft> - 2.11.0-2
- Correct markupsafe package name. 

* Sun Dec 04 2022 Riken Maharjan <rmaharjan@microsoft> - 2.11.0-1
- Update to 2.11.0

* Thu Sep 22 2022 Riken Maharjan <rmaharjan@microsoft> - 2.8.3-1
- License verified
- Original version for CBL-Mariner
