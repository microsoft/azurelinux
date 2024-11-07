%global srcname pip
%global _description %{expand:
A tool for installing and managing Python packages}

Summary:        A tool for installing and managing Python packages
Name:           python-pip
Version:        24.2
Release:        2%{?dist}
License:        MIT AND Python-2.0.1 AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND ISC AND LGPL-2.1-only AND MPL-2.0 AND (Apache-2.0 OR BSD-2-Clause)
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Tools
URL:            https://pip.pypa.io/
Source0:        https://github.com/pypa/pip/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

%description    %{_description}

%package -n python3-pip
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel

Requires:  python3-setuptools

%description -n python3-pip %{_description}

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
# Bootstrap `pip3` which casues ptest build failure.
# The manual installation of pip in the RPM buildroot requires pip
# to be already present in the chroot.
# For toolchain builds, `pip3` requirement is statisfied by raw-toolchain's
# version of python, so it does not do anything.
# For builds other than toolchain, we would require pip to be present.
# The line below install pip in the build chroot using the recently
# compiled python3.
# NOTE: This is a NO-OP for the toolchain build.
%{__python3} %{_libdir}/python%{python3_version}/ensurepip

%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{srcname}

%files -n python3-pip
%defattr(-,root,root,755)
%{_bindir}/pip*
%{python3_sitelib}/pip*

%changelog
* Thu Nov 07 2024 Suresh Thelkar <sthelkar@microsoft.com> - 24.2.2
- Patch CVE-2024-6345 by adding BuildRequires for setuptools
- This way it does not depdend bundled setuptools of python3 

* Wed Oct 23 2024 Bala <balakumaran.kannan@microsoft.com> - 24.2.1
- Upgrade to 24.2 for fixing CVE-2024-6345
- Update build and install steps for toml based build
- Remove CVE-2024-3651.patch as the fix is included in latest version

* Wed Aug 28 2024 Rachel Menge <rachelmenge@microsoft.com> - 24.0-2
- Patch CVE-2024-3651.patch
- Add python3-wheel BR to python3-pip subpackage

* Tue Feb 13 2024 Andrew Phelps <anphel@microsoft.com> - 24.0-1
- License verified
- Original version for Azure Linux.
