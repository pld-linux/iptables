Summary:	extensible packet filtering system && extensible NAT system
Summary(pl):	system filtrowania pakietów oraz system translacji adresów (NAT)
Name:		iptables
Version:	1.0.0alpha
Release:	1
Copyright:	GPL
Group:		Networking/Daemons
URL:		http://netfilter.kernelnotes.org/
Source0:	http://netfilter.kernelnotes.org/0.90/%{name}-%{version}.tar.bz2
Source1:	rc.firewall
#Requires:	kernel >= 2.3.99pre2
BuildRequires:	grep
BuildRequires:	textutils
BuildRequires:	/usr/bin/dvips
BuildRoot:	/tmp/%{name}-%{version}-root

%define		_sysconfdir	/etc

%description
An extensible NAT system, and an extensible packet filtering system (iptables).

%description -l pl
Wydajny system translacji adresów (NAT) oraz system filtrowania pakietów.

%prep
%setup -q

%build
make depend 2> /dev/null || :
make COPT_FLAGS="$RPM_OPT_FLAGS" LIBDIR="%{_libdir}" 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc{0,1,2,3,4,5,6}.d

make install DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_libdir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/
ln -s ../rc.firewall $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc0.d/K91firewall
ln -s ../rc.firewall $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc1.d/K91firewall
ln -s ../rc.firewall $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc2.d/S09firewall
ln -s ../rc.firewall $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc3.d/S09firewall
ln -s ../rc.firewall $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc4.d/S09firewall
ln -s ../rc.firewall $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc5.d/S09firewall
ln -s ../rc.firewall $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc6.d/K91firewall

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/*

strip --strip-unneeded $RPM_BUILD_ROOT{%{_libdir}/*/*.so,%{_sbindir}/*} || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(754,root,root) %config(noreplace) %{_sysconfdir}/rc.d/rc.firewall
%{_sysconfdir}/rc.d/rc*.d/*firewall
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/iptables/*.so
%{_mandir}/man*/*
