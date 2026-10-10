# ggplot2 语法速查与数据预处理（源自 1.6 节 + 第 2 章）

> 来源：《R 语言数据可视化之美：专业图表绘制指南（增强版）》第 1 章 1.6 节「R 语言绘图基础」、第 2 章「R 语言数据处理基础」。
> 用途：生成或修改 ggplot2 代码时查阅语法细节；在绘图前整理数据。
> 代码片段均摘自原书，可直接运行。

## B. ggplot2 语法体系（1.6 节，p.30–61）

### B1. 基础语法结构与 aes() 映射规则

语法框架：数据绘图部分 + 美化细节部分（图 1-6-1）`(p.30)`。特点：① 图层式设计，`ggplot()` 起始，图层间用 `+` 叠加，**越往后图层越在上方**；② 表征数据与图形细节分开，`stat_xxx()` 把统计变换融入绘图；③ 扩展包丰富（颜色/字体/主题）`(p.30)`。

必需输入（图 1-6-2）`(p.31)`：`ggplot()`——`DATA` 数据集（主要是 data.frame）、`MAPPINGS` 视觉通道映射（x、y 及 color/size/shape 等）、`STAT` 统计变换（默认 `"identity"` 无变换）、`POSITION` 位置调整（默认 `"identity"` 无调整）；`geom_xxx()` | `stat_xxx()` 几何图层或统计变换。
可选输入 5 项 `(p.31–32)`：`scale_xxx()` 度量、`coord_xxx()` 坐标变换（默认笛卡儿/直角）、`facet_xxx()` 分面、`guides()` 图例、`theme()` 主题。

```r
# 最小骨架（p.30 表 1-5-1 三种语法对照中的 ggplot2 写法）
ggplot(df, aes(x = SOD, y = tau)) + geom_point()                      # 散点图
ggplot(df, aes(SOD)) + geom_histogram(bins = 30, colour = "black",
                                      fill = "white")                 # 统计直方图
ggplot(df, aes(x = Class, y = SOD)) + geom_boxplot()                  # 箱形图
```

`ggplot()` 与 `geom()` 的继承关系 3 种情况 `(p.60–61)`：① 所有图层共享数据源与映射 → data/mapping 都写在 `ggplot()` 内，geom 自动继承（简单图表）；② 仅共享数据源 → data 写 `ggplot()` 内、各自的视觉通道映射写在各自 geom 内（较复杂图表）；③ 各图层独立 → 每个 geom 内都要写 data 和 mapping（高级图表 / 复杂地理信息多图层）。

```r
# ① 全部写在 ggplot 内（p.61）
ggplot(df1, aes(x, y, colour = x + y)) +
  geom_line(size = 1) + geom_point(shape = 16, size = 5) +
  guides(color = guide_colorbar(title = "Point\nLine"))
# ② 共享 data，各自 mapping（p.61）
ggplot(df1, aes(x, y)) +
  geom_line(aes(colour = x + y), size = 1) +
  geom_point(aes(fill = x + y), color = "black", shape = 21, size = 5) +
  scale_fill_distiller(name = "Point", palette = "YlOrRd") +
  scale_color_distiller(name = "Line", palette = "Blues")
# ③ 各自独立 data（p.61）
ggplot() +
  geom_line(aes(x, y, colour = x + y), df1, size = 1) +
  geom_point(aes(x, y, fill = x + y), df2, color = "black", shape = 21, size = 5)
```

**aes() 内部 vs 外部（关键规则）** `(p.44)`：**个性化映射（一一映射）**写在 `aes()` **内部**（每个观测值按指定变量值设定，即"增加一个维度"按颜色/大小/线条对每个记录值一一设定）；**统一设定（共性、统一化）**写在 `aes()` **外部**（所有观测值统一属性，如 `size = 5`、`linetype = "dash"`、`color = "blue"`，不消耗数据源任何维度）。

