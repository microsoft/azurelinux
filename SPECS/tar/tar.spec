Summary:        Archiving program
Name:           tar
Version:        1.35
Release:        1%{?dist}
License:        GPLv3+
URL:            https://www.gnu.org/software/tar
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz

%description
Contains GNU archiving program

%prep
%setup -q
%build
FORCE_UNSAFE_CONFIGURE=1  ./configure \
    --prefix=%{_prefix} \
    --bindir=/bin \
    --disable-silent-rules
make %{?_smp_mflags}

%install
install -vdm 755 %{buildroot}%{_sbindir}
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} -C doc install-html docdir=%{_defaultdocdir}/%{name}-%{version}
ln -sf tar %{buildroot}/bin/gtar
install -vdm 755 %{buildroot}/usr/share/man/man1
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}

%check
make  %{?_smp_mflags} check

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
/bin/tar
/bin/gtar
%{_libexecdir}/rmt
%{_defaultdocdir}/%{name}-%{version}/*
%{_mandir}/*/*

%changelog
* Mon Nov 27 2023 Andrew Phelps <anphel@microsoft.com> - 1.35-1
- Upgrade to version 1.35
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.34-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)
*   Fri Nov 05 2021 Andrew Phelps <anphel@microsoft.com> 1.34-1
-   Update to version 1.34
-   License verified
*   Wed Jul 29 2020 Andrew Phelps <anphel@microsoft.com> 1.32-2
-   Add symlink for gtar.
*   Wed Jun 03 2020 Joe Schmitt <joschmit@microsoft.com> 1.32-1
-   Update to version 1.32 to resolve CVE-2019-9923.
-   Fix macro in changelog.
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.30-4
-   Added %%license line automatically
*   Fri Apr 10 2020 Nick Samson <nisamson@microsoft.com> 1.30-3
-   Updated Source0, updated URL to https, validated license, removed %%define sha1
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.30-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> 1.30-1
-   Update to version 1.30
*   Tue Apr 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.29-1
-   Update to version 1.29.
*   Mon Oct 10 2016 ChangLee <changlee@vmware.com> 1.28-3
-   Modified %%check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.28-2
-   GA - Bump release of all rpms
*   Wed Jan 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.28-1
-   Update to 1.28-1.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.27.1-1
-   Initial build. First version
