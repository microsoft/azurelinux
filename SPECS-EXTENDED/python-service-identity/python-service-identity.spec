Vendor:         Microsoft Corporation
Distribution:   Azure Linux

Name:           python-service-identity
Version:        24.2.0
Release:        1%{?dist}
Summary:        Service identity verification for pyOpenSSL and cryptography
License:        MIT
URL:            https://github.com/pyca/service-identity
Source0:        https://files.pythonhosted.org/packages/07/a5/dfc752b979067947261dbbf2543470c58efe735c3c1301dd870ef27830ee/service_identity-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-hatch-fancy-pypi-readme
BuildRequires:  python3-hatch-vcs
BuildRequires:  python3-hatchling
# hatchling's runtime deps are not pulled into the minimal build chroot
# automatically, so list them explicitly (matches other Azure Linux
# hatchling-based packages, e.g. python-argcomplete, python-humanize).
# hatch-vcs resolves the version via setuptools_scm (read from the sdist
# PKG-INFO), so it is required too.
BuildRequires:  python3-pathspec
BuildRequires:  python3-pluggy
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-trove-classifiers
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
# Runtime dependencies are needed in the build chroot for %%pyproject_check_import.
BuildRequires:  python3-attrs
BuildRequires:  python3-cryptography
BuildRequires:  python3-pyasn1
BuildRequires:  python3-pyasn1-modules

%global common_description %{expand:
Use this package to verify that a PyCA cryptography certificate is valid for a
certain hostname or IP address, or when using pyOpenSSL and wanting to avoid
machine-in-the-middle attacks. service-identity implements RFC 6125 fully and
provides tools for inspecting certificates for service IDs.}

%description %{common_description}

%package -n python3-service-identity
Summary:        %{summary}
Requires:       python3-attrs
Requires:       python3-cryptography
Requires:       python3-pyasn1
Requires:       python3-pyasn1-modules
%{?python_provide:%python_provide python3-service-identity}

%description -n python3-service-identity %{common_description}

%prep
%autosetup -p1 -n service_identity-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files service_identity

%check
%pyproject_check_import

%files -n python3-service-identity -f %{pyproject_files}
%license %{python3_sitelib}/service_identity-%{version}.dist-info/licenses/LICENSE
%doc README.md

%changelog
* Thu Jun 11 2026 Adit Jha <aditjha@microsoft.com> - 24.2.0-1
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.
