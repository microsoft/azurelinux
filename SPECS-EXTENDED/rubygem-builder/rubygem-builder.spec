Vendor:         Microsoft Corporation
Distribution:   Mariner
%global gem_name builder

Name: rubygem-%{gem_name}
Version: 3.2.4
Release: 2%{?dist}
Summary: Builders for MarkUp
License: MIT
URL: http://onestepback.org
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Builder carries copy of Blankslate, which was in the meantime extracted into
# independent gem.
# https://github.com/jimweirich/builder/issues/24
#
# Moreover, rubygem-blankslate is not yet in Fedora.
# https://bugzilla.redhat.com/show_bug.cgi?id=771316
#
# Requires: rubygem(blankslate)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(minitest)
BuildArch: noarch

%description
Builder provides a number of builder objects that make creating structured
data simple to do. Currently the following builder objects are supported:
* XML Markup
* XML Events


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

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Remove shebangs from test files.
pushd %{buildroot}%{gem_instdir}
  find -type f -name '*.rb' -print | xargs sed -i '/#!\/usr\/bin\/env/d'
popd

# Remove shebang from rake file.
sed -i '/#!\/usr\/bin\/env/d' %{buildroot}%{gem_instdir}/rakelib/tags.rake


%check
pushd .%{gem_instdir}
ruby -Ilib:test -e 'Dir.glob "./test/test_*.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGES
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/builder.blurb
%{gem_instdir}/builder.gemspec
%doc %{gem_instdir}/doc
%{gem_instdir}/rakelib
%{gem_instdir}/test

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.2.4-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Apr 17 2020 Vít Ondruch <vondruch@redhat.com> - 3.2.4-1
- Update to Builder 3.2.4.
  Resolves: rhbz#1799993
  Resolves: rhbz#1782394

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 16 2017 Vít Ondruch <vondruch@redhat.com> - 3.2.3-1
- Update to Builder 3.2.3.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Josef Stribny <jstribny@redhat.com> - 3.2.2-3
- Fix tests to run with Minitest

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 Vít Ondruch <vondruch@redhat.com> - 3.2.2-1
- Update to Builder 3.2.2.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Feb 23 2013 Vít Ondruch <vondruch@redhat.com> - 3.1.4-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 17 2012 Vít Ondruch <vondruch@redhat.com> - 3.1.4-1
- Update to Builder 3.1.4.

* Thu Oct 11 2012 Vít Ondruch <vondruch@redhat.com> - 3.1.3-1
- Update to Builder 3.1.3.

* Wed Jul 18 2012 Vít Ondruch <vondruch@redhat.com> - 3.0.0-1
- Update to Builder 3.0.0.

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 2.1.2-9
- Fixed license.

* Thu Jan 19 2012 Vít Ondruch <vondruch@redhat.com> - 2.1.2-8
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Vít Ondruch <vondruch@redhat.com> - 2.1.2-6
- Fix FTBFS rhbz#712927.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 29 2008 Jeroen van Meeuwen <kanarip@kanarip.com> - 2.1.2-2
- Rebuild for review

* Sun Jul 13 2008 root <root@oss1-repo.usersys.redhat.com> - 2.1.2-1
- Initial package
