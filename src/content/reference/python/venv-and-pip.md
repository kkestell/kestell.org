---
title: "Virtual Environments and Packages"
description: ""
date: 2021-11-27
draft: false
---

## Virtual Environments

Create a virtual environment

```console
$ python -m venv myenv
```

Activate a virtual environment

```console
$ source myenv/bin/activate
```

Deactivate a virtual environment

```console
$ deactivate
```

## `pip`

Install a package

```console
$ pip install <package_name>
```

List installed packages

```console
$ pip list
```

Uninstall a package

```console
$ pip uninstall <package_name>
```

Upgrade a package

```console
$ pip install --upgrade <package_name>
```

Freeze installed packages to a requirements file

```console
$ pip freeze > requirements.txt
```

Install packages from a requirements file

```console
$ pip install -r requirements.txt
```
