# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from actiontext-6.0.3.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name actiontext

# TODO: Re-enable recompilation if possible. Currently, we don't have rollup.js
# in Fedora and therefore it requires network access. Still good for checking
# the results
%bcond_with js_recompilation

Name: rubygem-%{gem_name}
Version: 8.0.2
Release: 3%{?dist}
Summary: Rich text framework
License: MIT
URL: https://rubyonrails.org
Source0: https://rubygems.org/gems/%{gem_name}-%{version}%{?prerelease}.gem
# git clone https://github.com/rails/rails.git --no-checkout && cd rails/actiontext
# git archive -v -o actiontext-8.0.2-tests.tar.gz v8.0.2 test/
Source1: %{gem_name}-%{version}%{?prerelease}-tests.tar.gz
# Source code of pregenerated JS files.
# git clone https://github.com/rails/rails.git && cd rails/actiontext
# git archive -v -o actiontext-8.0.2-js.tar.gz v8.0.2 app/javascript rollup.config.js
Source2: %{gem_name}-%{version}%{?prerelease}-js.tar.gz

BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 3.2.0
BuildRequires: rubygem(actionmailer) = %{version}
BuildRequires: rubygem(activestorage) = %{version}
BuildRequires: rubygem(bundler)
BuildRequires: rubygem(image_processing)
BuildRequires: rubygem(importmap-rails)
BuildRequires: rubygem(railties) = %{version}
BuildRequires: rubygem(sprockets-rails)
BuildRequires: rubygem(sqlite3)
BuildRequires: rubygem(capybara) >= 3.26
BuildRequires: rubygem(puma)
BuildRequires: rubygem(selenium-webdriver)
BuildRequires: chromedriver chromium chromium-headless
# Chromium availability is limited:
# https://src.fedoraproject.org/rpms/chromium/blob/0d9761748509bb12051ab149d28c1052cd834f87/f/chromium.spec#_800
# and chrome-headless even more:
# https://src.fedoraproject.org/rpms/chromium/blob/0d9761748509bb12051ab149d28c1052cd834f87/f/chromium.spec#_46-48
ExclusiveArch: x86_64 aarch64 noarch
%{?with_js_recompilation:BuildRequires: %{_bindir}/npm}
BuildArch: noarch

# Bundles Trix editor.
# https://trix-editor.org/
# https://github.com/basecamp/trix
# app/assets/javascripts/trix.js
# TODO: would be nice to check the version. Althoug the bundled Trix is going
# to be extracted into independent gem: https://github.com/rails/rails/pull/55058
Provides: bundled(js-trix) = 2.1.12

%description
Edit and display rich text in Rails applications.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}%{?prerelease} -b1 -b2

%build
%if %{with js_recompilation}
# Recompile the embedded JS files from sources.
#
# This is practice suggested by packaging guidelines:
# https://fedoraproject.org/wiki/Packaging:Guidelines#Use_of_pregenerated_code

find app/assets/ -type f -exec sha512sum {} \;

rm -rf app/assets/javacripts/actiontext.*

ln -s %{builddir}/app/javascript ./app/javascript
cp -a %{builddir}/rollup.config.js .

# TODO: This requires network access. Use Fedora rollup.js if it becomes
# available eventually
# `rollup-plugin-terser` is missing from package.json, otherwise `npm install`
# would be enough.
# https://github.com/rails/rails/issues/54795
npm install rollup-plugin-terser
npx rollup --config rollup.config.js

# For comparison with the orginal checksum above.
find app/assets/ -type f -exec sha512sum {} \;
%endif

