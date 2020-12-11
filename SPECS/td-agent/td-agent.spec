%define      debug_package %{nil}
%define control_service() (systemctl %{1} %{2})
%define disable_service() (systemctl %{1} %{2})
%define enable_service() (systemctl %{1} %{2})
Summary:        The stable distribution of Fluentd
Name:           td-agent
Version:        4.0.1
Release:        1%{?dist}
License:        ASL 2.0 AND BSD AND MIT AND Jason Evans Open Source
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://github.com/fluent-plugins-nursery/td-agent-builder
#Source0:      https://github.com/fluent-plugins-nursery/td-agent-builder/archive/testing-uploading-artifacts3.tar.gz
Source0:        td-agent-builder-testing-uploading-artifacts3.tar.gz
Source1:        httpclient-2.8.2.4.gem
Source2:        td-client-1.0.7.gem
Source3:        td-0.16.8.gem
Source4:        fluent-plugin-td-1.1.0.gem
Source5:        jmespath-1.4.0.gem
Source6:        aws-partitions-1.288.0.gem
Source7:        aws-sigv4-1.1.1.gem
Source8:        aws-sdk-core-3.92.0.gem
Source9:        aws-sdk-kms-1.30.0.gem
Source10:       aws-sdk-sqs-1.24.0.gem
Source11:       aws-sdk-s3-1.61.1.gem
Source12:       fluent-plugin-s3-1.3.0.gem
Source13:       webhdfs-0.9.0.gem
Source14:       fluent-plugin-webhdfs-1.2.4.gem
Source15:       fluent-plugin-rewrite-tag-filter-2.3.0.gem
Source16:       ruby-kafka-1.0.0.gem
Source17:       ltsv-0.1.2.gem
Source18:       fluent-plugin-kafka-0.13.0.gem
Source19:       elasticsearch-7.6.0.gem
Source20:       fluent-plugin-elasticsearch-4.0.7.gem
Source21:       prometheus-client-0.9.0.gem
Source22:       fluent-plugin-prometheus-1.7.3.gem
Source23:       fluent-plugin-prometheus_pushgateway-0.0.2.gem
Source24:       fluent-plugin-record-modifier-2.1.0.gem
Source25:       systemd-journal-1.3.3.gem
Source26:       fluent-plugin-systemd-1.0.2.gem
Source27:       nokogiri-1.11.0.rc2.gem
Source28:       fluentd-f5cc77783b7483dd72dc039c96a3ad970daa7835.tar.gz
Source29:       bundler-2.1.4.gem
Source30:       msgpack-1.3.3.gem
Source31:       cool.io-1.6.0.gem
Source32:       serverengine-2.2.1.gem
Source33:       oj-3.10.6.gem
Source34:       async-http-0.50.13.gem
Source35:       http_parser.rb-0.6.0.gem
Source36:       yajl-ruby-1.4.1.gem
Source37:       sigdump-0.2.4.gem
Source38:       tzinfo-2.0.2.gem
Source39:       tzinfo-data-1.2019.3.gem
Source40:       jemalloc-5.2.1.tar.bz2
Source41:       ruby-2.7.1.tar.gz
Source42:       rubyinstaller-2.7.1-1-x64.7z
Source43:       strptime-0.2.5.gem
Source44:       concurrent-ruby-1.1.7.gem
Source45:       protocol-http2-0.13.2.gem
Source46:       protocol-http1-0.11.1.gem
Source47:       protocol-http-0.17.0.gem
Source48:       async-pool-0.3.3.gem
Source49:       async-io-1.30.1.gem
Source50:       async-1.27.0.gem
Source51:       protocol-hpack-1.4.2.gem
Source52:       timers-4.3.2.gem
Source53:       nio4r-2.5.4.gem
Source54:       console-1.10.1.gem
Source55:       fiber-local-1.0.0.gem
Source56:       ruby-progressbar-1.10.1.gem
Source57:       zip-zip-0.3.gem
Source58:       rubyzip-1.3.0.gem
Source59:       td-logger-0.3.27.gem
Source60:       parallel-1.20.1.gem
Source61:       hirb-0.7.3.gem
Source62:       fluent-logger-0.9.0.gem
Source63:       aws-eventstream-1.1.0.gem
Source64:       addressable-2.7.0.gem
Source65:       public_suffix-4.0.6.gem
Source66:       fluent-config-regexp-type-1.0.0.gem
Source67:       digest-crc-0.6.1.gem
Source68:       rake-13.0.1.gem
Source69:       rake-12.3.3.gem
Source70:       mini_portile2-2.5.0.gem
Source71:       ffi-1.13.1.gem
Source72:       librdkafka-1.4.0.tar.gz
Source73:       rdkafka-ruby-0.7.0.tar.gz
Source74:       elasticsearch-api-7.6.0.gem
Source75:       elasticsearch-transport-7.6.0.gem
Source76:       multi_json-1.15.0.gem
Source77:       faraday-1.1.0.gem
Source78:       ruby2_keywords-0.0.2.gem
Source79:       multipart-post-2.1.1.gem
Source80:       excon-0.78.0.gem
Source81:       quantile-0.2.1.gem
Patch0:         td-agent.patch
Patch1:         rdkafka.patch
BuildRequires:  build-essential
BuildRequires:  git
BuildRequires:  libedit-devel
BuildRequires:  libyaml-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  pkg-config
BuildRequires:  ruby
BuildRequires:  rubygem-bundler
BuildRequires:  sudo
BuildRequires:  systemd
BuildRequires:  tar
BuildRequires:  unzip
BuildRequires:  zlib-devel
Requires:       libxcrypt

