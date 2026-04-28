# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global	mainver		1.18.10
#%%global	prever		.rc4

%global	baserelease		1
%global	prerpmver		%(echo "%{?prever}" | sed -e 's|\\.||g')

%global	gem_name	nokogiri

%undefine __brp_mangle_shebangs

Summary:	An HTML, XML, SAX, and Reader parser
Name:		rubygem-%{gem_name}
Version:	%{mainver}
Release:	%{?prever:0.}%{baserelease}%{?prever:.%{prerpmver}}%{?dist}

# SPDX confirmed
# MIT: see LICENSE.md
# Apache-2.0
#  1.12.0 bundles forked and modified gumbo -
#  see gumbo-parser/src/attribute.c and ext/nokogiri/gumbo.c
#  also lib/nokogiri/html5 is licensed under ASL 2.0
License:	MIT AND Apache-2.0
Provides:	bundled(gumbo-parser) = 0.10.1

URL:		https://nokogiri.org
Source0:	https://rubygems.org/gems/%{gem_name}-%{mainver}%{?prever}.gem
# %%{SOURCE2} %%{name} %%{version}
Source1:	rubygem-%{gem_name}-%{version}%{?prever}-full.tar.gz
Source2:	nokogiri-create-full-tarball.sh
# Shut down libxml2 version unmatching warning
Patch0:	%{name}-1.11.0.rc4-shutdown-libxml2-warning.patch
BuildRequires:	ruby(release)
BuildRequires:	ruby(rubygems)
##
## For %%check
BuildRequires:	rubygem(minitest)
%if !0%{?rhel}
# For test/xml/test_document_encoding.rb
# Drop rubygem(rubyzip) build dependency in RHEL
BuildRequires:	rubygem(rubyzip)
%endif
BuildRequires:	rubygems-devel
Obsoletes:		ruby-%{gem_name} <= 1.5.2-2
#BuildRequires:	ruby(racc)
##
# test suite uses EUC-JP, SHIFT-JIS, etc
BuildRequires:	glibc-all-langpacks
## Others
BuildRequires:	gcc
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	ruby-devel
# ruby27 needs this explicitly
BuildRequires:	rubygem(racc)

%description
Nokogiri parses and searches XML/HTML very quickly, and also has
correctly implemented CSS3 selector support as well as XPath support.

Nokogiri also features an Hpricot compatibility layer to help ease the change
to using correct CSS and XPath.

%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.

%package	-n ruby-%{gem_name}
Summary:	Non-Gem support package for %{gem_name}
Requires:	%{name} = %{version}-%{release}
Provides:	ruby(%{gem_name}) = %{version}-%{release}

%description	-n ruby-%{gem_name}
This package provides non-Gem support for %{gem_name}.

%global	version	%{mainver}%{?prever}

%prep
%setup -q -n %{gem_name}-%{version} -a 1
cp -a %{gem_name}-%{version}/{.,*} .
mv ../%{gem_name}-%{version}.gemspec .

# patches
%patch -P0 -p1

# remove bundled external libraries
sed -i \
	-e 's|, "ports/archives/[^"][^"]*"||g' \
	-e 's|, "patches/[^"][^"]*"||g' \
	%{gem_name}-%{version}.gemspec
# Make sure gem build will complain later if the previous regex is not enough.
rm -rf \
	ports \
	patches \
	%{nil}

# Actually not needed when using system libraries
sed -i -e '\@mini_portile@d' %{gem_name}-%{version}.gemspec

# Don't use mini_portile2, but build libgumbo.a first and
# tell extconf.rb the path to the archive
sed -i \
	ext/nokogiri/extconf.rb \
	-e "s@^\(def process_recipe.*\)\$@\1 ; return true@" \
	-e "s@^\([ \t]*append_cppflags\).*gumbo.*\$@\1(\"-I$(pwd)/gumbo-parser/src\")@" \
	-e "\@libs.*gumbo@s@File\.join.*@\"$(pwd)/gumbo-parser/src/libgumbo.a\"@" \
	-e "\@LIBPATH.*gumbo@s|^\(.*\)\$|# \1|" \
	%{nil}

