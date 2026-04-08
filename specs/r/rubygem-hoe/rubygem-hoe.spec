# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name hoe
%undefine _changelog_trimtime

Summary:    	Hoe is a simple rake/rubygems helper for project Rakefiles
Name:       	rubygem-%{gem_name}
Version:    	4.6.0
Release:    	1%{?dist}
# SPDX confirmed
License:    	MIT
URL:        	https://github.com/seattlerb/hoe
Source0:    	http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Rescue Hoe.spec task when Manifest.txt
# seattlerb-Bugs-28571
Patch0:		rubygem-hoe-3.0.6-rescue-missing-Manifest.patch
# Workaround for "Fedora" ruby 2.7 psych
# ruby -e 'require "psych"; gem "psych"; require "psych";' produces 
# /usr/share/gems/gems/psych-3.1.0/lib/psych/parser.rb:34:in `<class:Parser>': 
# superclass mismatch for class Mark (TypeError)
Patch1:		rubygem-hoe-3.21.0-always-search-gem-for-psych.patch

Requires:	ruby(release)
BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
# %%check
BuildRequires:	rubygem(minitest)
BuildRequires:	rubygem(rake)
BuildArch:  	noarch
Provides:   	rubygem(%{gem_name}) = %{version}

%description
Hoe is a rake/rubygems helper for project Rakefiles. It helps generate
rubygems and includes a dynamic plug-in system allowing for easy
extensibility. Hoe ships with plug-ins for all your usual project
tasks including rdoc generation, testing, packaging, and deployment.
Plug-ins Provided:
* Hoe::Clean
* Hoe::Debug
* Hoe::Deps
* Hoe::Flay
* Hoe::Flog
* Hoe::Inline
* Hoe::Package
* Hoe::Publish
* Hoe::RCov
* Hoe::Signing
* Hoe::Test
See class rdoc for help. Hint: ri Hoe

%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}
mv ../%{gem_name}-%{version}.gemspec .

# Patches
%patch -P0 -p0
%patch -P1 -p1

# Allow RubyInline 3.8.4
sed -i -e '/RubyInline/s|~> 3\.9|>= 3.8.4|' \
	lib/hoe/inline.rb

# Allow rake-compiler 1.0 and above
sed -i -e '/rake-compiler/s|~> 1\.0|>= 1.0|' \
	lib/hoe/compiler.rb

%build
gem build %{gem_name}-%{version}.gemspec
%gem_install

pushd .%{gem_instdir}
# Umm...
%_fixperms .

