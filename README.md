# OwMG - Oh where Money Go

>已知:这是一个纯py记账软件,练习用

该项目基于纯C语言的实现见[cOwMG](https://github.com/Annaler/cOwMG)。

---

## 待修复/实现

1. 阅账

    * 实现Options/Settings for user(可选)
    * 缩进格式/排版相关问题未解决 x
    * 类似less,过多时分页展示，一页展示默认5?(as a config)
    >也就是说多一个config.json?or maybe just txt:config.txt?or just "config"

2. 查账

   * 精准匹配->模糊

* 临时备份（考虑）
  * 仅保存上一次更改后的数据
  * 防止意外退出
  * 与数据文件对比不一样时询问是否更新为备份文件

---

## feat

```python
print("没有账目，但是你发现了一条小蛇/Snake Only")
print("see,snake:b\n(   )\n(   )\n(. .)")
```

>似乎没必要
