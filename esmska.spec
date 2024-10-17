Name:           esmska
Version:        0.20.0
Release:        %mkrel 1
Summary:        Sending SMS over the Internet
Group:          Networking/Other
License:        GPLv3
URL:            https://code.google.com/p/esmska/

Source:         %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
Requires:       jre >= 1.6.0
BuildRequires:  java-devel >= 1.6.0
BuildRequires:  ant >= 1.7.1
BuildRequires:  ant-junit
BuildRequires:	ant-nodeps
BuildRequires:	desktop-file-utils

%description
Program for sending SMS over the Internet.
 * Send SMS to various operators international
 * Free, under free/open-source licence GNU AGPL 
 * Import contacts from other programs (DreamCom) and formats (vCard) 
 * Send SMS to multiple recipients at once 
 * History of sent messages 
 * Pluggable operator system - easy to provide support for more operators directly by users 
 * Extensive possibilities of changing appearance 

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Libraries/Java

%description javadoc
This package contains a javadoc for %{name}.

%prep
%setup -q

 sed -i -e 's/^#\s*checkUpdatePolicy\s*=\s*all.*/checkUpdatePolicy = gateways/' %{name}/include/%{name}.conf

%build
cd %{name}
# some files names needs UTF-8
LC_ALL="en_US.UTF-8" ant

%install
cd %{name}/dist
install -d -m 755 $RPM_BUILD_ROOT/%{_datadir}/%{name}
install -m 0644 %{name}.jar $RPM_BUILD_ROOT/%{_datadir}/%{name}/
install -m 0755 %{name}.sh $RPM_BUILD_ROOT/%{_datadir}/%{name}/
# jars
install -d -m 0755 $RPM_BUILD_ROOT/%{_datadir}/%{name}/lib
install -m 0644 lib/* $RPM_BUILD_ROOT/%{_datadir}/%{name}/lib
# other files
cp -r gateways $RPM_BUILD_ROOT/%{_datadir}/%{name}
# javadoc
install -d -m 755 $RPM_BUILD_ROOT/%{_javadocdir}/%{name}
cp -pr javadoc/* $RPM_BUILD_ROOT/%{_javadocdir}/%{name}
# esmska bin
install -d -m 0755 $RPM_BUILD_ROOT/%{_bindir}/
ln -sf ../../%{_datadir}/%{name}/%{name}.sh $RPM_BUILD_ROOT/%{_bindir}/%{name}
# icon
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/pixmaps
install -m 644 icons/%{name}.png $RPM_BUILD_ROOT%{_datadir}/pixmaps
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/applications
# esmska.conf
install -d -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install -m 0644 %{name}.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
ln -sf %{_sysconfdir}/%{name}/%{name}.conf $RPM_BUILD_ROOT/%{_datadir}/%{name}/%{name}.conf

desktop-file-install                 \
        --add-category Application                       \
        --dir $RPM_BUILD_ROOT%{_datadir}/applications    \
        ../resources/%{name}.desktop


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0755,root,root,0755)
%{_bindir}/%{name}
%defattr(-,root,root,0755)
%doc %{name}/dist/license/license.txt %{name}/dist/license/gnu-agpl.txt %{name}/dist/readme.txt
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_datadir}/%{name}
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop

%files javadoc
%defattr(-,root,root)
%{_javadocdir}/%{name}

