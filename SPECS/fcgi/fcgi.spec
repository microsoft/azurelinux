Summary:        FastCGI development kit
Name:           fcgi
Version:        2.4.0
Release:        7%{?dist}
License:        OML
# NOTE: below is an archive of FastCGI. The original project web page (http://www.fastcgi.com) is no longer online.
URL:            https://fastcgi-archives.github.io
Source0:        https://src.fedoraproject.org/lookaside/extras/%{name}/%{name}-%{version}.tar.gz/d15060a813b91383a9f3c66faf84867e/%{name}-%{version}.tar.gz
Patch0:         fcgi-EOF.patch
Patch1:         CVE-2012-6687.patch
Group:          Development/Libraries/C and C++
Vendor:         Microsoft Corporation
Distribution:   Mariner

%description
FastCGI is a language independent, scalable, open extension to CGI that
provides high performance without the limitations of server specific APIs.

%package   devel
Summary:    Header and development files
Requires:   %{name} = %{version}

%description   devel
FastCGI is a language independent, scalable, open extension to CGI that
provides high performance without the limitations of server specific APIs.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure \
   --disable-static
make

%install
make DESTDIR=%{buildroot} install
find %{buildroot}/%{_libdir} -name '*.a' -delete
find %{buildroot}/%{_libdir} -name '*.la' -delete

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE.TERMS
%{_bindir}/*
%{_libdir}/libfcgi*.so*

%files devel
%defattr(-,root,root)
%{_includedir}/*

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.4.0-7
- Added %%license line automatically

*   Mon Apr 27 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 2.4.0-6
-   Fixed 'Source0' and 'URL' tags.
-   License verified.
*   Thu Feb 27 2020 Henry Beberman <hebeberm@microsoft.com> 2.4.0-5
-   Glob to include libfcgi++ as well as libfcgi in RPM
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.4.0-4
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 2.4.0-3
-   Use standard configure macros
*   Wed May 24 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.4.0-2
-   Patch for CVE-2012-6687
*   Fri Dec 16 2016 Dheeraj Shetty <dheerajs@vmware.com> 2.4.0-1
-   Initial build. First version
