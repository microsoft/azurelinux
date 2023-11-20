Summary:	Gperf
Name:		gperf
Version:	3.1
Release:        5%{?dist}
License:	GPLv3+
URL:		http://freedesktop.org/wiki/Software/%{name}l/
Source0:	http://ftp.gnu.org/gnu/gperf/%{name}-%{version}.tar.gz
Group:		Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner

%description
Gperf generates a perfect hash function from a key set.

%prep
%setup -q

%build
./configure \
	--prefix=%{_prefix} \
	--docdir=%{_defaultdocdir}/%{name}-%{version}
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -v -m644 doc/gperf.{dvi,ps,pdf} %{buildroot}/%{_docdir}/%{name}-%{version}
pushd  %{buildroot}/usr/share/info &&
  for FILENAME in *; do
    install-info $FILENAME %{name}-%{version} 2>/dev/null
  done &&
popd

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%license COPYING
%{_docdir}/%{name}-%{version}/*
%{_mandir}/man1/*
%{_datadir}/info/*
%{_bindir}/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 3.1-5
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue Feb 08 2022 Thomas Crain <thcrain@microsoft.com> - 3.1-4
- Remove unused `%%define sha1` lines
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.1-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 3.1-2
- Initial CBL-Mariner import from Photon (license: Apache2).

*	Thu Apr 13 2017 Danut Moraru <dmoraru@vmware.com> - 3.1-1
-	Updated to version 3.1

*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 3.0.4-2
-	GA - Bump release of all rpms

*	Thu Oct 23 2014 Divya Thaluru <dthaluru@vmware.com> - 3.0.4-1
-	Initial build. First version
