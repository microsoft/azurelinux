Summary:        Program for compiling packages
Name:           make
Version:        4.4.1
Release:        1%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://www.gnu.org/software/make
Source0:        https://ftp.gnu.org/gnu/make/%{name}-%{version}.tar.gz

%if %{with_check}
BuildRequires: perl(lib)
BuildRequires: perl(FindBin)
%endif

%description
The Make package contains a program for compiling packages.

%prep
%autosetup

%build
./configure \
    --prefix=%{_prefix} \
    --disable-silent-rules
%make_build

%install
%make_install
rm -rf %{buildroot}%{_infodir}

%find_lang %{name}

%check
%make_build check

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_includedir}/gnumake.h
%{_mandir}/*/*

%changelog
* Mon Jan 22 2024 Andrew Phelps <anphel@microsoft.com> - 4.4.1-1
- Upgrade to version 4.4.1

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 4.3-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Jan 20 2022 Muhammad Falak <mwani@microsoft.com> - 4.3-2
- Fix ptest with an explicit BR on `perl(lib)`.

* Wed Nov 24 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.3-1
- Updated to version 4.3.
- Adding a test BR on "perl(FindBin)".

* Thu Oct 21 2021 Andrew Phelps <anphel@microsoft.com> - 4.2.1-6
- Add additional glibc 2.34 workarounds to glob.c
- License verified

* Mon Oct 19 2020 Andrew Phelps <anphel@microsoft.com> - 4.2.1-5
- Fix check test

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 4.2.1-4
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 4.2.1-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 09 2018 Alexey Makhalov <amakhalov@vmware.com> - 4.2.1-2
- Fix compilation issue against glibc-2.27

* Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> - 4.2.1-1
- Update package version

* Mon Oct 03 2016 ChangLee <changLee@vmware.com> - 4.1-4
- Modified check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.1-3
- GA - Bump release of all rpms

* Tue May 10 2016 Kumar Kaushik <kaushikk@vmware.com> - 4.1-2
- Fix for segfaults in chroot env.

* Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com> - 4.1-1
- Update version.

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> - 4.0-1
- Initial build. First version
