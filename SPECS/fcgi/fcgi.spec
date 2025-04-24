Summary:        FastCGI development kit
Name:           fcgi
Version:        2.4.5
Release:        1%{?dist}
License:        OML
# NOTE: below is an archive of FastCGI. The original project web page (http://www.fastcgi.com) is no longer online.
URL:            https://fastcgi-archives.github.io
Source0:        https://github.com/FastCGI-Archives/fcgi2/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Group:          Development/Libraries/C and C++
Vendor:         Microsoft Corporation
Distribution:   Azure Linux

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
%autosetup -n %{name}2-%{version} -p1

%build
./autogen.sh
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
%license LICENSE
%{_bindir}/*
%{_libdir}/libfcgi*.so*
%doc %{_mandir}/man1/cgi-fcgi.1*
%doc %{_mandir}/man3/FCGI_Accept.3*
%doc %{_mandir}/man3/FCGI_Finish.3*
%doc %{_mandir}/man3/FCGI_SetExitStatus.3*
%doc %{_mandir}/man3/FCGI_StartFilterData.3*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/fcgi*.pc

%changelog
* Tue Apr 22 2025 Kanishk Bansal <kanbansal@microsoft.com> - 2.4.5-1
- Upgrade to 2.4.5 to fix CVE-2025-23016
- Remove patch of CVE-2012-6687, fcgi-EOF
- Added missing man pages and pkgconfig files to package

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.4.0-7
- Added %%license line automatically

* Mon Apr 27 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 2.4.0-6
- Fixed 'Source0' and 'URL' tags.
- License verified.

* Thu Feb 27 2020 Henry Beberman <hebeberm@microsoft.com> 2.4.0-5
- Glob to include libfcgi++ as well as libfcgi in RPM

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.4.0-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 2.4.0-3
- Use standard configure macros

* Wed May 24 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.4.0-2
- Patch for CVE-2012-6687

* Fri Dec 16 2016 Dheeraj Shetty <dheerajs@vmware.com> 2.4.0-1
- Initial build. First version
