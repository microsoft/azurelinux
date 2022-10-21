%global gem_name introspection
Summary:        Dynamic inspection of the hierarchy of method definitions on a Ruby object
Name:           rubygem-%{gem_name}
Version:        0.0.4
Release:        13%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://jamesmead.org
Source0:        https://github.com/floehopper/introspection/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
BuildRequires:  ruby(release)
BuildRequires:  rubygem-metaclass < 0.1
BuildRequires:  rubygem-metaclass >= 0.0.1
BuildRequires:  rubygems-devel
# There is no #assert_nothing_raised in minitest 5.x
BuildRequires:  rubygem(minitest)
Provides:       rubygem(%{gem_name}) = %{version}-%{release}
BuildArch:      noarch

%description
Dynamic inspection of the hierarchy of method definitions on a Ruby object.

%package doc
Summary:        Documentation for %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gem_dir} %{gem_name}-%{version}.gem
mkdir -p %{buildroot}%{gem_instdir}
#add lib, test and samples files to buildroot from Source0
cp -a lib/ %{buildroot}%{gem_instdir}/
cp -a test/ %{buildroot}%{gem_instdir}/
cp -a samples/ %{buildroot}%{gem_instdir}/
#add COPYING, README, Rakefile and Gemfile files to buildroot from Source0
cp COPYING.txt %{buildroot}%{gem_instdir}/
cp README.md %{buildroot}%{gem_instdir}/
cp Rakefile %{buildroot}%{gem_instdir}/
cp Gemfile %{buildroot}%{gem_instdir}/

%check
pushd .%{gem_instdir}
# Disable Bundler.
sed -i '/bundler\/setup/ d' test/test_helper.rb

ruby -Ilib:test -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%license %{gem_instdir}/COPYING.txt
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_instdir}/README.md
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/samples
%{gem_instdir}/test
%doc %{gem_docdir}

%changelog
* Tue Mar 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.0.4-13
- Build from .tar.gz source.

* Tue Oct 19 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 0.0.4-12
- Initial CBL-Mariner import from Fedora 35 (license: MIT)
- License verified

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Pavel Valena <pvalena@redhat.com> - 0.0.4-1
- Update to introspection 0.0.4(rhbz#1390394)
  - Remove patch0, subsumed
  - Remove patch1, subsumed

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 19 2014 Vít Ondruch <vondruch@redhat.com> - 0.0.3-3
- Fix FTBFS in Rawhide (rhbz#1107144).

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 07 2014 Vít Ondruch <vondruch@redhat.com> - 0.0.3-1
- Update to introspection 0.0.3.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 25 2013 Vít Ondruch <vondruch@redhat.com> - 0.0.2-8
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 19 2012 Vít Ondruch <vondruch@redhat.com> - 0.0.2-5
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 04 2011 Vít Ondruch <vondruch@redhat.com> - 0.0.2-3
- Fix BuildRequires and test suite.
- Move README.md into -doc subpackage and mark it properly.

* Tue Oct 04 2011 Vít Ondruch <vondruch@redhat.com> - 0.0.2-2
- Clarified license.

* Mon Oct 03 2011 Vít Ondruch <vondruch@redhat.com> - 0.0.2-1
- Initial package
