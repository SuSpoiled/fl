修改自用

## 使用方法（推荐）

进入路由器 SSH，执行以下命令之一，把更新脚本中的 `URL_MAIN` 指向本仓库规则目录：

**方案 A：直连 GitHub（推荐）**

```sh
sed -i 's/^URL_MAIN.*/URL_MAIN="https:\/\/raw.githubusercontent.com\/suspoiled\/fl\/3.0\/fancyss_rules_ng"/g' /koolshare/scripts/ss_rule_update.sh
```
