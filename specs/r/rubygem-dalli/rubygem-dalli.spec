# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name dalli

# Depends on Rails and its needed by Rails
%bcond_with tests

Name: rubygem-%{gem_name}
Version: 3.2.0
Release: 10%{?dist}
Summary: High performance memcached client for Ruby
License: MIT
URL: https://github.com/petergoldstein/dalli
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Tests are not shipped with the gem, you may get them like so
# git clone https://github.com/petergoldstein/dalli.git --no-checkout
# git -C dalli archive -v -o dalli-3.2.0-tests.txz v3.2.0 test/
Source1: %{gem_name}-%{version}-tests.txz

BuildRequires: ruby(release)
BuildRequires: rubygems-devel
%if %{with tests}
BuildRequires: memcached
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(connection_pool)
%endif
BuildRequires: ruby
Requires:  rubygem(base64)
BuildArch: noarch

%description
High performance memcached client for Ruby


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
%setup -q -n %{gem_name}-%{version} -b1

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
%if %{with tests}
pushd .%{gem_instdir}
# Symlink tests into place
ln -s %{_builddir}/test .

sed -i '/bundler/ s/^/#/' test/helper.rb
ruby -Ilib:test -rdalli -e "Dir.glob('./test/test_*.rb').sort.each{ |x| require x }"
popd
%endif

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%license %{gem_instdir}/LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/History.md
%{gem_instdir}/Gemfile

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Nov 11 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.0-8
- Add Requires: rubygem(base64) explicitly for ruby34

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Feb 07 2022 Pavel Valena <pvalena@redhat.com> - 3.2.0-1
- Update to dalli 3.2.0.
  Resolves: rhbz#1689613

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May 29 2018 Pavel Valena <pvalena@redhat.com> - 2.7.8-1
- Update to dalli 2.7.8.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Vít Ondruch <vondruch@redhat.com> - 2.7.6-4
- Fix memcached 1.5.4 test compatibility.

* Wed Aug 30 2017 Pavel Valena <pvalena@redhat.com> - 2.7.6-3
- Fix FTBFS(tests only) in rawhide.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Pavel Valena <pvalena@redhat.com> - 2.7.6-1
- Update to 2.7.6.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 18 2015 Josef Stribny <jstribny@redhat.com> - 2.7.4-1
- Update to 2.7.4

* Mon Jun 16 2014 Josef Stribny <jstribny@redhat.com> - 2.7.2-2
- Fix the test the right way

* Mon Jun 16 2014 Josef Stribny <jstribny@redhat.com> - 2.7.2-1
- Update to dalli 2.7.2

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 08 2013 Josef Stribny <jstribny@redhat.com> - 2.6.4-2
- Enable tests

* Wed Jul 31 2013 Josef Stribny <jstribny@redhat.com> - 2.6.4-1
- Initial package
