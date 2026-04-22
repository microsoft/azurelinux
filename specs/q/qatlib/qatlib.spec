# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# SPDX-License-Identifier: MIT

%global libqat_soversion  4
%global libusdm_soversion 0
Name:             qatlib
Version:          25.08.0
Release: 5%{?dist}
Summary:          Intel QuickAssist user space library
# The entire source code is released under BSD.
# For a breakdown of inbound licenses see the INSTALL file.
License:          BSD-3-Clause AND ( BSD-3-Clause OR GPL-2.0-only )
URL:              https://github.com/intel/%{name}
Source0:          https://github.com/intel/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:    systemd gcc make autoconf autoconf-archive automake libtool systemd-devel openssl-devel zlib-devel nasm numactl-devel
Recommends:       qatlib-service
# https://bugzilla.redhat.com/show_bug.cgi?id=1897661
ExcludeArch:      %{arm} aarch64 %{power64} s390x i686 riscv64

%description
Intel QuickAssist Technology (Intel QAT) provides hardware acceleration
for offloading security, authentication and compression services from the
CPU, thus significantly increasing the performance and efficiency of
standard platform solutions.

Its services include symmetric encryption and authentication,
asymmetric encryption, digital signatures, RSA, DH and ECC, and
lossless data compression.

This package provides user space libraries that allow access to
Intel QuickAssist devices and expose the Intel QuickAssist APIs.

%package       devel
Summary:       Headers and libraries to build applications that use qatlib
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description   devel
This package contains headers and libraries required to build applications
that use the Intel QuickAssist APIs.

%package       tests
Summary:       Sample applications that use qatlib
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description   tests
This package contains sample applications that use the Intel QuickAssists APIs.

%package       service
Summary:       A daemon for qatlib resources management
Requires:      pciutils
Requires:      %{name}%{?_isa} = %{version}-%{release}
%{?systemd_requires}

%description   service
This package contains a daemon that manages QAT resources for the Intel
QuickAssist Technology user space library (qatlib).

%prep
%autosetup -p1

# Create a sysusers.d config file
cat >qatlib.sysusers.conf <<EOF
g qat -
EOF

%build
autoreconf -vif
%configure --enable-legacy-algorithms
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
%make_build

%install
%make_install
make DESTDIR=%{buildroot} samples-install
rm %{buildroot}/%{_libdir}/libqat.la
rm %{buildroot}/%{_libdir}/libusdm.la
rm %{buildroot}/%{_libdir}/libqat.a
rm %{buildroot}/%{_libdir}/libusdm.a

install -m0644 -D qatlib.sysusers.conf %{buildroot}%{_sysusersdir}/qatlib.conf

%post          service
%systemd_post qat.service

%preun         service
%systemd_preun qat.service

%postun        service
%systemd_postun_with_restart qat.service

%files
%doc INSTALL README.md
%license LICENSE*
%{_libdir}/libqat.so.%{libqat_soversion}*
%{_libdir}/libusdm.so.%{libusdm_soversion}*
%{_sysusersdir}/qatlib.conf

%files         devel
%{_libdir}/libqat.so
%{_libdir}/libusdm.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/qat

%files         tests
%doc quickassist/lookaside/access_layer/src/sample_code/README.txt
%attr(0754,-,qat) %{_bindir}/cpa_sample_code
%attr(0754,-,qat) %{_bindir}/dc_dp_sample
%attr(0754,-,qat) %{_bindir}/dc_stateless_sample
%attr(0754,-,qat) %{_bindir}/chaining_sample
%attr(0754,-,qat) %{_bindir}/dc_stateless_multi_op_sample
%attr(0754,-,qat) %{_bindir}/algchaining_sample
%attr(0754,-,qat) %{_bindir}/ccm_sample
%attr(0754,-,qat) %{_bindir}/cipher_sample
%attr(0754,-,qat) %{_bindir}/gcm_sample
%attr(0754,-,qat) %{_bindir}/hash_file_sample
%attr(0754,-,qat) %{_bindir}/hash_sample
%attr(0754,-,qat) %{_bindir}/ipsec_sample
%attr(0754,-,qat) %{_bindir}/ssl_sample
%attr(0754,-,qat) %{_bindir}/sym_dp_sample
%attr(0754,-,qat) %{_bindir}/dh_sample
%attr(0754,-,qat) %{_bindir}/eddsa_sample
%attr(0754,-,qat) %{_bindir}/prime_sample
%attr(0754,-,qat) %{_bindir}/hkdf_sample
%attr(0754,-,qat) %{_bindir}/ec_montedwds_sample
%attr(0754,-,qat) %{_bindir}/zuc_sample
%attr(0754,-,qat) %{_bindir}/update_sample
%{_datadir}/qat/calgary
%{_datadir}/qat/calgary32
%{_datadir}/qat/canterbury
%{_mandir}/man7/cpa_sample_code.7*

