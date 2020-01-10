Name:		libfastjson
Version:	0.99.4
Release:	2%{?dist}
Summary:	A JSON implementation in C
License:	MIT
URL:		https://github.com/rsyslog/libfastjson
Source0:	http://download.rsyslog.com/libfastjson/libfastjson-%{version}.tar.gz

# 1421612 - New defect found in libfastjson-0.99.4-1.el7
Patch0: libfastjson-0.99.4-rhbz1421612-nullptr-guard.patch

%description
LIBFASTJSON implements a reference counting object
model that allows you to easily construct JSON
objects in C, output them as JSON formatted strings
and parse JSON formatted strings back into the
C representation of JSON objects.

%package	devel
Summary:	Development files for libfastjson
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
This package contains libraries and header files for
developing applications that use libfastjson.

%prep
%setup -q
%patch0 -p1

for doc in ChangeLog; do
 iconv -f iso-8859-1 -t utf8 $doc > $doc.new &&
 touch -r $doc $doc.new &&
 mv $doc.new $doc
done

%build
export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE" # temporary workaround for EPEL5, fixed upstream
%configure --enable-shared --disable-static

%install
make V=1 DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete -print

%check
make V=1 check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS ChangeLog README.html
%{_libdir}/libfastjson.so.*

%files devel
%{_includedir}/libfastjson
%{_libdir}/libfastjson.so
%{_libdir}/pkgconfig/libfastjson.pc

%changelog
* Tue Mar 07 2017 Daniel Kopecek <dkopecek@redhat.com> - 0.99.4-2
- Fix defect found by clang-analyzer
  Resolves: #1421612

* Tue Jan 24 2017 Daniel Kopecek <dkopecek@redhat.com> - 0.99.4-1
- Import
  Resolves: #1395145
