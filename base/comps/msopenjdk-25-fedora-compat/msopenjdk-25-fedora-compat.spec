Name:           msopenjdk-25-fedora-compat
Version:        25.0.4.1
Release:        %autorelease
Summary:        Fedora compatibility aliases for Microsoft Build of OpenJDK 25
License:        MIT
URL:            https://aka.ms/openjdk
ExclusiveArch:  x86_64 aarch64

%global jvmdir %{_prefix}/lib/jvm

Obsoletes:      java-25-openjdk
Obsoletes:      java-25-openjdk-headless
Obsoletes:      java-25-openjdk-devel
Conflicts:      java-25-openjdk%{?_isa}
Conflicts:      java-25-openjdk-headless%{?_isa}
Conflicts:      java-25-openjdk-devel%{?_isa}

Provides:       java-25-openjdk = 1:%{version}-%{release}
Provides:       java-25 = 1:%{version}-%{release}
Provides:       java-openjdk = 1:%{version}-%{release}
Provides:       java = 1:%{version}-%{release}
Provides:       jre-25-openjdk = 1:%{version}-%{release}
Provides:       jre-25 = 1:%{version}-%{release}
Provides:       jre-openjdk = 1:%{version}-%{release}
Provides:       jre = 1:%{version}-%{release}
Provides:       java-25-openjdk-headless = 1:%{version}-%{release}
Provides:       java-25-headless = 1:%{version}-%{release}
Provides:       java-openjdk-headless = 1:%{version}-%{release}
Provides:       java-headless = 1:%{version}-%{release}
Provides:       jre-25-openjdk-headless = 1:%{version}-%{release}
Provides:       jre-25-headless = 1:%{version}-%{release}
Provides:       jre-openjdk-headless = 1:%{version}-%{release}
Provides:       jre-headless = 1:%{version}-%{release}
Provides:       libjawt.so()(64bit)
Provides:       java-sdk-25-openjdk = 1:%{version}-%{release}
Provides:       java-sdk-25 = 1:%{version}-%{release}
Provides:       java-25-devel = 1:%{version}-%{release}
Provides:       java-25-openjdk-devel = 1:%{version}-%{release}
Provides:       java-devel-openjdk = 1:%{version}-%{release}
Provides:       java-sdk-openjdk = 1:%{version}-%{release}
Provides:       java-devel = 1:%{version}-%{release}
Provides:       java-sdk = 1:%{version}-%{release}

Requires:       msopenjdk-25%{?_isa} = 25.0.4.1-1
Requires:       javapackages-filesystem
# classloader-leak-test-framework fails its Swing test when Microsoft Build of
# OpenJDK cannot load libfreetype.so.6 or initialize the system font configuration.
Requires:       freetype
Requires:       fontconfig
Requires:       xorg-x11-fonts-Type1
Requires:       libX11
Requires:       libXcomposite
Requires:       libXext
Requires:       libXi
Requires:       libXrender
Requires:       libXtst
Requires(posttrans): /usr/sbin/alternatives
Requires(posttrans): /usr/bin/find
Requires(preun): /usr/sbin/alternatives

%description
Compatibility package that exposes Microsoft Build of OpenJDK 25 through
Fedora-compatible Java capabilities and JVM directory alternatives. It contains
no Java runtime files.

%install
mkdir -p %{buildroot}%{_datadir}/doc/%{name}
printf '%s\n' 'Fedora compatibility aliases for msopenjdk-25.' > %{buildroot}%{_datadir}/doc/%{name}/README
mkdir -p %{buildroot}%{_libdir}
ln -s %{jvmdir}/msopenjdk-25/lib/libjawt.so %{buildroot}%{_libdir}/libjawt.so

%posttrans
# Fedora OpenJDK removal can leave empty directories that block the alternatives symlink.
find %{jvmdir}/java-25-openjdk -depth -type d -empty -delete 2>/dev/null || :
alternatives --add-follower java %{jvmdir}/msopenjdk-25/bin/java %{jvmdir}/jre jre %{jvmdir}/msopenjdk-25
alternatives --add-follower javac %{jvmdir}/msopenjdk-25/bin/javac %{jvmdir}/java java_sdk %{jvmdir}/msopenjdk-25
alternatives --install %{jvmdir}/java-25-openjdk java_sdk_25_openjdk %{jvmdir}/msopenjdk-25 2511
alternatives --install %{jvmdir}/java-25 java_sdk_25 %{jvmdir}/msopenjdk-25 2511
alternatives --install %{jvmdir}/java-openjdk java_sdk_openjdk %{jvmdir}/msopenjdk-25 2511
alternatives --install %{jvmdir}/jre-25-openjdk jre_25_openjdk %{jvmdir}/msopenjdk-25 2511
alternatives --install %{jvmdir}/jre-25 jre_25 %{jvmdir}/msopenjdk-25 2511
alternatives --install %{jvmdir}/jre-openjdk jre_openjdk %{jvmdir}/msopenjdk-25 2511
exit 0

%preun
if [ $1 -eq 0 ]; then
    alternatives --remove-follower java %{jvmdir}/msopenjdk-25/bin/java jre
    alternatives --remove-follower javac %{jvmdir}/msopenjdk-25/bin/javac java_sdk
    alternatives --remove java_sdk_25_openjdk %{jvmdir}/msopenjdk-25
    alternatives --remove java_sdk_25 %{jvmdir}/msopenjdk-25
    alternatives --remove java_sdk_openjdk %{jvmdir}/msopenjdk-25
    alternatives --remove jre_25_openjdk %{jvmdir}/msopenjdk-25
    alternatives --remove jre_25 %{jvmdir}/msopenjdk-25
    alternatives --remove jre_openjdk %{jvmdir}/msopenjdk-25
fi
exit 0

%files
%ghost %{jvmdir}/java
%ghost %{jvmdir}/java-25-openjdk
%ghost %{jvmdir}/java-25
%ghost %{jvmdir}/java-openjdk
%ghost %{jvmdir}/jre
%ghost %{jvmdir}/jre-25-openjdk
%ghost %{jvmdir}/jre-25
%ghost %{jvmdir}/jre-openjdk
%{_libdir}/libjawt.so
%{_datadir}/doc/%{name}/README

%changelog
%autochangelog
