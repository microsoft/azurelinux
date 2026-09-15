# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from hocon-0.9.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name hocon

%if 0%{?el7}
%global enable_checks 0
%else
%global enable_checks 1
%endif

Name: rubygem-%{gem_name}
Version: 1.4.0
Release: 9%{?dist}
Summary: HOCON Config Library
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License: Apache-2.0
URL: https://github.com/puppetlabs/ruby-hocon
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem

# SOURCE1 contains the upstream tag of the project from github
# in particular this includes the spec directory which was not
# included in the gemfile.
# https://github.com/puppetlabs/ruby-hocon/issues/65
# was originally resolved.
# However the rspec files were then removed again for a bizare reason.
# https://tickets.puppetlabs.com/browse/PA-2942
Source1: https://github.com/puppetlabs/ruby-hocon/archive/%{version}/ruby-hocon-%{version}.tar.gz

BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 1.9.0
%if 0%{?enable_checks}
BuildRequires: rubygem(rspec)
%endif
BuildArch: noarch

%description
A port of the Java Typesafe Config
library to Ruby.
https://github.com/typesafehub/config

%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
sed -i 's/\/usr\/bin\/env ruby/\/usr\/bin\/ruby/' bin/hocon

# unpack only the spec files from SOURCE1.
tar zxf %{SOURCE1} ruby-hocon-%{version}/spec --strip-components 1

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/
mkdir -p %{buildroot}%{_bindir}
mv %{buildroot}%{gem_instdir}/bin/hocon %{buildroot}/%{_bindir}/hocon


%check
%if 0%{?enable_checks}
rspec spec/
%endif

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/spec
%{gem_spec}
%{_bindir}/hocon

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/HISTORY.md
%doc %{gem_instdir}/README.md

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul  24 2024 Miroslav Suchý <msuchy@redhat.com> - 1.4.0-6
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Mar 25 2023 Steve Traylen <steve.traylen@cern.ch> - 1.4.0-1
- Update to 1.4.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec  7 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.1-6
- Apply upstreamed patch for ruby3.2 File.exists? removal

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Aug 21 2020 Steve Traylen <steve.traylen@cern.ch> - 1.3.1-1
- Update to 1.3.1

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 8 2019 Steve Traylen <steve.traylen@cern.ch> - 1.3.0-1
- Update to 1.3.0

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Nov 03 2017 Steve Traylen <steve.traylen@cern.ch> - 1.2.5-1
- Update to 1.2.5

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 23 2017 Steve Traylen <steve.traylen@cern.ch> - 1.2.4-1
- Update to 1.2.4

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 14 2015 Steve Traylen <steve.traylen@cern.ch> - 0.9.3-3
- Remove references to fc21.

* Thu Dec 03 2015 Steve Traylen <steve.traylen@cern.ch> - 0.9.3-2
- Use spec tests from upstream source.

* Tue Nov 03 2015 Steve Traylen <steve.traylen@cern.ch> - 0.9.3-1
- Initial package
