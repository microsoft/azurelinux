# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from ronn-ng-0.9.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name ronn-ng

Name:           rubygem-%{gem_name}
Version:        0.10.1
Release: 8%{?dist}
Summary:        Builds man pages from Markdown
License:        MIT
URL:            https://github.com/apjanke/ronn-ng
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/apjanke/ronn-ng.git && cd ronn-ng
# git archive -v -o ronn-ng-0.10.1-test.tar.gz v0.10.1 test/
Source1: %{gem_name}-%{version}-test.tar.gz
# https://github.com/apjanke/ronn-ng/pull/125
# load fileutils explicitly for ruby34
Patch0:         ronn-ng-pr125-ruby34-fileutils-deps.patch
BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby
BuildRequires:  rubygem(kramdown)
BuildRequires:  rubygem(kramdown-parser-gfm)
BuildRequires:  rubygem(mustache)
BuildRequires:  rubygem(nokogiri)
BuildRequires:  rubygem(test-unit)
BuildArch:      noarch

Requires:       groff-base
Provides:       rubygem-ronn = %{version}-%{release}
Obsoletes:      rubygem-ronn < 0.7.3-20

%description
Ronn-NG builds manuals in HTML and Unix man page format from Markdown.

The source format includes all of Markdown but has a more rigid structure and
syntax extensions for features commonly found in man pages (definition lists,
link notation, etc.). The ronn-format(7) manual page defines the format in
detail.

%package doc
Summary:        Documentation for %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b 1
(
cd %{_builddir}/test
%patch -P0 -p2
)

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


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Move man pages into the appropriate place
install -Dt %{buildroot}/%{_mandir}/man1/ -m 0644 %{buildroot}%{gem_instdir}/man/ronn.1
install -Dt %{buildroot}/%{_mandir}/man7/ -m 0644 %{buildroot}%{gem_instdir}/man/ronn-format.7

# Move completion scripts into the appropriate place
install -Dt %{buildroot}/usr/share/bash-completion/completions/ -m 0644 %{buildroot}%{gem_instdir}/completion/bash/ronn
install -Dt %{buildroot}/usr/share/zsh/site-functions/ -m 0644 %{buildroot}%{gem_instdir}/completion/zsh/_ronn

%check
pushd .%{gem_instdir}
cp -a %{_builddir}/test test

ruby -Itest -e 'Dir.glob "./test/test_*.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%{_bindir}/ronn
%{gem_instdir}/INSTALLING.md
%license %{gem_instdir}/LICENSE.txt
%{gem_instdir}/bin
%exclude %{gem_instdir}/completion
%{gem_instdir}/config.ru
%{gem_libdir}
%exclude %{gem_instdir}/man
%exclude %{gem_cache}
%{gem_spec}
%{_mandir}/man1/ronn.1*
%{_mandir}/man7/ronn-format.7*
%dir %_datadir/bash-completion//
%_datadir/bash-completion/completions/
%_datadir/zsh/site-functions/

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/AUTHORS
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/ronn-ng.gemspec

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 19 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.10.1-5
- Load fileutils explicitly for test for ruby34

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Mar 12 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 0.10.1-3
- Fix groff dependency

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 08 2024 Vít Ondruch <vondruch@redhat.com> - 0.10.1-1
- Update to Ronn-NG 0.10.1

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Sep 08 2022 Vít Ondruch <vondruch@redhat.com> - 0.9.1-6
- Fix FTBFS due to Ruby 3.1 / Psych 4.0 test incompatibility.
  Resolves: rhbz#2113704

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Sep 19 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.9.1-1
- Add BRs for tests, enable tests in %%check.
- Require /usr/bin/groff, not the package in case the file is moved.
- Keep the license file in the original location.
- Adjust various macros and invocations.

* Fri Aug 21 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.9.1-1
- Switch to https://github.com/apjanke/ronn-ng/ upstream fork (#1817168)
- Regenerate spec file with gem2rpm.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 4 2013 Ricky Elrod <codeblock@fedoraproject.org> 0.7.3-4
- Add groff-base Requires.
- Nuke a Requires of the base package from the -doc subpackage.
- Fix Requires for F18-, make it be >= 1.9.1.

* Fri Apr 5 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.7.3-3
- Fix Requires so the package works on F18- and F19+.
- Fix what is marked as doc.
- Remove some extra files from the gem_instdir which are only needed for building.

* Wed Apr 3 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.7.3-2
- Move things into a doc subpackage.
- Fix BuildRequires.
- Document why the test suite isn't running.
- Make some things that don't need to be installed, not install.
- Mark some files as doc files.

* Wed Apr 3 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.7.3-1
- Initial build.
