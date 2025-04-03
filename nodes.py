import os
import shutil
from PIL import Image
import comfy.utils



class BatchImageRenamer:
    """
    批量图片重命名与格式转换节点
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "输入文件目录": ("STRING", {
                    "default": "", 
                    "multiline": False,
                    "placeholder": "源文件夹绝对路径（如 /path/to/input）"
                }),
                "命名后保存目录": ("STRING", {
                    "default": "", 
                    "multiline": False,
                    "placeholder": "目标文件夹绝对路径（如 /path/to/output）"
                }),
                "文件名修改": ("STRING", {
                    "default": "image_{index:04d}",
                    "placeholder": "文件名模板（可用{index}占位符）"
                }),           
                "start_index": ("INT", {"default": 1, "min": 0, "max": 999999}),
                "文件格式": (["jpg", "png", "webp"], {"default": "jpg"}),
                "overwrite": ("BOOLEAN", {"default": False}),


                "info": ("STRING", {
                    "default": "📖 使用教程：\n1. 输入源/目标文件夹绝对路径\n2. 文件名模板可用 {index} 占位符\n3. 支持格式转换（jpg/png/webp）\n4. 设置起始索引和覆盖选项",
                    "multiline": True,
                    "disabled": True,  # 禁止编辑
                    "hidden": False    # 确保字段可见
                }),
                
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)
    FUNCTION = "rename_images"
    CATEGORY = "✍木子AI做号工具微信stone_liwei✍"
    OUTPUT_NODE = True

    def rename_images(self, 输入文件目录, 命名后保存目录, 文件名修改, start_index, new_extension, overwrite):
        # 输入验证
        if not os.path.exists(输入文件目录):
            raise ValueError(f"❌ 源文件夹不存在: {输入文件目录}")
            
        os.makedirs(命名后保存目录, exist_ok=True)

        # 获取所有图片文件
        supported_ext = ['.jpg', '.jpeg', '.png', '.webp']
        image_files = []
        for f in os.listdir(输入文件目录):
            file_path = os.path.join(输入文件目录, f)
            if os.path.isfile(file_path) and os.path.splitext(f)[1].lower() in supported_ext:
                image_files.append(file_path)

        if not image_files:
            raise ValueError("❌ 源文件夹中没有支持的图片文件（jpg/png/webp）")

        # 处理重命名
        success_count = 0
        for idx, src_path in enumerate(sorted(image_files), start=start_index):
            try:
                # 生成新文件名
                new_filename = 文件名修改.format(index=idx)
                new_path = os.path.join(命名后保存目录, f"{new_filename}.{new_extension}")

                # 处理重复文件
                if os.path.exists(new_path) and not overwrite:
                    raise FileExistsError(f"文件已存在: {new_path}")

                # 转换并保存图片
                img = Image.open(src_path).convert("RGB")
                save_kwargs = {"optimize": True}
                if new_extension == "jpg":
                    save_kwargs.update({"quality": 95, "subsampling": 0})
                elif new_extension == "webp":
                    save_kwargs["quality"] = 90

                img.save(new_path, **save_kwargs)
                success_count += 1
            except Exception as e:
                comfy.utils.print_error(f"处理文件失败 {src_path}: {str(e)}")

        return {"ui": {"text": [f"成功处理 {success_count}/{len(image_files)} 文件"]}, "result": (f"完成！输出至：{命名后保存目录}",)}





NODE_CLASS_MAPPINGS = {
"BatchImageRenamer": BatchImageRenamer
}
NODE_DISPLAY_NAME_MAPPINGS = {
"BatchImageRenamer": "⒈批量图片重命名😋微信stone_liwei"
}