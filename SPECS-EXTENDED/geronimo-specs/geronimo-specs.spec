Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package geronimo-specs
#
# Copyright (c) 2020 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%define bname geronimo
Name:           geronimo-specs
Version:        1.2
Release:        40%{?dist}
Summary:        Geronimo J2EE server J2EE specifications
License:        ASL 2.0
Group:          Development/Languages/Java
URL:            https://geronimo.apache.org
Source0:        %{_distro_sources_url}/%{name}-%{version}.tar.gz
# STEPS TO CREATE THE SOURCE FILE
# mkdir geronimo-specs-1.2
# cd geronimo-specs-1.2
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-activation_1.0.2_spec-1.2/
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-activation_1.1_spec-1.0/
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-annotation_1.0_spec-1.1.0/
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-ejb_2.1_spec-1.1/
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-ejb_3.0_spec-1.0/
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-el_1.0_spec-1.0/
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-interceptor_3.0_spec-1.0/
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-j2ee-connector_1.5_spec-1.1.1/
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-j2ee-deployment_1.1_spec-1.1/
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-j2ee-jacc_1.0_spec-1.1/
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-j2ee-management_1.0_spec-1.1/
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-j2ee-management_1.1_spec-1.0/
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-jacc_1.1_spec-1.0/
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-javaee-deployment_1.1MR3_spec-1.0/
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-jpa_3.0_spec-1.1.0/
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-jsp_2.0_spec-1.1/
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-jsp_2.1_spec-1.0/
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-jta_1.0.1B_spec-1.1.1/
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-jta_1.1_spec-1.1.0/
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-qname_1.1_spec-1.1/
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-servlet_2.4_spec-1.1.1/
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-servlet_2.5_spec-1.1/
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-stax-api_1.0_spec-1.0/
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-ws-metadata_2.0_spec-1.1.1/
# # AS WELL AS
# svn export https://svn.apache.org/repos/asf/geronimo/specs/trunk/geronimo-jaspi_1.0_spec/
# # AND
# curl -O https://svn.apache.org/repos/asf/geronimo/specs/trunk/pom.xml
# curl -O https://svn.apache.org/repos/asf/geronimo/specs/trunk/LICENSE.txt
# curl -O https://svn.apache.org/repos/asf/geronimo/specs/trunk/NOTICE.txt
# curl -O https://svn.apache.org/repos/asf/geronimo/specs/trunk/README.txt
# cd ..
# tar --sort=name \
#     --mtime="2021-04-26 00:00Z" \
#     --owner=0 --group=0 --numeric-owner \
#     --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#     -cf %%{name}-%%{version}.tar.gz %%{name}-%%{version}
Source1000:     geronimo-specs.build.xml
Source1001:     undot.py
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  junit >= 3.8.1
BuildConflicts: java-devel >= 11
BuildConflicts: java-headless >= 11
BuildConflicts: java-devel-openj9
BuildConflicts: java-headless-openj9
BuildArch:      noarch

%description
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications Note: You should use the subpackages for the
Specifications that you actually need.	The ones installed by the main
package are deprecated and will disapear in future releases.

%package -n geronimo-jaf-1_0_2-api
Summary:        Geronimo J2EE server J2EE specifications
Group:          Development/Languages/Java
Requires(pre):  update-alternatives
Provides:       jaf = 1.0.2
# TODO: drop asap
Provides:       activation_1_0_2_api = %{version}
Provides:       activation_api = 1.0.2
Provides:       jaf_1_0_2_api = %{version}
Provides:       jaf_api = 1.0.2

%description -n geronimo-jaf-1_0_2-api
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications: Java Activation Framework

%package -n geronimo-jaf-1_1-api
Summary:        Geronimo J2EE server J2EE specifications
Group:          Development/Languages/Java
Requires(pre):  update-alternatives
Provides:       jaf = 1.1
# TODO: drop asap
Provides:       activation_1_1_api = %{version}
Provides:       activation_api = 1.1
Provides:       jaf_1_1_api = %{version}
Provides:       jaf_api = 1.1

%description -n geronimo-jaf-1_1-api
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications Note: You should use the subpackages for the
Specifications that you actually need.	The ones installed by the main
package are deprecated and will disapear in future releases.

%package -n geronimo-annotation-1_0-api
Summary:        Geronimo J2EE server J2EE specifications
Group:          Development/Languages/Java
Requires(pre):  update-alternatives
Provides:       annotation_1_0_api
Provides:       annotation_api = 1.0

%description -n geronimo-annotation-1_0-api
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications Note: You should use the subpackages for the
Specifications that you actually need.	The ones installed by the main
package are deprecated and will disapear in future releases.

%package -n geronimo-ejb-2_1-api
Summary:        Geronimo J2EE server J2EE specifications
Group:          Development/Languages/Java
Requires:       jta_1_0_1B_api
Requires(pre):  update-alternatives
Provides:       ejb = 2.1
# TODO: drop asap
Provides:       ejb_2_1_api = %{version}
Provides:       ejb_api = 2.1

%description -n geronimo-ejb-2_1-api
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications: Enterprise JavaBeans Specification

