---
title: Python Virtual Environments and Packages
date: 2021-11-27
draft: false
---

## Virtual Environments

Create a virtual environment

```shell
python -m venv myenv
```

Activate a virtual environment

```shell
source myenv/bin/activate
```

Deactivate a virtual environment

```shell
deactivate
```

## `pip`

Install a package

```shell
pip install <package_name>
```

List installed packages

```shell
pip list
```

Uninstall a package

```shell
pip uninstall <package_name>
```

Upgrade a package

```shell
pip install --upgrade <package_name>
```

Freeze installed packages to a requirements file

```shell
pip freeze > requirements.txt
```

Install packages from a requirements file

```shell
pip install -r requirements.txt
```

Upgrade pip

```shell
pip install --upgrade pip
```
