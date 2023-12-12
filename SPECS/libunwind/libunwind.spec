Summary:        Portable and efficient C programming interface (API) to determine the call-chain of a program.
Name:           libunwind
Version:        1.6.2
Release:        2%{?dist}
License:        X11
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Utilities/Libraries
URL:            https://www.nongnu.org/libunwind/
Source0:        http://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.tar.gz

%description
Portable and efficient C programming interface (API) to determine the call-chain of a program. The API additionally provides the means to manipulate the preserved (callee-saved) state of each call-frame and to resume execution at any point in the call-chain (non-local goto). The API supports both local (same-process) and remote (across-process) operation. As such, the API is useful in a number of applications.

%package devel
Summary:        libunwind devel
Group:          Development/Tools

%description devel
This contains development tools and libraries for libunwind.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/libunwind*.so.*

%files devel
%{_includedir}/*unwind*
%{_libdir}/libunwind*.a
%{_libdir}/libunwind*.so
%{_libdir}/pkgconfig/libunwind*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.6.2-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue Jan 25 2022 Henry Li <lihl@microsoft.com> - 1.6.2-1
- Upgrade to version 1.6.2
- License Verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.2-4
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.2-3
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 1.2-2
-   Use standard configure macros

*   Mon Feb 06 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.2-1
-   Initial version of libunwind package for Photon.
