Name:		xmlgraphics-commons
Version:	2.12
Release:	1
Epoch:		0
Summary:	Shared image and graphics library for Batik and FOP
Group:		Development/Java
License:	ASL 2.0
URL:		https://xmlgraphics.apache.org/
Source0:	https://archive.apache.org/dist/xmlgraphics/commons/source/xmlgraphics-commons-2.12-src.tar.gz#/xmlgraphics-commons-%{version}-src.tar.gz

BuildArch:	noarch
BuildRequires:	python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildRequires:	mvn(commons-logging:commons-logging)
BuildSystem:	maven
BuildOption(install):	--file-name xmlgraphics-commons

Obsoletes:	%{name}-javadoc < %{version}-%{release}

%description
Apache XML Graphics Commons is the shared image, font, and PostScript
code used by Batik and FOP. 2.12 keeps the compiler source level at 1.8
and links the system commons-logging jar. The upstream archive also
ships a copy of that jar under lib/; this package deletes it.
Tests are skipped.

%prep
%autosetup -n xmlgraphics-commons-%{version}
rm -rf lib src/test src/tools src/documentation
python - <<'PY'
import shutil
from pathlib import Path

src = Path("src/main/java")
java_files = list(src.rglob("*.java"))
if len(java_files) != 318:
    raise SystemExit("java files " + str(len(java_files)))
if list(Path(".").rglob("*.jar")):
    raise SystemExit("prebuilt jar remains")
meta = Path("src/main/resources/META-INF")
meta.mkdir(parents=True, exist_ok=True)
for name in ("LICENSE", "NOTICE"):
    shutil.copy(name, meta / name)
services = list(meta.glob("services/*"))
if len(services) < 4:
    raise SystemExit("service registrations " + str(len(services)))

Path("pom.xml").write_text("""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.apache.xmlgraphics</groupId>
  <artifactId>xmlgraphics-commons</artifactId>
  <version>%{version}</version>
  <packaging>jar</packaging>
  <name>Apache XML Graphics Commons</name>
  <description>Shared image and graphics code for Batik and FOP.</description>
  <url>https://xmlgraphics.apache.org/</url>
  <licenses>
    <license>
      <name>Apache License, Version 2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0.txt</url>
    </license>
  </licenses>
  <dependencies>
    <dependency>
      <groupId>commons-logging</groupId>
      <artifactId>commons-logging</artifactId>
      <version>1.4.0</version>
    </dependency>
  </dependencies>
  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.source>1.8</maven.compiler.source>
    <maven.compiler.target>1.8</maven.compiler.target>
  </properties>
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.12.1</version>
        <configuration>
          <source>1.8</source>
          <target>1.8</target>
        </configuration>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-jar-plugin</artifactId>
        <version>3.3.0</version>
        <configuration>
          <archive>
            <manifestEntries>
              <Automatic-Module-Name>org.apache.xmlgraphics.commons</Automatic-Module-Name>
            </manifestEntries>
          </archive>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
""", encoding="utf-8")
pom = Path("pom.xml").read_text(encoding="utf-8")
for needle in (
    "<artifactId>xmlgraphics-commons</artifactId>",
    "<artifactId>commons-logging</artifactId>",
    "<version>1.4.0</version>",
    "<version>%{version}</version>",
    "<source>1.8</source>",
    "<target>1.8</target>",
    "<Automatic-Module-Name>org.apache.xmlgraphics.commons</Automatic-Module-Name>",
):
    if needle not in pom:
        raise SystemExit("pom missing " + needle)
for needle in ("junit", "mockito", "spotbugs", "checkstyle", "commons-io", "SNAPSHOT", "<release>"):
    if needle in pom:
        raise SystemExit("pom still contains " + needle)
PY

%build -a
cat > manifest-addition <<'EOF'
Automatic-Module-Name: org.apache.xmlgraphics.commons
EOF
jar ufm target/xmlgraphics-commons-%{version}.jar manifest-addition
java --module-path target/xmlgraphics-commons-%{version}.jar --describe-module org.apache.xmlgraphics.commons > module-describe.txt
# A versioned jar prints "name@version ... automatic", not "name automatic".
grep -q '^org.apache.xmlgraphics.commons' module-describe.txt || { cat module-describe.txt; exit 1; }
grep -q ' automatic$' module-describe.txt || { cat module-describe.txt; exit 1; }

%files -f .mfiles
%doc LICENSE NOTICE README
