import os
import threading
import time
from datetime import datetime
from typing import Dict, Optional

from ..douyin_fetcher.streamcap_adapter import StreamCapDouyinFetcher
from ..utils.logger import logger


class BarrageManager:
    """弹幕录制管理器"""
    
    def __init__(self):
        self.active_fetchers: Dict[str, StreamCapDouyinFetcher] = {}
        self.barrage_files: Dict[str, str] = {}  # recording_id -> file_path
        self.lock = threading.Lock()
    
    def start_barrage_recording(self, recording_id: str, live_url: str, platform: str, recording_dir: str) -> bool:
        """开始弹幕录制"""
        try:
            if platform != "douyin":
                logger.warning(f"弹幕录制暂不支持平台: {platform}")
                return False
            
            # 提取直播间ID
            live_id = self._extract_live_id(live_url)
            if not live_id:
                logger.error(f"无法从URL提取直播间ID: {live_url}")
                return False
            
            # 创建弹幕文件
            barrage_file = self._create_barrage_file(recording_id, recording_dir)
            if not barrage_file:
                return False
            
            # 创建弹幕抓取器 - 启用解析功能
            fetcher = StreamCapDouyinFetcher(
                live_id=live_id,
                on_chat=lambda msg: self._handle_chat_message(recording_id, msg),  # 解析聊天消息
                on_gift=lambda msg: self._handle_gift_message(recording_id, msg),  # 解析礼物消息
                on_member=lambda msg: self._handle_member_message(recording_id, msg),  # 解析观众进入消息
                on_like=lambda msg: self._handle_like_message(recording_id, msg),  # 解析点赞消息
                on_social=lambda msg: self._handle_social_message(recording_id, msg),  # 解析关注消息
                on_emoji_chat=lambda msg: self._handle_emoji_chat_message(recording_id, msg),  # 解析表情弹幕消息
                on_room_user_seq=lambda msg: self._handle_room_user_seq_message(recording_id, msg),  # 解析房间用户序列消息
                on_room_stats=lambda msg: self._handle_room_stats_message(recording_id, msg),  # 解析房间统计消息
                on_control=lambda msg: self._handle_control_message(recording_id, msg),  # 解析控制消息
                on_error=lambda msg: self._handle_error_message(recording_id, msg),  # 错误消息
                on_raw_message=None  # 不再保存原始消息
            )
            
            # 设置录制ID和文件路径
            fetcher.recording_id = recording_id
            fetcher.barrage_file = barrage_file
            
            with self.lock:
                self.active_fetchers[recording_id] = fetcher
                self.barrage_files[recording_id] = barrage_file
            
            # 在单独线程中启动弹幕抓取
            thread = threading.Thread(target=self._start_fetcher, args=(fetcher,))
            thread.daemon = True
            thread.start()
            
            logger.info(f"开始弹幕录制: {recording_id}, 文件: {barrage_file}")
            return True
            
        except Exception as e:
            logger.error(f"启动弹幕录制失败: {e}")
            return False
    
    def stop_barrage_recording(self, recording_id: str) -> bool:
        """停止弹幕录制"""
        try:
            with self.lock:
                if recording_id in self.active_fetchers:
                    fetcher = self.active_fetchers[recording_id]
                    fetcher.stop()
                    del self.active_fetchers[recording_id]
                    
                    if recording_id in self.barrage_files:
                        del self.barrage_files[recording_id]
                    
                    logger.info(f"停止弹幕录制: {recording_id}")
                    return True
            return False
        except Exception as e:
            logger.error(f"停止弹幕录制失败: {e}")
            return False
    
    def is_recording(self, recording_id: str) -> bool:
        """检查是否正在录制弹幕"""
        with self.lock:
            return recording_id in self.active_fetchers
    
    def get_barrage_file(self, recording_id: str) -> Optional[str]:
        """获取弹幕文件路径"""
        with self.lock:
            return self.barrage_files.get(recording_id)
    
    def _extract_live_id(self, live_url: str) -> Optional[str]:
        """从URL提取直播间ID"""
        try:
            if "live.douyin.com" in live_url:
                # 从完整URL提取ID
                if "/" in live_url:
                    return live_url.split("/")[-1].split("?")[0]
            elif "v.douyin.com" in live_url:
                # 短链接需要解析，这里简化处理
                logger.warning("短链接需要解析，暂不支持")
                return None
            return None
        except Exception as e:
            logger.error(f"提取直播间ID失败: {e}")
            return None
    
    def _create_barrage_file(self, recording_id: str, recording_dir: str) -> Optional[str]:
        """创建弹幕文件"""
        try:
            if not recording_dir:
                recording_dir = "downloads"
            
            # 确保目录存在
            os.makedirs(recording_dir, exist_ok=True)
            
            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"barrage_{recording_id}_{timestamp}.txt"
            file_path = os.path.join(recording_dir, filename)
            
            # 创建文件并写入头部信息
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"# 抖音直播间弹幕解析文件\n")
                f.write(f"# 录制ID: {recording_id}\n")
                f.write(f"# 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# 格式: [时间] [消息类型] [详细信息]\n")
                f.write(f"# 说明: 包含以下消息类型：\n")
                f.write(f"#       - 弹幕: 观众聊天消息\n")
                f.write(f"#       - 礼物: 观众赠送礼物\n")
                f.write(f"#       - 进场: 观众进入直播间\n")
                f.write(f"#       - 点赞: 观众点赞\n")
                f.write(f"#       - 关注: 观众关注主播\n")
                f.write(f"#       - 下单: 观众下单商品\n")
                f.write(f"#       - 统计: 直播间统计信息\n\n")
            
            return file_path
        except Exception as e:
            logger.error(f"创建弹幕文件失败: {e}")
            return None
    
    def _start_fetcher(self, fetcher: StreamCapDouyinFetcher):
        """启动弹幕抓取器"""
        try:
            fetcher.start()
        except Exception as e:
            logger.error(f"弹幕抓取器启动失败: {e}")
    
    def _handle_chat_message(self, recording_id: str, msg):
        """处理聊天消息"""
        try:
            user_name = getattr(msg.user, 'nick_name', '')
            content = getattr(msg, 'content', '')
            self._write_to_file(recording_id, f"[弹幕] {user_name}: {content}")
        except Exception as e:
            logger.error(f"处理聊天消息失败: {e}")
    
    def _handle_gift_message(self, recording_id: str, msg):
        """处理礼物消息"""
        try:
            user_name = getattr(msg.user, 'nick_name', '')
            gift_name = getattr(msg.gift, 'name', '')
            gift_count = getattr(msg, 'combo_count', 1)
            self._write_to_file(recording_id, f"[礼物] {user_name} 赠送 {gift_name} x{gift_count}")
        except Exception as e:
            logger.error(f"处理礼物消息失败: {e}")
    
    def _handle_member_message(self, recording_id: str, msg):
        """处理观众进入消息"""
        try:
            user_name = getattr(msg.user, 'nick_name', '')
            gender_value = getattr(msg.user, 'gender', 0)
            if gender_value == 1:
                gender = "男"
            elif gender_value == 0:
                gender = "女"
            else:
                gender = "未知"
            self._write_to_file(recording_id, f"[进场] [{gender}]{user_name} 进入了直播间")
        except Exception as e:
            logger.error(f"处理观众进入消息失败: {e}")
    
    def _handle_like_message(self, recording_id: str, msg):
        """处理点赞消息"""
        try:
            user_name = getattr(msg.user, 'nick_name', '')
            count = getattr(msg, 'count', 1)
            self._write_to_file(recording_id, f"[点赞] {user_name} 点了{count}个赞")
        except Exception as e:
            logger.error(f"处理点赞消息失败: {e}")
    
    def _handle_social_message(self, recording_id: str, msg):
        """处理关注消息"""
        try:
            user_name = getattr(msg.user, 'nick_name', '')
            user_id = getattr(msg.user, 'id', '')
            self._write_to_file(recording_id, f"[关注] [{user_id}]{user_name} 关注了主播")
        except Exception as e:
            logger.error(f"处理关注消息失败: {e}")
    
    def _handle_emoji_chat_message(self, recording_id: str, msg):
        """处理表情弹幕消息"""
        try:
            user_name = getattr(msg.user, 'nick_name', '')
            emoji_id = getattr(msg, 'emoji_id', '')
            default_content = getattr(msg, 'default_content', '')
            content = default_content if default_content else f"表情ID:{emoji_id}"
            self._write_to_file(recording_id, f"[表情] {user_name}: {content}")
        except Exception as e:
            logger.error(f"处理表情弹幕消息失败: {e}")
    
    def _handle_room_user_seq_message(self, recording_id: str, msg):
        """处理房间用户序列消息"""
        try:
            current = getattr(msg, 'total', 0)
            total = getattr(msg, 'total_pv_for_anchor', 0)
            self._write_to_file(recording_id, f"[统计] 当前观看人数: {current}, 累计观看人数: {total}")
        except Exception as e:
            logger.error(f"处理房间用户序列消息失败: {e}")
    
    def _handle_room_stats_message(self, recording_id: str, msg):
        """处理房间统计消息"""
        try:
            display_long = getattr(msg, 'display_long', '')
            if display_long:
                self._write_to_file(recording_id, f"[房间统计] {display_long}")
        except Exception as e:
            logger.error(f"处理房间统计消息失败: {e}")
    
    def _handle_control_message(self, recording_id: str, msg):
        """处理控制消息"""
        try:
            status = getattr(msg, 'status', 0)
            if status == 3:
                self._write_to_file(recording_id, "[控制] 直播间已结束")
            else:
                self._write_to_file(recording_id, f"[控制] 直播间状态: {status}")
        except Exception as e:
            logger.error(f"处理控制消息失败: {e}")

    def _handle_error_message(self, recording_id: str, msg):
        """处理错误消息"""
        try:
            self._write_to_file(recording_id, f"[系统] {msg}")
        except Exception as e:
            logger.error(f"处理错误消息失败: {e}")
    
    def _write_to_file(self, recording_id: str, message: str):
        """写入弹幕到文件"""
        try:
            with self.lock:
                if recording_id in self.barrage_files:
                    barrage_file = self.barrage_files[recording_id]
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    with open(barrage_file, "a", encoding="utf-8") as f:
                        f.write(f"[{timestamp}] {message}\n")
        except Exception as e:
            logger.error(f"写入弹幕文件失败: {e}")
    
    def _write_raw_message(self, recording_id: str, message_type: str, raw_data: bytes):
        """写入原始消息数据到文件"""
        try:
            with self.lock:
                if recording_id in self.barrage_files:
                    barrage_file = self.barrage_files[recording_id]
                    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]  # 包含毫秒
                    # 将原始数据转换为十六进制字符串
                    hex_data = raw_data.hex()
                    with open(barrage_file, "a", encoding="utf-8") as f:
                        f.write(f"[{timestamp}] [{message_type}] {hex_data}\n")
        except Exception as e:
            logger.error(f"写入原始消息文件失败: {e}")


# 全局弹幕管理器实例
barrage_manager = BarrageManager()
