Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname tcping

Name:           python-%{srcname}
Version:        0.1.1rc1
Release:        1%{?dist}
Summary:        Ping a host over TCP, reporting connection latency

License:        MIT
URL:            https://github.com/kontspace/tcping
Source0:        https://files.pythonhosted.org/packages/2a/a1/7e8ac7d81a1a89b1cdb8200fee2c0779410a63743806213cb9289ab6ee94/%{srcname}-%{version}.tar.gz
# The PyPI sdist does not bundle a license file; ship the upstream MIT LICENSE
# taken verbatim from the kontspace/tcping repository.
Source1:        LICENSE

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros

%global _description %{expand:
tcping measures the round-trip time to establish a TCP connection to a given
host and port, providing a ping-like utility for services that do not respond
to ICMP. It can be used from the command line and reports per-attempt latency
and summary statistics.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{srcname}-%{version}
cp -p %{SOURCE1} LICENSE

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{srcname}

%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%{_bindir}/tcping
%{_bindir}/tcping.py

%changelog
* Wed Jun 03 2026 Andy Zaugg <azaugg@linkedin.com> - 0.1.1rc1-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.
