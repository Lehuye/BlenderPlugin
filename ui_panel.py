# 面板UI文件，定义插件在侧边栏显示的面板和按钮
import bpy  # Blender Python API

# # 定义一个枚举属性用于 Tab 切换
# bpy.types.Scene.lehuye_tab = bpy.props.EnumProperty(
#     name="功能分类",
#     description="选择功能分类",
#     items=[
#         ('MATERIAL', "材质相关", "与材质相关的操作"),
#         ('ORIGIN', "轴心相关", "与轴心相关的操作")
#     ],
#     default='MATERIAL'
# )

class MaterialPanel(bpy.types.Panel):
    bl_label = "材质工具"
    bl_idname = "VIEW3D_PT_material_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lehuye'

    def draw(self, context):
        layout = self.layout
        layout.operator("material.clear_all", text="移除所有材质")


class OriginPanel(bpy.types.Panel):
    bl_label = "轴心工具"
    bl_idname = "VIEW3D_PT_origin_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lehuye'

    def draw(self, context):
        layout = self.layout
        layout.operator("origin.to_geometry", text="几何中心")
        layout.operator("origin.to_mass", text="质心")
        layout.operator("origin.to_cursor", text="原点（3D光标）")
        layout.operator("origin.to_volume", text="体积中心")


# 面板类：在侧栏显示文本输入框和按钮
class TextPanel(bpy.types.Panel):
    bl_label = "文本工具"
    bl_idname = "VIEW3D_PT_text_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lehuye'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # ---------------------
        # 单对象重命名
        # ---------------------
        # layout.label(text="单对象重命名")
        # layout.prop(scene, "rename_text", text="新名称")
        # layout.operator("object.rename_selected", text="重命名选中对象")
        # layout.separator()

        # ---------------------
        # 批量编号重命名
        # ---------------------
        layout.label(text="批量编号重命名")
        layout.prop(scene, "rename_text", text="名称主体")  # 使用同一个 rename_text
        layout.prop(scene, "rename_pos", text="编号位置")  # Enum: PREFIX / SUFFIX
        layout.prop(scene, "rename_start", text="起始编号")
        layout.prop(scene, "rename_order", text="顺序")     # Enum: ASC / DESC
        layout.operator("object.rename_selected", text="执行批量重命名")
        layout.separator()

class DXFGeneratorPanel(bpy.types.Panel):
    bl_label = "DXF 生成 3D"
    bl_idname = "VIEW3D_PT_generate_from_dxf"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lehuye'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="上传 DXF 并生成 3D")
        layout.prop(scene, "dxf_filepath", text="选择文件")
        layout.prop(scene, "level_height", text="楼层高度 (m)")
        layout.prop(scene, "wall_thickness", text="墙体厚度 (m)")
        layout.operator("object.generate_from_dxf", text="生成 3D 墙体")

def unregister_panel_props():
    del bpy.types.Scene.lehuye_tab