**视觉通道映射参数清单** `(p.34–35)`：`color/col/colour`（点、线、填充区域**轮廓**颜色）、`fill`（填充**区域**颜色）、`alpha`（透明度 0 完全透明→1 不透明）、`size`（点尺寸或线宽度，默认单位 pt；`geom_point()` 上加 `size` 映射即得**气泡图**）、`angle`（角度，仅 `geom_text()` 文本摆放角、`geom_spoke()` 短棒摆放角等有）、`vjust`（0="buttom"、0.5="middle"、1="top"）、`hjust`（0="left"、0.5="center"、1="right"，区间外数字微调比例不均）、`linetype`、`shape`。
注意：**`linetype`、`shape` 只适应于类别型变量** `(p.34–35)`。
- `linetype`：0=blank（白线）、1=solid（实线）、2=dashed（短虚线）、3=dotted（点线）、4=dotdash（点横线）、5=longdash（长虚线）、6=twodash（短长虚线）`(p.35)`。
- `shape`：`[0, 25]` 共 26 个整数（方/圆/三角/菱形等）；**只有 21~26 号点有 fill 属性，其余只有 color 轮廓属性** `(p.35)`。
- 非变量映射但重要：字体 `family`（内置仅 sans、serif、mono，扩展用 `extrafont` 包 / `showtext` 包）、字型 `fontface`（plain、bold、italic、bold.italic）`(p.38)`。

`geom_point()` 常用参数：`x`、`y`、`alpha`、`colour`、`fill`、`group`、`shape`、`size`、`stroke`（轮廓线条粗细）`(p.36)`。

表 1-6-2 元素归类（决定哪些映射能用）`(p.36)`：

| 元素 | geom 函数 | 类别型映射 | 数值型映射 |
|---|---|---|---|
| 点 | `geom_point()`、`geom_jitter()`、`geom_dotplot()` | color、fill、shape | color、fill、alpha、size |
| 线 | `geom_line()`、`geom_path()`、`geom_curve()`、`geom_density()`、`geom_linerange()`、`geom_step()`、`geom_abline()`、`geom_hline()` | color、linetype | color、size |
| 多边形 | `geom_polygon()`、`geom_rect()`、`geom_bar()`、`geom_ribbon()`、`geom_area()`、`geom_histogram()`、`geom_violin()` | color、fill | color、fill、alpha |
| 文本 | `geom_label()`、`geom_text()` | color | color、angle、vjust、hjust |

**视觉暗示精度排序（Cleveland & McGill, 1985）**——选映射时按精度从高到低 `(p.40–41)`：
位置 → 长度 → 角度 → 方向 → 面积 → 体积 → 饱和度 → 色相 → 纹理 → 形状。

### B2. 几何对象 geom_xxx 清单

表 1-6-1 按"输入变量数 × 变量类型"分类 `(p.33)`：

| 变量数 | 类型 | 函数 | 常用图表类型 |
|---|---|---|---|
| 1 | 连续型 | `geom_histogram()`、`geom_density()`、`geom_dotplot()`、`geom_freqpoly()`、`geom_qq()`、`geom_area()` | 统计直方图、核密度估计曲线图 |
| 1 | 离散型 | `geom_bar()` | 柱形图系列 |
| 2 | x-连续 / y-连续 | `geom_point()`、`geom_area()`、`geom_line()`、`geom_jitter()`、`geom_smooth()`、`geom_label()`、`geom_text()`、`geom_bin2d()`、`geom_hex()`、`geom_density2d()`、`geom_map()`、`geom_step()`、`geom_quantile()`、`geom_rug()` | 散点图系列、面积图系列、折线图系列，包括抖动散点图、平滑曲线图、文本、标签、二维统计直方图、二维核密度估计图、地理空间图表 |
| 2 | x-离散 / y-连续 | `geom_boxplot()`、`geom_violin()`、`geom_dotplot()`、`geom_col()` | 箱形图、小提琴图、点阵图、统计直方图 |
| 2 | x-离散 / y-离散 | `geom_count()` | 二维统计直方图 |
| 3 | x, y, z-连续 | `geom_contour()`、`geom_raster()`、`geom_tile()` | 等高线图、热力图 |

另有两类**未纳入该表** `(p.32–33)`：**图元（graphical primitive）系列**——`geom_curve()`、`geom_path()`、`geom_polygon()`、`geom_rect()`、`geom_ribbon()`、`geom_linerange()`、`geom_abline()`、`geom_hline()`、`geom_vline()`、`geom_segment()`、`geom_spoke()`，用于绘制矩形、多边形、线段等基本图表元素，供**创造新的图表类型**。**误差（error）展示系列**——`geom_crossbar()`（误差框）、`geom_errorbar()`（竖直误差线）、`geom_errorbarh()`（水平误差线）、`geom_pointrange()`（带误差棒的均值点），**必须先设置统计变换参数**才能自动根据数据计算均值与标准差。

