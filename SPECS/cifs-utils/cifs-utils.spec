Summary:        cifs client utils
Name:           cifs-utils
Version:        6.8
Release:        6%{?dist}
License:        GPLv3
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Nfs-utils-client
URL:            https://wiki.samba.org/index.php/LinuxCIFS_utils
Source0:        https://ftp.samba.org/pub/linux-cifs/cifs-utils/cifs-utils-%{version}.tar.bz2
Patch0:         CVE-2020-14342.patch
Patch1:         CVE-2020-14342-fix.patch
Patch2:         CVE-2021-20208.patch
BuildRequires:  libcap-ng-devel
BuildRequires:  libtalloc-devel
BuildRequires:  keyutils-devel
BuildRequires:  pam-devel
Requires:       libcap-ng

%description
Cifs-utils, a package of utilities for doing and managing mounts of the Linux CIFS filesystem.

%package -n pam_cifscreds
Summary:        PAM module to manage NTLM credentials in kernel keyring

%description -n pam_cifscreds
The pam_cifscreds PAM module is a tool for automatically adding
credentials (username and password) for the purpose of establishing
sessions in multiuser mounts.

When a cifs filesystem is mounted with the "multiuser" option, and does
not use krb5 authentication, it needs to be able to get the credentials
for each user from somewhere. The pam_cifscreds module can be used to
provide these credentials to the kernel automatically at login.

%package devel
Summary:        The libraries and header files needed for Cifs-Utils development.
Group:          Development/Libraries
Requires:       cifs-utils = %{version}-%{release}

%description devel
Provides header files needed for Cifs-Utils development.

%prep
%autosetup

%build
autoreconf -fiv
%configure
%make_build

%install
%make_install

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/cifscreds
/sbin/mount.cifs

%files -n pam_cifscreds
%{_libdir}/security/pam_cifscreds.so

%files devel
%defattr(-,root,root)
%{_includedir}/cifsidmap.h

%changelog
* Wed Sep 29 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.8-6
- Adding the 'pam_cifscreds' subpackage using Fedora 32 spec (license: MIT) as guidance.

* Mon May 03 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.8-5
- Adding a patch fo CVE-2021-20208.
- Updated "URL" tag to use HTTPS.
- License verified.

* Wed Sep 30 2020 Henry Beberman <henry.beberman@microsoft.com> - 6.8-4
- Add patch for CVE-2020-14342

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 6.8-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 6.8-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 07 2017 Ajay Kaher <akaher@vmware.com> - 6.8-1
- Upgraded to version 6.8

* Thu Apr 06 2017 Anish Swaminathan <anishs@vmware.com> - 6.7-1
- Upgraded to version 6.7

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 6.4-2
- GA - Bump release of all rpms

* Mon Jan 25 2016 Divya Thaluru <dthaluru@vmware.com> - 6.4-1
- Initial build. First version
