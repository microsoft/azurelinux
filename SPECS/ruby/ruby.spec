# The RubyGems library has to stay out of Ruby directory tree, since the
# RubyGems should be share by all Ruby implementations.
%global rubygems_dir  %{_datadir}/rubygems
%global gem_dir %{_datadir}/ruby/gems
%global rubygems_version        3.3.26
# Add version for default gems from https://stdgems.org/
# A helpful one-liner script to check the current default versions is available via RUBY_VER=3.1 ./get_gem_versions.sh
%global abbrev_version          0.1.0
%global base64_version          0.1.1
%global benchmark_version       0.2.0
# bigdecimal is available via rubygem-bigdecimal.spec with higher version 3.1.2 (default is 3.1.1)
%global bundler_version         2.3.26
%global cgi_version             0.3.5
%global csv_version             3.2.5
%global date_version            3.2.2
%global delegate_version        0.2.0
%global did_you_mean_version    1.6.1
%global digest_version          3.1.0
%global drb_version             2.1.0
%global english_version         0.7.1
%global erb_version             2.2.3
%global error_highlight_version 0.3.0
%global etc_version             1.3.0
%global fcntl_version           1.0.1
%global fiddle_version          1.1.0
%global fileutils_version       1.6.0
%global find_version            0.1.1
%global forwardable_version     1.3.2
%global getoptlong_version      0.1.1
%global io_console_version      0.5.11
%global io_nonblock_version     0.1.0
%global io_wait_version         0.2.1
%global ipaddr_version          1.2.4
%global irb_version             1.4.1
%global json_version            2.6.1
%global logger_version          1.5.0
%global mutex_m_version         0.1.1
%global net_http_version        0.3.0
%global net_protocol_version    0.1.2
%global nkf_version             0.1.1
%global observer_version        0.1.1
%global open3_version           0.1.1
%global openssl_version         3.0.1
%global open_uri_version        0.2.0
%global optparse_version        0.2.0
%global ostruct_version         0.5.2
%global pathname_version        0.2.0
%global pp_version              0.3.0
%global prettyprint_version     0.1.1
%global pstore_version          0.1.1
%global psych_version           4.0.4
%global racc_version            1.6.0
%global rdoc_version            6.4.0
%global readline_version        0.0.3
%global readline_ext_version    0.1.4
%global reline_version          0.3.1
%global resolv_version          0.2.1
%global resolv_replace_version  0.1.0
%global rinda_version           0.1.1
%global ruby2_keywords_version  0.0.5
%global securerandom_version    0.2.0
%global set_version             1.0.2
%global shellwords_version      0.1.0
%global singleton_version       0.1.1
%global stringio_version        3.0.1
%global strscan_version         3.0.1
%global syslog_version          0.1.0
%global tempfile_version        0.1.2
%global time_version            0.2.2
%global timeout_version         0.2.0
%global tmpdir_version          0.1.2
%global tsort_version           0.1.0
%global un_version              0.2.0
%global uri_version             0.12.2
%global weakref_version         0.1.1
%global win32ole_version        1.8.8
%global yaml_version            0.2.0
%global zlib_version            2.1.1

Summary:        Ruby
Name:           ruby
# TODO: When changing ruby version, these gemified stdlib
# provides should be versioned according to the ruby version.
# More info: https://stdgems.org/
Version:        3.1.4
Release:        3%{?dist}
License:        (Ruby OR BSD) AND Public Domain AND MIT AND CC0 AND zlib AND UCD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://www.ruby-lang.org/en/
Source0:        https://cache.ruby-lang.org/pub/ruby/3.1/%{name}-%{version}.tar.xz
Source1:        macros.ruby
Source2:        operating_system.rb
Source3:        rubygems.attr
Source4:        rubygems.con
Source5:        rubygems.prov
Source6:        rubygems.req
Source7:        macros.rubygems
# Updates default ruby-uri to 0.12.2 and vendored one to 0.10.3. Remove once ruby gets updated to a version that comes with both lib/uri/version.rb and lib/bundler/vendor/uri/lib/uri/version.rb versions >= 0.12.2 or == 0.10.3
Patch0:         CVE-2023-36617.patch
BuildRequires:  openssl-devel
BuildRequires:  readline
BuildRequires:  readline-devel
BuildRequires:  tzdata
%if %{with_check}
BuildRequires:  shadow-utils
BuildRequires:  sudo
%endif

