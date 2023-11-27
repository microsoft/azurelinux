Summary:        Programs for processing and formatting text
Name:           groff
Version:        1.23.0
Release:        1%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Text
URL:            https://www.gnu.org/software/groff/
Source0:        https://ftp.gnu.org/gnu/groff/%{name}-%{version}.tar.gz
# No patch has been made available for CVE-2000-0803
Patch0:         CVE-2000-0803.nopatch
Requires:       perl-DBD-SQLite
Requires:       perl-DBI
Requires:       perl-DBIx-Simple
Requires:       perl-File-HomeDir
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Provides:       perl(oop_fh.pl) = %{version}-%{release}
Provides:       perl(main_subs.pl) = %{version}-%{release}
Provides:       perl(man.pl) = %{version}-%{release}
Provides:       perl(subs.pl) = %{version}-%{release}
Provides:       groff-base = %{version}-%{release}
AutoReq:        no

%description
The Groff package contains programs for processing
and formatting text.

%prep
%setup -q

%build
PAGE=letter ./configure \
    --prefix=%{_prefix} \
    --with-grofferdir=%{_datadir}/%{name}/%{version}/groffer \
    --without-x
make

%install
install -vdm 755 %{_defaultdocdir}/%{name}-1.22/pdf
make DESTDIR=%{buildroot} install

# some binaries need alias with 'g' or 'z' prefix
for file in g{nroff,troff,tbl,pic,eqn,neqn,refer,lookbib,indxbib,soelim} zsoelim; do
    ln -s ${file#?} %{buildroot}%{_bindir}/${file}
    ln -s ${file#?}.1.gz %{buildroot}%{_mandir}/man1/${file}.1.gz
done

rm -rf %{buildroot}%{_infodir}

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSES
%{_bindir}/*
%{_libdir}/groff/*
%{_defaultdocdir}/%{name}-%{version}/*
%{_datarootdir}/%{name}/*
%{_mandir}/*/*

%changelog
* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.23.0-1
- Auto-upgrade to 1.23.0 - Azure Linux 3.0 - package upgrades

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.22.4-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Sat Nov 20 2021 Chris Co <chrco@microsoft.com> - 1.22.4-1
- Update to 1.22.4
- License verified

* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.22.3-7
- Adding Fedora's symbolic links to provide the same set of file paths.

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> - 1.22.3-6 (from dev branch)
- Use new perl package names.
- Provide groff-base.

* Mon Oct 05 2020 Daniel Burgener <daburgen@microsoft.com> - 1.22.3-6 (from 1.0 branch)
- Ensure build without X11 support
- Don't automatically add requirements when built in the toolchain

* Mon Sep 28 2020 Daniel McIlvaney <damcilva@microsoft.com> - 1.22.3-5
- Nopatch CVE-2000-0803.nopatch

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.22.3-4
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.22.3-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.22.3-2
- GA - Bump release of all rpms

* Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> - 1.22.3-1
- Updated to version 1.22.3

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> - 1.22.2-1
- Initial build. First version
