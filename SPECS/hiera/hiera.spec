Summary:        A simple hierarchical database supporting plugin data sources
Name:           hiera
Version:        3.7.0
Release:        5%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/puppetlabs/hiera
Source0:        http://downloads.puppetlabs.com/hiera/%{name}-%{version}.tar.gz
# Use /etc/puppet rather than /etc/puppetlabs/puppet
Patch0:         fix-puppetlab-paths.patch

BuildArch:      noarch

BuildRequires:  ruby-devel
BuildRequires:  rubygem(json)
BuildRequires:  rubygem(mocha)
BuildRequires:  rubygem(rspec)

%description
A simple hierarchical database supporting plugin data sources.

%prep
%setup -q
%patch0 -p1

%build
# Nothing to build

%install
mkdir -p %{buildroot}%{ruby_vendorlibdir}
mkdir -p %{buildroot}%{_sysconfdir}/puppet
mkdir -p %{buildroot}%{_bindir}
cp -pr lib/hiera %{buildroot}%{ruby_vendorlibdir}
cp -pr lib/hiera.rb %{buildroot}%{ruby_vendorlibdir}
install -p -m0755 bin/hiera %{buildroot}%{_bindir}
install -p -m0644 ext/hiera.yaml %{buildroot}%{_sysconfdir}/puppet
mkdir -p %{buildroot}%{_sharedstatedir}/hiera

%check
gem install rspec mocha json
rspec -Ilib spec

%files
%license COPYING LICENSE
%doc README.md
%{_bindir}/hiera
%{ruby_vendorlibdir}/hiera.rb
%{ruby_vendorlibdir}/hiera
%dir %{_sharedstatedir}/hiera
%dir %{_sysconfdir}/puppet
%config(noreplace) %{_sysconfdir}/puppet/hiera.yaml

%changelog
* Thu Dec 21 2023 Sindhu Karri <lakarri@microsoft.com> - 3.7.0-5
- Promote package to Mariner Base repo

* Thu Apr 21 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.7.0-4
- Spec clean-up.

* Thu Dec 30 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 3.7.0-3
- Initial CBL-Mariner import from Fedora 36 (license: MIT)
- License verified

* Fri Aug 20 2021 Steve Traylen <releng@fedoraproject.org> - 3.7.0-2
- Correct software homepage

* Fri Aug 20 2021 Steve Traylen <releng@fedoraproject.org> - 3.7.0-1
- Update to 3.7.0.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 13 2019 Steve Traylen <releng@fedoraproject.org> - 3.6.0-1
- Update to 3.6.0.
- Call rspec tests correctly - actually run them.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 1 2017 Steve Traylen <releng@fedoraproject.org> - 3.3.1-1
- Update to 3.3.1.
- Relocate hiera.yaml to /etc/puppet/hiera.yaml
- Remove items for old OSes.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 3 2015 Steve Traylen <steve.traylen@cern.ch> - 3.0.1-1
- New version 3.0.1

* Thu Jul 30 2015 Gaël Chamoulaud <gchamoul@redhat.com> - 1.3.4-4
- Removed 0001-Fix-errors-with-Puppet-4.patch

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 1.3.4-2
- Fix errors with Puppet4 (patch from Lukas Bezdicka)

* Wed Jun 11 2014 Steve Traylen <steve.traylen@cern.ch> - 1.3.4-1
- New version 1.3.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 3 2014 Steve Traylen <steve.traylen@cern.ch> - 1.3.3-1
- New version 1.3.3, Update to latest ruby guidelines.

* Wed May 14 2014 Steve Traylen <steve.traylen@cern.ch> - 1.3.2-2
- Packaging error

* Wed May 14 2014 Steve Traylen <steve.traylen@cern.ch> - 1.3.2-1
- New version 1.3.2

* Thu Feb 13 2014 Steve Traylen <steve.traylen@cern.ch> - 1.3.1-2
- New version 1.3.1

* Mon Sep 16 2013 Steve Traylen <steve.traylen@cern.ch> - 1.2.1-1
- New version 1.2.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 15 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.0-5
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 1 2012 Steve Traylen <steve.traylen@cern.ch> - 1.0.0-3
- Correct ruby(abi) requirement.

* Thu Sep 27 2012 Steve Traylen <steve.traylen@cern.ch> - 1.0.0-2
- Remove _isa tag for f18 from ruby-devel?

* Thu Sep 27 2012 Steve Traylen <steve.traylen@cern.ch> - 1.0.0-1
- Update to 1.0.0
- Add LICENSE file
- Add /var/lib/hiera as default data path.

* Wed May 30 2012 Steve Traylen <steve.traylen@cern.ch> - 1.0.0-0.2.rc3
- Update to 1.0.0rc3 and drop puppet functions.

* Wed May 16 2012 Steve Traylen <steve.traylen@cern.ch> - 1.0.0-0.2rc2
- Adapt to fedora guidelines.

* Mon May 14 2012 Matthaus Litteken <matthaus@puppetlabs.com> - 1.0.0-0.1rc2
- 1.0.0rc2 release

* Mon May 14 2012 Matthaus Litteken <matthaus@puppetlabs.com> - 1.0.0-0.1rc1
- 1.0.0rc1 release

* Thu May 03 2012 Matthaus Litteken <matthaus@puppetlabs.com> - 0.3.0.28-1
- Initial Hiera Packaging. Upstream version 0.3.0.28
