# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from globalid-0.3.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name globalid

%bcond_with bootstrap

Name: rubygem-%{gem_name}
Version: 1.2.1
Release: 4%{?dist}
Summary: Refer to any model with a URI: gid://app/class/id
License: MIT
URL: http://www.rubyonrails.org
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/rails/globalid.git && cd globalid
# git archive -v -o globalid-1.2.1-tests.tar.gz v1.2.1 test
Source1: %{gem_name}-%{version}-tests.tar.gz
# Fix Ruby 3.4 compatibility.
# https://github.com/rails/globalid/pull/192
Patch0: rubygem-globalid-1.2.1-Keep-using-URI-RFC2396-parser.patch
# Fix Rails 8 compatibility.
# https://github.com/rails/globalid/pull/197/commits/f05f178f6960e85f6cdb6d6bf8c1812fd83af74a
Patch1: rubygem-globalid-1.2.1-Fix-cache-format-for-Rails-8.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.5.0
%if %{without bootstrap}
BuildRequires: rubygem(activesupport)
BuildRequires: rubygem(activemodel)
BuildRequires: rubygem(railties)
%endif
BuildArch: noarch

%description
URIs for your models makes it easy to pass references around.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b 1

%patch 0 -p1

( cd %{builddir}
%patch 1 -p1
)

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%if %{without bootstrap}
%check
pushd .%{gem_instdir}
ln -s %{_builddir}/test test

# Avoid Bundler dependency.
sed -i "/bundler\/setup/ s/^/#/" ./test/helper.rb

# Prevent `NameError: uninitialized constant ActionController::Base` by
# explicit `-raction_controller`.
# https://github.com/rails/rails/issues/55215
ruby -Ilib:test -raction_controller -e "Dir.glob './test/cases/*test.rb', &method(:require)"
popd
%endif


%files
%dir %{gem_instdir}
%license %{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 20 2025 Vít Ondruch <vondruch@redhat.com> - 1.2.1-3
- Fix Rails 8 compatibility.

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 10 2024 Vít Ondruch <vondruch@redhat.com> - 1.2.1-1
- Update to globalid 1.2.1.
  Resolves: rhbz#2236912

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Feb 28 2023 Pavel Valena <pvalena@redhat.com> - 1.1.0-1
- Update to globalid 1.1.0.
  Resolves: rhbz#2161792

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 30 2021 Pavel Valena <pvalena@redhat.com> - 1.0.0-1
- Update to globalid 1.0.0.
  Resolves: rhbz#1986611

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 02 2019 Pavel Valena <pvalena@redhat.com> - 0.4.2-1
- Update to globalid 0.4.2.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 08 2018 Vít Ondruch <vondruch@redhat.com> - 0.4.1-1
- Disable Rails 5.2 incompatible test case.
- Modernize the .spec file a bit.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 16 2018 Pavel Valena <pvalena@redhat.com> - 0.4.1-1
- Update to 0.4.1.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jun Aruga <jaruga@redhat.com> - 0.4.0-1
- Update to 0.4.0

* Tue Feb 14 2017 Jun Aruga <jaruga@redhat.com> - 0.3.6-3
- Fix Fixnum/Bignum deprecated warning for Ruby 2.4.0.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 07 2016 Jun Aruga <jaruga@redhat.com> - 0.3.6-1
- Update to 0.3.6

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 19 2015 Josef Stribny <jstribny@redhat.com> - 0.3.3-1
- Update to 0.3.3

* Tue Jan 06 2015 Josef Stribny <jstribny@redhat.com> - 0.3.0-1
- Initial package
