#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	ISO country, subdivision, language, currency and script definitions and their translations
Summary(pl.UTF-8):	Definicje ISO dla krajów, podziału, języków, walut i pisma wraz z tłumaczeniami
Name:		python3-pycountry
Version:	24.6.1
Release:	1
License:	LGPL v2.1
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pycountry/
Source0:	https://files.pythonhosted.org/packages/source/p/pycountry/pycountry-%{version}.tar.gz
# Source0-md5:	61111cc27f09e44aa3bace260a8b3089
URL:		https://pypi.org/project/pycountry/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-poetry-core >= 1.0.0
%if %{with tests}
%if "%{py3_ver}" == "3.8"
BuildRequires:	python3-importlib_resources >= 5.12.1
%endif
BuildRequires:	python3-pytest >= 7.1.4
BuildRequires:	python3-pytest-cov >= 4.0.1
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
BuildRequires:	sed >= 4.0
Requires:	python3-modules >= 1:3.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ISO country, subdivision, language, currency and script definitions
and their translations.

%description -l pl.UTF-8
Definicje ISO dla krajów, podziału, języków, walut i pisma wraz z
tłumaczeniami.

%prep
%setup -q -n pycountry-%{version}

# required-plugins fails with PYTEST_DISABLE_PLUGIN_AUTOLOAD
%{__sed} -i -e 's/^required_plugins/#\&/' pyproject.toml

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_cov.plugin \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest src/pycountry/tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/pycountry/tests
# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/pycountry/COPYRIGHT.txt

find $RPM_BUILD_ROOT%{py3_sitescriptdir}/pycountry/locales -type d -maxdepth 1 | \
	%{__sed} -ne "s,$RPM_BUILD_ROOT\(.*locales/\([a-z]\+\(_[A-Z][A-Z]\)\?\).*\),%%lang(\2) \1,p" > py3.lang

# unify lang tags for zh_Hans and zh_Hant
%{__sed} -i -e '/zh_Hans/ s/lang(zh)/lang(zh_CN)/' -e '/zh_Hant/ s/lang(zh)/lang(zh_TW)/' py3.lang

%clean
rm -rf $RPM_BUILD_ROOT

%files -f py3.lang
%defattr(644,root,root,755)
%doc README.rst src/pycountry/COPYRIGHT.txt
%dir %{py3_sitescriptdir}/pycountry
%{py3_sitescriptdir}/pycountry/*.py
%{py3_sitescriptdir}/pycountry/py.typed
%{py3_sitescriptdir}/pycountry/__pycache__
%{py3_sitescriptdir}/pycountry/databases
%dir %{py3_sitescriptdir}/pycountry/locales
%{py3_sitescriptdir}/pycountry-%{version}.dist-info
