# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from actioncable-5.0.0.rc2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name actioncable

# TODO: Re-enable recompilation if possible. Currently, we don't have rollup.js
# in Fedora and therefore it requires network access. Still good for checking
# the results
%bcond_with js_recompilation

Name: rubygem-%{gem_name}
Version: 8.0.2
Release: 2%{?dist}
Summary: WebSocket framework for Rails
License: MIT
URL: https://rubyonrails.org
Source0: https://rubygems.org/gems/%{gem_name}-%{version}%{?prerelease}.gem
# git clone https://github.com/rails/rails.git && cd rails/actioncable
# git archive -v -o actioncable-8.0.2-tests.tar.gz v8.0.2 test/
Source1: %{gem_name}-%{version}%{?prerelease}-tests.tar.gz
# Source code of pregenerated JS files.
# git clone https://github.com/rails/rails.git && cd rails/actioncable
# git archive -v -o actioncable-8.0.2-js.tar.gz v8.0.2 app/javascript package.json rollup.config.js
Source2: %{gem_name}-%{version}%{?prerelease}-js.tar.gz

BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 3.2.0
BuildRequires: rubygem(actionpack) = %{version}
BuildRequires: rubygem(activesupport) = %{version}
BuildRequires: rubygem(puma)
BuildRequires: rubygem(websocket-driver)
BuildRequires: rubygem(zeitwerk)
BuildRequires: %{_bindir}/redis-server
BuildRequires: rubygem(redis)
%{?with_js_recompilation:BuildRequires: %{_bindir}/npm}
BuildArch: noarch

%description
Structure many real-time application concerns into channels over a single
WebSocket connection.


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

rm -rf app/assets

ln -s %{builddir}/app/javascript ./app/javascript
ln -s %{builddir}/package.json .
cp -a %{builddir}/rollup.config.js .

# TODO: This requires network access. Use Fedora rollup.js if it becomes
# available eventually
npm install
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

# We don't have websocket-client-simple in Fedora yet.
mv test/client_test.rb{,.disable}

# TODO: Needs AR together with PostgreSQL.
mv test/subscription_adapter/postgresql_test.rb{,.disable}

# test/javascript_package_test.rb requires rollup.js, which we don't have.
# OTOH, if we had it, we would recomplie the sources and the test would have
# less value.
mv test/javascript_package_test.rb{,.disable}

# Start a testing Redis server instance
REDIS_DIR=$(mktemp -d)
redis-server --dir $REDIS_DIR --pidfile $REDIS_DIR/redis.pid --daemonize yes

ruby -Ilib:test -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'

# Shutdown Redis.
kill -INT $(cat $REDIS_DIR/redis.pid)

)

%files
%dir %{gem_instdir}
%license %{gem_instdir}/MIT-LICENSE
%{gem_instdir}/app
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 04 2025 Vít Ondruch <vondruch@redhat.com> - 8.0.2-1
- Update to Action Cable 8.0.2.
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
- Update to actioncable 7.0.8.

* Mon Aug 28 2023 Pavel Valena <pvalena@redhat.com> - 7.0.7.2-1
- Update to actioncable 7.0.7.2.

* Thu Aug 10 2023 Pavel Valena <pvalena@redhat.com> - 7.0.7-1
- Update to actioncable 7.0.7.

* Sun Jul 23 2023 Pavel Valena <pvalena@redhat.com> - 7.0.6-1
- Update to actioncable 7.0.6.

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 30 2023 Pavel Valena <pvalena@redhat.com> - 7.0.5-1
- Update to actioncable 7.0.5.

* Tue Mar 14 2023 Pavel Valena <pvalena@redhat.com> - 7.0.4.3-1
- Update to actioncable 7.0.4.3.

* Fri Feb 17 2023 Vít Ondruch <vondruch@redhat.com> - 7.0.4.2-2
- Disable JS recompilation, because it does not do anything useful ATM apart
  from unnecessarily pulling in CoffeeScript.

* Wed Jan 25 2023 Pavel Valena <pvalena@redhat.com> - 7.0.4.2-1
- Update to actioncable 7.0.4.2.

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Sep 15 2022 Pavel Valena <pvalena@redhat.com> - 7.0.4-1
- Update to actioncable 7.0.4.

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Mar 14 2022 Pavel Valena <pvalena@redhat.com> - 7.0.2.3-1
- Update to actioncable 7.0.2.3.

