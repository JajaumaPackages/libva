Name:		libva
Version:	1.0.13
Release:	1%{?dist}
Summary:	Video Acceleration (VA) API for Linux
Group:		System Environment/Libraries
License:	MIT
URL:		http://freedesktop.org/wiki/Software/vaapi
# Tarball is modified to remove the i965 driver, which legal considers
# potentially problematic from a patent POV. Procedure to generate the
# modified tarball:
# 1. extract
# 2. remove all i965 references in configure.ac and Makefile.am
# 3. autoreconf -i
# 4. rm -rf i965_drv_video
# 5. re-tar
# original tarball at URL: http://cgit.freedesktop.org/libva/snapshot/libva-%{version}.tar.bz2
Source0:	libva-%{version}-mod.tar.bz2
# Use merged patch
Patch0:		libva-1.0.13-backport.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	libtool
BuildRequires:	libudev-devel
BuildRequires:	libXext-devel
BuildRequires:	libXfixes-devel
BuildRequires:	libdrm-devel
BuildRequires:	mesa-libGL-devel
# owns the %{_libdir}/dri directory
Requires:	mesa-dri-drivers

%description
Libva is a library providing the VA API video acceleration API.

%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package	utils
Summary:	Tools for %{name} (including vainfo)
Group:		Development/Libraries

%description	utils
The %{name}-utils package contains tools that are provided as part
of %{name}, including the vainfo tool for determining what (if any)
%{name} support is available on a system.

%prep
%setup -q -n %{name}-%{version}-mod
%patch0 -p1 -b .testprogs

%build
autoreconf -i
%configure --disable-static --enable-glx
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -regex ".*\.la$" | xargs rm -f --

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libva*.so.*
# Keep these specific: if any new real drivers start showing up
# in libva, we need to know about it so they can be patent-audited
%{_libdir}/dri/dummy_drv_video.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/va
%{_libdir}/libva*.so
%{_libdir}/pkgconfig/libva*.pc

%files utils
%defattr(-,root,root,-)
%{_bindir}/vainfo
%{_bindir}/avcenc
%{_bindir}/h264encode
%{_bindir}/mpeg2vldemo
%{_bindir}/putsurface

%changelog
* Wed Jun 08 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.13-1
- Update to 1.0.13

* Fri Apr 08 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.12-1
- Update to 1.0.12

* Mon Feb 21 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.10-1
- Update to 1.0.10

* Tue Jan 25 2011 Adam Williamson <awilliam@redhat.com> - 1.0.8-1
- bump to new version
- fix modded tarball to actually not have i965 dir
- merge with the other spec I seem to have lying around somewhere

* Wed Nov 24 2010 Adam Williamson <awilliam@redhat.com> - 1.0.6-1
- switch to upstream from sds branch (sds now isn't carrying any very
  interesting changes according to gwenole)
- pull in the dont-install-test-programs patch from sds
- split out libva-utils again for multilib purposes
- drop -devel package obsolete/provides itself too

* Tue Nov 23 2010 Adam Williamson <awilliam@redhat.com> - 0.31.1-3.sds4
- drop obsoletes and provides of itself (hangover from freeworld)

* Tue Nov 23 2010 Adam Williamson <awilliam@redhat.com> - 0.31.1-2.sds4
- fix the tarball to actually remove the i965 code (duh)

* Thu Oct 7 2010 Adam Williamson <awilliam@redhat.com> - 0.31.1-1.sds4
- initial package (based on package from elsewhere by myself and Nic
  Chauvet with i965 driver removed)
