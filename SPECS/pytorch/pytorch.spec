%global _empty_manifest_terminate_build 0
Summary:        Tensors and Dynamic neural networks in Python with strong GPU acceleration.
Name:           pytorch
Version:        2.2.2
Release:        12%{?dist}
License:        BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://pytorch.org/
Source0:        https://github.com/pytorch/pytorch/releases/download/v%{version}/%{name}-v%{version}.tar.gz#/%{name}-%{version}.tar.gz
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
BuildRequires:  python3-six

Patch1:         CVE-2024-27318.patch
Patch2:         CVE-2022-1941.patch
Patch3:         CVE-2024-5187.patch
Patch4:         CVE-2024-27319.patch
Patch5:         CVE-2021-22918.patch
Patch6:         CVE-2024-7776.patch
Patch7:         CVE-2021-22569.patch
Patch8:         CVE-2025-32434.patch
Patch9:         CVE-2025-3730.patch
Patch10:        CVE-2025-2953.patch
Patch11:        CVE-2025-55552.patch
Patch12:        CVE-2025-55560.patch
Patch13:        CVE-2025-46152.patch
Patch14:        CVE-2025-3001.patch
Patch15:        CVE-2026-24747.patch
Patch16:        CVE-2026-0994.patch

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
%autosetup -p 1 -n %{name}-v%{version}

%build
export USE_CUDA=0
export BUILD_CAFFE2=0
%ifarch aarch64
export MAX_JOBS=4
%endif
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
* Wed Feb 11 2026 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 2.2.2-12
- Patch for CVE-2026-0994

* Wed Jan 28 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 2.2.2-11
- Patch for CVE-2026-24747

* Thu Dec 25 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 2.2.2-10
- Patch for CVE-2025-3001

* Thu Dec 04 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 2.2.2-9
- Patch for CVE-2025-55560 & CVE-2025-46152
 
* Mon Nov 24 2025 Archana Shettigar <v-shettigara@microsoft.com> - 2.2.2-8
- Patch CVE-2025-55552

* Tue Apr 29 2025 Archana Shettigar <v-shettigara@microsoft.com> - 2.2.2-7
- Patch CVE-2025-2953

* Wed Apr 23 2025 Kanishk Bansal <kanbansal@microsoft.com> - 2.2.2-6
- Patch CVE-2025-32434, CVE-2025-3730

* Mon Mar 31 2025 Kanishk Bansal <kanbansal@microsoft.com> - 2.2.2-5
- Patch CVE-2021-22569, CVE-2024-7776

* Mon Jan 20 2025 Archana Choudhary <archana1@microsoft.com> - 2.2.2-4
- patch for CVE-2024-27319, CVE-2021-22918

* Tue Nov 12 2024 Sean Dougherty <sdougherty@microsoft.com> - 2.2.2-3
- Add patch to address CVE-2024-5187
- Remove unnecessary double vendoring of the third_party directory. Doubling happens because the contents of the submodule tarball are pulled directly from the original source tarball and then re-uploaded as this "submodule tarball".

* Tue Sep 17 2024 Archana Choudhary <archana1@microsoft.com> - 2.2.2-2
- patch for CVE-2024-27318, CVE-2022-1941

* Tue Apr 02 2024 Riken Maharjan <rmaharjan@microsoft.com> - 2.2.2-1
- Upgrade to pytorch 2.2.2

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