Requires:       gmp
Requires:       openssl
Provides:       %{_prefix}/local/bin/ruby
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}(release) = %{version}-%{release}
Provides:       %{name}-libs = %{version}-%{release}
# TODO: When changing ruby version, these gemified stdlib
# provides should be versioned according to the ruby version.
# More info: https://stdgems.org/
Provides:       rubygem-abbrev = %{abbrev_version}-%{release}
Provides:       rubygem(abbrev) = %{abbrev_version}-%{release}
Provides:       rubygem-base64 = %{base64_version}-%{release}
Provides:       rubygem(base64) = %{base64_version}-%{release}
Provides:       rubygem-benchmark = %{benchmark_version}-%{release}
Provides:       rubygem(benchmark) = %{benchmark_version}-%{release}
Provides:       rubygem-bundler = %{bundler_version}-%{release}
Provides:       rubygem(bundler) = %{bundler_version}-%{release}
# we have transitioned away from a seperate spec/package for bundler, obsolete that package
Obsoletes:      rubygem-bundler < %{bundler_version}-%{release}
Provides:       rubygem-cgi = %{cgi_version}-%{release}
Provides:       rubygem(cgi) = %{cgi_version}-%{release}
Provides:       rubygem-csv = %{csv_version}-%{release}
Provides:       rubygem(csv) = %{csv_version}-%{release}
Provides:       rubygem-date = %{date_version}-%{release}
Provides:       rubygem(date) = %{date_version}-%{release}
Provides:       rubygem(delegate) = %{delegate_version}-%{release}
Provides:       rubygem-delegate = %{delegate_version}-%{release}
Provides:       rubygem(did_you_mean) = %{did_you_mean_version}-%{release}
Provides:       rubygem-did_you_mean = %{did_you_mean_version}-%{release}
Provides:       rubygem(digest) = %{digest_version}-%{release}
Provides:       rubygem-digest = %{digest_version}-%{release}
Provides:       rubygem(drb) = %{drb_version}-%{release}
Provides:       rubygem-drb = %{drb_version}-%{release}
Provides:       rubygem(english) = %{english_version}-%{release}
Provides:       rubygem-english = %{english_version}-%{release}
Provides:       rubygem(erb) = %{erb_version}-%{release}
Provides:       rubygem-erb = %{erb_version}-%{release}
Provides:       rubygem(error) = %{error_highlight_version}-%{release}
Provides:       rubygem-error = %{error_highlight_version}-%{release}
Provides:       rubygem(etc) = %{etc_version}-%{release}
Provides:       rubygem-etc = %{etc_version}-%{release}
Provides:       rubygem(fcntl) = %{fcntl_version}-%{release}
Provides:       rubygem-fcntl = %{fcntl_version}-%{release}
Provides:       rubygem(fiddle) = %{fiddle_version}-%{release}
Provides:       rubygem-fiddle = %{fiddle_version}-%{release}
Provides:       rubygem-fileutils = %{fileutils_version}-%{release}
Provides:       rubygem(fileutils) = %{fileutils_version}-%{release}
Provides:       rubygem-find = %{find_version}-%{release}
Provides:       rubygem(find) = %{find_version}-%{release}
Provides:       rubygem-forwardable = %{forwardable_version}-%{release}
Provides:       rubygem(forwardable) = %{forwardable_version}-%{release}
Provides:       rubygem-getoptlong = %{getoptlong_version}-%{release}
Provides:       rubygem(getoptlong) = %{getoptlong_version}-%{release}
Provides:       rubygem-io-console = %{io_console_version}-%{release}
Provides:       rubygem(io-console) = %{io_console_version}-%{release}
Provides:       rubygem-io-nonblock = %{io_nonblock_version}-%{release}
Provides:       rubygem(io-nonblock) = %{io_nonblock_version}-%{release}
Provides:       rubygem-io-wait = %{io_wait_version}-%{release}
Provides:       rubygem(io-wait) = %{io_wait_version}-%{release}
Provides:       rubygem-ipaddr = %{ipaddr_version}-%{release}
Provides:       rubygem(ipaddr) = %{ipaddr_version}-%{release}
Provides:       rubygem-irb = %{irb_version}-%{release}
Provides:       rubygem(irb) = %{irb_version}-%{release}
Provides:       rubygem-json = %{json_version}-%{release}
Provides:       rubygem(json) = %{json_version}-%{release}
Provides:       rubygem-logger = %{logger_version}-%{release}
Provides:       rubygem(logger) = %{logger_version}-%{release}
Provides:       rubygem-mutex_m = %{mutex_m_version}-%{release}
Provides:       rubygem(mutex_m) = %{mutex_m_version}-%{release}
Provides:       rubygem-net-http = %{net_http_version}-%{release}
Provides:       rubygem(net-http) = %{net_http_version}-%{release}
Provides:       rubygem-net-protocol = %{net_protocol_version}-%{release}
Provides:       rubygem(net-protocol) = %{net_protocol_version}-%{release}
Provides:       rubygem-nkf = %{nkf_version}-%{release}
Provides:       rubygem(nkf) = %{nkf_version}-%{release}
Provides:       rubygem-observer = %{observer_version}-%{release}
Provides:       rubygem(observer) = %{observer_version}-%{release}
Provides:       rubygem-open3 = %{open3_version}-%{release}
Provides:       rubygem(open3) = %{open3_version}-%{release}
Provides:       rubygem-openssl = %{openssl_version}-%{release}
Provides:       rubygem(openssl) = %{openssl_version}-%{release}
Provides:       rubygem-open-uri = %{open_uri_version}-%{release}
Provides:       rubygem(open-uri) = %{open_uri_version}-%{release}
Provides:       rubygem-optparse = %{optparse_version}-%{release}
Provides:       rubygem(optparse) = %{optparse_version}-%{release}
Provides:       rubygem-ostruct = %{ostruct_version}-%{release}
Provides:       rubygem(ostruct) = %{ostruct_version}-%{release}
Provides:       rubygem-pathname = %{pathname_version}-%{release}
Provides:       rubygem(pathname) = %{pathname_version}-%{release}
Provides:       rubygem-pp = %{pp_version}-%{release}
Provides:       rubygem(pp) = %{pp_version}-%{release}
Provides:       rubygem-prettyprint = %{prettyprint_version}-%{release}
Provides:       rubygem(prettyprint) = %{prettyprint_version}-%{release}
Provides:       rubygem-pstore = %{pstore_version}-%{release}
Provides:       rubygem(pstore) = %{pstore_version}-%{release}
Provides:       rubygem-psych = %{psych_version}-%{release}
Provides:       rubygem(psych) = %{psych_version}-%{release}
Provides:       rubygem-racc = %{racc_version}-%{release}
Provides:       rubygem(racc) = %{racc_version}-%{release}
Provides:       rubygem-rdoc = %{rdoc_version}-%{release}
Provides:       rubygem(rdoc) = %{rdoc_version}-%{release}
Provides:       rubygem-readline = %{readline_version}-%{release}
Provides:       rubygem(readline) = %{readline_version}-%{release}
Provides:       rubygem-readline-ext = %{readline_ext_version}-%{release}
Provides:       rubygem(readline-ext) = %{readline_ext_version}-%{release}
Provides:       rubygem-reline = %{reline_version}-%{release}
Provides:       rubygem(reline) = %{reline_version}-%{release}
Provides:       rubygem-resolv = %{resolv_version}-%{release}
Provides:       rubygem(resolv) = %{resolv_version}-%{release}
Provides:       rubygem-resolv-replace = %{resolv_replace_version}-%{release}
Provides:       rubygem(resolv-replace) = %{resolv_replace_version}-%{release}
Provides:       rubygem-rinda = %{rinda_version}-%{release}
Provides:       rubygem(rinda) = %{rinda_version}-%{release}
Provides:       rubygem-ruby2_keywords = %{ruby2_keywords_version}-%{release}
Provides:       rubygem(ruby2_keywords) = %{ruby2_keywords_version}-%{release}
Provides:       rubygem-rubygems = %{rubygems_version}-%{release}
Provides:       rubygem(rubygems) = %{rubygems_version}-%{release}
Provides:       rubygem-securerandom = %{securerandom_version}-%{release}
Provides:       rubygem(securerandom) = %{securerandom_version}-%{release}
Provides:       rubygem-set = %{set_version}-%{release}
Provides:       rubygem(set) = %{set_version}-%{release}
Provides:       rubygem-shellwords = %{shellwords_version}-%{release}
Provides:       rubygem(shellwords) = %{shellwords_version}-%{release}
Provides:       rubygem-singleton = %{singleton_version}-%{release}
Provides:       rubygem(singleton) = %{singleton_version}-%{release}
Provides:       rubygem-stringio = %{stringio_version}-%{release}
Provides:       rubygem(stringio) = %{stringio_version}-%{release}
Provides:       rubygem-strscan = %{strscan_version}-%{release}
Provides:       rubygem(strscan) = %{strscan_version}-%{release}
Provides:       rubygem-syslog = %{syslog_version}-%{release}
Provides:       rubygem(syslog) = %{syslog_version}-%{release}
Provides:       rubygem-tempfile = %{tempfile_version}-%{release}
Provides:       rubygem(tempfile) = %{tempfile_version}-%{release}
Provides:       rubygem-time = %{time_version}-%{release}
Provides:       rubygem(time) = %{time_version}-%{release}
Provides:       rubygem-timeout = %{timeout_version}-%{release}
Provides:       rubygem(timeout) = %{timeout_version}-%{release}
Provides:       rubygem-tmpdir = %{tmpdir_version}-%{release}
Provides:       rubygem(tmpdir) = %{tmpdir_version}-%{release}
Provides:       rubygem-tsort = %{tsort_version}-%{release}
Provides:       rubygem(tsort) = %{tsort_version}-%{release}
Provides:       rubygem-un = %{un_version}-%{release}
Provides:       rubygem(un) = %{un_version}-%{release}
Provides:       rubygem-uri = %{uri_version}-%{release}
Provides:       rubygem(uri) = %{uri_version}-%{release}
Provides:       rubygem-weakref = %{weakref_version}-%{release}
Provides:       rubygem(weakref) = %{weakref_version}-%{release}
Provides:       rubygem-win32ole = %{win32ole_version}-%{release}
Provides:       rubygem(win32ole) = %{win32ole_version}-%{release}
Provides:       rubygem-yaml = %{yaml_version}-%{release}
Provides:       rubygem(yaml) = %{yaml_version}-%{release}
Provides:       rubygem-zlib = %{zlib_version}-%{release}
Provides:       rubygem(zlib) = %{zlib_version}-%{release}

