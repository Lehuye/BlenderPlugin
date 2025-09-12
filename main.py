import bpy
from .ui_panel import MaterialPanel
from .material_clear import MATERIAL_OT_clear_all
from .origin_tools import (
    ORIGIN_OT_to_geometry,
    ORIGIN_OT_to_mass,
    ORIGIN_OT_to_cursor,
    ORIGIN_OT_to_volume
)

classes = [
    MATERIAL_OT_clear_all,
    ORIGIN_OT_to_geometry,
    ORIGIN_OT_to_mass,
    ORIGIN_OT_to_cursor,
    ORIGIN_OT_to_volume,
    MaterialPanel
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