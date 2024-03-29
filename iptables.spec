#
# TODO:
# - recheck ebtables functionality:
#   - is it still valid: "The original old ebtables is still needed e.g. for libvirt's nwfilter"?
#   - is ebtables init script/service usable with iptables ebtables implementation now?
#     if so, then move them here from legacy ebtables.spec
# - update BR to real required llh version
#
# Conditional build:
%bcond_without	doc		# HOWTOS documentation (which requires TeX)
%bcond_without	dist_kernel	# distribution (patched) kernel enhancements (alias for with: ipt_IPV4OPTSSTRIP ipt_rpc xt_layer7)
%bcond_without	nftables	# nftables compatibility
%bcond_without	pcap		# pcap-dependend utils (nfbpf_compile, nfsynproxy)
%bcond_with	vserver		# xt_owner module with vserver support
%bcond_with	batch		# iptables-batch utils
%bcond_with	static		# static libraries, no dynamic modules (all linked into binaries)
%bcond_with	ipt_IPV4OPTSSTRIP # ipt_IPV4OPTSSTRIP module (requires kernel patch to work)
%bcond_with	ipt_rpc		# ipt_rpc module (requires kernel patch to work)
%bcond_with	xt_layer7	# xt_layer7 module (requires kernel patch to work)
%bcond_with	usekernelsrc	# include kernel headers from %{_kernelsrcdir}
%bcond_with	default_nft	# use nftables backend by default

%if %{with dist_kernel}
%define	with_ipt_IPV4OPTSSTRIP	1
%define	with_ipt_rpc		1
%define	with_xt_layer7		1
%endif

%define		orgname	iptables

Summary:	Extensible packet filtering system && extensible NAT system
Summary(pl.UTF-8):	System filtrowania pakietów oraz system translacji adresów (NAT)
Summary(pt_BR.UTF-8):	Ferramenta para controlar a filtragem de pacotes no kernel-2.6.x
Summary(ru.UTF-8):	Утилиты для управления пакетными фильтрами ядра Linux
Summary(uk.UTF-8):	Утиліти для керування пакетними фільтрами ядра Linux
Summary(zh_CN.UTF-8):	Linux内核包过滤管理工具
Name:		iptables%{?with_vserver:-vserver}
Version:	1.8.10
Release:	1
License:	GPL v2
Group:		Networking/Admin
Source0:	https://netfilter.org/projects/iptables/files/%{orgname}-%{version}.tar.xz
# Source0-md5:	5eaa3bb424dd3a13c98c0cb026314029
Source1:	cvs://cvs.samba.org/netfilter/%{orgname}-howtos.tar.bz2
# Source1-md5:	2ed2b452daefe70ededd75dc0061fd07
Source2:	iptables.init
Source3:	ip6tables.init
Source6:	iptables-config
Source7:	ip6tables-config
Source8:	iptables.service
Source9:	ip6tables.service
# these are not compatible with this package! there are no ebtables-save and ebtables-restore here
Source10:	ebtables.init
Source11:	ebtables-config
Source12:	ebtables.service
# --- GENERAL CHANGES (patches<10):
Patch0:		%{orgname}-man.patch
# additional utils; off by default
Patch1:		%{orgname}-batch.patch
Patch2:		no-libiptc.patch
Patch3:		%{orgname}-aligned_u64.patch
# --- ADDITIONAL/CHANGED EXTENSIONS:
# just ipt_IPV4OPTSSTRIP now
Patch10:	%{orgname}-20070806.patch
# xt_layer7; almost based on iptables-1.4-for-kernel-2.6.20forward-layer7-2.18.patch
# http://downloads.sourceforge.net/l7-filter/netfilter-layer7-v2.18.tar.gz
Patch11:	%{orgname}-layer7.patch
# ipt_rpc
Patch12:	%{orgname}-old-1.3.7.patch
# xt_IMQ; http://linuximq.net/patchs/iptables-1.4.12-IMQ-test4.diff
Patch13:	%{orgname}-imq.patch
# enhances ipt_owner/ip6t_owner; http://people.linux-vserver.org/~dhozac/p/m/iptables-1.3.5-owner-xid.patch (currently disabled, needs update for xt_owner)
Patch14:	%{orgname}-owner-xid.patch
# adjusts xt_owner for vserver-enabled kernel
Patch15:	%{orgname}-owner-struct-size-vs.patch
Patch16:	%{orgname}-rpc.patch
Patch18:	%{orgname}-default_nft.patch
URL:		https://netfilter.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	groff
%{?with_nftables:BuildRequires:	libmnl-devel >= 1.0}
BuildRequires:	libnetfilter_conntrack-devel >= 1.0.6
BuildRequires:	libnfnetlink-devel >= 1.0
%{?with_nftables:BuildRequires:	libnftnl-devel >= 1.2.6}
%{?with_pcap:BuildRequires:	libpcap-devel}
BuildRequires:	libtirpc-devel >= 0.2.0
BuildRequires:	libtool >= 2:2
BuildRequires:	linux-libc-headers >= 7:2.6.22.1
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	rpmbuild(macros) >= 1.647
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with doc}
BuildRequires:	sed >= 4.0
BuildRequires:	sgml-tools
BuildRequires:	sgmls
BuildRequires:	tetex-dvips
BuildRequires:	tetex-format-latex
BuildRequires:	tetex-latex
BuildRequires:	tetex-tex-babel
BuildRequires:	texlive-fonts-cmsuper
BuildRequires:	texlive-fonts-jknappen
%endif
Requires:	%{orgname}-libs = %{version}-%{release}
%{?with_nftables:Requires:	libmnl >= 1.0}
Requires:	libnetfilter_conntrack >= 1.0.6
Requires:	libnfnetlink >= 1.0
%{?with_nftables:Requires:	libnftnl >= 1.2.6}
Provides:	firewall-userspace-tool
%{?with_vserver:Provides:	iptables = %{version}-%{release}}
Conflicts:	arptables < 0.0.5
Obsoletes:	ipchains < 1.4
Obsoletes:	iptables24-compat < 1.3
Obsoletes:	netfilter
Conflicts:	xtables-addons < 1.25
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

