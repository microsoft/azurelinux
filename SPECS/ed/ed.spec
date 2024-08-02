%global use_llvm_clang %{nil}
%global use_llvm_linker %{nil}
%global __spec_prep_template \
%{__spec_prep_pre}\
%{nil}
%global __spec_build_template \
%{__spec_build_pre}\
%{set_build_flags}\
%{nil}

Summary:        Ed - A line-oriented text editor
Name:           ed
Version:        1.20
Release:        1%{?dist}
URL:            https://www.gnu.org/software/ed/
License:        GPLv3
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# We don't have lzip to decompress it. Hence converted to tar.gz
Source0:        https://ftp.gnu.org/gnu/ed/ed-1.20.tar.lz#/%{name}-%{version}.tar.gz
# CVE-2015-2987 applies to a different program named ED
Patch0:         CVE-2015-2987.nopatch

%description
Ed - A line-oriented text editor

%prep
%autosetup -p1

%build
./configure \
    --prefix=%{_prefix}
make V=1 %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}%{_libdir}

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
* Wed Feb 07 2024 Joe Schmitt <joschmit@microsoft.com> - 1.20-1
- Upgrade to version 1.20

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 1.14.2-9
- Replace incorrect %%{_lib} usage with %%{_libdir}

*   Wed Oct 14 2020 Henry Beberman <henry.beberman@microsoft.com> 1.14.2-8
-   Nopatch CVE-2015-2987. Applies to a different program named ed.
-   Switch setup to autosetup
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
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Sep 27 2018 Sujay G <gsujay@vmware.com> 1.14.2-1
-   Initial build.