### B3. stat_xxx 统计变换

`stat_xxx()` 在数据绘制前做聚合和其他计算；**一个 stat() 必须与一个 geom() 对应**才能计算 `(p.33)`。每个 `geom_xxx()` 都含 `stat` 参数，每个 `stat_xxx()` 都含 `geom` 参数 `(p.34)`。

```r
# 均值散点：两种写法等价（p.34）
# (a1) 以 stat_ 开头，指定 geom
ggplot(mydata, aes(Class, Value, fill = Class)) +
  stat_summary(fun.y = "mean", fun.args = list(mult = 1), geom = "point",
               color = "white", size = 4)
# (b1) 以 geom_ 开头，指定 stat
ggplot(mydata, aes(Class, Value, fill = Class)) +
  geom_point(stat = "summary", fun.y = "mean", fun.args = list(mult = 1),
             color = "white", size = 4)

# 带误差线散点：两种写法等价（p.34）
ggplot(mydata, aes(Class, Value, fill = Class)) +
  stat_summary(fun.data = "mean_sdl", fun.args = list(mult = 1),
               geom = "pointrange", color = "black", size = 1.2)
```

- `fun.data`：指定完整的汇总函数，输入数字向量、输出数据框，常见 4 种 `mean_cl_boot`、`mean_cl_normal`、`mean_sdl`、`median_hilow` `(p.34)`。
- `fun.y`：指定对 y 的汇总函数，输入数字向量、返回单个数字（median / mean 等），y 通常被分组，每组返回 1 个数字；不涉及统计变换时直接用 `geom_xxx()`，无须设 `stat`（默认 `stat = "identity"`）`(p.34)`。

### B4. 标度 scale_xxx（表 1-6-3 `(p.39)`）

默认度量为 `scale_xxx_identity()`；`scale_*_manual()` 表示**手动自定义离散度量**，适用于 colour、fill、alpha、linetype、shape、size `(p.38)`。

| 度量 | 数值型 | 类别型 |
|---|---|---|
| x / y 轴 | `scale_x/y_continuous()`、`scale_x/y_log10()`、`scale_x/y_sqrt()`、`scale_x/y_reverse()`、`scale_x/y_date()`、`scale_x/y_datetime()`、`scale_x/y_time()` | `scale_x/y_discrete()` |
| colour / fill | `scale_colour/fill_continuous()`、`scale_fill_distiller()`、`scale_colour/fill_gradient()`、`scale_colour/fill_gradient2()`、`scale_colour/fill_gradientn()`、`scale_colour/fill_discrete()`、`scale_colour/fill_brewer()`、`scale_colour/fill_manual()` | 见左 |
| alpha | `scale_alpha_continuous()` / `scale_alpha_manual()` | `scale_alpha_discrete()` |
| linetype | — | `scale_linetype_discrete()`、`scale_linetype_manual()` |
| shape | — | `scale_shape()`、`scale_shape_manual()` |
| size | `scale_size()`、`scale_size_area()`、`scale_size_manual()` | — |

坐标轴度量**关键参数** `(p.50)`：
① `name` 指定坐标轴名称（也作为对应图例名）；② `breaks` 指定刻度位置（粗网格线位置）；③ `labels` 指定刻度标签内容；④ `limits` 指定显示范围（支持反区间）；⑤ `expand` 扩展显示范围；⑥ `trans` 指定变换函数（自带 `exp()`、`log()`、`log10()`，还支持 `scales::percent()` 百分比刻度及自定义）。

```r
# 坐标轴度量调整（p.50）
X 轴度量：scale_x_continuous(name = "Time(d)", breaks = seq(0, 20, 2))
Y 轴度量：scale_y_continuous(breaks = seq(0, 90, 10), limits = c(0, 90),
                              expand = c(0, 1))

# 线性 vs 对数（p.50–51）
scale_y_continuous(breaks = seq(0, 2.1, 0.5), limits = c(0, 2))   # 线性
scale_y_log10(name = 'log(value)', limits = c(0.00001, 10))       # 对数
```

对数尺度的适用判断 `(p.50)`：（1）数据有**数量级的差异**时，可同时显示很大和很小的数据；（2）数据有**指数增长或幂定律**特性时，可将曲线变为直线。典型：里氏震级、音量、光强度、溶液 pH `(p.50)`。

