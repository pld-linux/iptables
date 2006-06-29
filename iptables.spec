#
# TODO:
#		- fix makefile (-D_UNKNOWN_KERNEL_POINTER_SIZE issue)
#
# Conditional build:
%bcond_without	doc		# without documentation (HOWTOS) which needed TeX
%bcond_without	dist_kernel	# without distribution kernel
#
%define		_netfilter_snap		20060504
%define		llh_version		7:2.6.13.0-1
%define		name6			ip6tables
#
Summary:	Extensible packet filtering system && extensible NAT system
Summary(pl):	System filtrowania pakietów oraz system translacji adresów (NAT)
Summary(pt_BR):	Ferramenta para controlar a filtragem de pacotes no kernel-2.6.x
Summary(ru):	õÔÉÌÉÔÙ ÄÌÑ ÕÐÒÁ×ÌÅÎÉÑ ÐÁËÅÔÎÙÍÉ ÆÉÌØÔÒÁÍÉ ÑÄÒÁ Linux
Summary(uk):	õÔÉÌ¦ÔÉ ÄÌÑ ËÅÒÕ×ÁÎÎÑ ÐÁËÅÔÎÉÍÉ Æ¦ÌØÔÒÁÍÉ ÑÄÒÁ Linux
Summary(zh_CN):	LinuxÄÚºË°ü¹ýÂË¹ÜÀí¹¤¾ß
Name:		iptables
Version:	1.3.5
%define		_rel 1.2.6.16
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.netfilter.org/pub/iptables/%{name}-%{version}.tar.bz2
# Source0-md5:	00fb916fa8040ca992a5ace56d905ea5
Source1:	cvs://cvs.samba.org/netfilter/%{name}-howtos.tar.bz2
# Source1-md5:	2ed2b452daefe70ededd75dc0061fd07
Source2:	%{name}.init
Source3:	%{name6}.init

Patch0:		%{name}-%{_netfilter_snap}.patch
Patch1:		%{name}-Makefile.patch
Patch2:		%{name}-man.patch

Patch5:		%{name}-comment-%{_netfilter_snap}.patch
Patch6:		%{name}-expire-%{_netfilter_snap}.patch
Patch7:		%{name}-1.3.0-imq1.diff

Patch10:	%{name}-connbytes-xtables.patch

Patch12:	%{name}-ipp2p-%{_netfilter_snap}.patch
Patch13:	grsecurity-1.2.11-iptables.patch
#Patch7:		%{name}-nf-ULOG.patch
#Patch8:		%{name}-nf-geoip.patch
#Patch10:	%{name}-nf-ip_queue_vwmark.patch
#Patch11:	%{name}-hot_dirty_fix.patch
Patch14:	%{name}-layer7-2.2.patch
Patch999:	%{name}-llh-dirty-hack.patch

URL:		http://www.netfilter.org/
%if %{with doc}
BuildRequires:	sgml-tools
BuildRequires:	sgmls
BuildRequires:	texconfig
BuildRequires:	tetex-dvips
BuildRequires:	tetex-format-latex
BuildRequires:	tetex-latex
BuildRequires:	tetex-tex-babel
BuildRequires:	sed >= 4.0
%endif
%if %{with dist_kernel} && %{_netfilter_snap} != 0
BuildRequires:	kernel-headers(netfilter) >= %{_netfilter_snap}
BuildRequires:	kernel-source
Requires:	kernel(netfilter) >= %{_netfilter_snap}
%endif
#BuildRequires:	linux-libc-headers >= %{llh_version}
BuildConflicts:	kernel-headers < 2.3.0
Provides:	firewall-userspace-tool
Obsoletes:	netfilter
Obsoletes:	ipchains
Obsoletes:	iptables-ipp2p
Obsoletes:	iptables24-compat
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An extensible NAT system, and an extensible packet filtering system.
Replacement of ipchains in 2.4 and higher kernels.

%description -l pl
Wydajny system translacji adresów (NAT) oraz system filtrowania
pakietów. Zamiennik ipchains w j±drach 2.4 i nowszych.

%description -l pt_BR
Esta é a ferramenta que controla o código de filtragem de pacotes do
kernel 2.4, obsoletando ipchains. Com esta ferramenta você pode
configurar filtros de pacotes, NAT, mascaramento (masquerading),
regras dinâmicas (stateful inspection), etc.

