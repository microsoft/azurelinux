%define  debug_package %{nil}
Summary:        elixir
Name:           elixir
Version:        1.15.4
Release:        1%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://elixir-lang.org
Source0:        https://github.com/elixir-lang/elixir/archive/v%{version}/elixir-%{version}.tar.gz
BuildRequires:  erlang
BuildRequires:  glibc-lang

%description
elixir programming language

%prep
%autosetup

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
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.15.4-1
- Auto-upgrade to 1.15.4 - Azure Linux 3.0 - package upgrades

* Mon Feb 27 2023 Sam Meluch <sammeluch@microsoft.com> - 1.14.3-1
- Original version for CBL-Mariner
- License verified
