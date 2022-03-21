Summary:        C based http parser for high performance applications.
Name:           http-parser
# Note: this package is no longer actively maintained.
# We should consider using https://github.com/nodejs/llhttp instead, 
# if dependent packages support it.
Version:        2.9.4
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/nodejs/http-parser
Source0:        https://github.com/nodejs/http-parser/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz     
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  gcc

%description
This is a parser for HTTP messages written in C. It parses both requests and responses. The parser is designed to be used in performance HTTP applications. It does not make any syscalls nor allocations, it does not buffer data, it can be interrupted at anytime.

%package devel
Summary:        http-parser devel
Group:          Development/Tools
Requires:       %{name} = %{version}
%description devel
This contains development tools and libraries for http-parser.

%prep
%setup -q

%build
make PREFIX=%{_prefix} %{?_smp_mflags} CFLAGS="%{build_cflags}"

%install
make PREFIX="%{_prefix}" DESTDIR="%{buildroot}" install

%files
%defattr(-,root,root)
%license LICENSE-MIT
%{_libdir}/libhttp_parser.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/http_parser.h
%{_libdir}/libhttp_parser.so

%changelog
* Fri Feb 18 2022 Cameron Baird <cameronbaird@microsoft.com> - 2.9.4-1
- Update source to v2.9.4

* Sun May 31 2020 Henry Beberman <henry.beberman@microsoft.com> - 2.8.1-5
- Update make to explicitly consume cflags

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.8.1-4
- Added %%license line automatically

* Tue Apr 14 2020 Nick Samson <nisamson@microsoft.com> 2.8.1-3
- Updated Source0, License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.8.1-2
- Initial CBL-Mariner import from Photon (license: Apache2).

*  Fri Aug 03 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 2.8.1-1
-  Update to version 2.8.1 to get it to build with gcc 7.3

*  Wed Jul 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.7.1-1
-  Initial version of http-parser package for Photon.