# #line directive can confuse debuginfo, removing for now
sed -i \
	gumbo-parser/src/char_ref.c \
	-e '\@^#line [0-9]@s|^\(.*\)$|// \1|'

# Compile libgumbo.a with -fPIC
sed -i \
	gumbo-parser/src/Makefile \
	-e 's|^\(CFLAGS.*=.*\)$|\1 -fPIC|'

%build
# Ummm...
env LANG=C.UTF-8 gem build %{gem_name}-%{version}.gemspec

# 1.6.0 needs this
export NOKOGIRI_USE_SYSTEM_LIBRARIES=yes

%set_build_flags
# First build libgumbo.a
pushd gumbo-parser/src/
make libgumbo.a
popd

%gem_install

# Permission
chmod 0644 .%{gem_dir}/cache/%{gem_name}-%{mainver}%{?prever}.gem

# Remove precompiled Java .jar file
find .%{gem_instdir}/lib/ -name '*.jar' -delete
# For now remove JRuby support
rm -rf .%{gem_instdir}/ext/java


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}

# Also first copy these, clean up later
cp -a ./gumbo-parser  %{buildroot}%{gem_instdir}/

# Remove backup file
find %{buildroot} -name \*.orig_\* | xargs rm -vf

# move arch dependent files to %%gem_extdir
mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a ./%{gem_extdir_mri}/* %{buildroot}%{gem_extdir_mri}/

pushd %{buildroot}
rm -f .%{gem_extdir_mri}/{gem_make.out,mkmf.log}
popd


# move bin/ files
mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
	%{buildroot}%{_bindir}/

# remove all shebang
for f in $(find %{buildroot}%{gem_instdir} -name \*.rb)
do
	sed -i -e '/^#!/d' $f
	chmod 0644 $f
done

# Copy document files from full source
cp -p [A-Z]* %{buildroot}%{gem_instdir}/

# cleanups
# Remove bundled gumbo parser
pushd %{buildroot}%{gem_instdir}
rm -rf \
	Gemfile* \
	Rakefile \
	Vagrantfile \
	dependencies.yml \
	ext \
	*gemspec \
	patches \
	ports \
	%{nil}
pushd gumbo-parser
find . -type f | \
	grep -v CHANGES.md | \
	grep -v THANKS | \
	grep -v README.md | \
	xargs rm -f

popd
rm -f %{buildroot}%{gem_cache}

%check
# Ah....
# test_exslt(TestXsltTransforms) [./test/test_xslt_transforms.rb:93]
# fails without TZ on sparc
export TZ="Asia/Tokyo"
#???
LANG=C.UTF-8

# Copy test files from full tarball
cp -a test/ ./%{gem_instdir}
pushd ./%{gem_instdir}

# Remove unneeded simplecov coverage test
sed -i test/helper.rb \
	-e '\@^  require.*simplecov@,\@^  end$@s|^|#|'

# Remove minitest-reporters. It does not provide any additional value while
# it blows up the dependency chain.
sed -i '/require..minitest.reporters./ s/^/#/' test/helper.rb
sed -i '/Minitest::Reporters/ s/^/#/' test/helper.rb

# PPC64LE with ruby3.1 does not seem to support GC.compact
%ifarch ppc64le
export NOKOGIRI_TEST_GC_LEVEL=major
%endif
%ifarch s390x
# With ruby 3.2 GC_LEVEL=compact seems to cause segfault:
# change to major for now
if pkg-config --atleast-version 3.2 ruby ; then
export NOKOGIRI_TEST_GC_LEVEL=major
fi
%endif

env \
	RUBYLIB=".:lib:test:%{buildroot}%{gem_extdir_mri}" \
	ruby \
	-e \
	"require 'test/helper' ; Dir.glob('test/**/test_*.rb'){|f| require f}" || \
	exit 1

for f in $SKIPTEST
do
	mv $f.skip $f
done

popd

%files
%{_bindir}/%{gem_name}
%{gem_extdir_mri}/

%dir	%{gem_instdir}/
%license	%{gem_instdir}/LICENSE*.md
%doc	%{gem_instdir}/CHANGELOG.md
%doc	%{gem_instdir}/README.md

