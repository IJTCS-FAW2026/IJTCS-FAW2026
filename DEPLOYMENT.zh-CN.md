# IJTCS-FAW 2026 网站部署说明

本目录是一个无依赖的 GitHub Pages 静态网站初稿。直接上传到 GitHub 仓库根目录即可部署，不需要 Node、Python、Jekyll 或数据库。

## 推荐部署方式

### 方案 A：使用 IJTCS-FAW 组织账号

若能够取得 `ijtcs-faw` GitHub 组织权限，建议新建仓库：

```text
2026
```

然后将本目录内所有文件上传到仓库根目录。在 GitHub 中进入：

```text
Settings -> Pages -> Build and deployment -> Deploy from a branch
```

选择：

```text
Branch: main
Folder: /root
```

部署后网址通常为：

```text
https://ijtcs-faw.github.io/2026/
```

### 方案 B：先放在个人或课题组账号下

若暂时没有官方组织权限，可先新建仓库，例如：

```text
ijtcs-faw-2026
```

同样启用 GitHub Pages。部署后临时网址通常为：

```text
https://<用户名>.github.io/ijtcs-faw-2026/
```

等内容确认后，再迁移到正式账号。

## 正式发布前必须修改

当前版本是初稿，默认禁止搜索引擎收录。正式发布前需要做以下修改：

1. 删除各 HTML 文件顶部的草稿提示条：

```html
<div class="draft-ribbon">Draft website · Information marked TBA must be confirmed before public launch</div>
```

2. 删除或修改每个 HTML 文件里的 noindex 元信息：

```html
<meta name="robots" content="noindex, nofollow">
```

3. 将 `robots.txt` 改为：

```text
User-agent: *
Allow: /
```

4. 替换所有 `TBA` 占位符。
5. 确认会议日期、投稿系统、组委会名单、注册费、会场、出版安排、邀请报告人。
6. 官方 logo 和赞助机构 logo 只有在获得确认后再放入网站。

## 修改页面的方法

主要页面文件如下：

```text
index.html              主页
cfp.html                Call for Papers
submission.html         投稿说明
committees.html         组委会
program.html            会议日程
keynotes.html           邀请报告
registration.html       注册信息
attending.html          会场、交通、住宿、签证
accepted-papers.html    录用论文
previous.html           历届会议
contact.html            联系方式
```

样式文件为：

```text
assets/css/style.css
```

移动端菜单脚本为：

```text
assets/js/main.js
```

图片放在：

```text
assets/img/
```

PDF、会议手册、CFP 文件等下载材料放在：

```text
assets/files/
```
