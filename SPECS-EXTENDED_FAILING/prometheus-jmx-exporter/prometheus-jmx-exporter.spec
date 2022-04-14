Vendor:         Microsoft Corporation
Distribution:   Mariner
%global version_id parent
%global upstream_name jmx_exporter
%global simple_client_version 0.6.0

# Filter requires for the Java Agent as deps are shaded within.
%global jmx_or_client io\\.prometheus\\.jmx:.*|io\\.prometheus:simpleclient.*|org\\.yaml:snakeyaml.*
%global mvn_requires_filter .*mvn\\(%{jmx_or_client}\\)
%global __requires_exclude ^%{mvn_requires_filter}$

Name:           prometheus-jmx-exporter
Version:        0.12.0
Release:        4%{?dist}
Summary:        Prometheus JMX Exporter

License:        ASL 2.0
URL:            https://github.com/prometheus/jmx_exporter/

Source0:        https://github.com/prometheus/jmx_exporter/archive/%{version_id}-%{version}.tar.gz
Patch1:         properly_rewrite_namespace.patch

BuildArch:  noarch

BuildRequires: maven-local
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires: mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires: mvn(org.apache.maven.plugins:maven-shade-plugin)
BuildRequires: mvn(org.yaml:snakeyaml)
BuildRequires: mvn(io.prometheus:simpleclient)
BuildRequires: mvn(io.prometheus:simpleclient_hotspot)
BuildRequires: mvn(io.prometheus:simpleclient_common)
BuildRequires: mvn(io.prometheus:simpleclient_httpserver)

Provides: bundled(io.prometheus.jmx:collector) = %{version}
Provides: bundled(io.prometheus:simpleclient) = %{simple_client_version}
Provides: bundled(org.yaml:snakeyaml) = 1.17
Provides: bundled(biz.source_code:base64coder) = 2010.12.19
Provides: bundled(commons-codec:commons-codec) = 1.11
Provides: bundled(io.prometheus:simpleclient_hotspot) = %{simple_client_version}
Provides: bundled(io.prometheus:simpleclient_httpserver) = %{simple_client_version}
Provides: bundled(io.prometheus:simpleclient_common) = %{simple_client_version}

%description
JMX to Prometheus exporter: a collector that can be configured to scrape
and expose MBeans of a JMX target. This exporter is intended to be run as
a Java Agent, exposing a HTTP server and serving metrics of the local JVM.

%prep
%setup -q -n %{upstream_name}-%{version_id}-%{version}

%patch1 -p1

%pom_remove_plugin org.vafer:jdeb jmx_prometheus_httpserver
%pom_remove_plugin org.apache.maven.plugins:maven-failsafe-plugin jmx_prometheus_javaagent
%pom_remove_plugin org.codehaus.mojo:build-helper-maven-plugin jmx_prometheus_javaagent

# Don't install artefacts from the reactor but the java agent itself. This is because
# the agent needs deps from the reactor but shades them.
%mvn_package "io.prometheus.jmx:jmx_prometheus_httpserver" __noinstall
%mvn_package "io.prometheus.jmx:parent" __noinstall

# Don't depend on obsolete sonatype-oss-parent
# See: https://github.com/prometheus/jmx_exporter/issues/420
%pom_xpath_remove pom:project/pom:parent

%build
%mvn_build -f -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE
%doc NOTICE

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.12.0-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 03 2019 Severin Gehwolf <sgehwolf@redhat.com> - 0.12.0-2
- Add patch to properly name-space included dependencies

* Mon Aug 12 2019 Severin Gehwolf <sgehwolf@redhat.com> - 0.12.0-1
- Initial package.

