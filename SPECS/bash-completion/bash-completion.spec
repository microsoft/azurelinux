Name:          bash-completion
Version:       2.11
Release:       1%{?dist}
Summary:       Programmable completion for bash
Group:         Applications/Shells
Vendor:        Microsoft Corporation
Distribution:  Mariner
URL:           https://github.com/scop/bash-completion
Source0:       https://github.com/scop/%{name}/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
License:       GPLv2+

Requires:      bash
Requires:      %{name}-devel = %{version}-%{release}
%global debug_package %{nil}

%description
bash-completion is a collection of shell functions that take advantage of the programmable completion feature of bash 2.04 and later.

%package devel
Group:         Development/Libraries
Summary:       Development files for %{name}
Requires:      %{name} = %{version}-%{release}

%description devel
This package contains files need for development.

%prep
%setup -q

%build
autoreconf -f -i
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -d %{buildroot}%{_sysconfdir}/profile.d
install -m644 bash_completion.sh %{buildroot}%{_sysconfdir}/profile.d/

# provided in udev since 198
rm -f %{buildroot}%{_datadir}/bash-completion/completions/udevadm

rm -f %{buildroot}%{_sysconfdir}/profile.d/bash_completion.sh
rm -f %{buildroot}%{_datadir}/bash-completion/bash_completion
rm -f %{buildroot}%{_datadir}/bash-completion/completions/rfkill

# provided in NetworkManager
rm -f %{buildroot}%{_datadir}/bash-completion/completions/nmcli

# provided in util-linux
rm -f %{buildroot}%{_datadir}/bash-completion/completions/\
{cal,chsh,dmesg,eject,hexdump,ionice,hwclock,ionice,look,mount,renice,rtcwake,su,umount}

%files
%defattr(-,root,root)
%license COPYING
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/*
%dir %{_datadir}/bash-completion/helpers
%{_datadir}/bash-completion/helpers/perl
%{_datadir}/bash-completion/helpers/python
%doc AUTHORS COPYING

%files devel
%defattr(-,root,root)
%dir %{_datadir}/cmake/bash-completion
%{_datadir}/cmake/bash-completion/bash-completion-config*.cmake
%{_datadir}/pkgconfig/bash-completion.pc

%changelog
* Mon Jan 10 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 2.11-1
- Upgrade to 2.11.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.7-5
- Removing the explicit %%clean stage.

* Wed Oct 27 2021 Muhammad Falak <mwani@microsft.com> - 2.7-4
- Remove epoch

* Mon Mar 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.7-3
- Require devel subpackage from base package for compatibility with other distros

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.7-2
- Added %%license line automatically

* Wed Mar 18 2020 Emre Girgin <mrgirgin@microsoft.com> - 2.7-1
- Version update to 2.7. License verified.

* Wed Oct 9 2019 Andrew Phelps <anphel@microsoft.com> - 2.5-1
- Initial CBL-Mariner import from OpenMamba

* Tue Feb 07 2017 Automatic Build System <autodist@mambasoft.it> - 2.5-1mamba
- automatic version update by autodist

* Wed Sep 07 2016 Automatic Build System <autodist@mambasoft.it> - 2.4-1mamba
- automatic version update by autodist

* Sun May 22 2016 Silvan Calarco <silvan.calarco@mambasoft.it> - 2.3-2mamba
- remove mount and umout provided in util-linux >= 2.28

* Sat Apr 30 2016 Silvan Calarco <silvan.calarco@mambasoft.it> - 2.3-1mamba
- update to 2.3

* Wed Sep 03 2014 Silvan Calarco <silvan.calarco@mambasoft.it> - 2.1-6mamba
- previous patch had not been applied

* Sat Aug 02 2014 Silvan Calarco <silvan.calarco@mambasoft.it> - 2.1-5mamba
- fix patch for bash 4.3
- remove conclicting files for chsh provided by latest util-linux

* Mon May 05 2014 Silvan Calarco <silvan.calarco@mambasoft.it> - 2.1-4mamba
- patch against bash 4.3 (see https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=741479)

* Mon Apr 29 2013 Silvan Calarco <silvan.calarco@mambasoft.it> - 2.1-3mamba
- remove completion files conflicting with util-linux since 2.23

* Mon Apr 15 2013 Silvan Calarco <silvan.calarco@mambasoft.it> - 2.1-2mamba
- remove nmcli completion already provided by NetworkManager

* Sun Apr 14 2013 Automatic Build System <autodist@mambasoft.it> - 2.1-1mamba
- update to 2.1

* Sun Mar 17 2013 Silvan Calarco <silvan.calarco@mambasoft.it> - 2.0-2mamba
- remove udevadm completion file provided by udev >= 198

* Wed Aug 15 2012 Automatic Build System <autodist@mambasoft.it> - 2.0-1mamba
- update to 2.0

* Thu May 10 2012 Silvan Calarco <silvan.calarco@mambasoft.it> - 1.99-1mamba
- update to 1.99

* Thu Aug 25 2011 Silvan Calarco <silvan.calarco@mambasoft.it> - 1.3-1mamba
- update to 1.3

* Wed Feb 02 2011 Davide Madrisan <davide.madrisan@gmail.com> - 1.2-1mamba
- update url
- remove files not applicable to openmamba
- add upstream patch for rpm

* Tue Feb 01 2011 Silvan Calarco <silvan.calarco@mambasoft.it> - 20060301-3mamba
- remove unuseful %dir to fix a self installation loop

* Fri Sep 26 2008 Silvan Calarco <silvan .calarco@mambasoft.it> - 20060301-2mamba
- fix installation of /etc/bash_completion
- add bash_completion.sh in /etc/profile.d
- install contrib file in /etc/bash_completion.d

* Tue Sep 23 2008 Ercole 'ercolinux' Carpanetto <ercole69@gmail.com> - 20060301-1mamba
- package created by autospec