%{gem_instdir}/bin/
%{gem_instdir}/lib/

%dir	%{gem_instdir}/gumbo-parser
%dir	%{gem_instdir}/gumbo-parser/src
%doc	%{gem_instdir}/gumbo-parser/[A-Z]*
%license	%{gem_instdir}/gumbo-parser/src/README.md

%{gem_dir}/specifications/%{gem_name}-%{mainver}%{?prever}.gemspec

%files	doc
%defattr(-,root,root,-)
%doc	%{gem_instdir}/CODE_OF_CONDUCT.md
%doc	%{gem_instdir}/CONTRIBUTING.md
%doc	%{gem_instdir}/ROADMAP.md
%doc	%{gem_instdir}/SECURITY.md
%doc	%{gem_dir}/doc/%{gem_name}-%{mainver}%{?prever}/

%changelog
* Mon Sep 15 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.18.10-1
- 1.18.10

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 21 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.18.9-1
- 1.18.9

* Wed Apr 23 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.18.8-1
- 1.18.8

* Mon Apr 07 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.18.7-1
- 1.18.7

* Sat Mar 29 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.18.6-1
- 1.18.6

* Wed Mar 26 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.18.5-2
- Suppress warnings from Nokogiri::VERSION_INFO (bug 2354787)

* Thu Mar 20 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.18.5-1
- 1.18.5

* Sun Mar 16 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.18.4-1
- 1.18.4

* Wed Feb 19 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.18.3-1
- 1.18.3

* Mon Jan 20 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.18.2-1
- 1.18.2

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 07 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.18.1-2
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.4

* Mon Dec 30 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.18.1-1
- 1.18.1

* Sat Dec 28 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.18.0-1
- 1.18.0

* Fri Dec 13 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.17.2-1
- 1.17.2

* Wed Dec 11 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.17.1-1
- 1.17.1

* Mon Dec 09 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.17.0-1
- 1.17.0

* Thu Dec 05 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.16.8-1
- 1.16.8

* Wed Jul 31 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.16.7-1
- 1.16.7

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 16 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.16.6-1
- 1.16.6

* Tue May 14 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.16.5-1
- 1.16.5

* Thu Apr 25 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.16.4-2
- Make rubygem-minizip testsuite dependency optional, drop on RHEL
  (Patch by Jun Aruga <jaruga@redhat.com>)

* Thu Apr 11 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.16.4-1
- 1.16.4

* Sun Mar 17 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.16.3-1
- 1.16.3

* Mon Feb 05 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.16.2-1
- 1.16.2

* Sun Feb 04 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.16.1-1
- 1.16.1

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.16.0-2
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.3

* Fri Dec 29 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.16.0-1
- 1.16.0

* Sat Nov 18 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.15.5-1
- 1.15.5
- Backport upstream patch for libxml2 2.12.0 error handling change

* Sat Aug 12 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.15.4-1
- 1.15.4

* Sun Aug  6 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.15.3-4
- Prefer upstream patch for the previous change

* Fri Aug  4 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.15.3-3
- Support MiniTest 5.19+

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul  6 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.15.3-1
- 1.15.3

* Thu May 25 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.15.2-1
- 1.15.2

* Sun May 21 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.15.1-1
- 1.15.1

* Tue May 16 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.15.0-1
- 1.15.0

* Fri May 12 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.4-1
- 1.14.4
- Note that CVE-2022-34169 is for vendored xalan-j, not affecting Fedora
  nokogiri

* Wed Apr 12 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.3-1
- 1.14.3
- SPDX confirmed

* Tue Feb 14 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.2-1
- 1.14.2

* Tue Jan 31 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.1-1
- 1.14.1

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan 15 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.0-1
- 1.14.0

* Tue Jan 03 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.13.10-2.1
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.2

* Sun Dec 25 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.13.10-2
- Use %%gem_extdir_mri instead of ext for %%check due to ruby3.2 change
  for ext cleanup during build

* Fri Dec  9 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.13.10-1
- 1.13.10
- Address CVE-2022-23476

* Thu Oct 20 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.13.9-2
- s390x: change GC_LEVEL to major on ruby3.2 for now

