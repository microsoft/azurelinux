%define      debug_package %{nil}
%define gem_name fluentd
%global gem_dir %{_datadir}/gems
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
Summary:        Fluentd event collector
Name:           fluentd
Version:        1.11.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            http://fluentd.org/
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1:        fluentd.service
Source2:        strptime-0.2.5.gem
Source3:        tzinfo-data-1.2019.3.gem
Source4:        tzinfo-2.0.2.gem
Source5:        sigdump-0.2.4.gem
Source6:        http_parser.rb-0.6.0.gem
Source7:        serverengine-2.2.1.gem
Source8:        msgpack-1.3.3.gem
Source9:        cool.io-1.6.0.gem
Source10:       yajl-ruby-1.4.1.gem
Source11:       concurrent-ruby-1.1.7.gem
BuildRequires:  systemd
BuildRequires:  jemalloc
BuildRequires:  ruby
BuildRequires:  rubygem-bundler
Requires:       systemd
Requires:       jemalloc

%define gem_instdir %{gem_dir}%{gemdir}/gems/%{gem_name}-%{version}
%define gem_libdir %{gem_instdir}/lib
%define gem_cache %{gem_dir}%{gemdir}/cache/%{gem_name}-%{version}.gem
%define gem_spec %{gem_dir}%{gemdir}/specifications/%{gem_name}-%{version}.gemspec
%define gem_docdir %{gem_dir}%{gemdir}/doc/%{gem_name}-%{version}

# %gem_install - Install gem into appropriate directory.
#
# Usage: %gem_install [options]	
#
# -n <gem_file>      Overrides gem file name for installation.	
# -d <install_dir>   Set installation directory.
#
%define gem_install(d:n:) mkdir -p %{-d*}%{!?-d:.%{gem_dir}} \
\
CONFIGURE_ARGS="--with-cflags='%{optflags}' --with-cxxflags='%{optflags}' $CONFIGURE_ARGS" \
gem install -V --local --build-root %{-d*}%{!?-d:.} --force --document=ri,rdoc %{-n*}%{!?-n:%{gem_name}-%{version}.gem} \
%{nil}

# %gemspec_remove_dep - Remove dependency from .gemspec.	
#
# Usage: %gemspec_remove_dep -g <gem> [options] [requirements]	
#
# Remove dependency named <gem> from .gemspec file. The macro removes runtime	
# dependency by default. The [requirements] argument can be used to specify
# the dependency constraints more precisely. It is expected to be valid Ruby
# code. The macro fails if these specific requirements can't be removed.
#
# -s <gemspec_file>   Overrides the default .gemspec location.	
# -d                  Remove development dependecy.
#
%define gemspec_remove_dep(g:s:d) read -d '' gemspec_remove_dep_script << 'EOR' || : \
  gemspec_file = '%{-s*}%{!?-s:%{_builddir}/%{gem_name}-%{version}/%{gem_name}.gemspec}' \
  \
  name = '%{-g*}' \
  requirements = %{*}%{!?1:nil} \
  \
  type = :%{!?-d:runtime}%{?-d:development} \
  \
  spec = Gem::Specification.load(gemspec_file) \
  abort("#{gemspec_file} is not accessible.") unless spec \
  \
  dep = spec.dependencies.detect { |d| d.type == type && d.name == name } \
  if dep \
    if requirements \
      requirements = Gem::Requirement.create(requirements).requirements \
      requirements.each do |r| \
        unless dep.requirement.requirements.reject! { |dependency_requirements| dependency_requirements == r } \
          abort("Requirement '#{r.first} #{r.last}' was not possible to remove for dependency '#{dep}'!") \
        end \
      end \
      spec.dependencies.delete dep if dep.requirement.requirements.empty? \
    else \
      spec.dependencies.delete dep \
    end \
  else \
    abort("Dependency '#{name}' was not found!") \
  end \
  File.write gemspec_file, spec.to_ruby \
EOR\
echo "$gemspec_remove_dep_script" | ruby \
unset -v gemspec_remove_dep_script \
%{nil}

%description
Fluentd is an open source data collector designed to scale and simplify log
management. It can collect, process and ship many kinds of data in near
real-time.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%gemspec_remove_dep -g tzinfo-data 

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

cp %{SOURCE2} .
cp %{SOURCE3} .
cp %{SOURCE4} .
cp %{SOURCE5} .
cp %{SOURCE6} .
cp %{SOURCE7} .
cp %{SOURCE8} .
cp %{SOURCE9} .
cp %{SOURCE10} .
cp %{SOURCE11} .

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install -n %{gem_name}-%{version}.gem -d .%{gem_dir}