%package libs
Summary:	iptables libraries
Summary(pl.UTF-8):	Biblioteki iptables
Group:		Libraries
Conflicts:	iptables < 1.4.3-1

%description libs
iptables libraries.

%description libs -l pl.UTF-8
Biblioteki iptables.

%package devel
Summary:	Libraries and headers for developing iptables extensions
Summary(pl.UTF-8):	Biblioteki i nagłówki do tworzenia rozszerzeń iptables
Group:		Development/Libraries
Requires:	%{orgname}-libs = %{epoch}:%{version}-%{release}
Obsoletes:	iptables24-devel < 1.3

%description devel
Libraries and headers for developing iptables extensions.

%description devel -l pl.UTF-8
Biblioteki i pliki nagłówkowe niezbędne do tworzenia rozszerzeń dla
iptables.

%package static
Summary:	Static iptables libraries
Summary(pl.UTF-8):	Biblioteki statyczne iptables
Group:		Development/Libraries
Requires:	%{orgname}-devel = %{epoch}:%{version}-%{release}

%description static
Static iptables libraries.

%description static -l pl.UTF-8
Biblioteki statyczne iptables.

%package init
Summary:	Iptables init (RedHat style)
Summary(pl.UTF-8):	Iptables init (w stylu RedHata)
Group:		Networking/Admin
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts >= 0.4.3.0
Requires:	systemd-units >= 38
Obsoletes:	firewall-init < 3
Obsoletes:	firewall-init-ipchains < 2.2
Obsoletes:	iptables24-init < 1.3
%{?with_vserver:Provides:	iptables-init = %{version}-%{release}}

%description init
Iptables-init is meant to provide an alternate way than firewall-init
to start and stop packet filtering through iptables(8).

%description init -l pl.UTF-8
Iptables-init ma na celu udostępnienie alternatywnego w stosunku do
firewall-init sposobu włączania i wyłączania filtrów IP jądra poprzez
iptables(8).

