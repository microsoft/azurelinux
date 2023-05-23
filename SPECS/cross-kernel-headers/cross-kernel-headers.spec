# Globals which should be in a macro file.
# These should be set programatically in the future.
%global _host_arch      x86_64
%global _target_arch    aarch64
%global _tuple          %{_target_arch}-%{_vendor}-linux-gnu
%global _cross_name     %{_target_arch}-%{_vendor}-linux-gnu

# Folders which should be in our macro file
%global _opt                /opt/
%global _crossdir           /opt/cross/

# Generally we include '/usr' in most paths.
# Can we also use '/usr' for our paths? This will bring us in line with the
# %%configure macro which sets these.
%global _bindir            /bin
%global _sbindir           /sbin
%global _libdir            /lib
%global _lib64dir          /lib64
%global _libexecdir        /libexec
%global _datadir           /share
%global _docdir            /share/doc
%global _includedir        /include
%global _infodir           /share/info
%global _mandir            /share/man
%global _oldincludedir     /include


# Why is this wrong? We get "x86_64-pc-linux-gnu" when eval'd, but our 
# tools select "aarch64-linux-gnu"
%global _host_vendor        %{nil}

# If we want our cross compile aware packges to also support native, we
# need logic to switch modes something like this:
%if "%{_target_arch}" != "%{_host_arch}"
%global _cross_prefix       %{_crossdir}%{_tuple}/
%global _cross_sysroot      %{_crossdir}%{_tuple}/sysroot/
%global _cross_includedir   /usr/%{_host}/%{_tuple}/include/
%global _cross_infodir      %{_crossdir}%{_tuple}/share/info
%global _cross_bindir       %{_tuple}/bin
%global _cross_libdir       %{_tuple}/lib
%global _tuple_name         %{_tuple}-
%else
%global _cross_prefix       %{nil}
%global _cross_sysroot      %{nil}
%global _cross_includedir   %{_includedir}
%global _cross_infodir      %{_infodir}
%global _cross_bindir       %{_bindir}
%global _cross_libdir       %{_libdir}
%global _tuple_name         %{nil}
%endif

Summary:        Linux API header files
Name:           %{_cross_name}-kernel-headers
Version:        5.15.57.1
Release:        3%{?dist}
License:        GPLv2
URL:            https://github.com/microsoft/CBL-Mariner-Linux-Kernel
Group:          System Environment/Kernel
Vendor:         Microsoft Corporation
Distribution:   Mariner
#Source0:       https://github.com/microsoft/CBL-Mariner-Linux-Kernel/archive/rolling-lts/mariner-2/%%{version}.tar.gz
Source0:        kernel-%{version}.tar.gz
BuildArch:      noarch
Provides:       %{_cross_name}-glibc-kernheaders = %{version}-%{release}
%if "%{_target_arch}" == "x86_64"
%define arch x86_64
%endif

%if "%{_target_arch}" == "aarch64"
%define arch arm64
%endif

%description
The Linux API Headers expose the kernel's API for use by Glibc.

%prep
%setup -q -n CBL-Mariner-Linux-Kernel-rolling-lts-mariner-2-%{version}

%build
make mrproper

