#
# Conditional build:
%bcond_without patchedkernel	# without ippool, prestate, log (which requires patched 2.4.x kernel) 4
%bcond_without howto		# without documentation (HOWTOS) which needed TeX. 5
#
#%define		netfilter_snap	0
%define		netfilter_snap	20031206
%define		iptables_version	1.2.9
Summary:	Extensible packet filtering system && extensible NAT system
Summary(pl):	System filtrowania pakietСw oraz system translacji adresСw (NAT)
Summary(pt_BR):	Ferramenta para controlar a filtragem de pacotes no kernel-2.4.x
Summary(ru):	Утилиты для управления пакетными фильтрами ядра Linux
Summary(uk):	Утил╕ти для керування пакетними ф╕льтрами ядра Linux
Summary(zh_CN):	Linuxдз╨к╟Э╧Щбк╧эюМ╧╓╬ъ
Name:		iptables
%if %{netfilter_snap} != 0
Version:	%{iptables_version}_%{netfilter_snap}
%else
Version:	%{iptables_version}
%endif
%define		_rel	1
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Networking/Daemons
URL:		http://www.netfilter.org/
Vendor:		Netfilter mailing list <netfilter@lists.samba.org>
Source0:	ftp://ftp.netfilter.org/pub/iptables/snapshot/%{name}-%{iptables_version}-%{netfilter_snap}.tar.bz2
# Source0-md5:	6f6070d1b489a684d622b901fa307290
Source1:	cvs://cvs.samba.org/netfilter/%{name}-howtos.tar.bz2

Source2:	%{name}.init
Patch0:		%{name}-man.patch
Patch3:		http://trash.net/~kaber/imq/pom-20030625.diff
Patch4:		grsecurity-%{iptables_version}-iptables.patch
# CVS up-to-date
#Patch9:		iptables-1.2.8-CVS-20030715.patch
# patches from netfilter
#Patch10:	ipt_REJECT-fake-source.patch.userspace
#Patch11:	mark-bitwise-ops.patch.userspace
Patch12:	iptables-1.2.9-ipt_p2p.patch
# http://rnvs.informatik.uni-leipzig.de/ipp2p/index_en.html
Patch13:	ipp2p-0.5a_vs_iptables-1.2.9.patch.gz

%{?with_howto:BuildRequires:	sgml-tools}
%{?with_howto:BuildRequires:	sgmls}
%{?with_howto:BuildRequires:	tetex-dvips}
%{?with_howto:BuildRequires:	tetex-format-latex}
%{?with_howto:BuildRequires:	tetex-latex}
%{?with_howto:BuildRequires:	tetex-tex-babel}
BuildRequires:	perl-base
%if %{netfilter_snap} != 0
%{?with_patchedkernel:BuildRequires:	kernel-headers(netfilter) = %{iptables_version}-%{netfilter_snap}}
%else
%{?with_patchedkernel:BuildRequires:	kernel-headers(netfilter) = %{iptables_version}}
%endif
%{?with_patchedkernel:BuildRequires:       kernel-source}
BuildConflicts:	kernel-headers < 2.3.0
Provides:	firewall-userspace-tool
Obsoletes:	netfilter
Obsoletes:	ipchains
%if %{netfilter_snap} != 0
%{?with_patchedkernel:Requires:	kernel(netfilter) = %{iptables_version}-%{netfilter_snap}}
%else
%{?with_patchedkernel:Requires:	kernel(netfilter) = %{iptables_version}}
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-%{netfilter_snap}-root-%(id -u -n)

%description
An extensible NAT system, and an extensible packet filtering system.
Replacement of ipchains in 2.4 kernels.

%description -l pl
Wydajny system translacji adresСw (NAT) oraz system filtrowania
pakietСw. Zamiennik ipchains w j╠drach 2.4

%description -l pt_BR
Esta И a ferramenta que controla o cСdigo de filtragem de pacotes do
kernel 2.4, obsoletando ipchains. Com esta ferramenta vocЙ pode
configurar filtros de pacotes, NAT, mascaramento (masquerading),
regras dinБmicas (stateful inspection), etc.