%files         service
%{_sbindir}/qatmgr
%{_sbindir}/qat_init.sh
%{_unitdir}/qat.service
%{_mandir}/man8/qatmgr.8*
%{_mandir}/man8/qat_init.sh.8*

%changelog
* Thu Jan 22 2026 Vladislav Dronov <vdronov@redhat.com> - 25.08.0-4
- Update to qatlib 25.08.0 @ 686d209b

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 25.08.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 25.08.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 17 2025 Giovanni Cabiddu <giovanni.cabiddu@intel.com> - 25.08.0-1
- Update to qatlib 25.08.0
- Add autoconf-archive as a dependency
- Remove fix-systemd-path.patch as fix is present on the upstream project
- Add update_sample to qatlib-tests
- Add manpage for cpa_sample_code

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 24.09.0-7
- Add sysusers.d config file to allow rpm to create users/groups automatically

* Thu Jan 23 2025 Giovanni Cabiddu <giovanni.cabiddu@intel.com> - 24.09.0-6
- Add patch to remove hardcoded installation path to fix the build on F42

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 24.09.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 01 2024 Vladis Dronov <vdronov@redhat.com> - 24.09.0-4
- Update to qatlib 24.09.0 @ 36fb0903

* Mon Sep 16 2024 Giovanni Cabiddu <giovanni.cabiddu@intel.com> - 24.09.0-3
- Move pciutils as a dependency of the qat-service subpackage

* Mon Sep 16 2024 Giovanni Cabiddu <giovanni.cabiddu@intel.com> - 24.09.0-2
- Add pciutils as a dependency as required by qatlib

* Tue Sep 10 2024 Giovanni Cabiddu <giovanni.cabiddu@intel.com> - 24.09.0-1
- Update to qatlib 24.09.0
- Add numactl-devel as a dependency since it is required by qatlib 24.09.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 24.02.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 20 2024 Giovanni Cabiddu <giovanni.cabiddu@intel.com> - 24.02.0-1
- Update to qatlib 24.02.0
- Add zuc_sample to qatlib-tests package

* Thu Feb 08 2024 Vladis Dronov <vdronov@redhat.com> - 23.11.0-4
- Use proper SPDX license identifiers

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Nov 17 2023 Giovanni Cabiddu <giovanni.cabiddu@intel.com> - 23.11.0-1
- Update to qatlib 23.11.0

* Thu Sep 07 2023 Giovanni Cabiddu <giovanni.cabiddu@intel.com> - 23.08.0-1
- Add chaining_sample to qatlib-tests package
- Update to qatlib 23.08.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 23.02.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Feb 24 2023 Giovanni Cabiddu <giovanni.cabiddu@intel.com> - 23.02.0-1
- Update to qatlib 23.02.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 22.07.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 15 2022 Giovanni Cabiddu <giovanni.cabiddu@intel.com> - 22.07.2-1
- Update to qatlib 22.07.2

* Thu Oct 20 2022 Giovanni Cabiddu <giovanni.cabiddu@intel.com> - 22.07.1-1
- Update to qatlib 22.07.1

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 22.07.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 22 2022 Giovanni Cabiddu <giovanni.cabiddu@intel.com> - 22.07.0-1
- Update to qatlib 22.07
- Removed patches as fixes are present in qatlib 22.07
- Moved qat.service to separate rpm

* Tue Mar 22 2022 Vladis Dronov <vdronov@redhat.com> - 21.11.0-3
- Fix small issues in qatlib-tests package
- Update documentation from the upstream

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 21.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Nov 10 2021 Giovanni Cabiddu <giovanni.cabiddu@intel.com> - 21.11.0-1
- Update to qatlib 21.11
- Add qatlib-tests package

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 21.08.0-2
- Rebuilt with OpenSSL 3.0.0

* Wed Sep 08 2021 Giovanni Cabiddu <giovanni.cabiddu@intel.com> - 21.08.0-1
- Update to qatlib 21.08

* Mon Aug 16 2021 Vladis Dronov <vdronov@redhat.com> - 21.05.0-3
- Add documentation files to the package

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 21.05.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue May 18 2021 Giovanni Cabiddu <giovanni.cabiddu@intel.com> - 21.05.0-1
- Update to qatlib 21.05

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 20.10.0-4
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec  14 2020 Giovanni Cabiddu <giovanni.cabiddu@intel.com> - 20.10.0-2
- Add ExcludeArch i686

* Mon Nov  16 2020 Giovanni Cabiddu <giovanni.cabiddu@intel.com> - 20.10.0-1
- Update to qatlib 20.10
- Fixes to spec to address comments from Fedora review

* Mon Aug  10 2020 Mateusz Polrola <mateuszx.potrola@intel.com> - 20.08.0-1
- Initial version of the package
