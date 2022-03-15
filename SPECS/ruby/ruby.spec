# The RubyGems library has to stay out of Ruby directory tree, since the
# RubyGems should be share by all Ruby implementations.
%global rubygems_dir %{_datadir}/rubygems
%global ruby_libdir %{_datadir}/%{name}
%global bigdecimal_version 3.1.1
%global io_console_version 0.5.6
%global psych_version      3.1.0
%global irb_version        1.2.6
%global json_version       2.3.0
%global minitest_version   5.13.0
%global power_assert_version  1.1.7
%global rdoc_version       6.2.1.1
%global test_unit_version  3.3.4
%global gem_dir %{_libdir}/ruby/gems
Summary:        Ruby
Name:           ruby
Version:        2.7.4
Release:        2%{?dist}
License:        (Ruby OR BSD) AND Public Domain AND MIT AND CC0 AND zlib AND UCD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://www.ruby-lang.org/en/
Source0:        https://cache.ruby-lang.org/pub/ruby/2.7/%{name}-%{version}.tar.xz
Source1:        macros.ruby
Source2:        operating_system.rb
Source3:        rubygems.attr
Source4:        rubygems.con
Source5:        rubygems.prov
Source6:        rubygems.req
Source7:        macros.rubygems
# Fix ruby_version abuse.
# https://bugs.ruby-lang.org/issues/11002
Patch0:         ruby-2.3.0-ruby_version.patch
# http://bugs.ruby-lang.org/issues/7807
Patch1:         ruby-2.1.0-Prevent-duplicated-paths-when-empty-version-string-i.patch
BuildRequires:  openssl-devel
BuildRequires:  readline
BuildRequires:  readline-devel
BuildRequires:  tzdata
Requires:       gmp
Requires:       openssl
%if %{with_check}
BuildRequires:  shadow-utils
BuildRequires:  sudo
%endif
Provides:       %{_prefix}/local/bin/ruby
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}(release) = %{version}-%{release}
Provides:       %{name}-libs = %{version}-%{release}
Provides:       rubygems = %{version}-%{release}
Provides:       rubygems-devel = %{version}-%{release}
Provides:       ruby(rubygems) = %{version}-%{release}
# TODO: When moving to Ruby 3.X for Mariner 2.0 release, these gemified stdlib
# provides should be versioned according to the gem version.
# More info: https://stdgems.org/
Provides:       rubygem(bigdecimal) = %{version}-%{release}
Provides:       rubygem(io-console) = %{version}-%{release}
Provides:       rubygem(psych) = %{version}-%{release}
Provides:       rubygem(did_you_mean) = %{version}-%{release}
Provides:       rubygem(irb) = %{version}-%{release}
Provides:       rubygem(json) = %{version}-%{release}
Provides:       rubygem-bigdecimal = %{version}-%{release}
Provides:       rubygem-io-console = %{version}-%{release}
Provides:       rubygem-psych = %{version}-%{release}
Provides:       rubygem-irb = %{version}-%{release}
Provides:       rubygem-did_you_mean = %{version}-%{release}
Provides:       rubygem-json = %{version}-%{release}

%description
The Ruby package contains the Ruby development environment.
This is useful for object-oriented scripting.

%package -n rubygem-bigdecimal
Summary:        BigDecimal provides arbitrary-precision floating point decimal arithmetic
Version:        %{bigdecimal_version}
License:        Ruby OR BSD
Requires:       ruby(release)
Requires:       ruby(rubygems) >= %{rubygems_version}
Provides:       rubygem(bigdecimal) = %{version}-%{release}

%description -n rubygem-bigdecimal
Ruby provides built-in support for arbitrary precision integer arithmetic.
For example:

42**13 -> 1265437718438866624512

BigDecimal provides similar support for very large or very accurate floating
point numbers. Decimal arithmetic is also useful for general calculation,
because it provides the correct answers people expect–whereas normal binary
floating point arithmetic often introduces subtle errors because of the
conversion between base 10 and base 2.

%package -n rubygem-minitest
Summary:        Minitest provides a complete suite of testing facilities
Version:        %{minitest_version}
License:        MIT
Requires:       ruby(release)
Requires:       ruby(rubygems) >= %{rubygems_version}
Provides:       rubygem(minitest) = %{version}-%{release}
BuildArch:      noarch