* Thu Oct 20 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.13.9-1
- 1.13.9

* Wed Jul 27 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.13.8-1
- 1.13.8

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.7-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.13.7-2
- Bump release

* Wed Jul 13 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.13.7-1
- 1.13.7

* Tue May 10 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.13.6-1
- 1.13.6
- Addresses CVE-2022-29181

* Thu May  5 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.13.5-1
- 1.13.5

* Thu Apr 14 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.13.4-1
- 1.13.4
- Addresses CVE-2022-24836

* Tue Feb 22 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.13.3-1
- 1.13.3

* Wed Jan 26 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.13.1-2
- Set NOKOGIRI_TEST_GC_LEVEL to major on ppc64le as
  ruby31 does not seem to support GC.compat on the platform

* Wed Jan 26 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.13.1-1.2
- F-36: rebuild against ruby31

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 14 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.13.1-1
- 1.13.1

* Sun Jan  9 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.13.0-1
- 1.13.0

* Tue Sep 28 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.12.5-1
- 1.12.5

* Wed Sep  1 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.12.4-1
- 1.12.4

* Thu Aug 12 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.12.3-1
- 1.12.3

* Sat Aug  7 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.12.2-1
- 1.12.2

* Sat Aug  7 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.12.1-1
- 1.12.1

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.7-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jun 19 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.11.7-1
- 1.11.7

* Sun May 16 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.11.4-1
- 1.11.4

* Fri May 07 2021 Vít Ondruch <vondruch@redhat.com> - 1.11.3-2
- Remove rubygem(minitest-reporters) dependency.

* Thu Apr  8 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.11.3-1
- 1.11.3

* Fri Mar 12 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.11.2-1
- 1.11.2

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan  8 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.11.1-1
- 1.11.1

* Wed Jan 06 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.11.0-1.1
- F-34: rebuild against ruby 3.0

* Wed Jan  6 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.11.0-1
- 1.11.0

* Thu Dec 31 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.11.0-0.1.rc4
- 1.11.0.rc4

* Thu Oct 22 2020 Vít Ondruch <vondruch@redhat.com> - 1.10.10-2
- Drop unnecessary rubygem(pkg-config) dependency.

* Sat Aug  8 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.10.10-1
- 1.10.10

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.9-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Mar  6 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.10.9-1
- 1.10.9

* Thu Feb 13 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.10.8-1
- 1.10.8

* Fri Jan 31 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.10.7-3
- Also Requires rubygem(racc)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.7-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.10.7-2
- F-32: rebuild against ruby27

* Fri Dec  6 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.10.7-1
- 1.10.7

* Tue Nov  5 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.10.5-1
- 1.10.5

* Fri Aug 16 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.10.4-1
- 1.10.4

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.3-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 23 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.10.3-1
- 1.10.3

* Tue Mar 26 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.10.2-1
- 1.10.2

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.10.1-1
- 1.10.1

* Mon Jan 21 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.10.0-2
- F-30: rebuild against ruby26

* Wed Jan  9 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.10.0-1
- 1.10.0

* Mon Dec 31 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.1-1
- 1.9.1

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.8.5-1.1
- Use C.UTF-8 locale
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Tue Oct  9 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.5-1
- 1.8.5

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jul  6 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.4-1
- 1.8.4

* Mon Jun 18 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.3-1
- 1.8.3

* Tue Feb  6 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.2-1
- 1.8.2

* Thu Jan 25 2018 Yaakov Selkowitz <yselkowi@redhat.com> - 1.8.1-1.3
- Drop compatibility with old releases

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1.8.1-1.2
- Rebuilt for switch to libxcrypt

* Wed Jan 03 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.1-1.1
- F-28: rebuild for ruby25

* Wed Sep 20 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.1-1
- 1.8.1

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 12 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.0-1
- 1.8.0

* Fri May 12 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.7.2-1
- 1.7.2

* Tue Mar 21 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.7.1-1
- 1.7.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 11 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.7.0.1-2
- F-26: rebuild for ruby24

* Thu Jan  5 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.7.0.1-1
- 1.7.0.1

