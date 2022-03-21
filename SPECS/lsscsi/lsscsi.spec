Summary:        List SCSI devices information.
Name:           lsscsi
Version:        0.32
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Hardware/Others.
URL:            https://sg.danny.cz/scsi/lsscsi.html
Source0:        http://sg.danny.cz/scsi/%{name}-%{version}.tar.xz

%description
This lists the information about SCSI devices.

%prep
%autosetup

%build
%configure

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
make %{?_smp_mflags} -k check

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_mandir}/*

%changelog
* Mon Feb 07 2022 Henry Li <lihl@microsoft.com> - 0.32-1
- Upgrade to version 0.32
- Use autosetup
- Delete sha1 macro
- License Verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.30-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.30-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*	Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 0.30-1
-	Update to version 0.30

*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.28-2
-	GA - Bump release of all rpms

*	Fri Apr 08 2016 Kumar Kaushik <kaushikk@vmware.com> 0.28-1
-	Initial build. First version
