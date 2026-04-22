# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global	gem_name	json

%global	pkg_version_num		2.13.2
%dnl		%global	pkg_version_alpha
%global	gem_version()		%{pkg_version_num}%{?pkg_version_alpha:.%pkg_version_alpha}

Name:           rubygem-%{gem_name}
Version:        %{pkg_version_num}%{?pkg_version_alpha:~%pkg_version_alpha}
Release: 2%{?dist}

Summary:        A JSON implementation in Ruby

# SPDX confirmed
License:        Ruby OR BSD-2-Clause
URL:            https://github.com/flori/json
Source0:        https://rubygems.org/gems/%{gem_name}-%{gem_version}.gem
Source1:        rubygem-%{gem_name}-%{gem_version}-missing-files.tar.gz
# Source1 is created by $ %%SOURCE2 v%%version
Source2:        json-create-tarball-missing-files.sh

BuildRequires:  gcc
BuildRequires:  ruby(release)
BuildRequires:  ruby-devel
BuildRequires:  rubygems-devel
BuildRequires:  rubygem(rake)
BuildRequires:  rubygem(bigdecimal)
BuildRequires:  rubygem(test-unit-ruby-core)
BuildRequires:  rubygem(test-unit)

Obsoletes:	rubygem-%{gem_name}-gui < %{version}
Obsoletes:	ruby-%{gem_name}-gui < %{version}
Obsoletes:	ruby-%{gem_name} < %{version}

%description
This is a implementation of the JSON specification according
to RFC 4627 in Ruby.
You can think of it as a low fat alternative to XML,
if you want to store data to disk or transmit it over
a network rather than use a verbose markup language.

%package	doc
Summary:	Documentation for %{name}

Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.

%prep
%global	version	%gem_version

%setup -q -n %{gem_name}-%{gem_version} -a 1
mv ./%{gem_name}-%{version}/test .
mv ../%{gem_name}-%{version}.gemspec .

# Change cflags to honor Fedora compiler flags correctly
find . -name extconf.rb | xargs sed -i -e 's|-O3|-O2|' -e 's|-O0|-O2|'

%build
gem build %{gem_name}-%{version}.gemspec
%gem_install

find . -name \*gem -exec chmod 0644 {} \;

# remove pure
rm -fr .%{gem_instdir}/lib/json/pure*

%install
mkdir -p $RPM_BUILD_ROOT%{gem_dir}
mkdir -p $RPM_BUILD_ROOT%{gem_extdir_mri}
 
