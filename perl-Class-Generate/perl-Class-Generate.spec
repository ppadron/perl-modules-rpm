Name:           perl-Class-Generate
Version:        1.10
Release:        1%{?dist}
Summary:        Generate Perl class hierarchies
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Class-Generate/
Source0:        http://www.cpan.org/authors/id/S/SW/SWARTIK/Class-Generate-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
The Class::Generate package exports functions that take as arguments a
class specification and create from these specifications a Perl 5 class.
The specification language allows many object-oriented constructs: typed
members, inheritance, private members, required members, default values,
object methods, class methods, class variables, and more.

%prep
%setup -q -n Class-Generate-%{version}

# filtering provides
cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} $* |\
sed -e '/perl(Class::Generate::/d'
EOF
%define __perl_provides %{_builddir}/Class-Generate-%{version}/%{name}-prov
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
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Jan 28 2010 Pedro Padron <ppadron@php.net> 1.10-1
- First build.
