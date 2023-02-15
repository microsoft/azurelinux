Summary:       CBL-Mariner release files
Name:          mariner-release
Version:       1.0
Release:       56%{?dist}
License:       MIT
Group:         System Environment/Base
URL:           https://aka.ms/cbl-mariner
Vendor:        Microsoft Corporation
Distribution:  Mariner
BuildArch:     noarch

# Allows package management tools to find and set the default value
# for the "releasever" variable from the RPM database.
Provides: system-release(releasever)

%description
Azure CBL-Mariner release files such as yum configs and other /etc/ release related files

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc
install -d $RPM_BUILD_ROOT/usr/lib

echo "CBL-Mariner %{mariner_release_version}" > %{buildroot}/etc/mariner-release
echo "MARINER_BUILD_NUMBER=%{mariner_build_number}" >> %{buildroot}/etc/mariner-release

cat > %{buildroot}/etc/lsb-release <<- "EOF"
DISTRIB_ID="Mariner"
DISTRIB_RELEASE="%{mariner_release_version}"
DISTRIB_CODENAME=Mariner
DISTRIB_DESCRIPTION="CBL-Mariner %{mariner_release_version}"
EOF

version_id=`echo %{mariner_release_version} | grep -o -E '[0-9]+.[0-9]+' | head -1`
cat > %{buildroot}/usr/lib/os-release << EOF
NAME="Common Base Linux Mariner"
VERSION="%{mariner_release_version}"
ID=mariner
VERSION_ID="$version_id"
PRETTY_NAME="CBL-Mariner/Linux"
ANSI_COLOR="1;34"
HOME_URL="%{url}"
BUG_REPORT_URL="%{url}"
SUPPORT_URL="%{url}"
EOF

ln -sv ../usr/lib/os-release %{buildroot}/etc/os-release

cat > %{buildroot}/etc/issue <<- EOF
Welcome to CBL-Mariner %{mariner_release_version} (%{_arch}) - Kernel \r (\l)
EOF

cat > %{buildroot}/etc/issue.net <<- EOF
Welcome to CBL-Mariner %{mariner_release_version} (%{_arch}) - Kernel %r (%t)
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/mariner-release
%config(noreplace) /etc/lsb-release
%config(noreplace) /usr/lib/os-release
%config(noreplace) /etc/os-release
%config(noreplace) /etc/issue
%config(noreplace) /etc/issue.net

