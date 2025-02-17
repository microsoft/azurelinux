Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# Copyright (c) 2016-2020, Intel Corporation
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Intel Corporation nor the names of its contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

%global libpqos_ver 6.0.0
%global desc %{expand: \
This package provides basic support for Intel Resource Director Technology
including, Cache Monitoring Technology (CMT), Memory Bandwidth Monitoring
(MBM), Cache Allocation Technology (CAT), Code and Data Prioritization 
(CDP) and Memory Bandwidth Allocation (MBA).}

Name:		intel-cmt-cat
Version:	24.05
Release:	1%{?dist}
Summary:	Intel cache monitoring and allocation technology config tool

License:	BSD-3-Clause
URL: 		https://github.com/intel/intel-cmt-cat
Source: 	%{url}/archive/v%{version}/%{name}-%{version}.tar.gz

Patch0:		0001-alter-install-paths.patch
Patch1:		0002-remove-build-and-install-of-examples.patch
Patch2:		0003-allow-debian-flags-to-be-added.patch

ExclusiveArch:	x86_64

BuildRequires:	gcc
BuildRequires:	make

%description
%{desc}

%package devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel %{desc}

Development files.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%make_build

%install
%make_install

%ldconfig_scriptlets

%files
%license LICENSE
%doc ChangeLog README.md
%{_bindir}/membw
%{_sbindir}/pqos
%{_sbindir}/pqos-msr
%{_sbindir}/pqos-os
%{_sbindir}/rdtset
%{_lib64dir}/libpqos.so.6
%{_lib64dir}/libpqos.so.%{libpqos_ver}
%{_mandir}/man8/membw.8*
%{_mandir}/man8/pqos.8*
%{_mandir}/man8/pqos-msr.8*
%{_mandir}/man8/pqos-os.8*
%{_mandir}/man8/rdtset.8*

%files -n %{name}-devel
%{_includedir}/pqos.h
%{_lib64dir}/libpqos.so

%changelog
* Mon Nov 11 2024 Sumit Jena <v-sumitjena@microsoft.com> - 24.05-1
- Update to version 24.05
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.1.0-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Fri Dec 18 2020 Khawar Abbasi <khawar.abbasi@intel.com> - 4.1.0-1
- New release 4.1.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Khawar Abbasi <khawar.abbasi@intel.com> - 4.0.0-1
- New release 4.0.0

* Mon Feb 17 2020 Marcel Cornu <marcel.d.cornu@intel.com> - 3.1.1-3
- Patched compilation issue on Fedora 32 (RhBug: 1799525)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 30 2019 Marcel cornu <marcel.d.cornu@intel.com> - 3.1.1-1
- New release 3.1.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 27 2019 Marcel cornu <marcel.d.cornu@intel.com> - 3.0.1-1
- New release 3.0.1

* Mon Feb 18 2019 Marcel cornu <marcel.d.cornu@intel.com> - 3.0.0-1
- New release 3.0.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 16 2018 Marcel cornu <marcel.d.cornu@intel.com>, Michal Aleksinski <michalx.aleksinski@intel.com> 2.1.0-1
- New release 2.1.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Marcel cornu <marcel.d.cornu@intel.com>, Michal Aleksinski <michalx.aleksinski@intel.com> - 2.0.0-1
- New release 2.0.0

* Thu Mar 08 2018 Marcel cornu <marcel.d.cornu@intel.com>, Michal Aleksinski <michalx.aleksinski@intel.com> - 1.2.0-3
- Updated spec file with BuildRequires tag

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 29 2017 Marcel Cornu <marcel.d.cornu@intel.com>, Wojciech Andralojc <wojciechx.andralojc@intel.com> 1.2.0-1
- New release 1.2.0

* Thu Aug 3 2017 Aaron Hetherington <aaron.hetherington@intel.com>, Marcel Cornu <marcel.d.cornu@intel.com> 1.1.0-1
- New release 1.1.0

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 21 2017 Aaron Hetherington <aaron.hetherington@intel.com>, Marcel Cornu <marcel.d.cornu@intel.com> 1.0.1-1
- Spec file bug fixes

* Wed Jun 07 2017 Aaron Hetherington <aaron.hetherington@intel.com>, Marcel Cornu <marcel.d.cornu@intel.com> 1.0.1-1
- new release
- bug fixes

* Fri May 19 2017 Aaron Hetherington <aaron.hetherington@intel.com>, Michal Aleksinski <michalx.aleksinski@intel.com> 1.0.0-1
- new release

* Tue Feb 14 2017 Aaron Hetherington <aaron.hetherington@intel.com> 0.1.5-1
- new release

* Mon Oct 17 2016 Aaron Hetherington <aaron.hetherington@intel.com> 0.1.5
- new release

* Tue Apr 19 2016 Tomasz Kantecki <tomasz.kantecki@intel.com> 0.1.4-3
- global typo fix
- small edits in the description

* Mon Apr 18 2016 Tomasz Kantecki <tomasz.kantecki@intel.com> 0.1.4-2
- LICENSE file added to the package

* Thu Apr 7 2016 Tomasz Kantecki <tomasz.kantecki@intel.com> 0.1.4-1
- initial version of the package