%description
The Ruby package contains the Ruby development environment.
This is useful for object-oriented scripting.

%package -n rubygems
Summary:        The Ruby standard for packaging ruby libraries
Version:        %{rubygems_version}
License:        Ruby OR MIT
Requires:       ruby(release)
Recommends:     rubygem-io-console
Recommends:     rubygem-rdoc
Provides:       gem = %{rubygems_version}
Provides:       ruby(rubygems) = %{rubygems_version}
BuildArch:      noarch

%description -n rubygems
RubyGems is the Ruby standard for publishing and managing third party
libraries.

%package -n rubygems-devel
Summary:        Macros and development tools for packaging RubyGems
Version:        %{rubygems_version}
License:        Ruby OR MIT
Requires:       ruby(rubygems) >= %{rubygems_version}
# Needed for RDoc documentation format generation.
Requires:       rubygem-json
Requires:       rubygem-rdoc
BuildArch:      noarch

%description -n rubygems-devel
Macros and development tools for packaging RubyGems.

%prep
%autosetup -p1
# Remove all bundled gems
pushd gems
find -not -name 'bundled_gems' -delete
sed -i '2,$d' bundled_gems
popd
# Remove bigdecimal. Add them back when version provided by ruby >= current version
rm -rf ext/bigdecimal

