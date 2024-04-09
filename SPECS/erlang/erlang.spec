%define  debug_package %{nil}
Summary:        erlang
Name:           erlang
Version:        26.2.3
Release:        2%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages
URL:            https://erlang.org
Source0:        https://github.com/erlang/otp/archive/OTP-%{version}/otp-OTP-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         OTP-24-Code.patch
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  unixODBC-devel
BuildRequires:  unzip

%if 0%{?with_check}
BuildRequires:  clang-tools-extra
%endif

%description
Erlang is a programming language and runtime system for building massively scalable soft real-time systems with requirements on high availability.

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
./otp_build check --no-docs

%post

%files
%defattr(-,root,root)
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
* Mon Apr 01 2024 Sam Meluch <sammeluch@microsoft.com> - 26.2.3-2
- Add patch to fix issue when running with compiled code from OTP-24 on aarch64

* Thu Mar 21 2024 Sam Meluch <sammeluch@microsoft.com> - 26.2.3-1
- Update to version 26.2.3

* Tue Feb 14 2023 Sam Meluch <sammeluch@microsoft.com> - 25.2-1
- Update to version 25.2

* Wed Jan 19 2022 Cameron Baird <cameronbaird@microsoft.com> - 24.2-1
- Update to version 24.2

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 22.0.7-2
- Added %%license line automatically

* Thu Mar 19 2020 Henry Beberman <henry.beberman@microsoft.com> 22.0.7-1
- Update to 22.0.7. Fix URL. Fix Source0 URL. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 19.3-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Jan 31 2019 Siju Maliakkal <smaliakkal@vmware.com> 19.3-3
- Revert to old version to fix rabbitmq-server startup failure

* Fri Dec 07 2018 Ashwin H <ashwinh@vmware.com> 21.1.4-1
- Update to version 21.1.4

* Mon Sep 24 2018 Dweep Advani <dadvani@vmware.com> 21.0-1
- Update to version 21.0

* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 19.3-2
- Remove BuildArch

* Thu Apr 06 2017 Chang Lee <changlee@vmware.com> 19.3-1
- Updated Version

* Mon Dec 12 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 19.1-1
- Initial.
