Vendor:         Microsoft Corporation
Distribution:   Mariner

# Generated from mysql2-0.3.11.gem by gem2rpm -*- rpm-spec -*-
%global gem_name mysql2

Name: rubygem-%{gem_name}
Version: 0.5.3
Release: 7%{?dist}
Summary: A simple, fast Mysql library for Ruby, binding to libmysql
License: MIT
URL: https://github.com/brianmario/mysql2
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone --no-checkout https://github.com/brianmario/mysql2.git
# cd mysql2 && git archive -v -o mysql2-0.5.3-tests.txz 0.5.3 spec/
Source1: %{gem_name}-%{version}-tests.txz

# Required in lib/mysql2.rb
Requires: rubygem(bigdecimal)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby-devel
BuildRequires: gcc
BuildRequires: mariadb-connector-c-devel
%if %{with_check}
BuildRequires: mariadb-server
BuildRequires: rubygem(rspec)
# Used in mysql_install_db
BuildRequires: /bin/hostname
BuildRequires: rubygem(bigdecimal)
# Used in spec/em/em_spec.rb
BuildRequires: rubygem(eventmachine)
%endif

%description
The Mysql2 gem is meant to serve the extremely common use-case of
connecting, querying and iterating on results. Some database libraries
out there serve as direct 1:1 mappings of the already complex C API\'s
available. This one is not.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

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
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Prevent dangling symlink in -debuginfo.
rm -rf %{buildroot}%{gem_instdir}/ext


%check
pushd .%{gem_instdir}
# Move the tests into place
ln -s %{_builddir}/spec spec

TOP_DIR=$(pwd)
# Use testing port because the standard mysqld port 3306 is occupied.
# Assign a random port to consider a case of multi builds in parallel in a host.
# https://src.fedoraproject.org/rpms/rubygem-pg/pull-request/3
MYSQL_TEST_PORT="$((13306 + ${RANDOM} % 1000))"
MYSQL_TEST_USER=$(id -un)
MYSQL_TEST_DATA_DIR="${TOP_DIR}/data"
MYSQL_TEST_SOCKET="${TOP_DIR}/mysql.sock"
MYSQL_TEST_LOG="${TOP_DIR}/mysql.log"
MYSQL_TEST_PID_FILE="${TOP_DIR}/mysql.pid"

mkdir "${MYSQL_TEST_DATA_DIR}"
mysql_install_db \
  --datadir="${MYSQL_TEST_DATA_DIR}" \
  --log-error="${MYSQL_TEST_LOG}"

%{_libexecdir}/mysqld \
  --datadir="${MYSQL_TEST_DATA_DIR}" \
  --log-error="${MYSQL_TEST_LOG}" \
  --socket="${MYSQL_TEST_SOCKET}" \
  --pid-file="${MYSQL_TEST_PID_FILE}" \
  --port="${MYSQL_TEST_PORT}" \
  --ssl &

for i in $(seq 10); do
  sleep 1
  if grep -q 'ready for connections.' "${MYSQL_TEST_LOG}"; then
    break
  fi
  echo "Waiting connections... ${i}"
done

# See https://github.com/brianmario/mysql2/blob/master/.travis_setup.sh
mysql -u $MYSQL_TEST_USER \
  -e 'CREATE DATABASE /*M!50701 IF NOT EXISTS */ test' \
  -S "${MYSQL_TEST_SOCKET}" \
  -P "${MYSQL_TEST_PORT}"

# See https://github.com/brianmario/mysql2/blob/master/tasks/rspec.rake
cat <<EOF > spec/configuration.yml
root:
  host: localhost
  username: ${MYSQL_TEST_USER}
  password:
  database: test
  port: ${MYSQL_TEST_PORT}
  socket: ${MYSQL_TEST_SOCKET}

user:
  host: localhost
  username: ${MYSQL_TEST_USER}
  password:
  database: mysql2_test
  port: ${MYSQL_TEST_PORT}
  socket: ${MYSQL_TEST_SOCKET}
EOF

# This test would require changes in host configuration.
sed -i '/^  it "should be able to connect via SSL options" do$/,/^  end$/ s/^/#/' \
  spec/mysql2/client_spec.rb

# performance_schema.session_account_connect_attrs is unexpectedly empty.
# https://github.com/brianmario/mysql2/issues/965
sed -i '/^  it "should set default program_name in connect_attrs" do$/,/^  end$/ s/^/#/' \
  spec/mysql2/client_spec.rb
sed -i '/^  it "should set custom connect_attrs" do$/,/^  end$/ s/^/#/' \
  spec/mysql2/client_spec.rb

popd

# Clean up
kill "$(cat "${MYSQL_TEST_PID_FILE}")"

%files
%dir %{gem_instdir}
%{gem_dir}/extensions
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%exclude %{gem_instdir}/support
%license %{gem_instdir}/LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/CHANGELOG.md


%changelog
* Mon Nov 28 2022 Muhammad Falak <mwani@microsoft.com> - 0.5.3-7
- License verified

* Wed Nov 17 2021 Muhammad Falak <mwani@microsoft.com> - 0.5.3-6
- Introduce macro '%{mariner_failing_tests}' to gate `--run-check` failures

* Thu Sep 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.5.3-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Updating ruby paths to CBL-Mariner definitions.

* Thu Jul  2 2020 Alex Chernyakhovsky <achernya@mit.edu> - 0.5.3-4
- Update tests to build and run on F32

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Vít Ondruch <vondruch@redhat.com> - 0.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.7

* Mon Dec 02 2019 Jun Aruga <jaruga@redhat.com> - 0.5.3-1
- New upstream release 0.5.3

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.2-2
- F-30: rebuild against ruby26

* Thu Jul 19 2018 Jun Aruga <jaruga@redhat.com> - 0.5.2-1
- New upstream release 0.5.2

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 0.4.10-3
- Rebuilt for switch to libxcrypt

* Thu Jan 04 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.4.10-2
- F-28: rebuild for ruby25

* Thu Nov 23 2017 Jun Aruga <jaruga@redhat.com> - 0.4.10-1
- New upstream release 0.4.10

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Adam Williamson <awilliam@redhat.com> - 0.4.8-1
- New upstream release 0.4.8 (builds against MariaDB 10.2)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 11 2017 Vít Ondruch <vondruch@redhat.com> - 0.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.4

* Thu Jun 09 2016 Miroslav Suchý <msuchy@redhat.com> - 0.4.4-1
- New upstream release 0.4.4

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Vít Ondruch <vondruch@redhat.com> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3

* Tue Sep  8 2015 Miroslav Suchý <msuchy@redhat.com> 0.4.0-1
- rebase to mysql2-0.4.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> - 0.3.16-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Miroslav Suchý <msuchy@redhat.com> 0.3.16-1
- rebase to mysql2-0.3.16

* Tue Apr 15 2014 Vít Ondruch <vondruch@redhat.com> - 0.3.15-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Tue Feb 11 2014 Miroslav Suchý <msuchy@redhat.com> 0.3.15-2
- rebase to mysql2-0.3.15

* Wed Sep 11 2013 Alexander Chernyakhovsky <achernya@mit.edu> - 0.3.13-1
- Initial package
