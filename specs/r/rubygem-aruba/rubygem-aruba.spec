# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from aruba-0.4.11.gem by gem2rpm -*- rpm-spec -*-
%global     gem_name    aruba

Summary:    CLI Steps for Cucumber, hand-crafted for you in Aruba
Name:       rubygem-%{gem_name}
Version:    2.3.3
Release: 2%{?dist}

# SPDX confirmed
# templates/, jquery.js existed on 0.14.14, no longer included in 2.0 and above
License:        MIT
URL:            https://github.com/cucumber/aruba
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1:        %{name}-%{version}-testsuite.tar.gz
# Source1 is created by $ bash %%SOURCE2 %%VERSION
Source2:        %{gem_name}-create-test-suite-tarball.sh
# Make bundler runtime dependency optional
Patch1:         rubygem-aruba-2.0.0-make-bundler-optional.patch
# https://github.com/cucumber/aruba/commit/bd2aea600f7e989e4da734c3e823c3ce12ce629b
# We still use diff-lcs 1.5, revert the above patch for now
Patch2:         rubygem-aruba-2.3.1-diff-lcs-1_6-change.patch


BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby
# For %%check
BuildRequires:  rubygem(childprocess)
BuildRequires:  rubygem(contracts)
BuildRequires:  rubygem(cucumber)
BuildRequires:  rubygem(irb)
BuildRequires:  rubygem(minitest)
BuildRequires:  rubygem(rspec) >= 3
BuildRequires:  rubygem(thor)
BuildRequires:  less

BuildArch:      noarch

%description
Aruba is Cucumber extension for Command line applications written
in any programming language.


%package        doc
Summary:        Documentation for %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc
Documentation for %{name}

%prep
%setup -q -n %{gem_name}-%{version} -a 1
pushd %{gem_name}-%{version}
for f in *
do
    basef=$(basename $f)
    target=../${basef}
    ln -sf $(pwd)/$f $target
done
# For tests
ln -sf ../lib
popd
%patch -P1 -p1
%patch -P2 -p1 -R

mv ../%{gem_name}-%{version}.gemspec .

# Relax cucumber dependency
# Partially revert https://github.com/cucumber/aruba/pull/906
sed -i '\@cucumber@s|>= 8.0|>= 7.0|' %{gem_name}-%{version}.gemspec
# Remove bundler dependency harder
sed -i '\@dependency.*bundler@d' %{gem_name}-%{version}.gemspec

