Summary:	Text editor
Name:		nano
Version:	3.0
Release:        3%{?dist}
License:	GPLv3+
URL:		http://www.nano-editor.org/
Group:		Applications/Editors
Source0:	http://www.nano-editor.org/dist/v3/%{name}-%{version}.tar.xz
%define sha1 nano=0396d85df64a7927ca2d3425a0263dacf8502220
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:	ncurses-devel
Requires:	ncurses

%description
The Nano package contains a small, simple text editor

%package lang
Summary:	Lang for nano
Requires:	%{name} = %{version}
%description lang
Lang for nano

%prep
%setup -q -n %{name}-%{version}
%build
./configure --prefix=%{_prefix}      \
            --sysconfdir=%{_sysconfdir} \
            --enable-utf8     \
            --infodir=%{_infodir}/%{name}-%{version} \
            --docdir=%{_docdir}/%{name}-%{version}
make

%install
make DESTDIR=%{buildroot} install
install -v -m644 %{_builddir}/%{name}-%{version}/doc/sample.nanorc %{_sysconfdir}
install -v -m644 %{_builddir}/%{name}-%{version}/doc/nano.html %{_docdir}/%{name}-%{version}.html
%find_lang %{name}

%check
make %{?_smp_mflags} check

%files lang -f %{name}.lang
%defattr(-,root,root)
%license COPYING

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man*/*
%{_infodir}/%{name}-%{version}/*
%{_datadir}/nano/*
%{_datadir}/doc/%{name}-%{version}/*

%changelog
* Sat May 09 00:21:02 PST 2020 Nick Samson <nisamson@microsoft.com> - 3.0-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Wed Sep 12 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 3.0-1
-   Update package version
*   Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 2.8.0-1
-   Update package version
*   Mon Oct 03 2016 ChangLee <changlee@vmware.com> 2.5.2-3
-   Modified check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.5.2-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Kumar Kaushik <kaushikk@vmware.com> 2.5.2-1
-   Updating to new version.
*   Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 2.2.6-2
-   Handled locale files with macro find_lang
*   Tue Dec 30 2014 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.2.6-1
-   Initial build.	First version
