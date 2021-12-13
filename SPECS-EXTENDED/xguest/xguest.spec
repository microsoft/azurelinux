Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary: Creates xguest user as a locked down user 
Name: xguest
Version: 1.0.10
Release: 42%{?dist}
License: GPLv2+
BuildArch: noarch
Source: http://people.fedoraproject.org/~dwalsh/xguest/%{name}-%{version}.tar.bz2
URL: http://people.fedoraproject.org/~dwalsh/xguest/

Requires(pre): pam >= 0.99.8.1-17 selinux-policy-targeted > 3.6.3-12
Requires(pre): policycoreutils-sandbox

%description
Installing this package sets up the xguest user to be used as a temporary
account to switch to or as a kiosk user account. The account is disabled unless
SELinux is in enforcing mode. The user is only allowed to log in via graphical login program.
The home and temporary directories of the user will be polyinstantiated and
mounted on tmpfs.

%prep
%setup -q

%build

%install
%{__rm} -fR %{buildroot}
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/security/namespace.d/
%{__mkdir} -p %{buildroot}/var/lib/xguest/home
install -m0644 xguest.conf %{buildroot}/%{_sysconfdir}/security/namespace.d/

%post
if [ $1 -eq 1 ]; then
semanage user -a  -S targeted -P xguest -R xguest_r xguest_u  2> /dev/null  || :
(useradd -c "Guest" -Z xguest_u -d /var/lib/xguest/home/xguest xguest || semanage login -a -S targeted -s xguest_u xguest || semanage login -m -S targeted -s xguest_u xguest) 2>/dev/null || exit 1
head -c 32  /dev/urandom | passwd xguest --stdin

echo "xguest:exclusive" >> /etc/security/sepermit.conf

semanage -S targeted -i - << _EOF
boolean -m --on allow_polyinstantiation 
boolean -m --on xguest_connect_network
boolean -m --on xguest_mount_media
boolean -m --on xguest_use_bluetooth
_EOF
fi

%files
%{_sysconfdir}/security/namespace.d/xguest.conf
%doc README LICENSE
%dir /var/lib/xguest/home
%dir /var/lib/xguest

%preun
if [ $1 -eq 0 ]; then
sed -i '/^xguest/d' /etc/security/sepermit.conf

fi

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.10-42
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jun 16 2016 Lukas Vrabec <lvrabec@redhat.com> - 1.0.10-34
- Security fix for CVE-2016-4980

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 26 2013 Dan Walsh <dwalsh@redhat.com> - 1.0.10-30
- Add random password so xguest will show up in gdm.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Dan Walsh <dwalsh@redhat.com> - 1.0.10-28
- Remove sabayon support from xguest, no longer supported.
- Remove /etc/skel directories

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 14 2013 Dan Walsh <dwalsh@redhat.com> - 1.0.10-26
- Remove /etc/security/namespace.d from payload 

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 2 2012 Dan Walsh <dwalsh@redhat.com> - 1.0.10-4
- Remove Requirement for gdm
- Fix xguest entry in /etc/shadow so gdm lists it

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 7 2011 Dan Walsh <dwalsh@redhat.com> - 1.0.10-2
- Change xguest homedir to be /var/lib/xguest/home/xguest

* Fri Sep 23 2011 Dan Walsh <dwalsh@redhat.com> - 1.0.10-1
- Make sure none of the gpk apps start on the desktop

* Tue Aug 2 2011 Dan Walsh <dwalsh@redhat.com> - 1.0.9-6
- Change location of xguest home dir to /var/lib/xguest/home

* Wed Jun 15 2011 Dan Walsh <dwalsh@redhat.com> - 1.0.9-5
- Add requires for selinux-policy-targeted

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 1 2011 Dan Walsh <dwalsh@redhat.com> - 1.0.9-3
- Fix boolean handling in the post install

* Wed Jan 5 2011 Dan Walsh <dwalsh@redhat.com> - 1.0.9-2
- Fix semanage boolean line to use -i -

* Wed Oct 6 2010 Dan Walsh <dwalsh@redhat.com> - 1.0.9-1
- Fix placement of xguest.zip file

* Tue Feb 9 2010 Dan Walsh <dwalsh@redhat.com> - 1.0.8-3
- Fix sabayon remove

* Mon Jan 25 2010 Dan Walsh <dwalsh@redhat.com> - 1.0.8-2
- Fix sabayon installation

* Wed Nov 25 2009 Dan Walsh <dwalsh@redhat.com> - 1.0.8-1
- Fix sabayon file

* Wed Aug 26 2009 Dan Walsh <dwalsh@redhat.com> - 1.0.7-7
- Switch to use policycoreutils-sandbox init script

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 23 2009 Dan Walsh <dwalsh@redhat.com> - 1.0.7-5
- Changed to require policycoreutils-python

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Dan Walsh <dwalsh@redhat.com> - 1.0.7-1
- Change xguest init script to have proper summary

* Thu Jan 22 2009 Dan Walsh <dwalsh@redhat.com> - 1.0.6-8
- Modify xguest to be able to be installed in a livecd

* Fri Apr 4 2008 Dan Walsh <dwalsh@redhat.com> - 1.0.6-7
- Require newer version of policy

* Wed Mar 19 2008 Dan Walsh <dwalsh@redhat.com> - 1.0.6-6
- Change gecos field to say "Guest"

* Wed Feb 27 2008 Dan Walsh <dwalsh@redhat.com> - 1.0.6-5
- Leave xguest_u assignment on preun and always set the user to xguest_u on install

* Mon Feb 11 2008 Florian La Roche <laroche@redhat.com> - 1.0.6-4
- fix post requires on pam

* Thu Jan 31 2008 Dan Walsh <dwalsh@redhat.com> - 1.0.6-3
- Add support for exclusive login for xguest

* Tue Dec 18 2007 Dan Walsh <dwalsh@redhat.com> - 1.0.6-2
- Remove lines from namespace.init on package removal

* Mon Dec 17 2007 Dan Walsh <dwalsh@redhat.com> - 1.0.6-1
- Remove xguest init.d script on uninstall
- Fix description


* Fri Dec 7 2007 Dan Walsh <dwalsh@redhat.com> - 1.0.5-2
- Turn on the xguest booleans

* Fri Dec 7 2007 Dan Walsh <dwalsh@redhat.com> - 1.0.5-1
- Allow xguest to run nm-applet

* Tue Nov 27 2007 Dan Walsh <dwalsh@redhat.com> - 1.0.4-2
- Fix permissions on /etc/init.d/xguest

* Wed Nov 21 2007 Dan Walsh <dwalsh@redhat.com> - 1.0.4-1
- Add mount code to allow sharing of file system so hal and automount will work.
- I have added an initscript to set the / as shared and /tmp, /var/tmp and /home/xguest as private

* Fri Oct 26 2007 Dan Walsh <dwalsh@redhat.com> - 1.0.3-1
- Remove exit lines
- Add LICENSE

* Mon Oct 22 2007 Dan Walsh <dwalsh@redhat.com> - 1.0.2-1
- Cleanup spec file

* Mon Oct 22 2007 Dan Walsh <dwalsh@redhat.com> - 1.0.1-2
- Turn on allow_polyinstantiation boolean

* Fri Oct 12 2007 Dan Walsh <dwalsh@redhat.com> - 1.0.1-1
- Add sabayon support

* Thu Sep 13 2007 Dan Walsh <dwalsh@redhat.com> - 1.0.0-1
- Initial version
