# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# SPDX-License-Identifier: MIT

# Build as an OpenSSL provider instead of as an engine
%bcond provider %[0%{?fedora} >= 41 || 0%{?rhel} >= 10]
# QAT_HW only acceleration for RHEL
%bcond sw %{undefined rhel}

# Define the directory where the OpenSSL engines are installed
%if %{with provider}
%global modulesdir %(pkg-config --variable=modulesdir libcrypto)
%else
%global enginesdir %(pkg-config --variable=enginesdir libcrypto)
%endif

Name:           qatengine
Version:        2.0.0
Release: 4%{?dist}
Summary:        Intel QuickAssist Technology (QAT) OpenSSL Engine

# Most of the source code is BSD, with the following exceptions:
# - qat.txt, qat_err.h & qat_err.c files are Apache License 2.0
License:        BSD-3-Clause
URL:            https://github.com/intel/QAT_Engine
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# https://bugzilla.redhat.com/show_bug.cgi?id=1909065
ExclusiveArch:  x86_64

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  openssl-devel >= 1.1.1
BuildRequires:  qatlib-devel >= 23.02.0
%if !0%{?rhel}
BuildRequires:  intel-ipp-crypto-mb-devel >= 1.0.6
BuildRequires:  intel-ipsec-mb-devel >= 2.0
%endif
BuildRequires:  openssl

%description
This package provides the Intel QuickAssist Technology OpenSSL Engine
(an OpenSSL Plug-In Engine) which provides cryptographic acceleration
for both hardware and optimized software using Intel QuickAssist Technology
enabled Intel platforms.

%prep
%autosetup -n QAT_Engine-%{version}

%build
autoreconf -ivf
%configure %{?with_sw:--enable-qat_sw} %{?with_provider:--enable-qat_provider}
%make_build

%install
%make_install

%if 0%{?rhel}
find %{buildroot} -name "*.la" -delete
%endif

%check
%if %{with provider}
export OPENSSL_MODULES=%{buildroot}%{modulesdir}
openssl list -providers -provider qatprovider
%else
export OPENSSL_ENGINES=%{buildroot}%{enginesdir}
openssl engine -v %{name}
%endif

%files
%license LICENSE*
%doc README.md docs*
%if %{with provider}
%{modulesdir}/qatprovider.so
%else
%{enginesdir}/%{name}.so
%endif

%changelog
* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 10 2025 Nagha Abirami <naghax.abirami@intel.com> - 2.0.0-1
- Update to qatengine v2.0.0

* Mon Mar 10 2025 Nagha Abirami <naghax.abirami@intel.com> - 1.9.0-1
- Update to qatengine v1.9.0

* Thu Jan 23 2025 Yogaraj Alamenda <yogaraj.alamenda@intel.com> - 1.8.1-1
- Update to qatengine v1.8.1
- Update e_qat_err files license info

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Dec 5 2024 Jaya Naga Venkata Sudhakar <bavirisettyx.jaya.naga.venkata.sudhakar@intel.com> - 1.8.0-1
- Update to qatengine v1.8.0

* Thu Nov 14 2024 Ali Erdinc Koroglu <aekoroglu@fedoraproject.org> - 1.7.0-2
- Rebuilt for intel-ipsec-mb-2.0

* Thu Oct 24 2024 Yogaraj Alamenda <yogaraj.alamenda@intel.com> - 1.7.0-1
- Update to qatengine v1.7.0
- Remove qat_contig_mem from upstream package

* Fri Sep 20 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.6.2-2
- Build as a provider for F41 and EL10

* Wed Aug 14 2024 Krithika Kumaravelu <krithikax.kumaravelu@intel.com> - 1.6.2-1
- Update to qatengine v1.6.2

* Fri Aug 09 2024 Yogaraj Alamenda <yogaraj.alamenda@intel.com> - 1.6.1-3
- Add openssl-devel-engine dependency from F41

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jun 20 2024 Venkatesh J <venkatesh.j@intel.com> - 1.6.1-1
- Update to qatengine v1.6.1

* Thu Mar 14 2024 Jaya Naga Venkata Sudhakar <bavirisettyx.jaya.naga.venkata.sudhakar@intel.com> - 1.6.0-1
- Update to qatengine v1.6.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 25 2023 Jaya Naga Venkata Sudhakar <bavirisettyx.jaya.naga.venkata.sudhakar@intel.com> - 1.5.0-1
- Update to qatengine v1.5.0

* Wed Nov 22 2023 Vladis Dronov <vdronov@redhat.com> - 1.4.0-2
- Rebuild due to qatlib so-version bump

* Wed Sep 13 2023 Yogaraj Alamenda <yogarajx.alamenda@intel.com> - 1.4.0-1
- Update to qatengine v1.4.0

