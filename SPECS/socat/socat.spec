Summary:        Multipurpose relay (SOcket CAT)
Name:           socat
Version:        1.7.4.4
Release:        1%{?dist}
License:        GPL2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Internet
URL:            http://www.dest-unreach.org/socat
Source0:        http://www.dest-unreach.org/socat/download/%{name}-%{version}.tar.gz

%description
Socat is a command line based utility that establishes two bidirectional byte streams and transfers data between them. Because the streams can be constructed from a large set of different types of data sinks and sources (see address types), and because lots of address options may be applied to the streams, socat can be used for many different purposes.

%prep
%setup -q

%build
./configure --prefix=%{_prefix} --sysconfdir=%{_sysconfdir}

make %{?_smp_mflags} CFLAGS="%{build_cflags} -Doff64_t=__off64_t -D_GNU_SOURCE"

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete

%check
make %{?_smp_mflags} test

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.7.4.4-1
- Auto-upgrade to 1.7.4.4 - Azure Linux 3.0 - package upgrades

* Mon Jan 24 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.7.4.3-1
- Update to version 1.7.4.3.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.7.3.4-3
- Removing the explicit %%clean stage.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.7.3.4-2
- Added %%license line automatically

* Tue Mar 24 2020 Henry Beberman <henry.beberman@microsoft.com> 1.7.3.4-1
- Switch to 1.7.3.4. Updated Source0 URL. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.0.b9-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Sep 19 2018 Srinidhi Rao <srinidhir@vmware.com> 2.0.0.b9-1
- Upgrade to 2.0.0-b9

* Tue Sep 19 2017 Bo Gan <ganb@vmware.com> 1.7.3.2-4
- Disable test 302

* Tue Sep 12 2017 Xiaolin Li <xiaolinl@vmware.com> 1.7.3.2-3
- Fix make check issue.

* Tue May 02 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.7.3.2-2
- Correct the GPL license version.

* Thu Apr 13 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.7.3.2-1
- Update to version 1.7.3.2

* Wed Jan 11 2017 Xiaolin Li <xiaolinl@vmware.com>  1.7.3.1-1
- Initial build.