%description -n rubygem-minitest
minitest/unit is a small and incredibly fast unit testing framework.
minitest/spec is a functionally complete spec engine.
minitest/benchmark is an awesome way to assert the performance of your
algorithms in a repeatable manner.
minitest/mock by Steven Baker, is a beautifully tiny mock object
framework.
minitest/pride shows pride in testing and adds coloring to your test
output.

%package -n rubygem-power_assert
Summary:        Power Assert for Ruby
Version:        %{power_assert_version}
License:        Ruby OR BSD
Requires:       ruby(release)
Requires:       ruby(rubygems) >= %{rubygems_version}
Provides:       rubygem(power_assert) = %{version}-%{release}
BuildArch:      noarch

%description -n rubygem-power_assert
Power Assert shows each value of variables and method calls in the expression.
It is useful for testing, providing which value wasn't correct when the
condition is not satisfied.

%package -n rubygem-rdoc
Summary:        A tool to generate HTML and command-line documentation for Ruby projects
Version:        %{rdoc_version}
# SIL: lib/rdoc/generator/template/darkfish/css/fonts.css
License:        GPLv2 AND Ruby AND MIT AND OFL
Requires:       ruby(release)
Requires:       ruby(rubygems) >= %{rubygems_version}
Requires:       rubygem(io-console) >= %{io_console_version}
Requires:       rubygem(json) >= %{json_version}
Requires:       rubygem(psych) >= %{psych_version}
Provides:       rdoc = %{version}-%{release}
Provides:       ri = %{version}-%{release}
Provides:       rubygem(rdoc) = %{version}-%{release}
BuildArch:      noarch

%description -n rubygem-rdoc
RDoc produces HTML and command-line documentation for Ruby projects.  RDoc
includes the 'rdoc' and 'ri' tools for generating and displaying online
documentation.

%package -n rubygem-test-unit
Summary:        An xUnit family unit testing framework for Ruby
Version:        %{test_unit_version}
# lib/test/unit/diff.rb is a double license of the Ruby license and PSF license.
# lib/test-unit.rb is a dual license of the Ruby license and LGPLv2.1 or later.
License:        (Ruby OR BSD) AND (Ruby OR BSD OR Python) AND (Ruby OR BSD OR LGPLv2+)
Requires:       ruby(release)
Requires:       ruby(rubygems) >= %{rubygems_version}
Requires:       rubygem(power_assert)
Provides:       rubygem(test-unit) = %{version}-%{release}
BuildArch:      noarch

%description -n rubygem-test-unit
Test::Unit (test-unit) is unit testing framework for Ruby, based on xUnit
principles. These were originally designed by Kent Beck, creator of extreme
programming software development methodology, for Smalltalk's SUnit. It allows
writing tests, checking results and automated testing in Ruby.

%prep
%autosetup -p1

%build
autoconf

%configure \
        --with-rubylibprefix=%{_libdir}/ruby \
        --with-archlibdir=%{_libdir} \
        --with-rubyarchprefix=%{_libdir}/ruby \
        --with-sitedir=%{_prefix}/local/share/ruby/site_ruby \
        --with-sitearchdir=%{_prefix}/local/%{_lib}/ruby/site_ruby \
        --with-vendordir=%{_libdir}/ruby/vendor_ruby \
        --with-vendorarchdir=%{_libdir}/ruby/vendor_ruby \
        --with-rubyhdrdir=%{_includedir} \
        --with-rubyarchhdrdir=%{_includedir} \
        --with-sitearchhdrdir=%{_prefix}/local/%{_lib}/ruby/site_ruby/$(uname -m) \
        --with-vendorarchhdrdir=%{_libdir}/ruby/vendor_ruby/$(uname -m) \
        --with-rubygemsdir=%{rubygems_dir} \
        --enable-shared \
        --with-compress-debug-sections=no \
        --with-ruby-version='' \
        --docdir=%{_docdir}/%{name}-%{version}
%make_build COPY="cp -p"

%install
%make_install

# The following install steps are taken from the Fedora 34 spec (license: MIT) and modified for Mariner
# https://src.fedoraproject.org/rpms/ruby/tree/f34

# Move macros file into proper place and replace the %%{name} macro, since it
# would be wrongly evaluated during build of other packages.
mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -m 644 %{SOURCE1} %{buildroot}%{_rpmconfigdir}/macros.d/macros.ruby
sed -i "s/%%{name}/%{name}/" %{buildroot}%{_rpmconfigdir}/macros.d/macros.ruby

