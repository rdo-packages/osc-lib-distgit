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
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools
BuildRequires:  git
BuildRequires:  python2-oslo-i18n
BuildRequires:  python2-keystoneauth1
BuildRequires:  python2-mock
BuildRequires:  python2-fixtures
BuildRequires:  python2-oslotest
BuildRequires:  python2-reno
BuildRequires:  python2-os-testr
BuildRequires:  python2-testtools
BuildRequires:  python2-osprofiler
BuildRequires:  python2-oslo-utils
BuildRequires:  python2-os-client-config
BuildRequires:  python2-openstacksdk
BuildRequires:  python2-requests
BuildRequires:  python2-stevedore
%if 0%{?fedora} > 0
BuildRequires:  python2-cliff
BuildRequires:  python2-simplejson
BuildRequires:  python2-testrepository
BuildRequires:  python2-requests-mock
%else
BuildRequires:  python-cliff
BuildRequires:  python-simplejson
BuildRequires:  python-testrepository
BuildRequires:  python-requests-mock
%endif

Requires:   python2-six >= 1.10.0
Requires:   python2-pbr >= 2.0.0
Requires:   python2-keystoneauth1 >= 3.3.0
Requires:   python2-openstacksdk >= 0.9.19
Requires:   python2-os-client-config >= 1.28.0
Requires:   python2-oslo-i18n >= 3.15.3
Requires:   python2-oslo-utils >= 3.33.0
Requires:   python2-stevedore >= 1.20.0
%if 0%{?fedora} > 0
Requires:   python2-cliff >= 2.8.0
Requires:   python2-simplejson >= 3.5.1
%else
Requires:   python-cliff >= 2.8.0
Requires:   python-simplejson >= 3.5.1
%endif

%description -n python2-%{library}
%{common_desc}

%package -n python2-%{library}-tests
Summary:    OpenStack osc-lib library tests
%{?python_provide:%python_provide python2-%{library}-tests}
Requires:   python2-%{library} = %{version}-%{release}
Requires:   python2-fixtures
Requires:   python2-mock
Requires:   python2-oslotest
Requires:   python2-os-testr
Requires:   python2-testtools
Requires:   python2-osprofiler
%if 0%{?fedora} > 0
Requires:   python2-requests-mock
Requires:   python2-testrepository
%else
Requires:   python-requests-mock
Requires:   python-testrepository
%endif

%description -n python2-%{library}-tests
%{common_desc}

This package contains the osc-lib library test files.


%package -n python-%{library}-doc
Summary:    OpenStack osc-lib library documentation

BuildRequires: python2-sphinx
BuildRequires: python2-openstackdocstheme
BuildRequires: python2-sphinxcontrib-apidoc

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
BuildRequires:  python3-openstacksdk
BuildRequires:  python3-requests
BuildRequires:  python3-simplejson
BuildRequires:  python3-stevedore


Requires:   python3-six >= 1.10.0
Requires:   python3-pbr >= 2.0.0
Requires:   python3-cliff >= 2.8.0
Requires:   python3-keystoneauth1 >= 3.3.0
Requires:   python3-os-client-config >= 1.28.0
Requires:   python3-oslo-i18n >= 3.15.3
Requires:   python3-oslo-utils >= 3.33.0
Requires:   python3-simplejson >= 3.5.1
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
Requires:   python3-openstacksdk >= 0.9.19


%description -n python3-%{library}-tests
%{common_desc}

This package contains the osc-lib library test files.

%endif # with_python3


%description
%{common_desc}


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
export PYTHONPATH=.
sphinx-build -b html doc/source doc/build/html
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
