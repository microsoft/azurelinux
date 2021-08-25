Summary:	Portable and efficient C programming interface (API) to determine the call-chain of a program.
Name:		libunwind
Version:	1.2
Release:        4%{?dist}
License:	X11
URL:		http://www.nongnu.org/libunwind/
Source0:	http://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.tar.gz
%define sha1 libunwind=a33e52d7ecd18b9375508369b566eeb2cc6eec3b
Group:		Utilities/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner

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
find %{buildroot} -name '*.la' -delete

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
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.2-4
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.2-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 1.2-2
-   Use standard configure macros
*   Mon Feb 06 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.2-1
-   Initial version of libunwind package for Photon.