# Install custom operating_system.rb.
mkdir -p %{buildroot}%{rubygems_dir}/rubygems/defaults
cp %{SOURCE2} %{buildroot}%{rubygems_dir}/rubygems/defaults

# Install rubygems files
install -m 644 %{SOURCE7} %{buildroot}%{_rpmconfigdir}/macros.d/macros.rubygems
sed -i "s/%%{name}/%{name}/" %{buildroot}%{_rpmconfigdir}/macros.d/macros.rubygems

mkdir -p %{buildroot}%{_rpmconfigdir}/fileattrs
install -m 644 %{SOURCE3} %{buildroot}%{_rpmconfigdir}/fileattrs
install -m 755 %{SOURCE4} %{buildroot}%{_rpmconfigdir}
install -m 755 %{SOURCE5} %{buildroot}%{_rpmconfigdir}
install -m 755 %{SOURCE6} %{buildroot}%{_rpmconfigdir}

# Install bigdecimal
mkdir -p %{buildroot}%{gem_dir}/gems/bigdecimal-%{bigdecimal_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{name}/bigdecimal-%{bigdecimal_version}/bigdecimal
mv %{buildroot}%{_libdir}/ruby/bigdecimal %{buildroot}%{gem_dir}/gems/bigdecimal-%{bigdecimal_version}/lib
touch %{buildroot}%{_libdir}/gems/%{name}/bigdecimal-%{bigdecimal_version}/gem.build_complete
ln -s %{gem_dir}/gems/bigdecimal-%{bigdecimal_version}/lib/bigdecimal %{buildroot}%{_libdir}/ruby/bigdecimal

# Install io-console
mkdir -p %{buildroot}%{gem_dir}/io-console-%{io_console_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{name}/io-console-%{io_console_version}/io
mv %{buildroot}%{_libdir}/ruby/io %{buildroot}%{gem_dir}/io-console-%{io_console_version}/lib
mv %{buildroot}%{gem_dir}/specifications/default/io-console-%{io_console_version}.gemspec %{buildroot}%{gem_dir}/specifications
ln -s %{gem_dir}/io-console-%{io_console_version}/lib/io %{buildroot}%{_libdir}/ruby/io

# install psych
mkdir -p %{buildroot}%{gem_dir}/psych-%{psych_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{name}/psych-%{psych_version}
mv %{buildroot}%{_libdir}/ruby/psych* %{buildroot}%{gem_dir}/psych-%{psych_version}/lib
mv %{buildroot}%{gem_dir}/specifications/default/psych-%{psych_version}.gemspec %{buildroot}%{gem_dir}/specifications
ln -s %{gem_dir}/psych-%{psych_version}/lib/psych %{buildroot}%{_libdir}/ruby/psych
ln -s %{gem_dir}/psych-%{psych_version}/lib/psych.rb %{buildroot}%{_libdir}/ruby/psych.rb

# Install irb
mkdir -p %{buildroot}%{gem_dir}/irb-%{irb_version}/lib
mv %{buildroot}%{_libdir}/ruby/irb* %{buildroot}%{gem_dir}/irb-%{irb_version}/lib
mv %{buildroot}%{gem_dir}/specifications/default/irb-%{irb_version}.gemspec %{buildroot}%{gem_dir}/specifications
ln -s %{gem_dir}/gems/irb-%{irb_version}/lib/irb.rb %{buildroot}%{_libdir}/ruby/irb.rb
# TODO: This should be possible to replaced by simple directory symlink
# after ~ F31 EOL (rhbz#1691039).
mkdir -p %{buildroot}%{_libdir}/ruby/irb
pushd %{buildroot}%{gem_dir}/irb-%{irb_version}/lib
find irb -type d -mindepth 1 -exec mkdir %{buildroot}%{_libdir}/ruby/'{}' \;
find irb -type f -exec ln -s %{gem_dir}/irb-%{irb_version}/lib/'{}' %{buildroot}%{_libdir}/ruby/'{}' \;
popd

# Install json
mkdir -p %{buildroot}%{gem_dir}/json-%{json_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{name}/json-%{json_version}
mv %{buildroot}%{_libdir}/ruby/json* %{buildroot}%{gem_dir}/json-%{json_version}/lib
mv %{buildroot}%{gem_dir}/specifications/default/json-%{json_version}.gemspec %{buildroot}%{gem_dir}/specifications
ln -s %{gem_dir}/json-%{json_version}/lib/json.rb %{buildroot}%{_libdir}/ruby/json.rb
ln -s %{gem_dir}/json-%{json_version}/lib/json %{buildroot}%{_libdir}/ruby/json

%check
chmod g+w . -R
useradd test -G root -m
# Only run stable tests
sudo -u test make test TESTS="-v"

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.so.2.7*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/ruby/*
%{_datadir}/ri/*
%{_docdir}/%{name}-%{version}
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_rpmconfigdir}/macros.d/macros.ruby
%{_rpmconfigdir}/macros.d/macros.rubygems
%{_rpmconfigdir}/fileattrs/rubygems.attr
%{_rpmconfigdir}/rubygems.req
%{_rpmconfigdir}/rubygems.prov
%{_rpmconfigdir}/rubygems.con
%dir %{rubygems_dir}
%{rubygems_dir}/rubygems

%files -n rubygem-bigdecimal
%{_libdir}/gems/%{name}/bigdecimal-%{bigdecimal_version}
%{gem_dir}/gems/bigdecimal-%{bigdecimal_version}

%files -n rubygem-minitest
%dir %{gem_dir}/gems/minitest-%{minitest_version}
%exclude %{gem_dir}/gems/minitest-%{minitest_version}/.*
%{gem_dir}/gems/minitest-%{minitest_version}/Manifest.txt
%{gem_dir}/gems/minitest-%{minitest_version}/design_rationale.rb
%{gem_dir}/gems/minitest-%{minitest_version}/lib
%{gem_dir}/specifications/minitest-%{minitest_version}.gemspec
%doc %{gem_dir}/gems/minitest-%{minitest_version}/History.rdoc
%doc %{gem_dir}/gems/minitest-%{minitest_version}/README.rdoc
%{gem_dir}/gems/minitest-%{minitest_version}/Rakefile
%{gem_dir}/gems/minitest-%{minitest_version}/test

%files -n rubygem-power_assert
%dir %{gem_dir}/gems/power_assert-%{power_assert_version}
%exclude %{gem_dir}/gems/power_assert-%{power_assert_version}/.*
%license %{gem_dir}/gems/power_assert-%{power_assert_version}/BSDL
%license %{gem_dir}/gems/power_assert-%{power_assert_version}/COPYING
%license %{gem_dir}/gems/power_assert-%{power_assert_version}/LEGAL
%{gem_dir}/gems/power_assert-%{power_assert_version}/lib
%{gem_dir}/specifications/power_assert-%{power_assert_version}.gemspec
%{gem_dir}/gems/power_assert-%{power_assert_version}/Gemfile
%{gem_dir}/gems/power_assert-%{power_assert_version}/Rakefile

%files -n rubygem-rdoc
%{_bindir}/rdoc
%{_bindir}/ri
%{gem_dir}/gems/rdoc-%{rdoc_version}
%{_mandir}/man1/ri*

%files -n rubygem-test-unit
%dir %{gem_dir}/gems/test-unit-%{test_unit_version}
%license %{gem_dir}/gems/test-unit-%{test_unit_version}/GPL
%license %{gem_dir}/gems/test-unit-%{test_unit_version}/LGPL
%license %{gem_dir}/gems/test-unit-%{test_unit_version}/COPYING
%license %{gem_dir}/gems/test-unit-%{test_unit_version}/PSFL
%{gem_dir}/gems/test-unit-%{test_unit_version}/lib
%{gem_dir}/gems/test-unit-%{test_unit_version}/sample
%{gem_dir}/gems/test-unit-%{test_unit_version}/test
%{gem_dir}/specifications/test-unit-%{test_unit_version}.gemspec
%doc %{gem_dir}/gems/test-unit-%{test_unit_version}/README.md
%{gem_dir}/gems/test-unit-%{test_unit_version}/Rakefile
%doc %{gem_dir}/gems/test-unit-%{test_unit_version}/doc

%changelog
* Tue Mar 15 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.7.4-2
- Build bigdecimal, minitest, test-unit, rdoc and power_assert rubygems

* Wed Mar 09 2022 Andrew Phelps <anphel@microsoft.com> - 2.7.4-1
- Update to version 2.7.4 to build with new autoconf

* Mon Jul 12 2021 Thomas Crain <thcrain@microsoft.com> - 2.7.2-4
- Add attribution for parts of the install script taken from Fedora 34 (license: MIT)
- Add provides for rubygem(json), and install json gem into the gemdir
- Modernize spec with macros

* Fri Apr 02 2021 Thomas Crain <thcrain@microsoft.com> - 2.7.2-3
- Merge the following releases from 1.0 to dev branch
- pawelwi@microsoft.com, 2.6.6-3: Adding 'BuildRequires' on 'shadow-utils' and 'sudo' to run the package tests.
- anphel@microsoft.com, 2.6.6-4: Run "make test" instead of "make check" to avoid unstable tests.

* Fri Mar 19 2021 Henry Li <lihl@microsoft.com> - 2.7.2-2
- Add bindir path to gem installation to install executable at
  system bin directory instead of bin directory under gem home directory
- Add Provides for rubygem-bigdecimal, rubygem-irb, rubygem-io-console, rubygem-did_you_mean
  and rubygem-psych

* Thu Mar 11 2021 Henry Li <lihl@microsoft.com> - 2.7.2-1
- Upgrade to version 2.7.2
- Add files like macros.rubygems, imported from Fedora 32 (license: MIT)
- Add patches to prevent ruby vesion abuse
- Modify ruby configuration
- Install necessary binaries for bigdecimal, irb, io-console and psych
- Add provides for /usr/local/bin/ruby, ruby(release), rubygems, rubygems-devel, ruby-libs,
  ruby(rubygems), rubygem(irb), rubygem(bigdecimal), rubygem(io-console), rubygem(psych),
  rubygem(did_you_mean)

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 2.6.6-3
- Add macros file, imported from Fedora 32 (license: MIT)

* Tue Jan 05 2021 Joe Schmitt <joschmit@microsoft.com> - 2.6.6-2
- Provide ruby-devel.

* Thu Oct 15 2020 Emre Girgin <mrgirgin@microsoft.com> - 2.6.6-1
- Upgrade to 2.6.6 to resolve CVEs.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.6.3-3
- Added %%license line automatically

* Wed May 06 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.6.3-2
- Removing *Requires for "ca-certificates".

* Fri Mar 13 2020 Paul Monson <paulmon@microsoft.com> - 2.6.3-1
- Update to version 2.6.3. License verified.

* Mon Feb 3 2020 Andrew Phelps <anphel@microsoft.com> - 2.5.3-3
- Disable compressing debug sections

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.5.3-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Jan 01 2019 Sujay G <gsujay@vmware.com> - 2.5.3-1
- Update to version 2.5.3, to fix CVE-2018-16395 & CVE-2018-16396

* Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> - 2.5.1-1
- Update to version 2.5.1

* Fri Jan 12 2018 Xiaolin Li <xiaolinl@vmware.com> - 2.4.3-2
- Fix CVE-2017-17790

* Wed Jan 03 2018 Xiaolin Li <xiaolinl@vmware.com> - 2.4.3-1
- Update to version 2.4.3, fix CVE-2017-17405

* Fri Sep 29 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.4.2-1
- Update to version 2.4.2

* Fri Sep 15 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.4.1-5
- [security] CVE-2017-14064

* Tue Sep 05 2017 Chang Lee <changlee@vmware.com> - 2.4.1-4
- Built with copy preserve mode and fixed %check

* Mon Jul 24 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.4.1-3
- [security] CVE-2017-9228

* Tue Jun 13 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.4.1-2
- [security] CVE-2017-9224,CVE-2017-9225
- [security] CVE-2017-9227,CVE-2017-9229

* Thu Apr 13 2017 Siju Maliakkal <smaliakkal@vmware.com> - 2.4.1-1
- Update to latest 2.4.1

* Wed Jan 18 2017 Anish Swaminathan <anishs@vmware.com> - 2.4.0-1
- Update to 2.4.0 - Fixes CVE-2016-2339

* Mon Oct 10 2016 ChangLee <changlee@vmware.com> - 2.3.0-4
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.3.0-3
- GA - Bump release of all rpms

* Wed Mar 09 2016 Divya Thaluru <dthaluru@vmware.com> - 2.3.0-2
- Adding readline support

* Wed Jan 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.3.0-1
- Updated to 2.3.0-1

* Tue Apr 28 2015 Fabio Rapposelli <fabio@vmware.com> - 2.2.1-2
- Added SSL support

* Mon Apr 6 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> - 2.2.1-1
- Version upgrade to 2.2.1

* Fri Oct 10 2014 Divya Thaluru <dthaluru@vmware.com> - 2.1.3-1
- Initial build.  First version
