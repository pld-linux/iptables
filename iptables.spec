#
# TODO:
#		- fix makefile (-D_UNKNOWN_KERNEL_POINTER_SIZE issue)
#
# Conditional build:
%bcond_without	doc		# without documentation (HOWTOS) which needed TeX
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without  vserver         # kernel build without vserver
#
%define		_netfilter_snap		20070806
%define		llh_version		7:2.6.22.1
%define		name6			ip6tables
#
Summary:	Extensible packet filtering system && extensible NAT system
Summary(pl.UTF-8):	System filtrowania pakietów oraz system translacji adresów (NAT)
Summary(pt_BR.UTF-8):	Ferramenta para controlar a filtragem de pacotes no kernel-2.6.x
Summary(ru.UTF-8):	Утилиты для управления пакетными фильтрами ядра Linux
Summary(uk.UTF-8):	Утиліти для керування пакетними фільтрами ядра Linux
Summary(zh_CN.UTF-8):	Linux内核包过滤管理工具
Name:		iptables
Version:	1.3.8
%define		_rel 5
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.netfilter.org/pub/iptables/%{name}-%{version}.tar.bz2
# Source0-md5:	0a9209f928002e5eee9cdff8fef4d4b3
Source1:	cvs://cvs.samba.org/netfilter/%{name}-howtos.tar.bz2
# Source1-md5:	2ed2b452daefe70ededd75dc0061fd07
Source2:	%{name}.init
Source3:	%{name6}.init
Patch0:		%{name}-%{_netfilter_snap}.patch
Patch1:		%{name}-man.patch
Patch2:		%{name}-1.3.0-imq1.diff
Patch3:		%{name}-connbytes-xtables.patch
Patch4:		grsecurity-1.2.11-iptables.patch
Patch5:		%{name}-layer7-2.3.patch
Patch6:		%{name}-old-1.3.7.patch
Patch7:		%{name}-account.patch
# http://people.linux-vserver.org/~dhozac/p/m/iptables-1.3.5-owner-xid.patch
Patch8:		%{name}-1.3.5-owner-xid.patch
Patch999:	%{name}-llh-dirty-hack.patch

URL:		http://www.netfilter.org/
%if %{with doc}
BuildRequires:	sgml-tools
BuildRequires:	sgmls
BuildRequires:	tetex-dvips
BuildRequires:	tetex-format-latex
BuildRequires:	tetex-latex
BuildRequires:	tetex-tex-babel
BuildRequires:	sed >= 4.0
%endif
%if %{with dist_kernel} && %{_netfilter_snap} != 0
BuildRequires:	kernel-headers(netfilter) >= %{_netfilter_snap}
#BuildRequires:	kernel-source
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

%description -l pl.UTF-8
Wydajny system translacji adresów (NAT) oraz system filtrowania
pakietów. Zamiennik ipchains w jądrach 2.4 i nowszych.

%description -l pt_BR.UTF-8
Esta é a ferramenta que controla o código de filtragem de pacotes do
kernel 2.4, obsoletando ipchains. Com esta ferramenta você pode
configurar filtros de pacotes, NAT, mascaramento (masquerading),
regras dinâmicas (stateful inspection), etc.

%description -l ru.UTF-8
iptables управляют кодом фильтрации сетевых пакетов в ядре Linux. Они
позволяют вам устанавливать межсетевые экраны (firewalls) и IP
маскарадинг, и т.п.

%description -l uk.UTF-8
iptables управляють кодом фільтрації пакетів мережі в ядрі Linux. Вони
дозволяють вам встановлювати міжмережеві екрани (firewalls) та IP
маскарадинг, тощо.

%package devel
Summary:	Libraries and headers for developing iptables extensions
Summary(pl.UTF-8):	Biblioteki i nagłówki do tworzenia rozszerzeń iptables
Group:		Development/Libraries
Obsoletes:	iptables24-devel

%description devel
Libraries and headers for developing iptables extensions.

%description devel -l pl.UTF-8
Biblioteki i pliki nagłówkowe niezbędne do tworzenia rozszerzeń dla
iptables.

%package init
Summary:	Iptables init (RedHat style)
Summary(pl.UTF-8):	Iptables init (w stylu RedHata)
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

%description init -l pl.UTF-8
Iptables-init ma na celu udostępnienie alternatywnego w stosunku do
firewall-init sposobu włączania i wyłączania filtrów IP jądra poprzez
iptables(8).

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%if %{with vserver}
%patch8 -p1
%endif

#patch999 -p1

chmod 755 extensions/.*-test*

%build
%{__make} all experimental \
	CC="%{__cc}" \
	COPT_FLAGS="%{rpmcflags} -D%{!?debug:N}DEBUG" \
	KERNEL_DIR="%{_kernelsrcdir}" \
	LIBDIR="%{_libdir}" \
	DO_SELINUX=1 \
	LDLIBS="-ldl"

%if %{with doc}
%{__make} -j1 -C iptables-howtos
sed -i 's:$(HTML_HOWTOS)::g; s:$(PSUS_HOWTOS)::g' iptables-howtos/Makefile
%endif

# Make a library, needed for OpenVCP
ar rcs libiptables.a iptables.o
ar rcs libip6tables.a ip6tables.o

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

install extensions/*so $RPM_BUILD_ROOT%{_libdir}/iptables

echo ".so iptables.8" > $RPM_BUILD_ROOT%{_mandir}/man8/%{name6}.8

# Devel stuff
cp -a include/{lib*,ip*} $RPM_BUILD_ROOT%{_includedir}
install lib*.a $RPM_BUILD_ROOT%{_libdir}
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
