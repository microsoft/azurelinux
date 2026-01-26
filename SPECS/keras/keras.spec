%define _enable_debug_package 0
%global debug_package %{nil}
Summary:        Keras is a high-level neural networks API.
Name:           keras
Version:        3.3.3
Release:        7%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://keras.io/
Source0:        https://github.com/keras-team/keras/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
#Removes circular dependency between keras and tensorflow. Plus Enables Wheel installation.
Patch00:        0001-Add-Keras-3.3.3.patch
Patch01:        CVE-2025-1550.patch
Patch02:        CVE-2025-8747.patch
Patch03:        CVE-2025-9905.patch
Patch04:        CVE-2025-12060.patch
Patch05:        CVE-2026-0897.patch
Patch06:        CVE-2025-12058.patch


# Fix for CVE-2025-9906 included as part of CVE-2025-8747 and kept here as nopatch
# and commented out, because from patch command perspective, these files
# have garbage content.

# Patch4:         CVE-2025-9906.nopatch

BuildRequires:  git
BuildRequires:  libstdc++-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-numpy
BuildRequires:  python3-packaging
BuildRequires:  python3-pip
BuildRequires:  python3-requests
BuildRequires:  python3-wheel
BuildRequires:  python3-pytorch
BuildRequires:  python3-absl-py
BuildRequires:  python3-optree
BuildRequires:  tar
BuildRequires:  which
ExclusiveArch:  x86_64

%description
Keras is a deep learning API written in Python, running on top of the machine learning platform TensorFlow.

%package -n     python3-keras
Summary:        python-keras
Requires:       python3-absl-py
Requires:       python3-rich
Requires:       python3-namex
Requires:       python3-h5py
Requires:       python3-optree
Requires:       python3-ml-dtypes


%description -n python3-keras
Python 3 version.

%prep
%autosetup -p1

# Version check
# change this and also change the 0001-Add-Keras-3.3.3.patch's version to match the version in the spec file
if [ "%{version}" != "3.3.3" ]; then
    echo "Error: Invalid version. Expected version 3.3.3."
    exit 1
fi

%build
%{py3_build}

%install
# this extra script modifies api that enables tensorflow to communicate with keras
python3 pip_build.py --install
%{pyproject_install}


%files -n python3-keras
%license LICENSE
%{python3_sitelib}/*


%changelog
* Mon Jan 26 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 3.3.3-7
- Patch for CVE-2025-12058

* Fri Jan 16 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 3.3.3-6
- Patch for CVE-2026-0897

* Fri Oct 31 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 3.3.3-5
- Patch for CVE-2025-12060

* Sat Sep 20 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 3.3.3-4
- Patch for CVE-2025-9905
- Add nopatch for CVE-2025-9906 (vulnerability addressed by patch of CVE-2025-8747)

* Mon Aug 11 2025 Kevin Lockwood <v-klockwood@microsoft.com> - 3.3.3-3
- Patch for CVE-2025-8747

* Wed Mar 12 2025 Bhagyashri Pathak <bhapathak@microsoft.com> - 3.3.3-2
- Patch for CVE-2025-1550

* Mon Jun 24 2024 Riken Maharjan <rmaharjan@microsoft.com> - 3.3.3-1
- Update keras to 3.3.3 to fix GC issue.

* Fri Mar 29 2024 Riken Maharjan <rmaharjan@microsoft.com> - 3.1.1-1
- update keras to 3.1.1

* Fri Feb 16 2024 Andrew Phelps <anphel@microsoft.com> - 2.11.0-3
- Relax requirement for python3-tf-nightly BR

* Tue Aug 01 2023 Riken Maharjan <rmaharjan@microsoft.com> - 2.11.0-2
- Remove bazel version.

* Mon Dec 12 2022 Riken Maharjan <rmaharjan@microsoft> - 2.11.0-1
- License verified
- Original version for CBL-Mariner
