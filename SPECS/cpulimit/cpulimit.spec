# vim: set sw=4 ts=4 et nu:
#
# spec file for package cpulimit
#
# Copyright (c) 2022 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Summary:        Limit the CPU Usage of a Process
Name:           cpulimit
Version:        3.0
Release:        1%{?dist}
License:        GPL-2.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Monitoring
URL:            https://limitcpu.sourceforge.net/
Source0:        https://downloads.sourceforge.net/limitcpu/%{name}-%{version}.tar.gz
Patch0:         %{name}-2.8-do_not_forget_version.patch
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make

%description
LimitCPU is a program to throttle the CPU cycles used by other applications.
LimitCPU will monitor a process and make sure its CPU usage stays at or
below a given percentage. This can be used to make sure your system
has plenty of CPU cycles available for other tasks. It can also be used
to keep laptops cool in the face of CPU-hungry processes and for limiting
virtual machines.

LimitCPU is the direct child of CPUlimit, a creation of Angelo Marletta,
which can be found at http://cpulimit.sourceforge.net

%prep
%autosetup -p1

%build
%make_build \
    CFLAGS="%{optflags}"

%install
%make_install PREFIX=%{buildroot}/%{_prefix}

%files
%license LICENSE
%doc CHANGELOG README
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0-1
- Auto-upgrade to 3.0 - Azure Linux 3.0 - package upgrades

* Fri Jan 27 2023 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.8-2
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- License Verified
- Converted the 'Release' tag to the '[number].[distribution]' format.
- Renamed patch version to 2.8 from 2.2 to match with SPEC version.

* Thu Dec 29 2022 Dirk Müller <dmueller@suse.com>
- update to 2.8:
  * Made exit message when child signal is caught only show up
  when in verbose mode.
  * Adjusted the way the VERSION value is assigned in the Makefile.
  CFLAGS was being overwritten by Debian's build process.

* Mon Dec 20 2021 Dirk Müller <dmueller@suse.com>
- update to 2.7:
  * Fixed compiler warnings regarding string lengths.

* Tue Aug 25 2020 Dirk Mueller <dmueller@suse.com>
- update to 2.6:
  * Fixed indentation to avoid compiler warnings. No functional change.
  * Updated manual page to warn against using -m on a script.

* Sun Feb 18 2018 avindra@opensuse.org
- new upstream version 2.5
  * Added some protection against causing a fork bomb when the
    throttled process is a parent to LimitCPU.
- includes 2.4
  * Introduced ability to watch children of the target process. This
    means forks of the process we are throttling can also be
    throttled, using the "-m" or "--monitor-forks" flags.
- includes 2.3
  * Applied patch to man page which fixes -s description.
  * Added --foreground, -f flag for launching target programs in the
    foreground. LimitCPU then waits for the target process to exit.
    Should be useful in scripts.
- rebase cpulimit-2.2-do_not_forget_version.patch
- cleanup with spec-cleaner

* Fri Dec 26 2014 andrea@opensuse.org
- new upstream version 2.2
  + Escaped double-dashed in manual page to avoid
  warnings from Debian check tool.
  + Added -s --signal flag. This flag allows the user to
  specify an alternative signal to send a watched process
  when cpulimit terminates. By default we send SIGCONT.
  The -s flag can accept a number (1-35) or a written
  value such as SIGCONT, SIGSTOP, SIGINT, SIGTERM.
- from version 2.1
  + Added the --quiet (-q) flag to make
  limitcpu run silently
  + Make sure error messages are printed to stderr.
  + Placed source code in Subversion (svn) repository.
  Accessable using the SVN checkout command. For
  details, please see the README file.
- from version 2.0
  + Added the -- flag to make sure child processes
  run with command line flags would not confuse
  cpulimit.
  + Corrected output of child process name in verbose mode.
- added cpulimit-2.2-do_not_forget_version.patch

* Wed Jul 24 2013 malcolmlewis@opensuse.org
- Updated to version 1.9:
  + Added --kill (-k) and --restore (-r) flags to allow target
    processes to be killed and restored rather than simply
    throttled.
- Updates from version 1.8:
  + When displaying verbose output, cpulimit now redisplays the
    column headers every 20 lines.
  + Fixed limiting CPU usage on multicore machines when the desired
    usage limit is great than 100%%.

* Fri Aug 24 2012 devel.openSUSE.org@gmail.com
- Upstream update to version 1.7:
  * Minor code cleanup.
  * Make sure we do not try to throttle our own process.
  * Added "tarball" option to the Makefile to assist
    in packaging. Moved version number to the makefile.
  * Added version information to CPUlimit's help screen.
  * Detect the number of CPU cores on the machine and
    cap the %% we can limit. 1 CPU means we can
    limit processes 1-100%%, 2 means 1-200%%, 4 means 1-400%%.
  * Removed extra priority changes. We now only bump
    our priority once, if we have access to do so.
    Also simplified priority increases so it's flexible
    rather than "all or nothing".
  * Since we now attempt to detect the number of CPUs
    available, we also give the user the ability to
    override our guess. The -c and --cpu flags have
    been added for this purpose.
  * Commands can be launched and throttled by appending
    commands to the end of CPUlimit's argument list. For
    example:
    cpulimit -l 25 firefox

* Tue May 17 2011 pascal.bleser@opensuse.org
- initial version (1.3)