%package -n geronimo-ejb-3_0-api
Summary:        Geronimo J2EE server J2EE specifications
Group:          Development/Languages/Java
Requires:       annotation_1_0_api
Requires:       interceptor_3_0_api
Requires:       jta_1_1_api
Requires(pre):  update-alternatives
Provides:       ejb = 3.0
# TODO: drop asap
Provides:       ejb_3_0_api = %{version}
Provides:       ejb_api = 3.0

%description -n geronimo-ejb-3_0-api
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications Note: You should use the subpackages for the
Specifications that you actually need.	The ones installed by the main
package are deprecated and will disapear in future releases.

%package -n geronimo-el-1_0-api
Summary:        Geronimo J2EE server J2EE specifications
Group:          Development/Languages/Java
Requires(pre):  update-alternatives
Provides:       el_1_0_api = %{version}
Provides:       el_api = 1.0

%description -n geronimo-el-1_0-api
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications Note: You should use the subpackages for the
Specifications that you actually need.	The ones installed by the main
package are deprecated and will disapear in future releases.

%package -n geronimo-interceptor-3_0-api
Summary:        Geronimo J2EE server J2EE specifications
Group:          Development/Languages/Java
Requires(pre):  update-alternatives
Provides:       interceptor_3_0_api = %{version}
Provides:       interceptor_api = 3.0

%description -n geronimo-interceptor-3_0-api
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications Note: You should use the subpackages for the
Specifications that you actually need.	The ones installed by the main
package are deprecated and will disapear in future releases.

%package -n geronimo-j2ee-1_4-apis
Summary:        Geronimo J2EE server J2EE specifications
Group:          Development/Languages/Java
Requires(pre):  update-alternatives
Provides:       ejb_2_1_api = %{version}
Provides:       ejb_api = 2.1
Provides:       j2ee_connector_1_5_api = %{version}
Provides:       j2ee_connector_api = 1.5
Provides:       j2ee_deployment_1_1_api = %{version}
Provides:       j2ee_deployment_api = 1.1
Provides:       j2ee_management_1_0_api = %{version}
Provides:       j2ee_management_api = 1.0
Provides:       jacc_1_0_api = %{version}
Provides:       jacc_api = 1.0
Provides:       jaf_1_0_2_api = %{version}
Provides:       jaf_api = 1.0.2
Provides:       jsp_2_0_api = %{version}
Provides:       jsp_api = 2.0
Provides:       jta_1_0_1B_api = %{version}
Provides:       jta_api = 1.0.1B
Provides:       qname_1_1_api = %{version}
Provides:       qname_api = 1.1
Provides:       servlet_2_4_api = %{version}
Provides:       servlet_api = 2.4
Provides:       ejb = 2.1
Provides:       j2ee-connector = 1.5
Provides:       j2ee-deployment = 1.1
Provides:       j2ee-management = 1.0
Provides:       jacc = 1.0
Provides:       jaf = 1.0.2
Provides:       jsp = 2.0
Provides:       jta = 1.0.1B
# Provides:  qname = 1.1
Provides:       servlet = 2.4
# added Epoch
Provides:       geronimo-qname-1_1-api = %{version}

%description -n geronimo-j2ee-1_4-apis
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications: J2EE Specification (the complete set in one jar)

%package -n geronimo-j2ee-connector-1_5-api
Summary:        Geronimo J2EE server J2EE specifications
Group:          Development/Languages/Java
Requires:       jta_1_0_1B_api
Requires(pre):  update-alternatives
Provides:       j2ee_connector_1_5_api = %{version}
Provides:       j2ee_connector_api = 1.5
Provides:       j2ee-connector = 1.5

%description -n geronimo-j2ee-connector-1_5-api
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications: J2EE Connector Architecture Specification

%package -n geronimo-j2ee-deployment-1_1-api
Summary:        Geronimo J2EE server J2EE specifications
Group:          Development/Languages/Java
Requires(pre):  update-alternatives
Provides:       j2ee_deployment_1_1_api = %{version}
Provides:       j2ee_deployment_api = 1.1
Provides:       j2ee-deployment = 1.1

%description -n geronimo-j2ee-deployment-1_1-api
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications: J2EE Application Deployment Specification

%package -n geronimo-javaee-deployment-1_1-api
Summary:        Geronimo J2EE server J2EE specifications
Group:          Development/Languages/Java
Requires(pre):  update-alternatives
Provides:       javaee_deployment_1_1_api = %{version}
Provides:       javaee_deployment_api = 1.1

%description -n geronimo-javaee-deployment-1_1-api
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications Note: You should use the subpackages for the
Specifications that you actually need.	The ones installed by the main
package are deprecated and will disapear in future releases.

%package -n geronimo-jacc-1_0-api
Summary:        Geronimo J2EE server J2EE specifications
Group:          Development/Languages/Java
Requires:       servlet_2_4_api
Requires(pre):  update-alternatives
Provides:       jacc = 1.0
# TODO: drop asap
Provides:       jacc_1_0_api = %{version}
Provides:       jacc_api = 1.0

%description -n geronimo-jacc-1_0-api
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications: Java Authorization Contract for Containers
Specification

