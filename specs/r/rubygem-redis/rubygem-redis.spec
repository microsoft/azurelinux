# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name redis

Name: rubygem-%{gem_name}
Version: 5.2.0
Release: 4%{?dist}
Summary: A Ruby client library for Redis
License: MIT
URL: https://github.com/redis/redis-rb
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/redis/redis-rb.git && cd redis-rb
# git archive -v -o redis-rb-5.2.0-tests.txz v5.2.0 makefile test/
Source1: %{gem_name}-rb-%{version}-tests.txz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(redis-client)
BuildRequires: %{_bindir}/make
BuildRequires: %{_bindir}/redis-server
BuildArch: noarch

%description
A Ruby client that tries to match Redis' API one-to-one, while still
providing an idiomatic interface.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b 1

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
pushd .%{gem_instdir}

cp -a %{_builddir}/{makefile,test} .

# We are using packaged Redis, so provide just dummy Redis build script.
mkdir bin
echo '#!/usr/bin/sh' > bin/build
chmod a+x bin/build

# The following steps correspond to GH workflow:
# https://github.com/redis/redis-rb/blob/ce2c258297efc2991e509d57e593e76285d58b0b/.github/workflows/test.yaml#L60-L65
# https://github.com/redis/redis-rb/blob/ce2c258297efc2991e509d57e593e76285d58b0b/.github/workflows/test.yaml#L136-L141
# TODO: There is no hiredis-client in Fedora yet, skipt the `hiredis` for now.
# for driver in ruby hiredis ; do
for driver in ruby ; do
  (
    export DRIVER=${driver}
    make BINARY=$(which redis-server) start
    ruby -Itest -e 'Dir.glob "./test/redis/**/*_test.rb", &method(:require)'
    ruby -Itest -e 'Dir.glob "./test/distributed/**/*_test.rb", &method(:require)'
    make stop
    # Give some time for Redis shutdown.
    sleep 1
  )
done

make BINARY=$(which redis-server) REDIS_CLIENT=$(which redis-cli) BUILD_DIR='${TMP}' start_sentinel wait_for_sentinel
ruby -Itest -e 'Dir.glob "./test/sentinel/**/*_test.rb", &method(:require)'
make stop_all
# Give some time for Redis shutdown.
sleep 1
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Aug 08 2024 Vít Ondruch <vondruch@redhat.com> - 5.2.0-1
- Update to redis 5.2.0.
  Resolves: rhbz#2230434

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Aug 04 2023 Vít Ondruch <vondruch@redhat.com> - 5.0.6-3
- Disable tests failing with Redis 7.2 and redis-client 0.15.0.
  Resolves: rhbz#2226404

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Feb 02 2023 Vít Ondruch <vondruch@redhat.com> - 5.0.6-1
- Update to redis 5.0.6.
  Resolves: rhbz#2120331

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Aug 10 2022 Vít Ondruch <vondruch@redhat.com> - 4.7.1-1
- Update to redis 4.7.1.
  Resolves: rhbz#2100842

* Wed Aug 10 2022 Vít Ondruch <vondruch@redhat.com> - 4.6.0-2
- Fix Redis 7+ compatibility.
  Resolves: rhbz#2114561

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Feb 21 2022 Pavel Valena <pvalena@redhat.com> - 4.6.0-1
- Update to redis 4.6.0.
  Resolves: rhbz#1986825

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 11 2021 Vít Ondruch <vondruch@redhat.com> - 4.3.1-1
- Update to redis 4.3.1.
  Resolves: rhbz#1970782

* Thu Apr 08 2021 Vít Ondruch <vondruch@redhat.com> - 4.2.5-3
- Fix Redis 6.2+ test failures.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Nov 27 2020 Vít Ondruch <vondruch@redhat.com> - 4.2.5-1
- Update to redis 4.2.5.
  Resolves: rhbz#1898465

* Thu Sep 10 2020 Vít Ondruch <vondruch@redhat.com> - 4.2.2-1
- Update to redis 4.2.2.
  Resolves: rhbz#1846288
  Resolves: rhbz#1863730

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.3-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Pavel Valena <pvalena@redhat.com> - 4.1.3-1
- Update to redis-rb 4.1.3.

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 09 2019 Vít Ondruch <vondruch@redhat.com> - 4.1.1-1
- Update to redis 4.1.1.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.0.1-3
- Use C.UTF-8 locale
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 23 2018 Pavel Valena <pvalena@redhat.com> - 4.0.1-1
- Update to redis 4.0.1.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Feb 08 2016 Greg Hellings <greg.hellings@gmail.com> - 3.2.2-2
- Update for rpmlint check
- Remove tests

* Mon Feb 08 2016 Greg Hellings <greg.hellings@gmail.com> - 3.2.2-1
- New upstream

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Feb 15 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.2.1-1
- Update to 3.2.1 (RHBZ #1192389)
- Remove Fedora 19 compatibility macros
- Use static test.conf, since upstream uses a dynamic ERB template now
- Correct comment about IPv6 support

* Mon Dec 15 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.2.0-1
- Update to 3.2.0 (RHBZ #1173070)
- Drop unneeded BRs
- Use %%license macro
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Unconditionally pass tests for now (RHBZ #1173070)

* Mon Jun 09 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.1.0-1
- Update to 3.1.0
- Remove gem2rpm comment
- Patch for Minitest 5

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 24 2014 Achilleas Pipinellis <axilleas@fedoraproject.org> - 3.0.7-1
- Update to 3.0.7

* Tue Sep 03 2013 Axilleas Pipinellis <axilleaspi@ymail.com> - 3.0.4-3
- Move %%exclude .gitignore to -doc
- Reference to redis related bug

* Thu Jun 27 2013 Axilleas Pipinellis <axilleaspi@ymail.com> - 3.0.4-2
- Fix failing test
- Remove redis from Requires
- Exclude dot file

* Sun Jun 23 2013 Axilleas Pipinellis <axilleaspi@ymail.com> - 3.0.4-1
- Initial package
