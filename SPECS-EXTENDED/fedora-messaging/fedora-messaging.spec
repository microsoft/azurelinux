# Don't add -s to Python shebang. fedora-messaging must be able to load
# plugins from /usr/local; see https://bugzilla.redhat.com/show_bug.cgi?id=2272526
%undefine _py3_shebang_s

%global pkgname fedora-messaging
%global srcname fedora_messaging

Name:           %{pkgname}
Version:        3.9.0
Release:        1%{?dist}
Summary:        Set of tools for using Fedora's messaging infrastructure
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
License:        GPL-2.0-or-later
URL:            https://github.com/fedora-infra/fedora-messaging
Source0:        https://files.pythonhosted.org/packages/source/f/%{pkgname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-poetry-core
BuildRequires:  systemd-rpm-macros

# Runtime dependencies needed for the offline-safe unit test subset in %%check.
BuildRequires:  python3-blinker
BuildRequires:  python3-click
BuildRequires:  python3-crochet
BuildRequires:  python3-jsonschema
BuildRequires:  python3-pika
BuildRequires:  python3-pyOpenSSL
BuildRequires:  python3-pytest
BuildRequires:  python3-requests
BuildRequires:  python3-service-identity
BuildRequires:  python3-tomli
BuildRequires:  python3-twisted

Requires:       python3-%{pkgname} = %{version}-%{release}

%global _description Tools and APIs to make working with AMQP in Fedora easier.

%description %{_description}

%package -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-blinker
Requires:       python3-click
Requires:       python3-crochet
Requires:       python3-jsonschema
Requires:       python3-pika
Requires:       python3-pyOpenSSL
Requires:       python3-requests
Requires:       python3-service-identity
Requires:       python3-tomli
Requires:       python3-twisted
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{_description}

%prep
%autosetup -n %{srcname}-%{version} -p0

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{srcname}
install -D -p -m 0644 config.toml.example %{buildroot}%{_sysconfdir}/fedora-messaging/config.toml
install -D -p -m 0644 configs/fedora.toml %{buildroot}%{_sysconfdir}/fedora-messaging/fedora.toml
install -D -p -m 0644 configs/fedora.stg.toml %{buildroot}%{_sysconfdir}/fedora-messaging/fedora.stg.toml
install -D -p -m 0644 configs/cacert.pem %{buildroot}%{_sysconfdir}/fedora-messaging/cacert.pem
# This is intentionally world-readable; it is for public Fedora broker access.
install -D -p -m 0644 configs/fedora-key.pem %{buildroot}%{_sysconfdir}/fedora-messaging/fedora-key.pem
install -D -p -m 0644 configs/fedora-cert.pem %{buildroot}%{_sysconfdir}/fedora-messaging/fedora-cert.pem
install -D -p -m 0644 configs/stg-cacert.pem %{buildroot}%{_sysconfdir}/fedora-messaging/stg-cacert.pem
install -D -p -m 0644 configs/fedora.stg-key.pem %{buildroot}%{_sysconfdir}/fedora-messaging/fedora.stg-key.pem
install -D -p -m 0644 configs/fedora.stg-cert.pem %{buildroot}%{_sysconfdir}/fedora-messaging/fedora.stg-cert.pem
install -D -p -m 0644 fm-consumer@.service %{buildroot}%{_unitdir}/fm-consumer@.service

%check
%pyproject_check_import
# Exclude broker/network integration tests and Twisted-reactor tests that are not
# reliable in Azure Linux's network-isolated builders; keep pure offline units.
%pytest -vv \
    tests/unit/test_cli.py \
    tests/unit/test_config.py \
    tests/unit/test_example.py \
    tests/unit/test_message.py \
    tests/unit/test_schema_utils.py \
    tests/unit/test_testing.py

%files
%license LICENSES/GPL-2.0-or-later.txt
%doc README.rst
%dir %{_sysconfdir}/fedora-messaging/
%config(noreplace) %{_sysconfdir}/fedora-messaging/config.toml
%config(noreplace) %{_sysconfdir}/fedora-messaging/fedora.toml
%config(noreplace) %{_sysconfdir}/fedora-messaging/fedora.stg.toml
%config(noreplace) %{_sysconfdir}/fedora-messaging/cacert.pem
%config(noreplace) %{_sysconfdir}/fedora-messaging/fedora-key.pem
%config(noreplace) %{_sysconfdir}/fedora-messaging/fedora-cert.pem
%config(noreplace) %{_sysconfdir}/fedora-messaging/stg-cacert.pem
%config(noreplace) %{_sysconfdir}/fedora-messaging/fedora.stg-key.pem
%config(noreplace) %{_sysconfdir}/fedora-messaging/fedora.stg-cert.pem
%{_bindir}/fedora-messaging
%{_unitdir}/fm-consumer@.service

%files -n python3-%{pkgname} -f %{pyproject_files}
%license LICENSES/GPL-2.0-or-later.txt

%changelog
* Thu Jun 11 2026 Adit Jha <aditjha@microsoft.com> - 3.9.0-1
- Initial Azure Linux import from Fedora rawhide (license: GPL-2.0-or-later). License verified.
