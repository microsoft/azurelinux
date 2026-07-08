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
Source0:        %{url}/releases/download/v%{version}/%{srcname}-%{version}.tar.gz

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
# Twisted imports typing_extensions but python3-twisted does not pull it into
# the minimal %%check chroot; required for the offline unit tests that import
# the package's Twisted-based modules.
BuildRequires:  python3-typing-extensions

Requires:       python3-%{pkgname} = %{version}-%{release}

%global _description %{expand:
Tools and APIs to make working with AMQP in Fedora easier.}

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
# python3-automat is a runtime dependency of Twisted's reactor, which
# fedora-messaging (and the koji-fedoramessaging plugin) loads when publishing.
# Azure Linux's python-twisted does not pull it in, so require it here to keep
# the plugin functional without modifying the shared python-twisted package.
Requires:       python3-automat
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{_description}

%prep
%autosetup -n %{srcname}-%{version} -p0

# Azure Linux 3 ships python3-jsonschema 2.6.0, but upstream pins jsonschema
# >=3.2.0; that lower bound in the wheel metadata makes pkg_resources raise a
# VersionConflict when the plugin loads, silently dropping every Koji event.
# 2.6.0 is sufficient here, so relax the bound before the wheel is built
# (anchored to ^jsonschema so types-jsonschema is left untouched).
sed -i -E 's/^jsonschema = .*/jsonschema = ">=2.6.0,<5.0.0"/' pyproject.toml

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{srcname}
# Azure Linux ships only the generic example config. The Fedora-specific
# broker connection profiles (fedora.toml, fedora.stg.toml) and their
# bundled certificate/key files are intentionally omitted: they point at
# Fedora's public broker and are irrelevant to the Azure Linux Koji message
# bus, which is configured for its own in-cluster broker via site config.
install -D -p -m 0644 config.toml.example %{buildroot}%{_sysconfdir}/fedora-messaging/config.toml
install -D -p -m 0644 fm-consumer@.service %{buildroot}%{_unitdir}/fm-consumer@.service

%check
%pyproject_check_import -e '*.api' -e '*.cli'
# Only run the offline unit tests that do not import the Twisted reactor.
# tests/unit/test_cli.py, test_example.py and test_testing.py pull in
# fedora_messaging.api/cli, which import the Twisted reactor and therefore
# require Automat -- a Twisted runtime dependency that is not available as an
# RPM in the Azure Linux build environment (upstream Twisted pip-installs it
# in its own test venv). The retained tests cover configuration parsing,
# message schema/validation, and schema utilities.
%pytest -vv \
    tests/unit/test_config.py \
    tests/unit/test_message.py \
    tests/unit/test_schema_utils.py

%files
%license LICENSES/GPL-2.0-or-later.txt
%doc README.rst
%dir %{_sysconfdir}/fedora-messaging/
%config(noreplace) %{_sysconfdir}/fedora-messaging/config.toml
%{_bindir}/fedora-messaging
%{_unitdir}/fm-consumer@.service

%files -n python3-%{pkgname} -f %{pyproject_files}
%license %{python3_sitelib}/%{srcname}-%{version}.dist-info/LICENSES/GPL-2.0-or-later.txt

%changelog
* Thu Jun 11 2026 Adit Jha <aditjha@microsoft.com> - 3.9.0-1
- Initial Azure Linux import from Fedora 43 (license: MIT).
- License verified.
- Omit Fedora-specific broker profiles (fedora.toml, fedora.stg.toml) and bundled cert/key files; ship only the generic example config.
- Require python3-automat so the Twisted reactor (used by the messaging plugin) works at runtime.
- Relax the jsonschema lower bound to >=2.6.0 so the package loads against Azure Linux 3's python3-jsonschema 2.6.0.
