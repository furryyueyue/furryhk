# FurryHK · 悦悦的扩条

悦悦的个人主页与「文字蒲公英」小游戏。这个说明汇总网站源码、界面交互、部署迁移和 EdgeOne 配置的历史变更，便于后续维护。

整理日期：**2026-10-26（北京时间）**。源码基线：[`4be79da`](https://github.com/furryyueyue/furryhk/commit/4be79da3f714405783f3112b1c4c602d040016dc)。

## 网站与文件

| 项目 | 地址或路径 | 说明 |
| --- | --- | --- |
| 根域名主页 | https://furryhk.cn/ | 保留人机验证；验证后直接显示主页，地址保留根域名 |
| www 主页 | https://www.furryhk.cn/ | 保留人机验证，独立作为主页入口 |
| 文字蒲公英 | https://pgy.furryhk.cn/ | 独立小游戏入口 |
| 历史邮箱服务域名 | `furryhk-mail.furryhk.cn` | 历史功能；不代表当前服务可用 |
| 主页源码 | [index.html](index.html) | HTML、样式与交互脚本 |
| 小游戏源码 | [games/text-dandelion/index.html](games/text-dandelion/index.html) | 文字蒲公英 |
| 静态资源 | [assets/](assets/) | 表情及其他页面资源 |
| 搜索引擎配置 | [robots.txt](robots.txt)、[sitemap.xml](sitemap.xml) | 抓取与站点地图 |
| IndexNow | [.github/workflows/indexnow.yml](.github/workflows/indexnow.yml) | main 推送或手动触发通知 |

这是静态网站，可以通过普通 HTTP 静态服务器预览。EdgeOne 人机校验、域名回源和服务器侧配置不随静态源码自动恢复。

## 2026-10-26：修复根域名验证后跳 www 再验证

### 原来的访问过程

访问 `furryhk.cn` → EdgeOne 校验 → 跳到 `www.furryhk.cn` → 再次校验 → 主页。

最终采用的方案是：**两个域名均可直接显示同一主页，各自保留验证，根域名不再因为这次回源访问而跨域跳转。**没有实现或宣称实现跨域名共享验证凭证。

### 实际发布的配置

位置：**腾讯云 EdgeOne → 站点加速 → 规则引擎**。

| 配置项 | 值 |
| --- | --- |
| 规则名称 | 根域名直接访问主页 |
| 匹配类型 | HOST |
| 运算符 | 等于 |
| 匹配值 | `furryhk.cn` |
| 操作 | Host Header 重写 |
| 模式 | 自定义 |
| 目标值 | `www.furryhk.cn` |

EdgeOne 接收根域名请求时，回源使用 `Host: www.furryhk.cn` 获取主页内容；访客地址栏继续保留 `furryhk.cn`。这不是向浏览器返回 301/302，也不是把 DNS 指向另一个网站。

### 验证与操作边界

- 用户完成根域名真人校验后，浏览器实际显示「悦悦的扩条 · FurryHK」主页，地址为 `https://furryhk.cn/?`；没有再跳到 www 的校验页。
- 单独打开 `https://www.furryhk.cn/`，仍显示 EdgeOne 真人校验入口；本次没有再次完成 www 的整套真人校验。
- 四个域名最终继续使用原站点级统一防护策略；人机校验开关未关闭。
- 期间曾从原策略复制根域名独立策略，随后恢复为站点级策略；该临时独立策略不是最终方案。
- 曾编辑「根域名跳转-www」草稿，后来取消，**没有发布该重定向规则**。
- 本次没有修改 1Panel、源站网站代码、DNS、邮箱记录，也没有直接删除源站已有重定向配置。
- 此变更位于 EdgeOne 控制台，下面的提交索引不包含它；本 README 是对实际操作的补充记录。

## 功能与界面变更汇总

以下按功能汇总已留有提交记录的改动。旧实现被替换、删除的情况会明确说明；完整逐条提交索引见文末。

### 主页内容与布局

- 建立个人主页，上传头像、联系二维码、收款图片等静态资源；主页文件逐步统一为 `index.html`。
- 调整玻璃质感、圆角、留白、系统字体、卡片配色及内容层次；降低移动端渲染负担。
- 更新个人标签和模块文案，逐步形成「数码人」「喜欢摄影」「线条小狗重度依赖」「我在折腾的小东西」等内容。
- 主页名称调整为「悦悦的扩条」；「我是悦悦」删除末尾句号；增加浅色昵称「你可以叫我 CN：悦悦 / 古茗」，移除昵称下方的账号标识。
- 优化横屏和平板双栏布局、宽屏居中、字号与间距；修复极窄屏横向溢出。
- 曾加入委托定制区域，后来删除；它属于历史功能。

### 联系方式、图片与动画

- 优化联系方式展开/收起动画，修复快速切换时的状态竞争、内容重叠和折叠时序。
- 联系二维码改为更清晰的资源，保持原始宽高比，确保完整显示。
- 图片放大增加打开与关闭过渡；处理二维码飞入/飞出时被弹层滚动边界裁切的问题。
- 头像保持不可放大；统一表情资源与点击位置反馈，延长反馈可见时间并修正层级。
- 「请我喝杯奶茶」增加缓慢展开、关闭及内容分阶段出现效果，修复展开状态判断。
- 早期多次试验加载环、模拟检查、加载完成提示；后续提交删除主页加载屏和完成提示。它们不是 EdgeOne 的真实安全验证。
- 增加动画回退、页面往返过渡和减少动态效果的兼容处理；不能仅凭提交记录宣称所有设备均达到固定帧率。

### 友情链接与页脚

- 新增友情链接区域，补齐好友头像、QQ/微信二维码；优化卡片配色、圆角、展开动画和二维码尺寸。
- 友情链接移动到奶茶支持区域上方；加入「小狼」及「友链申请请联系」提示。
- 增加底部 Bug 反馈邮件链接和预填主题「扩条Bug反馈」，使用小扳手标识。
- 增加与调整萌备、ICP备案展示和爪印装饰；曾使用「已备案，自己去查😆」，后来删除。
- 页脚备案最终调整为同一行横向排列；当前主页源码显示「桂ICP备2026023237号」及「萌ICP备20260881号」。
- 曾有恢复完整主页、临时修复工作流及线上文件回同步；临时工作流随后移除。它们保留在 Git 历史中。

### 文字蒲公英

- 新增文字蒲公英页面和主页入口，并提供返回主页链接。
- 实现逐字/顺序放飞、一键散开等交互，调整跟手触碰和尾巴碰撞判定。
- 加入缓慢三维旋转、连接中心的小尾巴与来源标注；优化文字深浅、旋转和空间呈现。
- 修复漏判触碰、背面种子不易触发、文字与整根细丝接触响应、放飞不连贯等问题。
- 顺序模式改为点击触发；减少合并指针事件带来的重复工作。
- 所有种子完成后显示「天天开心」。
- 增加主页到小游戏、小游戏返回主页的双向过渡；修正返回链接。
- 在既有 Canvas 像素预算内改善高像素密度屏幕的文字清晰度。
- 历史检查覆盖入口、返回、顺序放飞等流程；未据此宣称完成全部手机真机测试。

### 邮箱入口与反馈地址的历史变化

- 早期创建、重命名及删除邮箱页面与条款文件。
- 2026-10-20 提交删除过时邮箱服务入口、联系方式，并将 Bug 反馈改为 Gmail。
- 2026-10-25 存在把线上主页同步回仓库的提交。**整理时的 main 源码又包含免费邮箱入口、推荐邮箱模板，Bug 反馈链接为旧域名邮箱；本次浏览器看到的线上根域名主页，Bug 反馈则为 Gmail。**
- 因此，10 月 20 日的删除/替换属于真实历史提交，但不能写成仓库当前仍全部保持该状态。此次只补充说明，不顺带修改页面或邮箱 DNS。

### 搜索引擎与部署

- 增加 SEO 标题、描述、关键词、canonical、Open Graph、Twitter 卡片及结构化数据。
- 明确头像网站图标尺寸，统一搜索和分享预览头像。
- 增加 `robots.txt`、`sitemap.xml`、IndexNow 验证文件及自动通知工作流。
- 历史上使用过 GitHub Pages/CNAME 配置，后删除 CNAME；也曾尝试 Cloudflare Pages。
- 后续迁移到阿里云服务器，曾使用宝塔；用户现确认源站面板为 **1Panel**。
- 后续改用腾讯云体系，当前浏览器控制台显示 EdgeOne NS 接入与免费版站点。历史的 Cloudflare/宝塔步骤不能当成现行面板教程。
- 曾处理根域名接入与重定向问题，并做多地区 DNS/访问检查；历史抽样结果不等于持续保证所有地区均无源站泄露。

## 当前需要区分的状态

| 事项 | 截至本次整理的证据与状态 |
| --- | --- |
| 根域名重复验证 | 本次已发布 Host Header 重写，根域名验证后留在根域名主页，浏览器已确认 |
| www 验证保护 | 单独访问仍出现验证页；本次未重新完成验证后的整套回归 |
| 四域名防护策略关联 | 本次控制台确认四域名均关联站点级策略；不代表四个业务均已逐一验证可用 |
| 邮箱页面清理 | 历史提交存在；当前仓库与线上内容有差异，需另行处理部署一致性 |
| 阿里企业邮箱 DNS | 历史涉及 MX、SPF、DKIM、DMARC 排查；此次未修改、未重新验证，不能标记为修复完成 |
| 源站防泄露 | 源站访问限制、回源鉴权、权威 DNS 与历史记录仍需专项核验；此次未执行 |
| WAF、CC、DDoS | 控制台检查过部分现有开关；没有在此次完成整套加固与攻击验收 |
| 短信告警 | 历史有配置需求；此次没有确认联系人、订阅或真实告警投递成功 |
| 小游戏遗留项 | 历史检查曾发现字数文案与实际补字行为、备案同步等差异；此次没有重新修复或验收 |
| 首页动画偏好 | 用户要求无首页加载动画、交互简洁流畅；历史实际页面仍出现过入场动画，需按现行页面复核 |

## 维护约定

- 源码、线上部署和 EdgeOne 控制台配置分别核对，不能把“GitHub 已提交”直接当成“线上已更新”。
- 对根域名和 www 的改动，以两个域名都能直接访问且保留验证为验收目标；不要重新加上导致两次验证的跨域跳转。
- 修改网站解析时保留邮件相关记录；邮件功能是否正常需要独立验证。
- 本说明仅记录本网站项目；账号密码、云 API 密钥、服务器登录信息、源站 IP 和个人无关记录不写入公开仓库。
- 日期采用北京时间。提交索引中的原始标题用于追溯，不表示旧代码现在仍启用，也不表示提交标题提及的每个目标都经过完整验收。

## 完整历史提交索引

以下为整理时 main 历史的 **124 条提交**，从最近到最早，覆盖初始建站至 2026-10-25。模糊的“Update index.html”“Add files via upload”等标题保留原文，不猜测其具体修改；点击提交可查看差异。本次文档提交及之后的新提交请查看 [GitHub 完整历史](https://github.com/furryyueyue/furryhk/commits/main/)。

<details>
<summary>展开全部 124 条历史记录（北京时间）</summary>

| 时间 | 提交 | 原始更改说明 |
| --- | --- | --- |
| 2026-10-25 16:22 | [`4be79da`](https://github.com/furryyueyue/furryhk/commit/4be79da3f714405783f3112b1c4c602d040016dc) | chore: remove temporary sync workflow |
| 2026-10-25 16:21 | [`ddf8542`](https://github.com/furryyueyue/furryhk/commit/ddf8542eaf8fae45c93d4cfabb3ba21fd7861247) | chore: sync index.html with live server (footer filings + friends apply note) [skip ci] |
| 2026-10-25 16:21 | [`52c004e`](https://github.com/furryyueyue/furryhk/commit/52c004ed619054ccaf1fc871d1a5f8b0701be4d3) | chore: retry github sync via litterbox mirror |
| 2026-10-25 16:13 | [`266d9bf`](https://github.com/furryyueyue/furryhk/commit/266d9bf804a38851ae7177760642052f0253f01a) | chore: sync github index.html from live server |
| 2026-10-25 15:59 | [`9654cbd`](https://github.com/furryyueyue/furryhk/commit/9654cbd08b923b8134de47e368c122b03726e26d) | feat: add faint friends-apply note beside links heading [skip ci] |
| 2026-10-25 15:59 | [`b3c165f`](https://github.com/furryyueyue/furryhk/commit/b3c165f597ac5c3655162fe0e52e61892631e823) | chore: add friends-apply note workflow |
| 2026-10-24 11:46 | [`21fdbc5`](https://github.com/furryyueyue/furryhk/commit/21fdbc562c71a8a40250e5bd5ca634af3328e3d4) | chore: remove temporary footer-fix workflow |
| 2026-10-24 11:45 | [`0e43dd3`](https://github.com/furryyueyue/furryhk/commit/0e43dd34ce7b9342beda8e3da5dd481914d36734) | chore: footer filings inline; restore full index [skip ci] |
| 2026-10-24 11:45 | [`22711ed`](https://github.com/furryyueyue/furryhk/commit/22711ed9030700e495fb458497a0d657025c2a6f) | chore: add footer fix workflow |
| 2026-10-24 11:38 | [`60e5cd7`](https://github.com/furryyueyue/furryhk/commit/60e5cd74cc93caa197b2d2a83e935214321c7f5f) | chore: upload rebuild part 000 |
| 2026-10-24 11:04 | [`9e29c8d`](https://github.com/furryyueyue/furryhk/commit/9e29c8d2bc9ee0e27b5408db2afee50a199ebc3f) | chore: 删除已备案自己去查文案，桂ICP与萌ICP备案并排同一行 |
| 2026-10-24 11:01 | [`5a47a71`](https://github.com/furryyueyue/furryhk/commit/5a47a718d6b819f65392c4a8b2a2991e103d19f0) | chore: 删除已备案自己去查文案，桂ICP与萌ICP备案并排同一行 |
| 2026-10-23 22:46 | [`420f05a`](https://github.com/furryyueyue/furryhk/commit/420f05a901a5460169916364930fe5bc447bdf63) | chore: 删除已备案自己去查文案，桂ICP与萌ICP备案并排同一行 |
| 2026-10-20 14:37 | [`127aedc`](https://github.com/furryyueyue/furryhk/commit/127aedc7950e7be75b364d02a2c63fe5c04a3357) | Use Gmail for homepage bug feedback |
| 2026-10-20 14:34 | [`d9df48f`](https://github.com/furryyueyue/furryhk/commit/d9df48f0cfa11f21e68d440f2d36e2e64a49b723) | Remove deprecated email service and contact links from homepage |
| 2026-10-19 23:49 | [`c7a5793`](https://github.com/furryyueyue/furryhk/commit/c7a57933d3a6042a9f47e14b3a47ed0d822be54d) | style: remove profile handle below nickname |
| 2026-10-19 23:47 | [`2abc3ab`](https://github.com/furryyueyue/furryhk/commit/2abc3abe1c8c478741b1b9b298eade20b8b118a0) | style: remove heading punctuation and add subtle CN nickname |
| 2026-10-19 23:43 | [`426cfb2`](https://github.com/furryyueyue/furryhk/commit/426cfb2de9a7cae02e3a4b99cd03a8d7a6d4b652) | fix: update footer filing text with emoji |
| 2026-10-19 23:42 | [`86806ea`](https://github.com/furryyueyue/furryhk/commit/86806eac96560028de87794f7b42aa3ad0ab4305) | fix: display plain 已备案 text in footer |
| 2026-10-19 23:42 | [`060d938`](https://github.com/furryyueyue/furryhk/commit/060d9381b431c02b9cd6e9c1d8e992f67e237970) | fix: show filed status and full ICP number in footer |
| 2026-10-18 16:39 | [`f1a1bab`](https://github.com/furryyueyue/furryhk/commit/f1a1babb1bcbe75defb13660e6dc75b01ef96782) | Sharpen dandelion text on 3x displays within the existing canvas pixel budget |
| 2026-10-18 16:31 | [`904383d`](https://github.com/furryyueyue/furryhk/commit/904383d2a47fa6867042e150bf622980d32cb83c) | Fix rear dandelion seed brushing and reduce coalesced pointer work |
| 2026-10-18 15:18 | [`498e483`](https://github.com/furryyueyue/furryhk/commit/498e4832696ad1be84d4cbdcbed8bf176e3f8c72) | Smooth dandelion rotation and depth rendering; make sequence mode tap-only |
| 2026-10-18 02:35 | [`2c0e11c`](https://github.com/furryyueyue/furryhk/commit/2c0e11cb828e5ca02e2f5c91adc876bb9d0f54fe) | Release dandelion seeds immediately on full filament or glyph contact |
| 2026-10-18 02:14 | [`b7283fc`](https://github.com/furryyueyue/furryhk/commit/b7283fc079992a9cf9a695548dcac342371cfc76) | Add gentle 天天开心 ending after all dandelion seeds finish |
| 2026-10-18 02:05 | [`40549c2`](https://github.com/furryyueyue/furryhk/commit/40549c2b1826cc87c93251422b5a822e6788caae) | Smooth dandelion release and fix missed pointer contacts |
| 2026-10-17 23:08 | [`551e1d7`](https://github.com/furryyueyue/furryhk/commit/551e1d77ab5a59a3242b24ba4dca3a29e5603340) | feat: 添加3D缓慢旋转、尾巴连中心、小红书原创标注 |
| 2026-10-17 22:01 | [`0246b2b`](https://github.com/furryyueyue/furryhk/commit/0246b2b6b84e49a9fd45029f4569bd3a52140cd5) | fix: 返回主页链接指向主站https://furryhk.cn |
| 2026-10-17 21:10 | [`45e6b92`](https://github.com/furryyueyue/furryhk/commit/45e6b92783df414368a494b64791de0236af35db) | Smooth both directions of homepage and dandelion navigation |
| 2026-10-17 20:47 | [`e7b8508`](https://github.com/furryyueyue/furryhk/commit/e7b8508b0b57c7dd10524bddf0e68fef83dcf199) | Add smooth homepage-to-game opening transitions |
| 2026-10-17 20:34 | [`bbcb517`](https://github.com/furryyueyue/furryhk/commit/bbcb517a8e5c22c037fb1c45a394181e13d6d965) | Add text dandelion playground and finalize homepage footer |
| 2026-10-17 19:42 | [`f59bd58`](https://github.com/furryyueyue/furryhk/commit/f59bd582ea982b766cfe701e8905bab71e6d2598) | Add footer bug feedback email link with prefilled subject |
| 2026-10-17 19:37 | [`fef2fc9`](https://github.com/furryyueyue/furryhk/commit/fef2fc9d74d38c59b48bb0e457e97ef05681eb9a) | Prevent horizontal overflow on very narrow screens |
| 2026-10-17 19:32 | [`4921317`](https://github.com/furryyueyue/furryhk/commit/4921317bc524266602a70a03ad8a7a3f36328912) | Move friend links directly above the milk tea support section |
| 2026-10-07 14:26 | [`dd0fd83`](https://github.com/furryyueyue/furryhk/commit/dd0fd83c2c2c02b4746062adcad538afdfe94276) | Resize friend QR codes and show them fully |
| 2026-10-07 14:21 | [`81422e5`](https://github.com/furryyueyue/furryhk/commit/81422e5b71e2d6efa68cc3c9810f51d482d44485) | Polish friend links colors, rounded cards and reveal animation |
| 2026-10-07 13:36 | [`4c36abf`](https://github.com/furryyueyue/furryhk/commit/4c36abfb7a0a4a18711fe49e88f75b275f7b1855) | Fill friend WeChat 3/3 |
| 2026-10-07 13:35 | [`76c4147`](https://github.com/furryyueyue/furryhk/commit/76c414738866f7ff3fee374310ac5328c589cf65) | Fill friend WeChat 2/3 |
| 2026-10-07 13:34 | [`8dad80b`](https://github.com/furryyueyue/furryhk/commit/8dad80b0f2efeff006772f8942d4aea49409f6bf) | Fill friend WeChat 1/3 |
| 2026-10-07 13:33 | [`f496485`](https://github.com/furryyueyue/furryhk/commit/f49648585adeae33543f23fd6cf2a87f47a24d97) | Fill friend QQ 3/3 |
| 2026-10-07 13:32 | [`af875b0`](https://github.com/furryyueyue/furryhk/commit/af875b04353b241d1ebb71af2efcfb358ddff9e8) | Fill friend QQ 2/3 |
| 2026-10-07 13:31 | [`5c5fb77`](https://github.com/furryyueyue/furryhk/commit/5c5fb77de02c70e748a24ebe6b24edd67af83339) | Fill friend QQ 1/3 |
| 2026-10-07 13:30 | [`23b777f`](https://github.com/furryyueyue/furryhk/commit/23b777f5f12ba6cd04997998db1afd4d1dcee828) | Fill friend avatar 2/2 |
| 2026-10-07 13:29 | [`3b30d61`](https://github.com/furryyueyue/furryhk/commit/3b30d61f4be82596f607b9d2a28b7da3d1903286) | Fill friend avatar 1/2 |
| 2026-10-07 13:26 | [`db906fc`](https://github.com/furryyueyue/furryhk/commit/db906fcbe06eb161099ae0df3f1243269b674246) | Stage friends links section |
| 2026-10-04 14:45 | [`0e9ee09`](https://github.com/furryyueyue/furryhk/commit/0e9ee0971958cc4f413b1a68ab89ab24feaba2a6) | 明确头像网站图标尺寸并统一搜索及分享预览头像 |
| 2026-10-04 14:36 | [`03e3add`](https://github.com/furryyueyue/furryhk/commit/03e3addab23753a407ffd8609d046286c4571b36) | 在萌ICP备案链接前添加同色爪印装饰 |
| 2026-10-04 13:41 | [`a3246d5`](https://github.com/furryyueyue/furryhk/commit/a3246d50a253f977a4dafb2d12b2529f505f1859) | Add automatic IndexNow notifications |
| 2026-10-04 13:41 | [`44ccd06`](https://github.com/furryyueyue/furryhk/commit/44ccd062d2660279d32c490814cc01e8b1389300) | Add IndexNow verification key |
| 2026-10-04 13:40 | [`dea4c1a`](https://github.com/furryyueyue/furryhk/commit/dea4c1a7516466aaa444d23d6961d008c1ad025a) | Add sitemap for search engine discovery |
| 2026-10-04 13:40 | [`0343bed`](https://github.com/furryyueyue/furryhk/commit/0343bed293e227604bb2b34d678eef4e85e90ee9) | Add robots.txt for search engine crawling |
| 2026-10-04 13:40 | [`2fc05aa`](https://github.com/furryyueyue/furryhk/commit/2fc05aa826485a99c678f337c6f24f76213a0f37) | Improve homepage SEO and search engine metadata |
| 2026-10-04 13:12 | [`09027c3`](https://github.com/furryyueyue/furryhk/commit/09027c346063f5d8f59ff7f4f4f77060b5864f69) | 显示企鹅号并以原文件名重建高清联系二维码 |
| 2026-10-04 08:34 | [`ffb584a`](https://github.com/furryyueyue/furryhk/commit/ffb584a2c2532531d5aeea0cd400bda89de0866d) | 补回三个 template 缺失的 &lt;/div&gt; 闭合，完善页脚备案布局 |
| 2026-10-04 08:28 | [`637436b`](https://github.com/furryyueyue/furryhk/commit/637436ba122e4d32ca7f6a0d8ca2ae2535ab4015) | 修正页脚布局（备案号换行、删句号）并修复两处样式笔误 |
| 2026-10-04 08:25 | [`d3593e4`](https://github.com/furryyueyue/furryhk/commit/d3593e4aed6af188f8e514ff89bbb27a64700cae) | 修复打赏按钮展开判断（classList.contains） |
| 2026-10-04 08:21 | [`30dd603`](https://github.com/furryyueyue/furryhk/commit/30dd6030e3fa3827cf22730a8516f48b489abce8) | 页脚祝福语删句号，备案号移至下一行 |
| 2026-10-04 08:13 | [`ae443d0`](https://github.com/furryyueyue/furryhk/commit/ae443d041df7d9125b5f85a2977fb0fea2938f5d) | 页脚添加萌ICP备20268806号链接 |
| 2026-10-03 03:07 | [`dd4e6d6`](https://github.com/furryyueyue/furryhk/commit/dd4e6d62f3321e84f1c628f977d3df9e884bc547) | Fix animation fallback and QR resize layout |
| 2026-10-03 02:40 | [`976c7a0`](https://github.com/furryyueyue/furryhk/commit/976c7a0b33ea82f0f0a998d021ab3baec8514c44) | Center and enlarge tablet layout with gentle reward reveal |
| 2026-10-03 02:32 | [`5375aa4`](https://github.com/furryyueyue/furryhk/commit/5375aa44dd991dbb4625917f241a104b1b4649fd) | Refine landscape tablet spacing |
| 2026-10-03 02:31 | [`c9672a8`](https://github.com/furryyueyue/furryhk/commit/c9672a8840b31cace69a382cb3cb56ab5ac77520) | Keep QR image flight outside dialog scroll bounds |
| 2026-10-03 02:29 | [`8e802a4`](https://github.com/furryyueyue/furryhk/commit/8e802a443e7381ec338857e262f95d4c446be584) | Preserve QR aspect ratio and add landscape two-column layout |
| 2026-10-03 02:18 | [`fa2998d`](https://github.com/furryyueyue/furryhk/commit/fa2998d4ad310ed0d49e8fd2c1ebf480678b5ca7) | Animate the rendered QR image into and out of the viewer |
| 2026-10-03 02:09 | [`e9f1415`](https://github.com/furryyueyue/furryhk/commit/e9f1415d9b65860fe45157e96aca84479af76425) | Open QR images promptly and refine tap feedback |
| 2026-10-03 02:02 | [`7716dd1`](https://github.com/furryyueyue/furryhk/commit/7716dd1f0cd7e1aea41ae8fb8dccde11380fbcfa) | Keep click emoji visible above cards for a full beat |
| 2026-10-03 01:11 | [`eb33094`](https://github.com/furryyueyue/furryhk/commit/eb330944fbb8ff3c2ac6d8101bd802b056463eff) | Redesign homepage with smooth reveals and emoji feedback |
| 2026-10-02 23:48 | [`68beefe`](https://github.com/furryyueyue/furryhk/commit/68beefe4748609f5a7153347b95a560750f73da2) | Remove homepage loading screen and completion notice |
| 2026-09-27 03:29 | [`f0cbf53`](https://github.com/furryyueyue/furryhk/commit/f0cbf53c48e19930b28d56733c6c561bc6576d60) | Polish post-load notice behavior |
| 2026-09-27 03:29 | [`a2904f3`](https://github.com/furryyueyue/furryhk/commit/a2904f39032390f0fae2c201a8d2a9933127ad4b) | Fix stray character and show post-load notice |
| 2026-09-27 03:19 | [`6e893ea`](https://github.com/furryyueyue/furryhk/commit/6e893ea95ee0ea23f73458825e4923369d734790) | Match contact panel open and close animation |
| 2026-09-27 03:16 | [`b531ecf`](https://github.com/furryyueyue/furryhk/commit/b531ecfa2a27e60e3ba4dacc5f5280fe6ffd7f16) | Handle rapid contact changes while panel is collapsing |
| 2026-09-27 03:15 | [`5febe79`](https://github.com/furryyueyue/furryhk/commit/5febe79b5776cf3721893dd41784946bfd8135eb) | Synchronize contact switching with panel transition |
| 2026-09-27 03:12 | [`865e9ca`](https://github.com/furryyueyue/furryhk/commit/865e9caaa93d40813cec2f7686e372f5005e46d0) | Reduce mobile rendering load and preserve glass styling |
| 2026-09-27 03:11 | [`69a2c29`](https://github.com/furryyueyue/furryhk/commit/69a2c29c5266b0dcc5a2f4942bf3b455b5fff219) | Prevent contact accordion from overlapping page sections |
| 2026-09-27 03:09 | [`f351e35`](https://github.com/furryyueyue/furryhk/commit/f351e35e14e895f95e4f473c3c4d0fdd792845a6) | Stabilize contact panel animation and refine system font stack |
| 2026-09-27 03:05 | [`5cc744f`](https://github.com/furryyueyue/furryhk/commit/5cc744f82d6cc7c2436fe866ab0b587c1a49bed4) | Round contact panels and unify emoji artwork |
| 2026-09-27 02:56 | [`44ed6af`](https://github.com/furryyueyue/furryhk/commit/44ed6af2b7440eec22f4466eecc09b48496e56d8) | Smooth homepage animations and update feature teaser |
| 2026-09-27 02:51 | [`f11e5dd`](https://github.com/furryyueyue/furryhk/commit/f11e5dd1e0d7bd7d7ca1a00a2b85e36646bfb58f) | Fix intro progress script and defer profile images |
| 2026-09-27 02:49 | [`ef78cf3`](https://github.com/furryyueyue/furryhk/commit/ef78cf31128d3cc5852b064004b893bffc29f1f0) | Preload profile images and randomize intro duration |
| 2026-09-27 02:47 | [`1a321b3`](https://github.com/furryyueyue/furryhk/commit/1a321b34ed42708cf16328c721c68085c3c64787) | Use accurate page-loading language on the intro screen |
| 2026-09-27 02:45 | [`609fc76`](https://github.com/furryyueyue/furryhk/commit/609fc76d4948387031ff243fd268d67eb8be69dd) | Hide homepage behind a misty loader and label simulated check |
| 2026-09-27 02:43 | [`3cf5021`](https://github.com/furryyueyue/furryhk/commit/3cf5021ddd8d8458a34491a1d03a1255c1c89016) | Show only a loading ring and smooth payment-style success check |
| 2026-09-27 02:41 | [`066885e`](https://github.com/furryyueyue/furryhk/commit/066885eb546c424e6031f0d372915dfc38d5373a) | Replace welcome loader with five-second demo security check |
| 2026-09-27 02:38 | [`47e969d`](https://github.com/furryyueyue/furryhk/commit/47e969db4c67e2f09d296375c054003f14383206) | Set the homepage reveal to a slower slide-in |
| 2026-09-27 02:37 | [`a95a271`](https://github.com/furryyueyue/furryhk/commit/a95a2719839b223d22090a08e93cd484e2ce4cb6) | Refine slow glassy entrance and disable avatar zoom |
| 2026-09-27 02:35 | [`6828b32`](https://github.com/furryyueyue/furryhk/commit/6828b3278372ad4c6c67d2d7b4d09353e1b23ab7) | Tighten homepage animation and external link handling |
| 2026-09-27 02:34 | [`378624b`](https://github.com/furryyueyue/furryhk/commit/378624b8e50c9f9dee3406a06620d87476587de7) | Polish personal homepage and fix contact panel transitions |
| 2026-08-31 20:22 | [`37b5cfe`](https://github.com/furryyueyue/furryhk/commit/37b5cfe2aefcb87409ac56891019056ad7aced23) | Remove commission customization area from index.html  Removed the commission customization section and its related JavaScript functionality. |
| 2026-08-31 17:44 | [`0427760`](https://github.com/furryyueyue/furryhk/commit/0427760eea71a1a9c1311ddcaa13e8de321419ce) | Add commission customization section to index.html |
| 2026-08-31 17:36 | [`4a08a65`](https://github.com/furryyueyue/furryhk/commit/4a08a654e1559f4fb0b8895ab478e68e697f2646) | Implement custom commission area in index.html  Added a custom commission section with dynamic content display. |
| 2026-07-14 12:06 | [`c47e1d3`](https://github.com/furryyueyue/furryhk/commit/c47e1d313d4b883b6dcd713850b5657d0c34b6bb) | Update index.html |
| 2026-06-27 19:51 | [`e1501bd`](https://github.com/furryyueyue/furryhk/commit/e1501bd7cba767d531679d0e9589d5a73cf33031) | Delete CNAME |
| 2026-06-25 23:00 | [`5e72668`](https://github.com/furryyueyue/furryhk/commit/5e72668c0799d07dbc59a63d7d5948e3564fa4f8) | 图片没点开bug拉完了😡 |
| 2026-06-24 19:22 | [`34c37f4`](https://github.com/furryyueyue/furryhk/commit/34c37f4449d6caaf3ed90f0a4f197e108ddf8013) | Update index.html |
| 2026-06-24 19:19 | [`6c3ddb0`](https://github.com/furryyueyue/furryhk/commit/6c3ddb01e4b5f0653eb6b98b2b4593cfabe9eaa3) | Delete mail-terms.html |
| 2026-06-24 19:04 | [`bab3c6d`](https://github.com/furryyueyue/furryhk/commit/bab3c6dc244e232ec97d6f882dfd8e2a82b1e97b) | Delete mail |
| 2026-06-24 18:52 | [`e20587b`](https://github.com/furryyueyue/furryhk/commit/e20587b2fcfc58398c3ee8f3fabe7422855456a6) | Create mail |
| 2026-06-24 18:32 | [`fb39f7c`](https://github.com/furryyueyue/furryhk/commit/fb39f7c376f15213688d54a52712dd8a282ace3d) | Rename 744761a6c6cbdfcca6865e96e0f284c2.html to mail-terms.html |
| 2026-06-24 18:31 | [`32daa22`](https://github.com/furryyueyue/furryhk/commit/32daa226ef9aef165985b1a0f681e528a3f5e65b) | Add files via upload |
| 2026-06-24 18:22 | [`19cb31c`](https://github.com/furryyueyue/furryhk/commit/19cb31c67b38c3ccab169f9767479f0830024df7) | Rename 主页.html to index.html |
| 2026-06-24 18:17 | [`0d19b5b`](https://github.com/furryyueyue/furryhk/commit/0d19b5bacb9d044d34865abf775a61489d131b54) | Update and rename Code_20260624.html to 主页.html |
| 2026-06-24 18:12 | [`6a05e71`](https://github.com/furryyueyue/furryhk/commit/6a05e710f421809ba453ba7c1024b149ba550005) | Add files via upload |
| 2026-06-24 18:11 | [`fad55e2`](https://github.com/furryyueyue/furryhk/commit/fad55e21bdd62b88fe804786e8e244823424edae) | Delete index.html |
| 2026-06-24 18:10 | [`0c171ba`](https://github.com/furryyueyue/furryhk/commit/0c171ba2adb64b77984642d9632d18b782ac7e67) | Delete furryhk_github_pages_template.zip |
| 2026-06-23 20:07 | [`b7be9d8`](https://github.com/furryyueyue/furryhk/commit/b7be9d8322127cfe72c2c58675dbc72a8308ded3) | Rename loaderio-1e6d107e4a77d6d430a1a95dcc2695b8 to loaderio-1e6d107e4a77d6d430a1a95dcc2695b8.txt |
| 2026-06-23 20:06 | [`7c9a297`](https://github.com/furryyueyue/furryhk/commit/7c9a29744c8b56df9c85041fa0f2b8d53bcf04f8) | Rename loaderio-3ad31bef962e736d10cf87a89bb7e8ec.txt to loaderio-1e6d107e4a77d6d430a1a95dcc2695b8 |
| 2026-06-23 20:04 | [`7257ce6`](https://github.com/furryyueyue/furryhk/commit/7257ce6b53eb69046df5e8a4ebfdcb618d4268e0) | Update loaderio-3ad31bef962e736d10cf87a89bb7e8ec.txt |
| 2026-06-23 20:04 | [`be3350b`](https://github.com/furryyueyue/furryhk/commit/be3350bb8db0840b003fe6cb63297a50d56b0a51) | Add files via upload |
| 2026-06-23 19:00 | [`4dc14d2`](https://github.com/furryyueyue/furryhk/commit/4dc14d28d0c2211de3f4de0ad7758ea0b2da890f) | Update CNAME |
| 2026-06-23 14:29 | [`4b8b4fa`](https://github.com/furryyueyue/furryhk/commit/4b8b4fa09b430aa3c5ffe30b7fddd481fe2cac5f) | Delete loaderio-3ad31bef962e736d10cf87a89bb7e8ec.txt |
| 2026-06-23 14:12 | [`3741d4b`](https://github.com/furryyueyue/furryhk/commit/3741d4b00c2359450c34edb4cd6512016316b9ef) | Update loaderio-3ad31bef962e736d10cf87a89bb7e8ec.txt |
| 2026-06-23 14:04 | [`142afbe`](https://github.com/furryyueyue/furryhk/commit/142afbe7d57638093a46f9341ea7b9dbff75c1c4) | Add files via upload |
| 2026-06-23 14:04 | [`16d895d`](https://github.com/furryyueyue/furryhk/commit/16d895d35e7f7d1a20aa8d38d5ac7a47afe5d706) | Add files via upload |
| 2026-06-21 09:02 | [`3936c87`](https://github.com/furryyueyue/furryhk/commit/3936c87eac36b6bc35aff52864aaed158faa2c18) | Create CNAME |
| 2026-06-21 08:59 | [`ca43535`](https://github.com/furryyueyue/furryhk/commit/ca435351929d0e33a3ef67f70754fdd187a2aa08) | Delete CNAME |
| 2026-06-21 08:23 | [`10daa59`](https://github.com/furryyueyue/furryhk/commit/10daa59a4c0f72d25e93f057060bbbadb64d2164) | Create CNAME |
| 2026-06-21 08:17 | [`8ef105c`](https://github.com/furryyueyue/furryhk/commit/8ef105c7087a81df1ff7cfb89d7fa49b59fc8c57) | Update image source in index.html |
| 2026-06-21 08:12 | [`b776d57`](https://github.com/furryyueyue/furryhk/commit/b776d5734db0bee8e45dbe7fd144a43844d06530) | Update index.html |
| 2026-06-21 08:10 | [`b9719cb`](https://github.com/furryyueyue/furryhk/commit/b9719cbbdcd46e3bb9909ecd7110130221ac65d9) | 头像 |
| 2026-06-21 08:03 | [`0647a22`](https://github.com/furryyueyue/furryhk/commit/0647a22a5d3a75e1bd219c7adf31d61d55cc81cc) | 图片 |
| 2026-06-21 00:26 | [`3669bdf`](https://github.com/furryyueyue/furryhk/commit/3669bdfa921c4c079dd582bae7e9bf806d7b3f90) | Add files via upload |
| 2026-06-21 00:23 | [`7304a76`](https://github.com/furryyueyue/furryhk/commit/7304a76d63f53069c22b4085d74894c7e5ef60ff) | Create images |
| 2026-06-21 00:19 | [`274cd9d`](https://github.com/furryyueyue/furryhk/commit/274cd9d2fe0ce4e0a33d0b641c524fe8feed831d) | Add files via upload |

</details>
