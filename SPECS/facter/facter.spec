## START: Set by rpmautospec
## (rpmautospec version 0.2.5)
%define autorelease(e:s:pb:) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{?dist}
## END: Set by rpmautospec

%global gem_name facter
%global debug_package %{nil}

Name:           facter
Version:        4.2.5
Release:        2%{?dist}
Summary:        Command and ruby library for gathering system information
Vendor:		Microsoft Corporation
Distribution:	Mariner
License:        ASL 2.0
URL:            https://github.com/puppetlabs/facter
Source0:        https://downloads.puppetlabs.com/%{name}/%{name}-%{version}.gem

BuildRequires:  gnupg2
BuildRequires:  rubygems-devel
BuildRequires:  ruby >= 2.3
Requires:       ruby(rubygems)

# Add runtime deps for testing
BuildRequires:  rubygem(hocon) >= 1.3
BuildRequires:  rubygem(thor) >= 1.0.1

# Binaries that Facter can call for complete facts
%ifarch %ix86 x86_64 ia64
Requires:       dmidecode
Requires:       pciutils
Requires:       virt-what
%endif
Requires:       net-tools

Provides:       ruby-%{name} = %{version}
Obsoletes:      ruby-%{name} < 4
Obsoletes:      %{name}-devel < 4

BuildArch: noarch

%description
Facter is a lightweight program that gathers basic node information about the
hardware and operating system. Facter is especially useful for retrieving
things like operating system names, hardware characteristics, IP addresses, MAC
addresses, and SSH keys.

Facter is extensible and allows gathering of node information that may be
custom or site specific. It is easy to extend by including your own custom
facts. Facter can also be used to create conditional expressions in Puppet that
key off the values returned by facts.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.


%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/
rm %{buildroot}%{gem_instdir}/LICENSE

mkdir -p %{buildroot}%{_bindir}
cp -a .%{gem_instdir}/bin/facter %{buildroot}%{_bindir}
rm -rf %{buildroot}/%{gem_instdir}/bin


%check
# No test suite can run since the spec files are not part of the gem
# So try to run the executable and see if that works
GEM_HOME="%{buildroot}%{gem_dir}" %{buildroot}%{_bindir}/facter


%files
%license LICENSE
%dir %{gem_instdir}
%{_bindir}/facter
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}

%changelog
* Thu Dec 30 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> 4.2.5-2
- Initial CBL-Mariner import from Fedora 35 (license: MIT)
- License verified

* Sun Nov 21 2021 Igor Raits <ignatenkobrain@fedoraproject.org> 4.2.5-1
- Update to 4.2.5

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> 4.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 18 2021 Ewoud Kohl van Wijngaarden <ewoud@kohlvanwijngaarden.nl> 4.2.0-2
- Minor fixes for Facter 4.2.0

* Sun Jun 06 2021 Joel Capitao <jcapitao@redhat.com> 4.2.0-1
- Update to 4.2.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> 3.14.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Jonathan Wakely <jwakely@redhat.com> 3.14.7-7
- Rebuilt for Boost 1.75

* Sat Jan 09 2021 Benjamin Beasley <code@musicinmybrain.net> 3.14.7-6
- fix changelog entry

* Sat Jan 09 2021 Benjamin Beasley <code@musicinmybrain.net> 3.14.7-5
- Rebuild for cpp-hocon 0.3.0

* Wed Nov 04 2020 Jeff Law <law@redhat.com> 3.14.7-4
- Fix missing #includes for gcc-11

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> 3.14.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 03 2020 Jonathan Wakely <jwakely@redhat.com> 3.14.7-2
- Rebuild for Boost 1.73.0

* Tue Jan 28 2020 Adam Tkac <vonsch@gmail.com> 3.14.7-1
- update to 3.14.7

* Fri Oct 18 2019 Richard Shaw <hobbes1069@gmail.com> 3.14.2-3
- Rebuild for yaml-cpp 0.6.3.

* Wed Aug 14 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> 3.14.2-2
- Disable tests

