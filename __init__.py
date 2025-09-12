bl_info = {
    "name": "Lehuye Plugin",
    "author": "GitHub Copilot",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Lehuye",
    "description": "乐乎也多功能插件集",
    "category": "PluginTools"
}

from . import main  # 调用 main.py

def register():
    main.register()  # Blender 加载插件时注册

def unregister():
    main.unregister()  # Blender 卸载插件时注销