%define python3_sitearch %(python3 -c "from distutils.sysconfig import get_python_lib; import sys; sys.stdout.write(get_python_lib(1))")

Summary:        High-Level Crypto API
Name:           gpgme
Version:        1.13.1
Release:        4%{?dist}
License:        GPLv2+ or LGPLv2+
URL:            https://www.gnupg.org/(it)/related_software/gpgme/index.html
Group:          System Environment/Security
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://www.gnupg.org/ftp/gcrypt/%{name}/%{name}-%{version}.tar.bz2

Requires:	libassuan
Requires:	libgpg-error >= 1.32
Requires:	gnupg2
BuildRequires:	gnupg2
BuildRequires:	libgpg-error-devel >= 1.32
BuildRequires:	libassuan >= 2.2.0

%description
The GPGME package is a C language library that allows to add support for cryptography to a program. It is designed to make access to public key crypto engines like GnuPG or GpgSM easier for applications. GPGME provides a high-level crypto API for encryption, decryption, signing, signature verification and key management.

%package    devel
Group:      Development/Libraries
Summary:    Static libraries and header files from GPGME, GnuPG Made Easy.
Requires:   %{name} = %{version}-%{release}
Requires:   libgpg-error-devel >= 1.32

%description 	devel
Static libraries and header files from GPGME, GnuPG Made Easy.

%package -n     python3-gpg
Summary:        GPG bindings for Python 3
BuildRequires:  python3-devel
BuildRequires:  swig
Requires:       %{name} = %{version}-%{release}

%description -n python3-gpg
%{summary}.

%package -n     python-gpg
Summary:        GPG bindings for Python
BuildRequires:  python2-devel
BuildRequires:  swig
Requires:       %{name} = %{version}-%{release}

%description -n python-gpg
%{summary}.

%prep
%setup -q

%build
%configure \
    --enable-languages=cl,python \
    --disable-fd-passing \
    --disable-static \
    --disable-silent-rules \
    --disable-gpgsm-test
%make_build

%install
%make_install
rm %{buildroot}/%{_libdir}/*.la
rm -rf %{buildroot}/%{_infodir}

%post	-p /sbin/ldconfig

%postun	-p /sbin/ldconfig

%check
make check

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/aclocal/*
%{_datadir}/common-lisp/source/gpgme/*
%{_includedir}/*.h
%{_libdir}/*.so*
%{_libdir}/pkgconfig/%{name}*.pc

%files -n python3-gpg
%doc lang/python/README
%{python3_sitearch}/gpg-*.egg-info
%{python3_sitearch}/gpg/


%files -n python-gpg
%doc lang/python/README
%{python_sitearch}/gpg-*.egg-info
%{python_sitearch}/gpg/

%changelog
*   Wed May 13 2020 Emre Girgin <mrgirgin@microsoft.com> 1.13.1-4
-   Add python-gpg subpackage.
* Sat May 09 00:21:33 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.13.1-3
- Added %%license line automatically
*   Tue Apr 21 2020 Nicolas Ontiveros <niontive@microsoft.com> 1.13.1-2
-   Use gnupg2 for Requires and BR.
*   Fri Apr 17 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.13.1-1
-   Upgrading to version 1.13.1.
-   Removed 'sha1' macro.
-   Added building the 'python3-gpg' subpackage.
-   License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.11.1-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Sat Oct 20 2018 Ankit Jain <ankitja@vmware.com> 1.11.1-2
-   Removed gpg2, gnupg-2.2.10 doesn't provide gpg2
*   Tue Sep 11 2018 Anish Swaminathan <anishs@vmware.com> 1.11.1-1
-   Update version to 1.11.1
*   Wed Aug 30 2017 Alexey Makhalov <amakhalov@vmware.com> 1.9.0-3
-   Add requires gnupg
*   Thu Apr 20 2017 Alexey Makhalov <amakhalov@vmware.com> 1.9.0-2
-   Disabe C++ bindings
*   Thu Apr 13 2017 Danut Moraru <dmoraru@vmware.com> 1.9.0-1
-   Update to version 1.9.0
*   Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 1.6.0-3
-   Required libgpg-error-devel.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.0-2
-   GA - Bump release of all rpms
*   Thu Jan 14 2016 Xiaolin Li <xiaolinl@vmware.com> 1.6.0-1
-   Updated to version 1.6.0
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 1.5.3-2
-   Updated group.
*   Tue Dec 30 2014 Divya Thaluru <dthaluru@vmware.com> 1.5.3-1
-   Initial version
