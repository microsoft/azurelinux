Name:       rtctl
Version:    1.13
Release:    5%{?dist}
Summary:    Scripts for controlling scheduling priorities of system threads
Group:      Applications/System
License:    GPL
BuildArch:  noarch
Source0:    %{_mariner_sources_url}/rtctl-%{version}.tar.bz2
BuildRoot:  %{_tmppath}/%{name}-%{version}-build

%description
rtctl is a set of scripts used to manipulate the scheduling priorities of
groups of system threads.

%prep
%setup -q

%build
make

%install
rm -rf $RPM_BUILD_ROOT
make DEST=$RPM_BUILD_ROOT install

%files
%defattr(-,root,root,-)
%attr(0755, root, root) /usr/sbin/rtctl
%attr(0755, root, root) /usr/bin/rtctl_wrapper
%config(noreplace) /etc/rtgroups
%config(noreplace) /etc/sysconfig/rtctl
/etc/systemd/system/rtctl.service
/usr/share/man/man1/rtctl.1.gz
/usr/share/man/man5/rtgroups.5.gz

%post
systemctl enable rtctl

%preun
if [ "$1" = "0" ] ; then # uninstall
systemctl disable rtctl
fi

%changelog
* Wed Apr 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.13-5
- Updating source URL.

* Thu Jan 20 2022 Cameron Baird <cameronbaird@microsoft.com> 1.13-4
- Initial CBL-Mariner import from CentOS 8 (license: MIT).
- Remove %%clean stage
- License verified

* Tue Mar 09 2021 Hernan Gatta <hegatta@microsoft.com> - 1.13-3
- Initial import into ECF Mariner from CentOS 8 (License: GPL)

* Mon Dec 29 2014 Luis Claudio R. Goncalves <lgoncalv@redhat.com> - 1.13-2
- adjusted startup script messages (1162768)

* Tue Dec 23 2014 Luis Claudio R. Goncalves <lgoncalv@redhat.com> - 1.13-1
- make startup logic compatible with systemd (1162768)
- product name cleanup (1173311)

* Fri Sep 12 2014 Luis Claudio R. Goncalves <lgoncalv@redhat.com> - 1.12-4
- rtctl for RHEL-RT
