# MAKERTHON_2024

## 2024 全國大賽初賽

欢迎来到 2024 全国大赛项目！本项目结合了多种技术，包括 SwiftUI 应用程序、Arduino ESP8266、Python Django 服务器、相机模块，以及使用 Makefile 进行自动化管理。

## 项目结构

```plaintext
project/
├── arduino/                # Arduino ESP8266 相关代码
│   └── esp8266_code.ino
├── backend/                # Python Django 服务器相关代码
│   ├── manage.py
│   ├── backend/
│   │   └── settings.py
│   │   └── urls.py
│   │   └── wsgi.py
│   ├── app/
│   │   └── models.py
│   │   └── views.py
│   │   └── urls.py
│   └── ...
├── ios_app/                # SwiftUI 应用程序相关代码
│   ├── ContentView.swift
│   └── ...
├── camera/                 # 相机模块相关代码
│   └── camera_code.py
├── Makefile                # Makefile 脚本
└── README.md               # 项目说明文档
```
