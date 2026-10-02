# 02｜Windows 搭建步骤

## 1. 准备工具

从官方渠道获取 [Codex](https://developers.openai.com/codex/app/)、[Python](https://www.python.org/downloads/windows/)、[Git for Windows](https://git-scm.com/downloads/win) 和 [Obsidian](https://obsidian.md/download)。完成登录，核对工具版本与程序所需依赖。

本版不分发安装脚本。不要运行来源不明的初始化器，也不要把旧电脑的登录文件上传或复制到公开仓库。

## 2. 获取检索程序

阅读 [DSH-KRouter](https://github.com/398894496-arch/DSH-KRouter) 当前安装说明、平台支持和许可证。记录自己实际采用的版本。在新目录安装，先检查是否会写入全局配置或覆盖现有文件。

上游说明如依赖 Bash 或 cron，Windows 原生环境须选择明确支持的运行方式或自行验证适配；不能把旧环境的成功直接视为新环境兼容。本阅读版不提供已验收的 Windows 一键安装器。

## 3. 创建或恢复知识库

选择自己的存储位置，使用非敏感测试资料建立示例。首次搭建与恢复旧知识是两项工作；已有数据先备份，不覆盖。使用者自行维护其组织方式与检索配置。

## 4. 配置工作方法

按当前官方文档安装自己授权的 Skills，并合并工作规则。保留现有配置；遇到同名但内容不同的文件先比较。公开插件见 [插件与扩展](10-plugin-and-integrations.md)。

## 5. 先验收，再启用自动整理

核对登录、检索命中、来源可访问和输出正确性，再设置自动任务。注册前确认运行身份、时间、写入范围和额度。最后按 [验收清单](06-acceptance.md) 检查真实产物。
