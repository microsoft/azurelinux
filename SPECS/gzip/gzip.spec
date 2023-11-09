Summary:        Programs for compressing and decompressing files
Name:           gzip
Version:        1.13
Release:        1%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/File
URL:            https://www.gnu.org/software/gzip
Source0:        https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
%if %{with_check}
BuildRequires:  less
%endif

%description
The Gzip package contains programs for compressing and
decompressing files.

%prep
%setup -q

%build
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}%{_bindir}
rm -rf %{buildroot}%{_infodir}

# In most distros, the "uncompress" name is shipped as part of ncompress
# This an alias to gunzip
rm -f %{buildroot}%{_bindir}/uncompress

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.13-1
- Auto-upgrade to 1.13 - Azure Linux 3.0 - package upgrades

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.12-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue Sep 20 2022 Betty Lakes <bettylakes@microsoft.com> - 1.12-1
- Upgrade to 1.12

* Fri Oct 22 2021 Andrew Phelps <anphel@microsoft.com> - 1.11-1
- Update to version 1.11

* Mon May 17 2021 Thomas Crain <thcrain@microsoft.com> - 1.9-6
- Stop packaging 'uncompress' binary alias
- Lint spec
- Update URLs to secure variants
- License verified

* Tue Oct 20 2020 Andrew Phelps <anphel@microsoft.com> - 1.9-5
- Fix check test

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.9-4
- Added %%license line automatically

* Fri Mar 03 2020 Jon Slobodzian <joslobo@microsoft.com> - 1.9-3
- Fixed reference URL. Verified license.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.9-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> - 1.9-1
- Update to version 1.9

* Sat Sep 08 2018 Alexey Makhalov <amakhalov@vmware.com> - 1.8-2
- Fix compilation issue against glibc-2.28

* Fri Mar 24 2017 Dheeraj Shetty <dheerajs@vmware.com> - 1.8-1
- Upgrading to version 1.8

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.6-2
- GA - Bump release of all rpms

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> - 1.6-1
- Initial build. First version