%package -n geronimo-jacc-1_1-api
Summary:        Geronimo J2EE server J2EE specifications
Group:          Development/Languages/Java
Requires:       servlet_2_5_api
Requires(pre):  update-alternatives
Provides:       jacc_1_1_api = %{version}
Provides:       jacc_api = 1.1

%description -n geronimo-jacc-1_1-api
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications Note: You should use the subpackages for the
Specifications that you actually need.	The ones installed by the main
package are deprecated and will disapear in future releases.

%package -n geronimo-j2ee-management-1_0-api
Summary:        Geronimo J2EE server J2EE specifications
Group:          Development/Languages/Java
Requires:       ejb_2_1_api
Requires(pre):  update-alternatives
Provides:       j2ee_management_1_0_api = %{version}
Provides:       j2ee_management_api = 1.0
Provides:       j2ee-management = 1.0

%description -n geronimo-j2ee-management-1_0-api
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications: J2EE Application Management Specification

%package -n geronimo-j2ee-management-1_1-api
Summary:        Geronimo J2EE server J2EE specifications
Group:          Development/Languages/Java
Requires:       ejb_3_0_api
Requires(pre):  update-alternatives
Provides:       j2ee_management_1_1_api = %{version}
Provides:       j2ee_management_api = 1.1
Provides:       j2ee-management = 1.1

%description -n geronimo-j2ee-management-1_1-api
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications Note: You should use the subpackages for the
Specifications that you actually need.	The ones installed by the main
package are deprecated and will disapear in future releases.

%package -n geronimo-jpa-3_0-api
Summary:        Geronimo J2EE server J2EE specifications
Group:          Development/Languages/Java
Requires(pre):  update-alternatives
Provides:       jpa_3_0_api = %{version}
Provides:       jpa_api = 3.0

%description -n geronimo-jpa-3_0-api
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications Note: You should use the subpackages for the
Specifications that you actually need.	The ones installed by the main
package are deprecated and will disapear in future releases.

%package -n geronimo-jsp-2_0-api
Summary:        Geronimo J2EE server J2EE specifications
Group:          Development/Languages/Java
Requires:       servlet_2_4_api
Requires(pre):  update-alternatives
Provides:       jsp = 2.0
# TODO: drop asap
Provides:       jsp_2_0_api = %{version}
Provides:       jsp_api = 2.0

%description -n geronimo-jsp-2_0-api
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications: JavaServer Pages Specification

%package -n geronimo-jsp-2_1-api
Summary:        Geronimo J2EE server J2EE specifications
Group:          Development/Languages/Java
Requires:       el_1_0_api
Requires:       servlet_2_5_api
Requires(pre):  update-alternatives
Provides:       jsp = 2.1
# TODO: drop asap
Provides:       jsp_2_1_api = %{version}
Provides:       jsp_api = 2.1

%description -n geronimo-jsp-2_1-api
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications Note: You should use the subpackages for the
Specifications that you actually need.	The ones installed by the main
package are deprecated and will disapear in future releases.

%package -n geronimo-jta-1_0_1B-api
Summary:        Geronimo J2EE server J2EE specifications
Requires(pre):  update-alternatives
Provides:       jta_1_0_1B_api = %{version}
Provides:       jta_api = 1.0.1B
Provides:       jta = 1.0.1B

%description -n geronimo-jta-1_0_1B-api
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications: Java Transaction API Specification

%package -n geronimo-jta-1_1-api
Summary:        Geronimo J2EE server J2EE specifications
Requires(pre):  update-alternatives
Provides:       jta_1_1_api = %{version}
Provides:       jta_api = 1.1
Provides:       jta = 1.1

%description -n geronimo-jta-1_1-api
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications Note: You should use the subpackages for the
Specifications that you actually need.	The ones installed by the main
package are deprecated and will disapear in future releases.

%package -n geronimo-qname-1_1-api
Summary:        Geronimo J2EE server J2EE specifications
Group:          Development/Languages/Java
Requires(pre):  update-alternatives
Provides:       qname_1_1_api = %{version}
Provides:       qname_api = 1.1

%description -n geronimo-qname-1_1-api
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications: javax.xml.namespace.QName API

%package -n geronimo-servlet-2_4-api
Summary:        Geronimo J2EE server J2EE specifications
Group:          Development/Languages/Java
Requires(pre):  update-alternatives
Provides:       servlet = 2.4
# TODO: drop asap
Provides:       servlet_2_4_api = %{version}
Provides:       servlet_api = 2.4

%description -n geronimo-servlet-2_4-api
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications: J2EE Servlet v2.4 API

%package -n geronimo-servlet-2_5-api
Summary:        Geronimo J2EE server J2EE specifications
Group:          Development/Languages/Java
Requires(pre):  update-alternatives
Provides:       servlet = 2.5
# TODO: drop asap
Provides:       servlet_2_5_api = %{version}
Provides:       servlet_api = 2.5

%description -n geronimo-servlet-2_5-api
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications Note: You should use the subpackages for the
Specifications that you actually need.	The ones installed by the main
package are deprecated and will disapear in future releases.

