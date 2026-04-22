# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from bootsnap-1.3.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name bootsnap

Name: rubygem-%{gem_name}
Version: 1.15.0
Release: 13%{?dist}
Summary: Boot large ruby/rails apps faster
License: MIT
URL: https://github.com/Shopify/bootsnap
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem

# The bootsnap gem doesn't ship with the test suite.
# You may check it out like so:
# git clone http://github.com/Shopify/bootsnap.git --no-checkout
# cd bootsnap && git archive -v -o bootsnap-1.15.0-tests.txz v1.15.0 test/
Source1: %{gem_name}-%{version}-tests.txz
# Correctly determine StdLib files as stable.
# https://github.com/Shopify/bootsnap/issues/431
# https://github.com/Shopify/bootsnap/commit/72202aab5e5b3602ece4e8748bcdeefe2d789ab5
Patch0: rubygem-bootsnap-1.15.0-Use-RbConfig-CONFIG-rubylibdir-to-check-for-stdlib-files.patch
Patch1: rubygem-bootsnap-1.15.0-Use-RbConfig-CONFIG-rubylibdir-to-check-for-stdlib-files-test.patch
# Minitest 5.19 puts `MiniTest` constant behind environment variable.
# https://github.com/Shopify/bootsnap/pull/452
Patch2: rubygem-bootsnap-1.16.0-Fix-compatibility-with-Minitest-5.19.patch
# Patch for ruby3.3.0dev: relax method invocation checking for KernelRequireTest
# https://github.com/Shopify/bootsnap/pull/460
Patch3: rubygem-bootsnap-pr460-KernelRequireTest-method-invocation-check.patch

BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby-devel >= 2.0.0
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(bundler)
BuildRequires: rubygem(msgpack)
# Compiler is required for build of gem binary extension.
# https://fedoraproject.org/wiki/Packaging:C_and_C++#BuildRequires_and_Requires
BuildRequires: gcc

%description
Bootsnap is a library that plugs into Ruby, with optional support
for ActiveSupport and YAML, to optimize and cache expensive computations.

%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b 1

%patch 0 -p1

pushd %{_builddir}
%patch 1 -p1
%patch 2 -p1
%patch 3 -p1
popd

sed -i -e "/^\s*\$CFLAGS / s/^/#/g" \
  ext/bootsnap/extconf.rb

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}/%{gem_name}
cp -a .%{gem_extdir_mri}/gem.build_complete %{buildroot}%{gem_extdir_mri}/
cp -a .%{gem_extdir_mri}/%{gem_name}/*.so %{buildroot}%{gem_extdir_mri}/%{gem_name}

# Prevent dangling symlink in -debuginfo (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/ext/

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/exe -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
ln -s %{_builddir}/test test

cat <<GEMFILE > Gemfile
gem "minitest"
gem "mocha"
gem "msgpack"
GEMFILE

# Plese note that `KernelTest` testcases are executed in separate process,
# which needs to subsequetnly load `bootsnap/setup`, therefore we need to
# use RUBYOPT to define load paths. This is normally handled by Bunler and
# `gemspec` directive. But we would need to have the bootsnap .gemspec in
# the directory.
RUBYOPT="-I$(dirs +1)%{gem_extdir_mri}:$(dirs +1)%{gem_libdir}" \
  ruby -Itest -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%{_bindir}/bootsnap
%{gem_extdir_mri}
%license %{gem_instdir}/LICENSE.txt
%{gem_instdir}/exe
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 07 2025 Vít Ondruch <vondruch@redhat.com> - 1.15.0-10
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.4

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Vít Ondruch <vondruch@redhat.com> - 1.15.0-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.3

* Tue Nov 21 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.15.0-5
- Backport upstream fix for ruby3.3.0dev test failure fix for
  KernelRequireTest

* Thu Aug 03 2023 Vít Ondruch <vondruch@redhat.com> - 1.15.0-4
- Fix FTBFS due to compatibility with Minitest 5.19+.

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 12 2023 Vít Ondruch <vondruch@redhat.com> - 1.15.0-1
- Update to Bootsnap 1.15.0.
  Resolves: rhbz#1868112

* Wed Jan 04 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.7-9
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.2

* Sun Dec 25 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.7-8
- Use %%gem_extdir_mri instead of ext for %%check due to ruby3.2 change
  for ext cleanup during build

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 26 2022 Pavel Valena <pvalena@redhat.com> - 1.4.7-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.1

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan  6 2021 Vít Ondruch <vondruch@redhat.com> - 1.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.0

* Fri Jul 31 09:47:28 GMT 2020 Pavel Valena <pvalena@redhat.com> - 1.4.7-1
- Update to bootsnap 1.4.7.
  Resolves: rhbz#1862090

* Fri Jul 31 09:19:53 GMT 2020 Vít Ondruch <vondruch@redhat.com> - 1.3.2-7
- Re-enable ARM support. The problem should be gone since Ruby 2.6+.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.2-4
- Apply upstream patch to support ruby 2.7
- Unpack test tarball beforehand, as the above patch needs applying
- Rebuild against ruby27

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 18 2019 Pavel Valena <pvalena@redhat.com> - 1.3.2-1
- Update to Bootsnap 1.3.2.
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.6

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 30 2018 Pavel Valena <pvalena@redhat.com> - 1.3.0-1
- Initial package