* Wed Aug 14 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> 3.14.2-1
- Update to 3.14.2

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> 3.9.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> 3.9.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> 3.9.3-8
- Remove obsolete Group tag

* Tue Jan 22 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> 3.9.3-7
- Remove obsolete ldconfig scriptlets

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> 3.9.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 14 2018 Richard Shaw <hobbes1069@gmail.com> 3.9.3-5
- Rebuild for yaml-cpp 0.6.0.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> 3.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Jonathan Wakely <jwakely@redhat.com> 3.9.3-3
- Rebuilt for Boost 1.66

* Tue Nov 07 2017 James Hogarth <james.hogarth@gmail.com> 3.9.3-1
- Update to 3.9.3 for F28 facter3 Change

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> 2.4.4-6
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> 2.4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> 2.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Dennis Gilmore <dennis@ausil.us> 2.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Dennis Gilmore <dennis@ausil.us> 2.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 21 2015 Orion Poplawski <orion@cora.nwra.com> 2.4.4-1
- Update to 2.4.4

* Fri Apr 03 2015 Orion Poplawski <orion@cora.nwra.com> 2.4.3-1
- Update to 2.4.3

* Fri Feb 13 2015 Orion Poplawski <orion@cora.nwra.com> 2.4.1-1
- Update to 2.4.1

* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Tue Jan 06 2015 Orion Poplawski <orion@cora.nwra.com> 2.3.0-2
- Remove old patches

* Tue Jan 06 2015 Orion Poplawski <orion@cora.nwra.com> 2.3.0-1
- Update to 2.3.0

* Sat Oct 11 2014 Michael Stahnke <stahnma@puppetlabs.com> 2.2.0-1
- Updating facter to 2.2.0 as per bz#1108041

