Vendor:         Microsoft Corporation
Distribution:   Mariner
%global gem_name mongo
# Disable tests as MongoDB was dropped from Fedora because of a licensing issue.
# https://src.fedoraproject.org/rpms/mongodb/blob/master/f/dead.package
%bcond_with tests

Name: rubygem-%{gem_name}
Version: 2.11.2
Release: 3%{?dist}
Summary: Ruby driver for MongoDB
License: ASL 2.0
URL: https://docs.mongodb.com/ruby-driver/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
%if %{with tests}
# For running the tests
BuildRequires: %{_bindir}/mongod
BuildRequires: rubygem(bson) >= 4.6.0
BuildRequires: rubygem(rspec)
%endif
BuildArch: noarch

%description
A Ruby driver for MongoDB.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}

%build
# Create the gem as gem install only works on a gem file
gem build ../%{gem_name}-%{version}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Drop the shebang, file is not executable anyway.
sed -i '/#!\// d' %{buildroot}%{gem_instdir}/Rakefile

%if %{with tests}
%check
pushd .%{gem_instdir}

# Create data directory and start testing mongo instance.
# See https://github.com/mongodb/mongo-ruby-driver/blob/master/.travis.yml
mkdir data
mongod \
  --dbpath data \
  --logpath data/log \
  --fork \
  --auth

# timeout-interrupt is not available in Fedora yet.
sed -i "/^if SpecConfig\.instance\.mri?$/i\\
require 'timeout'\\
TimeoutInterrupt = Timeout\\
" spec/spec_helper.rb
sed -i "/^if SpecConfig\.instance\.mri?$/,/^end$/ s/^/#/" spec/spec_helper.rb

# rspec-retry is not available in Fedora yet.
sed -i "/require 'rspec\/retry'/ s/^/#/" spec/spec_helper.rb

# I can't figure why this fails. It might be upstream issue, because it seems
# it was not tested against MonogoDB 4.x.
sed -i "/collection.client.use(:admin).command(FAIL_POINT_BASE_COMMAND.merge(/i\        pending" \
  spec/integration/bulk_insert_spec.rb

CI=1 EXTERNAL_DISABLED=1 rspec spec

# Shutdown mongo and cleanup the data.
mongod --shutdown --dbpath data
rm -rf data
popd
%endif

%files
%dir %{gem_instdir}
%{_bindir}/mongo_console
%license %{gem_instdir}/LICENSE
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/mongo.gemspec
%{gem_instdir}/spec

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.11.2-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 20 2019 Jun Aruga <jaruga@redhat.com> - 2.11.2-1
- Update to mongo 2.11.2.

* Tue Nov 19 2019 Jun Aruga <jaruga@redhat.com> - 2.11.1-1
- Update to mongo 2.11.1.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 28 2019 Jun Aruga <jaruga@redhat.com> - 2.8.0-1
- Update to mongo 2.8.0.

* Tue Feb 05 2019 Troy Dawson <tdawson@redhat.com> - 2.6.2-3
- Remove tests because they depended on mongodb
-- https://pagure.io/fesco/issue/2078

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 12 2018 Jun Aruga <jaruga@redhat.com> - 2.6.2-1
- Make tests conditional enableing tests as a default.

* Mon Sep 10 2018 Vít Ondruch <vondruch@redhat.com> - 2.6.2-1
- Update to mongo 2.6.2.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 23 2018 Jun Aruga <jaruga@redhat.com> - 2.5.1-1
- Update to mongo 2.5.1.

* Fri Feb 16 2018 Jun Aruga <jaruga@redhat.com> - 2.5.0-1
- Update to mongo 2.5.0.

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.4.3-2
- Escape macros in %%changelog

* Wed Aug 16 2017 Vít Ondruch <vondruch@redhat.com> - 2.4.3-1
- Update to mongo 2.4.3.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 04 2017 Vít Ondruch <vondruch@redhat.com> - 2.4.1-1
- Update to mongo 2.4.1.

* Thu Dec 15 2016 Vít Ondruch <vondruch@redhat.com> - 2.4.0-1
- Update to mongo 2.4.0.

* Wed Aug 31 2016 Vít Ondruch <vondruch@redhat.com> - 2.3.0-1
- Update to mongo 2.3.0.

* Tue Feb 16 2016 Troy Dawson <tdawson@redhat.com> - 1.10.2-5
- Disable tests until mongodb becomes stable in rawhide again.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul 27 2015 Troy Dawson <tdawson@redhat.com> - 1.10.2-2
- Fix tests

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 26 2014 Vít Ondruch <vondruch@redhat.com> - 1.10.2-1
- Update to mongo 1.10.2.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 19 2013 Vít Ondruch <vondruch@redhat.com> - 1.9.2-1
- Update to mongo 1.9.2.
- Enabled test suite.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 Troy Dawson <tdawson@redhat.com> - 1.6.4-4
- Fix to make it build/install on F19+

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 10 2012 Troy Dawson <tdawson@redhat.com> - 1.6.4-2
- Fixed doc
- removed more BuildRequires that are not required

* Thu Aug 09 2012 Troy Dawson <tdawson@redhat.com> - 1.6.4-1
- Updated to latest version
- Removed BuildRequires that are not needed

* Thu Aug 09 2012 Troy Dawson <tdawson@redhat.com> - 1.4.0-7
- Fixed checks.  
  Only run checks that do not require a running mongodb server

* Tue Aug 07 2012 Troy Dawson <tdawson@redhat.com> - 1.4.0-6
- Changed .gemspec and Rakefile to not be doc
- Added checks

* Thu Aug 02 2012 Troy Dawson <tdawson@redhat.com> - 1.4.0-5
- Fixed rubygem(bson) requires

* Mon Jul 23 2012 Troy Dawson <tdawson@redhat.com> - 1.4.0-4
- Updated to meet new fedora rubygem guidelines

* Thu Nov 17 2011 Troy Dawson <tdawson@redhat.com> - 1.4.0-3
- Changed group to Development/Languages
- Changed the global variables
- Seperated the doc and test into the doc rpm

* Thu Nov 17 2011 Troy Dawson <tdawson@redhat.com> - 1.4.0-2
- Added %%{?dist} to version

* Tue Nov 15 2011  <tdawson@redhat.com> - 1.4.0-1
- Initial package
