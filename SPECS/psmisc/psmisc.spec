Summary:        Displays information about running processes
Name:           psmisc
Version:        23.6
Release:        1%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            http://psmisc.sourceforge.net/
Source0:        http://prdownloads.sourceforge.net/psmisc/%{name}-%{version}.tar.xz
BuildRequires:  ncurses-devel
Requires:       ncurses

%description
The Psmisc package contains programs for displaying information
about running processes.

%prep
%setup -q

%build
./configure \
	--prefix=%{_prefix}
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/bin
mv -v %{buildroot}%{_bindir}/fuser   %{buildroot}/bin
mv -v %{buildroot}%{_bindir}/killall %{buildroot}/bin
%find_lang %{name}

%check
make %{?_smp_mflags} check

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
/bin/*
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 23.6-1
- Auto-upgrade to 23.6 - Azure Linux 3.0 - package upgrades

* Wed Nov 10 2021 Chris Co <chrco@microsoft.com> - 23.4-1
- Update to 23.4
- Fix lint
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 23.2-4
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 23.2-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Oct 2 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> - 23.2-2
- Updated the tarball for v23.2

* Mon Sep 10 2018 Alexey Makhalov <amakhalov@vmware.com> - 23.2-1
- Version update to fix compilation issue againts glibc-2.28

* Mon Oct 03 2016 ChangLee <changLee@vmware.com> - 22.21-5
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 22.21-4
- GA - Bump release of all rpms

* Thu Apr 28 2016 Anish Swaminathan <anishs@vmware.com> - 22.21-3
- Add patch for incorrect fclose in pstree

* Fri Mar 11 2016 Kumar Kaushik <kaushikk@vmware.com> - 22.21-2
- Adding patch for type in fuser binary.

* Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com> - 22.21-1
- Update version

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> - 22.20-1
- Initial build. First version
