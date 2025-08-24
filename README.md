[![Update Fancyss Rules](https://github.com/suspoiled/fl/actions/workflows/fancyss-rules-3.0.yml/badge.svg)](https://github.com/suspoiled/fl/actions/workflows/fancyss-rules-3.0.yml)
---   
#### 每日UTC+8 3:45时自动更新规则，推荐在插件中设置每天4:00定时更新  
---
### 食用方法：
- 进入路由器SSH，运行以下命令会自动将`ss_rule_update`脚本中的`url_main`参数指向我的仓库（二选一即可）：
- `sed -i 's/^URL_MAIN.*/URL_MAIN="https:\/\/raw.githubusercontent.com\/suspoiled\/fl\/3.0\/fancyss_rules"/g' /koolshare/scripts/ss_rule_update.sh` 
- > x86版本fancyss插件请自行找到更新规则的脚本并替换`url_main`参数
### 每次fancyss插件更新后都需要\*重新运行一次\*更新`ss_rule_update`脚本的命令

