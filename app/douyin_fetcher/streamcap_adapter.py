"""
StreamCap Douyin Fetcher Adapter

本文件是适配器，用于将 DouyinLiveWebFetcher 的功能整合到 StreamCap 架构中。

代码来源:
- DouyinLiveWebFetcher: https://github.com/saermart/DouyinLiveWebFetcher
- StreamCap: https://github.com/ihmily/StreamCap

详细来源信息请查看项目根目录的 ATTRIBUTION.md 文件
"""

import threading
import websocket
from .liveMan import DouyinLiveWebFetcher
from .protobuf.douyin import (ChatMessage, GiftMessage, MemberMessage, LikeMessage, 
                             SocialMessage, EmojiChatMessage, RoomUserSeqMessage, 
                             RoomStatsMessage, ControlMessage, PushFrame)

class StreamCapDouyinFetcher(DouyinLiveWebFetcher):
    def __init__(self, live_id, on_chat=None, on_gift=None, on_member=None, on_like=None, 
                 on_social=None, on_emoji_chat=None, on_room_user_seq=None, on_room_stats=None, 
                 on_control=None, on_error=None, on_raw_message=None):
        super().__init__(live_id)
        self.on_chat = on_chat
        self.on_gift = on_gift
        self.on_member = on_member
        self.on_like = on_like
        self.on_social = on_social
        self.on_emoji_chat = on_emoji_chat
        self.on_room_user_seq = on_room_user_seq
        self.on_room_stats = on_room_stats
        self.on_control = on_control
        self.on_error = on_error
        self.on_raw_message = on_raw_message
        
        # 添加去重缓存
        self._message_cache = {}  # 存储最近处理的消息
        self._cache_timeout = 2  # 2秒内的重复消息将被忽略（购物消息更短）

    def start(self):
        try:
            self._connectWebSocket()
            if self.on_error:
                self.on_error("[弹幕] 连接已启动，等待消息...")
        except Exception as e:
            if self.on_error:
                self.on_error(f"[弹幕] 连接失败: {e}")

    def _wsOnOpen(self, ws):
        """连接建立成功 - 重写避免控制台输出"""
        if self.on_error:
            self.on_error("[弹幕] WebSocket连接成功")
        threading.Thread(target=self._sendHeartbeat).start()

    def _wsOnError(self, ws, error):
        if self.on_error:
            self.on_error(f"[WebSocket错误] {error}")

    def _wsOnClose(self, ws, close_status_code, close_msg):
        if self.on_error:
            self.on_error(f"[WebSocket关闭] code={close_status_code}, msg={close_msg}")

    def _sendHeartbeat(self):
        """发送心跳包 - 重写避免控制台输出"""
        while True:
            try:
                heartbeat = PushFrame(payload_type='hb').SerializeToString()
                self.ws.send(heartbeat, websocket.ABNF.OPCODE_PING)
                # 不输出到控制台
            except Exception as e:
                if self.on_error:
                    self.on_error(f"[心跳包错误] {e}")
                break

    def _wsOnMessage(self, ws, message):
        """接收消息 - 重写避免控制台输出"""
        import gzip
        from .protobuf.douyin import Response
        
        try:
            # 首先保存最初始的WebSocket消息
            if self.on_raw_message:
                self.on_raw_message("WebSocketRawMessage", message)
            
            # 根据proto结构体解析对象
            package = PushFrame().parse(message)
            response = Response().parse(gzip.decompress(package.payload))
            
            # 返回直播间服务器链接存活确认消息，便于持续获取数据
            if response.need_ack:
                ack = PushFrame(log_id=package.log_id,
                                payload_type='ack',
                                payload=response.internal_ext.encode('utf-8')
                                ).SerializeToString()
                ws.send(ack, websocket.ABNF.OPCODE_BINARY)
            
            # 根据消息类别解析消息体
            for msg in response.messages_list:
                method = msg.method
                try:
                    # 保存解析后的消息数据
                    if self.on_raw_message:
                        self.on_raw_message(method, msg.payload)
                    
                    # 定义需要过滤的无用消息类型（只包含数据长度且没有实际可读内容）
                    useless_message_types = {
                        'WebcastRanklistHourEntranceMessage',
                        'WebcastInRoomBannerMessage', 
                        'WebcastGiftSortMessage',
                        'WebcastRoomStreamAdaptationMessage',
                        'WebcastRoomRankMessage',
                        'WebcastFansclubMessage',
                        'WebcastRoomMessage',
                        'WebcastRoomUserSeqMessage',
                        'WebcastRoomStatsMessage',
                        'WebcastControlMessage'
                    }
                    
                    # 定义购物相关消息类型（需要保留）
                    shopping_message_types = {
                        'WebcastProductChangeMessage',
                        'WebcastLiveShoppingMessage', 
                        'WebcastLiveEcomGeneralMessage'
                    }
                    
                    # 定义核心消息类型（需要保留）
                    core_message_types = {
                        'WebcastChatMessage',
                        'WebcastGiftMessage', 
                        'WebcastMemberMessage',
                        'WebcastLikeMessage',
                        'WebcastSocialMessage',
                        'WebcastEmojiChatMessage'
                    }
                    
                    # 检查是否为无用消息
                    is_useless_message = method in useless_message_types
                    
                    # 检查是否为购物相关消息
                    is_shopping_message = method in shopping_message_types
                    
                    # 检查是否为核心消息
                    is_core_message = method in core_message_types
                    
                    # 检查是否包含购物关键词
                    has_shopping_keywords = any(keyword in method for keyword in ['Shopping', 'Ecom', 'Product', 'Order', 'Buy', 'Purchase', 'Cart', 'Item', 'Goods', 'Trade', 'Commerce', 'Sale', 'Shop'])
                    
                    # 只记录非核心消息，核心消息由各自的解析方法处理
                    if self.on_error and not is_useless_message and not is_core_message:
                        if is_shopping_message or has_shopping_keywords:
                            # 暂时禁用去重，确保能看到所有购物消息
                            self.on_error(f"[消息类型] {method} - 数据长度: {len(msg.payload)}")
                        else:
                            # 对于其他未知消息，尝试解析内容
                            readable_content = self._extractReadableContent(msg.payload)
                            if readable_content:
                                self.on_error(f"[🔍 未知消息] {method} - 内容: {readable_content}")
                            # 如果没有可读内容，则不输出
                    
                    # 处理所有消息，但过滤掉无用消息的日志输出
                    if method == 'WebcastChatMessage' and self.on_chat:
                        self._parseChatMsg(msg.payload)
                    elif method == 'WebcastGiftMessage' and self.on_gift:
                        self._parseGiftMsg(msg.payload)
                    elif method == 'WebcastMemberMessage' and self.on_member:
                        self._parseMemberMsg(msg.payload)
                    elif method == 'WebcastLikeMessage' and self.on_like:
                        self._parseLikeMsg(msg.payload)
                    elif method == 'WebcastSocialMessage' and self.on_social:
                        self._parseSocialMsg(msg.payload)
                    elif method == 'WebcastEmojiChatMessage' and self.on_emoji_chat:
                        self._parseEmojiChatMsg(msg.payload)
                    elif method == 'WebcastRoomUserSeqMessage' and self.on_room_user_seq:
                        self._parseRoomUserSeqMsg(msg.payload)
                    elif method == 'WebcastRoomStatsMessage' and self.on_room_stats:
                        self._parseRoomStatsMsg(msg.payload)
                    elif method == 'WebcastControlMessage' and self.on_control:
                        self._parseControlMsg(msg.payload)
                    elif method == 'WebcastProductChangeMessage':
                        # 暂时禁用去重，确保下单信息正常显示
                        self._parseProductChangeMsg(msg.payload)
                    elif method == 'WebcastLiveShoppingMessage':
                        # 暂时禁用去重，确保下单信息正常显示
                        self._parseLiveShoppingMsg(msg.payload)
                    elif method == 'WebcastLiveEcomGeneralMessage':
                        # 暂时禁用去重，确保下单信息正常显示
                        self._parseLiveEcomGeneralMsg(msg.payload)
                except Exception as e:
                    if self.on_error:
                        self.on_error(f"[消息解析异常] {method}: {e}")
        except Exception as e:
            if self.on_error:
                self.on_error(f"[消息解析错误] {e}")

    def _parseChatMsg(self, payload):
        try:
            message = ChatMessage().parse(payload)
            if self.on_chat:
                self.on_chat(message)
            # 不调用基类方法，避免控制台输出
        except Exception as e:
            if self.on_error:
                self.on_error(f"[弹幕解析错误] {e}")

    def _parseGiftMsg(self, payload):
        try:
            message = GiftMessage().parse(payload)
            if self.on_gift:
                self.on_gift(message)
            # 不调用基类方法，避免控制台输出
        except Exception as e:
            if self.on_error:
                self.on_error(f"[礼物解析错误] {e}")

    def _parseMemberMsg(self, payload):
        try:
            message = MemberMessage().parse(payload)
            if self.on_member:
                self.on_member(message)
            # 不调用基类方法，避免控制台输出
        except Exception as e:
            if self.on_error:
                self.on_error(f"[观众进入解析错误] {e}")

    def _parseProductChangeMsg(self, payload):
        """处理商品变更消息 - 可能包含下单信息"""
        try:
            from .protobuf.douyin import ProductChangeMessage
            message = ProductChangeMessage().parse(payload)
            # 总是处理商品变更消息，不依赖on_error回调
            if True:  # 强制处理商品变更消息
                toast = getattr(message, 'update_toast', '')
                if toast:
                    self.on_error(f"[商品变更] {toast}")
        except Exception as e:
            if self.on_error:
                self.on_error(f"[商品变更解析错误] {e}")

    def _parseLiveShoppingMsg(self, payload):
        """处理直播购物消息 - 可能包含下单信息"""
        try:
            from .protobuf.douyin import LiveShoppingMessage
            message = LiveShoppingMessage().parse(payload)
            # 总是处理购物消息，不依赖on_error回调
            if True:  # 强制处理购物消息
                msg_type = getattr(message, 'msg_type', 0)
                promotion_id = getattr(message, 'promotion_id', 0)
                common = getattr(message, 'common', None)
                
                # 获取时间戳信息
                create_time = 0
                if common:
                    create_time = getattr(common, 'create_time', 0)
                
                # 根据类型判断可能的操作
                type_map = {
                    1: "商品展示",
                    2: "下单操作", 
                    3: "加购物车",
                    4: "关注商品",
                    5: "取消关注"
                }
                operation = type_map.get(msg_type, f"未知操作({msg_type})")
                
                # 添加时间戳信息
                import time
                if create_time > 0:
                    time_str = time.strftime("%H:%M:%S", time.localtime(create_time / 1000))
                    self.on_error(f"[直播购物] {time_str} - {operation}, 商品ID:{promotion_id}")
                else:
                    self.on_error(f"[直播购物] {operation}, 商品ID:{promotion_id}")
                
                # 如果是下单操作，特别标记
                if msg_type == 2:
                    if create_time > 0:
                        time_str = time.strftime("%H:%M:%S", time.localtime(create_time / 1000))
                        self.on_error(f"[🛒 下单] {time_str} - 商品ID:{promotion_id}")
                    else:
                        self.on_error(f"[🛒 下单] 商品ID:{promotion_id}")
                    
        except Exception as e:
            if self.on_error:
                self.on_error(f"[直播购物解析错误] {e}")

    def _parseLiveEcomGeneralMsg(self, payload):
        """处理直播电商通用消息 - 直接保存为用户下单信息"""
        try:
            # 总是处理电商消息，不依赖on_error回调
            if True:  # 强制处理电商消息
                # 尝试解析消息内容
                data_length = len(payload)
                hex_data = payload.hex()
                
                # 查找可能包含商品信息的字符串
                try:
                    # 尝试解码十六进制数据中的字符串
                    decoded_strings = []
                    i = 0
                    while i < len(hex_data):
                        if i + 2 <= len(hex_data):
                            try:
                                # 尝试解码两个十六进制字符
                                byte_val = int(hex_data[i:i+2], 16)
                                if 32 <= byte_val <= 126:  # 可打印ASCII字符
                                    decoded_strings.append(chr(byte_val))
                                else:
                                    decoded_strings.append('.')
                            except:
                                decoded_strings.append('.')
                        i += 2
                    
                    decoded_text = ''.join(decoded_strings)
                    
                    # 查找关键词
                    keywords = ['Product', 'Order', 'Buy', 'Cart', 'Item', 'Goods', 'Purchase', 'Sale', 'Shop', 'Commerce', 'Ecom', 'Refresh', 'Update']
                    found_keywords = [kw for kw in keywords if kw in decoded_text]
                    
                    # 直接保存为用户下单信息
                    if found_keywords:
                        # 通过on_error回调保存下单信息
                        if self.on_error:
                            self.on_error(f"[下单] 用户下单商品 - 关键词: {', '.join(found_keywords)}")
                            self.on_error(f"[下单] 详细信息: {decoded_text[:200]}...")
                    else:
                        # 即使没有找到关键词，也保存为下单信息
                        if self.on_error:
                            self.on_error(f"[下单] 用户下单商品 - 数据长度: {data_length}")
                            self.on_error(f"[下单] 详细信息: {decoded_text[:100]}...")
                        
                except Exception as decode_error:
                    # 即使解析失败，也保存为下单信息
                    if self.on_error:
                        self.on_error(f"[下单] 用户下单商品 - 解析失败")
                        self.on_error(f"[下单] 原始数据: {hex_data[:100]}...")
                    
        except Exception as e:
            if self.on_error:
                self.on_error(f"[下单] 用户下单商品 - 处理异常: {e}")

    def _parseLikeMsg(self, payload):
        """处理点赞消息"""
        try:
            message = LikeMessage().parse(payload)
            if self.on_like:
                self.on_like(message)
        except Exception as e:
            if self.on_error:
                self.on_error(f"[点赞解析错误] {e}")

    def _parseSocialMsg(self, payload):
        """处理关注消息"""
        try:
            message = SocialMessage().parse(payload)
            if self.on_social:
                self.on_social(message)
        except Exception as e:
            if self.on_error:
                self.on_error(f"[关注解析错误] {e}")

    def _parseEmojiChatMsg(self, payload):
        """处理表情弹幕消息"""
        try:
            message = EmojiChatMessage().parse(payload)
            if self.on_emoji_chat:
                self.on_emoji_chat(message)
        except Exception as e:
            if self.on_error:
                self.on_error(f"[表情弹幕解析错误] {e}")

    def _parseRoomUserSeqMsg(self, payload):
        """处理房间用户序列消息"""
        try:
            message = RoomUserSeqMessage().parse(payload)
            if self.on_room_user_seq:
                self.on_room_user_seq(message)
        except Exception as e:
            if self.on_error:
                self.on_error(f"[房间用户序列解析错误] {e}")

    def _parseRoomStatsMsg(self, payload):
        """处理房间统计消息"""
        try:
            message = RoomStatsMessage().parse(payload)
            if self.on_room_stats:
                self.on_room_stats(message)
        except Exception as e:
            if self.on_error:
                self.on_error(f"[房间统计解析错误] {e}")

    def _parseControlMsg(self, payload):
        """处理控制消息"""
        try:
            message = ControlMessage().parse(payload)
            if self.on_control:
                self.on_control(message)
        except Exception as e:
            if self.on_error:
                self.on_error(f"[控制消息解析错误] {e}")

    def _isDuplicateMessage(self, method, payload):
        """检查是否为重复消息 - 基于内容特征进行智能去重"""
        import time
        import hashlib
        
        current_time = time.time()
        
        # 清理过期的缓存
        expired_keys = [k for k, v in self._message_cache.items() if current_time - v > self._cache_timeout]
        for key in expired_keys:
            del self._message_cache[key]
        
        # 对于购物相关消息，使用更精确的去重策略
        if method in ['WebcastLiveEcomGeneralMessage', 'WebcastLiveShoppingMessage', 'WebcastProductChangeMessage']:
            # 尝试提取关键特征进行去重
            content_signature = self._extractMessageSignature(method, payload)
            if content_signature:
                if content_signature in self._message_cache:
                    # 添加调试日志
                    if self.on_error:
                        self.on_error(f"[调试] 检测到重复消息: {method}, 签名: {content_signature[:16]}...")
                    return True
                self._message_cache[content_signature] = current_time
                # 添加调试日志
                if self.on_error:
                    self.on_error(f"[调试] 新消息已缓存: {method}, 签名: {content_signature[:16]}...")
                return False
            else:
                # 如果无法提取特征，使用payload hash但时间窗口更短
                message_hash = hashlib.md5(f"{method}_{payload}".encode()).hexdigest()
                if message_hash in self._message_cache:
                    if self.on_error:
                        self.on_error(f"[调试] 检测到重复消息(备用): {method}, hash: {message_hash[:16]}...")
                    return True
                self._message_cache[message_hash] = current_time
                if self.on_error:
                    self.on_error(f"[调试] 新消息已缓存(备用): {method}, hash: {message_hash[:16]}...")
                return False
        
        # 对于其他消息，使用payload hash（但缩短时间窗口）
        message_hash = hashlib.md5(f"{method}_{payload}".encode()).hexdigest()
        if message_hash in self._message_cache:
            return True
        
        self._message_cache[message_hash] = current_time
        return False

    def _extractMessageSignature(self, method, payload):
        """提取消息的关键特征用于去重"""
        try:
            # 对于WebcastLiveEcomGeneralMessage，尝试提取关键信息
            if method == 'WebcastLiveEcomGeneralMessage':
                # 尝试从payload中提取关键特征
                try:
                    # 查找可能包含商品ID或时间戳的关键部分
                    hex_data = payload.hex()
                    
                    # 查找ProductRefreshMessage等关键标识
                    if 'ProductRefreshMessage' in payload.decode('utf-8', errors='ignore'):
                        # 提取payload的前100个字节作为特征（通常包含关键信息）
                        signature = hashlib.md5(f"{method}_{payload[:100]}".encode()).hexdigest()
                        return signature
                except:
                    pass
            
            # 对于WebcastLiveShoppingMessage，基于商品ID和时间戳
            elif method == 'WebcastLiveShoppingMessage':
                try:
                    from .protobuf.douyin import LiveShoppingMessage
                    message = LiveShoppingMessage().parse(payload)
                    promotion_id = getattr(message, 'promotion_id', 0)
                    common = getattr(message, 'common', None)
                    create_time = 0
                    if common:
                        create_time = getattr(common, 'create_time', 0)
                    
                    # 基于商品ID和时间戳（精确到秒）生成签名
                    time_second = create_time // 1000 if create_time > 0 else 0
                    signature = f"{method}_{promotion_id}_{time_second}"
                    return hashlib.md5(signature.encode()).hexdigest()
                except:
                    pass
            
            # 对于WebcastProductChangeMessage，基于商品信息
            elif method == 'WebcastProductChangeMessage':
                try:
                    from .protobuf.douyin import ProductChangeMessage
                    message = ProductChangeMessage().parse(payload)
                    update_timestamp = getattr(message, 'updateTimestamp', 0)
                    update_toast = getattr(message, 'updateToast', '')
                    
                    # 基于时间戳和toast内容生成签名
                    time_second = update_timestamp // 1000 if update_timestamp > 0 else 0
                    signature = f"{method}_{time_second}_{update_toast}"
                    return hashlib.md5(signature.encode()).hexdigest()
                except:
                    pass
            
            return None
        except:
            return None

    def _extractReadableContent(self, payload):
        """从payload中提取可读文本内容"""
        try:
            # 方法1: 尝试直接解码为UTF-8字符串
            try:
                decoded_text = payload.decode('utf-8', errors='ignore')
                # 过滤掉只包含控制字符或不可打印字符的字符串
                readable_chars = [c for c in decoded_text if c.isprintable() and ord(c) >= 32]
                if len(readable_chars) > 5:  # 至少要有5个可读字符
                    return ''.join(readable_chars)[:200]  # 限制长度
            except:
                pass
            
            # 方法2: 尝试从十六进制数据中提取字符串
            try:
                hex_data = payload.hex()
                decoded_strings = []
                i = 0
                while i < len(hex_data):
                    if i + 2 <= len(hex_data):
                        try:
                            byte_val = int(hex_data[i:i+2], 16)
                            if 32 <= byte_val <= 126:  # 可打印ASCII字符
                                decoded_strings.append(chr(byte_val))
                            else:
                                decoded_strings.append('.')
                        except:
                            decoded_strings.append('.')
                    i += 2
                
                decoded_text = ''.join(decoded_strings)
                # 查找连续的可读字符
                readable_parts = []
                current_part = ""
                for char in decoded_text:
                    if char.isprintable() and ord(char) >= 32:
                        current_part += char
                    else:
                        if len(current_part) > 3:  # 至少3个连续可读字符
                            readable_parts.append(current_part)
                        current_part = ""
                
                if current_part and len(current_part) > 3:
                    readable_parts.append(current_part)
                
                if readable_parts:
                    return ' '.join(readable_parts)[:200]  # 限制长度
            except:
                pass
            
            # 方法3: 查找特定的关键词模式
            try:
                # 查找可能包含有用信息的模式
                text = payload.decode('utf-8', errors='ignore')
                keywords = ['用户', '商品', '订单', '购买', '下单', '购物', '价格', '数量', '名称', '描述', '时间', '状态']
                found_keywords = [kw for kw in keywords if kw in text]
                if found_keywords:
                    return f"包含关键词: {', '.join(found_keywords)}"
            except:
                pass
                
            return None
        except:
            return None 