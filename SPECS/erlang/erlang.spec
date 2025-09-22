%define  debug_package %{nil}
Summary:        erlang
Name:           erlang
Version:        25.3.2.21
Release:        3%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://erlang.org
Source0:        https://github.com/erlang/otp/archive/OTP-%{version}/otp-OTP-%{version}.tar.gz
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  unixODBC-devel
BuildRequires:  unzip

Patch0:         CVE-2025-4748.patch
Patch1:         CVE-2025-48038.patch
Patch2:         CVE-2025-48040.patch
Patch3:         CVE-2025-48041.patch

%description
erlang programming language

%prep
%autosetup -p1 -n otp-OTP-%{version}

%build
export ERL_TOP=`pwd`
%configure
make

%install

%make_install

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
* Sat Sep 13 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 25.3.2.21-3
- Patch for CVE-2025-48041, CVE-2025-48040, CVE-2025-48038

* Thu Jun 19 2025 Kevin Lockwood <v-klockwood@microsoft.com> - 25.3.2.21-2
- Patch CVE-2025-4748

* Wed May 14 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 25.3.2.21-1
- Auto-upgrade to 25.3.2.21 - for CVE-2025-46712

* Thu Apr 17 2025 Kshitiz Godara <kgodara@microsoft.com> - 25.3.2.20-1
- Upgrade minor version to fix CVE-2025-32433

* Thu Apr 03 2025 Sandeep Karambelkar <skarambelkar@microsoft.com> - 25.2-4
- Include patch to fix CVE-2025-30211

* Fri Feb 28 2025 Kanishk Bansal <kanbansal@microsoft.com> - 25.2-3
- Include patch to fix CVE-2025-26618

* Wed Jan 17 2024 Harshit Gupta <guptaharshit@microsoft.com> - 25.2-2
- Include patch to fix CVE-2023-48795

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
