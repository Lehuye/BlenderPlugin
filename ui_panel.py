# 面板UI文件，定义插件在侧边栏显示的面板和按钮
import bpy  # Blender Python API

# 定义一个枚举属性用于 Tab 切换
bpy.types.Scene.lehuye_tab = bpy.props.EnumProperty(
    name="功能分类",
    description="选择功能分类",
    items=[
        ('MATERIAL', "材质相关", "与材质相关的操作"),
        ('ORIGIN', "轴心相关", "与轴心相关的操作")
    ],
    default='MATERIAL'
)

# 定义一个面板类，显示在3D视图的侧边栏中
class MaterialPanel(bpy.types.Panel):
    bl_label = "材质工具"  # 面板名称
    bl_idname = "VIEW3D_PT_material_tools"  # 面板唯一标识
    bl_space_type = 'VIEW_3D'  # 显示空间类型
    bl_region_type = 'UI'  # 区域类型
    bl_category = 'Lehuye'  # 侧边栏分类名称

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        # Tab 切换按钮
        layout.prop(scene, "lehuye_tab", expand=True)
        layout.separator()
        # 根据 Tab 显示不同内容
        if scene.lehuye_tab == 'MATERIAL':
            layout.operator("material.clear_all", text="移除所有材质")
        elif scene.lehuye_tab == 'ORIGIN':
            layout.operator("origin.to_geometry", text="几何中心")
            layout.operator("origin.to_mass", text="质心")
            layout.operator("origin.to_cursor", text="原点（3D光标）")
            layout.operator("origin.to_volume", text="体积中心")

# 注销时删除属性
def unregister_panel_props():
    del bpy.types.Scene.lehuye_tab
