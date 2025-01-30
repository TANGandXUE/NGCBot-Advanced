import os
from rapidocr_onnxruntime import RapidOCR
from OutPut.outPut import op

class ImageCache:
    def __init__(self):
        self.image_records = {}  # {user_id+room_id: (msg_id, extra)}
        self.ocr_engine = RapidOCR()
        
        # 使用相对于项目根目录的路径
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.image_dir = os.path.join(root_dir, "FileCache", "ocr_images")
        
        # 确保目录存在并有正确权限
        try:
            if not os.path.exists(self.image_dir):
                # 递归创建目录
                os.makedirs(self.image_dir, mode=0o777, exist_ok=True)
            
            # 测试目录写入权限
            test_file = os.path.join(self.image_dir, "test_write.tmp")
            try:
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
                op(f"[Debug] 图片目录初始化成功: {self.image_dir}")
            except Exception as e:
                op(f"[Error] 图片目录写入测试失败: {e}")
                # 尝试修复权限
                os.chmod(self.image_dir, 0o777)
                
        except Exception as e:
            op(f"[Error] 图片目录初始化失败: {e}")
            # 如果创建目录失败，使用临时目录
            self.image_dir = os.path.join(os.path.expanduser('~'), 'temp_ocr_images')
            os.makedirs(self.image_dir, mode=0o777, exist_ok=True)
            op(f"[Warning] 使用备用目录: {self.image_dir}")
            
    def record_image(self, sender, room_id, msg_id, extra):
        """记录用户发送的图片信息"""
        key = f"{sender}_{room_id}"
        self.image_records[key] = (msg_id, extra)
        op(f"[Debug] 记录图片信息:")
        op(f"- 用户: {sender}")
        op(f"- 群ID: {room_id}")
        op(f"- 消息ID: {msg_id}")
        op(f"- Extra: {extra}")
        
    def get_image_ocr(self, wcf, sender, room_id):
        """获取图片OCR结果"""
        key = f"{sender}_{room_id}"
        if key not in self.image_records:
            op(f"[Debug] 未找到图片记录: {key}")
            return None
            
        msg_id, extra = self.image_records[key]
        op(f"[Debug] 开始处理图片:")
        op(f"- 消息ID: {msg_id}")
        op(f"- Extra: {extra}")
        
        try:
            # 下载图片
            op(f"[Debug] 开始下载图片...")
            image_path = wcf.download_image(
                id=int(msg_id),
                extra=str(extra),
                dir=str(self.image_dir),
                timeout=60
            )
            
            if not image_path:
                op(f"[Error] 图片下载失败")
                return None
                
            if not os.path.exists(image_path):
                op(f"[Error] 下载的图片文件不存在: {image_path}")
                return None
                
            # OCR识别
            op(f"[Debug] 开始OCR识别: {image_path}")
            result, elapse = self.ocr_engine(image_path)
            
            # 删除临时图片
            try:
                os.remove(image_path)
                op(f"[Debug] 临时图片删除成功")
            except Exception as e:
                op(f"[Warning] 删除临时图片失败: {e}")
            
            if not result:
                return None
                
            # 提取文本
            text = "\n".join([item[1] for item in result])
            op(f"[Debug] OCR识别成功: {len(result)} 个结果")
            
            return text
            
        except Exception as e:
            op(f"[Error] OCR处理失败: {e}")
            return None
        finally:
            self.clear_image(sender, room_id)
            
    def clear_image(self, sender, room_id):
        """清除用户的图片记录"""
        key = f"{sender}_{room_id}"
        if key in self.image_records:
            del self.image_records[key]
            op(f"[Debug] 清除图片信息: {key}") 