%description
The stable distribution of Fluentd

%prep
cd %{_prefix}/src/mariner/SOURCES
tar xzvf %{SOURCE73}
cd rdkafka-ruby-0.7.0
patch -p1 < %{PATCH1}
gem build ./rdkafka.gemspec
cp rdkafka-0.7.0.gem ..
cd ..
tar czvf gemfile.tar.gz *.gem
%setup -q -n td-agent-builder-testing-uploading-artifacts3
%patch0 -p1

%build

%install
sudo rake build:rpm_config TD_AGENT_STAGING_PATH=%{buildroot}
sudo rake build:all TD_AGENT_STAGING_PATH=%{buildroot}
mkdir -p %{buildroot}%{_mandir}/man1
for man in `find %{buildroot} -type f -wholename '*/man/man[1-9]/*.[1-9]'`; do
    gzip ${man}
done

cd -
mkdir -p %{buildroot}%{_localstatedir}/run/td-agent
mkdir -p %{buildroot}%{_localstatedir}/log/td-agent
mkdir -p %{buildroot}%{_localstatedir}/log/td-agent/buffer
mkdir -p %{buildroot}%{_sysconfdir}/td-agent/plugin
mkdir -p %{buildroot}/tmp/td-agent

%pre
sudo ln -S %{_sbindir}/useradd %{_sbindir}/adduser
if ! getent group td-agent >/dev/null; then
    %{_sbindir}/groupadd -r td-agent
fi
if ! getent passwd td-agent >/dev/null; then
    %{_sbindir}/adduser -r -g td-agent -d %{_localstatedir}/lib/td-agent -s /sbin/nologin -c 'td-agent' td-agent
fi

%preun
if [ $1 -eq 0 ]; then
  %{control_service stop td-agent}
  %{disable_service disable td-agent}
fi

%post
if [ $1 -eq 1 ]; then
  %{enable_service enable td-agent}
fi
if [ $1 -eq 2 ]; then
  %{control_service condrestart td-agent}
fi
if [ -d "%{_sysconfdir}/prelink.conf.d/" ]; then
  echo "prelink detected. Installing %{_sysconfdir}/prelink.conf.d/td-agent-ruby.conf ..."
  if [ ! -f %{_sysconfdir}/prelink.conf.d/td-agent-ruby.conf ]; then
      cp -f /opt/td-agent/share/td-agent-ruby.conf %{_sysconfdir}/prelink.conf.d/td-agent-ruby.conf
  else
    if [ $(grep '\-b /opt/td-agent/embedded/bin/ruby' -c %{_sysconfdir}/prelink.conf.d/td-agent-ruby.conf) -eq 1 ]; then
      echo "old-prelink detected, Update %{_sysconfdir}/prelink.conf ..."
      sed -i"" %{_sysconfdir}/prelink.conf.d/td-agent-ruby.conf -e "s,/embedded/,/,"
    fi
  fi
elif [ -f "%{_sysconfdir}/prelink.conf" ]; then
  if [ $(grep '\-b /opt/td-agent/embedded/bin/ruby' -c %{_sysconfdir}/prelink.conf) -eq 1 ]; then
    echo "old-prelink detected, but %{_sysconfdir}/prelink.conf.d/ does't exist. Update %{_sysconfdir}/prelink.conf ..."
    sed -i"" %{_sysconfdir}/prelink.conf -e "s,/embedded/,/,"
  elif [ $(grep '\-b /opt/td-agent/bin/ruby' -c %{_sysconfdir}/prelink.conf) -eq 0 ]; then
    echo "prelink detected, but %{_sysconfdir}/prelink.conf.d/ does't exist. Adding %{_sysconfdir}/prelink.conf ..."
    echo "-b /opt/td-agent/bin/ruby" >> %{_sysconfdir}/prelink.conf
  fi
fi
sudo systemctl start td-agent

%files
%doc README.md
%license LICENSE
%defattr(-,root,root,-)
/opt/*
/opt/td-agent/share/td-agent.conf.tmpl
%{_prefix}/%{_unitdir}/td-agent.service
%{_tmpfilesdir}/td-agent.conf
%{_bindir}/td
%{_sbindir}/td-agent
%{_sbindir}/td-agent-gem
%config(noreplace) %{_sysconfdir}/td-agent/td-agent.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/td-agent
%attr(0755,td-agent,td-agent) %dir %{_localstatedir}/log/td-agent
%attr(0755,td-agent,td-agent) %dir %{_localstatedir}/log/td-agent/buffer
%attr(0755,td-agent,td-agent) %dir %{_sysconfdir}/td-agent
%attr(0755,td-agent,td-agent) %dir %{_sysconfdir}/td-agent/plugin
# NOTE: %{_tmpfilesdir} is available since CentOS 7
%attr(0755,td-agent,td-agent) %dir /tmp/td-agent

%changelog
* Tue Dec 01 2020 Henry Li <lihl@microsoft.com> - 4.0.1-1
- Original version for CBL-Mariner