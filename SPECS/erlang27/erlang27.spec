%define  debug_package %{nil}
%global upstream_name erlang
Summary:        Erlang/OTP 27
Name:           erlang27
Version:        27.3.4.18
Release:        1%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages
URL:            https://erlang.org
Source0:        https://github.com/erlang/otp/archive/OTP-%{version}/otp-OTP-%{version}.tar.gz#/%{upstream_name}-%{version}.tar.gz
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  unixODBC-devel
BuildRequires:  unzip

%if 0%{?with_check}
BuildRequires:  clang-tools-extra
%endif

# Shares %%{_bindir} and %%{_libdir}/erlang with the OTP 26 'erlang' package.
Conflicts:      %{upstream_name}

%description
Erlang is a programming language and runtime system for building massively scalable soft real-time systems with requirements on high availability.
This package provides the Erlang/OTP 27 release series.

%prep
%autosetup -n otp-OTP-%{version} -p1

%build
export ERL_TOP=`pwd`
%configure
%make_build

%install
%make_install

%check
export ERL_TOP=`pwd`
./otp_build check --no-docs --no-format-check

%files
%license LICENSE.txt
%{_bindir}/ct_run
%{_bindir}/dialyzer
%{_bindir}/epmd
%{_bindir}/erl
%{_bindir}/erlc
%{_bindir}/escript
%{_bindir}/run_erl
%{_bindir}/to_erl
%{_bindir}/typer
%{_libdir}/erlang/*

%changelog
* Thu Sep 24 2026 Sumit Jena <v-sumitjena@microsoft.com> - 27.3.4.18-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.
