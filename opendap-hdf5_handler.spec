#
# Conditional build:
%bcond_with	tests	# make check (requires BES server)
#
Summary:	HDF5 data handler module for the OPeNDAP data server
Summary(pl.UTF-8):	Moduł obsługujący dane HDF5 dla serwera danych OPeNDAP
Name:		opendap-hdf5_handler
Version:	2.2.1
Release:	1
License:	LGPL v2.1+
Group:		Daemons
Source0:	http://www.opendap.org/pub/source/hdf5_handler-%{version}.tar.gz
# Source0-md5:	d20371b73401244c2c65c3c27fbf53fe
URL:		http://opendap.org/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.10
%{?with_tests:BuildRequires:	bes >= 3.9.0}
BuildRequires:	bes-devel >= 3.9.0
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	hdf5-devel >= 1.6
BuildRequires:	libdap-devel >= 3.11.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
Requires:	bes >= 3.9.0
Requires:	hdf5 >= 1.6
Requires:	libdap >= 3.11.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the HDF5 data handler module for the OPeNDAP data server. It
reads HDF5 files and returns DAP responses that are compatible with
DAP2 and the dap-server software.

%description -l pl.UTF-8
Ten pakiet zawiera moduł obsługujący dane HDF5 dla serwera danych
OPeNDAP. Odczytuje pliki HDF5 i zwraca odpowiedzi DAP zgodne z
oprogramowaniem DAP2 i dap-server.

%prep
%setup -q -n hdf5_handler-%{version}

# don't use -L/usr/lib for hdfeos2
%{__sed} -i -e '/LDFLAGS.*HDFEOS2_DIR/d' configure.ac

%build
# rebuild autotools for -as-needed to work
%{__libtoolize}
%{__aclocal} -I conf
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-cache-dir=/var/cache/bes \
	--with-hdfeos2=/usr
%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/bes/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bes/modules/h5.conf
%attr(755,root,root) %{_libdir}/bes/libhdf5_module.so
%dir %{_datadir}/hyrax/data/hdf5
%{_datadir}/hyrax/data/hdf5/*.h5
