Name:           perl-Nmap-Scanner
Version:        1.0
Release:        1%{?dist}
Summary:        Perform and manipulate nmap scans using perl
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Nmap-Scanner/
Source0:        http://www.cpan.org/modules/by-module/Nmap/Nmap-Scanner-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(Class::Generate)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(XML::SAX)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       nmap >= 3.21

%description
This set of modules provides perl class wrappers for the network mapper
(nmap) scanning tool (see http://www.insecure.org/nmap/). Using these
modules, a developer, network administrator, or other techie can create
perl routines or classes which can be used to automate and integrate nmap
scans elegantly into new and existing perl scripts.

%prep
%setup -q -n Nmap-Scanner-%{version}

# filtering requires
cat << \EOF > %{_builddir}/Nmap-Scanner-%{version}/%{name}-req
#!/bin/sh
%{__perl_requires} $* |\
sed -e '/perl(Nmap/d'
EOF
%define __perl_requires %{_builddir}/Nmap-Scanner-%{version}/%{name}-req
chmod 755 %{__perl_requires}

# filtering provides
cat << \EOF > %{_builddir}/Nmap-Scanner-%{version}/%{name}-prov
#!/bin/sh
%{__perl_provides} $* |\
sed -e '/perl(Nmap::Scanner::/d' | sed -e '/perl(NmapHandler/d'
EOF
%define __perl_provides %{_builddir}/Nmap-Scanner-%{version}/%{name}-prov
chmod 755 %{__perl_provides}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
%{?!_with_network_tests: rm t/* }
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README run-examples.sh todo
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Jan 28 2010 Pedro Padron <pedro.padron@locaweb.com.br> 1.0-1
- First build.