%package -n geronimo-stax-1_0-api
Summary:        Geronimo J2EE server J2EE specifications
Group:          Development/Languages/Java
Requires(pre):  update-alternatives
Provides:       stax_1_0_api = %{version}
Provides:       stax_api = 1.0

%description -n geronimo-stax-1_0-api
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications Note: You should use the subpackages for the
Specifications that you actually need.	The ones installed by the main
package are deprecated and will disapear in future releases.

%package -n geronimo-ws-metadata-2_0-api
Summary:        Geronimo J2EE server J2EE specifications
Group:          Development/Languages/Java
Requires(pre):  update-alternatives
Provides:       ws_metadata_2_0_api = %{version}
Provides:       ws_metadata_api = 2.0

%description -n geronimo-ws-metadata-2_0-api
Geronimo is Apache's ASF-licenced J2EE server project. These are the
J2EE-Specifications Note: You should use the subpackages for the
Specifications that you actually need.	The ones installed by the main
package are deprecated and will disapear in future releases.

%prep
%setup -q
chmod -R go=u-w *
mkdir etc
cp LICENSE.txt etc
mkdir external_repo
ln -s %{_javadir} external_repo/JPP
cp %{SOURCE1000} build.xml
for i in */pom.xml; do
  %pom_remove_parent ${i}
  %pom_xpath_inject "pom:project" "<groupId>org.apache.geronimo.specs</groupId>" ${i}
done
%pom_xpath_set pom:project/pom:version 1.1.1 geronimo-spec-j2ee

%build
ant -Dant.build.javac.source=8 -Dant.build.javac.target=8

%install
set +x
# Directory for poms
install -d -m 0755 %{buildroot}/%{_mavenpomdir}
# subpackage jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 0644 \
  geronimo-activation_1.0.2_spec-1.2/target/geronimo-activation_1.0.2_spec-1.2.jar \
  %{buildroot}%{_javadir}/geronimo-jaf-1.0.2-api.jar
install -m 0644 geronimo-activation_1.0.2_spec-1.2/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-jaf-1.0.2-api.pom
%add_maven_depmap JPP-geronimo-jaf-1.0.2-api.pom geronimo-jaf-1.0.2-api.jar -f jaf-1.0.2-api

install -m 0644 \
  geronimo-activation_1.1_spec-1.0/target/geronimo-activation_1.1_spec-1.0.jar \
  %{buildroot}%{_javadir}/geronimo-jaf-1.1-api.jar
install -m 0644 geronimo-activation_1.1_spec-1.0/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-jaf-1.1-api.pom
%add_maven_depmap JPP-geronimo-jaf-1.1-api.pom geronimo-jaf-1.1-api.jar -f jaf-1.1-api

install -m 0644 \
  geronimo-annotation_1.0_spec-1.1.0/target/geronimo-annotation_1.0_spec-1.1.jar \
  %{buildroot}%{_javadir}/geronimo-annotation-1.0-api.jar
install -m 0644 geronimo-annotation_1.0_spec-1.1.0/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-annotation-1.0-api.pom
%add_maven_depmap JPP-geronimo-annotation-1.0-api.pom geronimo-annotation-1.0-api.jar -a "javax.annotation:jsr250-api,org.eclipse.jetty.orbit:javax.annotation" -f annotation-1.0-api

install -m 0644 \
  geronimo-ejb_2.1_spec-1.1/target/geronimo-ejb_2.1_spec-1.1.jar \
  %{buildroot}%{_javadir}/geronimo-ejb-2.1-api.jar
install -m 0644 geronimo-ejb_2.1_spec-1.1/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-ejb-2.1-api.pom
%add_maven_depmap JPP-geronimo-ejb-2.1-api.pom geronimo-ejb-2.1-api.jar -f ejb-2.1-api

install -m 0644 \
  geronimo-ejb_3.0_spec-1.0/target/geronimo-ejb_3.0_spec-1.0.jar \
  %{buildroot}%{_javadir}/geronimo-ejb-3.0-api.jar
install -m 0644 geronimo-ejb_3.0_spec-1.0/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-ejb-3.0-api.pom
%add_maven_depmap JPP-geronimo-ejb-3.0-api.pom geronimo-ejb-3.0-api.jar -f ejb-3.0-api

install -m 0644 \
  geronimo-el_1.0_spec-1.0/target/geronimo-el_1.0_spec-1.0.jar \
  %{buildroot}%{_javadir}/geronimo-el-1.0-api.jar
install -m 0644 geronimo-el_1.0_spec-1.0/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-el-1.0-api.pom
%add_maven_depmap JPP-geronimo-el-1.0-api.pom geronimo-el-1.0-api.jar -f el-1.0-api

install -m 0644 \
  geronimo-interceptor_3.0_spec-1.0/target/geronimo-interceptor_3.0_spec-1.0.jar \
  %{buildroot}%{_javadir}/geronimo-interceptor-3.0-api.jar
install -m 0644 geronimo-interceptor_3.0_spec-1.0/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-interceptor-3.0-api.pom
%add_maven_depmap JPP-geronimo-interceptor-3.0-api.pom geronimo-interceptor-3.0-api.jar -f interceptor-3.0-api

