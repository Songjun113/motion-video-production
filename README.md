# Motion Video Production

![Motion Video Production](docs/readme-banner.png)

让 Codex 把论文、产品界面、数据或创意制作成完整动效视频。默认先确认分镜与关键静帧，再制作动画和声音、检查编码后的 MP4。技术路线根据内容与运行环境选择。

## 公开展示案例

本仓库以 Ding 等发表于 **Nature Communications (2025)** 的 [EEG 单指实时机器人手控制研究](https://doi.org/10.1038/s41467-025-61064-x) 为示例。视频展示从脑电、解码到机器人手指动作的过程，采用明亮画面、变化构图、独立对象动画与合成音效。

新案例正在制作，完成后将在这里提供实际分镜、完整 MP4 和可运行源码。

## 安装到 Codex

把仓库放入 `$CODEX_HOME/skills/motion-video-production`；未设置 `CODEX_HOME` 时，默认位置为 `~/.codex/skills/motion-video-production`。

Windows PowerShell：

```powershell
$skillRoot = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $env:USERPROFILE '.codex/skills' }
git clone https://github.com/Songjun113/motion-video-production.git (Join-Path $skillRoot 'motion-video-production')
```

如果已安装同名 Skill，请先备份并检查已有修改再更新。新建 Codex 会话后使用 `$motion-video-production` 调用。

## 使用

```text
使用 $motion-video-production，为附件论文制作 20 秒横屏动效视频。
采用明亮的产品宣传风格，突出问题、机制和主要结果。
先给我分镜及关键静帧，确认后交付带音效的完整 MP4。
```

希望连续完成时，加上：`直接出片，无需中途确认。`

Skill 会根据任务选择 Web / Canvas / SVG、Remotion、HyperFrames、Python、FFmpeg、Blender 或混合路线。实际可用的渲染器取决于环境；附带的 Python 案例仅需本地依赖。

## 工作流程

1. 提炼内容，核实数据与素材来源。
2. 设计视觉风格、分镜、关键静帧和对象转场。
3. 确认后制作分层动画、字幕和声音。
4. 输出 MP4，检查时长、分辨率、帧率、完整解码、画面及音频。

## 内容来源

- Yidan Ding, Chalisa Udompanyawit, Yisha Zhang & Bin He (2025). *EEG-based brain-computer interface enables real-time robotic hand control at individual finger level*. Nature Communications 16, 5401. DOI: [10.1038/s41467-025-61064-x](https://doi.org/10.1038/s41467-025-61064-x).
- 论文采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)；视频为原创示意性解说动画，数据含义及人群范围见案例说明。
- 封面是 AI 生成的项目展示图，[提示词](docs/banner-prompt.md)已保留。

仓库未指定软件开源许可证；第三方论文许可不自动适用于仓库全部代码。
