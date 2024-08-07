Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# crash core analysis suite
#
Summary: ptdump extension module for the crash utility
Name: crash-ptdump-command
Version: 1.0.7
Release: 3%{?dist}
License: GPLv2
Group: Development/Debuggers
Source: https://github.com/crash-utility/crash-extensions/blob/master/ptdump-%{version}.tar.gz
URL: https://crash-utility.github.io/extensions.html
ExclusiveOS: Linux
ExclusiveArch: x86_64
Buildroot: %{_tmppath}/%{name}-root
BuildRequires: crash-devel >= 5.1.5
Requires: crash >= 5.1.5
Patch0: rhel8_build.patch

%description
Retrieve and decode the log buffer generated by the Intel(R) Processor
Trace facility

%prep
%setup -q -n ptdump-%{version}
%patch 0 -p1 -b rhel8_build.patch

%build
make -f ptdump.mk ARCH=SUPPORTED TARGET=X86_64 TARGET_CFLAGS=

%install
rm -Rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_libdir}/crash/extensions/
cp %{_builddir}/ptdump-%{version}/ptdump.so %{buildroot}%{_libdir}/crash/extensions/

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/crash/extensions/ptdump.so

%changelog
* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.7-3
- Removing the explicit %%clean stage.
- License verified.

* Sun Jul 25 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0.7-2
- Initial CBL-Mariner import from CentOS 8 (license: MIT).
- Modified spec to provide architecture arguments to make

* Wed Jul 8 2020 Bhupesh Sharma <bhsharma@redhat.com> - 1.0.7-1
- ptdump: Rebase to upstream extension version ptdump-1.0.7 (github)
  Resolves: rhbz#1851749

* Wed Jan 29 2020 Dave Anderson <anderson@redhat.com> - 1.0.3-5
- ptdump: fix build warning: warning: this ‘if’ clause does not guard
- ptdump: fix failure: ptdump: invalid size request: 0 type: "read page for write" 
- ptdump: fix heap memory and fd leak when fault happens
  Resolves: rhbz#1786497

* Wed Sep 19 2018 Dave Anderson <anderson@redhat.com> - 1.0.3-4
- Address annocheck link issue
  Resolves: rhbz#1630557

* Mon Aug 13 2018 Dave Anderson <anderson@redhat.com> - 1.0.3-3
- Bump release for mass rebuild
  Resolves: rhbz#1615510

* Wed May 31 2017 Dave Anderson <anderson@redhat.com> - 1.0.3-2.el7
- Add RPM_OPT_FLAGS to gcc line in ptdump.mk
  Resolves: rhbz#1450708
- Set gdb scope to get appropriate ring_buffer structure
  Resolves: rhbz#1451181

* Tue Mar 15 2016 Dave Anderson <anderson@redhat.com> - 1.0.3-1.el7
- Fix for coverity scan issues generated by 1.0.2
  Resolves: rhbz#1298172

* Mon Mar 14 2016 Dave Anderson <anderson@redhat.com> - 1.0.2-1.el7
- Memory leak fix and coverity scan fixes.
  Resolves: rhbz#1298172

* Mon Feb 29 2016 Dave Anderson <anderson@redhat.com> - 1.0.1-1.el7
- Initial check-in.
  Resolves: rhbz#1298172

* Tue Jan 26 2016 MUNEDA Takahiro <muneda.takahiro@jp.fujitsu.com> - 1.0.1-1
- Initial crash-ptdump-command package
