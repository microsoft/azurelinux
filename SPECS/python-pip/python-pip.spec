%global srcname pip
%global _description %{expand:
A tool for installing and managing Python packages}

Summary:        A tool for installing and managing Python packages
Name:           python-pip
Version:        24.2
Release:        6%{?dist}
License:        MIT AND Python-2.0.1 AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND ISC AND LGPL-2.1-only AND MPL-2.0 AND (Apache-2.0 OR BSD-2-Clause)
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Tools
URL:            https://pip.pypa.io/
Source0:        https://github.com/pypa/pip/archive/%{version}/%{srcname}-%{version}.tar.gz
Patch0:         CVE-2024-37891.patch
Patch1:         CVE-2025-8869.patch
Patch2:         CVE-2025-50181.patch
Patch3:         CVE-2026-1703.patch

BuildArch:      noarch

%if 0%{?with_check}
BuildRequires:  git
%endif

%description    %{_description}

%package -n python3-pip
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-wheel

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
* Fri Feb 20 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 24.2-6
- Patch for CVE-2026-1703

* Tue Sep 30 2025 Jyoti Kanase <v-jykanase@microsoft.com> - 24.2-4
- Patch for CVE-2025-50181
- Added %check

* Mon Sep 29 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 24.2-4
- Patch for CVE-2025-8869

* Mon Jul 07 2025 Kavya Sree Kaitepalli <kkaitepalli@microsoft.com> - 24.2-3
- Bump release to build with asciidoc

* Fri Nov 22 2024 Kavya Sree Kaitepalli <kkaitepalli@microsoft.com> - 24.2-2
- Patch for CVE-2024-37891

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
