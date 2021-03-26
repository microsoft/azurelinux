Summary:        software font engine.
Name:           freetype
Version:        2.9.1
Release:        5%{?dist}
License:        BSD/GPL
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://www.freetype.org/
Source0:        https://download.savannah.gnu.org/releases/freetype/freetype-%{version}.tar.gz
BuildRequires:  libtool
BuildRequires:  zlib-devel

%description
FreeType is a software font engine that is designed to be small, efficient, highly customizable, and portable while capable of producing high-quality output (glyph images). It can be used in graphics libraries, display servers, font conversion tools, text image generation tools, and many other products as well.

%package	devel
Summary:        Header and development files
Requires:       freetype = %{version}-%{release}

%description	devel
It contains the libraries and header files to create applications

%prep
%setup -q

%build
./configure \
	--prefix=%{_prefix} \
	--with-harfbuzz=no \
	--enable-freetype-config
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print
find %{buildroot} -name '*.a' -delete

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license docs/LICENSE.TXT
%{_libdir}/*.so*
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_bindir}/freetype-config

%changelog
* Thu Mar 25 2021 Henry Li <lihl@microsoft.com> - 2.9.1-5
- Add enable-fretype-config to configuration
- Add /usr/bin/freetype-config to freetype-devel

* Sat May 09 00:21:42 PST 2020 Nick Samson <nisamson@microsoft.com> - 2.9.1-4
- Added %%license line automatically

*   Fri Apr 17 2020 Nicolas Ontiveros <niontive@microsoft.com> 2.9.1-3
-   Rename freetype2 to freetype.
-   Update URL.
-   Remove sha1 macro.
-   Update Source0.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.9.1-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*	Wed Sep 12 2018 Sujay G <gsujay@vmware.com> 2.9.1-1
-	version bump to 2.9.1

*       Thu Jun 14 2018 Tapas Kundu <tkundu@vmware.com> 2.7.1-4
-       CVE-2018-6942

*       Mon May 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.7.1-3
-       CVE-2017-8287

*       Fri Apr 28 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.7.1-2
-       CVE-2017-7857, CVE-2017-7858 and CVE-2017-7864

*       Fri Nov 11 2016 Dheeraj Shetty <dheerajs@vmware.com> 2.7.1-1
-       Initial version
