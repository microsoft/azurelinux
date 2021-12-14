Vendor:         Microsoft Corporation
Distribution:   Mariner
%global version_id parent
%global upstream_name client_java

Name:          prometheus-simpleclient-java
Version:       0.6.0
Release:       4%{?dist}
Summary:       Prometheus JVM Client

License:       ASL 2.0 and CC0
URL:           https://github.com/prometheus/client_java/

Source0:       https://github.com/prometheus/client_java/archive/%{version_id}-%{version}.tar.gz

BuildArch:     noarch

BuildRequires: maven-local
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires: mvn(junit:junit)

%description
Prometheus instrumentation library for JVM applications.

%prep
%setup -q -n %{upstream_name}-%{version_id}-%{version}

# Remove included jar files
find . -name \*.jar -print0 | xargs -0 rm

# Only build the following artefacts as these are actually dependencies
# of prometheus_jmxexporter
# 
# io.prometheus:simpleclient
# io.prometheus:simpleclient_hotspot
# io.prometheus:simpleclient_httpserver
# io.prometheus:simpleclient_common
for m in simpleclient_caffeine \
         simpleclient_dropwizard \
         simpleclient_graphite_bridge \
         simpleclient_hibernate \
         simpleclient_guava \
         simpleclient_log4j \
         simpleclient_log4j2 \
         simpleclient_logback \
         simpleclient_pushgateway \
         simpleclient_servlet \
         simpleclient_spring_web \
         simpleclient_spring_boot \
         simpleclient_jetty \
         simpleclient_jetty_jdk8 \
         simpleclient_vertx \
         benchmark; do
%pom_disable_module $m
done

# Remove test dependencies for hotspot
%pom_remove_dep io.prometheus:simpleclient_servlet simpleclient_hotspot
%pom_remove_dep org.mockito:mockito-core simpleclient_hotspot
%pom_remove_dep org.eclipse.jetty:jetty-servlet simpleclient_hotspot
# Remove test dependencies for httpserver
%pom_remove_dep org.assertj:assertj-core simpleclient_httpserver

# Don't depend on obsolete sonatype-oss-parent
# See: https://github.com/prometheus/client_java/pull/497
%pom_xpath_remove pom:project/pom:parent

# Remove tests which wouldn't compile with removed deps
for i in $(find simpleclient_hotspot/src/test/java/io/prometheus/client/hotspot -name \*.java); do
  if ! echo $i | grep -q -E 'VersionInfoExportsTest\.java|MemoryAllocationExportsTest\.java'; then
    rm $i
  fi
done
rm -rf simpleclient_httpserver/src/test/java

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE
%doc NOTICE

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.0-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Severin Gehwolf <sgehwolf@redhat.com> - 0.6.0-2
- Enable some tests during build.

* Mon Aug 12 2019 Severin Gehwolf <sgehwolf@redhat.com> - 0.6.0-1
- Initial package.

