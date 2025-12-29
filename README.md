# 24点扑克牌游戏 - 移动版

一个有趣的24点数学游戏，支持3人对战模式，可以在Android手机和iPad上运行。

## 游戏特色

- 🎴 精美的扑克牌图形界面，带有立体效果和金边
- 👥 3人对战模式，支持计分和排行榜
- 🎆 答对时有烟花庆祝效果
- ✅ 自动检测确保每道题都有解
- 📱 完美适配手机和平板屏幕
- 🎨 绿色主题，护眼舒适

## 在电脑上运行

### 前置要求

- Python 3.9 或更高版本
- pip 包管理器

### 安装步骤

1. 克隆或下载此仓库
2. 安装依赖：
   ```bash
   pip install kivy
   ```
3. 运行游戏：
   ```bash
   python game_24_mobile.py
   ```

## 使用GitHub Actions自动打包APK

### 方法一：推送代码自动触发（推荐）

1. **将代码推送到GitHub仓库**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/你的用户名/你的仓库名.git
   git push -u origin main
   ```

2. **等待自动构建**
   - 推送代码后，GitHub Actions会自动开始构建APK
   - 构建过程大约需要10-20分钟
   - 构建完成后，在GitHub仓库的"Actions"标签页可以查看构建状态

3. **下载APK**
   - 进入构建成功的页面
   - 在"Artifacts"部分下载"game24-apk"
   - 解压后即可获得APK文件

### 方法二：手动触发构建

1. 进入GitHub仓库
2. 点击"Actions"标签
3. 选择"Build Android APK"工作流
4. 点击"Run workflow"按钮
5. 选择分支并点击"Run workflow"
6. 等待构建完成后下载APK

### 方法三：创建Release时自动构建

1. 创建并推送标签：
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. 在GitHub上创建Release
3. APK会自动附加到Release中

## 在手机上安装

### Android设备

1. 下载APK文件
2. 在手机设置中启用"允许安装未知来源应用"
3. 点击APK文件进行安装
4. 安装完成后即可开始游戏

### iOS设备（iPad/iPhone）

iOS设备需要额外的步骤：

1. **使用BeeWare框架**（需要Mac电脑）
   ```bash
   pip install briefcase
   briefcase create ios
   briefcase build ios
   briefcase package ios
   ```

2. **或使用在线服务**
   - 使用Codemagic等CI/CD服务
   - 或使用TestFlight进行测试分发

## 游戏操作

### 基本操作

- **点击扑克牌**：选择要使用的数字
- **点击运算符**：添加 +、-、*、/ 或括号
- **清空**：重新开始当前题目
- **验证**：检查答案是否等于24
- **提示**：查看参考答案
- **跳过**：跳过当前题目，进入下一题
- **排行**：查看玩家排行榜

### 游戏规则

1. 必须使用所有4张牌
2. 每张牌只能使用一次
3. 可以使用加、减、乘、除和括号
4. 表达式的结果必须等于24
5. 答对一题得10分
6. 玩家轮流答题

## 项目结构

```
count_number_24/
├── .github/
│   └── workflows/
│       └── build-android.yml    # GitHub Actions配置
├── data/
│   ├── icon.png                 # 应用图标
│   └── presplash.png           # 启动画面
├── game_24.py                  # PC版游戏（Tkinter）
├── game_24_mobile.py           # 移动版游戏（Kivy）
├── buildozer.spec              # Buildozer配置文件
├── create_assets.py            # 创建图标和启动画面的脚本
├── README.md                   # 本文件
└── README_MOBILE.md            # 移动版详细说明
```

## 技术栈

- **前端框架**：Kivy（跨平台Python GUI框架）
- **打包工具**：Buildozer
- **CI/CD**：GitHub Actions
- **编程语言**：Python 3.9+

## 系统要求

### Android
- Android 5.0 (API 21) 或更高版本
- ARM64-v8a 或 armeabi-v7a 架构
- 至少 50MB 可用存储空间

### iOS
- iOS 12.0 或更高版本
- iPhone 6s 或更新机型
- iPad Air 2 或更新机型

## 故障排除

### 构建失败

1. 检查GitHub Actions日志
2. 确保buildozer.spec配置正确
3. 检查Python版本兼容性

### APK安装失败

1. 确保启用了"未知来源"安装
2. 检查Android版本是否兼容
3. 尝试重新下载APK

### 游戏运行问题

1. 确保设备有足够的存储空间
2. 重启设备后重试
3. 检查是否有其他应用冲突

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 联系方式

如有问题或建议，请通过GitHub Issues联系。

---

**享受游戏，挑战你的数学能力！** 🎮🧮
