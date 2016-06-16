%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif


%global library osc-lib
%global module osc_lib

Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    OpenStack library for writing OSC plugins
License:    ASL 2.0
URL:        https://github.com/openstack/%{library}/

Source0:    http://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz

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
BuildRequires:  python-coverage
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-oslotest
BuildRequires:  python-reno
BuildRequires:  python-requests-mock
BuildRequires:  python-os-testr
BuildRequires:  python-testtools
BuildRequires:  python-osprofiler
BuildRequires:  python-oslo-utils
BuildRequires:  bandit
BuildRequires:  python-os-client-config
BuildRequires:  python-requests
BuildRequires:  python-simplejson
BuildRequires:  python-stevedore
BuildRequires:  python-backports-ssl_match_hostname

Requires:   python-oslo-config >= 2:3.4.0
Requires:   python-six >= 1.9.0
Requires:   python-pbr >= 1.6.0
Requires:   python-cliff >= 1.15.0
Requires:   python-keystoneauth1 >= 2.1.0
Requires:   python-os-client-config >= 1.13.1
Requires:   python-oslo-i18n >= 2.1.0
Requires:   python-oslo-utils >= 3.11.0
Requires:   python-requests >= 2.10.0
Requires:   python-simplejson >= 2.2.0
Requires:   python-stevedore >= 1.10.0
Requires:   python-backports-ssl_match_hostname

%description -n python2-%{library}
osc-lib is a package of common support modules for writing OSC plugins.


%package -n python2-%{library}-tests
Summary:    OpenStack osc-lib library tests
Requires:   python2-%{library} = %{version}-%{release}

%description -n python2-%{library}-tests
osc-lib is a package of common support modules for writing OSC plugins.

This package contains the osc-lib library test files.


%package -n python-%{library}-doc
Summary:    OpenStack osc-lib library documentation

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx

%description -n python-%{library}-doc
osc-lib is a package of common support modules for writing OSC plugins.

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
BuildRequires:  python3-coverage
BuildRequires:  python3-oslo-sphinx
BuildRequires:  python3-oslotest
BuildRequires:  python3-reno
BuildRequires:  python3-requests-mock
BuildRequires:  python3-os-testr
BuildRequires:  python3-testtools
BuildRequires:  python3-oslo-utils
BuildRequires:  bandit
BuildRequires:  python3-os-client-config
BuildRequires:  python3-requests
BuildRequires:  python3-simplejson
BuildRequires:  python3-stevedore


Requires:   python3-oslo-config >= 2:3.4.0
Requires:   python3-six >= 1.9.0
Requires:   python3-pbr >= 1.6.0
Requires:   python3-cliff >= 1.15.0
Requires:   python3-keystoneauth1 >= 2.1.0
Requires:   python3-os-client-config >= 1.13.1
Requires:   python3-oslo-i18n >= 2.1.0
Requires:   python3-oslo-utils >= 3.11.0
Requires:   python3-requests >= 2.10.0
Requires:   python3-simplejson >= 2.2.0
Requires:   python3-stevedore >= 1.10.0


%description -n python3-%{library}
osc-lib is a package of common support modules for writing OSC plugins.

%package -n python3-%{library}-tests
Summary:    OpenStack osc-lib library tests
Requires:   python3-%{library} = %{version}-%{release}

%description -n python3-%{library}-tests
osc-lib is a package of common support modules for writing OSC plugins.

This package contains the osc-lib library test files.

%endif # with_python3


%description
osc-lib is a package of common support modules for writing OSC plugins.


%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

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
%doc html README.rst

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
