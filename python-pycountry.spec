#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	ISO country, subdivision, language, currency and script definitions and their translations
Summary(pl.UTF-8):	Definicje ISO dla krajów, podziału, języków, walut i pisma wraz z tłumaczeniami
Name:		python-pycountry
# keep 18.x here for python2 support
Version:	18.12.8
Release:	1
License:	LGPL v2.1
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pycountry/
Source0:	https://files.pythonhosted.org/packages/source/p/pycountry/pycountry-%{version}.tar.gz
# Source0-md5:	46223fa49c45c304083de7d5b1870fb7
URL:		https://pypi.org/project/pycountry/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ISO country, subdivision, language, currency and script definitions
and their translations.

%description -l pl.UTF-8
Definicje ISO dla krajów, podziału, języków, walut i pisma wraz z
tłumaczeniami.

%package -n python3-pycountry
Summary:	ISO country, subdivision, language, currency and script definitions and their translations
Summary(pl.UTF-8):	Definicje ISO dla krajów, podziału, języków, walut i pisma wraz z tłumaczeniami
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.3

%description -n python3-pycountry
ISO country, subdivision, language, currency and script definitions
and their translations.

%description -n python3-pycountry -l pl.UTF-8
Definicje ISO dla krajów, podziału, języków, walut i pisma wraz z
tłumaczeniami.

%prep
%setup -q -n pycountry-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
%{__python} -m pytest src/pycountry/tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest src/pycountry/tests
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/pycountry/tests
%py_postclean

find $RPM_BUILD_ROOT%{py_sitescriptdir}/pycountry/locales -type d -maxdepth 1 | \
	%{__sed} -ne "s,$RPM_BUILD_ROOT\(.*locales/\([a-z]\+\(_[A-Z][A-Z]\)\?\).*\),%%lang(\2) \1,p" > py2.lang
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/pycountry/tests

find $RPM_BUILD_ROOT%{py3_sitescriptdir}/pycountry/locales -type d -maxdepth 1 | \
	%{__sed} -ne "s,$RPM_BUILD_ROOT\(.*locales/\([a-z]\+\(_[A-Z][A-Z]\)\?\).*\),%%lang(\2) \1,p" > py3.lang
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files -f py2.lang
%defattr(644,root,root,755)
%doc HISTORY.txt README TODO.txt
%dir %{py_sitescriptdir}/pycountry
%{py_sitescriptdir}/pycountry/*.py[co]
%{py_sitescriptdir}/pycountry/databases
%dir %{py_sitescriptdir}/pycountry/locales
%{py_sitescriptdir}/pycountry-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-pycountry -f py3.lang
%defattr(644,root,root,755)
%doc HISTORY.txt README TODO.txt
%dir %{py3_sitescriptdir}/pycountry
%{py3_sitescriptdir}/pycountry/*.py
%{py3_sitescriptdir}/pycountry/__pycache__
%{py3_sitescriptdir}/pycountry/databases
%dir %{py3_sitescriptdir}/pycountry/locales
%{py3_sitescriptdir}/pycountry-%{version}-py*.egg-info
%endif
