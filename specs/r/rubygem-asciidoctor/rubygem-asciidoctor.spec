# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name asciidoctor
%global mandir %{_mandir}/man1

%define pre %nil
%global gittag v%{version}%{pre}

Summary: A fast, open source AsciiDoc implementation in Ruby
Name: rubygem-%{gem_name}
Version: 2.0.26
Release: 1%{?dist}
License: MIT
URL: https://asciidoctor.org
Source0: https://github.com/asciidoctor/asciidoctor/archive/%{gittag}/%{gem_name}-%{version}%{pre}.tar.gz
%if 0%{?el7}
Requires: ruby(release)
BuildRequires: ruby(release)
%endif
BuildRequires: rubygems-devel
BuildRequires: ruby(rubygems)
%if ! 0%{?rhel}
# Dependencies aren't available on EPEL
BuildRequires: rubygem(coderay)
BuildRequires: rubygem(concurrent-ruby)
BuildRequires: rubygem(erubi)
BuildRequires: rubygem(haml)
BuildRequires: rubygem(logger)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(nokogiri)
BuildRequires: rubygem(rouge)
BuildRequires: rubygem(slim)
BuildRequires: rubygem(tilt)
%endif
BuildArch: noarch
Provides: asciidoctor = %{version}
%if 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%if %{?pre:1}
%global gem_instdir() %{gem_dir}/gems/%{gem_name}-%{version}%{pre}
%global gem_cache   %{gem_dir}/cache/%{gem_name}-%{version}%{pre}.gem
%global gem_spec    %{gem_dir}/specifications/%{gem_name}-%{version}%{pre}.gemspec
%global gem_docdir  %{gem_dir}/doc/%{gem_name}-%{version}%{pre}
%endif

%description
A fast, open source text processor and publishing toolchain, written in Ruby,
for transforming AsciiDoc markup into HTML 5, DocBook 4.5, DocBook 5.0 and
custom output formats. The transformation from AsciiDoc to custom output
formats is performed by running the nodes in the parsed document tree through a
collection of templates written in a template language supported by Tilt.

%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
%autosetup -n %{gem_name}-%{version}%{pre} -p1

# Include tests in the gem, they're disabled by default
sed -i -e 's/#\(s\.test_files\)/\1/' %{gem_name}.gemspec

# Fix shebang (avoid Requires: /usr/bin/env)
sed -i -e 's|#!/usr/bin/env ruby|#!/usr/bin/ruby|' bin/%{gem_name}

