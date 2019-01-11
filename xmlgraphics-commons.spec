%{?_javapackages_macros:%_javapackages_macros}

Name:           xmlgraphics-commons
Version:        2.2
Release:        1
Epoch:          0
Summary:        XML Graphics Commons
Group:          Development/Java
License:        ASL 2.0
URL:            http://xmlgraphics.apache.org/
Source0:        http://archive.apache.org/dist/xmlgraphics/commons/source/xmlgraphics-commons-2.2-src.tar.gz

BuildArch:      noarch
BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  javapackages-local
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-junit >= 0:1.6
BuildRequires:  junit
BuildRequires:  apache-commons-io >= 1.3.1
BuildRequires:  apache-commons-logging >= 1.0.4
Requires:       java
Requires:       apache-commons-io >= 1.3.1
Requires:       apache-commons-logging >= 1.0.4

%description
Apache XML Graphics Commons is a library that consists of
several reusable components used by Apache Batik and
Apache FOP. Many of these components can easily be used
separately outside the domains of SVG and XSL-FO. You will
find components such as a PDF library, an RTF library,
Graphics2D implementations that let you generate PDF &
PostScript files, and much more.

%package        javadoc
Summary:        Javadoc for %{name}

%description    javadoc
%{summary}.


%prep
%setup -q %{name}-%{version}
rm -f `find . -name "*.jar"`

# create pom from template
sed "s:@version@:%{version}:g" %{name}-pom-template.pom \
    > %{name}.pom


%build
export CLASSPATH=$(build-classpath commons-logging)
export OPT_JAR_LIST="ant/ant-junit junit"
pushd lib
ln -sf $(build-classpath commons-io) .
popd
ant package javadocs

%install
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -Dpm 0644 build/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
install -pm 644 %{name}.pom %{buildroot}/%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap

install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr build/javadocs/* %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%doc LICENSE NOTICE README

%files javadoc
%doc LICENSE NOTICE
%doc %{_javadocdir}/%{name}
