%define oname AppImageLauncher
Name:           appimagelauncher
Version:        3.0.0
Release:        0.alpha.1
License:        MIT
Summary:        AppImage system intergation
URL:            https://github.com/TheAssassin/AppImageLauncher
Source:         https://github.com/TheAssassin/AppImageLauncher/archive/refs/tags/v3.0.0-alpha-1/%{oname}-3.0.0-alpha-1.tar.gz
BuildRequires:  automake
BuildRequires:  cmake
BuildRequires:  git
BuildRequires:  pkgconfig(libappimage)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(fuse3)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(xpm)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  boost-devel

%description
Integrate AppImages to your application launcher with one click, and manage, update and remove them from there. 
Double-click AppImages to open them, without having to make them executable first.

AppImageLauncher plays well with other applications managing AppImages, for example app stores. 
However, it doesn't depend on any of those, and can run completely standalone.

%prep
%autosetup -n %{oname}-3.0.0-alpha-1

%build
%cmake

%make_build

%install
%make_install -C build

%files
