# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from marcel-0.3.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name marcel

Name: rubygem-%{gem_name}
Version: 1.0.2
Release: 14%{?dist}
Summary: Simple mime type detection using magic numbers, file names, and extensions
# * Portions of Marcel are adapted from the [mimemagic] gem, released under
#   the terms of the MIT License.
# * Marcel's magic signature data is adapted from
#   [Apache Tika](https://tika.apache.org), released under the terms of the
#   Apache License.
# Automatically converted from old format: MIT and ASL 2.0 - review is highly recommended.
License: LicenseRef-Callaway-MIT AND Apache-2.0
URL: https://github.com/rails/marcel
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/rails/marcel.git && cd marcel
# git archive -v -o marcel-1.0.2-test.tar.gz v1.0.2 test/
Source1: %{gem_name}-%{version}-test.tar.gz
# From https://github.com/rails/marcel/commit/12fc8daae656ccb09441c4a3c376b5de3af05172
Patch0: marcel-12fc8da-minitest-5_19-compat.patch
# Fix test compatibility with Rack 3+
Patch1: rubygem-marcel-1.0.5-Limit-Rack-Lint-InputWrapper-test-to-Rack-2.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.2
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(rack)
BuildArch: noarch

%description
Simple mime type detection using magic numbers, file names, and extensions.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -a 1
%patch -P0 -p1
%patch -P1 -p1

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

%check
ln -sf $(pwd)/test .%{gem_instdir}
pushd .%{gem_instdir}

# Byebug is just development dependency.
sed -i "/require 'byebug'/ s/^/#/" test/test_helper.rb

ruby -Ilib:test -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/MIT-LICENSE
%license %{gem_instdir}/APACHE-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 10 2025 Vít Ondruch <vondruch@redhat.com> - 1.0.2-12
- Fix test compatibility with Rack 3+

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 1.0.2-10
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 20 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.2-6
- Backport upstream patch for minitest 5.19 compatibility

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 18 2022 Pavel Valena <pvalena@redhat.com> - 1.0.2-1
- Update to marcel 1.0.2.
  Resolves: rhbz#2006133

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Apr 09 2021 Vít Ondruch <vondruch@redhat.com> - 1.0.1-1
- Update to Marcel 1.0.1.
  Resolves: rhbz#1947831

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 02 2018 Jun Aruga <jaruga@redhat.com> - 0.3.2-1
- Initial package