%package ebtables
Summary:	Ethernet Bridge Tables - xtables compatibility wrapper
Summary(pl.UTF-8):	Ethernet Bridge Tables – nakładka kompatybilności na xtables
Group:		Networking/Admin
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts >= 0.4.3.0
Requires:	systemd-units >= 38
# do not 'provide' something this is not really compatible with
#Provides:	ebtables
Conflicts:	ebtables < 2.0.11
%{?with_vserver:Provides:	iptables-ebtables = %{version}-%{release}}

%description ebtables
ebtables is a tool for managing Linux 2.5.x (and above) Link Layer
firewalling subsystem.

This package contains a compatibility wrapper over xtables providing
some functionality of the original ebtables tool.

Note: this is not really a fully-compatible drop-in replacement!

%description ebtables -l pl.UTF-8
ebtables to narzędzie do zarządzania podsystemem firewalla warstwy
połączenia (Link Layer) Linuksa 2.5.x (i nowszych).

Ten pakiet zawiera warstwę zgodności dla xtables zapewniającą część
funkcjonalności oryginalnego narzędzia ebtables.

Uwaga: nie jest to w pełni zgodny zamiennik!

%prep
%setup -q -n iptables-%{version} -a1
%patch0 -p1
%if %{with batch}
%patch1 -p1
%endif
%patch2 -p1
%patch3 -p1

%{?with_ipt_IPV4OPTSSTRIP:%patch10 -p1}
%{?with_xt_layer7:%patch11 -p1}
%{?with_ipt_rpc:%patch12 -p1}
%patch13 -p1
%if %{with vserver}
%patch14 -p1
%patch15 -p1
%endif
%patch16 -p1
%if %{with nftables} && %{with default_nft}
%patch18 -p1
%endif

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	CFLAGS="%{rpmcflags} %{rpmcppflags} -D%{!?debug:N}DEBUG" \
	%{?with_usekernelsrc:--with-kernel=%{_kernelsrcdir}} \
	%{?with_pcap:--enable-bpf-compiler} \
	--enable-libipq \
	%{?with_pcap:--enable-nfsynproxy} \
	%{!?with_nftables:--disable-nftables} \
	%{?with_static:--enable-static}

%{__make} -j1 all \
	V=1

%if %{with doc}
%{__make} -j1 -C iptables-howtos
sed -i 's:$(HTML_HOWTOS)::g; s:$(PSUS_HOWTOS)::g' iptables-howtos/Makefile
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT{%{_includedir},%{_libdir},%{_mandir}/man3} \
	$RPM_BUILD_ROOT%{systemdunitdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_libdir}

# use ld script for -liptc backward compat (see no-libiptc.patch for source)
%{__sed} \
%ifarch %{x8664} alpha aarch64 hppa64 mips64 ppc64 s390x sparc64
	-e 's,@BITS@,64,' \
%else
	-e 's,@BITS@,32,' \
%endif
	-e 's,@LIBDIR@,%{_libdir},g' \
	-e "s,@ARCH@,$(echo "%{_build_arch}" | tr _ -)," libiptc/libiptc.ld.in >$RPM_BUILD_ROOT%{_libdir}/libiptc.so

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib{ip4tc,ip6tc,ipq,xtables}.la

install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/iptables
install -p %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/ip6tables

install -p %{SOURCE6} $RPM_BUILD_ROOT/etc/sysconfig/iptables-config
install -p %{SOURCE7} $RPM_BUILD_ROOT/etc/sysconfig/ip6tables-config

install -p %{SOURCE8} $RPM_BUILD_ROOT%{systemdunitdir}/iptables.service
install -p %{SOURCE9} $RPM_BUILD_ROOT%{systemdunitdir}/ip6tables.service

# these won't work as they are now
#install -p %{SOURCE10} $RPM_BUILD_ROOT/etc/rc.d/init.d/ebtables
#install -p %{SOURCE11} $RPM_BUILD_ROOT/etc/sysconfig/ebtables-config
#install -p %{SOURCE12} $RPM_BUILD_ROOT%{systemdunitdir}/ebtables.service

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post init
/sbin/chkconfig --add iptables
/sbin/chkconfig --add ip6tables
%systemd_post iptables.service ip6tables.service