install -m 0644 \
  geronimo-j2ee-connector_1.5_spec-1.1.1/target/geronimo-j2ee-connector_1.5_spec-1.1.1.jar \
  %{buildroot}%{_javadir}/geronimo-j2ee-connector-1.5-api.jar
install -m 0644 geronimo-j2ee-connector_1.5_spec-1.1.1/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-j2ee-connector-1.5-api.pom
%add_maven_depmap JPP-geronimo-j2ee-connector-1.5-api.pom geronimo-j2ee-connector-1.5-api.jar -f j2ee-connector-1.5-api

install -m 0644 \
  geronimo-j2ee-deployment_1.1_spec-1.1/target/geronimo-j2ee-deployment_1.1_spec-1.1.jar \
  %{buildroot}%{_javadir}/geronimo-j2ee-deployment-1.1-api.jar
install -m 0644 geronimo-j2ee-deployment_1.1_spec-1.1/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-j2ee-deployment-1.1-api.pom
%add_maven_depmap JPP-geronimo-j2ee-deployment-1.1-api.pom geronimo-j2ee-deployment-1.1-api.jar -f j2ee-deployment-1.1-api

install -m 0644 \
  geronimo-javaee-deployment_1.1MR3_spec-1.0/target/geronimo-javaee-deployment_1.1MR3_spec-1.0.jar \
  %{buildroot}%{_javadir}/geronimo-javaee-deployment-1.1-api.jar
install -m 0644 geronimo-javaee-deployment_1.1MR3_spec-1.0/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-javaee-deployment-1.1-api.pom
%add_maven_depmap JPP-geronimo-javaee-deployment-1.1-api.pom geronimo-javaee-deployment-1.1-api.jar -f javaee-deployment-1.1-api

install -m 0644 \
  geronimo-j2ee-jacc_1.0_spec-1.1/target/geronimo-j2ee-jacc_1.0_spec-1.1.jar \
  %{buildroot}%{_javadir}/geronimo-jacc-1.0-api.jar
install -m 0644 geronimo-j2ee-jacc_1.0_spec-1.1/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-jacc-1.0-api.pom
%add_maven_depmap JPP-geronimo-jacc-1.0-api.pom geronimo-jacc-1.0-api.jar -f jacc-1.0-api

install -m 0644 \
  geronimo-jacc_1.1_spec-1.0/target/geronimo-jacc_1.1_spec-1.0.jar \
  %{buildroot}%{_javadir}/geronimo-jacc-1.1-api.jar
install -m 0644 geronimo-jacc_1.1_spec-1.0/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-jacc-1.1-api.pom
%add_maven_depmap JPP-geronimo-jacc-1.1-api.pom geronimo-jacc-1.1-api.jar -f jacc-1.1-api

install -m 0644 \
  geronimo-j2ee-management_1.0_spec-1.1/target/geronimo-j2ee-management_1.0_spec-1.1.jar \
  %{buildroot}%{_javadir}/geronimo-j2ee-management-1.0-api.jar
install -m 0644 geronimo-j2ee-management_1.0_spec-1.1/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-j2ee-management-1.0-api.pom
%add_maven_depmap JPP-geronimo-j2ee-management-1.0-api.pom geronimo-j2ee-management-1.0-api.jar -f j2ee-management-1.0-api

install -m 0644 \
  geronimo-j2ee-management_1.1_spec-1.0/target/geronimo-j2ee-management_1.1_spec-1.0.jar \
  %{buildroot}%{_javadir}/geronimo-j2ee-management-1.1-api.jar
install -m 0644 geronimo-j2ee-management_1.1_spec-1.0/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-j2ee-management-1.1-api.pom
%add_maven_depmap JPP-geronimo-j2ee-management-1.1-api.pom geronimo-j2ee-management-1.1-api.jar -f j2ee-management-1.1-api

install -m 0644 \
  geronimo-spec-j2ee/target/geronimo-j2ee_1.4_spec-1.2-jar-with-dependencies.jar \
  %{buildroot}%{_javadir}/geronimo-j2ee-1.4-apis.jar
install -m 0644 geronimo-spec-j2ee/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-j2ee-1.4-apis.pom
%add_maven_depmap JPP-geronimo-j2ee-1.4-apis.pom geronimo-j2ee-1.4-apis.jar -f j2ee-1.4-apis

install -m 0644 \
  geronimo-jpa_3.0_spec-1.1.0/target/geronimo-jpa_3.0_spec-1.1.jar \
  %{buildroot}%{_javadir}/geronimo-jpa-3.0-api.jar
install -m 0644 geronimo-jpa_3.0_spec-1.1.0/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-jpa-3.0-api.pom
%add_maven_depmap JPP-geronimo-jpa-3.0-api.pom geronimo-jpa-3.0-api.jar -f jpa-3.0-api -a javax.persistence:persistence-api

install -m 0644 \
  geronimo-jsp_2.0_spec-1.1/target/geronimo-jsp_2.0_spec-1.1.jar \
  %{buildroot}%{_javadir}/geronimo-jsp-2.0-api.jar