gem build ../%{gem_name}-%{version}%{?prerelease}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
( cd .%{gem_instdir}
cp -a %{builddir}/test .

mkdir ../tools
# Fake test_common.rb. It does not provide any functionality besides
# `force_skip` alias.
touch ../tools/test_common.rb
# Netiher strict_warnings.rb appears to be useful.
touch ../tools/strict_warnings.rb

export BUNDLE_GEMFILE=${PWD}/../Gemfile

# The `Gemfiles` is unavoidable, otherwise `importmap-rails` are not properly
# loaded.
cat > $BUNDLE_GEMFILE <<EOF
gem "actionmailer"
gem "activestorage"
gem "capybara"
gem "image_processing"
gem "importmap-rails"
gem "puma"
gem "railties"
gem "selenium-webdriver"
gem "sprockets-rails"
gem "sqlite3"
EOF

# test/javascript_package_test.rb requires rollup.js, which we don't have.
# OTOH, if we had it, we would recomplie the sources and the test would have
# less value.
mv test/javascript_package_test.rb{,.disable}

ruby -Itest -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
)

%files
%dir %{gem_instdir}
%license %{gem_instdir}/MIT-LICENSE
%{gem_instdir}/app
%{gem_instdir}/db
%{gem_libdir}
%{gem_instdir}/package.json
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 09 2025 Vít Ondruch <vondruch@redhat.com> - 8.0.2-1
- Update to Action Text 8.0.2.
  Related: rhbz#2238177

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Sep 10 2023 Pavel Valena <pvalena@redhat.com> - 7.0.8-1
- Update to actiontext 7.0.8.

* Mon Aug 28 2023 Pavel Valena <pvalena@redhat.com> - 7.0.7.2-1
- Update to actiontext 7.0.7.2.

* Thu Aug 10 2023 Pavel Valena <pvalena@redhat.com> - 7.0.7-1
- Update to actiontext 7.0.7.

* Sun Jul 23 2023 Pavel Valena <pvalena@redhat.com> - 7.0.6-1
- Update to actiontext 7.0.6.

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 30 2023 Pavel Valena <pvalena@redhat.com> - 7.0.5-1
- Update to actiontext 7.0.5.

* Tue Mar 14 2023 Pavel Valena <pvalena@redhat.com> - 7.0.4.3-1
- Update to actiontext 7.0.4.3.

* Wed Jan 25 2023 Pavel Valena <pvalena@redhat.com> - 7.0.4.2-1
- Update to actiontext 7.0.4.2.

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Sep 15 2022 Pavel Valena <pvalena@redhat.com> - 7.0.4-1
- Update to actiontext 7.0.4.

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Mar 14 2022 Pavel Valena <pvalena@redhat.com> - 7.0.2.3-1
- Update to actiontext 7.0.2.3.

* Wed Feb 09 2022 Pavel Valena <pvalena@redhat.com> - 7.0.2-1
- Update to actiontext 7.0.2.

* Thu Feb 03 2022 Pavel Valena <pvalena@redhat.com> - 7.0.1-1
- Update to actiontext 7.0.1.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Sep 17 2021 Pavel Valena <pvalena@redhat.com> - 6.1.4.1-1
- Update to actiontext 6.1.4.1.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 30 2021 Pavel Valena <pvalena@redhat.com> - 6.1.4-1
- Update to actiontext 6.1.4.

* Tue May 18 2021 Pavel Valena <pvalena@redhat.com> - 6.1.3.2-1
- Update to actiontext 6.1.3.2.

* Fri Apr 09 2021 Pavel Valena <pvalena@redhat.com> - 6.1.3.1-1
- Update to actiontext 6.1.3.1.

* Thu Feb 18 2021 Pavel Valena <pvalena@redhat.com> - 6.1.3-1
- Update to actiontext 6.1.3.

* Mon Feb 15 2021 Pavel Valena <pvalena@redhat.com> - 6.1.2.1-1
- Update to actiontext 6.1.2.1.

* Wed Jan 27 2021 Pavel Valena <pvalena@redhat.com> - 6.1.1-1
- Update to actiontext 6.1.1.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct  8 12:04:45 CEST 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.4-1
- Update to actiontext 6.0.3.4.
  Resolves: rhbz#1877508

* Tue Sep 22 01:18:56 CEST 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.3-1
- Update to actiontext 6.0.3.3.
  Resolves: rhbz#1877508

* Mon Aug 17 05:18:06 GMT 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.2-1
- Update to actiontext 6.0.3.2.

* Mon Aug 03 07:01:37 GMT 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.1-2
- Initial package Action Text 6.0.3.1.
