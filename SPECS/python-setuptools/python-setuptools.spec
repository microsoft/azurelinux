%global debug_package %{nil}
%define python3_majmin 3.12
%global _description %{expand:
Setuptools is a fully-featured, actively-maintained, and stable library designed to facilitate packaging Python projects.}

Summary:        Easily build and distribute Python packages
Name:           python-setuptools
Version:        69.0.3
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Tools
URL:            https://pypi.python.org/pypi/setuptools
Source0:        https://pypi.org/packages/source/s/setuptools/setuptools-%{version}.tar.gz
Patch0:         CVE-2024-6345.patch

%description    %{_description}

%package -n python3-setuptools
Summary:        %{summary}

# Early builds of Azure Linux 3.0 included python3-setuptools with the python3.spec. Obsolete to prevent build conflicts.
Obsoletes:      python3-setuptools <= 3.9.14
BuildArch:      noarch

# Note: these build requirements are only for the non-toolchain build environment (since they are already available in the toolchain environment)
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel

Provides:       python3dist(setuptools) = %{version}-%{release}
Provides:       python%{python3_majmin}dist(setuptools) = %{version}-%{release}

%description -n python3-setuptools %{_description}

%prep
%autosetup -n setuptools-%{version}

%build
pip3 wheel -w dist --no-cache-dir --no-build-isolation --no-deps $PWD

%install
pip3 install --no-cache-dir --no-index --ignore-installed --root %{buildroot} \
    --no-user --find-links=dist setuptools

# add path file pointing to distutils
cat > %{python3_sitelib}/distutils-precedence.pth <<- "EOF"
import os; var = 'SETUPTOOLS_USE_DISTUTILS'; enabled = os.environ.get(var, 'local') == 'local'; enabled and __import__('_distutils_hack').add_shim();
EOF

%files -n python3-setuptools
%defattr(-,root,root,755)
%{python3_sitelib}/distutils-precedence.pth
%{python3_sitelib}/pkg_resources/*
%{python3_sitelib}/setuptools/*
%{python3_sitelib}/_distutils_hack/
%{python3_sitelib}/setuptools-%{version}.dist-info/*

%changelog
* Tue Jul 23 2024 <lakarri@microsoft.com> - 69.0.3-3
- Fix CVE-2024-6345 with a patch

* Mon Mar 11 2024 Andrew Phelps <anphel@microsoft.com> - 69.0.3-2
- Change Requires from python3-devel to python3
- Add BuildRequires to fix regular package build
* Tue Feb 13 2024 Andrew Phelps <anphel@microsoft.com> - 69.0.3-1
- License verified
- Original version for CBL-Mariner