install -m 0644 geronimo-jsp_2.0_spec-1.1/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-jsp-2.0-api.pom
%add_maven_depmap JPP-geronimo-jsp-2.0-api.pom geronimo-jsp-2.0-api.jar -f jsp-2.0-api

install -m 0644 \
  geronimo-jsp_2.1_spec-1.0/target/geronimo-jsp_2.1_spec-1.0.jar \
  %{buildroot}%{_javadir}/geronimo-jsp-2.1-api.jar
install -m 0644 geronimo-jsp_2.1_spec-1.0/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-jsp-2.1-api.pom
%add_maven_depmap JPP-geronimo-jsp-2.1-api.pom geronimo-jsp-2.1-api.jar -f jsp-2.1-api

install -m 0644 \
  geronimo-jta_1.0.1B_spec-1.1.1/target/geronimo-jta_1.0.1B_spec-1.1.1.jar \
  %{buildroot}%{_javadir}/geronimo-jta-1.0.1B-api.jar
install -m 0644 geronimo-jta_1.0.1B_spec-1.1.1/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-jta-1.0.1B-api.pom
%add_maven_depmap JPP-geronimo-jta-1.0.1B-api.pom geronimo-jta-1.0.1B-api.jar -f jta-1.0.1B-api

install -m 0644 \
  geronimo-jta_1.1_spec-1.1.0/target/geronimo-jta_1.1_spec-1.1.jar \
  %{buildroot}%{_javadir}/geronimo-jta-1.1-api.jar
install -m 0644 geronimo-jta_1.1_spec-1.1.0/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-jta-1.1-api.pom
%add_maven_depmap JPP-geronimo-jta-1.1-api.pom geronimo-jta-1.1-api.jar -f jta-1.1-api -a "javax.transaction:jta,org.eclipse.jetty.orbit:javax.transaction"

install -m 0644 \
  geronimo-qname_1.1_spec-1.1/target/geronimo-qname_1.1_spec-1.1.jar \
  %{buildroot}%{_javadir}/geronimo-qname-1.1-api.jar
install -m 0644 geronimo-qname_1.1_spec-1.1/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-qname-1.1-api.pom
%add_maven_depmap JPP-geronimo-qname-1.1-api.pom geronimo-qname-1.1-api.jar -f qname-1.1-api

install -m 0644 \
  geronimo-servlet_2.4_spec-1.1.1/target/geronimo-servlet_2.4_spec-1.1.1.jar \
  %{buildroot}%{_javadir}/geronimo-servlet-2.4-api.jar
install -m 0644 geronimo-servlet_2.4_spec-1.1.1/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-servlet-2.4-api.pom
%add_maven_depmap JPP-geronimo-servlet-2.4-api.pom geronimo-servlet-2.4-api.jar -f servlet-2.4-api

install -m 0644 \
  geronimo-servlet_2.5_spec-1.1/target/geronimo-servlet_2.5_spec-1.1.jar \
  %{buildroot}%{_javadir}/geronimo-servlet-2.5-api.jar
install -m 0644 geronimo-servlet_2.5_spec-1.1/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-servlet-2.5-api.pom
%add_maven_depmap JPP-geronimo-servlet-2.5-api.pom geronimo-servlet-2.5-api.jar -f servlet-2.5-api

install -m 0644 \
  geronimo-stax-api_1.0_spec-1.0/target/geronimo-stax-api_1.0_spec-1.0.jar \
  %{buildroot}%{_javadir}/geronimo-stax-1.0-api.jar
install -m 0644 geronimo-stax-api_1.0_spec-1.0/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-stax-1.0-api.pom
%add_maven_depmap JPP-geronimo-stax-1.0-api.pom geronimo-stax-1.0-api.jar -f stax-1.0-api

install -m 0644 \
  geronimo-ws-metadata_2.0_spec-1.1.1/target/geronimo-ws-metadata_2.0_spec-1.1.1.jar \
  %{buildroot}%{_javadir}/geronimo-ws-metadata-2.0-api.jar
install -m 0644 geronimo-ws-metadata_2.0_spec-1.1.1/pom.xml \
  %{buildroot}/%{_mavenpomdir}/JPP-geronimo-ws-metadata-2.0-api.pom
%add_maven_depmap JPP-geronimo-ws-metadata-2.0-api.pom geronimo-ws-metadata-2.0-api.jar -f ws-metadata-2.0-api

%files -n geronimo-jaf-1_0_2-api -f .mfiles-jaf-1.0.2-api
%license geronimo-activation_1.0.2_spec-1.2/LICENSE.txt

%files -n geronimo-jaf-1_1-api -f .mfiles-jaf-1.1-api
%license geronimo-activation_1.1_spec-1.0/LICENSE.txt

%files -n geronimo-annotation-1_0-api -f .mfiles-annotation-1.0-api
%license geronimo-annotation_1.0_spec-1.1.0/LICENSE.txt

%files -n geronimo-ejb-2_1-api -f .mfiles-ejb-2.1-api
%license geronimo-ejb_2.1_spec-1.1/LICENSE.txt

%files -n geronimo-ejb-3_0-api -f .mfiles-ejb-3.0-api
%license geronimo-ejb_3.0_spec-1.0/LICENSE.txt