```r
# size / fill / shape 度量调整（p.40）
ggplot(df, aes(x = SOD, y = tau, size = age)) +
  geom_point(shape = 21, color = "black", fill = "#FF0000", stroke = 0.25, alpha = 0.8) +
  scale_size(range = c(1, 8))                       # range = 气泡面积映射显示范围

ggplot(df, aes(SOD, tau, fill = age, size = age)) +
  geom_point(shape = 21, colour = "black", stroke = 0.25, alpha = 0.8) +
  scale_size(range = c(1, 8)) +
  scale_fill_distiller(palette = "Reds", direction = 0)   # direction=0 由浅到深

ggplot(df, aes(x = SOD, y = tau, fill = Class)) +
  geom_point(shape = 21, size = 3, colour = "black", stroke = 0.25) +
  scale_fill_manual(values = c("#36BED9", "#FF0000", "#FBAD01")) +
  scale_shape_manual(values = c(21, 22, 23))
```
（`scale_fill_distiller(palette = "Reds")` 需先加载 RColorBrewer 包 `(p.39)`。）

标尺类型（图 1-6-17 `(p.49)`）：数字标尺（线性 / 对数 / 百分比）、分类标尺（分类 / 顺序）、时间标尺（月、日、小时）。
柱形图 = X 分类标尺 + Y 数字标尺；条形图 = X 数字标尺 + Y 分类标尺；饼图与圆环图也是数字 + 分类的组合 `(p.51)`。

### B5. 坐标系 coord_xxx

三类常用坐标系：直角坐标系、极坐标系、地理坐标系 `(p.44)`。

**直角坐标系** 4 种 `(p.45)`：`coord_cartesian()`（**默认**，其他坐标系都由直角坐标系画图后变换而来）；`coord_fixed()` 固定纵横比，**绘制华夫饼图和复合型散点饼图时需 `coord_fixed(ratio = 1)`**；`coord_flip()` 翻转 X/Y 轴，把竖直柱形图转成水平**条形图**，也用于**水平箱形图**；`coord_trans()` 刻度比例尺变化（应用很少，可把曲线变成直线；数据在某轴方向密集程度变化时可调节使数据点集中显示）。

**极坐标系** `(p.46–47)`：雷达图、饼图、南丁格尔玫瑰图（极坐标柱形图/堆积柱形图）都是极坐标系。

```r
# 极坐标（p.47）；theta 为要极坐标化的中心轴：X 轴→圆周，Y 轴→半径
coord_polar(theta = "x", start = 0, direction = 1, clip = "on")
# direction=1 顺时针，-1 逆时针；start 为起始角度（距 12 点针的弧度）
# 注意：极坐标转化比较耗费计算机资源，最好先清空内存：
rm(list = ls()); gc()
```

极坐标 vs 直角坐标的选择 `(p.48)`：极坐标可将数据 365 度围绕圆心排列，便于看**周期、方向**上的变化趋势；**对连续时间段的变化趋势的显示则不如直角坐标系**。

**地理坐标系** `(p.48, p.83)`：`coord_quickmap()` 保留经纬直线的快速近似绘制，**最适合靠近赤道的较小区域**；`coord_map()` 通过 `projection` 设定投影（墨卡托、兰勃特等角圆锥、Albers 等积正割圆锥、等距圆柱、正交投影等）。常用投影（共 20 多种）：墨卡托（正轴等角圆柱，等角、航海图常用，但**面积变形，极点比例达无穷大**）、兰勃特等角割圆锥、阿伯斯正轴等积割圆锥、等距圆柱 `(p.47)`。

三维/高维扩展 `(p.45)`：`GGally::ggparcoord()` 绘制**平行坐标系**，用于高维几何与多元数据可视化。

### B6. 分面 facet_xxx

`facet_xxx()`：分面系统，将某个变量进行分面变换，包括**按行、按列和网格**形式分面绘图；书中说明这部分详见第 8 章 8.2 节 `(p.31)`。（第 1 章未给出分面代码，仅列语法位；数据示例 `Facet_Data.csv`，含 tau、SOD、age、Class 四列 `(p.36)`。）

### B7. 图例 theme / guide

`guide_colorbar()` / `guide_colourbar()` 调整**连续变量**图例；`guide_legend()` 用于**离散变量**图例，也可用于连续变量 `(p.53)`。`guides()` 把两种图例嵌套进去，`guides(fill = guide_colorbar())` 在**多图例共同处理时尤为有效**；也可在 `scale_xxx()` 中指定 `guide = "colorbar"` 或 `guide = "legend"` `(p.54)`。