* Sat Aug 16 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Dennis Gilmore <dennis@ausil.us> 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 05 2014 Lubomir Rintel <lkundrak@v3.sk> 2.0.1-2
- Fix el7 conditionals as suggested by Orion Poplawski (BZ #1087946)

* Tue Apr 29 2014 Sam Kottler <shk@linux.com> 2.0.1-1
- Update to 2.0.1

* Wed Jan 29 2014 Todd Zullinger <tmz@pobox.com> 1.7.4-3
- Send dmidecode errors to /dev/null in the virtual fact

* Wed Jan 29 2014 Todd Zullinger <tmz@pobox.com> 1.7.4-2
- Create /etc/facter/facts.d for external facts

* Wed Jan 29 2014 Todd Zullinger <tmz@pobox.com> 1.7.4-1
- Update to 1.7.4

* Wed Jan 29 2014 Todd Zullinger <tmz@pobox.com> 1.7.3-4
- Fix a typo in the changelog

* Tue Jan 28 2014 Todd Zullinger <tmz@pobox.com> 1.7.3-3
- Move definition of enable_check macro

* Tue Oct 08 2013 Sam Kottler <shk@redhat.com> 1.7.3-2
- Move enabled_check into its own conditional and disabled it on F20+

* Tue Oct 08 2013 Sam Kottler <shk@redhat.com> 1.7.3-1
- Update to 2.7.3 (BZ #1016817)

* Sat Aug 03 2013 Dennis Gilmore <dennis@ausil.us> 1.6.18-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 22 2013 Sam Kottler <shk@redhat.com> 1.6.18-7
- Add upstream patch to prevent using the loopback IP (127.0.0.1) instead
  of the first valid one (BZ#976942)

* Wed Apr 03 2013 Todd Zullinger <tmz@pobox.com> 1.6.18-6
- Avoid warnings when virt-what produces no output

* Tue Apr 02 2013 Todd Zullinger <tmz@pobox.com> 1.6.18-5
- Apply upstream patch to filter virt-what warnings from virtual fact

* Tue Mar 19 2013 Todd Zullinger <tmz@pobox.com> 1.6.18-4
- Ensure man page is installed on EL < 7

* Tue Mar 19 2013 Todd Zullinger <tmz@pobox.com> 1.6.18-3
- Require virt-what for improved KVM detection (#905592)

* Tue Mar 19 2013 Todd Zullinger <tmz@pobox.com> 1.6.18-2
- Restart puppet in %postun (#806370)

* Mon Mar 18 2013 Todd Zullinger <tmz@pobox.com> 1.6.18-1
- Update to 1.6.18

* Wed Mar 13 2013 Vít Ondruch <vondruch@redhat.com> 1.6.17-3
- Keep the spec working for older releases.

* Tue Mar 12 2013 Vít Ondruch <vondruch@redhat.com> 1.6.17-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Mon Feb 25 2013 Jeroen van Meeuwen (Ergo Project) <jeroen.van.meeuwen@ergo-project.org> 1.6.17-1
- Check in version 1.6.17

* Wed Feb 13 2013 Dennis Gilmore <dennis@ausil.us> 1.6.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 04 2012 Michael Stahnke <stahnma@puppetlabs.com> 1.6.16-1
- Update facter to 1.6.16

* Wed Nov 28 2012 Michael Stahnke <stahnma@puppetlabs.com> 1.6.15-1
- Rebase to 1.6.15 and fix issue found in bz #871211

* Wed Nov 07 2012 Michael Stahnke <stahnma@puppetlabs.com> 1.6.14-3
- Adding the GPG asc file as per discussion by maintainers

* Mon Nov 05 2012 Michael Stahnke <stahnma@puppetlabs.com> 1.6.14-1
- Rebase facter to 1.6.14.

* Thu Jul 19 2012 Dennis Gilmore <dennis@ausil.us> 1.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 05 2012 Todd Zullinger <tmz@pobox.com> 1.6.6-1
- Update to 1.6.6

* Sun Feb 19 2012 Todd Zullinger <tmz@pobox.com> 1.6.5-11
- Remove INSTALL from %doc

* Sun Feb 19 2012 Todd Zullinger <tmz@pobox.com> 1.6.5-10
- Update summary and description

* Sun Feb 19 2012 Todd Zullinger <tmz@pobox.com> 1.6.5-9
- Disable useless debuginfo generation (#795106, thanks to Ville Skyttä)

* Wed Feb 15 2012 Todd Zullinger <tmz@pobox.com> 1.6.5-8
- Only run rspec checks on Fedora >= 17

* Wed Feb 15 2012 Todd Zullinger <tmz@pobox.com> 1.6.5-7
- Preserve timestamps when installing files

* Wed Feb 15 2012 Todd Zullinger <tmz@pobox.com> 1.6.5-6
- Make ec2 facts work on CentOS again (#790849, thanks to Jeremy Katz)

* Wed Feb 15 2012 Todd Zullinger <tmz@pobox.com> 1.6.5-5
- Drop BuildArch: noarch and make dmidecode/pciutils deps arch-specific

* Wed Feb 15 2012 Todd Zullinger <tmz@pobox.com> 1.6.5-4
- Make spec file work for EPEL and Fedora

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> 1.6.5-3
- Rebuilt for Ruby 1.9.3.

* Thu Jan 26 2012 Todd Zullinger <tmz@pobox.com> 1.6.5-2
- Require net-tools and pciutils, thanks to Dominic Cleal (#783749)

* Thu Jan 26 2012 Todd Zullinger <tmz@pobox.com> 1.6.5-1
- Update to 1.6.5

* Thu Jan 05 2012 Todd Zullinger <tmz@pobox.com> 1.6.4-3
- Require dmidecode (upstream #11041)

* Thu Jan 05 2012 Todd Zullinger <tmz@pobox.com> 1.6.4-2
- Re-order BuildRequires/Requires

* Thu Jan 05 2012 Todd Zullinger <tmz@pobox.com> 1.6.4-1
- Update to 1.6.4

* Sat Oct 15 2011 Todd Zullinger <tmz@pobox.com> 1.6.2-1
- Update to 1.6.2

* Thu Sep 29 2011 Todd Zullinger <tmz@pobox.com> 1.6.1-2
- Minor spec file reformatting

* Thu Sep 29 2011 Todd Zullinger <tmz@pobox.com> 1.6.1-1
- Update to 1.6.1

* Wed Jul 27 2011 Todd Zullinger <tmz@pobox.com> 1.6.0-2
- Update license tag, GPLv2+ -> ASL 2.0

* Wed Jul 27 2011 Todd Zullinger <tmz@pobox.com> 1.6.0-1
- Update to 1.6.0, update SL patch from upstream

* Thu May 26 2011 Todd Zullinger <tmz@pobox.com> 1.5.9-2
- Improve Scientific Linux support, courtesy of Orion Poplawski

* Thu May 26 2011 Todd Zullinger <tmz@pobox.com> 1.5.9-1
- Update to 1.5.9

* Tue Feb 08 2011 Dennis Gilmore <dennis@ausil.us> 1.5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Aug 28 2010 Todd Zullinger <tmz@pobox.com> 1.5.8-1
- Update to facter-1.5.8

* Wed Jul 28 2010 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.5.7-3
- dist-git conversion

* Wed Nov 25 2009 Bill Nottingham <notting@fedoraproject.org> 1.5.7-2
- Fix typo that causes a failure to update the common directory. (releng

* Sat Sep 26 2009 Todd Zullinger <tmz@fedoraproject.org> 1.5.7-1
- Update to 1.5.7

* Wed Aug 12 2009 Jeroen van Meeuwen <kanarip@fedoraproject.org> 1.5.5-3
- 1.5.5-3

* Fri Jul 24 2009 Jesse Keating <jkeating@fedoraproject.org> 1.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 22 2009 Todd Zullinger <tmz@fedoraproject.org> 1.5.5-1
- Update to 1.5.5

* Tue Mar 03 2009 Todd Zullinger <tmz@fedoraproject.org> 1.5.4-1
- Update to 1.5.4

* Tue Feb 24 2009 Jesse Keating <jkeating@fedoraproject.org> 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep 10 2008 Todd Zullinger <tmz@fedoraproject.org> 1.5.2-1
- New version

* Mon Sep 08 2008 David Lutterkort <lutter@fedoraproject.org> 1.5.1-1
- New version

* Thu Jul 17 2008 David Lutterkort <lutter@fedoraproject.org> 1.5.0-2
- Change mkdir in install to mkdir -p

* Thu Jul 17 2008 David Lutterkort <lutter@fedoraproject.org> 1.5.0-1
- New version

* Mon Sep 24 2007 David Lutterkort <lutter@fedoraproject.org> 1.3.8-1
- Version 1.3.8

* Sat Mar 31 2007 David Lutterkort <lutter@fedoraproject.org> 1.3.7-1
- New version 1.3.7

* Fri Jan 19 2007 David Lutterkort <lutter@fedoraproject.org> 1.3.6-1
- New version 1.3.6

* Thu Jan 18 2007 David Lutterkort <lutter@fedoraproject.org> 1.3.5-2
- Fix bz 223168

* Wed Oct 11 2006 David Lutterkort <lutter@fedoraproject.org> 1.3.5-1
- Version 1.3.5

* Wed Sep 13 2006 David Lutterkort <lutter@fedoraproject.org> 1.3.3-4
- Rebuild for FC6 successful

* Wed Sep 13 2006 David Lutterkort <lutter@fedoraproject.org> 1.3.3-3
- Rebuild for FC6

* Sun Aug 27 2006 Ville Skyttä <scop@fedoraproject.org> 1.3.3-2
- http://fedoraproject.org/wiki/Extras/Schedule/FC6MassRebuild

* Wed Jul 12 2006 David Lutterkort <lutter@fedoraproject.org> 1.3.3-1
- auto-import facter-1.3.3-1 on branch devel from facter-1.3.3-1.src.rpm
