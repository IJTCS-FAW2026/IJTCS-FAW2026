# IJTCS-FAW 2026 网站部署说明

本仓库是 IJTCS-FAW 2026 正式静态网站，无需 Node、Python、Jekyll 或数据库构建。

## 当前部署

- 仓库：`IJTCS-FAW2026/IJTCS-FAW2026`
- 分支：`main`
- 发布目录：仓库根目录
- 网站：<https://ijtcs-faw2026.github.io/IJTCS-FAW2026/>

## 搜索引擎收录

正式页面已设置 `index, follow` 和 canonical 地址；`robots.txt` 允许抓取并指向 `sitemap.xml`。`404.html` 保留 `noindex, follow`，避免错误页面进入索引。

## 内容维护

未公布项目统一显示为 `TBA`。信息确认后，应同时更新所有相关页面，并检查：

1. 日期和委员会名单是否在各页一致；
2. 投稿、注册和外部链接是否有效；
3. 图片来源及使用说明是否记录在 `assets/img/IMAGE-CREDITS.md`；
4. HTML 本地资源链接是否存在；
5. `sitemap.xml` 是否包含新增的公开页面。

## 主要文件

```text
index.html              主页与 Overview
cfp.html                Call for Papers 与 Tracks
tutorials.html          Call for Tutorials 与教程提案说明
submission.html         投稿说明
committees.html         委员会
program.html            会议日程
keynotes.html           邀请报告
registration.html       注册信息
attending.html          会场、交通、住宿、签证
accepted-papers.html    录用论文
special-issue.html      Special Issue
previous.html           历届会议
support.html            支持机构
contact.html            联系方式
assets/css/style.css    全站样式
assets/js/main.js       移动端菜单
assets/img/             图片资源
```
