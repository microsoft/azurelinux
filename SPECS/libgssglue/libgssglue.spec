Summary:        This library exports a gssapi interface
Name:           libgssglue
Version:        0.4
Release:        6%{?dist}
License:        BSD and MIT
URL:            http://www.citi.umich.edu/projects/nfsv4/linux/
Group:          System Environment/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        http://www.citi.umich.edu/projects/nfsv4/linux/libgssglue/%{name}-%{version}.tar.gz

%description
This library exports a gssapi interface, but doesn't implement any gssapi mechanisms itself; instead it calls gssapi routines in other libraries, depending on the mechanism.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}
%description    devel
It contains the libraries and header files to create applications

%prep
%setup -q
%build
%configure --prefix=/usr --disable-static

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot}/%{_libdir} -name '*.la' -delete

%post

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/libgssglue.so.*

%files  devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libgssglue.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Feb 08 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.4-6
- Remove unused `%%define sha1` lines
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.4-5
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.4-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Oct 25 2018 Ajay Kaher <akaher@vmware.com> - 0.4-3
- Corrected spec file name

* Thu Jul 26 2018 Ajay Kaher <akaher@vmware.com> - 0.4-2
- Resolved compilation error for aarch64

* Mon Jan 22 2018 Xiaolin Li <xiaolinl@vmware.com> - 0.4-1
- Initial build. First version
