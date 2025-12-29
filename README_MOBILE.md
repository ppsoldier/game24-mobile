# 24点扑克牌游戏 - 移动版

## 游戏功能

- 扑克牌图形界面，带有立体效果和金边
- 3人对战模式，带有计分和排行榜
- 答对时有烟花庆祝效果
- 自动检测确保每道题都有解
- 适配手机和平板屏幕

## 在电脑上运行

1. 确保已安装Python 3.9+
2. 安装依赖：
   ```bash
   pip install kivy
   ```
3. 运行游戏：
   ```bash
   python game_24_mobile.py
   ```

## 打包成Android APK

由于buildozer在Windows上打包需要Linux环境，有以下几种方法：

### 方法1：使用在线打包服务（推荐）

1. 访问 https://github.com/kivy/buildozer-gh-action
2. 上传你的代码到GitHub仓库
3. 使用GitHub Actions自动打包APK
4. 下载生成的APK文件

### 方法2：使用虚拟机或WSL

1. 安装Ubuntu虚拟机或启用WSL
2. 在Linux环境中安装buildozer：
   ```bash
   pip install buildozer
   sudo apt-get install -y build-essential git ffmpeg libsdl2-dev libsdl2-image-dev \
   libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev \
   libavcodec-dev zlib1g-dev libgstreamer1.0-dev gstreamer1.0-plugins-base \
   gstreamer1.0-plugins-good
   ```
3. 在项目目录运行：
   ```bash
   buildozer android debug
   ```
4. 等待打包完成，APK文件在bin目录中

### 方法3：使用BeeWare（支持iOS）

对于iPad/iPhone，可以使用BeeWare框架：

1. 安装BeeWare：
   ```bash
   pip install briefcase
   ```
2. 创建iOS项目：
   ```bash
   briefcase create ios
   briefcase build ios
   briefcase package ios
   ```

## 游戏操作

- 点击扑克牌选择数字
- 点击运算符按钮添加符号
- 点击"验证"检查答案
- 点击"提示"查看参考答案
- 点击"跳过"跳过当前题目
- 点击"排行"查看排行榜

## 注意事项

- 需要使用所有4张牌
- 表达式必须等于24
- 支持加减乘除和括号
- 每答对一题得10分

## 系统要求

- Android 5.0 (API 21) 或更高版本
- iOS 12.0 或更高版本
- 屏幕分辨率：至少 360x640