cp -a .%{gem_dir}/* %{buildroot}/%{gem_dir}
cp -a .%{gem_extdir_mri}/{gem.build_complete,json} %{buildroot}/%{gem_extdir_mri}/

mkdir -p %{buildroot}%{ruby_libdir}
mkdir -p %{buildroot}%{ruby_libarchdir}
ln -s %{gem_libdir}/json.rb %{buildroot}%{ruby_libdir}/json.rb
ln -s %{gem_libdir}/json %{buildroot}%{ruby_libdir}/json
ln -s %{gem_extdir_mri}/json/ %{buildroot}%{ruby_libarchdir}/json

find $RPM_BUILD_ROOT%{gem_instdir} -name \*.rb -print0 | \
	xargs --null chmod 0644

# We don't need those files anymore.
pushd $RPM_BUILD_ROOT%{gem_instdir}
rm -rf \
	%{gem_name}.gemspec \
	Gemfile \
	ext \
	java \
	lib/json/truffle_ruby/ \
	test \
	%{nil}
popd

%check
rm -rf .%{gem_instdir}/test
cp -a ./test .%{gem_instdir}/

pushd .%{gem_instdir}
ruby -Ilib:test:test/json:$RPM_BUILD_ROOT%{gem_extdir_mri}:. \
	-e "gem 'test-unit'; require 'test_helper' ; Dir.glob('test/json/*_test.rb').sort.each {|f| require f}"
popd


%files
%dir %{gem_instdir}
%dir %{gem_libdir}
%dir %{gem_libdir}/%{gem_name}

%license %{gem_instdir}/BSDL
%license %{gem_instdir}/COPYING
%license %{gem_instdir}/LEGAL
%doc %{gem_instdir}/CHANGES.md
%doc %{gem_instdir}/README.md

%{gem_libdir}/%{gem_name}.rb
%{gem_libdir}/%{gem_name}/add
%{gem_libdir}/%{gem_name}/common.rb
%{gem_libdir}/%{gem_name}/ext.rb
%dir	%{gem_libdir}/%{gem_name}/ext
%dir	%{gem_libdir}/%{gem_name}/ext/generator/
%{gem_libdir}/%{gem_name}/ext/generator/*.rb
%{gem_libdir}/%{gem_name}/version.rb
%{gem_libdir}/%{gem_name}/generic_object.rb

%{ruby_libdir}/json*
%{ruby_libarchdir}/json*
%{gem_extdir_mri}/
%{gem_spec}

%exclude %{gem_cache}

%files      doc
%{gem_docdir}/


%changelog
* Thu Jul 31 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.13.2-1
- 2.13.2

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue May 27 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.12.2-1
- 2.12.2

* Fri May 16 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.12.0-1
- 2.12.0

* Tue Apr 29 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.11.3-1
- 2.11.3

* Wed Mar 12 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.10.2-1
- 2.10.2

* Tue Feb 11 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.10.1-1
- 2.10.1

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 07 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.9.1-2
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.4

* Thu Dec 19 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.9.1-1
- 2.9.1

* Thu Dec 05 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.9.0-1
- 2.9.0

* Thu Nov 07 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.8.1-1
- 2.8.1

* Sat Nov 02 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.8.0~alpha1-14
- 2.8.0 alpha1 (e660b61)

* Fri Nov 01 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.7.5-201
- Apply upstream patch for JSON.generate behavior, restoring activesupport json
  usage

* Wed Oct 30 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.7.5-200
- 2.7.5

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.2-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Apr 04 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.7.2-200
- 2.7.2

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-203
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-202
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.7.1-201
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.3

* Tue Dec  5 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.7.1-200
- 2.7.1

* Sun Dec  3 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.7.0-201
- Backport upstream patch for JSON.dump regression for hash

* Fri Dec  1 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.7.0-200
- 2.7.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.3-204
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Apr 21 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.6.3-203
- SPDX migration

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.3-202
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 03 2023 Vít Ondruch <vondruch@redhat.com> - 2.6.3-201
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.2

* Mon Dec  5 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.6.3-200
- 2.6.3

* Wed Oct  5 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.6.2-202
- Remove no longer needed recompilation

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed May 18 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.6.2-200
- 2.6.2

* Wed Jan 26 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.6.1-202
- F-36: rebuild against ruby31

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Oct 24 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.6.1-200
- 2.6.1

* Fri Oct 22 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.6.0-200
- 2.6.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-202
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan  6 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.5.1-200
- 2.5.1

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul  2 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.1-200
- 2.3.1

* Tue Apr 14 2020 Vít Ondruch <vondruch@redhat.com> - 2.3.0-202
- Avoid unexpected JRuby dependency.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.0-200
- 2.3.0

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 26 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.0-200
- Update to 2.2.0
- Bump release

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-107
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-106
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-105
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 2.1.0-104
- Rebuilt for switch to libxcrypt

* Wed Jan 03 2018 Vít Ondruch <vondruch@redhat.com> - 2.1.0-103
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.5

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-102
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Apr 21 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.0-100
- Update to 2.1.0

* Thu Apr 13 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.4-100
- Update to 2.0.4

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 15 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.3-100
- Update to 2.0.3

* Tue Jul 12 2016 Vít Ondruch <vondruch@redhat.com> - 1.8.3-103
- Make symlinks for json gem.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.3-102
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.3-101
- F-24: rebuild against ruby23

* Thu Sep 24 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.3-100
- Update to 1.8.3

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.2-100
- Update to 1.8.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7-104
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 25 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 1.7.7-103
- Fixes for Ruby 2.1 packaging guidelines (#1107150)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7-102
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7-101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Josef Stribny <jstribny@redhat.com> - 1.7.7-100
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to JSON 1.7.7

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 06 2012 Xavier Lamien <laxathom@lxtnow.net> - 1.7.5-1
- Update to Upstream release.
- Add mtasaka changes request.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jan 22 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.6.5-1
- 1.6.5

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 1.4.6-2
- Rebuilt for gcc bug 634757

* Sat Sep 18 2010 Xavier Lamien <laxathom@fedoraproject.org> - 1.4.6-1
- Update release.
- Enabled test stage.

* Fri Jun 11 2010 Xavier Lamien <laxathom@fedoraproject.org> - 1.4.3-3
- Move ruby's site_lib editor to ruby-json-gui.

* Mon May 10 2010 Xavier Lamien <laxathom@fedoraproject.org> - 1.4.3-2
- Move editor out of ruby-json sub-package.

* Sun May 09 2010 Xavier Lamien <laxathom@fedoraproject.org> - 1.4.3-1
- Update release.
- Split-out json editor.

* Thu Oct 29 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.9-1
- Update release.

* Wed Aug 12 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.7-3
- Fix gem scripts and install_dir.
- Enable %%check stage.

* Wed Aug 05 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.7-2
- Rebuild in correct buildir process.
- Add sub packages.

* Mon Aug 03 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.7-1
- Update release.

* Sat Jun 06 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.6-1
- Update release.

* Tue May 12 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.5-1
- Update release.

* Thu Apr 02 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.4-1
- Update release.

* Sat Jul 12 2008 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.3-1
- Initial RPM release.
