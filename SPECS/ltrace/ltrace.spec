Summary:	ltrace intercepts and records dynamic library calls.
Name:		ltrace
Version:	0.7.3
Release:        8%{?dist}
License:	GPLv2+
URL:		http://www.ltrace.org/
Group:		Development/Debuggers
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:	http://www.ltrace.org/%{name}_%{version}.orig.tar.bz2
Patch0:		Move-get_hfa_type-from-IA64-backend-to-type.c-name-i.patch
Patch1:		Set-child-stack-alignment-in-trace-clone.c.patch
Patch2:		Implement-aarch64-support.patch
Patch3:		add-missing-stdint.h-include.patch
Patch4:		Add-missing-include-stdio.h.patch
BuildRequires:	elfutils-libelf-devel
Requires:	elfutils-libelf

%description
ltrace intercepts and records dynamic library calls which are called by an executed process and the signals received by that process. It can also intercept and print the system calls executed by the program.

%prep
%setup -q
%ifarch aarch64
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%endif

%build
autoreconf -fiv
%configure \
	--disable-werror

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%license COPYING
%{_sysconfdir}/ltrace.conf
%{_bindir}/*
%{_datadir}

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 0.7.3-8
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.7.3-7
- Removing the explicit %%clean stage.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.7.3-6
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.7.3-5
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 0.7.3-4
-   Aarch64 support
*       Mon Oct 03 2016 ChangLee <changLee@vmware.com> 0.7.3-3
-       Modified check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.7.3-2
-	GA - Bump release of all rpms
*	Wed Nov 25 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.7.3-1
-	Initial build.	First version