popd

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{_prefix}/* \
	%{buildroot}%{_prefix}/

chmod 0644 %{buildroot}%{gem_dir}/cache/*gem

find %{buildroot}/%{gem_instdir}/bin -type f | xargs chmod 0755
find %{buildroot}/%{_bindir} -type f | xargs chmod 0755

chmod 0755 %{buildroot}/%{gem_instdir}/template/bin/file_name.erb
# Don't remove template files
#rm -f %{buildroot}/%{gem_instdir}/template/.autotest.erb

rm -f %{buildroot}%{gem_cache}
pushd %{buildroot}%{gem_instdir}
rm -rf \
	.autotest \
	Manifest.txt \
	Rakefile \
	test/ \
	%{nil}
popd

%check
pushd .%{gem_instdir}

# Save original Rakefile
sed -i.isolate -e \
	'/Hoe\.plugin :isolate/d' Rakefile
# Make sure that hoe currently building are loaded
export RUBYLIB=$(pwd)/lib

unset SOURCE_DATE_EPOCH
rake test -v --trace

mv Rakefile{.isolate,}
popd

%files
%{_bindir}/sow
%dir %{gem_instdir}/
%{gem_instdir}/bin/
%{gem_instdir}/lib/
%{gem_instdir}/template/
%{gem_spec}
%doc %{gem_instdir}/[A-Z]*

%files	doc
%{gem_docdir}

%changelog
* Thu Jan 29 2026 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.6.0-1
- 4.6.0

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Sat Jan 03 2026 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.5.1-1
- 4.5.1

* Tue Dec 30 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.5.0-1
- 4.5.0

* Thu Aug 07 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.3.0-1
- 4.3.0

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 26 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.2.3-2
- Upstream patch for rubygems 3.6.7 change wrt setting DEFAULT_SOURCE_DATE_EPOCH

* Sat Mar 29 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.2.3-1
- 4.2.3

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 30 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.2.2-1
- 4.2.2

* Thu May 23 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.2.1-1
- 4.2.1

* Sun May 05 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.2.0-4
- Backport upstream PR for rake 13.2 OpenStruct removal change

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 16 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.2.0-1
- 4.2.0

* Wed Dec  6 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.1.0-1
- 4.1.0

- Fri Jul 28 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.0.5-1
- 4.0.5

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun  8 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.0.4-1
- 4.0.4

* Thu May  4 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.0.3-1
- 4.0.3

* Sun Jan 29 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.0.2-1
- 4.0.2

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan  1 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.0.1-1
- 4.0.1

* Fri Oct 21 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.26.0-1
- 3.26.0

* Fri Aug 19 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.25.0-1
- 3.25.0

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.24.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 21 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.24.0-1
- 3.24.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.23.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan  7 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.23.1-1
- 3.23.1

* Sun Jul 25 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.23.0-2
- Rebuild for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 21 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.23.0-1
- 3.23.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.22.3-1
- 3.22.3

* Fri Sep  4 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.22.2-1
- 3.22.2

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Feb 14 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.22.1-1
- 3.22.1

* Fri Jan 31 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.21.0-3
- Workaround for Fedora ruby 27 psych behavior
  - Always gem "psych" beforehand

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.21.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 14 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.21.0-1
- 3.21.0

* Mon Nov 25 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.20.0-1
- 3.20.0

* Tue Sep 17 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.18.1-1
- 3.18.1

* Thu Aug 15 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.18.0-3
- unset SOURCE_DATE_EPOCH for %%check

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 19 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.18.0-1
- 3.18.0

* Mon Mar 18 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.17.2-1
- 3.17.2

* Tue Mar 12 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.17.1-3
- Patches from the upstream to fix build with ruby 2.6

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 17 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.17.1-1
- 3.17.1

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri May  4 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.17.0-1
- 3.17.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 31 2017 Mamoru TASAKA <mtasaka@tbz.t-com.ne.jp> - 3.16.2-1
- 3.16.2

* Fri Aug  4 2017 Mamoru TASAKA <mtasaka@tbz.t-com.ne.jp> - 3.16.1-1
- 3.16.1

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.15.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 11 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.15.3-2
- relax rake dependency

* Thu Dec  1 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.15.3-1
- 3.15.3

* Fri Oct 14 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.15.2-1
- 3.15.2

* Fri Jun 24 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.15.1-1
- 3.15.1

* Thu Apr 14 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.15.0-1
- 3.15.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 21 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.14.2-1
- 3.14.2

* Sun Sep 13 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.14.0-1
- 3.14.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb  5 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.13.1-1
- 3.13.1

* Fri Oct  3 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.13.0-1
- 3.13.0

* Fri Jun  6 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.12.0-1
- 3.12.0

* Thu Apr 10 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.11.0-1
- 3.11.0

* Mon Mar 17 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.10.0-1
- 3.10.0

* Sat Feb 15 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.9.0-1
- 3.9.0

* Wed Jan 29 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.8.1-1
- 3.8.1

* Tue Dec 24 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.7.3-1
- 3.7.3

* Thu Dec 12 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.7.2-1
- 3.7.2

* Fri Aug 23 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.7.1-1
- 3.7.1

* Thu Aug 15 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.7.0-1
- 3.7.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Apr 28 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.6.0-1
- 3.6.0

* Thu Apr 11 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.3-2
- 3.5.3

* Wed Apr  3 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.2-1
- 3.5.2

* Thu Mar  5 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.1-2
- F-19: Rebuild for ruby 2.0.0

* Mon Mar  4 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.1-1
- 3.5.1

* Fri Jan 25 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.0-1
- 3.5.0

* Wed Jan  2 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-1
- 3.4.0

* Tue Jan  1 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.0-1
- A Happy New Year
- 3.3.0

* Thu Oct 11 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 3.1.0-1
- 3.1.0

* Wed Sep 12 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 3.0.8-1
- 3.0.8

* Tue Aug 14 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 3.0.7-1
- 3.0.7

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 31 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 3.0.6-1
- 3.0.6

* Tue Jan 24 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.12.5-5
- Require rubyforge again

* Sun Jan 22 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.12.5-4
- Rebuild against ruby 1.9

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 26 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.12.5-1
- 2.12.5

* Sun Dec  4 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.12.4-1
- 2.12.4

* Fri Sep  9 2011 Mamoru Tasaka <mtasaka@fedroaproject.org> - 2.12.3-1
- 2.12.3

* Sun Aug 28 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.12.2-1
- 2.12.2

* Thu Aug 18 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.12.0-2
- Fix glob order issue under test/

* Thu Aug 18 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.12.0-1
- 2.12.0

* Sun Jul  3 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.10.0-1
- 2.10.0

* Sun Jun 26 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.9.6-1
- 2.9.6

* Sun Apr  3 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.9.4-1
- 2.9.4

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.9.1-1
- 2.9.1

* Wed Feb  2 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.9.0-1
- 2.9.0

* Fri Dec 10 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.8.0-1
- 2.8.0

* Sat Nov 20 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.7.0-2
- 2.7.0

* Fri Sep 17 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.6.2-3
- Rescue Hoe.spec task when Manifest.txt is missing

* Sat Sep  4 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.6.2-2
- Kill unneeded patch

* Fri Sep  3 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.6.2-1
- 2.6.2
- Drop development dependency
- Split documentation files

* Sat Jun  5 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.6.1-1
- 2.6.1

* Thu Jun  3 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.6.0-3
- Use upstreamed patch for rubyforge-without-account.patch
- Fix test failure related to glob
  (build failed with Matt's mass build, also failed on koji)

* Wed Apr 28 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.6.0-1
- 2.6.0
- gemcutter dependency dropped

* Thu Mar  4 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.5.0-3
- Enable test
- Some cleanups

* Mon Feb 15 2010 Darryl L. Pierce <dpierce@redhat.com> 2.5.0-2
- Updated the dependency on rubygem-rubyforge to >= 2.0.3.

* Mon Feb 15 2010 Darryl L. Pierce <dpierce@redhat.com> 2.5.0-1
- Added dependency on rubygem-gemcutter >= 0.2.1.
- Added dependency on rubygem-minitest >= 1.4.2.
- Release 2.5.0 of Hoe.

* Sat Aug  8 2009 Darryl L. Pierce <dpierce@redhat.com> - 2.3.3-1
- Release 2.3.3 of Hoe.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul  1 2009 Darryl L. Pierce <dpierce@redhat.com> - 2.3.2-1
- Release 2.3.2 of Hoe.

* Fri Jun 26 2009 Darryl L. Pierce <dpierce@redhat.com> - 2.3.1-1
- Release 2.3.1 of Hoe.

* Thu Jun 18 2009 Darryl L. Pierce <dpierce@redhat.com> - 2.2.0-1
- Release 2.2.0 of Hoe.

* Mon Jun 15 2009 Darryl L. Pierce <dpierce@redhat.com> - 2.1.0-1
- Release 2.1.0 of Hoe.

* Wed Jun  3 2009 Darryl L. Pierce <dpierce@redhat.com> - 2.0.0-1
- Release 2.0.0 of Hoe.

* Fri Apr 17 2009 Darryl L. Pierce <dpierce@redhat.com> - 1.12.2-1
- Release 1.12.2 of Hoe.

* Wed Apr  1 2009 Darryl L. Pierce <dpierce@redhat.com> - 1.12.1-1
- Release 1.12.1 of Hoe.

* Tue Mar 17 2009 Darryl L. Pierce <dpierce@redhat.com> - 1.11.0-1
- Release 1.11.0 of Hoe.

* Tue Mar 10 2009 Darryl L. Pierce <dpierce@redhat.com> - 1.10.0-1
- Release 1.10.0 of Hoe.

* Fri Feb 27 2009 Darryl L. Pierce <dpierce@redhat.com> - 1.9.0-1
- Release 1.9.0 of Hoe.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 21 2009 Darryl L. Pierce <dpierce@redhat.com> - 1.8.3-1
- Release 1.8.3 of Hoe.

* Mon Oct 27 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.8.2-1
- Release 1.8.2 of Hoe.

* Thu Oct 23 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.8.1-2
- Last build failed.

* Thu Oct 23 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.8.1-1
- Release 1.8.1 of the gem.

* Mon Oct 13 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.8.0-1
- Release 1.8.0 of the gem.

* Tue Jul 01 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.7.0-1
- Release 1.7.0 of the gem.

* Wed Jun 18 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.6.0-1
- Release 1.6.0 of the gem.

* Mon Jun 09 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.5.3-2
- Fixed the dependency for the newer version of rubygem-rubyforge.

* Tue Jun 03 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.5.3-1
- New release of Hoe.

* Wed May 14 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.5.1-6
- Fixed the build, which failed only on devel.

* Wed May 14 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.5.1-5
- First official build.

* Mon May 12 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.5.1-4
- Update for Fedora 8 and 9.

* Tue Apr 29 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.5.1-3
- Fixed the license to read MIT.

* Mon Apr 28 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.5.1-2
- Updated the spec to comply with Ruby packaging guidelines.

* Fri Apr 18 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.5.1-1
- Initial package