%preun init
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del iptables
	/sbin/chkconfig --del ip6tables
fi
%systemd_preun iptables.service ip6tables.service

%postun init
%systemd_reload

%triggerpostun init -- iptables-init < 1.4.13-2
%systemd_trigger iptables.service ip6tables.service

%files
%defattr(644,root,root,755)
%{?with_doc:%doc iptables-howtos/{NAT,networking-concepts,packet-filtering}-HOWTO*}
%attr(755,root,root) %{_bindir}/iptables-xml
%attr(755,root,root) %{_sbindir}/ip6tables
%attr(755,root,root) %{_sbindir}/ip6tables-apply
%attr(755,root,root) %{_sbindir}/ip6tables-legacy
%attr(755,root,root) %{_sbindir}/ip6tables-legacy-restore
%attr(755,root,root) %{_sbindir}/ip6tables-legacy-save
%attr(755,root,root) %{_sbindir}/ip6tables-restore
%attr(755,root,root) %{_sbindir}/ip6tables-save
%attr(755,root,root) %{_sbindir}/iptables
%attr(755,root,root) %{_sbindir}/iptables-apply
%attr(755,root,root) %{_sbindir}/iptables-legacy
%attr(755,root,root) %{_sbindir}/iptables-legacy-restore
%attr(755,root,root) %{_sbindir}/iptables-legacy-save
%attr(755,root,root) %{_sbindir}/iptables-restore
%attr(755,root,root) %{_sbindir}/iptables-save
%attr(755,root,root) %{_sbindir}/xtables-legacy-multi
%if %{with batch}
%attr(755,root,root) %{_sbindir}/iptables-batch
%attr(755,root,root) %{_sbindir}/ip6tables-batch
%endif
%attr(755,root,root) %{_sbindir}/nfnl_osf
%if %{with pcap}
%attr(755,root,root) %{_sbindir}/nfbpf_compile
%attr(755,root,root) %{_sbindir}/nfsynproxy
%endif
%{_datadir}/xtables
%dir %{_libdir}/xtables
%attr(755,root,root) %{_libdir}/xtables/libip6t_DNPT.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_HL.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_NETMAP.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_REJECT.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_SNPT.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_ah.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_dst.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_eui64.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_frag.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_hbh.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_hl.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_icmp6.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_ipv6header.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_mh.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_rt.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_srh.so
%attr(755,root,root) %{_libdir}/xtables/libipt_CLUSTERIP.so
%attr(755,root,root) %{_libdir}/xtables/libipt_ECN.so
%{?with_ipt_IPV4OPTSSTRIP:%attr(755,root,root) %{_libdir}/xtables/libipt_IPV4OPTSSTRIP.so}
%attr(755,root,root) %{_libdir}/xtables/libipt_NETMAP.so
%attr(755,root,root) %{_libdir}/xtables/libipt_REJECT.so
%attr(755,root,root) %{_libdir}/xtables/libipt_TTL.so
%attr(755,root,root) %{_libdir}/xtables/libipt_ULOG.so
%attr(755,root,root) %{_libdir}/xtables/libipt_ah.so
%attr(755,root,root) %{_libdir}/xtables/libipt_icmp.so
%attr(755,root,root) %{_libdir}/xtables/libipt_realm.so
%{?with_ipt_rpc:%attr(755,root,root) %{_libdir}/xtables/libipt_rpc.so}
%attr(755,root,root) %{_libdir}/xtables/libipt_ttl.so
%attr(755,root,root) %{_libdir}/xtables/libxt_AUDIT.so
%attr(755,root,root) %{_libdir}/xtables/libxt_CHECKSUM.so
%attr(755,root,root) %{_libdir}/xtables/libxt_CLASSIFY.so
%attr(755,root,root) %{_libdir}/xtables/libxt_CONNMARK.so
%attr(755,root,root) %{_libdir}/xtables/libxt_CONNSECMARK.so
%attr(755,root,root) %{_libdir}/xtables/libxt_CT.so
%attr(755,root,root) %{_libdir}/xtables/libxt_DNAT.so
%attr(755,root,root) %{_libdir}/xtables/libxt_DSCP.so
%attr(755,root,root) %{_libdir}/xtables/libxt_HMARK.so
%attr(755,root,root) %{_libdir}/xtables/libxt_IDLETIMER.so
%attr(755,root,root) %{_libdir}/xtables/libxt_IMQ.so
%attr(755,root,root) %{_libdir}/xtables/libxt_LED.so
%attr(755,root,root) %{_libdir}/xtables/libxt_LOG.so
%attr(755,root,root) %{_libdir}/xtables/libxt_MARK.so
%attr(755,root,root) %{_libdir}/xtables/libxt_MASQUERADE.so
%attr(755,root,root) %{_libdir}/xtables/libxt_NAT.so
%attr(755,root,root) %{_libdir}/xtables/libxt_NFLOG.so
%attr(755,root,root) %{_libdir}/xtables/libxt_NFQUEUE.so
%attr(755,root,root) %{_libdir}/xtables/libxt_NOTRACK.so
%attr(755,root,root) %{_libdir}/xtables/libxt_RATEEST.so
%attr(755,root,root) %{_libdir}/xtables/libxt_REDIRECT.so
%attr(755,root,root) %{_libdir}/xtables/libxt_SECMARK.so
%attr(755,root,root) %{_libdir}/xtables/libxt_SET.so
%attr(755,root,root) %{_libdir}/xtables/libxt_SNAT.so
%attr(755,root,root) %{_libdir}/xtables/libxt_SYNPROXY.so
%attr(755,root,root) %{_libdir}/xtables/libxt_TCPMSS.so
%attr(755,root,root) %{_libdir}/xtables/libxt_TCPOPTSTRIP.so
%attr(755,root,root) %{_libdir}/xtables/libxt_TEE.so
%attr(755,root,root) %{_libdir}/xtables/libxt_TOS.so
%attr(755,root,root) %{_libdir}/xtables/libxt_TPROXY.so
%attr(755,root,root) %{_libdir}/xtables/libxt_TRACE.so
%attr(755,root,root) %{_libdir}/xtables/libxt_addrtype.so
%attr(755,root,root) %{_libdir}/xtables/libxt_bpf.so
%attr(755,root,root) %{_libdir}/xtables/libxt_cgroup.so
%attr(755,root,root) %{_libdir}/xtables/libxt_cluster.so
%attr(755,root,root) %{_libdir}/xtables/libxt_comment.so
%attr(755,root,root) %{_libdir}/xtables/libxt_connbytes.so
%attr(755,root,root) %{_libdir}/xtables/libxt_connlabel.so
%attr(755,root,root) %{_libdir}/xtables/libxt_connlimit.so
%attr(755,root,root) %{_libdir}/xtables/libxt_connmark.so
%attr(755,root,root) %{_libdir}/xtables/libxt_conntrack.so
%attr(755,root,root) %{_libdir}/xtables/libxt_cpu.so
%attr(755,root,root) %{_libdir}/xtables/libxt_dccp.so
%attr(755,root,root) %{_libdir}/xtables/libxt_devgroup.so
%attr(755,root,root) %{_libdir}/xtables/libxt_dscp.so
%attr(755,root,root) %{_libdir}/xtables/libxt_ecn.so
%attr(755,root,root) %{_libdir}/xtables/libxt_esp.so
%attr(755,root,root) %{_libdir}/xtables/libxt_hashlimit.so
%attr(755,root,root) %{_libdir}/xtables/libxt_helper.so
%attr(755,root,root) %{_libdir}/xtables/libxt_ipcomp.so
%attr(755,root,root) %{_libdir}/xtables/libxt_iprange.so
%attr(755,root,root) %{_libdir}/xtables/libxt_ipvs.so
%{?with_xt_layer7:%attr(755,root,root) %{_libdir}/xtables/libxt_layer7.so}
%attr(755,root,root) %{_libdir}/xtables/libxt_length.so
%attr(755,root,root) %{_libdir}/xtables/libxt_limit.so
%attr(755,root,root) %{_libdir}/xtables/libxt_mac.so
%attr(755,root,root) %{_libdir}/xtables/libxt_mark.so
%attr(755,root,root) %{_libdir}/xtables/libxt_multiport.so
%attr(755,root,root) %{_libdir}/xtables/libxt_nfacct.so
%attr(755,root,root) %{_libdir}/xtables/libxt_osf.so
%attr(755,root,root) %{_libdir}/xtables/libxt_owner.so
%attr(755,root,root) %{_libdir}/xtables/libxt_physdev.so
%attr(755,root,root) %{_libdir}/xtables/libxt_pkttype.so
%attr(755,root,root) %{_libdir}/xtables/libxt_policy.so
%attr(755,root,root) %{_libdir}/xtables/libxt_quota.so
%attr(755,root,root) %{_libdir}/xtables/libxt_rateest.so
%attr(755,root,root) %{_libdir}/xtables/libxt_recent.so
%attr(755,root,root) %{_libdir}/xtables/libxt_rpfilter.so
%attr(755,root,root) %{_libdir}/xtables/libxt_sctp.so
%attr(755,root,root) %{_libdir}/xtables/libxt_set.so
%attr(755,root,root) %{_libdir}/xtables/libxt_socket.so
%attr(755,root,root) %{_libdir}/xtables/libxt_standard.so
%attr(755,root,root) %{_libdir}/xtables/libxt_state.so
%attr(755,root,root) %{_libdir}/xtables/libxt_statistic.so
%attr(755,root,root) %{_libdir}/xtables/libxt_string.so
%attr(755,root,root) %{_libdir}/xtables/libxt_tcp.so
%attr(755,root,root) %{_libdir}/xtables/libxt_tcpmss.so
%attr(755,root,root) %{_libdir}/xtables/libxt_time.so
%attr(755,root,root) %{_libdir}/xtables/libxt_tos.so
%attr(755,root,root) %{_libdir}/xtables/libxt_u32.so
%attr(755,root,root) %{_libdir}/xtables/libxt_udp.so
%{_mandir}/man1/iptables-xml.1*
%{_mandir}/man8/ip6tables.8*
%{_mandir}/man8/ip6tables-apply.8*
%{_mandir}/man8/ip6tables-restore.8*
%{_mandir}/man8/ip6tables-save.8*
%{_mandir}/man8/iptables.8*
%{_mandir}/man8/iptables-apply.8*
%{_mandir}/man8/iptables-extensions.8*
%{_mandir}/man8/iptables-restore.8*
%{_mandir}/man8/iptables-save.8*
%{_mandir}/man8/nfnl_osf.8*
%if %{with pcap}
%{_mandir}/man8/nfbpf_compile.8*
%endif
%if %{with nftables}
%attr(755,root,root) %{_sbindir}/arptables
%attr(755,root,root) %{_sbindir}/arptables-nft
%attr(755,root,root) %{_sbindir}/arptables-nft-restore
%attr(755,root,root) %{_sbindir}/arptables-nft-save
%attr(755,root,root) %{_sbindir}/arptables-restore
%attr(755,root,root) %{_sbindir}/arptables-save
%attr(755,root,root) %{_sbindir}/ip6tables-nft
%attr(755,root,root) %{_sbindir}/ip6tables-nft-restore
%attr(755,root,root) %{_sbindir}/ip6tables-nft-save
%attr(755,root,root) %{_sbindir}/iptables-nft
%attr(755,root,root) %{_sbindir}/iptables-nft-restore
%attr(755,root,root) %{_sbindir}/iptables-nft-save
%attr(755,root,root) %{_sbindir}/xtables-monitor
%attr(755,root,root) %{_sbindir}/xtables-nft-multi
%attr(755,root,root) %{_sbindir}/iptables-restore-translate
%attr(755,root,root) %{_sbindir}/iptables-translate
%attr(755,root,root) %{_sbindir}/ip6tables-restore-translate
%attr(755,root,root) %{_sbindir}/ip6tables-translate
%attr(755,root,root) %{_libdir}/xtables/libarpt_mangle.so
%attr(755,root,root) %{_libdir}/xtables/libebt_802_3.so
%attr(755,root,root) %{_libdir}/xtables/libebt_among.so
%attr(755,root,root) %{_libdir}/xtables/libebt_arp.so
%attr(755,root,root) %{_libdir}/xtables/libebt_arpreply.so
%attr(755,root,root) %{_libdir}/xtables/libebt_dnat.so
%attr(755,root,root) %{_libdir}/xtables/libebt_ip.so
%attr(755,root,root) %{_libdir}/xtables/libebt_ip6.so
%attr(755,root,root) %{_libdir}/xtables/libebt_log.so
%attr(755,root,root) %{_libdir}/xtables/libebt_mark.so
%attr(755,root,root) %{_libdir}/xtables/libebt_mark_m.so
%attr(755,root,root) %{_libdir}/xtables/libebt_nflog.so
%attr(755,root,root) %{_libdir}/xtables/libebt_pkttype.so
%attr(755,root,root) %{_libdir}/xtables/libebt_redirect.so
%attr(755,root,root) %{_libdir}/xtables/libebt_snat.so
%attr(755,root,root) %{_libdir}/xtables/libebt_stp.so
%attr(755,root,root) %{_libdir}/xtables/libebt_vlan.so
%{_mandir}/man8/arptables-nft.8*
%{_mandir}/man8/arptables-nft-restore.8*
%{_mandir}/man8/arptables-nft-save.8*
%{_mandir}/man8/ip6tables-restore-translate.8*
%{_mandir}/man8/ip6tables-translate.8*
%{_mandir}/man8/iptables-restore-translate.8*
%{_mandir}/man8/iptables-translate.8*
%{_mandir}/man8/xtables-legacy.8*
%{_mandir}/man8/xtables-monitor.8*
%{_mandir}/man8/xtables-nft.8*
%{_mandir}/man8/xtables-translate.8*
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libip4tc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libip4tc.so.2
%attr(755,root,root) %{_libdir}/libip6tc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libip6tc.so.2
%attr(755,root,root) %{_libdir}/libipq.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libipq.so.0
%attr(755,root,root) %{_libdir}/libxtables.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxtables.so.12

