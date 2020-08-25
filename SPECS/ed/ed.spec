Summary:        Ed - A line-oriented text editor
Name:           ed
Version:        1.14.2
Release:        7%{?dist}
URL:            https://www.gnu.org/software/ed/
License:        GPLv3
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
# Official source under https://ftp.gnu.org/gnu/ed/ed-1.14.2.tar.lz.
# We don't have lzip to decompress it.
Source0:        https://src.fedoraproject.org/repo/pkgs/%{name}/%{name}-%{version}.tar.xz/sha512/de838a6df785c7dc80f4b5ba84330bbe743983fd81218321d4ab84c4c3688fdafb4c005502f3228f0bfa2b6bcf342d64d9523ab73ee440b4f305a033f567cbc2/%{name}-%{version}.tar.xz
%description
Ed - A line-oriented text editor

%prep
%setup -q

%build
./configure \
    --prefix=%{_prefix}
make V=1 %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}%{_lib}

rm -rf %{buildroot}%{_infodir}/dir

%check
make  %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/ed
%{_bindir}/red
%{_infodir}/ed.info.gz
%{_mandir}/man1/*

%changelog
*   Wed Aug 05 2020 Andrew Phelps <anphel@microsoft.com> 1.14.2-7
-   Remove conflicting 'dir' file from _infodir
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.14.2-6
-   Added %%license line automatically
*   Mon Apr 27 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.14.2-5
-   Fixed 'Source0' and 'URL' tags.
-   License verified.
*   Mon Mar 30 2020 Chris Co <chrco@microsoft.com> 1.14.2-4
-   Fix changelog to not inadvertently define a sha1 macro
*   Thu Mar 26 2020 Chris Co <chrco@microsoft.com> 1.14.2-3
-   Delete invalid ed-devel package
-   Delete unused sha1
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.14.2-2
-   Initial CBL-Mariner import from Photon (license: dual Apache2/GPL2).
*   Thu Sep 27 2018 Sujay G <gsujay@vmware.com> 1.14.2-1
-   Initial build.
