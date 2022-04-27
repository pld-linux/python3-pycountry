#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	ISO country, subdivision, language, currency and script definitions and their translations
Summary(pl.UTF-8):	Definicje ISO dla krajów, podziału, języków, walut i pisma wraz z tłumaczeniami
Name:		python3-pycountry
Version:	22.3.5
Release:	1
License:	LGPL v2.1
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pycountry/
Source0:	https://files.pythonhosted.org/packages/source/p/pycountry/pycountry-%{version}.tar.gz
# Source0-md5:	47a8668fc5d86fcd2c608c19846e2912
URL:		https://pypi.org/project/pycountry/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.6
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

%build
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest src/pycountry/tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/pycountry/tests

find $RPM_BUILD_ROOT%{py3_sitescriptdir}/pycountry/locales -type d -maxdepth 1 | \
	%{__sed} -ne "s,$RPM_BUILD_ROOT\(.*locales/\([a-z]\+\(_[A-Z][A-Z]\)\?\).*\),%%lang(\2) \1,p" > py3.lang

%clean
rm -rf $RPM_BUILD_ROOT

%files -f py3.lang
%defattr(644,root,root,755)
%doc HISTORY.txt README.rst TODO.txt
%dir %{py3_sitescriptdir}/pycountry
%{py3_sitescriptdir}/pycountry/*.py
%{py3_sitescriptdir}/pycountry/__pycache__
%{py3_sitescriptdir}/pycountry/databases
%dir %{py3_sitescriptdir}/pycountry/locales
%{py3_sitescriptdir}/pycountry-%{version}-py*.egg-info