* Tue Sep 12 2023 Yogaraj Alamenda <yogarajx.alamenda@intel.com> - 1.3.1-1
- Update to qatengine v1.3.1

* Fri Sep 08 2023 Giovanni Cabiddu <giovanni.cabiddu@intel.com> - 1.3.0-2
- Rebuild due to qatlib so-version bump

* Wed Aug 09 2023 Yogaraj Alamenda <yogarajx.alamenda@intel.com> - 1.3.0-1
- Update to qatengine v1.3.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Yogaraj Alamenda <yogarajx.alamenda@intel.com> - 1.2.0-1
- Update to qatengine v1.2.0

* Thu May 04 2023 Yogaraj Alamenda <yogarajx.alamenda@intel.com> - 1.1.0-1
- Update to qatengine v1.1.0

* Thu Apr 13 2023 Ali Erdinc Koroglu <aekoroglu@linux.intel.com> - 1.0.0-2
- Enable QAT_HW & QAT SW Co-ex Acceleration for non RHEL distros

* Wed Mar 22 2023 Yogaraj Alamenda <yogarajx.alamenda@intel.com> - 1.0.0-1
- Update to qatengine v1.0.0

* Thu Feb 09 2023 Yogaraj Alamenda <yogarajx.alamenda@intel.com> - 0.6.19-1
- Update to qatengine v0.6.19

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 08 2022 Yogaraj Alamenda <yogarajx.alamenda@intel.com> - 0.6.18-1
- Update to qatengine v0.6.18

* Wed Nov 02 2022 Yogaraj Alamenda <yogarajx.alamenda@intel.com> - 0.6.17-1
- Update to qatengine v0.6.17

* Mon Oct 03 2022 Yogaraj Alamenda <yogarajx.alamenda@intel.com> - 0.6.16-1
- Update to qatengine v0.6.16

* Wed Aug 24 2022 Yogaraj Alamenda <yogarajx.alamenda@intel.com> - 0.6.15-1
- Update to qatengine v0.6.15

* Sat Jul 30 2022 Vladis Dronov <vdronov@redhat.com> - 0.6.14-2
- Rebuild due to qatlib so-version bump

* Wed Jul 20 2022 Yogaraj Alamenda <yogarajx.alamenda@intel.com> - 0.6.14-1
- Update to qatengine v0.6.14

* Wed Jun 22 2022 Yogaraj Alamenda <yogarajx.alamenda@intel.com> - 0.6.13-1
- Update to qatengine v0.6.13

* Fri Apr 01 2022 Yogaraj Alamenda <yogarajx.alamenda@intel.com> - 0.6.12-1
- Update to qatengine v0.6.12

* Thu Jan 27 2022 Yogaraj Alamenda <yogarajx.alamenda@intel.com> - 0.6.11-1
- Update to qatengine v0.6.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Oct 28 2021 Yogaraj Alamenda <yogarajx.alamenda@intel.com> - 0.6.10-1
- Update to qatengine v0.6.10

* Mon Oct 18 2021 Yogaraj Alamenda <yogarajx.alamenda@intel.com> - 0.6.9-1
- Update to qatengine v0.6.9

* Fri Sep 10 2021 Yogaraj Alamenda <yogarajx.alamenda@intel.com> - 0.6.8-1
- Update to qatengine v0.6.8

* Thu Sep 09 2021 Yogaraj Alamenda <yogarajx.alamenda@intel.com> - 0.6.7-2
- Rebuilt for qatlib v21.08

* Fri Jul 30 2021 Yogaraj Alamenda <yogarajx.alamenda@intel.com> - 0.6.7-1
- Update to qatengine v0.6.7

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 20 2021 Yogaraj Alamenda <yogarajx.alamenda@intel.com> - 0.6.6-1
- Update to qatengine v0.6.6

* Thu Mar 18 2021 Yogaraj Alamenda <yogarajx.alamenda@intel.com> - 0.6.5-1
- Update to qatengine v0.6.5
- Update doc with additional docs

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 11 2020 Yogaraj Alamenda <yogarajx.alamenda@intel.com> 0.6.4-1
- Update to qatengine v0.6.4

* Mon Nov 30 2020 Yogaraj Alamenda <yogarajx.alamenda@intel.com> 0.6.3-1
- Update to qatengine v0.6.3
- Update License and library installation

* Wed Nov 18 2020 Dinesh Balakrishnan <dineshx.balakrishnan@intel.com> 0.6.2-1
- Update to qatengine v0.6.2
- Address review comments

* Tue Sep 08 2020 Dinesh Balakrishnan <dineshx.balakrishnan@intel.com> 0.6.1-1
- Initial version of rpm package
