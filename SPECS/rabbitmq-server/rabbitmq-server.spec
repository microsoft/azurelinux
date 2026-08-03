%define  debug_package %{nil}
Summary:        rabbitmq-server
Name:           rabbitmq-server
Version:        3.13.7
Release:        9%{?dist}
License:        Apache-2.0 and MPL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages
URL:            https://rabbitmq.com
Source0:        https://github.com/rabbitmq/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.xz
Patch0:			CVE-2025-30219.patch
Patch1:			CVE-2025-50200.patch
Patch2:			CVE-2026-8466.patch
Patch3:			CVE-2026-43968.patch
Patch4:			CVE-2026-7790.patch
Patch5:			CVE-2026-43973.patch
Patch6:			CVE-2026-57211.patch
Patch7:			CVE-2026-57212.patch
Patch8:			CVE-2026-57213.patch
Patch9:			CVE-2026-57214.patch
Patch10:		CVE-2026-57215.patch
Patch11:		CVE-2026-57217.patch
Patch12:		CVE-2026-57218.patch
Patch13:		CVE-2026-57219.patch
Patch14:		CVE-2026-57220.patch
Patch15:		CVE-2026-57221.patch
Patch16:		CVE-2026-57216.patch
Patch17:		CVE-2026-43966.patch
Patch18:		CVE-2026-44839.patch
Patch19:		CVE-2026-59248.patch
Patch20:		CVE-2026-65624.patch

BuildRequires:  elixir
BuildRequires:  erlang
BuildRequires:  glibc-lang
BuildRequires:  libxslt
BuildRequires:  python
BuildRequires:  python%{python3_pkgversion}-simplejson
BuildRequires:  rsync
BuildRequires:  unzip
BuildRequires:  xmlto
BuildRequires:  zip

Requires:       elixir
Requires:       erlang
Requires:       glibc-lang
Requires:       libxslt
Requires:       python
Requires:       python%{python3_pkgversion}-simplejson
Requires:       rsync
Requires:       unzip
Requires:       xmlto
Requires:       zip

%description
RabbitMQ is a reliable and mature messaging and streaming broker, which is easy to deploy on cloud environments, on-premises, and on your local machine.

%prep
%autosetup -p1

%build
export LANG="en_US.UTF-8"
# Running with -j1 to solve a race condition during build with a patch added to erlang to resolve
# an arm64 build error related to heap allocation
%make_build -j1

%install
export LANG="en_US.UTF-8"
# Install rabbitmq-server
%make_install PREFIX=%{_prefix} RMQ_ROOTDIR=%{_prefix}/lib/rabbitmq

install -p -D -m 0755 ./scripts/rabbitmq-script-wrapper %{_sbindir}/rabbitmqctl
install -p -D -m 0755 ./scripts/rabbitmq-script-wrapper %{_sbindir}/rabbitmq-server
install -p -D -m 0755 ./scripts/rabbitmq-script-wrapper %{_sbindir}/rabbitmq-plugins
install -p -D -m 0755 ./scripts/rabbitmq-script-wrapper %{_sbindir}/rabbitmq-diagnostics

# Make necessary symlinks
mkdir -p %{_prefix}/lib/rabbitmq/bin
for app in rabbitmq-defaults rabbitmq-env rabbitmq-plugins rabbitmq-diagnostics rabbitmq-server rabbitmqctl ; do
	ln -s %{_prefix}/lib/rabbitmq/lib/rabbitmq_server-%{version}/sbin/${app} %{_prefix}/lib/rabbitmq/bin/${app}
done

%files
%license LICENSE LICENSE-*
%{_libdir}/rabbitmq/lib/rabbitmq_server-%{version}/*

%changelog
* Fri Jul 31 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 3.13.7-9
- Patch for CVE-2026-65624, CVE-2026-59248

* Thu Jul 23 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 3.13.7-8
- Patch for CVE-2026-43966, CVE-2026-44839

* Wed Jul 15 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 3.13.7-7
- Patch for CVE-2026-57221, CVE-2026-57220, CVE-2026-57219, CVE-2026-57218, CVE-2026-57217, CVE-2026-57215, CVE-2026-57214, CVE-2026-57213, CVE-2026-57212, CVE-2026-57211, CVE-2026-57216

* Wed Jun 17 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 3.13.7-6
- Patch for CVE-2026-43973

* Sat May 30 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 3.13.7-5
- Patch for CVE-2026-7790, CVE-2026-43968

* Wed May 27 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 3.13.7-4
- Patch for CVE-2026-8466

* Wed Oct 29 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 3.13.7-3
- Patch for CVE-2025-50200

* Mon Mar 31 2025 Ankita Pareek <ankitapareek@microsoft.com> - 3.13.7-2
- Address CVE-2025-30219 with a patch

* Tue Sep 17 2024 Archana Choudhary <archana1@microsoft.com> - 3.13.7-1
- Upgrade rabbitmq-server to version 3.13.7
- deps/jose is updated to 1.11.10
- Fixes CVE-2023-50966

* Thu Mar 28 2024 Sam Meluch <sammeluch@microsoft.com> - 3.13.0-1
- Upgrade rabbitmq-server to version 3.13.0 for Azure Linux 3.0
- Remove now unused vendor tarballs

* Tue Mar 14 2023 Sam Meluch <sammeluch@microsoft.com> - 3.11.11-1
- Original version for CBL-Mariner
- License Verified
