# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global library osc-lib
%global module osc_lib

%global common_desc osc-lib is a package of common support modules for writing OSC plugins.
%global with_doc 1

Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    OpenStack library for writing OSC plugins
License:    ASL 2.0
URL:        https://github.com/openstack/%{library}/

Source0:    https://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz

BuildArch:  noarch

%package -n python%{pyver}-%{library}
Summary:    OpenStack library for writing OSC plugins
%{?python_provide:%python_provide python%{pyver}-%{library}}
%if %{pyver} == 3
Obsoletes: python2-%{library} < %{version}-%{release}
%endif

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  git
BuildRequires:  python%{pyver}-oslo-i18n
BuildRequires:  python%{pyver}-keystoneauth1
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-fixtures
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-os-testr
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-oslo-utils
BuildRequires:  python%{pyver}-os-client-config
BuildRequires:  python%{pyver}-openstacksdk
BuildRequires:  python%{pyver}-requests
BuildRequires:  python%{pyver}-stevedore
BuildRequires:  python%{pyver}-cliff
BuildRequires:  python%{pyver}-testrepository
BuildRequires:  python%{pyver}-requests-mock
BuildRequires:  python%{pyver}-simplejson

Requires:   python%{pyver}-six >= 1.10.0
Requires:   python%{pyver}-pbr >= 2.0.0
Requires:   python%{pyver}-keystoneauth1 >= 3.7.0
Requires:   python%{pyver}-openstacksdk >= 0.15.0
Requires:   python%{pyver}-os-client-config >= 1.28.0
Requires:   python%{pyver}-oslo-i18n >= 3.15.3
Requires:   python%{pyver}-oslo-utils >= 3.33.0
Requires:   python%{pyver}-stevedore >= 1.20.0
Requires:   python%{pyver}-cliff >= 2.8.0
Requires:   python%{pyver}-simplejson >= 3.5.1

%description -n python%{pyver}-%{library}
%{common_desc}

%package -n python%{pyver}-%{library}-tests
Summary:    OpenStack osc-lib library tests
%{?python_provide:%python_provide python%{pyver}-%{library}-tests}
%if %{pyver} == 3
Obsoletes: python2-%{library} < %{version}-%{release}-tests
%endif

Requires:   python%{pyver}-%{library} = %{version}-%{release}
Requires:   python%{pyver}-fixtures
Requires:   python%{pyver}-mock
Requires:   python%{pyver}-oslotest
Requires:   python%{pyver}-os-testr
Requires:   python%{pyver}-testtools
Requires:   python%{pyver}-requests-mock
Requires:   python%{pyver}-testrepository

%description -n python%{pyver}-%{library}-tests
%{common_desc}

This package contains the osc-lib library test files.

%if 0%{?with_doc}
%package -n python%{pyver}-%{library}-doc
Summary:    OpenStack osc-lib library documentation
%{?python_provide:%python_provide python%{pyver}-%{library}-doc}

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-openstackdocstheme
BuildRequires: python%{pyver}-sphinxcontrib-apidoc

%description -n python%{pyver}-%{library}-doc
%{common_desc}

This package contains the documentation.
%endif

%description
%{common_desc}


%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
sphinx-build-%{pyver} -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

%check
PYTHON=python%{pyver} %{pyver_bin} setup.py test

%files -n python%{pyver}-%{library}
%license LICENSE
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/%{module}-*.egg-info
%exclude %{pyver_sitelib}/%{module}/tests

%files -n python%{pyver}-%{library}-tests
%license LICENSE
%{pyver_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files -n python%{pyver}-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog
