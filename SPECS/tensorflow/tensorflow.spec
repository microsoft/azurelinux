Summary:        TensorFlow is an open source machine learning framework for everyone.
Name:           tensorflow
Version:        2.16.1
Release:        7%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://www.tensorflow.org/
Source0:        https://github.com/tensorflow/tensorflow/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-cache2.tar.gz
Patch0:         CVE-2024-7592.patch
Patch1:         CVE-2024-6232.patch
Patch2:         CVE-2024-8088.patch
Patch3:         CVE-2024-3651.patch
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
BuildRequires:  patchelf
BuildRequires:  tar
BuildRequires:  which
ExclusiveArch:  x86_64

%description
TensorFlow is an open source machine learning framework for everyone.

%package -n     python3-tensorflow
Summary:        python-tensorflow
Requires:       python3-absl-py
Requires:       python3-astunparse
Requires:       python3-devel
Requires:       python3-flatbuffers
Requires:       python3-gast
Requires:       python3-google-pasta
Requires:       python3-grpcio
Requires:       python3-h5py
Requires:       python3-keras
Requires:       python3-libclang
Requires:       python3-ml-dtypes
Requires:       python3-opt-einsum
Requires:       python3-numpy
Requires:       python3-protobuf
Requires:       python3-requests
Requires:       python3-setuptools
Requires:       python3-six
Requires:       python3-termcolor
Requires:       python3-tensorboard
Requires:       python3-typing-extensions
Requires:       python3-wrapt

%description -n python3-tensorflow
Python 3 version.

%prep
# use -N to **not** apply patches, will apply patch after getting SOURCE1 in build stage
%autosetup -N

%build
MD5_HASH=$(echo -n $PWD | md5sum | awk '{print $1}')
mkdir -p /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external
tar -xvf %{SOURCE1} -C /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external

#remove go_sdk and its marker file

rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi__click
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi__colorama
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi__importlib_metadata
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi__installer
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi__more_itertools
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi__packaging
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi__pep517
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi__pip
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi__pip_tools
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi__pyproject_hooks
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi__tomli
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi__zipp
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_absl_py
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_astunparse
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_certifi
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_charset_normalizer
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_dill
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_dm_tree
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_gast
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_grpcio
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_h5py
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_idna
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_keras
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_markdown
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_markdown_it_py
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_markupsafe
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_mdurl
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_namex
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_numpy
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_opt_einsum
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_packaging
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_portpicker
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_protobuf
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_psutil
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_pygments
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_requests
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_rich
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_setuptools
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_six
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_tblib
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_tensorboard
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_tensorboard_data_server
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_termcolor
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_tf_keras
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_typing_extensions
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_urllib3
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_werkzeug
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_wheel
rm -rf /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/pypi_wrapt


# Need to patch CVE-2024-7592 in the bundled python for applicable archs: `ExclusiveArch:  x86_64`
pushd /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/python_x86_64-unknown-linux-gnu/lib/python3.12/http
patch -p1 < %{PATCH0}
popd

# Need to patch CVE-2024-6232 in the bundled python for applicable archs: `ExclusiveArch:  x86_64`
pushd /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/python_x86_64-unknown-linux-gnu/lib/python3.12/
patch -p1 < %{PATCH1}
popd

# Need to patch CVE-2024-8088 in the bundled python for applicable archs: `ExclusiveArch:  x86_64`
pushd /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/python_x86_64-unknown-linux-gnu/lib/python3.12/
patch -p1 < %{PATCH2}
popd  

# Need to patch CVE-2024-3651 in the bundled python for applicable archs: `ExclusiveArch:  x86_64`
pushd /root/.cache/bazel/_bazel_$USER/$MD5_HASH/external/python_x86_64-unknown-linux-gnu/lib/python3.12/site-packages/pip/_vendor/idna
patch -p1 < %{PATCH3}
popd

export TF_PYTHON_VERSION=3.12
ln -s %{_bindir}/python3 %{_bindir}/python

# Remove the .bazelversion file so that latest bazel version available will be used to build TensorFlow.
rm .bazelversion

bazel --batch build  //tensorflow/tools/pip_package:build_pip_package


./bazel-bin/tensorflow/tools/pip_package/build_pip_package pyproject-wheeldir/
# --------


%install
%{pyproject_install}


%files -n python3-tensorflow
%license LICENSE
%{python3_sitelib}/*
%{_bindir}/import_pb_to_tensorboard
%{_bindir}/saved_model_cli
%{_bindir}/tensorboard
%{_bindir}/tf_upgrade_v2
%{_bindir}/tflite_convert
%{_bindir}/toco
%{_bindir}/toco_from_protos

%changelog
* Wed Sep 25 2024 Archana Choudhary <archana1@microsoft.com> - 2.16.1-7
- Bump release to build with new python3 to fix CVE-2024-6232, CVE-2024-8088, CVE-2024-3651

* Fri Aug 23 2024 Brian Fjeldstad <bfjelds@microsoft.com> - 2.16.1-6
- Bump release to build with new python3 to fix CVE-2024-7592

* Thu May 30 2024 Neha Agarwal <nehaagarwal@microsoft.com> - 2.16.1-5
- Bump release to build with new python-werkzeug to fix CVE-2024-34069

* Wed May 29 2024 Neha Agarwal <nehaagarwal@microsoft.com> - 2.16.1-4
- Bump release to build with new llvm to fix CVE-2024-31852

* Mon Apr 29 2024 Riken Maharjan <rmaharjan@microsoft> - 2.16.1-3
- Add tensorboard as runtime requirement

* Wed Mar 27 2024 Riken Maharjan <rmaharjan@microsoft> - 2.16.1-2
- Remove Unnecessary requirements and add keras as runtime req

* Tue Mar 05 2024 Riken Maharjan <rmaharjan@microsoft> - 2.16.1-1
- Update to 2.16.1

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