%description -l ru
iptables управляют кодом фильтрации сетевых пакетов в ядре Linux. Они
позволяют вам устанавливать межсетевые экраны (firewalls) и IP
маскарадинг, и т.п.

%description -l uk
iptables управляють кодом ф╕льтрац╕╖ пакет╕в мереж╕ в ядр╕ Linux. Вони
дозволяють вам встановлювати м╕жмережев╕ екрани (firewalls) та IP
маскарадинг, тощо.

%package devel
Summary:	Libraries and headers for developing iptables extensions
Summary(pl):	Biblioteki i nagЁСwki do tworzenia rozszerzeЯ iptables
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Libraries and headers for developing iptables extensions.

%description devel -l pl
Biblioteki i pliki nagЁСwkowe niezbЙdne do tworzenia rozszerzeЯ dla
iptables.

%package init
Summary:	Iptables init (RedHat style)
Summary(pl):	Iptables init (w stylu RedHata)
Group:		Networking/Admin
PreReq:		rc-scripts
Requires(post,preun):   /sbin/chkconfig
Requires:	%{name}
Obsoletes:	firewall-init

%description init
Iptables-init is meant to provide an alternate way than firewall-init
to start and stop packet filtering through iptables(8).

%description init -l pl
Iptablea-init ma na celu udostЙpnienie alternatywnego w stosunku do
firewall-init sposobu wЁ╠czania i wyЁ╠czania filtrСw IP j╠dra poprzez
iptables(8).

%prep
%setup -q -a1 -n %{name}-%{iptables_version}-%{netfilter_snap}
%patch0 -p1
%{?with_patchedkernel:%patch3 -p1}
%{?with_patchedkernel:patch -p1 < userspace/IMQ.patch.userspace}
%{?with_patchedkernel:%patch4 -p1}
# % {!?_without_patchedkernel:%patch9 -p1}
#%{?with_patchedkernel:%patch10 -p1}
#%{?with_patchedkernel:%patch11 -p1}
%{?with_patchedkernel:%patch12 -p1}
%{?with_patchedkernel:%patch13 -p1}

chmod 755 extensions/.*-test*
%{__perl} -pi -e 's/\$\(HTML_HOWTOS\)//g; s/\$\(PSUS_HOWTOS\)//g' iptables-howtos/Makefile

%build
%{__make} depend 2> /dev/null || :
%{__make} CC="%{__cc}" \
	COPT_FLAGS="%{rpmcflags} -D%{!?debug:N}DEBUG" \
	LIBDIR="%{_libdir}" \
	LDLIBS="-ldl" \
	all experimental

%{?with_howto:%{__make} -C iptables-howtos}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/iptables,%{_mandir}/man3,%{_initrddir}}

echo ".so iptables-save.8" > ip6tables-save.8
echo ".so iptables-restore.8" > ip6tables-restore.8

%{__make} install install-experimental \
	DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_libdir}

echo ".so iptables.8" > $RPM_BUILD_ROOT%{_mandir}/man8/ip6tables.8

# Devel stuff
cp -a include/* $RPM_BUILD_ROOT%{_includedir}/iptables
install lib*/lib*.a $RPM_BUILD_ROOT%{_libdir}
install libipq/*.3 $RPM_BUILD_ROOT%{_mandir}/man3

%{?with_patchedkernel:install ippool/lib*.a $RPM_BUILD_ROOT%{_libdir}}
%{?with_patchedkernel:install ippool/ippool $RPM_BUILD_ROOT%{_sbindir}}

install %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/iptables

%clean
rm -rf $RPM_BUILD_ROOT

%post init
/sbin/chkconfig --add %{name}

%preun init
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc %{?with_howto:iptables-howtos/{NAT,networking-concepts,packet-filtering}-HOWTO*}
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/iptables
%attr(755,root,root) %{_libdir}/iptables/*.so
%{_mandir}/man8/*

%files devel
%defattr(644,root,root,755)
%{?with_howto:%doc iptables-howtos/netfilter-hacking-HOWTO*}
%{_libdir}/lib*.a
%{_includedir}/iptables
%{_mandir}/man3/*

%files init
%defattr(644,root,root,755)
%attr(755,root,root) %{_initrddir}/iptables