```r
# 图例位置（p.54）——图 1-6-23(a) 默认：白色矩形背景 + 右侧
theme(legend.background = element_rect(fill = "white"),
      legend.position = "right")
# 图例放图表内部左上角，背景设为无；c(0.2, 0.8) = X 方向 20%、Y 方向 80%
theme(legend.background = element_blank(),
      legend.position = c(0.2, 0.8))
```
`legend.position` 取值：`"none"`（无图例）、`"left"`、`"right"`（默认）、`"bottom"`、`"top"`；也可用两个元素的数值向量（0~1）控制图例在图表中间的具体位置，**超出数值往往导致图例隐藏**；若用数值向量把图例放进图表内部，**最好同时把 legend.background 设为透明或无** `(p.54)`。

### B8. 主题系统 theme()

主题系统主要对象分**文本（text）、矩形（rect）、线条（line）**三大类，对应 `element_text()`、`element_rect()`、`element_line()`，另 `element_blank()` 表示该对象设置为无 `(p.55)`。

- `element_text()`（参数 family, face, colour, size, hjust, vjust, angle, lineheight）→ `plot.title/subtitle/caption`、`axis.title(.x/.y)`、`axis.text(.x/.y)`、`legend.text(.align/title)`、`strip.text(.x/.y)`。
- `element_rect()`（参数 colour, size, type）→ `plot.background/spacing/margin`、`panel.background/border/spacing`、`legend.background/margin/spacing(.x/.y)`、`strip.background`。
- `element_line()`（参数 fill, colour, size, type）→ `panel.grid.major/minor(.x/.y)`、`axis.line(.x/.y)`、`axis.ticks(.x/.y/length/margin)`。
- 高频：`axis.text.x`（极坐标柱形图、径向柱形图 X 轴标签旋转角度）、`axis.text.y`（时间序列峰峦图 Y 轴标签替换）、`legend.position`、`legend.background` `(p.55)`。

**可用主题清单** `(p.56)`：ggplot2 自带 `theme_gray()`、`theme_minimal()`、`theme_bw()`、`theme_light()`、`theme_test()`、`theme_classic()`；模板包 `ggthemes`、`ggtech`、`ggthemer`、`ggsci`（**专门为学术图表开发**，https://nanx.me/ggsci/articles/ggsci.html）、`cowplot`。
交互工具：`ggThemeAssist` 包（需先装 `shiny`，RStudio → Tools → Addins → "ggplot Theme Assistant"，Done 后输出主题代码，注意可能少括号或引号）`(p.56)`；新手绘图插件 `esquisse`，`devtools::install_github("dreamRs/esquisse")`，启动 `esquisse:::esquisser()` 或 Tools → Addins → "ggplot2 builder" `(p.59–60)`。（书中 1.6 节**未出现 ggpubr**。）

**风格选择建议** `(p.56–57)`：
- `theme_gray()`（ggplot2 默认风格：绘图区背景 RGB(229,229,229) 灰色，主网格线 RGB(255,255,255)、次网格线 RGB(242,242,242)）→ **适合 PPT 演示**；
- `theme_classic()` / `theme_test()`（背景 RGB(255,255,255) 白色，无主次网格线，classic 还去掉绘图区边框）→ **适合学术论文**；图表尺寸较小时仍能清晰表达，不会因背景线条太多而显凌乱。

### B9. 位置调整 position

`geom_xxx()` 中 `position` 表示绘图数据系列的位置调整，默认 `"identity"`（无位置调整），**在柱形图和条形图系列中经常用到**（簇状柱形图、堆积柱形图、百分比堆积柱形图）`(p.58)`。

| 函数 | 功能 | 参数说明 |
|---|---|---|
| `position_dodge()` | 水平并列放置 | `position_dodge(width = NULL, preserve = ("total","single"))`；作用于簇状柱形图 `geom_bar()`、箱形图 `geom_boxplot()` 等 |
| `position_identity()` | 位置不变 | 散点图、折线图可行（默认）；**多分类柱形图会出现序列遮盖，不可行** |
| `position_stack()` | 垂直堆叠 | `position_stack(vjust = 1, reverse = FALSE)`；柱形图和面积图默认 stack 堆积 |
| `position_fill()` | 百分比填充 | `position_fill(vjust = 1, reverse = FALSE)`；垂直堆叠，但**只能反映各组百分比** |
| `position_jitter()` | 扰动处理 | `position_jitter(width = NULL, height = NULL)`；部分重叠，作用于散点图 |
| `position_jitterdodge()` | 并列抖动 | `position_jitterdodge(jitter.width = NULL, jitter.height = 0, dodge.width = 0.75)`；**仅用于箱形图和散点图在一起的情形，有顺序：必须箱形在前、散点在后，抖动只能用在散点几何对象中** |
| `position_nudge()` | 整体位置微调 | `position_nudge(x = 0, y = 0)`；整体向 x/y 平移，常用于 `geom_text()` 文本对象 |