%description -l ru
iptables ÕÐÒÁ×ÌÑÀÔ ËÏÄÏÍ ÆÉÌØÔÒÁÃÉÉ ÓÅÔÅ×ÙÈ ÐÁËÅÔÏ× × ÑÄÒÅ Linux. ïÎÉ
ÐÏÚ×ÏÌÑÀÔ ×ÁÍ ÕÓÔÁÎÁ×ÌÉ×ÁÔØ ÍÅÖÓÅÔÅ×ÙÅ ÜËÒÁÎÙ (firewalls) É IP
ÍÁÓËÁÒÁÄÉÎÇ, É Ô.Ð.

%description -l uk
iptables ÕÐÒÁ×ÌÑÀÔØ ËÏÄÏÍ Æ¦ÌØÔÒÁÃ¦§ ÐÁËÅÔ¦× ÍÅÒÅÖ¦ × ÑÄÒ¦ Linux. ÷ÏÎÉ
ÄÏÚ×ÏÌÑÀÔØ ×ÁÍ ×ÓÔÁÎÏ×ÌÀ×ÁÔÉ Í¦ÖÍÅÒÅÖÅ×¦ ÅËÒÁÎÉ (firewalls) ÔÁ IP
ÍÁÓËÁÒÁÄÉÎÇ, ÔÏÝÏ.

%package devel
Summary:	Libraries and headers for developing iptables extensions
Summary(pl):	Biblioteki i nag³ówki do tworzenia rozszerzeñ iptables
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	iptables24-devel

%description devel
Libraries and headers for developing iptables extensions.

%description devel -l pl
Biblioteki i pliki nag³ówkowe niezbêdne do tworzenia rozszerzeñ dla
iptables.

%package init
Summary:	Iptables init (RedHat style)
Summary(pl):	Iptables init (w stylu RedHata)
Group:		Networking/Admin
Release:	%{_rel}
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}
Obsoletes:	firewall-init
Obsoletes:	firewall-init-ipchains
Obsoletes:	iptables24-init

%description init
Iptables-init is meant to provide an alternate way than firewall-init
to start and stop packet filtering through iptables(8).

%description init -l pl
Iptables-init ma na celu udostêpnienie alternatywnego w stosunku do
firewall-init sposobu w³±czania i wy³±czania filtrów IP j±dra poprzez
iptables(8).

%prep
%setup -q -a1

%patch0 -p1
%{!?without_dist_kernel:%patch1 -p1}
%patch2 -p1

%patch5 -p1
%patch6 -p1
%patch7 -p1

%patch10 -p1

%patch12 -p1
%patch13 -p1
#patch4 -p1
#patch5 -p1
#patch7 -p1
#patch8 -p1
#patch9 -p1
#patch10 -p1
#patch11 -p1
%patch14 -p1

%patch999 -p1

chmod 755 extensions/.*-test*

# needs update (still valid?)
rm extensions/.string-test
rm extensions/.expire-test6

%build
%{__make} all experimental \
	CC="%{__cc}" \
	COPT_FLAGS="%{rpmcflags} -D%{!?debug:N}DEBUG" \
	KERNEL_DIR="%{_kernelsrcdir}" \
	LIBDIR="%{_libdir}" \
	LDLIBS="-ldl"

%if %{with doc}
%{__make} -C iptables-howtos
sed -i 's:$(HTML_HOWTOS)::g; s:$(PSUS_HOWTOS)::g' iptables-howtos/Makefile
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_includedir},%{_libdir},%{_mandir}/man3}

echo ".so iptables-save.8" > %{name6}-save.8
echo ".so iptables-restore.8" > %{name6}-restore.8

%{__make} install install-experimental \
	DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_libdir}

echo ".so iptables.8" > $RPM_BUILD_ROOT%{_mandir}/man8/%{name6}.8

# Devel stuff
cp -a include/{lib*,ip*} $RPM_BUILD_ROOT%{_includedir}
install lib*/lib*.a $RPM_BUILD_ROOT%{_libdir}
install libipq/*.3 $RPM_BUILD_ROOT%{_mandir}/man3

install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name6}

%clean
rm -rf $RPM_BUILD_ROOT

%post init
/sbin/chkconfig --add %{name}
/sbin/chkconfig --add %{name6}

%preun init
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del %{name}
	/sbin/chkconfig --del %{name6}
fi

%files
%defattr(644,root,root,755)
%{?with_doc:%doc iptables-howtos/{NAT,networking-concepts,packet-filtering}-HOWTO*}
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/iptables
%attr(755,root,root) %{_libdir}/iptables/*.so
%{_mandir}/man8/*

%files devel
%defattr(644,root,root,755)
%{?with_doc:%doc iptables-howtos/netfilter-hacking-HOWTO*}
%{_libdir}/lib*.a
%{_includedir}/*.h
%dir %{_includedir}/libip*
%{_includedir}/libip*/*.h
%{_mandir}/man3/*

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/*
