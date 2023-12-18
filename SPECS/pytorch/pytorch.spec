%global _empty_manifest_terminate_build 0
Summary:        Tensors and Dynamic neural networks in Python with strong GPU acceleration.
Name:           pytorch
Version:        2.0.0
Release:        3%{?dist}
License:        BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pytorch.org/
Source0:        https://github.com/pytorch/pytorch/releases/download/v%{version}/%{name}-v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Use the generate_source_tarball.sh script to create a tarball of submodules during version updates.
Source1:        %{name}-%{version}-submodules.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  python3-PyYAML
BuildRequires:  python3-devel
BuildRequires:  python3-filelock
BuildRequires:  python3-hypothesis
BuildRequires:  python3-jinja2
BuildRequires:  python3-numpy
BuildRequires:  python3-setuptools
BuildRequires:  python3-typing-extensions

%description
PyTorch is a Python package that provides two high-level features:
- Tensor computation (like NumPy) with strong GPU acceleration
- Deep neural networks built on a tape-based autograd system
You can reuse your favorite Python packages such as NumPy, SciPy and Cython to extend PyTorch when needed.

%package -n     python3-pytorch
Summary:        Tensors and Dynamic neural networks in Python with strong GPU acceleration.
Requires:       python3-filelock
Requires:       python3-numpy
Requires:       python3-typing-extensions
Requires:       python3-sympy
Requires:       python3-jinja2
Requires:       python3-opt-einsum
Requires:       python3-networkx

%description -n python3-pytorch
PyTorch is a Python package that provides two high-level features:
- Tensor computation (like NumPy) with strong GPU acceleration
- Deep neural networks built on a tape-based autograd system
You can reuse your favorite Python packages such as NumPy, SciPy and Cython to extend PyTorch when needed.

%package -n python3-pytorch-doc
Summary:        Development documents and examples for torch

%description -n python3-pytorch-doc
PyTorch is a Python package that provides two high-level features:
- Tensor computation (like NumPy) with strong GPU acceleration
- Deep neural networks built on a tape-based autograd system
You can reuse your favorite Python packages such as NumPy, SciPy and Cython to extend PyTorch when needed.

%prep
%autosetup -a 1 -n %{name}-v%{version}

%build
export MAX_JOBS=1
export USE_CUDA=0
export BUILD_CAFFE2=0
%py3_build

%install
%py3_install
install -d -m755 %{buildroot}/%{_pkgdocdir}

cp -arf docs %{buildroot}/%{_pkgdocdir}

%files -n python3-pytorch
%license LICENSE
%{_bindir}/convert-caffe2-to-onnx
%{_bindir}/convert-onnx-to-caffe2
%{_bindir}/torchrun
%{python3_sitearch}/*

%files -n python3-pytorch-doc
%license LICENSE
%{_docdir}/*

%changelog
* Thu Apr 06 2023 Riken Maharjan <rmaharjan@microsoft.com> - 2.0.0-2
- Add missing runtine for 2.0.0

* Mon Apr 03 2023 Riken Maharjan <rmaharjan@microsoft.com> - 2.0.0-1
- upgrade to 2.0.0

* Thu Feb 02 2023 Mandeep Plaha <mandeepplaha@microsoft.com> - 1.13.1-1
- Initial CBL-Mariner import from OpenEuler (license: BSD)
- License verified
- Upgrade version to 1.13.1

* Mon Jun 13 2022 Zhipeng Xie <xiezhipeng1@huawei.com> - 1.11.0-1
- upgrade to 1.11.0

* Mon Jun 28 2021 wulei <wulei80@huawei.com> - 1.6.0-3
- fixes: error: the CXX compiler identification is unknown

* Thu Feb 4 2021 Zhipeng Xie<xiezhipeng1@huawei.com> - 1.6.0-2
- disable SVE to fix compile error in gcc 9

* Sun Sep 27 2020 Zhipeng Xie<xiezhipeng1@huawei.com> - 1.6.0-1
- Package init
