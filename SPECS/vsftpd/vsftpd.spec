Summary:        Very secure and very small FTP daemon.
Name:           vsftpd
Version:        3.0.5
Release:        1%{?dist}
License:        GPLv2 with exceptions
URL:            https://security.appspot.com/vsftpd.html
Group:          System Environment/Daemons
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://security.appspot.com/downloads/%{name}-%{version}.tar.gz

Patch0:         vsftpd-gen-debuginfo.patch
BuildRequires:  libcap-devel pam-devel openssl-devel libnsl2-devel
Requires:       libcap pam openssl libnsl2

%description
Very secure and very small FTP daemon.
%prep
%setup -q
%patch0

%build
sed -i 's/#undef VSF_BUILD_SSL/#define VSF_BUILD_SSL/g' builddefs.h
sed -i -e 's|#define VSF_SYSDEP_HAVE_LIBCAP|//&|' sysdeputil.c
make %{?_smp_mflags} CFLAGS="%{optflags}" LDFLAGS="-lssl -lcrypto"

%install
install -vdm 755 %{buildroot}%{_sbindir}
install -vdm 755 %{buildroot}%{_mandir}/{man5,man8}
install -vdm 755 %{buildroot}%{_sysconfdir}
install -vm 755 vsftpd        %{buildroot}%{_sbindir}/vsftpd
install -vm 644 vsftpd.8      %{buildroot}%{_mandir}/man8/
install -vm 644 vsftpd.conf.5 %{buildroot}%{_mandir}/man5/
cat >> %{buildroot}/etc/vsftpd.conf << "EOF"
background=YES
listen=YES
nopriv_user=vsftpd
secure_chroot_dir=/usr/share/vsftpd/empty
pasv_enable=Yes
pasv_min_port=40000
pasv_max_port=40100
#allow_writeable_chroot=YES
#write_enable=YES
#local_umask=022
#anon_upload_enable=YES
#anon_mkdir_write_enable=YES
EOF

%post
if [ $1 -eq 1 ] ; then
  install -v -d -m 0755 %{_datadir}/vsftpd/empty
  install -v -d -m 0755 /home/ftp
  if ! getent group vsftpd >/dev/null; then
      groupadd -g 47 vsftpd
  fi
  if ! getent group ftp >/dev/null; then
      groupadd -g 45 ftp
  fi
  if ! getent passwd vsftpd >/dev/null; then
      useradd -c "vsftpd User"  -d /dev/null -g vsftpd -s /bin/false -u 47 vsftpd
  fi
  if ! getent passwd ftp >/dev/null; then
      useradd -c anonymous_user -d /home/ftp -g ftp    -s /bin/false -u 45 ftp
  fi
fi

%postun
if [ $1 -eq 0 ] ; then
  if getent passwd vsftpd >/dev/null; then
      userdel vsftpd
  fi
  if getent passwd ftp >/dev/null; then
      userdel ftp
  fi
  if getent group vsftpd >/dev/null; then
      groupdel vsftpd
  fi
fi

%files
%defattr(-,root,root)
%license LICENSE
%{_sysconfdir}/*
%{_sbindir}/*
%{_datadir}/*

%changelog
*   Wed Apr 13 2022 Henry Beberman <henry.beberman@microsoft.com> - 3.0.5-1
-   Upgrade to version 3.0.5 to fix CVE-2021-3618
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.0.3-10
-   Added %%license line automatically
*   Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> 3.0.3-9
-   Renaming Linux-PAM to pam
*   Fri Apr 17 2020 Nicolas Ontiveros <niontive@microsoft.com> 3.0.3-8
-   Change libnsl to libnsl2.
*   Tue Mar 24 2020 Henry Beberman <henry.beberman@microsoft.com> 3.0.3-7
-   Fix linking against OpenSSL 1.1. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> small FTP daemon.3.0.3-6
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Sep 21 2018 Alexey Makhalov <amakhalov@vmware.com> 3.0.3-5
-   Use libnsl instead of obsoleted nsl from glibc
*   Thu Mar 15 2018 Xiaolin Li <xiaolinl@vmware.com> 3.0.3-4
-   Enable ssl support.
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0.3-3
-   Ensure non empty debuginfo
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 3.0.3-2
-   BuildRequires Linux-PAM-devel
*   Wed Nov 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.0.3-1
-   Upgraded to version 3.0.3, fixes CVE-2015-1419
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0.2-3
-   GA - Bump release of all rpms
*   Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0.2-2
-   Fix for upgrade issues
*   Mon Jul 6 2015 Alexey Makhalov <amakhalov@vmware.com> 3.0.2-1
-   initial version
