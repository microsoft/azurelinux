Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# Spec file for IBM's TSS for the TPM 2.0
#
%{!?__global_ldflags: %global __global_ldflags -Wl,-z,relro}

%global incname ibmtss

Name:		tss2
# this is the release of the TSS library
Version:        2.3.2
# this is the release of the fedora package, goes back to 1 when version changes
Release:        2%{?dist}
Summary:        IBM's TCG Software Stack (TSS) for TPM 2.0 and related utilities

License:        BSD-3-Clause AND LicenseRef-TCGL
URL:            https://sourceforge.net/projects/ibmtpm20tss/
Source0:        https://sourceforge.net/projects/ibmtpm20tss/files/ibmtss%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  gcc
BuildRequires:  openssl-devel
Requires:       openssl

%description
TSS2 is a user space Trusted Computing Group's Software Stack (TSS) for
TPM 2.0.  It implements the functionality equivalent to the TCG TSS
working group's ESAPI, SAPI, and TCTI layers (and perhaps more) but with
a hopefully far simpler interface.

It comes with about 120 "TPM tools" that can be used for rapid prototyping,
education and debugging. 

%package devel
Summary:        Development libraries and headers for IBM's TSS 2.0
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries and headers for IBM's TSS 2.0. You will need this in
order to build TSS 2.0 applications.

%prep
%autosetup -p1 -c %{name}-%{version}

%build
autoreconf -vi
%configure --disable-static --disable-tpm-1.2 --program-prefix=tss
CCFLAGS="%{optflags}" \
LNFLAGS="%{__global_ldflags}" \
%{make_build}

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%ldconfig_scriptlets

# files in the tss2 package
%files
%license LICENSE
# becomes /usr/bin/tss*, the command line utilities
%{_bindir}/tss*
# becomes /usr/lib64
%{_libdir}/libibmtss.so.2
%{_libdir}/libibmtss.so.2.*
%{_libdir}/libibmtssutils.so.2
%{_libdir}/libibmtssutils.so.2.*
%attr(0644, root, root) %{_mandir}/man1/tss*.1*

# files devel is the tss2-devel package
%files devel
# becomes /usr/include/ibmtss, the headers
%{_includedir}/%{incname}
# becomes /usr/lib64
%{_libdir}/libibmtss.so
%{_libdir}/libibmtssutils.so
%doc ibmtss.docx

%changelog
* Mon Jan 13 2025 Archana Shettigar <v-shettigara@microsoft.com> - 2.3.2-2
- Initial Azure Linux import from Fedora 41 (license: MIT).
- Removed epoch
- License verified

* Thu Aug 15 2024 Ken Goldman <kgoldman@us.ibm.com> - 1:2.3.2-1
- Trivial fixes for Fedora 41 Openssl 3.2.2 removal of SHA-1 signing
* Mon May 20 2024 Ken Goldman <kgoldman@us.ibm.com> - 1:2.3.1-1
- Add support for loadexternal schemes
- Fix ObjectTemplates to accept caller curveID
- Add Nuvoton configure utilities to VS projects
- ifdef out functions deprecated with openssl 3.x
- Recode the OpenSSL pkeyutl uses.  OpenSSL 3.x no longer ignores the oaep hash algorithm for the pkcs1 scheme.
- Add userWithAuth to unseal policy sample scripts.  This is best practice.
- Add policyparameters, policycapability

* Fri Oct 6 2023 Ken Goldman <kgoldman@us.ibm.com> - 1:2.1.1-2
- Update license

* Fri Sep 29 2023 Ken Goldman <kgoldman@us.ibm.com> - 1:2.1.1-1
- Updates to release 2.1

* Mon Aug 21 2023 Jerry Snitselaar <jsnitsel@redhat.com> - 1:1.6.0-8
- migrated to SPDX license
- resolves: rhbz#2219549* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.0-5

- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1:1.6.0-3
- Rebuilt with OpenSSL 3.0.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Feb 8 2021 Jerry Snitselaar <jsnitsel@redhat.com> - 1.6.0-1
- Rebase to v1.6.0 release.
- Manpage cleanup.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1331-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1331-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Feb 14 2020 Tom Stellard <tstellar@redhat.com> - 1331-5
- Use make_build macro
- https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1331-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Jeff Law <law@redhat.com> - 1331-3
- Ensure tssprintcmd has the compilation compilation flags,
  PIC in particular

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1331-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jerry Snitselaar <jsnitsel@redhat.com> - 1331-1
- Rebase to version 1331

* Tue May 28 2019 Jerry Snitselaar <jsnitsel@redhat.com> - 1234-4
- Fix covscan issues
- Fix compile and linker flag issues

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1234-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1234-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Jerry Snitselaar <jsnitsel@redhat.com> - 1234-1
- Version bump.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1027-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Merlin Mathesius <mmathesi@redhat.com> - 1027-1
- Version bump. Now supported for all architectures.
- Generate man pages since they are no longer included in source archive.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 713-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 713-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 713-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Oct 05 2016 Hon Ching(Vicky) Lo <lo1@us.ibm.com> - 713-7
- Removed defattr from the devel subpackage 

* Mon Sep 26 2016 Hon Ching(Vicky) Lo <lo1@us.ibm.com> - 713-6
- Added s390x arch as another "ExcludeArch"

* Mon Sep 26 2016 Hon Ching(Vicky) Lo <lo1@us.ibm.com> - 713-5
- Replaced ExclusiveArch with ExcludeArch 
 
* Mon Sep 19 2016 Hon Ching(Vicky) Lo <lo1@us.ibm.com> - 713-4
- Used ExclusiveArch instead of BuildArch tag
- Removed attr from symlink in devel subpackage 
- Added manpages and modified the Source0
- Added CCFLAGS and LNFLAGS to enforce hardening and optimization

* Wed Aug 17 2016 Hon Ching(Vicky) Lo <lo1@us.ibm.com> - 713-3
- Modified supported arch to ppc64le

* Sat Aug 13 2016 Hon Ching(Vicky) Lo <lo1@us.ibm.com> - 713-2
- Minor spec fixes 

* Tue Aug 09 2016 Hon Ching(Vicky) Lo <lo1@us.ibm.com> - 713-1
- Updated for initial submission 

* Fri Mar 20 2015 George Wilson <gcwilson@us.ibm.com>
- Initial implementation