* Fri Feb 11 2022 Pavel Valena <pvalena@redhat.com> - 7.0.2-2
- Update to actioncable 7.0.2.

* Thu Feb 03 2022 Pavel Valena <pvalena@redhat.com> - 7.0.1-1
- Update to actioncable 7.0.1.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Sep 17 2021 Pavel Valena <pvalena@redhat.com> - 6.1.4.1-1
- Update to actioncable 6.1.4.1.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 30 2021 Pavel Valena <pvalena@redhat.com> - 6.1.4-1
- Update to actioncable 6.1.4.

* Tue May 18 2021 Pavel Valena <pvalena@redhat.com> - 6.1.3.2-1
- Update to actioncable 6.1.3.2.

* Fri Apr 09 2021 Pavel Valena <pvalena@redhat.com> - 6.1.3.1-1
- Update to actioncable 6.1.3.1.

* Thu Feb 18 2021 Pavel Valena <pvalena@redhat.com> - 6.1.3-1
- Update to actioncable 6.1.3.

* Mon Feb 15 2021 Pavel Valena <pvalena@redhat.com> - 6.1.2.1-1
- Update to actioncable 6.1.2.1.
  Resolves: rhbz#1906179

* Wed Jan 27 2021 Pavel Valena <pvalena@redhat.com> - 6.1.1-1
- Update to actioncable 6.1.1.
  Resolves: rhbz#1906179

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct  8 12:08:41 CEST 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.4-1
- Update to actioncable 6.0.3.4.
  Resolves: rhbz#1877503

* Tue Sep 22 01:22:47 CEST 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.3-1
- Update to actioncable 6.0.3.3.
  Resolves: rhbz#1877503

* Mon Aug 17 05:22:37 GMT 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.2-1
- Update to actioncable 6.0.3.2.
  Resolves: rhbz#1742788

* Mon Aug 03 07:01:37 GMT 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.1-1
- Update to ActionCable 6.0.3.1.
  Resolves: rhbz#1742788

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 28 2019 Pavel Valena <pvalena@redhat.com> - 5.2.3-1
- Update to Action Cable 5.2.3.

* Thu Mar 14 2019 Pavel Valena <pvalena@redhat.com> - 5.2.2.1-1
- Update to Action Cable 5.2.2.1.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 05 2018 Pavel Valena <pvalena@redhat.com> - 5.2.2-1
- Update to Action Cable 5.2.2.

* Wed Aug 08 2018 Pavel Valena <pvalena@redhat.com> - 5.2.1-1
- Update to Action Cable 5.2.1.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May 01 2018 Pavel Valena <pvalena@redhat.com> - 5.2.0-1
- Update to Action Cable 5.2.0.

* Fri Feb 16 2018 Pavel Valena <pvalena@redhat.com> - 5.1.5-1
- Update to Action Cable 5.1.5.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 11 2017 Pavel Valena <pvalena@redhat.com> - 5.1.4-1
- Update to Action Cable 5.1.4.

* Tue Aug 08 2017 Pavel Valena <pvalena@redhat.com> - 5.1.3-1
- Update to Action Cable 5.1.3.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Pavel Valena <pvalena@redhat.com> - 5.1.2-1
- Update to Action Cable 5.1.2.

* Mon May 22 2017 Pavel Valena <pvalena@redhat.com> - 5.1.1-1
- Update to Action Cable 5.1.1.

* Thu Mar 02 2017 Pavel Valena <pvalena@redhat.com> - 5.0.2-1
- Update to Action Cable 5.0.2.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 03 2017 Pavel Valena <pvalena@redhat.com> - 5.0.1-2
- Enable JS recompilation.
- Use recompile script from previous Action Cable version

* Mon Jan 02 2017 Pavel Valena <pvalena@redhat.com> - 5.0.1-1
- Update to Action Cable 5.0.1.
- Disable JS recompilation.

* Tue Aug 16 2016 Pavel Valena <pvalena@redhat.com> - 5.0.0.1-1
- Update to Actioncable 5.0.0.1

* Thu Jun 30 2016 Vít Ondruch <vondruch@redhat.com> - 5.0.0-1
- Initial package