```r
# 构造数据（p.58）
N <- 100
df <- data.frame(group = rep(c(1, 2), each = N * 2),
                 y = append(append(rnorm(N, 5, 1), rnorm(N, 2, 1)),
                            append(rnorm(N, 1, 1), rnorm(N, 3, 1))),
                 x = rep(c("A", "B", "A", "B"), N))

# 1. 未调整间距（p.59）
ggplot(df, aes(x = x, y = y, fill = as.factor(group))) +
  geom_boxplot(outlier.size = 0, colour = 'black') +
  geom_jitter(aes(group = as.factor(group)), shape = 21, alpha = 0.5)

# 2. 只调整抖动散点间距（p.59）
ggplot(df, aes(x = x, y = y, fill = as.factor(group))) +
  geom_boxplot(outlier.size = 0, colour = 'black') +
  geom_jitter(aes(group = as.factor(group)), shape = 21, alpha = 0.5,
              position = position_jitterdodge())

# 3. 同时调整箱形图与抖动散点间距（p.59）——推荐写法
ggplot(df, aes(x = x, y = y, fill = as.factor(group))) +
  geom_boxplot(position = position_dodge(0.75), outlier.size = 0, colour = 'black') +
  geom_jitter(aes(group = as.factor(group)), shape = 21, alpha = 0.5,
              position = position_jitterdodge(dodge.width = 0.75))
```


---

## D. 数据处理基础（第 2 章，p.85–92）

### D0. 包与函数总览 `(p.85)`

| 包 | 定位 | 常用函数 |
|---|---|---|
| base | 安装 R 自带，无须加载 | `transform()`、`rbind()`、`cbind()`、`merge()`、`apply()`、`aggregate()`、`sort()` |
| **dplyr** | Hadley Wickham 的 "a grammar of data manipulation"，专注 dataframe，速度更快 | `select()` 变量筛选、`filter()` 记录筛选、`arrange()` 排序、`mutate()` 变形（计算）、`summarize()` 汇总、`group_by()` 分组、`sample_n()`/`sample_frac()` 随机抽样、`%>%` 多步操作连接符；`bind_cols()`、`bind_rows()`；`left_join()`、`right_join()`、`inner_join()`、`full_join()` |
| **tidyr** | 常与 dplyr 共用，渐有取代 reshape2 之势 | `gather()` 宽→长、`spread()` 长→宽、`unite()` 多列合一列、`separate()` 一列分多列；`drop_na()`、`fill()` |
| **reshape2** | Hadley Wickham 的数据重构包 | `melt()`、`dcast()`、`add_margin()`；含 `french_fries` 数据集 |
| **tidyverse** | 2017 年创建的 R 包集合，核心为 ggplot2、dplyr、tidyr、readr、purrr、tibble、stringr、forcats | readr 读数据、tidyr 整理、dplyr 转换、ggplot2 可视化、purrr 函数式编程 `(p.85)` |

前置原则：使用 R ggplot2 绘图时**通常使用一维数据列表的数据框**；若导入的是二维数据列表，需用 `reshape2::melt()` 或 `tidyr::gather()` 转成一维 `(p.24, p.61)`。
一维 vs 二维判断：**看每一列是否是一个独立的参数**——是则一维，每列都是同类参数则二维 `(p.25)`。**建议数据录入时采用一维数据列表形式** `(p.25)`。

### D1. 表格的变换（宽 ↔ 长）(`p.85–86`)

