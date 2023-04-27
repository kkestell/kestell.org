---
title: "Virtual Environments and Packages"
description: ""
date: 2021-11-27
draft: false
---

## Virtual Environments

Create a virtual environment

```
python -m venv myenv
```

Activate a virtual environment

```
source myenv/bin/activate
```

Deactivate a virtual environment

```
deactivate
```

## `pip`

Install a package

```
pip install <package_name>
```

List installed packages

```
pip list
```

Uninstall a package

```
pip uninstall <package_name>
```

Upgrade a package

```
pip install --upgrade <package_name>
```

Freeze installed packages to a requirements file

```
pip freeze > requirements.txt
```

Install packages from a requirements file

```
pip install -r requirements.txt
```

Upgrade pip

```
pip install --upgrade pip
```
