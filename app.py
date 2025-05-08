bl_info = {
    "name": "Lehuye Auto Save",
    "author": "OpenAI",
    "version": (1, 2),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Lehuye",
    "description": "自动保存当前文件，可在侧栏设定开关与时间",
    "category": "System"
}

import bpy
import threading
import time

# 保存线程控制
save_thread = None
save_thread_stop = False


# 属性
class LehuyeProperties(bpy.types.PropertyGroup):
    auto_save_enabled: bpy.props.BoolProperty(
        name="启用自动保存",
        description="是否启用自动保存当前 .blend 文件",
        default=False
    )

    save_interval: bpy.props.IntProperty(
        name="保存间隔（秒）",
        description="设置自动保存的时间间隔",
        default=60,
        min=5,
        max=3600
    )


# 自动保存线程函数
def auto_save_loop():
    global save_thread_stop
    while not save_thread_stop:
        prefs = bpy.context.scene.lehuye_settings
        if prefs.auto_save_enabled and bpy.data.filepath:
            bpy.ops.wm.save_mainfile()
            print("Lehuye 自动保存完成")
        time.sleep(prefs.save_interval)


# 面板 UI：显示在侧边栏中
class LehuyePanel(bpy.types.Panel):
    bl_label = "Lehuye 自动保存"
    bl_idname = "VIEW3D_PT_lehuye_auto_save"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Lehuye"

    def draw(self, context):
        layout = self.layout
        props = context.scene.lehuye_settings

        layout.prop(props, "auto_save_enabled")
        layout.prop(props, "save_interval")


# 注册
def register():
    global save_thread, save_thread_stop

    bpy.utils.register_class(LehuyeProperties)
    bpy.types.Scene.lehuye_settings = bpy.props.PointerProperty(type=LehuyeProperties)

    bpy.utils.register_class(LehuyePanel)

    save_thread_stop = False
    save_thread = threading.Thread(target=auto_save_loop, daemon=True)
    save_thread.start()


# 注销
def unregister():
    global save_thread_stop

    save_thread_stop = True

    bpy.utils.unregister_class(LehuyePanel)
    del bpy.types.Scene.lehuye_settings
    bpy.utils.unregister_class(LehuyeProperties)