```r
df <- data.frame(x = c('A','B','C'), '2010' = c(1,3,4), '2011' = c(3,5,2),
                 check.names = FALSE)

# 宽 -> 长：多行聚集成列，二维 -> 一维（p.86）
df_melt   <- reshape2::melt(df, id.vars = "x", variable.name = "year",
                            value.name = "value")
df_gather <- tidyr::gather(df, year, value, -x)
# id.vars("x")：标识观测的变量；variable.name("year")：保存原始变量名；value.name("value")：保存原始值

# 长 -> 宽：一列按变量展开为多行，一维 -> 二维（p.86）
df_dcast  <- reshape2::dcast(df_melt, x ~ year, value.var = "value")
df_spread <- tidyr::spread(df_gather, year, value)
# dcast 用公式 id.vars ~ variable.name 描述形状：左边 x，右边 year
```

### D2. 变量的变换（新增列）(`p.86–87`)

```r
# base::transform()：可新增列、改变原变量列的值，也可赋值 NULL 删除列变量（p.86）
dat1 <- transform(df_melt, value2 = value * 2)
# 结合向量化条件语句 ifelse()（p.87）
dat2 <- transform(df_melt, value2 = ifelse(year == "2011", value * 2, value))
# dplyr::mutate() 同效，且允许新列对刚刚建立起来的列进行计算（transform 做不到）
dat2 <- dplyr::mutate(df_melt, value2 = ifelse(year == "2011", value * 2, value))
```

### D3. 表格的排序 (`p.87`)

```r
# 向量排序（p.19, p.87）
Vec <- c(1, 4, 3, 5, 2)
order <- sort(Vec, index.return = TRUE, decreasing = TRUE)
# index.return=TRUE 返回排序索引；decreasing=TRUE 降序；$x=[5 4 3 2 1]，$ix=[4 2 3 5 1]

# 数据框按列排序（p.87）
dat_arrange1 <- dplyr::arrange(df_melt, value)         # 升序
dat_arrange2 <- dplyr::arrange(df_melt, desc(value))   # 降序
```

### D4. 表格的拼接（加行 / 加列）(`p.87–88`)

```r
df1 <- data.frame(x = c("a","b","c"), y = 1:3)
df2 <- data.frame(z = c("B","D","H"), g = c(2,5,3))
df3 <- data.frame(x = c("g","d"),     y = c(2,5))

dat_cbind <- cbind(df1, df2)   # 添加列 / 横向添加表格（p.88）
dat_rbind <- rbind(df1, df3)   # 添加行 / 纵向添加表格（p.88）
# dplyr 对应：bind_cols()、bind_rows()（p.87）
```

### D5. 表格的融合（需要共同列 common key）(`p.88–90`)

两个数据框不一致、不能简单 cbind/rbind 时，需要一个共同列作为融合依据 `(p.88)`。

```r
# merge()：优势是可对每个数据框指定不同匹配列名；缺点是运行速度比较慢（p.88）
dat_merge1 <- merge(df1, df2, by = "x", all = TRUE)
dat_merge2 <- merge(df1, df3, by.x = "x", by.y = "g")      # by.x 左表匹配列，by.y 右表匹配列
dat_merge3 <- merge(df1, df4, by = c("x","y"), all = TRUE)

# dplyr *_join() 系列（p.89）
dat_join1 <- dplyr::left_join(x = df1, y = df2, by = "x")   # 只保留左表所有数据
dat_join2 <- dplyr::right_join(x = df1, y = df2, by = "x")  # 只保留右表所有数据
dat_join3 <- dplyr::inner_join(x = df1, y = df2, by = "x")  # 只保留两表公共部分（通常用来生成有效数据）
dat_join4 <- dplyr::full_join(x = df1, y = df2, by = "x")   # 两表并集，保留所有信息

# 复杂融合（p.90）
dat_join5 <- dplyr::left_join(x = df1, y = df4, by = c("x","y"))    # 多列匹配
dat_join6 <- dplyr::left_join(x = df1, y = df3, by = c("x" = "g"))  # 不同列名合并
dat_join7 <- dplyr::left_join(x = df1, y = df4, by = "x",
                              suffix = c(".1",".2"))                 # 同名列加后缀都保留
```
`full_join()` 主要生成两个集合的并集；`inner_join()` 通常用来生成有效的数据；`left_join()`/`right_join()` 使用场景偏少；**融合时会用 NA（缺失值）代替不存在的值** `(p.89)`。

### D6. 表格的分组操作 (`p.90–92`)

