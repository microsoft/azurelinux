# The RubyGems library has to stay out of Ruby directory tree, since the
# RubyGems should be share by all Ruby implementations.
%global rubygems_dir %{_datadir}/rubygems
%global bigdecimal_version 2.0.0
%global io_console_version 0.5.6
%global psych_version      3.1.0
%global irb_version        1.2.6
%global gem_dir %{_libdir}/ruby/gems
Summary:        Ruby
Name:           ruby
Version:        2.7.2
Release:        1%{?dist}
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
Provides:       %{_prefix}/local/bin/ruby
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}(release) = %{version}-%{release}
Provides:       %{name}-libs = %{version}-%{release}
Provides:       rubygems = %{version}-%{release}
Provides:       rubygems-devel = %{version}-%{release}
Provides:       ruby(rubygems) = %{version}-%{release}
Provides:       rubygem(bigdecimal) = %{version}-%{release}
Provides:       rubygem(io-console) = %{version}-%{release}
Provides:       rubygem(psych) = %{version}-%{release}
Provides:       rubygem(did_you_mean) = %{version}-%{release}
Provides:       rubygem(irb) = %{version}-%{release}

%description
The Ruby package contains the Ruby development environment.
This is useful for object-oriented scripting.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

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
        --with-sitearchhdrdir={_prefix}/local/%{_lib}/ruby/site_ruby/$(_arch) \
        --with-vendorarchhdrdir=%{_libdir}/ruby/vendor_ruby/$(_arch) \
        --with-rubygemsdir=%{rubygems_dir} \
        --enable-shared \
        --with-compress-debug-sections=no \
        --with-ruby-version='' \
        --docdir=%{_docdir}/%{name}-%{version}
make %{?_smp_mflags} COPY="cp -p"

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install

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
mkdir -p %{buildroot}%{gem_dir}/bigdecimal-%{bigdecimal_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{name}/bigdecimal-%{bigdecimal_version}/bigdecimal
mv %{buildroot}%{_libdir}/ruby/bigdecimal %{buildroot}%{gem_dir}/bigdecimal-%{bigdecimal_version}/lib
mv %{buildroot}%{gem_dir}/specifications/default/bigdecimal-%{bigdecimal_version}.gemspec %{buildroot}%{gem_dir}/specifications
ln -s %{gem_dir}/bigdecimal-%{bigdecimal_version}/lib/bigdecimal %{buildroot}%{_libdir}/ruby/bigdecimal

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

%check
chmod g+w . -R
useradd test -G root -m
sudo -u test  make check TESTS="-v"

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*


%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.so.*
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

%changelog
* Thu Mar 11 2021 Henry Li <lihl@microsoft.com> - 2.6.6-4
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

*   Thu Oct 15 2020 Emre Girgin <mrgirgin@microsoft.com> 2.6.6-1
-   Upgrade to 2.6.6 to resolve CVEs.

*   Sat May 09 00:20:42 PST 2020 Nick Samson <nisamson@microsoft.com> - 2.6.3-3
-   Added %%license line automatically

*   Wed May 06 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 2.6.3-2
-   Removing *Requires for "ca-certificates".

*   Fri Mar 13 2020 Paul Monson <paulmon@microsoft.com> 2.6.3-1
-   Update to version 2.6.3. License verified.

*   Mon Feb 3 2020 Andrew Phelps <anphel@microsoft.com> 2.5.3-3
-   Disable compressing debug sections

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.5.3-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Tue Jan 01 2019 Sujay G <gsujay@vmware.com> 2.5.3-1
-   Update to version 2.5.3, to fix CVE-2018-16395 & CVE-2018-16396

*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 2.5.1-1
-   Update to version 2.5.1

*   Fri Jan 12 2018 Xiaolin Li <xiaolinl@vmware.com> 2.4.3-2
-   Fix CVE-2017-17790

*   Wed Jan 03 2018 Xiaolin Li <xiaolinl@vmware.com> 2.4.3-1
-   Update to version 2.4.3, fix CVE-2017-17405

*   Fri Sep 29 2017 Xiaolin Li <xiaolinl@vmware.com> 2.4.2-1
-   Update to version 2.4.2

*   Fri Sep 15 2017 Xiaolin Li <xiaolinl@vmware.com> 2.4.1-5
-   [security] CVE-2017-14064

*   Tue Sep 05 2017 Chang Lee <changlee@vmware.com> 2.4.1-4
-   Built with copy preserve mode and fixed %check

*   Mon Jul 24 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.1-3
-   [security] CVE-2017-9228

*   Tue Jun 13 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.1-2
-   [security] CVE-2017-9224,CVE-2017-9225
-   [security] CVE-2017-9227,CVE-2017-9229

*   Thu Apr 13 2017 Siju Maliakkal <smaliakkal@vmware.com> 2.4.1-1
-   Update to latest 2.4.1

*   Wed Jan 18 2017 Anish Swaminathan <anishs@vmware.com> 2.4.0-1
-   Update to 2.4.0 - Fixes CVE-2016-2339

*   Mon Oct 10 2016 ChangLee <changlee@vmware.com> 2.3.0-4
-   Modified %check

*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.3.0-3
-   GA - Bump release of all rpms

*   Wed Mar 09 2016 Divya Thaluru <dthaluru@vmware.com> 2.3.0-2
-   Adding readline support

*   Wed Jan 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.3.0-1
-   Updated to 2.3.0-1

*   Tue Apr 28 2015 Fabio Rapposelli <fabio@vmware.com> 2.2.1-2
-   Added SSL support

*   Mon Apr 6 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.2.1-1
-   Version upgrade to 2.2.1

*   Fri Oct 10 2014 Divya Thaluru <dthaluru@vmware.com> 2.1.3-1
-   Initial build.  First version
