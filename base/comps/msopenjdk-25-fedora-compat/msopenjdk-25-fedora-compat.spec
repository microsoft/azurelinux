Name:           msopenjdk-25-fedora-compat
Version:        25.0.4.1
Release:        %autorelease
Summary:        Fedora compatibility aliases for Microsoft Build of OpenJDK 25
License:        MIT
URL:            https://aka.ms/openjdk
BuildArch:      noarch

%global jvmdir %{_prefix}/lib/jvm

Provides:       java-25-openjdk-headless = %{version}-%{release}
Provides:       java-25-headless = %{version}-%{release}
Provides:       java-openjdk-headless = %{version}-%{release}
Provides:       java-headless = %{version}-%{release}
Provides:       jre-25-openjdk-headless = %{version}-%{release}
Provides:       jre-25-headless = %{version}-%{release}
Provides:       jre-openjdk-headless = %{version}-%{release}
Provides:       jre-headless = %{version}-%{release}
Provides:       libjawt.so()(64bit)
Provides:       java-sdk-25-openjdk = %{version}-%{release}
Provides:       java-sdk-25 = %{version}-%{release}
Provides:       java-25-devel = %{version}-%{release}
Provides:       java-25-openjdk-devel = %{version}-%{release}
Provides:       java-devel-openjdk = %{version}-%{release}
Provides:       java-sdk-openjdk = %{version}-%{release}
Provides:       java-devel = %{version}-%{release}
Provides:       java-sdk = %{version}-%{release}

Requires:       msopenjdk-25 = 25.0.4.1-1
Requires(post): /usr/sbin/alternatives
Requires(preun): /usr/sbin/alternatives

%description
Compatibility package that exposes Microsoft Build of OpenJDK 25 through
Fedora-compatible Java capabilities and JVM directory alternatives. It contains
no Java runtime files.

%install
mkdir -p %{buildroot}%{_datadir}/doc/%{name}
printf '%s\n' 'Fedora compatibility aliases for msopenjdk-25.' > %{buildroot}%{_datadir}/doc/%{name}/README

%post
alternatives --install %{jvmdir}/java-25-openjdk java_sdk_25_openjdk %{jvmdir}/msopenjdk-25 2511
alternatives --install %{jvmdir}/java-25 java_sdk_25 %{jvmdir}/msopenjdk-25 2511
alternatives --install %{jvmdir}/java-openjdk java_sdk_openjdk %{jvmdir}/msopenjdk-25 2511
alternatives --install %{jvmdir}/jre-25-openjdk jre_25_openjdk %{jvmdir}/msopenjdk-25 2511
alternatives --install %{jvmdir}/jre-25 jre_25 %{jvmdir}/msopenjdk-25 2511
alternatives --install %{jvmdir}/jre-openjdk jre_openjdk %{jvmdir}/msopenjdk-25 2511

%preun
if [ $1 -eq 0 ]; then
    alternatives --remove java_sdk_25_openjdk %{jvmdir}/msopenjdk-25
    alternatives --remove java_sdk_25 %{jvmdir}/msopenjdk-25
    alternatives --remove java_sdk_openjdk %{jvmdir}/msopenjdk-25
    alternatives --remove jre_25_openjdk %{jvmdir}/msopenjdk-25
    alternatives --remove jre_25 %{jvmdir}/msopenjdk-25
    alternatives --remove jre_openjdk %{jvmdir}/msopenjdk-25
fi

%files
%ghost %{jvmdir}/java-25-openjdk
%ghost %{jvmdir}/java-25
%ghost %{jvmdir}/java-openjdk
%ghost %{jvmdir}/jre-25-openjdk
%ghost %{jvmdir}/jre-25
%ghost %{jvmdir}/jre-openjdk
%{_datadir}/doc/%{name}/README

%changelog
%autochangelog