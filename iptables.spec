Summary:	extensible packet filtering system && extensible NAT system
Summary(pl):	system filtrowania pakiet�w oraz system translacji adres�w (NAT)
Name:		iptables
Version:	1.2
Release:	3
License:	GPL
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
URL:		http://netfilter.kernelnotes.org/
Vendor:		Netfilter mailing list <netfilter@lists.samba.org>
Source0:	http://netfilter.kernelnotes.org/%{name}-%{version}.tar.bz2
Source1:	cvs://cvs.samba.org/netfilter/%{name}-howtos.tar.bz2
Source2:	rc.firewall
Patch0:		ftp://sith.mimuw.edu.pl/pub/users/baggins/iptables-psd.patch
Patch1:		%{name}-ip6libdir.patch
BuildRequires:	sgml-tools
BuildRequires:	sgmls
BuildRequires:	mysql-devel
#Requires:	kernel >= 2.4.0test9
Obsoletes:	netfilter
Obsoletes:	ipchains
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc

%description
An extensible NAT system, and an extensible packet filtering system.

%description -l pl
Wydajny system translacji adres�w (NAT) oraz system filtrowania
pakiet�w.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1
chmod 755 extensions/.psd-test
perl -pi -e 's/\$\(HTML_HOWTOS\)//g; s/\$\(PSUS_HOWTOS\)//g' iptables-howtos/Makefile

%build
%{__make} depend 2> /dev/null || :
%{__make} COPT_FLAGS="$RPM_OPT_FLAGS" \
	LIBDIR="%{_libdir}" \
	all

%{__make} -C iptables-howtos

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc{0,1,2,3,4,5,6}.d

%{__make} install DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_libdir}

install ip6tables $RPM_BUILD_ROOT%{_sbindir}/
install ippool/ippool $RPM_BUILD_ROOT%{_sbindir}/

install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/
ln -s ../rc.firewall $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc0.d/K91firewall
ln -s ../rc.firewall $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc1.d/K91firewall
ln -s ../rc.firewall $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc2.d/S09firewall
ln -s ../rc.firewall $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc3.d/S09firewall
ln -s ../rc.firewall $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc4.d/S09firewall
ln -s ../rc.firewall $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc5.d/S09firewall
ln -s ../rc.firewall $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc6.d/K91firewall

gzip -9 KNOWN_BUGS iptables-howtos/*.{txt,ps}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc KNOWN_BUGS.gz iptables-howtos/*.gz
%{_sysconfdir}/rc.d/rc*.d/*firewall
%attr(754,root,root) %config(noreplace) %verify(not mtime md5 size) %{_sysconfdir}/rc.d/rc.firewall

%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/iptables/*.so

%{_mandir}/man*/*
