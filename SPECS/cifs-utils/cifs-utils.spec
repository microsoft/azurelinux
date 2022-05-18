Summary:        cifs client utils
Name:           cifs-utils
Version:        6.14
Release:        2%{?dist}
License:        GPLv3
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Nfs-utils-client
URL:            https://wiki.samba.org/index.php/LinuxCIFS_utils
Source0:        https://download.samba.org/pub/linux-cifs/%{name}/%{name}-%{version}.tar.bz2
Patch0:         CVE-2022-29869.patch
Patch1:         CVE-2022-27239.patch
BuildRequires:  keyutils-devel
BuildRequires:  libcap-ng-devel
BuildRequires:  libtalloc-devel
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
%configure --prefix=%{_prefix} ROOTSBINDIR=%{_sbindir}
%make_build

%install
%make_install

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/cifscreds
%{_bindir}/smb2-quota
%{_bindir}/smbinfo
%{_sbindir}/mount.cifs
%{_sbindir}/mount.smb3

%files -n pam_cifscreds
%{_libdir}/security/pam_cifscreds.so

%files devel
%defattr(-,root,root)
%{_includedir}/cifsidmap.h

%changelog
* Tue May 17 2022 Chris Co <chrco@microsoft.com> - 6.14-2
- Address CVE-2022-27239, CVE-2022-29869
- Fix lint

* Fri Jan 14 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 6.14-1
- Upgrade to 6.14.

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