%install
mkdir -p %{buildroot}%{gem_instdir}
cp -a .%{gem_instdir}/* %{buildroot}%{gem_instdir}/

mkdir -p %{buildroot}%{gem_libdir}
cp -a .%{gem_libdir}/* %{buildroot}%{gem_libdir}/

#mkdir -p %{buildroot}%{gem_spec}
#cp -a .%{gem_spec}/* %{buildroot}%{gem_spec}/

mkdir -p %{buildroot}%{gem_docdir}
cp -a .%{gem_docdir}/* %{buildroot}%{gem_docdir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{gem_dir}%{_bindir}/* %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_sysconfdir}/%{gem_name}
mv .%{gem_instdir}/fluent.conf %{buildroot}%{_sysconfdir}/%{gem_name}

mkdir -p %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/

#rm -f %{buildroot}%{gem_dir}%{_bindir}/*
rm -f %{buildroot}%{gem_instdir}/{.gitignore,.travis.yml}

%pre
# NOTE(mmagr): httpd logs have 0700 mode now for root, so we need to run
#              fluentd service as root to be able to collect all logs
#getent group fluentd >/dev/null || groupadd -r fluentd
#getent passwd fluentd >/dev/null || \
#    useradd -r -g fluentd -d /etc/fluentd -s /sbin/nologin \
#    -c "Fluentd data collection agent" fluentd
#exit 0

%post
%systemd_post fluentd.service

%preun
%systemd_preun fluentd.service

%postun
%systemd_postun fluentd.service

%files
%defattr(-,root,root)
%dir %{gem_instdir}
%{gem_instdir}/*
%attr(755, root, root) %{_bindir}/fluent-cat
%attr(755, root, root) %{_bindir}/fluent-debug
%attr(755, root, root) %{_bindir}/fluent-gem
%attr(755, root, root) %{_bindir}/fluentd
%attr(755, root, root) %{_bindir}/fluent-binlog-reader
%attr(755, root, root) %{_bindir}/fluent-ca-generate
%attr(755, root, root) %{_bindir}/fluent-plugin-config-format
%attr(755, root, root) %{_bindir}/fluent-plugin-generate
%{gem_instdir}/bin
%{gem_libdir}
%attr(644, root, root) /%{_unitdir}/fluentd.service
%dir %{_sysconfdir}/%{gem_name}
%config(noreplace) %{_sysconfdir}/%{gem_name}/fluent.conf

%files doc
%defattr(-,root,root)
%doc %{gem_docdir}
%{gem_instdir}/Rakefile
%{gem_instdir}/test/
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/example/*
%doc %{gem_instdir}/AUTHORS
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md

%changelog
* Wed Dec 16 2020 Henry Li <lihl@microsoft.com> - 1.11.0-1
- Initial import from RedHat. License verified.

* Tue Feb 13 2018 Sandro Bonazzola <sbonazzo@redhat.com> - 0.12.42-2
- Rebase on 0.12.42
- Require jemalloc

* Fri Jan 19 2018 Sandro Bonazzola <sbonazzo@redhat.com> - 0.12.41-2
- Remove tzinfo-data also from gem spec.

* Thu Dec 07 2017 Richard Megginson <rmeggins@redhat.com> - 0.12.41-1
- version 0.12.41

* Wed Aug 23 2017 Rich Megginson <rmeggins@redhat.com> - 0.12.39-2
- remove utf-8 patch to allow file buffering to work

* Tue Aug 15 2017 Rich Megginson <rmeggins@redhat.com> - 0.12.39-1
- version 0.12.39

* Fri Jul 21 2017 Sandro Bonazzola <sbonazzo@redhat.com> - 0.12.37-2
- Restored runtime dependency hostname lost during rebase on 0.12.37

* Fri Jul 21 2017 Rich Megginson <rmeggins@redhat.com> - 0.12.37-1
- version 0.12.37

* Fri Jul 14 2017 Juan Badia Payno <jbadiapa@redhat.com> - 0.12.31-5
- Add runtime dependency hostname,so this package can be used by
other distros than CentOS

* Thu Jun 15 2017 Sandro Bonazzola <sbonazzo@redhat.com> - 0.12.31-4
- Add missing requirement on rubygem-thread_safe

* Mon Apr 10 2017 Lon Hohberger <lon@redhat.com> - 0.12.31-3
- Fix %%defattr line to match expected UID/GIDs (rhbz#1426169)

* Tue Feb 28 2017 Martin Mágr <mmagr@redhat.com> - 0.12.31-2
- Run fluentd service as root to be able to gather httpd logs (rhbz#1426169)

* Mon Jan  9 2017 Rich Megginson <rmeggins@redhat.com> - 0.12.31-1
- update to 0.12.31

* Mon Dec 12 2016 Rich Megginson <rmeggins@redhat.com> - 0.12.30-1
- update to 0.12.30

* Tue Sep 20 2016 Rich Megginson <rmeggins@redhat.com> - 0.12.29-1
- update to 0.12.29

* Thu Aug 04 2016 Rich Megginson <rmeggins@redhat.com> - 0.12.20-2
- Rebuild to add provides for rubygem(fluentd)

* Fri Feb 05 2016 Troy Dawson <tdawson@redhat.com> - 0.12.20-1
- Updated to latest release

* Fri Oct 16 2015 Troy Dawson <tdawson@redhat.com> - 0.12.16-1
- Updated to latest release
- Added patch to fix UTF error

* Wed Sep 09 2015 Troy Dawson <tdawson@redhat.com> - 0.12.15-2
- Add a provides to spec file

* Mon Aug 31 2015 Troy Dawson <tdawson@redhat.com> - 0.12.15-1
- Updated to latest release

* Wed Jul 29 2015 Graeme Gillies <ggillies@redhat.com> - 0.12.5-3
- Corrected ownership on executable files in /usr/bin

* Tue Jun 02 2015 Graeme Gillies <ggillies@redhat.com> - 0.12.5-2
- Fixed file ownership permissions for package

* Mon Feb 16 2015 Graeme Gillies <ggillies@redhat.com> - 0.12.5-1
- Upgraded to 0.12.5

* Mon Jan 05 2015 Graeme Gillies <ggillies@redhat.com> - 0.12.2-1
- Initial package