%build
gem build %{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
    %{buildroot}%{gem_dir}/

rm -f %{buildroot}%{gem_cache}

%check
pushd %{gem_name}-%{version}
for f in *
do
    basef=$(basename $f)
    target=../%{gem_instdir}/${basef}
    unlink $target || true
    ln -sf $(pwd)/$f $target
done
popd

pushd .%{gem_instdir}

# We don't care about code coverage.
sed -i spec/spec_helper.rb \
    -e '\@[sS]imple[Cc]ov@d' \
    %{nil}

env RUBYOPT=-rtime \
    rspec spec

# We don't care about code coverage.
sed -i features/support/env.rb \
    -e '\@require.*simplecov@d'
> features/support/simplecov_setup.rb

# Let the test cli-app find Aruba.
sed -i fixtures/cli-app/spec/spec_helper.rb \
    -e "\@\$LOAD_PATH@s|\.\./\.\./lib|$(pwd)/lib|"

# Kill tests which requires python explicitly
# (to reduce BR, anyway this test is not important)
sed -i features/step_definitions/hooks.rb \
	-e '\@platform.which@s|"python"|"no-python"|'

# The following test fails on ppc64le, due to different block size
# (expected: 64k actual: 4k), disabling
PPC64_ENV_P=$(uname -m | grep -q ppc64 && echo 0 || echo 1)
if test x"${PPC64_ENV_P}" == x0
then
    mv features/04_aruba_api/filesystem/report_disk_usage.feature{,.skip}
fi

# Disable bundler tests.
mv features/03_testing_frameworks/cucumber/disable_bundler.feature{,.skip}

# Adjust test cases referring to $HOME.
sed -i features/04_aruba_api/core/expand_path.feature -e "s|/home/\[\^/\]+|$(echo $HOME)|" 
sed -i features/02_configure_aruba/home_directory.feature \
    -e "\@Scenario: Default value@,\@Scenario@s|/home/|$(echo $HOME)|"
sed -i features/02_configure_aruba/home_directory.feature \
    -e "\@Set to aruba's working directory@,\@Scenario@s|/home/|$(echo $HOME)/|"

# Make the Aruba always awailable.
export CUCUMBER_PUBLISH_QUIET=true
env RUBYOPT=-I$(pwd)/lib cucumber -f progress

# Go back the skipped test
if test x"${PPC64_ENV_P}" == x0
then
    mv features/04_aruba_api/filesystem/report_disk_usage.feature{.skip,}
fi
mv features/03_testing_frameworks/cucumber/disable_bundler.feature{.skip,}

popd # from .%%{gem_instdir}

%files
%dir        %{gem_instdir}
%license    %{gem_instdir}/LICENSE
%doc        %{gem_instdir}/README.md

%{gem_libdir}
%{gem_instdir}/exe
%{gem_spec}

%files doc
%doc    %{gem_docdir}
%doc    %{gem_instdir}/CONTRIBUTING.md
%doc    %{gem_instdir}/CHANGELOG.md

%changelog
* Sat Dec 06 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.3-1
- 2.3.3

* Sun Sep 14 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.2-1
- 2.3.2

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jun 15 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.1-1
- 2.3.1

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 03 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.0-1
- 2.3.0

* Thu Nov 28 2024 Vít Ondruch <vondruch@redhat.com> - 2.2.0-10
- Drop BR: rubygem(pry)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Feb 08 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.0-8
- Adjust testsuite for Minitest 5.22.2

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 27 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.0-5
- Patch for ruby3.3

* Thu Nov  9 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.0-4
- Explicitly add BR: less for BR: pry
- Change cucumber publish quiet method

* Mon Sep 11 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.0-2
- Kill python test entirely to redure BR, it is not important
  (related to bug 2237692)

* Fri Sep  8 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.0-1
- 2.2.0
- Relax cucumber dependency

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Mar 21 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.0-4
- Correct license tag

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu May 26 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.0-1
- 2.1.0

* Sun Apr 24 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.1-1
- 2.0.1

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 19 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.0-3
- Use upstream patch for rspec-core rspec test suite issue
  (Gem.win_platform? related)

* Fri Jan 14 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.0-2
- Make bundler optional again
- Workaround patch to make rspec-core test suite pass
- Some cleanup

* Mon Sep 06 2021 Pavel Valena <pvalena@redhat.com> - 2.0.0-1
- Update to aruba 2.0.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Apr  6 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.14.14-6
- Add BR: rubygem(irb)

* Mon Feb  1 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.14.14-5
- Disable cucumber test failing on ppc64le

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 30 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.14.14-1
- 0.14.14

* Thu Dec 26 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.14.13-1
- 0.14.13

* Tue Nov  5 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.14.12-1
- 0.14.12

* Sat Aug 17 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.14.11-1
- 0.14.11

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 21 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.14.9-1
- 0.14.9

* Wed Feb 27 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.14.8-1
- 0.14.8

* Tue Feb 26 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.14.7-3
- Some cleanup

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Vít Ondruch <vondruch@redhat.com>
- Enable test suite.

* Tue Jan 29 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.14.7-1
- 0.14.7

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul  2 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.14.6-1
- 0.14.6

* Fri Apr  6 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.14.5-1
- 0.14.5

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 31 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.14.3-1
- 0.14.3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan  2 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.14.2-1
- 0.14.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 15 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.6.2-1
- 0.6.2

* Mon Sep  1 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.6.1-1
- 0.6.1

* Wed Aug 13 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.6.0-1
- 0.6.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.4-1
- 0.5.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 22 2013 Josef Stribny <jstribny@redhat.com> - 0.5.2-1
- Update to aruba 0.5.2

* Sat Feb 23 2013 Vít Ondruch <vondruch@redhat.com> - 0.4.11-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Mon Feb 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.4.11-5
- Disable tests that do not actually test anything (patch from upstream).

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 19 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.4.11-2
- Remove the ffi dependency and add conflicts with the problematic version.

* Fri Feb 24 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.4.11-1
- Initial package