%build
# Remove GCC specs and build environment linker scripts
# from the flags used when compiling outside of an RPM environment
export XCFLAGS="%{build_cflags}"
export XLDFLAGS="%{build_ldflags}"
export CFLAGS="%{extension_cflags}"
export LDFLAGS="%{extension_ldflags}"

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
%{_libdir}/*.so.3.1
%{_libdir}/*.so.3.1.4
%{_libdir}/pkgconfig/*.pc
%{_libdir}/ruby/*
%{_datadir}/ri/*
%{_docdir}/%{name}-%{version}
%{_mandir}/man1/*
%{_rpmconfigdir}/macros.d/macros.ruby
%{_rpmconfigdir}/macros.d/macros.rubygems
%{_rpmconfigdir}/fileattrs/rubygems.attr
%{_rpmconfigdir}/rubygems.req
%{_rpmconfigdir}/rubygems.prov
%{_rpmconfigdir}/rubygems.con
%dir %{rubygems_dir}
%{rubygems_dir}/rubygems

%files -n rubygems
%{_bindir}/gem
%dir %{rubygems_dir}
%{rubygems_dir}/rubygems

%files -n rubygems-devel
%{_rpmconfigdir}/macros.d/macros.rubygems
%{_rpmconfigdir}/fileattrs/rubygems.attr
%{_rpmconfigdir}/rubygems.req
%{_rpmconfigdir}/rubygems.prov
%{_rpmconfigdir}/rubygems.con

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 3.1.4-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon Aug 14 2023 Saul Paredes <saulparedes@microsoft.com> - 3.1.4-2
- Patch CVE-2023-36617

* Wed May 03 2023 Rakshaa Viswanathan <rviswanathan@microsoft.com> - 3.1.4-1
- Upgrade ruby to 3.1.4
- Update time_version to v0.2.2 to resolve CVE-2023-28756
- Update uri_version to v0.11.1 to resolve CVE-2023-28755

* Mon Dec 12 2022 Daniel McIlvaney <damcilva@microsoft.com> - 3.1.3-1
- Update to resolve CVE-2021-33621
- Add rubygem-bundler default gem back since the versions have converged.

* Tue May 31 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 3.1.2-3
- Remove bundled gems from ruby.
- Add provides for all default gems.

* Fri Apr 22 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.1.2-2
- Adding "Provides" for bundled gems: "minitest", "power_assert", "rake", and "test-unit".
- Updated vendor macros.

* Fri Apr 15 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 3.1.2-1
- Update to v3.1.2.
- Fix CVEs 2021-41817 and 2021-41819.
- Remove gems building with ruby, add them separately.

* Tue Apr 12 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.7.4-6
- Adding "gemdir" macro for compatibility with older specs.

* Mon Apr 11 2022 Olivia Crain <oliviacrain@microsoft.com> - 2.7.4-5
- Specify which flags should be stored for extension building

* Tue Mar 29 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.7.4-4
- Fixing "Provides".

* Fri Mar 25 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.7.4-3
- Build rubygem, openssl, io-console, json, psych rubygems (taken from Fedora 33, license: MIT)

* Tue Mar 15 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.7.4-2
- Build bigdecimal, minitest, test-unit, rdoc and power_assert rubygems (taken from Fedora 37, license: MIT)

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
