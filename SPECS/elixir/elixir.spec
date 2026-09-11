%define  debug_package %{nil}
Summary:        elixir
Name:           elixir
Version:        1.16.1
Release:        3%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages
URL:            https://elixir-lang.org
Source0:        https://github.com/elixir-lang/elixir/archive/v%{version}/elixir-%{version}.tar.gz
Patch0:         CVE-2026-49762.patch
Patch1:         CVE-2026-75758.patch
BuildRequires:  erlang
BuildRequires:  glibc-lang

%description
elixir programming language

%prep
%autosetup -p1

%build
export LANG="en_US.UTF-8"
%make_build

%install
%make_install PREFIX=/usr

%files
%license LICENSE
%{_bindir}/elixir
%{_bindir}/elixirc
%{_bindir}/iex
%{_bindir}/mix
%{_libdir}/elixir/*
%{_mandir}/man1/elixir.1.gz
%{_mandir}/man1/elixirc.1.gz
%{_mandir}/man1/iex.1.gz
%{_mandir}/man1/mix.1.gz


%changelog
* Mon Aug 31 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.16.1-3
- Patch for CVE-2026-75758

* Thu Jun 11 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.16.1-2
- Patch for CVE-2026-49762

* Tue Feb 20 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.16.1-1
- Updated to 1.16.1.

* Mon Feb 27 2023 Sam Meluch <sammeluch@microsoft.com> - 1.14.3-1
- Original version for CBL-Mariner
- License verified