%files devel
%defattr(644,root,root,755)
%{?with_doc:%doc iptables-howtos/netfilter-hacking-HOWTO*}
%attr(755,root,root) %{_libdir}/libip4tc.so
%attr(755,root,root) %{_libdir}/libip6tc.so
%attr(755,root,root) %{_libdir}/libipq.so
%attr(755,root,root) %{_libdir}/libiptc.so
%attr(755,root,root) %{_libdir}/libxtables.so
%{_includedir}/libipq.h
%{_includedir}/xtables.h
%{_includedir}/xtables-version.h
%{_includedir}/libiptc
%{_pkgconfigdir}/libip4tc.pc
%{_pkgconfigdir}/libip6tc.pc
%{_pkgconfigdir}/libipq.pc
%{_pkgconfigdir}/libiptc.pc
%{_pkgconfigdir}/xtables.pc
%{_mandir}/man3/ipq_*.3*
%{_mandir}/man3/libipq.3*

%if %{with static}
%files static
%defattr(644,root,root,755)
%{_libdir}/libip4tc.a
%{_libdir}/libip6tc.a
%{_libdir}/libipq.a
%{_libdir}/libxtables.a
%endif

%files init
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/iptables-config
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ip6tables-config
%attr(754,root,root) /etc/rc.d/init.d/iptables
%attr(754,root,root) /etc/rc.d/init.d/ip6tables
%{systemdunitdir}/iptables.service
%{systemdunitdir}/ip6tables.service

%if %{with nftables}
%files ebtables
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ebtables
%attr(755,root,root) %{_sbindir}/ebtables-nft
%attr(755,root,root) %{_sbindir}/ebtables-nft-restore
%attr(755,root,root) %{_sbindir}/ebtables-nft-save
%attr(755,root,root) %{_sbindir}/ebtables-restore
%attr(755,root,root) %{_sbindir}/ebtables-save
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ethertypes
%{_mandir}/man8/ebtables-nft.8*
%if %{with nftables}
%attr(755,root,root) %{_sbindir}/ebtables-translate
%{_mandir}/man8/ebtables-translate.8*
%endif
%endif
