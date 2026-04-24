# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name minitest-around

Name: rubygem-%{gem_name}
Version: 0.5.0
Release: 6%{?dist}
Summary: Around block for minitest
License: MIT
URL: https://github.com/splattael/minitest-around
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(cucumber)
BuildArch: noarch

%description
Alternative for setup/teardown dance.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

# cucumber 7 syntax change
sed -i config/cucumber.yml -e "s|~@ignore|'not @ignore'|"
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

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




# Run the test suite
%check
pushd .%{gem_instdir}
  sed -i "/require 'bundler/ s/^/#/" test/helper.rb
  RUBYOPT=-Ilib ruby -e 'Dir.glob "./test/*_{test,spec}.rb", &method(:require)'
  RUBYOPT=-Ilib cucumber --tag 'not @todo' --tag 'not @rspec'
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/README.md
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%{gem_spec}
%exclude %{gem_instdir}/.*
%exclude %{gem_cache}

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/config
%exclude %{gem_instdir}/features
%exclude %{gem_instdir}/Gemfile
%exclude %{gem_instdir}/Rakefile
%exclude %{gem_instdir}/examples
%exclude %{gem_instdir}/minitest-around.gemspec
%exclude %{gem_instdir}/test

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 16 2023 Ilia Gradina <ilgrad@fedoraproject.org> - 0.5.0-1
- Update to 0.5.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 14 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.4.1-9
- Fix for cucumber 7 syntax change

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-8
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Ilya Gradina <ilya.gradina@gmail.com> - 0.4.1-1
- update to 0.4.1

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Nov 10 2016 Ilya Gradina <ilya.gradina@gmail.com> - 0.4.0-3
- change in check section

* Tue Nov 08 2016 Ilya Gradina <ilya.gradina@gmail.com> - 0.4.0-2
- fix tests
 
* Sat Nov 05 2016 Ilya Gradina <ilya.gradina@gmail.com> - 0.4.0-1
- update to 0.4.0

* Tue Aug 16 2016 Ilya Gradina <ilya.gradina@gmail.com> - 0.3.2-2
- changes in files hierarchy

* Tue Sep 29 2015 Ilya Gradina <ilya.gradina@gmail.com> - 0.3.2-1
- Initial package
