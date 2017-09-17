%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif


%global library osc-lib
%global module osc_lib

%global common_desc osc-lib is a package of common support modules for writing OSC plugins.

Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    OpenStack library for writing OSC plugins
License:    ASL 2.0
URL:        https://github.com/openstack/%{library}/

Source0:    https://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz

BuildArch:  noarch

%package -n python2-%{library}
Summary:    OpenStack library for writing OSC plugins
%{?python_provide:%python_provide python2-%{library}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git
BuildRequires:  python-testrepository
BuildRequires:  python-oslo-i18n
BuildRequires:  python-keystoneauth1
BuildRequires:  python-cliff
BuildRequires:  python-mock
BuildRequires:  python-fixtures
BuildRequires:  python-oslotest
BuildRequires:  python-reno
BuildRequires:  python-requests-mock
BuildRequires:  python-os-testr
BuildRequires:  python-testtools
BuildRequires:  python-osprofiler
BuildRequires:  python-oslo-utils
BuildRequires:  python-os-client-config
BuildRequires:  python-requests
BuildRequires:  python-simplejson
BuildRequires:  python-stevedore

Requires:   python-six >= 1.9.0
Requires:   python-pbr >= 2.0.0
Requires:   python-cliff >= 2.8.0
Requires:   python-keystoneauth1 >= 3.1.0
Requires:   python-os-client-config >= 1.28.0
Requires:   python-oslo-i18n >= 2.1.0
Requires:   python-oslo-utils >= 3.20.0
Requires:   python-simplejson >= 2.2.0
Requires:   python-stevedore >= 1.20.0

%description -n python2-%{library}
%{common_desc}

%package -n python2-%{library}-tests
Summary:    OpenStack osc-lib library tests
%{?python_provide:%python_provide python2-%{library}-tests}
Requires:   python2-%{library} = %{version}-%{release}
Requires:   python-fixtures
Requires:   python-mock
Requires:   python-oslotest
Requires:   python-requests-mock
Requires:   python-os-testr
Requires:   python-testrepository
Requires:   python-testtools
Requires:   python-osprofiler

%description -n python2-%{library}-tests
%{common_desc}

This package contains the osc-lib library test files.


%package -n python-%{library}-doc
Summary:    OpenStack osc-lib library documentation

BuildRequires: python-sphinx
BuildRequires: python-openstackdocstheme

%description -n python-%{library}-doc
%{common_desc}

This package contains the documentation.

%if 0%{?with_python3}
%package -n python3-%{library}
Summary:    OpenStack Example library
%{?python_provide:%python_provide python3-%{library}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  git
BuildRequires:  python3-testrepository
BuildRequires:  python3-oslo-i18n
BuildRequires:  python3-keystoneauth1
BuildRequires:  python3-cliff
BuildRequires:  python3-mock
BuildRequires:  python3-fixtures
BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-oslotest
BuildRequires:  python3-reno
BuildRequires:  python3-requests-mock
BuildRequires:  python3-os-testr
BuildRequires:  python3-testtools
BuildRequires:  python3-oslo-utils
BuildRequires:  python3-os-client-config
BuildRequires:  python3-requests
BuildRequires:  python3-simplejson
BuildRequires:  python3-stevedore
BuildRequires:  openstack-macros

Requires:   python3-six >= 1.9.0
Requires:   python3-pbr >= 2.0.0
Requires:   python3-cliff >= 2.8.0
Requires:   python3-keystoneauth1 >= 3.1.0
Requires:   python3-os-client-config >= 1.28.0
Requires:   python3-oslo-i18n >= 2.1.0
Requires:   python3-oslo-utils >= 3.20.0
Requires:   python3-simplejson >= 2.2.0
Requires:   python3-stevedore >= 1.20.0


%description -n python3-%{library}
%{common_desc}

%package -n python3-%{library}-tests
Summary:    OpenStack osc-lib library tests
%{?python_provide:%python_provide python3-%{library}-tests}
Requires:   python3-%{library} = %{version}-%{release}
Requires:   python3-fixtures
Requires:   python3-mock
Requires:   python3-oslotest
Requires:   python3-requests-mock
Requires:   python3-os-testr
Requires:   python3-testrepository
Requires:   python3-testtools
Requires:   python3-osprofiler


%description -n python3-%{library}-tests
%{common_desc}

This package contains the osc-lib library test files.

%endif # with_python3


%description
%{common_desc}


%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

%check
%if 0%{?with_python3}
%{__python3} setup.py test
rm -rf .testrepository
%endif
%{__python2} setup.py test

%files -n python2-%{library}
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/%{module}-*.egg-info
%exclude %{python2_sitelib}/%{module}/tests

%files -n python2-%{library}-tests
%license LICENSE
%{python2_sitelib}/%{module}/tests

%files -n python-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst

%if 0%{?with_python3}
%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-*.egg-info
%exclude %{python3_sitelib}/%{module}/tests

%files -n python3-%{library}-tests
%license LICENSE
%{python3_sitelib}/%{module}/tests
%endif # with_python3

%changelog