%changelog
*   Tue Feb 14 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.0-56
-   Updating version for February update 2.
*   Tue Feb 07 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.0-55
-   Updating version for February update.
*   Fri Jan 20 2023 Riken Maharjan <rmaharjan@microsoft.com> - 1.0-54
-   Updating version for January update 2.
*   Thu Jan 05 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.0-53
-   Updating version for January update.
*   Mon Dec 19 2022 Jon Slobodzian <joslobo@microsoft.com> - 1.0-52
-   Updating version for December update 3.
*   Mon Dec 12 2022 Jon Slobodzian <joslobo@microsoft.com> - 1.0-51
-   Updating version for December update 2.
*   Thu Dec 01 2022 Jon Slobodzian <joslobo@microsoft.com> - 1.0-50
-   Updating version for December update.
*   Wed Nov 09 2022 Jon Slobodzian <joslobo@microsoft.com> - 1.0-49
-   Updating version for November update.
*   Fri Oct 21 2022 Jon Slobodzian <joslobo@microsoft.com> - 1.0-48
-   Updating version for October update 2
*   Thu Oct 06 2022 Jon Slobodzian <joslobo@microsoft.com> - 1.0-47
-   Updating version for October update.
*   Fri Sep 23 2022 Jon Slobodzian <joslobo@microsoft.com> - 1.0-46
-   Updating version for September update 2.
*   Fri Sep 09 2022 Jon Slobodzian <joslobo@microsoft.com> - 1.0-45
-   Updating version for September update.
*   Tue Aug 16 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-44
-   Updating version for August update 2.
*   Wed Aug 04 2022 Andrew Phelps <anphel@microsoft.com> - 1.0-43
-   Updating version for August update.
*   Fri Jul 08 2022 Jon Slobodzian <joslobo@microsoft.com> - 1.0-42
-   Updating version for July Update.
*   Tue Jun 07 2022 Jon Slobodzian <joslobo@microsoft.com> - 1.0-41
-   Updating version for June update.
*   Fri May 20 2022 Jon Slobodzian <joslobo@microsoft.com> - 1.0-40
-   Updating version for May update.
*   Sat Apr 09 2022 Jon Slobodzian <joslobo@microsoft.com> - 1.0-39
-   Updating version for April update.
*   Wed Mar 30 2022 Jon Slobodzian <joslobo@microsoft.com> - 1.0-38
-   Updating version for March update 3.
*   Tue Mar 15 2022 Jon Slobodzian <joslobo@microsoft.com> - 1.0-37
-   Updating version for March update 2.
*   Sat Mar 05 2022 Jon Slobodzian <joslobo@microsoft.com> - 1.0-36
-   Updating version for March update.
*   Fri Feb 25 2022 Jon Slobodzian <joslobo@microsoft.com> - 1.0-35
-   Updating version for February update 2.
*   Thu Feb 24 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-34
-   Surrounding 'VERSION_ID' inside 'os-release' with double quotes.
*   Mon Feb 07 2022 Jon Slobodzian <joslobo@microsoft.com> - 1.0-33
-   Updating version for February update.
*   Wed Jan 26 2022 Jon Slobodzian <joslobo@microsoft.com> - 1.0-32
-   Updating version for January update-2 (CVE-2022-0185 and CVE-2021-4034)
*   Sat Jan 15 2022 Jon Slobodzian <joslobo@microsoft.com> - 1.0-31
-   Updating version for January update.
*   Wed Jan 12 2022 Jon Slobodzian <joslobo@microsoft.com> - 1.0-30
-   Updating version for January update.
*   Wed Dec 22 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-29
-   Updating version for December update.
*   Thu Nov 25 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-28
-   Updating version for November update.
*   Thu Nov 25 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-27
-   Updating version for November update.
*   Thu Nov 11 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-27
-   Updating version for off-cycle post-October update to fix kernel CVE
*   Fri Nov 05 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-26
-   Updating version for off-cycle post-October update to fix vim CVE and update glibc to patch 
-   dotnet/glibc garbage collector issue (pthread_cond_signal failed to wake up pthread_cond_wait)
*   Wed Nov 03 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-25
-   Updating version for off-cycle post-October update to service toolchain CVE's and miscellaneous bug fixes.
*   Tue Oct 26 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-24
-   Updating version for October update.
*   Tue Sep 28 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-23
-   Updating version for September update.
*   Mon Aug 30 2021 Mateusz Malisz <mamalisz@microsoft.com> - 1.0-22
-   Updating version for August update.
*   Thu Aug 19 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-21
-   Off-cycle update for Kernel CVE's
*   Fri Jul 23 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-20
-   Updating version for July update
*   Fri Jun 25 2021 Andrew Phelps <anphel@microsoft.com> - 1.0-19
-   Updating version for June update
*   Thu Jun 15 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-18
-   Updating version for Mid-May update to fix ISO boot issue.
*   Thu Jun 3 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-17
-   Updating version for May update
*   Wed Apr 27 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-16
-   Updating version for April update
*   Tue Mar 30 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-15
-   Updating version for March update
*   Mon Feb 22 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-14
-   Updating version for February update
*   Sun Jan 24 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0-13
-   Updating version for January update
*   Mon Dec 21 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-12
-   Updating version for December update.
*   Fri Nov 20 2020 Nicolas Guibourge <nicolasg@microsoft.com> - 1.0-11
-   Updating version for November update
*   Sat Oct 24 2020 Jon Slobodzian <joslobo@microsoft.com> - 1.0-10
-   Updating version for October update
*   Fri Sep 04 2020 Mateusz Malisz <mamalisz@microsoft.com> - 1.0-9
-   Remove empty %%post section, dropping dependency on /bin/sh
*   Tue Aug 24 2020 Jon Slobodzian <joslobo@microsoft.com> - 1.0-8
-   Changing CBL-Mariner ID from "Mariner" to "mariner" to conform to standard.  Also updated Distrib-Description and Name per internal review.
*   Tue Aug 18 2020 Jon Slobodzian <joslobo@microsoft.com> - 1.0-7
-   Restoring correct Name, Distribution Name, CodeName and ID.
*   Fri Jul 31 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-6
-   Updating distribution name.
*   Wed Jul 29 2020 Nick Samson <nisamson@microsoft.com> - 1.0-5
-   Updated os-release file and URL to reflect project naming
*   Wed Jun 24 2020 Jon Slobodzian <joslobo@microsoft.com> - 1.0-4
-   Updated license for 1.0 release.
*   Mon May 04 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-3
-   Providing "system-release(releasever)" for the sake of DNF
-   and other package management tools.
*   Thu Jan 30 2020 Jon Slobodzian <joslobo@microsoft.com> 1.0-2
-   Remove Microsoft name from distro version.
*   Wed Sep 04 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.0-1
-   Original version for CBL-Mariner.
