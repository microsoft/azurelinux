Summary:        AsciiDoc is a human readable text document format
Name:           asciidoc
Version:        8.6.10
Release:        4%{?dist}
License:        GPLv2
URL:            http://asciidoc.org/
Group:          System Environment/Development
Vendor:         Microsoft Corporation
Distribution:   Mariner
#Source0:       https://github.com/%{name}/%{name}-py3/archive/%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3
BuildRequires:  python-xml
BuildRequires:  libxslt
BuildRequires:  docbook-style-xsl
BuildRequires:  docbook-dtd-xml
BuildRequires:  python2
Requires:       python3
Requires:       python-xml
Requires:       libxslt
Requires:       docbook-style-xsl
Requires:       docbook-dtd-xml
Requires:       python2

%description
AsciiDoc is a human readable text document format that can be easily converted to other document formats.

%prep
%setup -q -n %{name}-py3-%{version}

%build
autoreconf -v
export CFLAGS="%{optflags}"
./configure  --prefix=%{_prefix} --sysconfdir=%{_sysconfdir}

make %{?_smp_mflags}

%install
rm -rf %{buildroot}%{_infodir}
make DESTDIR=%{buildroot} install

%check
python tests/testasciidoc.py update
python tests/testasciidoc.py run

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_sysconfdir}/*
%{_mandir}/*

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 8.6.10-4
- Added %%license line automatically

*   Tue May 05 2020 Emre Girgin <mrgirgin@microsoft.com> 8.6.10-3
-   Renaming docbook-xsl to docbook-style-xsl
*   Tue May 05 2020 Emre Girgin <mrgirgin@microsoft.com> 8.6.10-2
-   Renaming docbook-xml to docbook-dtd-xml
*   Wed Mar 25 2020 Emre Girgin <mrgirgin@microsoft.com> 8.6.10-1
-   Update to verison 8.6.10 and python3 implementation. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 8.6.9-5
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Wed Sep 06 2017 Anish Swaminathan <anishs@vmware.com> 8.6.9-4
-   Use system sysconfdir
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 8.6.9-3
-   Fix arch
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 8.6.9-2
-   GA - Bump release of all rpms
*   Fri Jun 5 2015 Touseef Liaqat <tliaqat@vmware.com> 8.6.9-1
-   Initial build.  First version
