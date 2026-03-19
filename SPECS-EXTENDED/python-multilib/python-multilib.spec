Vendor:         Microsoft Corporation
Distribution:   Azure Linux

Name:           python-multilib
Version:        1.3
Release:        1%{?dist}
Summary:        A module for determining if a package is multilib or not
License:        GPL-2.0-only
URL:            https://pagure.io/releng/python-multilib
Source0:        https://releases.pagure.org/releng/python-multilib/%{name}-%{version}.tar.bz2

BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3-wheel

%global _description %{expand:
A Python module that supports several multilib methods useful for determining
if a 32-bit package should be included with its 64-bit analogue in a compose.}

%description %{_description}

%package conf
Summary:        Configuration files for %{name}

%description conf
This package provides the configuration files for %{name}.


%package -n python3-multilib
Summary:        %{summary}
%{?python_provide:%python_provide python3-multilib}
Requires:       python3
Requires:       python3-six
Requires:       %{name}-conf = %{version}-%{release}

%description -n python3-multilib %{_description}


%prep
%autosetup -n %{name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files multilib
install -D -m 0644 etc/multilib.conf %{buildroot}%{_sysconfdir}/multilib.conf

%check
%pyproject_check_import

%files conf
%config(noreplace) %{_sysconfdir}/multilib.conf


%files -n python3-multilib -f %{pyproject_files}
%license LICENSE
%doc README.md


%changelog
* Wed Mar 18 2026 GitHub Copilot <copilot@github.com> - 1.3-1
- Initial Azure Linux import from Fedora rawhide.
- License verified.