%files -n geronimo-el-1_0-api -f .mfiles-el-1.0-api
%license geronimo-el_1.0_spec-1.0/LICENSE.txt

%files -n geronimo-interceptor-3_0-api -f .mfiles-interceptor-3.0-api
%license geronimo-interceptor_3.0_spec-1.0/LICENSE.txt

%files -n geronimo-j2ee-1_4-apis -f .mfiles-j2ee-1.4-apis
%license geronimo-spec-j2ee/LICENSE.txt

%files -n geronimo-j2ee-connector-1_5-api -f .mfiles-j2ee-connector-1.5-api
%license geronimo-j2ee-connector_1.5_spec-1.1.1/LICENSE.txt

%files -n geronimo-j2ee-deployment-1_1-api -f .mfiles-j2ee-deployment-1.1-api
%license geronimo-j2ee-deployment_1.1_spec-1.1/LICENSE.txt

%files -n geronimo-javaee-deployment-1_1-api -f .mfiles-javaee-deployment-1.1-api
%license geronimo-javaee-deployment_1.1MR3_spec-1.0/LICENSE.txt

%files -n geronimo-jacc-1_0-api -f .mfiles-jacc-1.0-api
%license geronimo-j2ee-jacc_1.0_spec-1.1/LICENSE.txt

%files -n geronimo-jacc-1_1-api -f .mfiles-jacc-1.1-api
%license geronimo-jacc_1.1_spec-1.0/LICENSE.txt

%files -n geronimo-j2ee-management-1_0-api -f .mfiles-j2ee-management-1.0-api
%license geronimo-j2ee-management_1.0_spec-1.1/LICENSE.txt

%files -n geronimo-j2ee-management-1_1-api -f .mfiles-j2ee-management-1.1-api
%license geronimo-j2ee-management_1.1_spec-1.0/LICENSE.txt

%files -n geronimo-jpa-3_0-api -f .mfiles-jpa-3.0-api
%license geronimo-jpa_3.0_spec-1.1.0/LICENSE.txt

%files -n geronimo-jsp-2_0-api -f .mfiles-jsp-2.0-api
%license geronimo-jsp_2.0_spec-1.1/LICENSE.txt

%files -n geronimo-jsp-2_1-api -f .mfiles-jsp-2.1-api
%license geronimo-jsp_2.1_spec-1.0/LICENSE.txt

%files -n geronimo-jta-1_0_1B-api -f .mfiles-jta-1.0.1B-api
%license geronimo-jta_1.0.1B_spec-1.1.1/LICENSE.txt

%files -n geronimo-jta-1_1-api -f .mfiles-jta-1.1-api
%license geronimo-jta_1.1_spec-1.1.0/LICENSE.txt

%files -n geronimo-qname-1_1-api -f .mfiles-qname-1.1-api
%license geronimo-qname_1.1_spec-1.1/LICENSE.txt

%files -n geronimo-servlet-2_4-api -f .mfiles-servlet-2.4-api
%license geronimo-servlet_2.4_spec-1.1.1/LICENSE.txt

%files -n geronimo-servlet-2_5-api -f .mfiles-servlet-2.5-api
%license geronimo-servlet_2.5_spec-1.1/LICENSE.txt

%files -n geronimo-stax-1_0-api -f .mfiles-stax-1.0-api
%license geronimo-stax-api_1.0_spec-1.0/LICENSE.txt

%files -n geronimo-ws-metadata-2_0-api -f .mfiles-ws-metadata-2.0-api
%license geronimo-ws-metadata_2.0_spec-1.1.1/LICENSE.txt

%changelog
* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2-40
- Updating naming for 3.0 version of Azure Linux.

* Wed Apr 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2-39
- Updating source URL.

* Wed Feb 23 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2-38
- Removing following components due to incompatibility with Java 11:
  - commonj;
  - corba;
  - javamail;
  - jaxr;
  - jaxrpc;
  - jms;
  - saaj;
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2-37
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.2-36.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Remove %%pre scriptlets that attempt to remove alternatives that have not been installed.

* Mon Jan 27 2020 Fridrich Strba <fstrba@suse.com>
- On supported platforms, avoid building with OpenJ9, in order to
  prevent build cycles.
* Tue Dec 10 2019 Fridrich Strba <fstrba@suse.com>
- Set version for the specs comming from tag 1_1_1 in order to
  avoid unexpanded version macros in pom files.
* Mon Apr 15 2019 Fridrich Strba <fstrba@suse.com>
- Removed patches:
  * geronimo-specs-1.2-pom_xml.patch
  * geronimo-specs-corba-2.3-pom_xml.patch
  * geronimo-specs-j2ee-1.4-pom_xml.patch
  * geronimo-specs-j2ee-connector-1.5-pom_xml.patch
  * geronimo-specs-jta-1.0.1B-pom_xml.patch
  * geronimo-specs-servlet-2.4-pom_xml.patch
    + Not needed since we are not building with maven and some
    of the modifications are possible using the
    javapackages-local macros.
- Remove all reference to parent pom, since we are not building
  with maven, and don't package the parent pom in this build.