```r
df <- data.frame(x = c('A','B','C','A','C'), '2010' = c(1,3,4,4,3),
                 '2011' = c(3,5,2,8,9), check.names = FALSE)
df_melt <- reshape2::melt(df, id.vars = 'x', variable.name = "year",
                          value.name = "value")

# (1) 按行 / 列操作（p.91）
df_rowsum <- apply(df[, 2:3], 1, sum)   # 按行求和（也可用 rowSums()）
df_colsum <- apply(df[, 2:3], 2, sum)   # 按列求和（也可用 colSums()）

# (2) 分组汇总 aggregate()："~" 左侧为需操作的变量，右侧为分组依据（p.91）
df_group1 <- aggregate(value ~ year, df_melt, mean)
df_group2 <- aggregate(value ~ year + x, df_melt, mean)
df_group3 <- aggregate(cbind(value, year) ~ x, df_melt, mean)

# (3) 分组运算 group_by() + summarise() + %>%（p.91–92）
df_groupmean1 <- df_melt %>%
                 dplyr::group_by(year) %>%
                 dplyr::summarise(avg = mean(value))

df_groupmean2 <- df_melt %>%
                 dplyr::group_by(year, x) %>%
                 dplyr::summarise(avg = mean(value))
```
`group_by()` 的优势：先按一个或多个变量分组，再接 dplyr 其他函数做分组运算——`summarise()` 汇总（与 `aggregate()` 结果一致）、`arrange()` 分组排序等，**可实现更多的分组运算操作**；不同运算之间用 `%>%` 连接 `(p.91)`。
`%>%` 是 dplyr 新引进的操作符：把数据集名作为开头，依次进行多步操作，编程者可按数据处理时的思路写代码，程序上清晰体现处理步骤与背后逻辑 `(p.91)`。

### D7. 缺失值处理（1.4.4 `(p.26)`）

R 中两种缺失数据：**NA**（向量中的另一种元素，用 `is.na()` 检查）与 **NULL**（没有任何东西，表示数据空白而非缺失，不能成为向量或数据框的一部分，用 `is.null()` 判定）`(p.25–26)`。

```r
tidyr::drop_na(df, y)          # 直接删除带 NA 的行（p.26）
tidyr::fill(df, y)             # 使用最邻近的元素填充 NA（p.26）
tidyr::fill(df, list(y = 2))   # 使用指定的数值替代 NA（p.26）
```

### D8. 与绘图直接相关的数据准备补充（1.4 节）

```r
# 因子水平顺序决定图表的类别排列顺序（p.20）；as.factor() 默认按字母顺序，用 levels 覆盖
Cut_Facor2 <- factor(x = c("Fair","Good","Very Good","Premium","Ideal"),
                     levels = c("Good","Fair","Very Good","Ideal","Premium"),
                     ordered = TRUE)
# 数值型因子转数值必须 as.numeric(as.character())；直接 as.numeric() 得到的是水平序号（p.20）
Num_Facor <- factor(x = c(1,3,5,2), levels = c(5,3,2,1), ordered = TRUE)
as.numeric(as.character(Num_Facor))   # 1 3 5 2
as.numeric(Num_Facor)                 # 4 2 1 3

# 连续变量离散化（分箱），用于把连续型转成类别型映射（p.19）
Cut_Vector <- cut(Num_Vector, breaks = c(0,3,6,9,11),
                  labels = c("0~3","3~6","6~9",">9"), right = TRUE)

# 日期型处理（时序数据必需）（p.17–18）：strftime() 提取年/月/周
c_Year  <- as.integer(strftime(c, '%Y'))   # 年份：2012
c_month <- as.integer(strftime(c, '%m'))   # 月份：6
c_week  <- as.integer(strftime(c, '%W'))   # 周数：24

# 空数据框：插值、拟合后存储新数据再绘图（p.21）。必须 stringsAsFactors=FALSE，否则逐行输入报 factor level 错
Df_Empty1 <- data.frame(var_a = numeric(), var_b = character(), stringsAsFactors = FALSE)
Df_Empty2 <- data.frame(matrix(ncol = 2, nrow = 0,
                               dimnames = list(c(), c("var_a","var_b"))))

# 导入优先 CSV（p.23–24）
mydata <- read.csv("Data.csv", sep = ",", na.strings = "NA", stringsAsFactors = FALSE)
```
导入注意：批量数据分两步——① 显式指定 `stringsAsFactors = FALSE`；② 依次将所需列转换为因子。**否则 R 会自动把字符型转成因子，导致数据只按默认字母顺序展示** `(p.23)`。

---
