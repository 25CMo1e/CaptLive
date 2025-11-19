import argparse
import multiprocessing
import os

import flet as ft # 主要的UI框架
from dotenv import load_dotenv # 环境变量管理
from screeninfo import get_monitors # 获取屏幕信息

from app.app_manager import App, execute_dir # 应用管理器
from app.ui.components.save_progress_overlay import SaveProgressOverlay # 保存进度覆盖层
from app.utils.logger import logger # 日志记录器

DEFAULT_HOST = "127.0.0.1" # 默认主机
DEFAULT_PORT = 6006    # 默认端口
WINDOW_SCALE = 0.65 # 窗口缩放比例
MIN_WIDTH = 950 # 最小宽度
ASSETS_DIR = "assets" # 资源目录


def setup_window(page: ft.Page, is_web: bool) -> None: # 设置窗口
    page.window.icon = os.path.join(execute_dir, ASSETS_DIR, "icon.ico") # 设置窗口图标
    page.window.center() # 窗口居中
    page.window.to_front() # 窗口置顶
    page.skip_task_bar = True # 跳过任务栏
    page.always_on_top = True # 窗口始终置顶
    page.focused = True # 窗口聚焦

    if not is_web:
        try: # 获取屏幕信息
            screen = get_monitors()[0]
            page.window.width = int(screen.width * WINDOW_SCALE) # 设置窗口宽度
            page.window.height = int(screen.height * WINDOW_SCALE) # 设置窗口高度
        except IndexError:
            logger.warning("No monitors detected, using default window size.") # 没有检测到屏幕，使用默认窗口大小


def get_route_handler() -> dict[str, str]:
    return { # 获取路由处理函数
        "/": "home",
        "/home": "home",
        "/settings": "settings", # 设置
        "/storage": "storage", # 存储
        "/about": "about", # 关于
    }


def handle_route_change(page: ft.Page, app: App) -> callable:
    route_map = get_route_handler() # 获取路由处理函数

    def route_change(e: ft.RouteChangeEvent) -> None: # 路由变化处理函数
        tr = ft.TemplateRoute(e.route) # 获取路由
        page_name = route_map.get(tr.route) # 获取页面名称
        if page_name:
            page.run_task(app.switch_page, page_name) # 切换页面
        else:
            logger.warning(f"Unknown route: {e.route}, redirecting to /") # 未知路由，重定向到 /
            page.go("/") # 重定向到 /

    return route_change


def handle_window_event(page: ft.Page, app: App, save_progress_overlay: 'SaveProgressOverlay') -> callable:

    async def on_window_event(e: ft.ControlEvent) -> None:
        if e.data == "close":
            save_progress_overlay.show() # 显示保存进度覆盖层
            page.update()
            try:
                await app.cleanup() # 清理
            except Exception as ex:
                logger.error(f"Cleanup failed: {ex}")
            finally:
                page.window.destroy() # 销毁窗口
    return on_window_event


def handle_disconnect(page: ft.Page) -> callable:
    """Handle disconnection for web mode.""" # 处理断开连接

    def disconnect(_: ft.ControlEvent) -> None:
        page.pubsub.unsubscribe_all() # 取消订阅所有

    return disconnect


def main(page: ft.Page) -> None:

    page.title = "StreamCap" # 设置标题
    page.theme_mode = ft.ThemeMode.LIGHT # 设置主题模式浅色
    page.window.min_width = MIN_WIDTH # 设置最小宽度
    page.window.min_height = MIN_WIDTH * WINDOW_SCALE # 设置最小高度

    is_web = args.web or platform == "web" # 判断是否为web模式
    setup_window(page, is_web) # 设置窗口

    app = App(page) # 应用
    save_progress_overlay = SaveProgressOverlay(app) # 保存进度覆盖层
    page.overlay.append(save_progress_overlay.overlay) # 添加保存进度覆盖层

    page.on_route_change = handle_route_change(page, app) # 路由变化处理函数
    page.window.prevent_close = True # 防止关闭
    page.window.on_event = handle_window_event(page, app, save_progress_overlay) # 窗口事件处理函数

    if is_web:
        page.on_disconnect = handle_disconnect(page) # 处理断开连接

    page.update() # 更新
    page.on_route_change(ft.RouteChangeEvent(route=page.route)) # 路由变化处理函数


if __name__ == "__main__":
    load_dotenv() # 加载环境变量        
    platform = os.getenv("PLATFORM") # 获取平台
    default_host = os.getenv("HOST", DEFAULT_HOST) # 获取主机
    default_port = int(os.getenv("PORT", DEFAULT_PORT)) # 获取端口

    parser = argparse.ArgumentParser(description="Run the Flet app with optional web mode.")
    parser.add_argument("--web", action="store_true", help="Run the app in web mode") # 运行在web模式
    parser.add_argument("--host", type=str, default=default_host, help=f"Host address (default: {default_host})") # 主机地址
    parser.add_argument("--port", type=int, default=default_port, help=f"Port number (default: {default_port})") # 端口
    args = parser.parse_args()

    multiprocessing.freeze_support() # 冻结支持
    if args.web or platform == "web": # 判断是否为web模式
        logger.debug("Running in web mode on http://" + args.host + ":" + str(args.port)) # 运行在web模式
        ft.app(
            target=main, # 目标
            view=ft.AppView.WEB_BROWSER, # 网页浏览器
            host=args.host, # 主机地址      
            port=args.port, # 端口
            assets_dir=ASSETS_DIR, # 资源目录
            use_color_emoji=True, # 使用颜色表情
        )

    else: # 否则运行桌面程序
        ft.app(target=main, assets_dir=ASSETS_DIR) # 运行