- Stop using alternatives to handle different versions of provides.
- Avoid multiplication of jar symlinks
* Fri Apr 12 2019 Julio Gonzalez Gil <jgonzalez@suse.com>
- Obsoletes, conflicts and provides must use only %%%%{version} as the
  the release is managed automatically by OBS and not needed  (bsc#1132514)
* Tue Mar 19 2019 Fridrich Strba <fstrba@suse.com>
- Let each package obsolete and conflict with the
  %%%%{name}-poms < %%%%{version}-%%%%{release} in order to make upgrades
  smooth
* Thu Dec 13 2018 Fridrich Strba <fstrba@suse.com>
- Add alias javax.jms:jms to geronimo-jms-1_1-api
* Wed Nov 21 2018 Fridrich Strba <fstrba@suse.com>
- Add aliases org.eclipse.jetty.orbit:javax.transaction and
  javax.transaction:jta to geronimo-jta-1_1-api
* Mon Nov 12 2018 Fridrich Strba <fstrba@suse.com>
- Add alias javax.persistence:persistence-api to
  geronimo-jpa-3.0-api subpackage
* Mon Nov 12 2018 Fridrich Strba <fstrba@suse.com>
- Package the pom files together with their corresponding jars,
  since packaging poms separately makes no sense at all
- Rename geronimo-specs-poms package to geronimo-specs-pom, since
  it now contains only the parent pom.
* Fri Nov  9 2018 Fridrich Strba <fstrba@suse.com>
- Add two aliases to the maven artifact in
  geronimo-annotation-1_0-api sub-package
* Mon Jul 16 2018 fstrba@suse.com
- BuildConflict with java-devel >= 11, since the build uses tools
  and APIs removed in jdk11
* Thu May 17 2018 fstrba@suse.com
- Build with source and target 8 to prepare for a possible removal
  of 1.6 compatibility
* Fri Sep  8 2017 fstrba@suse.com
- Specify java source and target version to 1.6 in order to allow
  build with jdk9
- Modified source:
  * geronimo-specs.build.xml
  - specify encoding UTF-8, since the files use UTF-8 characters
* Fri May 19 2017 tchvatal@suse.com
- Remove javadoc to cut build time in half
* Fri May 19 2017 tchvatal@suse.com
- Fix building with new javapackages-tools
- Remove unused conditionals
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Tue Jul 29 2014 tchvatal@suse.com
- Do not mess with defattr as it is pointless.
* Fri Jul 25 2014 tchvatal@suse.com
- Try to use the update-alternatives properly.
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Tue Sep  3 2013 mvyskocil@suse.com
- use add_maven_depmap from javapackages-tools
* Mon Dec 17 2012 mvyskocil@suse.com
- drop useless excalibur-avalon from build requires
* Mon Sep 19 2011 mvyskocil@suse.cz
- fix a typo in alternatives --install call causing a build failure
* Wed May  6 2009 mvyskocil@suse.cz
- Update to 1.2
  * bugfix release and update release
  * JPA support.
  * CA - Certificate Authority capabilities, you can now issue certificates in
    reply to CSRs. See https://cwiki.apache.org/GMOxDOC12/certification-authority.html
- synchronized specfile with jpackage 5.0
  * mavenized
  * obsoleted geronimo-specs-j2ee-management-pom.patch,
    geronimo-specs-pom_xml.patch, geronimo-spec-javamail-sun-security.patch
  * do not use triggers
  * use alternatives system
- used one build.xml for all packages ==> shorter %%%%build section
- fdupes used on javadoc
- new packages
  * geronimo-ws-metadata
  * geronimo-stax-1_0-api
  * geronimo-servlet-2_5
  * geronimo-jta-1_1-api
  * geronimo-jsp-2_1-api
  * geronimo-jpa-3_0-api
  * geronimo-javamail-1_4-api
  * geronimo-j2ee-management-1_1
  * geronimo-jacc-1_1-api
  * geronimo-javaee-deployment
  * geronimo-interceptor-3_0-api
  * geronimo-el-1_0-api
  * geronimo-ejb-3_0-api
  * geronimo-annotation-1_0-api
  * geronimo-jaf-1_1-api
  * geronimo-specs-javadoc
- undot.py to remove dots from package names
- remove %%%%{release} from Requires
* Mon Dec  1 2008 mvyskocil@suse.cz
- added a Conflicts to gnu-jaf to geronimo-jav-1_0_2-api
* Tue Aug 26 2008 anosek@suse.cz
- fixed path to LICENSE.txt files in spec
* Mon Aug 25 2008 mvyskocil@suse.cz
- target=1.5 source=1.5
- removed a gcj support
- fixed some rpmlint warnings
* Mon Apr 21 2008 ro@suse.de
- changed requires of main package to use underscores as well
* Thu Apr 17 2008 mvyskocil@suse.cz
- Dots in names was replaced by underscore
- Added a PreReq on coreutils
- Removed of BuildRoot removal in %%install phase
* Mon Apr  7 2008 mvyskocil@suse.cz
- First release in Suse (JPP 1.7) version 1.1
  - build dependency for log4j update [bnc#355798]
  - added a build support using ant
  - FIXME: the corba-3.0 package is not currently included
