

# CarConnectivity WebUI by m7xlab

[![PyPI version](https://img.shields.io/pypi/v/carconnectivity-webui-by-m7xlab)](https://pypi.org/project/carconnectivity-webui-by-m7xlab/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/carconnectivity-webui-by-m7xlab?label=PyPI%20Downloads)](https://pypi.org/project/carconnectivity-webui-by-m7xlab/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/carconnectivity-webui-by-m7xlab)](https://pypi.org/project/carconnectivity-webui-by-m7xlab/)
[![GitHub](https://img.shields.io/github/license/m7xlab/CarConnectivity-plugin-webui)](https://github.com/m7xlab/CarConnectivity-plugin-webui/blob/main/LICENSE)
[![Django](https://img.shields.io/badge/Django-5.0-green)](https://www.djangoproject.com/)

> Modern Django-based WebUI for CarConnectivity with Apple-inspired design

## About

This is a modern Django-based WebUI plugin for [CarConnectivity](https://github.com/tillsteinbach/CarConnectivity) - a Python API to connect to various car services. 

**Note**: This is an enhanced fork maintained by m7xlab, featuring a complete rewrite with Django framework and Apple-inspired design system.

### Original Project
Based on the original [CarConnectivity-plugin-webui](https://github.com/tillsteinbach/CarConnectivity-plugin-webui) by Till Steinbach.

## ✨ New: Modern Django-Based UI with Apple-Inspired Design

The WebUI has been completely redesigned with:
- **Modern Framework**: Migrated from Flask to Django 5.0
- **Apple-Inspired Design**: Clean, minimalist interface with glassmorphism effects
- **Dark Mode**: Full dark mode support with automatic detection
- **Responsive**: Mobile-first design that works on all devices
- **Smooth Animations**: 60fps transitions and micro-interactions
- **Modern Icons**: Heroicons SVG icon library
- **Better Performance**: Optimized static file serving with WhiteNoise
- **Enhanced Security**: Django's built-in security features

<img src="https://raw.githubusercontent.com/GedasKr/CarConnectivity-webui-by-m7xlab/main/screenshots/screenshot1.png" width="300">
<img src="https://raw.githubusercontent.com/GedasKr/CarConnectivity-webui-by-m7xlab/main/screenshots/screenshot2.png" width="300">
<img src="https://raw.githubusercontent.com/GedasKr/CarConnectivity-webui-by-m7xlab/main/screenshots/screenshot3.png" width="300">

## How to install

### Install using PIP
If you want to use CarConnectivity Web UI, the easiest way is to obtain it from [PyPI](https://pypi.org/project/carconnectivity-webui-by-m7xlab/). Just install using:
```bash
pip3 install carconnectivity-webui-by-m7xlab
```
after you installed CarConnectivity

### Install from Source (Development)
```bash
git clone https://github.com/tillsteinbach/CarConnectivity-plugin-webui.git
cd CarConnectivity-plugin-webui
pip3 install -e .
```

## Configuration
In your carconnectivity.json configuration add a section for the webui plugin like this. A documentation of all possible config options can be found [here](https://github.com/tillsteinbach/CarConnectivity-plugin-webui/tree/main/doc/Config.md).
```
{
    "carConnectivity": {
        "connectors": [
            ...
        ]
        "plugins": [
            {
                "type": "webui",
                "config": {
                    "username": "admin", // Admin username for login
                    "password": "secret" // Admin password for login
                }
            }
        ]
    }
}
```

## How to use
You will default find the webinterface on http port 4000 on the machine that is hosting carconnectivity. You can change interface with the `host` parameter and the port with the `port parameter`.
Always set your personal username and password to protect your data from theft.

## Updates
If you want to update, the easiest way is:
```bash
pip3 install carconnectivity-webui-by-m7xlab --upgrade
```

## Features

- 🎨 **Modern Design**: Apple-inspired UI with glassmorphism effects
- 🌓 **Dark Mode**: Automatic dark mode detection with manual toggle
- 📱 **Responsive**: Works perfectly on mobile, tablet, and desktop
- ⚡ **Fast**: Optimized performance with Django and WhiteNoise
- 🔒 **Secure**: Django's built-in security features
- ♿ **Accessible**: WCAG 2.1 AA compliant
- 🎭 **Smooth Animations**: 60fps transitions and micro-interactions
- 🎯 **Modern Icons**: Heroicons SVG icon library

## Logs

The **Log** page shows the **system log** of the CarConnectivity process that runs this WebUI.

- **Source**: Logs are not read from files or other services. The [CarConnectivity](https://github.com/tillsteinbach/CarConnectivity) core attaches an in-memory handler to Python’s `logging` module and appends `LogRecord` objects to a ring buffer. The WebUI reads that buffer and formats each record with a standard formatter (`%(asctime)s - %(name)s - %(levelname)s - %(message)s`). So you see **only logs from this process** (CarConnectivity + connectors + plugins in the same runtime).
- **Buffer size**: The UI shows only the **last N entries** in that buffer (N is defined in CarConnectivity core, often around a dozen). For a longer or full history, use **container logs** (e.g. `docker logs`, pod logs, or a log file if you redirect stdout/stderr to a file). Container logs capture everything the process writes to stdout/stderr—including the same Python log lines plus HTTP server access logs (e.g. Werkzeug), urllib3, and other libraries—so they are more complete and can look different from the UI.
- **Order**: The `?order=` query controls sort order on the log page:
  - `order=desc` (default): **Latest first** — most recent entries at the top.
  - `order=asc`: **Oldest first** — chronological order from the start of the buffer.
- **Other containers**: Logs from **other containers** (e.g. a separate database container, Grafana, or nginx) are **not** available here. To see those, use the container’s own logging (e.g. `docker logs`, Kubernetes logs, or Grafana’s log datasources).
