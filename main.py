import bpy

#从ui_pennel引入面板类
from .ui_panel import MaterialPanel,TextPanel,OriginPanel,DXFGeneratorPanel, GenerateMazePanel,FixModelPanel,CreatePolygonPanel,VIEW3D_PT_stairs_panel

# 引入的类名
from .ultrs import (
    MATERIAL_OT_clear_all,
    ORIGIN_OT_to_geometry,
    ORIGIN_OT_to_mass,
    ORIGIN_OT_to_cursor,
    ORIGIN_OT_to_volume,
    OBJECT_OT_rename_batch,
    OBJECT_OT_generate_from_dxf, # DXF 快速生成 3D
    MESH_OT_generate_maze_grid, #* 快速生成四壁 */
    OBJECT_OT_fix_model,
    OBJECT_OT_create_polygon,
    OBJECT_OT_generate_stairs,

)

classes = [
    # 材质工具
    MaterialPanel,
    MATERIAL_OT_clear_all,

    # 中心轴心工具
    OriginPanel,
    ORIGIN_OT_to_geometry,
    ORIGIN_OT_to_mass,
    ORIGIN_OT_to_cursor,
    ORIGIN_OT_to_volume,

    # Text 面板
    TextPanel,
    OBJECT_OT_rename_batch,

    # 快速生成四壁
    GenerateMazePanel,
    MESH_OT_generate_maze_grid,     # 快速生成四壁

    # DXF 生成面板和操作类
    DXFGeneratorPanel,
    OBJECT_OT_generate_from_dxf,

    # 修复模型
    FixModelPanel,
    OBJECT_OT_fix_model,

    # 创建多边形
    CreatePolygonPanel,
    OBJECT_OT_create_polygon,

    VIEW3D_PT_stairs_panel,
    OBJECT_OT_generate_stairs,

    

]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):  # 注销顺序反向
        bpy.utils.unregister_class(cls)

# 仅用于调试脚本时直接运行
if __name__ == "__main__":
    register()