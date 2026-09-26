# Backend Code Style

## 参考规范

- PEP 8
- Google Python Style Guide

## 命名

- 模块与函数：`snake_case`
- 类：`PascalCase`
- 常量：`UPPER_SNAKE_CASE`
- 私有辅助函数：单下划线前缀

## 代码组织

- controller 只处理 HTTP 请求与响应
- service 负责业务逻辑
- repository 负责数据库访问
- schema 负责请求与响应模型
- model 负责数据库表结构

## 规则

- 禁止使用 `eval`、`exec` 执行用户输入
- 类型标注覆盖公共函数
- 异常信息必须可读，不向用户暴露堆栈
- 每个数据库写操作必须在测试中验证
- 每行最多 100 字符
- 提交信息使用 `feat:`、`fix:`、`test:`、`docs:`、`chore:` 前缀

## 测试

所有新功能先写失败测试，再实现最小代码，最后运行 `python -m pytest -v`。
