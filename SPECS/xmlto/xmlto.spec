Summary:        The  purpose  of  xmlto is to convert an XML file to the desired format
Name:           xmlto
Version:        0.0.28
Release:        7%{?dist}
License:        GPLv2+
URL:            https://pagure.io/xmlto
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        http://releases.pagure.org/xmlto/%{name}-%{version}.tar.gz
BuildRequires:  docbook-style-xsl
BuildRequires:  docbook-dtd-xml
BuildRequires:  libxslt-devel
Requires:       docbook-style-xsl
Requires:       libxslt

%description
The  purpose  of  xmlto is to convert an XML file to the desired format

%prep
%setup -q

%build
./configure \
    --prefix=%{_prefix}

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_mandir}/*/*
%{_datadir}/xmlto/*

%changelog
* Wed Mar 16 2022 Andrew Phelps <anphel@microsoft.com> - 0.0.28-7
- Remove unneeded systemd requires

* Tue Feb 08 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.0.28-6
- Remove unused `%%define sha1` lines
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.0.28-5
- Added %%license line automatically

* Tue May 05 2020 Emre Girgin <mrgirgin@microsoft.com> - 0.0.28-4
- Renaming docbook-xsl to docbook-style-xsl

* Tue May 05 2020 Emre Girgin <mrgirgin@microsoft.com> - 0.0.28-3
- Renaming docbook-xml to docbook-dtd-xml

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.0.28-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Apr 06 2017 Dheeraj Shetty <dheerajs@vmware.com> - 0.0.28-1
- Initial build.  First version