# ref: https://github.com/asciidoctor/asciidoctor/issues/4684
# the upstream plans to remove logger dep, but for now
# add logger dep explicitly for ruby3_5
%gemspec_add_dep -g logger -s ./%{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install -n %{gem_name}-%{version}%{pre}.gem

%check
pushd .%{gem_instdir}

%if ! 0%{?rhel}
# Asciidoctor tests require Minitest 5, so we can't run them on EPEL
#
# disable tests which require open-uri-cached gem
sed -Ei "/test 'should cache remote (SVG|image) when allow-uri-read, cache-uri, and (inline option|data-uri) are set' do/a \\
      skip('open-uri-cached gem is not avaiable on Fedora')" test/blocks_test.rb
LANG=C.UTF-8 ruby -I"lib:test" -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
%endif
popd

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
       %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
       %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{mandir}
cp -a .%{gem_instdir}/man/*.1 \
       %{buildroot}%{mandir}/

%files
%dir %{gem_instdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/asciidoctor.gemspec
%exclude %{gem_instdir}/man
%exclude %{gem_instdir}/test
%exclude %{gem_instdir}/features
%license %{gem_instdir}/LICENSE
%doc %{gem_instdir}/CHANGELOG.adoc
%doc %{gem_instdir}/README.*
%lang(de) %doc %{gem_instdir}/README-de.*
%lang(fr) %doc %{gem_instdir}/README-fr.*
%lang(ja) %doc %{gem_instdir}/README-jp.*
%lang(zh_CN) %doc %{gem_instdir}/README-zh_CN.*
%{gem_instdir}/data
%{_bindir}/*
%{gem_instdir}/bin
%{gem_libdir}
%{mandir}/*
%{gem_spec}

%files doc
%doc %{gem_docdir}

%changelog
* Mon Dec 15 2025 Dominik Mierzejewski <dominik@greysector.net> - 2.0.26-1
- updated to 2.0.26 (resolves rhbz#2265214)
- droped upstreamed patches

* Wed Nov 05 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.20-11
- Add logger dep for ruby3_5

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.20-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.20-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 14 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.20-8
- Backport upstream PR to remove base64 dependency
- Backport upstream fix for ruby34 formatting change

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.20-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.20-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 29 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.20-4
- Apply the upstream PR to support ruby 3.3 Logger

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu May 25 2023 Todd Zullinger <tmz@pobox.com> - 2.0.20-2
- improve ruby-2.5 compatibility (epel8)

* Thu May 18 2023 Todd Zullinger <tmz@pobox.com> - 2.0.20-1
- update to asciidoctor 2.0.20 (rhbz#2208089)

* Wed May 17 2023 Todd Zullinger <tmz@pobox.com> - 2.0.19-1
- update to asciidoctor 2.0.19 (rhbz#2208089)

* Mon Feb 20 2023 Todd Zullinger <tmz@pobox.com> - 2.0.18-3
- fixes for ruby-3.2.x and rouge-4.1.0 (rhbz#2171711)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Oct 15 2022 Todd Zullinger <tmz@pobox.com> - 2.0.18-1
- update to asciidoctor 2.0.18 (rhbz#1989716)

* Tue Aug 02 2022 Todd Zullinger <tmz@pobox.com> - 2.0.17-1
- update to asciidoctor 2.0.17 (rhbz#2113688)
- disable tests which require open-uri-cached gem

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Neal Gompa <ngompa@fedoraproject.org> - 2.0.15-3
- Simplify RHEL conditionals

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Apr 27 2021 Todd Zullinger <tmz@pobox.com> - 2.0.15-1
- update to asciidoctor 2.0.15
  Resolves: rhbz#1954314
- remove el6 conditionals

* Mon Apr 19 2021 Todd Zullinger <tmz@pobox.com> - 2.0.14-1
- Update to asciidoctor 2.0.14
  Resolves: rhbz#1950947

* Sat Apr 10 2021 Todd Zullinger <tmz@pobox.com> - 2.0.13-1
- Update to asciidoctor 2.0.13
  Resolves: rhbz#1948231

* Wed Jan 27 2021 Pavel Valena <pvalena@redhat.com> - 2.0.12-1
- Update to asciidoctor 2.0.12.
  Resolves: rhbz#1893940

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 19 2020 Vít Ondruch <vondruch@redhat.com> - 2.0.10-4
- Replace build time Erubis dependency by Erubi.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Sep 22 2019 Todd Zullinger <tmz@pobox.com> - 2.0.10-1
- Update to Asciidoctor 2.0.10

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 19 2019 Todd Zullinger <tmz@pobox.com> - 1.5.8-1
- Update to Asciidoctor 1.5.8 (resolves CVE-2018-18385)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.5.6.1-5
- Use C.UTF-8 locale
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 23 2018 Vít Ondruch <vondruch@redhat.com> - 1.5.6.1-3
- Enable entire test suite.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 24 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.5.6.1-1
- Update to Asciidoctor 1.5.6.1

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Vít Ondruch <vondruch@redhat.com> - 1.5.5-2
- Fix FTBFS.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Oct 14 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.5.5-1
- Update to Asciidoctor 1.5.5

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 05 2016 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.4-1
- Update to Asciidoctor 1.5.4 (rhbz#1295758)
- Use %%license macro
- Drop unnecessary "-p" flag to cp during %%install ("-a" already preserves
  timestamps)

* Mon Nov 02 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.3-1
- Update to Asciidoctor 1.5.3 (rhbz#1276851)
- Drop Fedora 19 and 20 macros (these distros are EOL)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Dec 05 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.2-1
- Update to Asciidoctor 1.5.2

* Fri Sep 19 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.1-1
- Update to Asciidoctor 1.5.1

* Tue Sep 09 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.0-1
- Update to Asciidoctor 1.5.0 final

* Fri Jun 06 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.0-0.4.preview.7
- Add %%{version} number to Provides: asciidoctor

* Fri Jun 06 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.0-0.3.preview.7
- Provide: asciidoctor
  https://github.com/asciidoctor/rubygem-asciidoctor-rpm/issues/5

* Tue May 20 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.0-0.2.preview.7
- Update to Asciidoctor 0.1.5.preview.7
- Drop unused patch

* Thu May 15 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.0-0.1.preview.6
- Update to Asciidoctor 0.1.5.preview.6
- Use HTTPS URLs
- Support Minitest 5
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Mark CHANGELOG, LICENSE, READMEs as %%doc
- Remove Rakefile in %%prep
- Remove Requires: /usr/bin/env

* Sun Sep 22 2013 Dan Allen <dan.j.allen@gmail.com> - 0.1.4-1
- Update to Asciidoctor 0.1.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 08 2013 Dan Allen <dan.j.allen@gmail.com> - 0.1.3-1
- Update to Asciidoctor 0.1.3

* Fri Mar 01 2013 Dan Allen <dan.j.allen@gmail.com> - 0.1.1-1
- Initial package
