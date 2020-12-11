Summary:        Programs for processing and formatting text
Name:           groff
Version:        1.22.3
Release:        7%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Text
URL:            https://www.gnu.org/software/groff
Source0:        http://ftp.gnu.org/gnu/groff/%{name}-%{version}.tar.gz
# No patch has been made available for CVE-2000-0803
Patch0:         CVE-2000-0803.nopatch
Requires:       perl-DBD-SQLite
Requires:       perl-DBI
Requires:       perl-DBIx-Simple
Requires:       perl-File-HomeDir
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Requires(preun): %{_sbindir}/update-alternatives
Provides:       perl(oop_fh.pl) = %{version}-%{release}
Provides:       perl(main_subs.pl) = %{version}-%{release}
Provides:       perl(man.pl) = %{version}-%{release}
Provides:       perl(subs.pl) = %{version}-%{release}
Provides:       groff-base = %{version}-%{release}

%description
The Groff package contains programs for processing
and formatting text.

%prep
%setup -q

%build
PAGE=letter ./configure \
    --prefix=%{_prefix} \
    --with-grofferdir=%{_datadir}/%{name}/%{version}/groffer
make

%install
install -vdm 755 %{_defaultdocdir}/%{name}-1.22/pdf
make DESTDIR=%{buildroot} install

# rename files for alternative usage
mv %{buildroot}%{_bindir}/soelim %{buildroot}%{_bindir}/soelim.%{name}
touch %{buildroot}%{_bindir}/soelim
mv %{buildroot}%{_mandir}/man1/soelim.1 %{buildroot}%{_mandir}/man1/soelim.%{name}.1
touch %{buildroot}%{_mandir}/man1/soelim.1
mv %{buildroot}%{_mandir}/man7/roff.7 %{buildroot}%{_mandir}/man7/roff.%{name}.7
touch %{buildroot}%{_mandir}/man7/roff.7

# some binaries need alias with 'g' or 'z' prefix
for file in g{nroff,troff,tbl,pic,eqn,neqn,refer,lookbib,indxbib,soelim} zsoelim; do
    ln -s ${file#?} %{buildroot}%{_bindir}/${file}
    ln -s ${file#?}.1.gz %{buildroot}%{_mandir}/man1/${file}.1.gz
done

rm -rf %{buildroot}%{_infodir}

%pre
# remove alternativized files if they are not symlinks
[ -L %{_bindir}/soelim ] || rm -f %{_bindir}/soelim >/dev/null 2>&1 || :
[ -L %{_mandir}/man1/soelim.1.gz ] || rm -f %{_mandir}/man1/soelim.1.gz >/dev/null 2>&1 || :
[ -L %{_mandir}/man7/roff.7.gz ] || rm -f %{_mandir}/man7/roff.7.gz >/dev/null 2>&1 || :

%post
# set up the alternatives files
%{_sbindir}/update-alternatives --install %{_bindir}/soelim soelim %{_bindir}/soelim.%{name} 300 \
    --slave %{_mandir}/man1/soelim.1.gz soelim.1.gz %{_mandir}/man1/soelim.%{name}.1.gz \
    >/dev/null 2>&1 || :
%{_sbindir}/update-alternatives --install %{_mandir}/man7/roff.7.gz roff.7.gz %{_mandir}/man7/roff.%{name}.7.gz 300 \
    >/dev/null 2>&1 || :

%preun
if [ $1 -eq 0 ]; then
    %{_sbindir}/update-alternatives --remove soelim %{_bindir}/soelim.%{name} >/dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove roff.7.gz %{_mandir}/man7/roff.%{name}.7.gz >/dev/null 2>&1 || :
fi

%postun
if [ $1 -ge 1 ]; then
    if [ "$(readlink %{_sysconfdir}/alternatives/soelim)" == "%{_bindir}/soelim.%{name}" ]; then
        %{_sbindir}/update-alternatives --set soelim %{_bindir}/soelim.%{name} >/dev/null 2>&1 || :
    fi
    if [ "$(readlink %{_sysconfdir}/alternatives/roff.7.gz)" == "%{_mandir}/man7/roff.%{name}.7.gz" ]; then
        %{_sbindir}/update-alternatives --set roff.7.gz %{_mandir}/man7/roff.%{name}.7.gz >/dev/null 2>&1 || :
    fi
fi

%files
%defattr(-,root,root)
%license LICENSES
%{_bindir}/*
%{_libdir}/groff/*
%{_defaultdocdir}/%{name}-%{version}/*
%{_datarootdir}/%{name}/*
%{_mandir}/*/*

%changelog
* Fri Dec 11 2020 Joe Schmitt <joschmit@microsoft.com> - 1.22.3-7
- Ship compatibility symlinks.
- Compatibility symlink spec changes imported from Fedora 32 (license: MIT)

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> - 1.22.3-6
- Use new perl package names.
- Provide groff-base.

*   Mon Sep 28 2020 Daniel McIlvaney <damcilva@microsoft.com> 1.22.3-5
-   Nopatch CVE-2000-0803.nopatch

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.22.3-4
-   Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.22.3-3
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.22.3-2
-   GA - Bump release of all rpms

*   Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 1.22.3-1
-   Updated to version 1.22.3

*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.22.2-1
-   Initial build. First version
