# Blender 安装插件

在Blender中安装插件时，需要将文件夹打包为ZIP压缩文件才可以在Blender中从磁盘安装此插件。

因此需要运行此命令：
```bash
zip -r lehuyeplugin.zip .
```

此时在当前文件夹下会生成一个lehuyeplugin.zip压缩包，只需要在Blender中【编辑】【偏好设置】【插件】，【从磁盘导入】
选择该压缩包即可安装该插件。

# 文件结构

# 需要安装 Import curve dxf plugin

![](./screenshot/01.png)