%install
cd %{_builddir}/CBL-Mariner-Linux-Kernel-rolling-lts-mariner-2-%{version}
make ARCH=%{arch} headers
find usr/include -name '.*' -delete
rm usr/include/Makefile
mkdir -p                /%{buildroot}%{_cross_sysroot}%{_includedir}
cp -rv usr/include/*    /%{buildroot}%{_cross_sysroot}%{_includedir}

%files
%defattr(-,root,root)
%license COPYING
%{_cross_sysroot}%{_includedir}/*

%changelog
*   Thu Dec 15 2022 Dallas Delaney <dadelan@microsoft.com> - 5.15.57.1-3
-   Update to 5.15.57.1
*   Mon Jun 20 2022 Chris Co <chrco@microsoft.com> - 5.15.48.1-1
-   Update to 5.15.48.1
*   Thu Feb 11 2021 Daniel McIlvaney <damcilva@microsoft.com> - 5.4.51-13
-   Fork normal kernel-headers package into cross compile aware version
*   Mon Jan 11 2021 Thomas Crain <thcrain@microsoft.com> - 5.4.51-12
-   Update Release tag to match that of the kernel package
*   Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> 5.4.51-3
-   Add explicit provide for glibc-kernheaders
*   Tue Sep 01 2020 Chris Co <chrco@microsoft.com> 5.4.51-2
-   Update source hash
*   Wed Aug 19 2020 Chris Co <chrco@microsoft.com> 5.4.51-1
-   Update source to 5.4.51
*   Fri Jun 12 2020 Chris Co <chrco@microsoft.com> 5.4.42-1
-   Update source to 5.4.42
*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 5.4.23-2
-   Renaming linux-api-headers to kernel-headers
*   Tue Dec 10 2019 Chris Co <chrco@microsoft.com> 5.4.23-1
-   Update to Microsoft Linux Kernel 5.4.23.
-   Use make headers since with 5.4, headers_install now requires rsync.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.19.52-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Jun 17 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-1
-   Update to version 4.19.52
*   Tue May 07 2019 Ajay Kaher <akaher@vmware.com> 4.19.40-1
-   Update to version 4.19.40
*   Wed Mar 27 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-1
-   Update to version 4.19.32
*   Thu Mar 14 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.29-1
-   Update to version 4.19.29
*   Tue Mar 05 2019 Ajay Kaher <akaher@vmware.com> 4.19.26-1
-   Update to version 4.19.26
*   Tue Jan 15 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.15-1
-   Update to version 4.19.15
*   Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-1
-   Update to version 4.19.6
*   Mon Nov 05 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.1-1
-   Update to version 4.19.1
*   Thu Sep 20 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.18.9-1
-   Update to version 4.18.9
*   Wed Sep 19 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.67-1
-   Update to version 4.14.67
*   Mon Jul 09 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.14.54-1
-   Update to version 4.14.54
*   Fri Dec 22 2017 Alexey Makhalov <amakhalov@vmware.com> 4.14.8-1
-   Version update
*   Mon Dec 04 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.66-1
-   Version update
*   Tue Nov 21 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.64-1
-   Version update
*   Mon Nov 06 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.60-1
-   Version update
*   Thu Oct 05 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.53-1
-   Version update
*   Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-1
-   Version update
*   Mon Sep 04 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.47-1
-   Version update
*   Mon Aug 14 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.43-1
-   Version update
*   Wed Jun 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.34-1
-   Version update
*   Fri May 26 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.30-1
-   Version update
*   Tue May 16 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.28-1
-   Version update
*   Wed May 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.27-1
-   Update to linux-4.9.27
*   Sun May 7 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.26-1
-   Update to linux-4.9.26
*   Tue Apr 25 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.24-1
-   Update to linux-4.9.24
*   Tue Feb 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-1
-   Update to linux-4.9.13
*   Thu Feb 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.9-1
-   Update to linux-4.9.9
*   Tue Jan 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.2-1
-   Update to linux-4.9.2
*   Mon Dec 12 2016 Alexey Makhalov <amakhalov@vmware.com> 4.9.0-1
-   Update to linux-4.9.0
*   Mon Nov 28 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-1
-   Update to linux-4.4.35
*   Thu Nov 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-1
-   Update to linux-4.4.31
*   Wed Sep  7 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-1
-   Update kernel version to 4.4.20
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.4.8-2
-   GA - Bump release of all rpms
*   Thu Apr 28 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-1
-   Update to linux-4.4.8
*   Wed Dec 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-1
-   Upgrading kernel version to 4.2.0.
*   Wed Aug 12 2015 Sharath George <sharathg@vmware.com> 4.0.9-1
-   Upgrading kernel version.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.13.3-1
-   Initial build. First version
