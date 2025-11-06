import bpy
from .ui_panel import MaterialPanel,TextPanel,OriginPanel,DXFGeneratorPanel
from .ultrs import (
    MATERIAL_OT_clear_all,
    ORIGIN_OT_to_geometry,
    ORIGIN_OT_to_mass,
    ORIGIN_OT_to_cursor,
    ORIGIN_OT_to_volume,
    OBJECT_OT_rename_batch,
    OBJECT_OT_generate_from_dxf
)

classes = [
    MaterialPanel,
    MATERIAL_OT_clear_all,
    OriginPanel,
    ORIGIN_OT_to_geometry,
    ORIGIN_OT_to_mass,
    ORIGIN_OT_to_cursor,
    ORIGIN_OT_to_volume,
    TextPanel,
    OBJECT_OT_rename_batch,
    DXFGeneratorPanel,
    OBJECT_OT_generate_from_dxf,
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