* Thu Dec 29 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.7.0-1
- 1.7.0

* Mon Oct 10 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.8.1-1
- 1.6.8.1

* Fri Jul  1 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.8-3
- Kill pkg-config runtime redundant dependency (bug 1349893)

* Mon Jun 20 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.8-2
- 1.6.8

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.7.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.7.2-1
- 1.6.7.2

* Mon Jan 11 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.7-0.4.rc4
- F-24: rebuild against ruby23

* Fri Dec 11 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.7-0.3.rc3
- Shutdown libxml2 version mismatch warning

* Tue Dec  8 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.7-0.2.rc3
- Rebuild against new libxml2, to make rspec test succeed

* Thu Sep 24 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.7-0.1.rc3
- 1.6.7.rc3

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.6.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jan 25 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.6.2-1
- 1.6.6.2

* Fri Jan 23 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.6.1-1
- 1.6.6.1

* Thu Jan 15 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.5-2
- Rebuild for ruby 2.2

* Mon Dec  1 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.5-1
- 1.6.5

* Fri Nov  7 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.4.1-1
- 1.6.4.1

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3.1-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.3.1-1
- 1.6.3.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.2.1-1
- 1.6.2.1

* Thu Apr 17 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.1-2
- F-21: rebuild for ruby 2.1 / rubygems 2.2

* Wed Dec 25 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.1-1
- 1.6.1

* Fri Oct  4 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.0-1
- 1.6.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.9-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 28 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.5.9-1
- 1.5.9

* Tue Mar 26 2013 Vít Ondruch <vondruch@redhat.com> - 1.5.6-3
- Use %%{gem_extdir_mri} instead of %%{gem_extdir}.

* Sat Feb 23 2013 Vít Ondruch <vondruch@redhat.com> - 1.5.6-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  1 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.5.6-1
- A Happy New Year
- 1.5.6

* Fri Aug 17 2012 Vít Ondruch <vondruch@redhat.com> - 1.5.5-2
- Rebuilt againts libxml2 2.9.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.5-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.5.5-1
- 1.5.5

* Mon May 28 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.5.2-3
- Fix Obsoletes (bug 822931)

* Mon Apr  9 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.5.2-1
- 1.5.2

* Tue Apr 03 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.5.0-3
- Fix conditionals for F17 to work for RHEL 7 as well.

* Tue Jan 24 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.5.0-2
- F-17: rebuild for ruby19
- For now aviod build failure by touching some files

* Wed Jan 18 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.5.0-1
- 1.5.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-0.5.beta4.1
- F-17: Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 26 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.5.0-0.5.beta4
- Remove unneeded patch

* Fri Mar 18 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.5.0-0.4.beta4
- Patch for newer rake to make testsuite run

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-0.3.beta4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 30 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5.0-0.3.beta4
- 1.5.0.beta.4

* Tue Dec  7 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5.0-0.2.beta3
- 1.5.0.beta.3

* Sun Oct 17 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5.0-0.1.beta2
- Try 1.5.0.beta.2

* Fri Jul 30 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.4.3.1-1
- 1.4.3.1

* Wed May 26 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.4.2-1
- 1.4.2

* Thu Apr 29 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.4.1-2
- Fix build failure with libxml2 >= 2.7.7

* Tue Dec 15 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.4.1-1
- 1.4.1

* Mon Nov  9 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.4.0-1
- 1.4.0

* Sat Aug 22 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.3.3-2
- Fix test failure on sparc

* Wed Jul 29 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.3.3-1
- 1.3.3

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.3.2-3
- F-12: Mass rebuild

* Thu Jul  2 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.3.2-2
- Enable test
- Recompile with -O2

* Thu Jun 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.3.2-1
- 1.3.2

* Thu Jun 11 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.3.1-1
- 1.3.1

* Thu Mar 26 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.3-1
- 1.2.3

* Thu Mar 19 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.2-1
- 1.2.2

* Thu Mar 12 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.1-1
- 1.2.1

* Tue Feb 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.1.1-2
- F-11: Mass rebuild

* Thu Jan 15 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.1.1-1
- 1.1.1

* Thu Dec 25 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.1.0-1
- Initial packaging

