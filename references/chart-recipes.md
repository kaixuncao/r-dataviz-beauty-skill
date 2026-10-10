# R 可视化图表配方参考（chart-recipes）

> **用途**：本文件供 AI Skill 在「图表类型推荐 + R 代码生成」时查阅。所有图表名、包名、函数名、参数名、判断性结论与 `(p.页码)` 出处均摘自《R 语言数据可视化之美：专业图表绘制指南（增强版）》第 3–11 章（学术图表规范第 12 章除外），未作压缩或凭记忆改写；书中未出现的内容一律标注「书中未出现 / 书未给出」，Skill 不得凭空引用。

---

## 第 0 部分：图表 × R 包 × 核心函数 速查表

| 图表名 | 数据关系大类 | R 包 | 核心函数/geom | 页码 |
|---|---|---|---|---|
| 单数据系列柱形图 | 类别比较型 | ggplot2 | `geom_bar(stat="identity", width=)` | p.94–96 |
| 多数据系列（簇状）柱形图 | 类别比较型 | ggplot2 + reshape2 | `geom_bar(position=position_dodge(), width=)` + `melt()` | p.96–97 |
| 堆积柱形图 | 类别比较型 | ggplot2 + reshape2 | `geom_bar(position="stack")` + `colSums()` 排序 | p.97–98 |
| 百分比堆积柱形图 | 类别比较型 | ggplot2 + reshape2 | `geom_bar(position="fill")` | p.98 |
| 条形图系列（4 种同构） | 类别比较型 | ggplot2 | 柱形图代码 + `coord_flip()` | p.99 |
| 不等宽柱形图 | 类别比较型 | ggplot2 | `geom_rect()` + `geom_text()` | p.100–101 |
| 棒棒糖图 | 类别比较型 | ggplot2 | `geom_segment()` + `geom_point()` | p.102 |
| 克利夫兰点图（滑珠散点图） | 类别比较型 | ggplot2 | `geom_point()`（棒棒糖去掉 `geom_segment()`） | p.101–102 |
| 哑铃图 | 类别比较型 | ggplot2 + reshape2 | `geom_line(aes(group=City))` + `geom_point()` | p.102–103 |
| 坡度图（两年份） | 类别比较型 | ggplot2 | `geom_segment()` + `geom_vline()` + `geom_point()` + `theme_void()` | p.103–104 |
| 坡度图（多年份） | 类别比较型 | ggalt | `geom_xspline()` | p.104 |
| 南丁格尔玫瑰图（极坐标柱形图） | 类别比较型 | ggplot2 | `geom_bar()` + `coord_polar(theta="x", start=0)` | p.104–107 |
| 径向柱形图 | 类别比较型 | ggplot2 + RColorBrewer | `geom_bar()` + `coord_polar(theta="x",start=0)` + `ylim(c(负,正))` | p.108–109 |
| 极坐标跨度图 | 类别比较型 | ggplot2 + viridis | `geom_linerange(x,ymin,ymax)` + `scale_color_viridis()` + `coord_polar()` | p.109–110 |
| 雷达图（标准） | 类别比较型 | fmsb | `radarchart()` | p.112 |
| 雷达图（ggplot） | 类别比较型 | ggplot2 | `geom_polygon()`/`geom_path()` + 自制 `coord_radar()` | p.110–113 |
| 词云图（单个） | 类别比较型 | tm + wordcloud | `Corpus()`→`TermDocumentMatrix()`→`wordcloud()` | p.115–116 |
| 词云图（对比/共有） | 类别比较型 | tm + wordcloud | `comparison.cloud()` / `commonality.cloud()` | p.115–116 |
| 趋势显示二维散点图 | 数值关系型 | ggplot2（GAM 用 mgcv） | `geom_point()` + `geom_smooth(method='loess', span=)` | p.118–122 |
| 图片散点图 | 数值关系型 | ggimage | `geom_image()` | p.124 |
| 残差分析图 | 数值关系型 | stats + ggplot2 | `lm()`/`predict()`/`residuals()` + `geom_point()`+`geom_segment()` | p.122–123 |
| Q-Q 图 / P-P 图 | 数值关系型 | ggpubr / ggplot2 / CircStats | `ggqqplot()` / `geom_qq()`+`geom_qq_line()` / `pp.plot()` | p.125–126 |
| 高密度散点图 | 数值关系型 | ggplot2 | `geom_point(alpha=)` | p.126–127 |
| 聚类散点图 | 数值关系型 | stats + ggplot2 | `kmeans()` + `geom_point()` + `stat_ellipse(geom="polygon")` | p.126–128 |
| 多数据系列散点图 | 数值关系型 | ggplot2 | `geom_point()` + `scale_shape_manual()` + `scale_fill_manual()` | p.128–129 |
| 气泡图 | 数值关系型 | ggplot2 + ggrepel | `geom_point(size=,fill=)` + `scale_size_area()` + `geom_text_repel()` | p.129–131 |
| 圆堆积气泡图 | 数值关系型 | ggraph + ggforce | `pack_circles()` + `geom_circle()` | p.131–132 |
| 三维散点图（3/4 维） | 数值关系型 | plot3D / scatterplot3d / rgl / scales / fields | `scatter3D()` / `scatterplot3d()` / `plot3d()` / `rescale()` / `colkey()` | p.132–136 |
| 曲面拟合图 | 数值关系型 | plot3D / lattice / rgl / scatterplot3d | `persp3D()` / `wireframe()` / `surface3d()` / `plane3d()` + `lm()`/`loess()` | p.136–138 |
| 等高线图 | 数值关系型 | ggplot2 + directlabels + RColorBrewer | `geom_tile()`/`geom_raster()` + `geom_contour()` + `direct.label()` | p.139–140 |
| 切面图 | 数值关系型 | plot3D + RColorBrewer | `slice3D()` + `mesh()` + `ramp.col()` | p.140–141 |
| 三元相图（散点/等高线） | 数值关系型 | ggtern + ggplot2 | `ggtern()` + `geom_point()` / `stat_density_tern()` + `limit_tern()` | p.142–143 |
| 散点曲线图（4 变体） | 数值关系型 | ggalt / splines | `geom_xspline(spline_shape=)` / `spline(method=)` + `geom_area()` | p.143–145 |
| 三维瀑布图 | 数值关系型 | plot3D | `polygon3D()` + `segments3D()` + `lines3D()` + `perspbox()` | p.145–147 |
| 分面瀑布图 | 数值关系型 | ggplot2 + reshape2 | `facet_grid(variable~.)` + `geom_area()` | p.148 |
| 峰峦图（时序版） | 数值关系型 | ggplot2 | `geom_linerange()`/`geom_ribbon()` + `spline()` + `scale_y_continuous()` | p.148–149 |
| 相关系数图（热力/气泡/方块/标签） | 数值关系型 | ggplot2 / corrplot | `geom_tile()`、`geom_point()` / `corrplot()` | p.151–153 |
| 韦恩图 | 数值关系型 | VennDiagram / gplots / limma / venneuler | `venn.diagram()` / `venn()` / `vennDiagram()` / `venneuler()` | p.153–154 |
| 统计直方图 | 数据分布型 | ggplot2 | `geom_histogram(binwidth=, bins=)` | p.157–159 |
| 核密度估计图 | 数据分布型 | ggplot2 | `geom_density(bw=, kernel=)` | p.157–159 |
| 核密度估计峰峦图 / 山脊线图 | 数据分布型 | ggridges + RColorBrewer | `geom_density_ridges_gradient(scale=, rel_min_height=)` | p.159–160 |
| 二维散点 + 边际分布组合图 | 数据分布型 | ggpubr / ggExtra / gridExtra | `ggscatterhist(margin.plot=)` / `ggMarginal()` / `grid.arrange()` | p.160–161, p.174 |
| 抖动散点图 | 数据分布型 | ggplot2 | `geom_jitter()` + `position_jitter(width=)` | p.162 |
| 蜂巢图（beeswarm） | 数据分布型 | ggbeeswarm | `geom_beeswarm(shape=,size=,cex=)` | p.162–163 |
| 点阵图（dot plot） | 数据分布型 | ggplot2 | `geom_dotplot(binwidth=,binaxis=,stackdir=,dotsize=)` | p.163 |
| 带误差线的散点分布图 | 数据分布型 | ggplot2（+ggalt） | `geom_jitter()`/`geom_dotplot()` + `stat_summary(fun.data="mean_sdl")` + `geom_xspline()` | p.163–164 |
| 带误差线的柱形分布图（柱形+抖动） | 数据分布型 | ggplot2 | `stat_summary(fun.y=mean,geom='bar')` + `stat_summary(fun.data=mean_sdl,geom='errorbar')` + `geom_jitter()` | p.164–165 |
| 箱形图 | 数据分布型 | ggplot2 | `geom_boxplot(notch=, varwidth=, outlier.size=)` | p.165–169 |
| 可变宽度 / 带凹槽箱形图 | 数据分布型 | ggplot2 | `geom_boxplot(notch=TRUE, varwidth=TRUE)` | p.168–169 |
| letter-value 箱形图（大数据） | 数据分布型 | 书中未给出 R 函数名（文献 [35][36]） | — | p.169–170 |
| 瓶状图（vase plot） | 数据分布型 | 书中未给出 R 包名（文献 [40]） | — | p.170 |
| 梯度图（gradient plot） | 数据分布型 | denstrip | `denstrip()` | p.171 |
| 小提琴图 | 数据分布型 | ggplot2 | `geom_violin(trim=, draw_quantiles=)` | p.170–171 |
| 豆状图 / 豆荚图 | 数据分布型 | beanplot | `beanplot()` | p.170, p.173 |
| 海盗图（pirate plot） | 数据分布型 | yarrr | `pirateplot()` | p.170 |
| 云雨图（raincloud，书推荐） | 数据分布型 | ggplot2 + 自定义 | `geom_flat_violin()` + `geom_boxplot()` + `geom_jitter()` + `position_nudge()` | p.172 |
| 双数据系列箱形图 / 带抖动 | 数据分布型 | ggplot2 | `geom_boxplot(aes(fill=factor(treatment)), position=position_dodge(0.8))` | p.172–174 |
| 双数据系列小提琴图 | 数据分布型 | ggplot2 + 自定义 | `geom_split_violin(draw_quantiles=, trim=)` | p.173–174 |
| 水平箱形图 / 中值排序箱形图 | 数据分布型 | ggplot2 / ggstance | `geom_boxplot()+coord_flip()` 或 `geom_boxploth()` + `reorder(Class,Value,median)` | p.179–180 |
| 带显著性标签的箱形图 | 数据分布型 | ggpubr | `compare_means()` + `stat_compare_means()` + `ggboxplot()` | p.176–177 |
| 带连接线的双箱形图（成对样本） | 数据分布型 | ggpubr / ggforce | `ggpaired()` 或 `geom_bezier(aes(group=index))` | p.177–179 |
| 子母图（inset） | 数据分布型 | ggplot2 + grid | `grid::viewport(x,y,width,height)` + `print(p2, vp=subvp)` | p.174–175 |
| 二维统计直方图（方块/六方） | 数据分布型 | ggplot2 | `geom_bin2d(bins=)` / `geom_hex(bins=)` / `stat_binhex()` | p.180–181, p.184 |
| 二维核密度估计图（栅格/多边形） | 数据分布型 | ggplot2 | `stat_density_2d(geom="raster"/"polygon", aes(fill=..density../..level..))` | p.181 |
| 三维统计直方图 | 数据分布型 | gplots + plot3D | `hist2d(nbins=)` + `hist3D()` | p.182–183 |
| 三维核密度估计图 | 数据分布型 | MASS + plot3D | `kde2d(h=, n=)` + `persp3D()` | p.182–183 |
| 二维 + 一维统计分布组合图 | 数据分布型 | ggplot2 + gridExtra | `grid.arrange(ncol=, nrow=, widths=, heights=)` | p.183–184 |
| 金字塔图 / 镜面图（直方图型、面积图型） | 数据分布型 | ggplot2 | `geom_bar(position="identity")` / `geom_area(position="identity")` + `scale_y_continuous(labels=abs)` | p.184–185 |
| 折线图 | 时间序列型 | ggplot2 | `geom_line()` + `scale_x_date(date_labels=, date_breaks=)` | p.187–189 |
| 面积图 | 时间序列型 | ggplot2 | `geom_area()` + `alpha=` | p.187–189 |
| 颜色映射填充面积图 | 时间序列型 | ggplot2 | `geom_bar(aes(fill=y,colour=y))` + `geom_line()` | p.189 |
| 两条折线间填充面积图（夹层） | 时间序列型 | ggridges | `geom_ridgeline_gradient()` | p.188 |
| 堆积面积图 / 百分比堆积面积图 | 时间序列型 | ggplot2 + reshape2 | `geom_area(position="stack"/"full")` + `melt()` | p.190–191 |
| 日历图（以年为单位） | 时间序列型 | ggTimeSeries + data.table | `ggplot_calendar_heatmap()` / `stat_calendar_heatmap()` + `facet_wrap(~Year)` | p.191–193 |
| 日历图（以月为单位） | 时间序列型 | ggplot2 + dplyr | `geom_tile(colour="white")` + `facet_wrap(~monthf)` + `scale_y_reverse()` | p.194 |
| 螺旋柱形图 / 螺旋热力图 | 时间序列型 | ggplot2 + readxl + dplyr | `geom_polygon()` 自造四边形 + `coord_polar()` | p.195–197 |
| 径向柱形图 / 径向热力图 | 时间序列型 | ggplot2 | 同上，`layout` 由螺旋改径向 | p.195–196 |
| 螺旋面积图 | 时间序列型 | ggplot2 + data.table | `geom_ribbon()`（纯色）/ `geom_linerange()`+`geom_line()`（颜色映射） | p.197–199 |
| 量化波形图 / 河流图 / 主题河流图 | 时间序列型 | ggTimeSeries | `stat_steamgraph()` | p.199–201 |
| 地平线图 | 时间序列型 | ggalt / latticeExtra | `geom_horizon(bandwidth=)` + `facet_wrap(~variable, ncol=1)` | p.202–204 |
| 饼图 | 局部整体型 | graphics（书推荐）+ RColorBrewer + dplyr | `pie(x, labels=, init.angle=90, col=, border=)` | p.206–208 |
| 圆环图 | 局部整体型 | 书中未给出圆环图代码/专用包 | — | p.208 |
| 散点复合饼图（3 变量） | 局部整体型 | scatterpie | `geom_scatterpie(aes(x,y,r), cols=)` + `coord_fixed()` | p.208–210 |
| 气泡复合饼图（4 变量） | 局部整体型 | scatterpie | 同上 + `geom_scatterpie_legend()` | p.208–210 |
| 马赛克图 | 局部整体型 | ggplot2（书推荐）/ ggmosaic / graphics / vcd | `geom_rect()` / `geom_mosai()` / `mosaicplot()` / `mosaic()` | p.211–213 |
| 华夫饼图（块状） | 局部整体型 | waffle / ggplot2 | `geom_waffle()` / `geom_tile()` | p.214–215 |
| 华夫饼图（点状 dot matrix） | 局部整体型 | ggplot2 | `geom_point(color="black",shape=21,size=6)` | p.215 |
| PCA 降维散点图 | 高维数据 | FactoMineR + factoextra + ggplot2 | `PCA(df, graph=FALSE)` + `fviz_pca_ind()` | p.218–220 |
| t-SNE 降维散点图 | 高维数据 | Rtsne + ggplot2 | `Rtsne(as.matrix(...))` 取 `$Y` + `geom_point()` | p.220–221 |
| 分面图（列/行/矩阵） | 高维数据 | ggplot2（+wesanderson） | `facet_wrap()` / `facet_grid(rows=, cols=, scales=)` | p.221–225 |
| 矩阵散点图 | 高维数据 | GGally（书推荐）/ graphics | `ggpairs(columns=, lower=, diag=, upper=)` / `pairs()` | p.225–227 |
| 热力图（含层次聚类） | 高维数据 | pheatmap / gplots / ComplexHeatmap | `pheatmap(color=, breaks=, cutree_col=, cutree_row=)` / `heatmap.2()` | p.227–229 |
| 平行坐标系图（连续） | 高维数据 | GGally | `ggparcoord(columns=, groupColumn=, alphaLines=)` | p.230–231 |
| 平行类别坐标系图 | 高维数据 | ggforce | `geom_parallel_sets()` | p.231 |
| RadViz 图 | 高维数据 | Radviz | `make.S()`/`do.L()`/`do.radviz()`/`bubbleRadviz()`/`do.optim()` | p.232–233 |
| 星形图标法 | 高维数据 | graphics + RColorBrewer + dplyr | `stars(x, scale=, locations=, len=, draw.segments=)` | p.234–236 |
| 柱形图标法 | 高维数据 | ggplot2 + reshape + RColorBrewer | `facet_wrap(~category)` + `geom_bar(stat="identity")` | p.236–238 |
| 切尔诺夫脸谱图 | 高维数据 | aplpack | `faces(x, col.face=, col.hair=, labels=, cex=)` | p.238–239 |
| 表格图 | 高维数据 | tabplot + RColorBrewer | `tableplot(data, sortCol=, select=, pals=)` | p.241 |
| 节点链接图（层次，正交/径向） | 层次关系型 | igraph + ggraph + tidyverse | `graph_from_data_frame()` + `ggraph(layout='dendrogram', circular=)` + `geom_edge_diagonal()` + `geom_node_text()` | p.243–247 |
| 树形图（dendrogram，4 型） | 层次关系型 | factoextra（书推荐）/ ggdendro / ggraph / circlize / ggtree | `fviz_dend(hc, k=, type=)` / `ggdendrogram()` / `circlize_dendrogram()` / `ggtree()` | p.248–250 |
| 径向热力图 + 环状树形图（组合） | 层次关系型 | circlize + ComplexHeatmap | `circos.track()` + `circos.rect()` + `circos.dendrogram()` + `Legend()` | p.250–252 |
| 旭日图 | 层次关系型 | ggraph + igraph | `ggraph(layout='partition', circular=TRUE)` + `geom_node_arc_bar(aes(filter=depth<=3))` | p.252–255 |
| 冰柱图 | 层次关系型 | ggraph + igraph | `ggraph(layout='partition')` + `geom_node_tile()` + `scale_y_reverse()` | p.252–255 |
| 圆堆积图 | 层次关系型 | ggraph + igraph + tidyverse | `ggraph(layout='circlepack', weight="size")` + `geom_node_circle()` | p.255–256, p.259 |
| 矩形树状图 | 层次关系型 | treemap（书推荐）/ treemapify | `treemap(index=, vSize=, vColor=, type="index")` / `treemapify()` | p.256–259 |
| Voronoi 树图 | 层次关系型 | voronoiTreemap | — | p.259 |
| 相邻矩阵图（热力路线） | 网络关系型 | reshape2 + ggplot2 | `melt(df, id.vars='Region')` + `geom_tile()` + `coord_equal()` | p.262–263 |
| 相邻矩阵图（层次聚类路线） | 网络关系型 | ComplexHeatmap + circlize | `Heatmap(as.matrix(df), col=colorRamp2(...))` | p.264–265 |
| 和弦图 | 网络关系型 | circlize + viridis + reshape2 | `chordDiagram(x=, grid.col=, directional=, direction.type=)` + `circos.trackPlotRegion()` | p.265–270 |
| 桑基图 | 网络关系型 | ggalluvial + ggplot2 + reshape2 | `geom_flow()` + `geom_stratum()` + `geom_text(stat="stratum")` | p.270–273 |
| 网络节点链接图（力导向 fr） | 网络关系型 | igraph + ggraph | `ggraph(layout='fr')` + `geom_edge_link()` + `geom_node_point()` | p.275–277 |
| 网络节点链接图（径向） | 网络关系型 | igraph + ggraph | `ggraph(layout='linear', circular=TRUE)` + `geom_edge_arc()` | p.278–279 |
| 弧长链接图（arc diagram） | 网络关系型 | ggraph | `ggraph(layout="linear")` + `geom_edge_arc(fold=TRUE)` | p.277–279 |
| 径向热力图 + 节点链接图（组合） | 网络关系型 | circlize + ComplexHeatmap | `circos.rect()` + `circos.link()` + `Legend()` | p.279–281 |
| 蜂巢网络图（hive plot） | 网络关系型 | ggraph + igraph + wesanderson | `ggraph(layout='hive', axis=, sort.by=)` + `geom_edge_hive()` + `geom_axis_hive()` | p.281–283 |
| 边绑定图 | 网络关系型 | ggraph + igraph | `get_con(from=, to=)` + `geom_conn_bundle(tension=)` | p.283–286 |
| 世界地图 | 地理空间型 | maps + ggplot2 + RColorBrewer | `map_data("world")` + `geom_map()` + `geom_path()` + `coord_map("mercator")` | p.293–294 |
| 省级/国家地图（SHP） | 地理空间型 | rgdal + ggplot2 + dplyr | `readOGR()` → `fortify()` → `full_join()` → `geom_polygon()` | p.297 |
| 地图（tmap 路线，含比例尺/指北针） | 地理空间型 | tmap + rgdal | `tm_shape()` + `tm_fill()` + `tm_borders()` + `tm_scale_bar()` + `tm_compass()` | p.298–299 |
| 局部地图（百度/Google/Stamen） | 地理空间型 | baidumap + ggmap | `getBaiduMap()` / `get_map()` + `ggmap()` / `qmap()` | p.299–300 |
| 分级统计地图（choropleth） | 地理空间型 | ggplot2（rgdal 读取） | `geom_polygon(aes(fill=))` + `scale_fill_gradientn()` / `scale_fill_gradient2()` | p.300–302 |
| Cartogram 示意图（连续型） | 地理空间型 | cartogram + rgeos + rgdal | `cartogram_cont(dataProjected, 'orange')` + `gCentroid()` + `fortify()` | p.302–303 |
| 点描法地图（dot map） | 地理空间型 | ggplot2 | `geom_polygon()` 底图 + `geom_point(shape=21)` / `geom_label()` | p.304–305 |
| 带气泡的地图 | 地理空间型 | ggplot2 | `geom_point(aes(size=,fill=), shape=21)` + `coord_fixed()` | p.305–306 |
| 带双气泡的地图 | 地理空间型 | ggforce | `geom_arc_bar(aes(x0,y0,r0,r,start,end,fill=))` | p.306–307 |
| 带饼图的地图 | 地理空间型 | scatterpie | `geom_scatterpie(aes(x,y,group,r), cols=)` + `geom_scatterpie_legend()` | p.309–310 |
| 带柱形的地图 | 地理空间型 | ggplot2 + reshape2 | `geom_rect(aes(xmin,xmax,ymin,ymax,fill=))` | p.311–312 |
| 沃罗诺伊地图 | 地理空间型 | sp + deldir + raster + ggplot2 | `SpatialPointsDataFrame()` + 自写 `SPointsDF_to_voronoi_SPolysDF()` + `intersect()` | p.312–314 |
| 连接地图 / 流向地图 | 地理空间型 | ggplot2 | `geom_curve(aes(x,y,xend,yend), curvature=, arrow=)` | p.314–316 |
| 等位地图（核密度路线） | 地理空间型 | sm + sp + ggplot2 | `sm.density(ngrid=)` + `geom_raster()` + `geom_contour()` | p.317–319 |
| 等位地图（插值和克里格路线） | 地理空间型 | stats / gstat / geoR / fields | `loess()` / `lm()` 多项式 / `krige()` | p.319–321 |
| 线型地图 | 地理空间型 | ggplot2 + ggalt | `geom_linerange()` + `geom_xspline(spline_shape=-0.1)` + `scale_color_gradientn()` | p.322–324 |
| 点状地图 | 地理空间型 | ggplot2 + sp | `expand.grid()` + `findInterval()` + `geom_point(shape=21)` | p.324–326 |
| 三维柱形地图 | 地理空间型 | lattice / plot3D | `cloud()` / `hist3D()` | p.326–327 |
| 简化示意图（矩形/圆圈/六角形） | 地理空间型 | ggplot2 + geogrid | `geom_tile()` / `geom_point(size=14)` / `geom_polygon()` / `calculate_grid()` | p.327–329 |
| 网格分面地图 | 地理空间型 | geofacet + ggplot2 + plyr | `facet_geo(~ code, grid=Griddata)` | p.330–331 |
| 邮标法 | 地理空间型 | ggplot2 + reshape2 | `left_join(df_map, df_city)` + `melt()` + `facet_wrap(~variable)` | p.331–333 |
| 地铁线路图（示意/实际） | 地理空间型 | ggplot2（+ggmap 底图） | `geom_path(linejoin="bevel", lineend="square")` + `geom_point(shape=21)` | p.334–339 |

---

## 第 1 部分：类别比较型图表（第 3 章，p.93–116）

> **通用坑（贯穿全章）**：**「用 R 语言绘制柱形图和条形图的最大潜在问题就是排序问题。」** X 轴变量默认按输入数据顺序绘制，Y 轴变量和图例变量默认按字母顺序绘制，绘图依据的是**因子向量的水平（level）顺序**而非数据框行顺序；**「只排序数据框，而不改变 X 轴因子向量的水平顺序，并不会改变柱形图的绘制顺序。」** (p.94–95)

通用排序范式（先排序、再改水平）：(p.95–96)

```r
order <- sort(mydata$Price, index.return=TRUE, decreasing = TRUE)
mydata$Cut <- factor(mydata$Cut, levels = mydata$Cut[order$ix])
# 表格排序（不改水平，仅排序不够）：base::order() / dplyr::arrange()
mydata <- mydata[order(mydata[,2], decreasing = TRUE),]; mydata <- dplyr::arrange(mydata, desc(Price))
```

### 1.1 单数据系列柱形图（single series column chart）

- **用途**：显示一段时间内的数据变化或各项之间的比较情况；类别型/序数型变量映射到横轴位置，数值型变量映射到矩形高度。(p.94)
- **适用数据**：一个类别型或序数型变量（X）+ 一个数值型变量（Y），如 `Cut` × `Price`。(p.95)
- **何时别用 / 坑**：X 轴为序数型（Fair/Good/Very Good/Premium/Ideal、年月）时**直接按顺序绘制**即可；X 轴为**类别型**时**「一般推荐对数据进行降序处理后，再展示图表」**，否则 ggplot2 按字母顺序画柱形。(p.95)
- **实现路径**：ggplot2 的 `geom_bar()`；排序用 base `sort()`/`order()`、`dplyr::arrange()`。
- **最小可运行代码**：

```r
library(ggplot2)
mydata<-data.frame(Cut=c("Fair","Good","Very Good","Premium","Ideal"),
                   Price=c(4300,3800,3950,4700,3500))
order<-sort(mydata$Price,index.return=TRUE,decreasing = TRUE)
mydata$Cut <- factor(mydata$Cut, levels = mydata$Cut[order$ix])
ggplot(data=mydata,aes(Cut,Price))+
  geom_bar(stat = "identity", width = 0.8,colour="black",size=0.25,fill="#FC4E07",alpha=1)
```

- **关键参数**：`stat="identity"`（用原始 Y 值而非计数）；`width`（柱宽，范围 (0,1)）；`position`（见 1.5 节，4 选 1）。(p.94, p.96)
- **出处**：(p.94–96)

### 1.2 多数据系列柱形图（簇状/并列，grouped column chart）

- **用途**：同一类别下并列比较多个数据系列的数值。(p.96–97)
- **适用数据**：二维宽表（类别列 + 多个数值列），**关键是把二维表转一维表（长表）**。(p.96)
- **何时别用 / 坑**：**「最好将表格根据第 1 个数据系列的数值进行降序处理，然后再展示。」** (p.97)
- **实现路径**：`reshape2::melt()` 或 `tidyr::gather()` 做宽转长；`ggplot2::geom_bar()`。(p.96–97)
- **最小可运行代码**：

```r
library(reshape2)
mydata<-read.csv("MultiColumn_Data.csv",check.names=FALSE)
order<-sort(mydata$"1996",index.return=TRUE,decreasing = TRUE) #根据“1996”排序
mydata$Catergory<- factor(mydata$Catergory, levels = mydata$Catergory[order$ix])
mydata<-melt(mydata,id.vars='Catergory')
ggplot(data=mydata,aes(Catergory,value,fill=variable))+
  geom_bar(stat="identity", color="black", position=position_dodge(),width=0.7,size=0.25)
```

- **关键参数**：`position=position_dodge()`（并排展示）；`position_dodge(width=0.7)` 可改系列间隔。(p.97)
- **出处**：(p.96–97)

### 1.3 堆积柱形图（stacked column chart）

- **用途**：显示单个项目与整体之间的关系，比较各个类别的每个数值所占总数值的大小。(p.97)
- **适用数据**：类别列 + 多个数值列（宽表），图例变量为序数型。(p.98)
- **何时别用 / 坑**：① 要**先按列求和得到每个类别的总和，再降序**；② 图例变量若是序数型（Fair→Ideal）**需按顺序显示图例**，不能按字母序。(p.97–98)
- **实现路径**：`reshape2::melt()` + `geom_bar(position="stack")`。
- **最小可运行代码**：

```r
mydata<-read.csv("StackedColumn_Data.csv")
Order<-sort(colSums(mydata[,2:ncol(mydata)]),index.return=TRUE,decreasing = TRUE)
mydata<-mydata[,c(1,Order$ix+1)]
mydata$Clarity <- factor(mydata$Clarity, levels = mydata$Clarity[c(1:5)])
mydata<-melt(mydata,id.vars='Clarity')
ggplot(data=mydata,aes(variable,value,fill=Clarity))+
  geom_bar(stat="identity",position="stack", color="black", width=0.7,size=0.25)
```

- **关键参数**：`position="stack"`（垂直堆叠）；`colSums()` 决定排序依据。(p.98)
- **出处**：(p.97–98)

### 1.4 百分比堆积柱形图（100% stacked column chart）

- **用途**：比较各个类别的数值所占总数值的**百分比**大小；与三维百分比堆积柱形图表达相同信息。(p.98)
- **适用数据**：同堆积柱形图；需先算重点展示系列的占比。(p.98)
- **何时别用 / 坑**：① 「要先求重点想展示类别的占比（如 Ideal 数据系列，**一般推荐为占比最大的数据系列**），然后对数据进行降序处理」；② 序数型图例需按顺序显示。(p.98)
- **实现路径**：`geom_bar(position="fill")`。
- **最小可运行代码**：

```r
mydata<-read.csv("StackedColumn_Data.csv")
Per<-(as.matrix(mydata[5,2:ncol(mydata)])) / t(as.matrix(colSums(mydata[,2:ncol(mydata)])))
Ideal<-sort(as.numeric(Per),index.return=TRUE,decreasing = TRUE)
mydata<-mydata[,c(1,Ideal$ix+1)]
mydata$Clarity <- factor(mydata$Clarity, levels = mydata$Clarity[c(1:5)])
mydata<-melt(mydata,id.vars='Clarity')
ggplot(data=mydata,aes(variable,value,fill=Clarity))+
  geom_bar(stat="identity", position="fill",color="black", width=0.8,size=0.25)
```

- **关键参数**：`position="fill"`（百分比化，垂直堆叠）。(p.94, p.98)
- **出处**：(p.98)

### 1.5 变体选择：并列 / 堆积 / 百分比堆积怎么选

`geom_bar()` 的 `position` 共 4 种，原书判定性表述原样记录 (p.94)：

1. `identity`：不做任何位置调整，**「该情况在多分类柱形图中不可行，序列间会遮盖，但是在多序列散点图、折线图中即可行，不存在遮盖问题」**；
2. `stack`：垂直堆叠 → 堆积柱形图，用于「单个项目与整体之间的关系」(p.94, p.97)；
3. `dodge`：`position_dodge()` 水平抖动 → 簇状柱形图，直接比较各系列绝对值 (p.94, p.97)；
4. `fill`：百分比化 → 百分比堆积柱形图，比较占比而非绝对值 (p.94, p.98)。

排序依据随变体变化：多数据系列按**第 1 个数据系列**降序（p.97）；堆积按**各类别列求和**降序（p.97）；百分比堆积按**重点系列占比**降序（p.98）。

### 1.6 条形图系列（Bar Chart）

- **用途**：与柱形图「几乎可以表达相同多的数据信息」，但柱形变为横向，**「更加强调项目之间的大小」**；类别型/序数型变量映射到**纵轴**位置，数值型变量映射到矩形**宽度**。(p.99)
- **适用数据**：同柱形图系列（单数据系列 / 多数据系列 / 堆积 / 百分比堆积四种同构）。(p.99)
- **何时别用 / 坑**：**「尤其在项目名称较长及数量较多时，采用条形图可视化数据会更加美观、清晰」**——即短标签、少类别时用柱形图即可；Y 轴变量和图例变量同样默认按字母顺序，需照 1.1 节处理排序。(p.99)
- **实现路径**：ggplot2，只需在 1.1 节柱形图代码**添加 `coord_flip()`** 旋转 X-Y 坐标轴，书中未另给独立代码。(p.99)
- **最小可运行代码**：

```r
# 在 1.1 任一柱形图代码基础上追加：
+ coord_flip()   # 将 X-Y 坐标轴旋转，柱形图 -> 条形图
```

- **关键参数**：`coord_flip()`；其余 `position` 参数（`dodge`/`stack`/`fill`）与柱形图完全一致。(p.99)
- **出处**：(p.99)

### 1.7 不等宽柱形图（variable width column chart）

- **用途**：在柱形图中**同时表达两个维度**——高度表达一个数值（Y），宽度表达另一个数值（X），多用于市场调查研究、维度分析。(p.100)
- **适用数据**：类别名 + 两个数值变量（如 `Scale` 控制宽度、`ARPU` 控制高度）；需自行计算 `xmin/xmax/label`。(p.101)
- **何时别用 / 坑**：本质不是 `geom_bar()` 而是手算矩形，须**累积求和**构造 X 轴起止点；常规单数值比较不要用它。
- **实现路径**：ggplot2 `geom_rect()` + `geom_text()`。
- **最小可运行代码**：

```r
library(ggplot2)
mydata<-data.frame(Name=paste0("Project",1:5),Scale=c(35,30,20,10,5),ARPU=c(56,37,63,57,59))
mydata$xmin<-0; for (i in 2:5){ mydata$xmin[i]<-sum(mydata$Scale[1:i-1])}
for (i in 1:5){ mydata$xmax[i]<-sum(mydata$Scale[1:i]); mydata$label[i]<-sum(mydata$Scale[1:i])-mydata$Scale[i]/2}
ggplot(mydata)+
  geom_rect(aes(xmin=xmin,xmax=xmax,ymin=0,ymax=ARPU,fill=Name),colour="black",size=0.25)+
  geom_text(aes(x=label,y=ARPU+3,label=ARPU),size=4,col="black")+
  geom_text(aes(x=label,y=-2.5,label=Name),size=4,col="black")
```

- **关键参数**：`geom_rect()` 用**右下角 (xmin,ymin) 与左上角 (xmax,ymax)** 定位；宽度 = xmax−xmin（对应 X 轴数值），高度 = ymax−ymin（对应 Y 轴数值）。(p.100)
- **出处**：(p.100–101)

### 1.8 棒棒糖图（lollipop chart）与克利夫兰点图（Cleveland's dot plot / 滑珠散点图）

- **用途**：传达与柱形图/条形图相同的信息，只是把矩形换成线条，**「可减少展示空间，重点放在数据点上」**；克利夫兰点图**「重点强调数据的排序展示及互相之间的差距」**，一般都横向展示，Y 轴一般为类别型变量。(p.101)
- **适用数据**：一个类别变量 + 一个数值变量（横向版对应条形图，纵向版对应柱形图）。(p.101–102)
- **何时别用 / 坑**：**「相对柱形图与条形图，棒棒糖图更加适合数据量比较多的情况」**——数据量少时用柱形图更直观。(p.101)
- **实现路径**：ggplot2 `geom_segment()`（连接线）+ `geom_point()`（散点）。**克利夫兰点图 = 棒棒糖图去掉 `geom_segment()` 一行**，原书原文：**「克利夫兰点图就是在棒棒糖图的基础上只保留散点实现的」**（书中未另给代码）。(p.102)
- **最小可运行代码**：

```r
library(ggplot2)
mydata<-read.csv("DotPlots_Data.csv",sep=",",na.strings="NA",stringsAsFactors=FALSE)
mydata$sum<-rowSums(mydata[,2:3])
order<-sort(mydata$sum,index.return=TRUE,decreasing = FALSE)
mydata$City<- factor(mydata$City, levels = mydata$City[order$ix])
ggplot(mydata, aes(sum, City)) +
  geom_segment(aes(x=0, xend=sum, y=City, yend=City))+ #添加连接线
  geom_point(shape=21,size=3,colour="black",fill="#FC4E07")
```

- **关键参数**：`geom_segment(aes(x,y,xend,yend))` 起点/终点坐标；棒棒糖连接线平行于 X 轴，长度对应 X 轴数值。(p.102)
- **出处**：(p.101–102)

### 1.9 哑铃图（dumbbell plot）

- **用途**：**「可以看成多数据系列的克利夫兰点图」**，用直线连接两个数据系列的数据点；用于①展示同一时间段两个数据点的相对位置（增加/减少）；②比较两个类别之间的数据值差别。(p.101)
- **适用数据**：类别变量 + 两个数值系列（如 Male/Female），需熔成一维表。(p.102–103)
- **何时别用 / 坑**：需按其中一个系列排序（书中以女性系列数值排序显示）。
- **实现路径**：`reshape2::melt()` + `geom_line(aes(group=City))` + `geom_point()` + `scale_fill_manual()`。
- **最小可运行代码**：

```r
library(ggplot2)
library(reshape2)
mydata<-read.csv("DotPlots_Data.csv",sep=",",na.strings="NA",stringsAsFactors=FALSE)
mydata$City <- factor(mydata$City, levels = madata$City[order(mydata$Female)])
mydata<-melt(mydata,id.vars='City')
ggplot(mydata, aes(value,City,fill=variable)) +
  geom_line(aes(group = City)) +
  geom_point(shape=21,size=3,colour="black")+
  scale_fill_manual(values=c("#00AFBB", "#FC4E07","#36BED9"))+
  theme(legend.position = c(0.85,0.12))
```

- **关键参数**：`geom_line(aes(group=City))` 连接同一类别的两点；`geom_segment()` 亦可（起点=系列1点 P，终点=系列2点 Q）。(p.102)
- **出处**：(p.101–103)

> 注：上块中 `madata$City` 为原书印刷/OCR 形式，实际应为 `mydata$City`（原笔记亦如此保留）。

### 1.10 坡度图（slope chart）

- **用途**：**「可以看成是一种多数据系列的折线图」**，比较**两个不同时间或两个不同实验条件下**某些类别变量的数据变化关系，用绿/红标注增长与降低。(p.103)
- **适用数据**：类别变量 + 两个（或多个）时间点的数值；两年份版为宽表（continent, 1952, 1957），多年份版需 `melt()`。(p.103–104)
- **何时别用 / 坑**：只关心首尾两个时间点时才用它；中间过程趋势应改用折线图/分面图。
- **实现路径**：两年份版用 ggplot2 的 `geom_segment()` + `geom_vline()` + `geom_point()` + `geom_text()` + `theme_void()`；多年份版用 **ggalt 包的 `geom_xspline()`** 替代 `geom_segment()`（**「geom_segment()函数只能使用直线连接两点，而 geom_xspline()函数可以使光滑的曲线连接多个数据点」**）。(p.104)
- **最小可运行代码**（两年份版）：

```r
library(ggplot2)
df <- read.csv("Slopecharts_Data1.csv")
colnames(df) <- c("continent", "1952", "1957")
left_label <- paste(df$continent, round(df$`1952`),sep=", ")
right_label <- paste(df$continent, round(df$`1957`),sep=", ")
df$class <- ifelse((df$`1957` - df$`1952`) < 0, "red", "green")
p <- ggplot(df) +
  geom_segment(aes(x=1, xend=2, y=`1952`, yend=`1957`, col=class), size=.75, show.legend=F) +
  geom_vline(xintercept=1, linetype="solid", size=.1) + geom_vline(xintercept=2, linetype="solid", size=.1) +
  geom_point(aes(x=1, y=`1952`), size=3,shape=21,fill="grey80",color="black") +
  geom_point(aes(x=2, y=`1957`), size=3,shape=21,fill="grey80",color="black") +
  scale_color_manual(labels = c("Up", "Down"), values = c("green"="#A6D854","red"="#FC4E07")) +
  xlim(.5, 2.5)
p <- p + geom_text(label=left_label, y=df$`1952`, x=rep(1, NROW(df)), hjust=1.1, size=3.5)
p <- p + geom_text(label=right_label, y=df$`1957`, x=rep(2, NROW(df)), hjust=-0.1, size=3.5)
p + theme_void()
```

- **关键参数**：`col=class` 用 ifelse 生成 "red"/"green" 分类；`xlim(.5,2.5)` 控制两列间距；`theme_void()` 去背景。(p.104)
- **出处**：(p.103–104)

### 1.11 南丁格尔玫瑰图（Nightingale rose chart / coxcomb chart / polar area diagram）

- **用途**：即**极坐标柱形图**，用圆弧的**半径长短**表示数据大小，每个类别在径向图上划分为相等分段。(p.104–105)
- **适用数据**：单数据系列（X 为时间序列型）或多数据系列（X 为类别型 + 图例类别）。(p.106)
- **何时别用 / 坑**（原书判定性表述原样抄录，p.105）：
  - **「由于半径和面积是平方的关系，南丁格尔玫瑰图会将数据的比例大小夸大，所以适合对比大小相近的数值。」**
  - **「由于圆形有周期的特性，所以南丁格尔玫瑰图特别适用于 X 轴变量是环状周期型序数的情况，比如月份、星期、日期等。」**
  - **「在数据量表比较多时，使用南丁格尔玫瑰图更能节省绘图空间。」**
  - 缺点：**「面积较大的外围部分会更加引人注目，这跟数值的增量成反比。」**
- **实现路径**：ggplot2 `geom_bar()` + **`coord_polar(theta="x", start=0)`**；多数据系列另需 `dplyr::arrange()`、`aggregate()` 排序，`scale_fill_brewer()`、`guides(fill=guide_legend(reverse=TRUE))`。
- **最小可运行代码**（单数据系列）：

```r
library(ggplot2)
mydata <- data.frame( a=c("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"),
                      b=c(50, 60, 70, 20,90,110,30))
myAngle <-seq(-20,-340,length.out =7) #设定坐标轴标签的角度，使之垂直于中心线
ggplot(mydata, aes(x=a, y=b, fill=factor(b))) +
  geom_bar(width = 1,stat="identity",colour = "black",fill="#F8766D") +
  geom_text(aes(y = b-8,label = b),color="white") +
  coord_polar(theta = "x",start=0) +
  ylim(c(0,120))+
  theme_light()+ theme(axis.text.x=element_text(size = 13,colour="black",angle = myAngle))
```

（多数据系列版本的核心差异：先用 `aggregate()` + `dplyr::arrange(desc())` 定因子水平，再用 `geom_bar(width=1.0)` + `coord_polar(theta="x",start=0)` + `ylim(c(-2000,12000))` 留出空心区。）(p.106–107)

- **关键参数**：`coord_polar(theta="x", start=0)` 中 `theta` 表示把 X 轴还是 Y 轴映射到极坐标；`ylim()` 下限可设负数制造空心圆；`theme(axis.text.x=element_text(angle=myAngle))` 让标签垂直于中心线。(p.106)
- **出处**：(p.104–107)

### 1.12 径向柱形图（radial column chart / circular column chart）

- **用途**：使用**同心圆网格**绘制条形图，每个圆圈表示一个数值刻度，径向分隔线区分不同类别；数值由中心向外增加，也可把外圆设为零值以显示负值；条形可堆叠。(p.108)
- **适用数据**：类别变量 + 数值变量，可单系列或多数据系列（`fill=score` + `position_dodge()`）。(p.109)
- **何时别用 / 坑**：**「径向柱形图的绘制方法其实与极坐标柱形图的绘制方法基本类似……只是使 Y 轴坐标不从 0 开始」**，关键在于 `ylim(ymin,ymax)`；若 ymin=0 就退化成南丁格尔玫瑰图。(p.108–109)
- **实现路径**：ggplot2 `geom_bar()` + `coord_polar(theta="x",start=0)` + `ylim(c(-3,6))`；配色 `RColorBrewer` + `scale_fill_brewer(palette="YlGnBu")`。
- **最小可运行代码**：

```r
library(ggplot2)
library(RColorBrewer)
df <- data.frame(item=rep(LETTERS[1:10], 5),
                 score=rep(letters[1:5], each=10),
                 value=rep((1:5), each=10) + rnorm(50, 0, .5))
myAng <-seq(-20,-340,length.out =10)
ggplot(data=df,aes(item,value,fill=score))+
  geom_bar(stat="identity", color="black", position=position_dodge(),width=0.7,size=0.25)+
  coord_polar(theta = "x",start=0) +
  ylim(c(-3,6))+  #Y 轴数值范围设定为(-3, 6)
  scale_fill_brewer(palette="YlGnBu")+
  theme_light()+ theme(axis.text.x=element_text(size = 13,colour="black",angle = myAng))
```

- **关键参数**：`ylim(c(ymin,ymax))` 决定内圈空心大小；`position=position_dodge()` 决定多系列是否并列。(p.108–109)
- **出处**：(p.108–109)

同节变体**极坐标跨度图**（polar range chart）：时间序列波动范围，**「对于数据量较多的数据，可以使用线条（line）代替条形（bar）表示数据」**，用 `geom_linerange()` + `viridis::scale_color_viridis()` + `scale_x_date()` + `coord_polar()` 实现，参数为 `(x, ymin, ymax)`。(p.109–110)

### 1.13 雷达图（radar chart / spider chart）

- **用途**：比较多个**定量变量**，查看哪些变量具有相似数值、有无异常值、哪些变量得分高/低，是显示**性能表现**的理想之选；每个变量一条轴，所有变量连成多边形。(p.110)
- **适用数据**：变量名列（如 Math/English/…）+ 数值列 + **辅助 id 列（1~N 等差数列）**；`label_data` 示例为 `car/value/id` 三列。(p.110)
- **何时别用 / 坑**（原书列举的「重大缺点」，p.110）：
  1. **「在一个雷达图中使用多个多边形，会令图表难以阅读，而且相当混乱。特别是如果用颜色填满多边形，表面的多边形则会覆盖下面的其他多边形。」**
  2. **「过多变量也会导致出现太多的轴线，使图表变得复杂，难以阅读，故雷达图只能保持简单，因而限制了可用变量的数量。」**
  3. **「它未能很有效地比较每个变量的数值。即使借助蜘蛛网般的网格指引，也不如在直线轴上比较数值容易。」**
  另有两个绘制陷阱：直接用 `geom_polygon()`+`coord_polar()` 会**「起点和终点会绘制在同一 X 轴位置」**（需在末尾补一行首行数据）；补行后 X 轴标签会错位，须用 `scale_x_continuous(breaks=label_data$id, labels=label_data$car)` 替换。(p.110–111)
- **实现路径**：**fmsb 包的 `radarchart()`**（标准雷达图）；ggplot2 `geom_polygon()`/`geom_path()` 配**自制的 `coord_radar()` 辅助函数**（来源 https://github.com/cardiomoon/ggplot2new/tree/4e50b7dcfee3246a169702f88f7dd46cbf933f4b ）；用 `coord_polar()` 替代 `coord_radar()` 可得平滑线版本。(p.112)
- **最小可运行代码**：

```r
library(ggplot2)
coord_radar <- function (theta = "x", start = 0, direction = 1) {
  theta <- match.arg(theta, c("x", "y")); r <- if (theta == "x") "y" else "x"
  ggproto("CoordRadar", CoordPolar, theta = theta, r = r, start = start,
          direction = sign(direction), is_linear = function(coord) TRUE)}
label_data<-data.frame(car=c("Math" , "English" , "Biology" , "Music" , "R-Coding" ),
                       id=c(1:5) , value=c(12 , 2 ,14 ,20, 18))
AddRow<-c(NA,nrow(label_data)+1, label_data[1,ncol(label_data)])
mydata<-rbind(label_data,AddRow)
angle0<- 360 * (label_data$id-1) /nrow(label_data)
myAngle<-ifelse(angle0 >angle0[1], 180-angle0, angle0)
ggplot(data=mydata,aes(x=id, y=value)) +
  geom_polygon(color = "black", fill= "#E41A1C",alpha=0.1)+
  geom_point(size=5,shape=21,color = 'black', fill= "#E41A1C")+
  coord_radar()+  # 改 coord_polar() 得带平滑线的圆形雷达图
  scale_x_continuous(breaks =label_data$id,labels=label_data$car)+
  ylim(0,22)+ theme_light()+
  theme(axis.text.x=element_text(size = 11,colour="black",angle = myAngle))
```

- **关键参数**：`geom_polygon()` 依次连接数据点成**封闭多边形**，`geom_path()` 用线条依次连接（非封闭）；`coord_radar()` 与 `coord_polar()` 二选一决定直线还是平滑线；`ylim(0,22)` 固定半径刻度。(p.112)
- **出处**：(p.110–113)

### 1.14 词云图（word cloud chart）

- **用途**：使每个字的大小与其出现频率成正比，显示单词在给定文本中的出现频率；也可用于显示分配了元数据的单词、比较两个不同文本。(p.113)
- **适用数据**：纯文本（TXT）或「词 × 频数」的**词频权重矩阵（term.matrix，行名为词、每列为一个文本的频数）**。(p.115)
- **何时别用 / 坑**（原书「重大缺点」，p.113–114）：① **「较长的字词会更引人注意」**；② **「字母含有很多升部/降部的单词可能会更受人关注」**；③ **「分析精度不足，主要是为了美观」**。另：**「在词云图上使用颜色通常都是毫无意义的，主要是为了美观」**。(p.113)
- **实现路径**：**tm 包**（`DataframeSource()`→`Corpus()`→`tm_map()`→`TermDocumentMatrix()`）做语料清洗与分词；**wordcloud 包**的 `wordcloud()`、`comparison.cloud()`、`commonality.cloud()` 绘图。(p.115–116)
- **最小可运行代码**：

```r
library(tm)
library(wordcloud)
Paper1<-paste(scan("Paper1.txt", what = character(0),sep = ""), collapse = " ")  #读入 TXT 文档 1
Paper2<-paste(scan("Paper2.txt", what = character(0),sep = ""), collapse = " ")  #读入 TXT 文档 2
tmpText<- data.frame(c(Paper1, Paper2),row.names=c("Text1","Text2"))
df_title <- data.frame(doc_id=row.names(tmpText), text=tmpText$c.Paper1..Paper2.)
ds <- DataframeSource(df_title)
corp = Corpus(ds)
corp = tm_map(corp,removePunctuation); corp = tm_map(corp,PlainTextDocument)  # 清标点、转纯文本
corp = tm_map(corp,removeNumbers); corp = tm_map(corp,function(x){removeWords(x,stopwords())})
term.matrix <- TermDocumentMatrix(corp)
term.matrix <- as.matrix(term.matrix)
colnames(term.matrix) <- c("Paper1","paper2")
comparison.cloud(term.matrix,max.words=300,random.order=FALSE,colors=c("#00B2FF", "red"))
commonality.cloud(term.matrix,max.words=100,random.order=FALSE,color="#E7298A")
df<-data.frame(term.matrix)
wordcloud(row.names(df), df$Paper1, min.freq=10, col=brewer.pal(8, "Dark2"), rot.per=0.3)
```

- **关键参数**：`wordcloud(words, freq, min.freq, col, rot.per)` 只需文本与频率；`comparison.cloud(term.matrix)` 画**独有**词汇对比云，`commonality.cloud(term.matrix)` 画**共有**词汇云；`max.words`、`random.order=FALSE`（大词居中更稳定）。(p.115–116)
- **出处**：(p.113–116)

---

## 第 2 部分：数值关系型图表（第 4 章，p.117–154）

### 2.1 趋势显示的二维散点图（scatter chart / X-Y plot）

- **用途**：显示和比较数值，观察两个变量的数据变化以发现关系与相关性；提供三类关键信息：①是否存在数量关联趋势；②线性还是非线性；③是否有离群值（outlier）。(p.118)
- **适用数据**：两个数值变量（x, y），`mydata` 为 x、y 两列。(p.122)
- **何时别用 / 坑**：**「这两个变量之间的相关性并不等同于确定的因果关系，也可能需要考虑其他的影响因素。」** 相关性分正相关、负相关、无相关、线性相关、指数相关；离集群较远的点为离群点。(p.118)
- **实现路径**：ggplot2 `geom_point()` + `geom_smooth()`；参数回归用 Excel/Origin 的拟合模块，R 用 `lm()` 等；平滑曲线用 `geom_smooth()`。(p.122)
- **最小可运行代码**（LOESS 平滑）：

```r
library(ggplot2)
mydata<-read.csv("Scatter_Data.csv",stringsAsFactors=FALSE) # x 和 y 两列
ggplot(data = mydata, aes(x,y)) +
  geom_point(fill="black",colour="black",size=3,shape=21)+ # 绘制二维散点
  geom_smooth(method = 'loess',span=0.4,se=TRUE,colour="#00A5FF",fill="#00A5FF",alpha=0.2)
```

- **关键参数**：`geom_smooth(method=..., span=, se=TRUE)`；**参数回归模型**可选指数 y=ae^bx、线性 y=ax+b、对数 y=lnx+b、幂 y=ax^b、多项式；**非参数平滑**有 LOESS、GAM（R 中 **mgcv 包**拟合）、Savitzky-Golay、样条（spline）。(p.119–122)
- **出处**：(p.118–122)

### 2.2 图片散点图（image scatter plot）

- **实现路径**：**ggimage 包的 `geom_image()`**。(p.124)
- **出处**：(p.124)（仅在原书「包 → 函数 → 图」索引表中出现，正文未展开）

### 2.3 残差分析图（residual analysis chart）

- **用途**：用残差（观测值−预测值）分析数据的可靠性、周期性或其他干扰；以**颜色渐变 + 气泡面积**双视觉暗示映射残差绝对值，连线长度直观显示拟合效果。(p.122)
- **适用数据**：x、y 两列，用 `lm()` 拟合后新增 `predicted`、`residuals`、`Abs_Residuals` 共 5 列。(p.123)
- **何时别用 / 坑**：**「实验点的标准化残差落在(-2,2)区间以外的概率≤0.05。若某一实验点的标准化残差落在(-2,2)区间以外，可在 95%置信度将其判为异常实验点，不参与回归线拟合。」** (p.122) 省去颜色/面积两个视觉特征时可用 Excel、Origin。(p.123)
- **实现路径**：stats `lm()` + `predict()` + `residuals()`；ggplot2 `geom_point()` + `geom_smooth(method="lm")` + `geom_segment()`。
- **最小可运行代码**：

```r
library(ggplot2)
mydata<-read.csv("Residual_Analysis_Data.csv",stringsAsFactors=FALSE)
fit <- lm(y2 ~ x, data = mydata)     #线性拟合
mydata$predicted <- predict(fit); mydata$residuals <- residuals(fit)
mydata$Abs_Residuals<-abs(mydata$residuals)
ggplot(mydata, aes(x = x, y = y2)) +
  geom_point(aes(fill =Abs_Residuals, size = Abs_Residuals),shape=21,colour="black") +
  geom_smooth(method = "lm", se = FALSE, color = "lightgrey") +
  geom_point(aes(y = predicted), shape = 1) +
  geom_segment(aes(xend = x, yend = predicted), alpha = .2) +
  scale_fill_continuous(low = "black", high = "red") +
  guides(fill = guide_legend((title="Rresidual")), size = guide_legend((title="Rresidual")))
```

- **关键参数**：`geom_point(aes(fill=, size=))` 双映射残差绝对值；`geom_segment(aes(xend=x, yend=predicted))` 连实际点与拟合点。(p.123)
- **出处**：(p.122–123)

### 2.4 分布显示的二维散点图（Q-Q 图 / P-P 图）

- **用途**：从图形角度检验数据是否服从某种分布（贝塔、t、卡方、伽马、正态、均匀、帕累托、逻辑斯谛分布等）。Q-Q 图比较分位数，P-P 图比较累积比例。(p.125)
- **适用数据**：单个数值向量（如 `rnorm(250, mean=10, sd=1)`）或两个待比较分布的样本。(p.125–126)
- **何时别用 / 坑**：**「一般来说，当比较两组样本时，Q-Q 图是一种比直方图更加有效的方法，但是理解 Q-Q 图则需要更多的背景知识。」** 正态 Q-Q 图判据：点近似在一条直线附近，**斜率为标准差、截距为均值**；两分布相似时点近似落在 y=x 上；线性相关时落在某条直线上（未必是 y=x）。(p.125) P-P 图「各点不呈直线但有一定规律」时可先对变量做转换。(p.125)
- **实现路径**：**CircStats 包的 `pp.plot()`** 画 P-P 图；ggplot2 的 **`geom_qq()` + `geom_qq_line()`** 画 Q-Q 图；ggplot2 结合 **ggpubr 包**可画成图 4-1-7 样式。(p.126)
- **最小可运行代码**：

```r
library(ggpubr)
x <- rnorm(250 , mean=10 , sd=1)
ggqqplot(x,
  shape=21,fill="white",colour="black", #使用白色填充、黑色边框的圆圈绘制数据点
  ggtheme = ggplot2::theme_grey())      #采用 ggplot2 包的灰色风格
```

- **关键参数**：`ggqqplot()` 的 `shape/fill/colour/ggtheme`；`geom_qq()` 的 distribution 参数。(p.126)
- **出处**：(p.125–126)

### 2.5 高密度 / 聚类散点图（high density & cluster scatter plot）

- **用途**：显示数据集群形状与数据云团中各点关系，**「很适合用于聚类分析，根据二维特征对数据进行类别区分」**。(p.126)
- **适用数据**：两个数值变量 x、y（大数据量）；聚类后可加 `cluster` 类别列。(p.128)
- **何时别用 / 坑**：点太密时**「可以利用数据点的透明度观察数据的形状和密度」**（`alpha=0.2`）。(p.127) 常用聚类算法：k-means、FCM、KFCM、DBSCAN、MeanShift。(p.126)
- **实现路径**：**stats 包的 `kmeans()`**（R 中 k-means 实现）+ ggplot2 `geom_point()` + **`stat_ellipse()`**（椭圆标定）；`scale_color_manual()`/`scale_fill_manual()`。
- **最小可运行代码**：

```r
library(ggplot2)
mydata<-read.csv("HighDensity_Scatter_Data.csv",stringsAsFactors=FALSE)
kmeansResult<- kmeans(mydata, 2, nstart =20)   # k-means 算法
mydata$cluster <- as.factor(kmeansResult$cluster)
ggplot(data = mydata, aes(x,y,color=cluster)) +
   geom_point (alpha=0.2)+  # 绘制透明度为 0.2 的散点图
  stat_ellipse(aes(x=x,y=y,fill= cluster), geom="polygon", level=0.95, alpha=0.2) +
  scale_color_manual(values=c("#00AFBB","#FC4E07")) + scale_fill_manual(values=c("#00AFBB","#FC4E07"))
```

- **关键参数**：`kmeans(mydata, k, nstart=20)`；`stat_ellipse(geom="polygon", level=0.95)`（省略该语句即退化为纯聚类散点图）；`alpha` 控制透明度。(p.128)
- **出处**：(p.126–128)

### 2.6 多数据系列散点图

- **用途**：用不同填充颜色和不同形状两个视觉特征区分数据系列。(p.128)
- **适用数据**：x、y 两个数值变量 + `cluster` 类别列（三列）。(p.129)
- **何时别用 / 坑**：**图 4-1-9(b)「使用不同填充颜色和不同形状两个视觉特征……即使在黑白印刷时也能保证读者清晰地区分数据系列」**——只换颜色（图 a）在黑白印刷下会失效。**「R 中 ggplot2 包可供选择总共 20 种不同类型的形状」**。(p.128)
- **实现路径**：ggplot2 `geom_point()` + `scale_shape_manual()` + `scale_fill_manual()`。
- **最小可运行代码**：

```r
ggplot(data = mydata, aes(x,y,fill=cluster,shape=cluster)) +
  geom_point(size=4,colour="black",alpha=0.7)+
  scale_shape_manual(values=c(21,23))+       #不同形状标定不同类别
  scale_fill_manual(values=c("#00AFBB",  "#FC4E07"))
```

- **关键参数**：`aes(fill=cluster, shape=cluster)`；`scale_shape_manual(values=c(21,23))`（21/23 为带填充色的形状）。(p.129)
- **出处**：(p.128–129)

### 2.7 气泡图（bubble chart）

- **用途**：散点图变体，X/Y 两维定位，**「每个气泡的面积代表第三个维度的数据」**。(p.129)
- **适用数据**：三个数值变量：x、y + 第三维（如 `disp`）映射到面积，可再映射到填充颜色。(p.130)
- **何时别用 / 坑**：
  - **「圆圈状气泡的大小是映射到面积（circle area）而不是半径（circle radius）或者直径（circle diameter）绘制的。因为如果是基于半径或者直径，那么圆的大小不仅会呈指数级变化，而且还会导致视觉误差。」** 换算式：`Circle Area=π×(Circle Diameter/2)^2`；`Circle Diameter=(SQRT(Area/π))×2`。(p.129)
  - **「气泡图的数据大小容量有限，气泡太多会使图表难以阅读。静态的气泡图最好只表达三个维度的数据。」** (p.131)
  - **「多数据系列气泡图（第四个维度为数据类别）……虽然可以使用不同的颜色区分不同类别，但是推荐使用后面章节讲解的栅栏图展示数据。」** (p.131)
  - **「使用交互可视化方法制作的图表几乎不应用在学术图表中。」** (p.131)
  - 为免重叠遮挡一般设气泡透明度；加数据标签时注意不要严重重叠（overlap）。(p.129)
- **实现路径**：ggplot2 `geom_point()` + `scale_fill_gradient2()` + `scale_size_area()`；**ggrepel 包的 `geom_text_repel()`**（**「ggplot2 包自带的添加数据标签函数 geom_text()容易出现数据标签重叠的情况」**）。(p.130)
- **最小可运行代码**：

```r
library(ggrepel)
library(ggplot2)
ggplot(data=mtcars, aes(x=wt,y=mpg))+
   geom_point(aes(size=disp,fill=disp),shape=21,colour="black",alpha=0.8)+
   scale_fill_gradient2(low="#377EB8",high="#E41A1C",limits = c(0,max(mtcars$disp)),midpoint = mean(mtcars$disp))+
   scale_size_area(max_size=12)+ # 设置显示的气泡图气泡最大面积
   geom_text_repel(label = disp ) # 添加数据标签“disp”
```

- **关键参数**：`scale_size_area(max_size=12)`（按面积而非半径映射）；`scale_fill_gradient2()` 三段渐变色；`alpha` 防遮挡；方块状气泡变体只需换形状（图 4-1-10(d)）。(p.129–130)
- **出处**：(p.129–131)

### 2.8 圆堆积气泡图（packed circle / circular packing）

- **用途**：**「对大量数据的柱形图展示的一种替代方案，能够很好地节省图表的展示面积，以气泡的大小和颜色两个视觉通道映射数值」**。(p.131)
- **适用数据**：一组数值向量（如 `rnorm(50, mean=20, sd=10)`）+ 标签。(p.132)
- **何时别用 / 坑**：适合类别多、不关心精确比较的场景；精确数值比较仍应用柱形图。
- **实现路径**：**ggraph 包的 `pack_circles()`** 计算气泡位置 + **ggforce 包的 `geom_circle()`** 绘制气泡。(p.132)
- **最小可运行代码**：

```r
library(ggraph); library(ggforce)
set.seed(123)
sizes <-rnorm(50, mean = 20, sd = 10)
position <- pack_circles(sizes)
data <- data.frame(x = position[,1], y = position[,2], r = sqrt(sizes/pi), value=sizes,
  label=paste(sample(letters[1:24],50,TRUE), sample(letters[1:24],50,TRUE),
              sample(letters[1:24],50,TRUE), sep = "")))
ggplot(data) +
  geom_circle(aes(x0 = 0, y0 = 0, r = attr(position, 'enclosing_radius')*0.88),size=1) +
  geom_circle(aes(x0 = x, y0 = y, r = r,fill=r), data = data) +
  geom_text(aes(x=x,y=y,label=label,size=r))+
  scale_fill_distiller(palette='Spectral',name='value')+ guides(size=FALSE)+
  coord_fixed()+ theme_void()
```

- **关键参数**：`pack_circles(sizes)` 返回位置矩阵，其属性 `enclosing_radius` 为外圈半径；`geom_circle(aes(x0,y0,r))` 以圆心+半径定位；`r = sqrt(sizes/pi)` 保证面积正比于数值。(p.132)
- **出处**：(p.131–132)

### 2.9 三维散点图（3D scatter plot）

- **用途**：在三维 X-Y-Z 图上针对一个或多个数据序列绘出三个度量；可将 Z 变量再映射到颜色以更清晰观察变化关系。(p.132–133)
- **适用数据**：三个数值变量（x, y, z）；四维版本再增加颜色或点大小维度。(p.133–134)
- **何时别用 / 坑**：**「在 R 中，三维图表的绘制只能通过函数编程实现，比较难控制到每个图表元素，比如 X-Y-Z 坐标轴标题的位置、网格线等。」** 书中三维图**「投影方式都为正交投影（orthographic projection）」**。**「rgl 包的 plot3d()函数绘制的三维图表可以实现图表的旋转，能供用户从不同视角（view）去观察数据关系。」** (p.133)
- **实现路径**：**scatterplot3d 包的 `scatterplot3d()`**、**rgl 包的 `plot3d()`**、**plot3D 包的 `scatter3D()`**；颜色映射需 **RColorBrewer**（`colorRampPalette`）构造 colormap，图例用 **fields 包的 `colkey()`**。(p.133–134)
- **最小可运行代码**：

```r
library(plot3D)
df<-read.csv("ThreeD_Scatter_Data.csv",header=T)
pmar <- par(mar = c(5.1, 4.1, 4.1, 6.1))
with(df, scatter3D(x = mph, y = Gas_Mileage, z = Power,
                   pch = 21, cex = 1.5,col="black",bg="#F57446",
                   xlab = "0-60 mph (sec)", ylab = "Gas Mileage (mpg)", zlab = "Power (kW)",
                   zlim=c(40,180), ticktype = "detailed",bty = "f",box = TRUE, theta = 60, phi = 20, d=3,
                   colkey = FALSE))
```

（四维扩展：颜色渐变映射第四维 → `bg=prc`；大小映射第四维 → `cex = rescale(df$Weight, c(.5, 5))`，需 **scales 包**；二者结合即三维气泡图；图例须用 `legend()` 自定义生成。）(p.134–136)

- **关键参数**：`theta`/`phi`/`d` 控制视角与透视强度；`bty="f"`、`box=TRUE`、`ticktype="detailed"` 控制盒子与刻度；`colkey=FALSE` 关闭默认颜色条；`pch=21`+`bg` 实现带边框的填充点。(p.133–136)
- **出处**：(p.132–136)

### 2.10 曲面拟合图（surface fitting chart）

- **用途**：分析**二维变量**与目标函数之间的关系，求取 f(x,y) 与 x、y 的解析式，使数据点近似分布在空间曲面上。(p.136)
- **适用数据**：三列数值（x, y, z）实测点 + 自定义网格数据。(p.138)
- **何时别用 / 坑**：两种拟合方式取舍——**「插值方式得到的方程所表示的曲面全部通过这组数据点，比如 LOESS 曲面拟合；而逼近方式，只要求在某种准则下其方程表示的曲面与这组数据点接近即可，比如多项式曲面拟合。逼近方式一般使用最小二乘法实现。」** (p.136–137) 也可用二维散点+等高线代替三维曲面（用颜色表示 z，见 2.11 节）。(p.137)
- **实现路径**：**rgl 包的 `surface3d()`**、**scatterplot3d 包的 `plane3d()`**、**lattice 包的 `wireframe()`**、**plot3D 包的 `persp3D()`**；步骤为 `lm()`/`loess()` 拟合 → `expand.grid()` 生成网格 → `predict.lm()` 求 z → `persp3D()` 绘图。(p.138)
- **最小可运行代码**（二元二次多项式曲面拟合）：

```r
library(plot3D); library(reshape2); library(RColorBrewer)
mydata <- read.csv("Surface_Data.csv", sep= ",", header=T)
x <- mydata$x; y <- mydata$y; z <- mydata$z
x2<-x*x; y2<-y*y
poly_z <- lm(z ~ x + y +x2+y2)          #多项式拟合 z=a+bx+cy+dx2+ey2
N<-30
xmar <- seq(min(x),max(x),(max(x)-min(x))/N)
ymar <- seq(min(y),max(y),(max(y)-min(y))/N)
Grid_xy<-expand.grid(list(x=xmar,y=ymar))
Grid_xy$x2<-Grid_xy$x*Grid_xy$x; Grid_xy$y2<-Grid_xy$y*Grid_xy$y
Grid_z <- predict.lm(poly_z, newdata=Grid_xy)
pred_z<-matrix(Grid_z, length(xmar), length(ymar))
persp3D (xmar, ymar, pred_z, theta = 150, phi = 40, d=3, col = colormap,
      scale = TRUE, border = "black", bty = "f",box = TRUE,ticktype = "detailed",
      ylab = "0-60 mph (sec)", xlab = "Gax Mileage (mpg)", zlab="Power (KW)",
      clab="Power (KW)", zlim=c(20,180), colkey = list(length = 0.5, width = 1))
```

- **关键参数**：`lm(z ~ x + y + x2 + y2)` 多项式项须手工构造；`N` 控制网格密度（30×30）；`theta/phi` 视角；`colkey=list(length,width)` 显示颜色条。(p.138)
- **出处**：(p.136–138)

### 2.11 等高线图（contour map）

- **用途**：可视化二维空间标量场，把三维数据用二维方法表达、用颜色表示第三维；可有效表达相同数值区域，揭示走势与陡峭程度，寻找坡、峰、谷等形状。(p.139)
- **适用数据**：矩阵形式或 melt 后的 (Var1, Var2, value) 三列长表；值矩阵 z 来自 `read.table()`。(p.139–140)
- **何时别用 / 坑**：纯热力图（图 a）只有颜色没有等值线，无法精确读值；加标签（图 c）后**「不需要颜色映射的图例」**。(p.139)
- **实现路径**：ggplot2 的 **`geom_tile()`** 或 **`geom_raster()`**（热力分布图）+ **`geom_contour()`**（等高线）；**directlabels 包的 `direct.label()`** 加等高线数值标签；配色用 RColorBrewer `colorRampPalette(rev(brewer.pal(11,'Spectral')))(32)`。(p.139)
- **最小可运行代码**：

```r
library(reshape2); library(ggplot2); library(directlabels); library(RColorBrewer)
z<-as.matrix(read.table("等高线.txt",header=TRUE))
colnames(z)<-seq(1,ncol(z),by=1)
max_z<-max(z); min_z<-min(z)
breaks_lines<-seq(min(z),max(z),by=(max_z-min_z)/10)
map<-melt(z); colnames(map)<-c("Var1","Var2","value")
Contour<-ggplot(map,aes(x=Var1,y=Var2,z=value))+
          geom_tile(aes(fill=value))+          #根据高度填充
          scale_fill_gradientn(colours= colorRampPalette(rev(brewer.pal(11,'Spectral')))(32))+
          geom_contour(aes(colour= ..level..),breaks=breaks_lines,color="black")
direct.label(Contour, list("bottom.pieces", cex=0.8, fontface="plain", fontfamily="serif", colour='black'))
```

- **关键参数**：`geom_raster()` 与 `geom_tile()` 的**主要区别**是前者有 `interpolate=TRUE/FALSE` 参数，决定是否对热力图平滑处理；`geom_contour(aes(colour=..level..), breaks=breaks_lines)` 控制等值线层级；`direct.label(..., list("bottom.pieces", ...))` 放置数值标签。(p.139)
- **出处**：(p.139–140)

### 2.12 切面图（slice chart）

- **用途**：展示四维数据 v=f(x,y,z)，把前三维放在三维直角坐标系，第四维 v 映射到渐变颜色；可分割得到平行于 X-Y、X-Z、Y-Z 的三个切面，切面上的点通过 3-D 插值获得。(p.140–141)
- **适用数据**：三个坐标向量 x/y/z（`seq(-4,4,by=0.2)`）经 `mesh()` 生成网格 + 一个标量函数值 p。(p.141)
- **何时别用 / 坑**：三维体数据且需看内部结构时才用；普通三维关系用三维散点图即可。
- **实现路径**：**plot3D 包的 `slice3D()`** + `mesh()`；颜色用 RColorBrewer 构造 colormap，配合 `ramp.col(colormap, alpha=0.9)`。(p.141)
- **最小可运行代码**：

```r
library(plot3D)
library(RColorBrewer)
x <- y <- z <- seq(-4, 4, by = 0.2)
M <- mesh(x, y, z)
R <- with (M, sqrt(x^2 + y^2 + z^2))
p <- sin(2*R) /(R+1e-3)
colormap <- colorRampPalette(rev(brewer.pal(11,'Spectral')),alpha = TRUE)(32)
slice3D(x, y, z, colvar = p, facets = FALSE,
        col = ramp.col(colormap,alpha = 0.9),
        clab="p vlaue",
        xs = 0, ys = c(-4, 0, 4), zs = NULL,
        ticktype = "detailed",bty = "f",box = TRUE, theta = -120, phi = 30, d=3,
        colkey = list(length = 0.5, width = 1, cex.clab = 1))
```

- **关键参数**：`facets`：TRUE 得图 4-4-1(b) 效果，FALSE 得图 4-4-1(a)；`xs/ys/zs` 指定切面的位置向量；`colvar=p` 指定映射到颜色的变量。(p.141)
- **出处**：(p.140–141)

### 2.13 三元相图（ternary phase diagram）

- **用途**：表示独立组分数为 3 的体系（最多 4 个自由度）的成分；等边成分三角形三顶点为三个组元 A、B、C，三角形内任一点代表三元系某一成分，满足 sa+sb+sc=1。(p.142)
- **适用数据**：三个成分变量（如 `fragments` 数据集的 qm、qp、m），取值通常归一化到 0–1。(p.143)
- **何时别用 / 坑**：三组分之和不为常数的数据不适用；成分确定须按「由给定点向三顶点所对应的边绘制平行线」的几何规则解读。(p.142)
- **实现路径**：**ggtern 包的 `ggtern()`** + ggplot2 `geom_point()` 画三元相散点图；`ggtern()` + **`stat_density_tern()`** + `geom_point()` 画三元相等高线图；另用 `theme_showarrows()`、`limit_tern()`，排版用 `grid.arrange()`（原书代码写 `library(rcolorbrewer)`）。(p.143)
- **最小可运行代码**：

```r
library(ggplot2)
library(ggtern)
library(rcolorbrewer)
data(fragments)
arrangement = list()
for(base in c('ilr')){
 x = ggtern(fragments,aes(qm,qp,m)) + geom_point() +
   stat_density_tern(geom='polygon', aes(fill=..level..), base=base, colour='grey50') +
scale_fill_gradientn(colours=c(brewer.pal(7,"set1")[2],"white",brewer.pal(7,"set1")[1]),na.value=na)+
   theme_showarrows()+
   limit_tern(.5,1,.5)
  arrangement[[length(arrangement) + 1]] = x
}
grid.arrange(grobs = arrangement,nrow=1)
```

- **关键参数**：`ggtern(data, aes(A,B,C))` 三个成分映射；`stat_density_tern(geom='polygon', aes(fill=..level..), base='ilr')` 的 `base` 指定变换基（ilr 等）；`limit_tern(.5,1,.5)` 设定三元坐标轴范围。(p.143)
- **出处**：(p.142–143)

### 2.14 散点曲线图系列（scatter-line chart family）

- **用途**：用平滑曲线将散点依次连接，**「重点体现数据的趋势」**；变体包括带曲线的散点图(a)、不带标记的曲线图(b)、带面积填充的曲线图(c)、带填充的带散点曲线图(d)。(p.143–144)
- **适用数据**：x、y 两列数值；带填充版本需 `spline()` 插值出密集点（n=300）。(p.145)
- **何时别用 / 坑**：**「图 4-6-1(a)和图 4-6-1(b)同时适用于单数据系列和多数据系列；图 4-6-1(c)和图 4-6-1(d)更适用于单数据系列，因为使用面积填充的多数据系列会存在遮挡效果，从而降低数据的可读性。」** 另：**「geom_line()函数是先对数据根据 X 轴变量的数值排序，然后使用直线依次连接，常用于直角坐标系中。geom_path()函数是直接根据给定的数据点顺序，使用直线将各点连接，常用于地理空间坐标系中。」** (p.144–145)
- **实现路径**：**ggalt 包的 `geom_xspline()`**（光滑曲线；**「geom_line()函数只能绘制折线图」**）；填充版本用 **splines 包的 `spline()`** 插值 + `geom_line()` + `geom_area()` + `geom_point()`。(p.145)
- **最小可运行代码**（曲线版 / 填充版）：

```r
library(ggplot2); library(ggalt)
mydata<-read.csv("Line_Data.csv",header=T)
ggplot(mydata, aes(x, y) )+
  geom_xspline(spline_shape=-0.5, size=0.25)+
  geom_point(shape=21,size=4,color="black",fill="#F78179") +
  theme_gray()
# ---- 带填充版本 ----
library(splines)
newdata <- data.frame(spline(mydata$x,mydata$y,n=300,method="hyman" ))
ggplot(newdata, aes(x, y) )+
  geom_line(size=0.25)+
  geom_area(fill="#F78179",alpha=0.7)+
  geom_point(data=mydata,aes(x,y),shape=21,size=4,color="black",fill="white")
```

- **关键参数**：`geom_xspline(spline_shape=-0.5)` 的 `spline_shape` 控制曲率（负值为平滑，0 近似直线）；`spline(x, y, n=300, method=...)` 的 `method` 有 `"fmm"`、`"natural"`、`"periodic"`、`"monoH.FC"`、`"hyman"` 五种，其中 **「"hyman"只适应于单调递增或递减的数据插值，"natural"使用自然样条插值方法，"periodic"使用周期样条插值方法」**。(p.145)
- **出处**：(p.143–145)

### 2.15 瀑布图（waterfall plot）与替代方案：分面图 / 峰峦图

- **用途**：展示拥有**相同 X 轴变量数据**（如时间序列）、**不同 Y 轴离散型变量**（类别）和 **Z 轴数值变量**的数据变化关系；三维瀑布图可看成多数据系列三维面积图。(p.145)
- **适用数据**：宽表（第 1 列为 X_Axis，其余各列为一个类别随 X 变化的数值）。(p.147–148)
- **何时别用 / 坑**（原书对三种方案的取舍判断，p.145–146）：
  - **分面瀑布图**：**「相对三维瀑布图，分面瀑布图可以更好地展示数据信息，避免不同类别之间数据重叠引起的遮挡问题，但是不能很直接地比较不同类别之间的数据差异。」** 若再把 Z 变量映射到颜色（图 4-7-2(b)），**「这样有利于比较不同类别之间的数据差异」**。
  - **峰峦图**：在图 4-7-2(b) 基础上**「将 Y 轴坐标移除，并缩小数据类别之间的距离，这样可以有效地缩小图表的占有面积，同时可以很好地展示数据的完整信息，包括不同类别之间的数据差异比较」**。
- **实现路径**：三维瀑布图用 **plot3D 包的 `polygon3D()` + `segments3D()`（三维面积图）+ `lines3D()`（三维曲线图）** + `perspbox()`；分面版用 **ggplot2 的 `facet_grid()`** + `geom_area()`；峰峦图用 `geom_linerange()` 或 `geom_ribbon()` + `spline()` 插值 + `scale_y_continuous()` 自定义标签。(p.147–149)
- **最小可运行代码**（分面版，最简）：

```r
library(ggplot2); library(RColorBrewer); library(reshape2)
mydata0<-read.csv("Facting_Data.csv",stringsAsFactors=FALSE)
colnames(mydata0)<-c("X_Axis",seq(60,25,-5))
mydata<-melt(mydata0,id.vars = "X_Axis")
ggplot(mydata,aes(X_Axis,value,fill=variable))+
  geom_area(color="black",size=0.25)+
  facet_grid(variable~.)
```

（峰峦图核心：`mydata$offest <- -as.numeric(mydata$variable)*Step`，再 `geom_linerange(aes(x=x, ymin=offest, ymax=V1_density_offest, group=variable, color=y))` + `geom_line(aes(x=x, y=V1_density_offest))` + `scale_color_gradientn(colours=colormap)` + `scale_y_continuous(breaks=seq(-Step*N,-Step,Step), labels=rev(labels_Y))`。）(p.148–149)

- **关键参数**：`facet_grid(variable~.)` 行分面；`geom_linerange(aes(x,ymin,ymax))` 用直线连接 (x,y) 与 (x,ymax)；`geom_ribbon(aes(x,ymin,ymax))` 则连接整条序列并填充颜色；`Step` 控制峰峦图相邻曲线的间隔。(p.148)
- **出处**：(p.145–149)

### 2.16 相关系数图（correlation matrix chart）

- **用途**：相关系数矩阵的可视化。矩阵第 i 行 j 列为两列变量的相关系数，对角线均为 1，上下三角对称。(p.151)
- **适用数据**：多个数值变量构成的矩阵 → `cor(mtcars)` → `melt()` 成长表 (Var1, Var2, value)，可再派生 `AbsValue=abs(value)`。(p.153)
- **何时别用 / 坑**：
  - **「在相关矩阵中，所有的数据都在－1 到 1 之间，我们不仅要关注相关系数的绝对值大小，同时更加看重它们的正负号。因此，相关矩阵的颜色图和一般矩阵的颜色图应该有所区别：即应当选取两种色差较大的颜色序列来展示不同符号的相关系数。其中，红色表示正相关系数，蓝色表示负相关系数。」** (p.151–152)
  - **椭圆图判死**：**「观察图 4-8-1(d)可以发现：椭圆图比较失败，因为它将最大的面积留给了相关性最弱的数据，给其他信息的获取造成了干扰。所以不建议大家使用椭圆图表示相关系数矩阵。」** (p.152)
  - 推荐类型排序：热力图(a) > 气泡图(b)/方块图(c) > 气泡标签图(e)/带标签热力图(f)；椭圆图(d) 不推荐。(p.152)
- **实现路径**：ggplot2 的 **`geom_tile()`**（热力图）与 **`geom_point()`**（气泡/方块图）；**corrplot 包的 `corrplot()`**（可画椭圆图与气泡标签图，参考 https://cran.r-project.org/web/packages/corrplot/vignettes/corrplot-intro.html ）。(p.153)
- **最小可运行代码**：

```r
library(ggplot2); library(RColorBrewer); library(reshape2)
data("mtcars"); mat <- round(cor(mtcars), 1); mydata <- melt(mat)
colnames(mydata)<-c("Var1","Var2","value")
# 带标签的热力图 图 4-8-1(f)
ggplot(mydata, aes(x = Var1, y = Var2, fill = value,label=value)) +
  geom_tile(colour="black") +
  geom_text(size=3,colour="white")+
  coord_equal()+
  scale_fill_gradientn(colours=c(brewer.pal(7,"Set1")[2],"white",brewer.pal(7,"Set1")[1]),na.value=NA)
# 气泡图 图 4-8-1(b)
mydata$AbsValue<-abs(mydata$value)
ggplot(mydata, aes(x= Var1 , y=Var2)) +
 geom_point(aes(size=AbsValue,fill = value), shape=21, colour="black") +
 scale_fill_gradientn(colours=c(brewer.pal(7,"Set1")[2],"white",brewer.pal(7,"Set1")[1]),na.value=NA)+ scale_size_area(max_size=12, guide=FALSE)
```

- **关键参数**：`scale_fill_gradientn(colours=c(蓝,"white",红))` 双色 diverging 配色（Set1[2]=蓝、Set1[1]=红）；`coord_equal()` 保证格子为正方；`geom_point(aes(size=abs(value)))` 让面积映射绝对值、颜色映射符号；`scale_size_area(max_size=12)`。(p.153)
- **出处**：(p.151–153)

### 2.17 韦恩图（Venn diagram）

- **用途**：关系型图表，用图形层叠表示集合与集合之间的相交关系；每个集合一个圆圈，重叠部分为交集（intersection）。(p.153)
- **适用数据**：两个维度——分类数据映射集合名，关系数据映射集合关系；书中示例为 `list(B=1:1800, A=1571:2020, c=500:1100)` 这样的**元素列表**。(p.153–154)
- **何时别用 / 坑**：**「一般来说，超过 5 个集合的场景，不适合使用韦恩图。」** 书中仅列出 2 集合、3 集合、4 集合三种适合场景。(p.153–154)
- **实现路径**：**VennDiagram 包的 `venn.diagram()`**（**「以 VennDiagram 包的 venn.Diagram()函数绘制的韦恩图效果最佳」**）；另有 **gplots 包的 `venn()`**、**limma 包的 `vennDiagram()`**、**venneuler 包的 `venneuler()`**。(p.154)
- **最小可运行代码**：

```r
library(VennDiagram)
library(RColorBrewer)
venn.diagram(list(B = 1:1800, A = 1571:2020,c=500:1100),fill = c(brewer.pal(7,"Set1")[1:3]),
             alpha = c(0.5, 0.5,0.5), cex = 2, cat.cex=3,cat.fontface = 4,lty =2, fontfamily =3,
             resolution =300, filename = "trial2.tiff")
```

- **关键参数**：`fill`/`alpha` 各集合填充色与透明度；`cex`（数值字号）、`cat.cex`（集合名字号）、`cat.fontface`；`lty` 边框线型；`resolution` 与 `filename` **直接输出图形文件**（非 ggplot 对象）。(p.154)
- **出处**：(p.153–154)

---

## 第 3 部分：数据分布型图表（第 5 章）

> 本章原书用 4 类分布数据横向比较 14 种图表：n = 正态（μ=3, σ=1）、s = 右偏（Johnson 偏斜度 2.0、峰度 13.1）、k = 尖峰态（偏斜度 2.2、峰度 20.0）、mm = 双峰（μ1=1.89、μ2=3.79，σ1=σ2=0.31），**每类 100 个数据点** (p.161)。选型规则见「第 10 部分」。

### 3.1 统计直方图（histogram）

- **用途 / 适用数据**：显示各组频数/数量分布及组间差别，观察哪些数据集中、异常或孤立数据分布在何处 (p.157)。输入＝一个连续变量的大量观测（+ 可选分组变量）(p.159)。
- **何时别用 / 坑**：形状类似柱形图但含义完全不同——横轴标出每个组的端点、纵轴为频数 (p.157)；结果强依赖分组设置（组数/组距，频数=分组内数据元数量除以组距）(p.157)。
- **实现 / 关键参数**：`ggplot2::geom_histogram()` (p.158)；「geom_histogram()函数主要由两个参数控制统计分析结果」——`binwidth`（箱形宽度）、`bins`（箱形总数）(p.159)。

```r
library(ggplot2)
df<-read.csv("Hist_Density_Data.csv",stringsAsFactors=FALSE)
ggplot(df, aes(x=MXSPD, fill=Location))+
   geom_histogram(binwidth = 1,alpha=0.55,colour="black",size=0.25)
```

- **出处**：(p.157)(p.158)(p.159)

### 3.2 核密度估计图（kernel density plot）

- **用途 / 适用数据**：显示数据在 X 轴连续数据段内的分布状况，用平滑曲线得到更平滑的分布 (p.157)。输入＝一个连续变量的观测（+ 可选分组变量）。
- **何时别用 / 坑**：非参数方法（Rosenblatt 1955、Emanuel Parzen 1962，又名 Parzen 窗）(p.157)；「不同的带宽得到的估计结果差别很大」，用平均积分平方误差 MISE 衡量 h 优劣 (p.158)。
- **实现 / 关键参数**：`ggplot2::geom_density()` (p.158)；`bw`（带宽）、`kernel`（默认 `"gaussian"`，另有 `"epanechnikov", "rectangular", "triangular", "biweight", "cosine", "optcosine"`）(p.159)；书中列举的其他核：uniform()、triangular()、biweight()、triweight()、Epanechnikov()、normal() (p.158)。

```r
library(ggplot2)
df<-read.csv("Hist_Density_Data.csv",stringsAsFactors=FALSE)
ggplot(df, aes(x=MXSPD,  fill=Location))+
  geom_density(alpha=0.55,bw=1,colour="black",size=0.25)
```

- **出处**：(p.157)(p.158)(p.159)

### 3.3 核密度估计峰峦图 / 山脊线图（ridgeline）

- **用途 / 适用数据**：多数据系列的核密度估计可视化；X=数值范围，Y=类别（如月份），核密度值映射到颜色 (p.159)。输入＝连续变量 + 类别变量（类别数较多）。
- **何时别用 / 坑**：「建议将核密度估计峰峦图的数值映射到颜色条」(p.159)。
- **实现 / 关键参数**：`ggridges::geom_density_ridges_gradient()` + `scale_fill_gradientn()` + `RColorBrewer` (p.159)；`scale`（峰峦重叠缩放）、`rel_min_height`（截断最小高度、去尾）、`fill = ..density..`。

```r
library(ggplot2)
library(ggridges)
library(RColorBrewer)
ggplot(lincoln_weather, aes(x = `Mean Temperature [F]`, y = `Month`, fill = ..density..)) +
  geom_density_ridges_gradient(scale = 3, rel_min_height = 0.00,size = 0.3) +
  scale_fill_gradientn(colours = colorRampPalette(rev(brewer.pal(11,'Spectral')))(32))
```

- **出处**：(p.159)(p.160)

### 3.4 二维散点图与边际分布组合图

- **用途 / 适用数据**：二维散点图 + 统计直方图/核密度估计图/箱形图/小提琴图 (p.160)(p.174)。输入＝两个连续变量 (x, y)（+ 可选分类变量）。
- **何时别用 / 坑**：三种方案对比——`ggpubr::ggscatterhist()`「最为简单」，`gridExtra::grid.arrange()`「可控性最好，也最为复杂」(p.160)。
- **实现 / 关键参数**：`ggpubr::ggscatterhist()`（`margin.plot` 可选 `"density"`/`"histogram"`/`"boxplot"`，共 3 种）；`ggExtra::ggMarginal()`（可选 `"density"`/`"histogram"`/`"boxplot"`/`"violin"`，共 4 种）；`gridExtra::grid.arrange()` (p.160)。参数：`margin.plot`、`margin.params`、`palette`、`legend`（图例位置）、`ggtheme`。

```r
library(ggplot2)
library(ggpubr)
N<-200
data2 <- data.frame(x=c(rnorm(mean=1.5,sd=0.5,N), rnorm(mean=2.5,sd=0.5,N), rnorm(mean=1,sd=0.3,N)),
                    y=c(rnorm(mean=2,sd=0.2,N),  rnorm(mean=2.5,sd=0.5,N), rnorm(mean=1.5,sd=0.2,N)),
                    class=rep(c("A","B","C"),each=200))
ggscatterhist(data2,  x ='x', y = 'y', shape=21,color ="black",fill= "class", size =3, alpha = 0.8,
  palette = c("#00AFBB", "#E7B800", "#FC4E07"),
  margin.plot =  "density", margin.params = list(fill = "class", color = "black", size = 0.2),
  legend = c(0.9,0.15), ggtheme = theme_minimal())
```

- **出处**：(p.160)(p.161)(p.174)

### 3.5 抖动散点图（jitter chart）

- **用途 / 适用数据**：用散点展示分布，Y 值不变，X 值沿类别中心线在范围内随机生成 (p.162)。输入＝连续变量 + 类别变量，样本量不大时。
- **何时别用 / 坑**：「由于随机生成数据点的 X 轴数值，所以很容易存在数据点重合叠加的情况，不利于观察数据的分布规律」(p.162)。
- **实现 / 关键参数**：`ggplot2::geom_jitter()`；`position = position_jitter(width = NULL)`，`width` 为水平左右抖动范围 (p.162)。
- **出处**：(p.162)

### 3.6 蜂巢图（beeswarm chart）与点阵图（dot plot）

- **用途 / 适用数据**：数据点沿类别中心线向两侧均匀对称展开，美观且便于观察分布 (p.162)(p.163)。输入＝连续变量 + 类别变量（书例每类 100 个）(p.161)。
- **何时别用 / 坑**：两者均相对抖动散点克服了随机重叠问题。
- **实现 / 关键参数**：蜂巢图 `ggbeeswarm::geom_beeswarm()`（ggplot2 的拓展包），参数 `shape`、`size`、`cex`（间隙）(p.163)；点阵图 `ggplot2::geom_dotplot()`，参数 `binwidth`、`binaxis`（X/Y 方向）、`stackdir`（默认 `"up"`，另有 `"down"`、`"center"`）、`dotsize` (p.163)。
- **出处**：(p.162)(p.163)

### 3.7 带误差线的散点分布图系列

- **用途 / 适用数据**：抖动散点（或点阵）作背景展示分布，叠加每类的均值与标准差误差线（average + standard deviation）(p.163)；X 轴换成**连续型时间变量**时用曲线连接表示趋势，同时加误差线 (p.163)。输入＝连续变量 + 类别变量（或时间变量）。
- **何时别用 / 坑**：「如果只使用带误差线的散点图，就无法观察数据的分布情况，所以使用抖动散点图作为背景，可以很好地显示数据分布情况」(p.163)。
- **实现 / 关键参数**：`geom_jitter()`/`geom_dotplot()` + `stat_summary(fun.data="mean_sdl", geom="pointrange")` + `stat_summary(fun.y="mean", geom="point")` (p.163)(p.164)，`fun.args=list(mult=1)` 为 SD 倍数；带连接线版先用 `dplyr::group_by()` + `summarise()` 算均值与标准差，再用 `geom_point()` + `geom_errorbar()` + `ggalt::geom_xspline()` (p.163)。

```r
ggplot(mydata, aes(Class, Value))+
  geom_jitter(aes(fill = Class),position = position_jitter(0.3),shape=21, size = 2,color="black")+
  scale_fill_manual(values=c(brewer.pal(7,"Set2")[c(1,2,4,5)]))+
  stat_summary(fun.data="mean_sdl", fun.args = list(mult=1), geom="pointrange", color = "black",size = 1.2)+
  stat_summary(fun.y="mean", fun.args = list(mult=1), geom="point", color = "white",size = 4)+
  theme_light()
```

- **出处**：(p.163)(p.164)

### 3.8 柱形分布图系列（带误差线柱形图 / 柱形+抖动）

- **用途 / 适用数据**：用每类**均值**作柱高，按标准差绘制误差线 (p.164)。输入＝连续变量 + 类别变量。
- **何时别用 / 坑**：「但是如果只使用图 5-2-3(a) 展示数据，那么就会与带误差线的散点图存在同样的问题：无法显示数据的分布情况。图 5-2-3(a) 的类别 mm 为双峰分布，但是其与其他三个类别的均值与标准差基本相同，没有较大区别」(p.164)；补救：「在带误差线的柱形图的基础上，添加抖动散点图」(p.164)。
- **实现 / 关键参数**：`stat_summary(fun.y=mean, geom='bar')` + `stat_summary(fun.data=mean_sdl, geom='errorbar')` + `geom_jitter()` (p.165)；`width` 控制柱宽/误差线横杠宽。

```r
ggplot(mydata, aes(Class, Value))+
  stat_summary(fun.y=mean, geom='bar', fun.args = list(mult=1),colour="black",fill="white",width=.7) +
  stat_summary(fun.data = mean_sdl, fun.args = list(mult=1),geom='errorbar', color='black',width=.2) +
  geom_jitter(aes(fill = Class),position = position_jitter(0.2),shape=21, size = 2,alpha=0.9)+
  scale_fill_manual(values=c(brewer.pal(7,"Set2")[c(1,2,4,5)]))+
theme_light()
```

- **出处**：(p.164)(p.165)

### 3.9 箱形图（box plot / box-whisker plot）

- **用途 / 适用数据**：显示一组数据的最大值、最小值、中位数、上下四分位数，反映连续型定量数据分布的中心位置和散布范围 (p.165)。1977 年由 John W. Tukey 在 *Exploratory Data Analysis* 中提出 (p.165)。输入＝一组或多组连续型定量数据 + 分组变量。
- **何时别用 / 坑**：无法识别双峰/多峰分布 (p.167)；n<1000 时四分位数之外的估计不可靠 (p.169)；「简单的设计往往隐藏了有关数据分布的重要细节」(p.167)。补救：叠加 `geom_jitter()` (p.168)。
- **实现 / 关键参数**：`ggplot2::geom_boxplot()` (p.168)；`notch`（凹槽＝中位数置信区间，「如果凹槽不重合，表示中位数在 95% 的置信区间内就可以认为显著不同」）(p.168)、`varwidth`（箱宽映射到数据量）(p.169)、`outlier.size`、`outlier.alpha`、`width`、`position=position_dodge(width)` (p.172)(p.174)。

```r
ggplot(mydata, aes(Class, Value))+
  geom_boxplot(aes(fill = Class),notch = FALSE)+
  geom_jitter(binaxis = "y", position = position_jitter(0.3),stackdir = "center",dotsize = 0.4)+
  scale_fill_manual(values=c(brewer.pal(7,"Set2")[c(1,2,4,5)]))+
theme_light()
```

- **出处**：(p.165)(p.166)(p.167)(p.168)(p.169)

### 3.10 可变宽度 / 带凹槽箱形图

- **用途 / 适用数据**：箱形宽度解决「箱形图每个类别的数据量大小不同的问题」；凹槽表示中位数的置信区间 (p.168)。输入＝各类别样本量差异大的分组数据（书例 10、100、1000、10000）(p.168)。
- **实现 / 关键参数**：`geom_boxplot(notch=TRUE, varwidth=TRUE)`；`notch`（TRUE/FALSE 是否带凹槽）、`varwidth`（TRUE/FALSE 是否按数据量映射箱宽）(p.169)。

```r
library(ggplot2)
library(RColorBrewer)
freq <- 10 ^ ((1:4))
df <- data.frame(group = rep(letters[seq_along(freq)], freq), x = rnorm(sum(freq),3,1))
ggplot(df, aes(group,x))+
  geom_boxplot (aes(fill = group),notch = TRUE, varwidth = TRUE) +
  scale_fill_manual(values=c(brewer.pal(7,"Set2")[c(1,2,4,5)]))
theme_light()
```

- **出处**：(p.168)(p.169)

### 3.11 letter-value 箱形图（大数据的箱形图）

- **用途 / 适用数据**：面向 n ≈ 10,000 − 100,000，展示四分位数之外的数据分布与大量异常值（约 0.4 + 0.007n）(p.169)。在中值 M、四分位数 F 基础上向两端延伸增加箱形个数：1/8 eighths(E)、1/16 sixteenths(D)……直到估计误差增大到一定阈值 (p.169)。
- **何时别用 / 坑**：「它与传统箱形图存在一个同样的问题，即无法识别多峰分布的情况」(p.169)；书图 5-2-7(b) 中 mm 双峰「仅仅从图中无法识别，这就是箱形图的局限性所在」(p.170)。
- **实现 / 关键参数**：原书未给出 R 函数名，仅标注文献 [35][36] (p.169)；参数为延伸分位数层级（E、D…）与估计误差阈值。
- **出处**：(p.169)(p.170)

### 3.12 瓶状图（vase plot）与梯度图（gradient plot）

- **用途 / 适用数据**：瓶状图「使用核密度估计箱形部分的数据，从而得到核密度估计曲线，替代原有的箱形部分，主要用来显示数据的分布形状」(p.170)；梯度图「彩色的条带对应数据的核密度估计，黑色长条代表数据的均值或者中位数，表达的数据信息与小提琴图类似」(p.171)。输入＝连续变量 + 类别变量。
- **何时别用 / 坑**：瓶状图「绘图时需要设定核密度估计的带宽（bandwidth）」(p.170)。
- **实现 / 关键参数**：瓶状图原书未给出 R 包名，仅标注文献 [40] (p.170)；梯度图 `denstrip::denstrip()` (p.171)。
- **出处**：(p.170)(p.171)

### 3.13 小提琴图（violin plot）

- **用途 / 适用数据**：显示数据分布及其概率密度，结合了箱形图和密度图的特征 (p.170)。中间黑色粗条＝四分位数范围，细黑线＝95% 置信区间，黑色横线＝中位数 (p.170)。输入＝连续变量 + 类别变量。
- **何时别用 / 坑**：「虽然小提琴图可以比箱形图显示更多详情，但它们也可能包含较多干扰信息，而且绘图时需要设定核密度估计的带宽」(p.170)；书中做法是在小提琴图内再添加箱形图 (p.171)。
- **实现 / 关键参数**：`ggplot2::geom_violin()`，主要参数与核密度估计曲线一样为 `bw`（带宽）(p.170)(p.171)；另有 `trim`（是否截断到数据范围）、`draw_quantiles`。

```r
ggplot(mydata, aes(Class, Value))+
  geom_violin(aes(fill = Class),trim = FALSE)+
  geom_boxplot(width = 0.2)+
  scale_fill_manual(values=c(brewer.pal(7,"Set2")[c(1,2,4,5)]))+
  theme_light()
```

- **出处**：(p.170)(p.171)

### 3.14 豆状图 / 豆荚图（bean plot）与海盗图（pirate plot）

- **用途 / 适用数据**：豆状图在小提琴密度部分基础上，用短横条表示每个数据的数值，长横线表示类别均值，形似豌豆、短横条像种子 (p.170)；海盗图综合抖动散点图（原始数据）、柱形图（均值）、小提琴图（核密度估计）和方块图——95% 高密度区间 HDI 或置信区间 CI (p.170)。输入＝连续变量 + 类别变量。
- **何时别用 / 坑**：海盗图「虽然能完整地表达数据的所有信息，但是过于复杂」；「建议将该图表用于前期数据分布的探索，再具体确定选择合适的图表类型展示数据」(p.170)。
- **实现 / 关键参数**：豆状图 `beanplot::beanplot()`，双数据系列「使用 beanplot 包的 beanplot()函数就可以直接实现」(p.173)；海盗图 `yarrr::pirateplot()` (p.170)。
- **出处**：(p.170)(p.173)

### 3.15 云雨图（raincloud plot，书中推荐）

- **用途 / 适用数据**：核密度估计曲线图 + 箱形图 + 抖动散点图的组合，「清晰、完整、美观地展示了所有数据信息」(p.172)。输入＝连续变量 + 类别变量。
- **何时别用 / 坑**：书中为推荐项——比海盗图「没那么冗余」，比小提琴图「省却多余的核密度估计曲线的同时，增加了抖动散点图」(p.172)。
- **实现 / 关键参数**：自定义半小提琴函数 `geom_flat_violin()` + `geom_boxplot()` + `geom_jitter()`，用 `position=position_nudge(x)` 把半小提琴和箱形移到类别中心线左/上侧 (p.172)。

```r
ggplot(mydata, aes(x=Class, y=Value))  +
  geom_flat_violin(aes(fill=Class),position=position_nudge(x=.25),color="black") +
  geom_jitter(aes(color=Class), width=0.1) +
  geom_boxplot(width=.1,position=position_nudge(x=0.25),fill="white",size=0.5) +
  coord_flip() +
  theme_light()
```

- **出处**：(p.172)

### 3.16 双数据系列箱形图 / 带抖动散点的双系列箱形图

- **用途 / 适用数据**：同一类别下比较两个处理组（treatment）的分布 (p.172)。输入＝连续变量 + 类别变量 + 第二个分组变量。
- **实现 / 关键参数**：`geom_boxplot(aes(fill=factor(treatment)), position=position_dodge(0.8))` (p.174)；加抖动时用自定义变量 `dist_cat_n`/`scat_adj` 把散点沿箱形中心线分布，`position_jitter(width, height)` 取 `height=0` 只水平抖动 (p.174)；`outlier.size` 控制离群点大小。

```r
library(ggplot2)
set.seed(141079)
data <- data.frame(BAI2013 = rnorm(300), class = rep(letters[1:3], 100),
                 treatment = rep(c("elevated","ambient"),150))
ggplot(data, aes(x = class, y = BAI2013))+
  geom_boxplot(outlier.size = 1, aes(fill=factor(treatment)), position = position_dodge(0.8),size=0.5) +
  guides(fill=guide_legend(title="treatment"))+ theme_light()
data<-transform(data,dist_cat_n=as.numeric(class), scat_adj=ifelse(treatment == "ambient",-0.2,0.2))
ggplot(data, aes(x =class, y = BAI2013))+
    geom_boxplot(outlier.size = 0, aes(fill=factor(treatment)), position = position_dodge(0.8),size=0.4) +
    geom_jitter(aes(scat_adj+dist_cat_n, BAI2013,fill = factor( treatment)),
                position=position_jitter(width=0.1,height=0), shape=21, size = 1.5)+
  guides(fill=guide_legend(title="treatment"))+ theme_light()
```

- **出处**：(p.172)(p.174)

### 3.17 双数据系列小提琴图（geom_split_violin）

- **用途 / 适用数据**：小提琴图本身由左右对称的两个核密度曲线构成，双系列时保留各一半（左一个、右一个）拼接 (p.173)。输入＝连续变量 + 类别变量 + 第二个分组变量。
- **何时别用 / 坑**：ggplot2 未提供该函数，需自定义 `geom_split_violin()`（来源 gist: Karel-Kroeze/746685f5613e01ba820a31e57f87ec87）(p.173)(p.174)。
- **实现 / 关键参数**：`geom_split_violin(draw_quantiles = 0.5, trim = FALSE)` + `geom_jitter()` (p.174)。

```r
data<-transform(data,dist_cat_n=as.numeric(class), scat_adj=ifelse(treatment == "ambient",-0.15,0.15))
ggplot(data, aes(x = class, y = BAI2013,fill=factor(treatment)))+
  geom_split_violin(draw_quantiles = 0.5,trim = FALSE)+
  geom_jitter(aes(scat_adj+dist_cat_n, BAI2013,fill = factor(treatment)),
              position=position_jitter(width=0.1,height=0), shape=21, size = 1)+
  guides(fill=guide_legend(title="treatment"))+
  theme_light()
```

- **出处**：(p.173)(p.174)

### 3.18 水平显示的箱形图 与 中值排序显示的箱形图

- **用途 / 适用数据**：水平翻转显示 (p.179)；「排序显示数据对更快地发现数据规律和获取数据信息尤为重要。对应 X 轴为类别向量时，最好将箱形图按中值降序后显示」(p.179)。输入＝连续变量 + 类别变量。
- **何时别用 / 坑**：「使用 ggplot2 包的 geom_boxplot() 函数，结合 coord_flip() 函数可以实现箱形图的水平翻转……虽然箱形图部分实现了水平翻转，但是右边的图例（legend）部分还是竖直的」；换成 `ggstance::geom_boxploth()` 可解决 (p.179)。
- **实现 / 关键参数**：水平 `ggplot2::geom_boxplot() + coord_flip()`，更好方案 `ggstance::geom_boxploth()` (p.179)；排序用 `reorder(Class, Value, median)` → `factor(..., levels=rev(levels(...)))` 反转水平 → `geom_boxplot()` (p.180)。

```r
Order_Class<-with(mydata,reorder(Class,Value,median))
Order_Class<-factor(Order_Class,levels=rev(levels(Order_Class)))
ggplot(mydata, aes(Order_Class,Value))+
  geom_boxplot(aes(fill = Class),notch = FALSE,outlier.alpha=1) +
  scale_fill_manual(values=c(brewer.pal(7,"Set2")[c(1,2,4,5)]))+
  scale_y_continuous(breaks=seq(0,15,3))+
  theme_light()
```

- **出处**：(p.179)(p.180)

### 3.19 带显著性标签的箱形图

- **用途 / 适用数据**：在箱形图上添加 p-value 与显著性标签（出版物图表）(p.176)。输入＝连续变量 + 类别变量。
- **R 中常用的比较方法（表 5-2-1）**：T-test → `t.test()`（两组，参数）；Wilcoxon test → `wilcox.test()`（两组，非参数）；ANOVA → `aov()` 或 `anova()`（多组，参数）；Kruskal-Wallis → `kruskal.test()`（多组，非参数）(p.176)。
- **实现 / 关键参数**：`ggpubr::compare_means()`（一组或多组间比较）+ `ggpubr::stat_compare_mean()`（自动添加 p-value、显著性标签）+ `ggpubr::ggboxplot()` (p.176)；`method`（"anova"/"t.test"/"wilcox.test"）、`comparisons`（成对比较列表）、`label="p.signif"`、`ref.group=".all."`、`hide.ns`、`add="jitter"`。

```r
library(ggpubr)
palette<-c(brewer.pal(7,"Set2")[c(1,2,4,5)])
ggboxplot(mydata, x = "Class", y = "Value",fill = "Class", palette = palette,
          add = "none",size=0.5,add.params = list(size = 0.25))+
  geom_hline(yintercept = mean(mydata$Value), linetype = 2)+
  stat_compare_means(method = "anova", label.x=0.8,label.y = 7.8)+
  stat_compare_means(label = "p.signif", method = "t.test",ref.group = ".all.", hide.ns = TRUE,label.y = 8) +
  theme_light()
compaired <- list(c("n", "s"), c("n","k"), c("n","mm"), c("s","k"))
ggboxplot(mydata, x = "Class", y = "Value",fill = "Class", palette = palette, add = "jitter",size=0.5)+
stat_compare_means(comparisons = compaired,method = "wilcox.test")+ theme_light()
```

- **出处**：(p.176)(p.177)

### 3.20 带连接线的双箱形图（成对样本 paired sample）

- **用途 / 适用数据**：比较成对样本（如治疗前后的两次测量），每个主体有两个测量值 (p.177)。输入＝同一主体的两次测量。
- **何时别用 / 坑**：`ggpubr::ggpaired()`「每对样本数据之间是使用直线连接的，这就导致数据可视化效果并不美观」，改为自定义 + `ggforce::geom_bezier()` 用光滑贝塞尔曲线连接 (p.178)；「其关键在于构造贝塞尔连接曲线的数据集」(p.178)。
- **实现 / 关键参数**：`ggpubr::ggpaired()` 或 `ggforce::geom_bezier()` + `reshape2::melt()` + `dplyr::arrange()` (p.178)；`geom_bezier(aes(group = index))` 按个体分组连曲线，`outlier.size = 0` 隐藏离群点避免与散点重复。数据集 `df_bezier` 由 `df_point` 按 class 拆分后 melt+arrange 构造控制点。

```r
library(ggplot2); library(reshape2); library(ggforce); library(dplyr)
set.seed(141079)
df_point <- data.frame(BAI2013 = rnorm(60), class = rep(rep(letters[1:3], each=10),2),
                   treatment = rep(c("elevated","ambient"),each=30), index=rep(seq(1,30),2))
ggplot()+
  geom_boxplot(data=df_point,aes(x = factor(treatment), y = BAI2013,fill=factor(treatment)),
               width=0.35,position = position_dodge(0),size=0.5,outlier.size = 0) +
  geom_point(data=df_point,aes(x = factor(treatment), y = BAI2013,fill=factor(treatment)),
             shape=21,colour="black",size=2)+
  geom_bezier(data= df_bezier,aes(x= treatment, y = value, group = index,linetype = 'cubic'),
              size=0.25,colour="grey20") +
  scale_fill_manual(values=brewer.pal(7,"Set2")[c(5,2)])+
  facet_grid(.~class)+ labs(x="treatment",y="Value")+ theme_light()
```

- **出处**：(p.177)(p.178)(p.179)

### 3.21 子母图（inset plot）

- **用途 / 适用数据**：在主图基础上再添加子图（与边际组合图「类似，但不完全相同」）(p.174)。输入＝两个图形对象（主图 + 子图）。
- **实现 / 关键参数**：`ggplot2` + `grid::viewport()`（ggplot2 基于 grid 绘图原理设计）；`viewport(x, y, width, height)`——x/y 为中心位点相对父图层的位置，width/height 为子图形大小 (p.175)。

```r
library(ggplot2)
library(grid)
p1 <- ggplot(iris, aes(Sepal.Length, Sepal.Width, fill = Species)) +
  geom_point(size = 4,shape=21,color="black") + theme_bw() + xlim(4, 10) + theme_light()
p2 <- ggplot(iris, aes(Species, Sepal.Width, fill = Species)) +
  geom_boxplot() + theme_bw() + ggtitle("Submian: Box plot") + theme_light()
subvp <- viewport(x = 0.78, y = 0.38, width = 0.4, height = 0.5)
p1
print(p2, vp = subvp)
```

- **出处**：(p.174)(p.175)

### 3.22 二维统计直方图 与 二维核密度估计图

- **用途 / 适用数据**：二维统计直方图展示二维数据的频数分布，X-Y 轴均为数值型，每个方块（bin）的颜色代表对应频数 (p.180)；二维核密度估计图分栅格形（raster）与多边形（polygon）两种 (p.181)。输入＝两个连续变量。
- **实现 / 关键参数**：`ggplot2::geom_bin2d()`（方块形，图 5-3-1a）、`ggplot2::geom_hex()`（六方形，图 5-3-1b），参数 `bins` 为 X/Y 轴分别设定的区间数目 (p.181)；另处用 `stat_binhex()` (p.184)。二维核密度用 `ggplot2::stat_density_2d()`，`geom="raster"` 对应栅格形、`geom="polygon"` 对应多边形，`aes(fill = ..density..)` 或 `..level..`、`contour`、`bins`、`h`（带宽）(p.181)。

```r
library(RColorBrewer); library(ggplot2)
colormap<- rev(brewer.pal(11,'Spectral'))
df <- data.frame(x=c(rnorm(mean=1.5, 5000), rnorm(mean=2.5, 5000)),
                 y=c(rnorm(mean=1.6, 5000), rnorm(mean=2.2, 5000)))
ggplot(df, aes(x,y)) +
  # geom_hex(bins = 40,na.rm=TRUE)+              # 对应六方形
  geom_bin2d (bins=40,na.rm=TRUE) +              # 对应方块形
  scale_fill_gradientn(colours=colormap)+ theme_classic()
ggplot(df, aes(x,y))+
  stat_density_2d (geom ="raster",aes(fill = ..density..),contour = F)+   # 栅格形
  # stat_density_2d (geom ="polygon",aes(fill = ..level..),bins=30 )+     # 多边形
  scale_fill_gradientn(colours= colormap)+ theme_classic()
```

- **出处**：(p.180)(p.181)

### 3.23 三维统计分布图（三维统计直方图 / 三维核密度估计图）

- **用途 / 适用数据**：三维柱形展示二维频数；三维曲面展示二维核密度 (p.182)。输入＝两个连续变量。
- **实现 / 关键参数**：三维统计直方图 = `gplots::hist2d()`（`nbins` 为 X/Y 方向箱形总数）+ `plot3D::hist3D()`；三维核密度估计图 = `MASS::kde2d()`（`h` 为 X/Y 方向带宽，`n` 为网格数）+ `plot3D::persp3D()` (p.182)；视角参数 `theta`、`phi`、`d`，`colkey`。

```r
library(plot3D); library(gplots)
df_hist<-hist2d(df$x,df$y, nbins=30)
pmar <- par(mar = c(5.1, 4.1, 4.1, 6.1))
hist3D(x=df_hist$x,y=df_hist$y,z=df_hist$counts, col = colormap, border = "black",space=0,alpha = 1,lwd=0.1,
       xlab = "x", ylab = "y",zlab = "Count", clab="Count", ticktype = "detailed",bty = "f",box = TRUE,
       theta = 65, phi = 20, d=3, colkey = list(length = 0.5, width = 1))
library(MASS)
df_density <- kde2d(df$x,df$y, n = 50, h = c(width.SJ(df$x), width.SJ(df$y)))
persp3D (df_density$x, df_density$y, df_density$z, theta = 60, phi = 20, d=3, col = colormap,
         border = "black", lwd=0.1, bty = "f",box = TRUE,ticktype = "detailed",
         xlab = "x", ylab = "y",zlab = "desnity",clab="desnity", colkey = list(length = 0.5, width = 1))
```

- **出处**：(p.182)(p.183)

### 3.24 二维与一维统计分布组合图

- **用途 / 适用数据**：二维统计直方图/核密度估计图结合一维统计分布图表，「更加详细地揭示数据的分布情况」(p.183)。输入＝两个连续变量。
- **实现 / 关键参数**：`gridExtra::grid.arrange()` 组合 ggplot2 绘制的一维与二维统计分布图 (p.183)；`grid.arrange(..., ncol, nrow, widths, heights)`，边际图用 `theme_void()` 去背景。

```r
library(ggplot2); library(gridExtra); library(RColorBrewer)
Colormap <- rev(brewer.pal(11,'Spectral'))
N<-300
data <- data.frame(x=c(rnorm(mean=1.5,N), rnorm(mean=2.5,N)), y=c(rnorm(mean=1.6,N), rnorm(mean=2.2,N)))
hist_top <- ggplot(data, aes(x)) + geom_density(colour="black",fill='#5E4FA2',size=0.25)+ theme_void()
hist_right <- ggplot(data, aes(y)) + geom_density(colour="black",fill='#5E4FA2',size=0.25)+
  theme_void()+ coord_flip()
scatter<-ggplot(data, aes(x, y)) + stat_binhex(bins = 15,na.rm=TRUE,color="black")+
  scale_fill_gradientn(colours=Colormap)+ theme_minimal()
grid.arrange(hist_top, empty, scatter, hist_right, ncol=2, nrow=2, widths=c(4,1), heights=c(1,4))
```

- **出处**：(p.183)(p.184)

### 3.25 金字塔图（population pyramid）与镜面图

- **用途 / 适用数据**：「通常用来理解人口结构……是彼此背靠背的一对直方图，通常用于显示所有年龄组和男女人口的分布情况」；X=人口数量，Y=年龄组别；最适合检测人口模式的变化或差异 (p.184)。底部宽顶部窄＝高生育率和高死亡率；顶部宽底部窄＝人口老龄化且生育率低 (p.184)。输入＝两个数据系列（male/female）+ 类别变量（年龄分段）+ 数值。
- **实现 / 关键参数**：**直方图类型**用 `geom_bar(stat="identity", position="identity")`；**面积图类型**用 `geom_area(stat="identity", position="identity")`。技巧：female 数值取负，再用 `scale_y_continuous(labels = abs, ...)` 把标签转回正值，`coord_flip()` 翻转 (p.184)(p.185)。面积图 X 轴只能为数值型，需先构造 X 轴辅助数据 `age_x` 再替换坐标标签 (p.184)。

```r
library(ggplot2)
df<-read.csv("Population_Pyramid_Data.csv",header=TRUE)
df[df$gender == "female",]$pop<--df[df$gender == "female",]$pop
df$age<-factor(df$age,levels=df$age[seq(1,nrow(df)/2,1)])
# 图 5-4-1(a1) 直方图类型的金字塔图
ggplot(data = df, aes(x =age , y = pop, fill = gender)) +
  geom_bar(stat = "identity",position = "identity",color="black",size=0.25) +
  scale_y_continuous(labels = abs, limits = c(-400, 400), breaks = seq(-400, 400, 100)) +
  coord_flip() + theme_light()
# 图 5-4-1(b1) 面积图类型的金字塔图
df$age_x<-rep(seq(0, 100,5),2)
ggplot(data = df, aes(x =age_x , y = pop, fill = gender)) +
  geom_area(stat = "identity", position = "identity",color="black",size=0.25) +
  scale_fill_manual(values=c("#36BED9","#FBAD01"))+
  scale_y_continuous(labels = abs, limits = c(-400, 400), breaks = seq(-400, 400, 100)) +
  scale_x_continuous(breaks = seq(0, 100, 5),labels=df$age[seq(1,nrow(df)/2,1)])+ coord_flip() + theme_light()
```

- **出处**：(p.184)(p.185)

### 3.26 【附】分布型示例数据的构造（书例）

- **用途 / 适用数据**：4 类各 100 点：n（正态 μ=3, σ=1）、s（右偏 Johnson，偏斜度 2.0、峰度 13.1）、k（尖峰态，偏斜度 2.2、峰度 20.0）、mm（双峰 μ1=1.89、μ2=3.79，σ1=σ2=0.31）(p.161)。
- **实现 / 关键参数**：`rnorm()` 构造高斯单峰/多峰数据；`SuppDists::rJohnson()` 构造 Johnson 分布数据；配合 `geom_density()` + `facet_grid()` (p.161)(p.162)。

```r
library(ggplot2); library(RColorBrewer); library(SuppDists)
set.seed(141079)
findParams <- function(mu, sigma, skew, kurt) {
  value <- .C("JohnsonMomentFitR", as.double(mu), as.double(sigma), as.double(skew), as.double(kurt - 3),
              gamma = double(1), delta = double(1), xi = double(1), lambda = double(1), type = integer(1), PACKAGE = "SuppDists")
  list(gamma = value$gamma, delta = value$delta, xi = value$xi, lambda = value$lambda, type = c("SN", "SL", "SU", "SB")[value$type])
}
n <- rnorm(100,3,1); s <- rJohnson(100, findParams(3, 1, 2., 13.1)); k <- rJohnson(100, findParams(3, 1, 2.2, 20))
mm <- rnorm(100, rep(c(2, 4), each = 50) * sqrt(0.9), sqrt(0.1))
mydata <- data.frame( Class = factor(rep(c("n" , "s", "k", "mm"), each = 100), c("n", "s", "k", "mm")), Value = c(n, s, k, mm))
ggplot(mydata, aes(Value,fill=Class))+
  geom_density(alpha=1,bw=0.3,colour="black",size=0.25)+
  scale_fill_manual(values=brewer.pal(7,"Set2")[c(1,2,4,5)])+ facet_grid(Class~.)+ theme_light()
```

- **出处**：(p.161)(p.162)

---

## 第 4 部分：时间序列型图表（第 6 章）

> 本章原书的时间序列图表取舍判断（折线图 vs 曲线图、面积图系列数上限、堆积面积图 vs 堆积柱形图、日历图/螺旋图/量化波形图/地平线图的适用理由）已统一汇总到「第 10 部分」。

### 4.1 折线图（line chart）

- **用途 / 适用数据**：在连续间隔或时间跨度上显示定量数值，最常用来显示趋势和关系；也能给出某时间段内的整体概览 (p.187)。输入＝X 为类别型或序数型（日期）变量，Y 为数值型变量，可多数据系列 (p.187)。
- **何时别用 / 坑**：不推荐三维折线图；堆积/百分比堆积折线图改用面积图；X 轴为数值格式时改用曲线图 (p.187)。
- **实现 / 关键参数**：`ggplot2::geom_line()` (p.189)；`aes(x=date, y=value, colour/group=系列)`、`scale_x_date(date_labels="%Y", date_breaks="2 year")`。
- **出处**：(p.187)(p.189)

### 4.2 面积图（area graph）

- **用途 / 适用数据**：在折线图基础上将折线与自变量坐标轴之间的区域用颜色或纹理填充，更好地突出趋势信息；「最常用来显示趋势，而非表示具体数值」(p.187)。输入＝时间/连续 X + 数值 Y。
- **何时别用 / 坑**：多系列需设透明度避免遮挡；系列数不超过 3 个，多则用折线图/分面面积图/峰峦图 (p.187)。
- **实现 / 关键参数**：`ggplot2::geom_area()`；颜色映射填充用 `geom_bar()` + `geom_line()` (p.189)；`alpha`（透明度）、`fill=y` 颜色映射、`spline(..., n=1000, method="natural")` 插值加密、`scale_x_date()`。

```r
library(ggplot2); library(RColorBrewer)
mydata<-read.csv("Area.csv",stringsAsFactors=FALSE)
mydata$date<-as.Date(mydata$date)
newdata<-data.frame(spline(as.numeric(mydata$date),mydata$value,n=1000,method= "natural"))
newdata$date<-as.Date(newdata$x,origin = "1970-01-01")
ggplot(newdata, aes(x =date, y = y) )+
  geom_bar(aes(fill=y,colour=y),stat = "identity",alpha=1,width = 1)+
  geom_line(color="black",size=0.5)+
  scale_color_gradientn(colours= brewer.pal(9,'Reds'),name = "Value")+
  scale_x_date(date_labels = "%Y",date_breaks = "2 year")
```

- **出处**：(p.187)(p.189)

### 4.3 两条折线间填充面积图（夹层填充面积图）

- **用途 / 适用数据**：「两条折线之间可以使用面积填充，这样可以很清晰地观察数据之间的差异变化」，仅适用于双数据系列的数值差异比较 (p.188)。输入＝两个数据系列的同一时间轴数值（书例 AMZN vs AAPL）。
- **三种形式**：(a) 单色填充；(b) 分段填充（AMZN > AAPL 用蓝色，反之用红色）；(c) 颜色映射填充 (p.188)。
- **实现 / 关键参数**：(c) 用 `ggridges::geom_ridgeline_gradient()` (p.188)。
- **出处**：(p.188)

### 4.3.1 颜色映射填充面积图

- **用途 / 适用数据**：仅适用于**单数据系列**的面积图 (p.187)。实现为 `geom_bar()` + `geom_line()` (p.189)。

### 4.4 堆积面积图 / 百分比堆积面积图

- **用途 / 适用数据**：堆积面积图「每一个系列的开始点是先前数据系列的结束点」，最大面积代表所有数据量总和，适合比较同一间隔内多个变量的变化 (p.190)。百分比堆积面积图「该图并不能反映总量的变化，但是可以清晰地反映每个数值所占百分比随时间或类别变化的趋势线，对于分析各个指标分量占比极为有用」(p.190)。输入＝时间（连续）+ 多个数值系列（长表）。
- **何时别用 / 坑**：「所以层叠面积图不适用于表示带有负值的数据集」(p.190)；X 轴只能表示连续数据（时间或数值），分类数据请用堆积柱形图 (p.190)。
- **实现 / 关键参数**：`ggplot2::geom_area(position="stack")` / `geom_area(position="full")` (p.190)；需先 `reshape2::melt()` 转长表。

```r
library(ggplot2)
mydata<-read.csv("StackedArea_Data.csv",stringsAsFactors=FALSE)
mydata$Date<-as.Date(mydata$Date)
mydata<-melt(mydata,id="Date")
ggplot(mydata, aes(x =Date, y = value,fill=variable) )+
  geom_area(position="stack",alpha=1)+
  geom_line(position="stack",size=0.25,color="black")+
  scale_x_date(date_labels = "%Y",date_breaks = "2 year")
```

- **出处**：(p.190)(p.191)

### 4.5 日历图（calendar heatmap：以年为单位 / 以月为单位）

- **用途 / 适用数据**：以年为单位的日历热力图，Value 按 Date 在日历上展示并映射到颜色 (p.191)；以月为单位的日历图格子内可标注日期数字 (p.194)。输入＝(Date, Value)。
- **何时别用 / 坑**：`ggTimeSeries::ggplot_calendar_heatmap()`「可以绘制如图 6-2-2(a) 所示的日历图，但是不能设定日历图每个时间单元的边框格式」；改用 `stat_calendar_heatmap()` + `ggplot()` 可调整边框格式 (p.193)。关键：「使用 as.integer(strftime()) 日期型处理组合函数获取某天对应所在的年份、月份、周数等数据信息」(p.193)。
- **实现 / 关键参数**：年单位 `ggTimeSeries::ggplot_calendar_heatmap()` / `ggTimeSeries::stat_calendar_heatmap()` + `data.table::data.table()` + `RColorBrewer` + `facet_wrap(~Year)` (p.193)；月单位 `ggplot2::geom_tile()` + `facet_wrap()` + `dplyr` 构造 `monthweek` (p.194)；`geom_tile(colour="white")`（格子边框）、`monthweek=1+week-min(week)`（月内第几周）、`scale_y_reverse()`、`strftime(date, "%Y"/"%m"/"%W"/"%u")`。

```r
library(ggplot2); library(data.table); library(ggTimeSeries); library(RColorBrewer)
set.seed(1234)
dat <- data.table(date = seq(as.Date("1/01/2014", "%d/%m/%Y"),as.Date("31/12/2017", "%d/%m/%Y"),"days"),
                  ValueCol = runif(1461))
dat[, ValueCol := ValueCol + (strftime(date,"%u") %in% c(6,7) * runif(1) * 0.75), .I]
dat[, ValueCol := ValueCol + (abs(as.numeric(strftime(date,"%m")) - 6.5)) * runif(1) * 0.75, .I]
dat$Year<- as.integer(strftime(dat$date, '%Y')); dat$month <- as.integer(strftime(dat$date, '%m')); dat$week<- as.integer(strftime(dat$date, '%W'))
MonthLabels <- dat[,list(meanWkofYr = mean(week)), by = c('month') ]; MonthLabels$month <-month.abb[MonthLabels$month]
ggplot(data=dat,aes(date=date,fill=ValueCol))+
  stat_calendar_heatmap()+
  scale_fill_gradientn(colours= rev(brewer.pal(11,'Spectral')))+
  facet_wrap(~Year, ncol = 1,strip.position = "right")+
  scale_y_continuous(breaks=seq(7, 1, -1),labels=c("Mon","Tue","Wed","Thu","Fri","Sat","Sun"))+
  scale_x_continuous(breaks = MonthLabels[,meanWkofYr], labels = MonthLabels[, month],expand = c(0, 0)) +
  xlab(NULL)+ ylab(NULL)
```

（以月为单位）

```r
library(dplyr)
dat17 <- filter(dat,Year==2017)[,c(1,2)]
dat17$monthf<-factor(as.integer(strftime(dat17$date, '%m')),levels=as.character(1:12),labels=c("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"),ordered=TRUE)
dat17$weekdayf<-factor(as.integer(strftime(dat17$date, '%u')),levels=(1:7),labels=(c("Mon","Tue","Wed","Thu","Fri","Sat","Sun")),ordered=TRUE)
dat17$week<- as.integer(strftime(dat17$date, '%W'))
dat17<-dat17 %>% group_by(monthf)%>%mutate(monthweek=1+week-min(week))
dat17$day<-strftime(dat17$date, "%d")
ggplot(dat17, aes(weekdayf, monthweek, fill=ValueCol)) +
  geom_tile(colour = "white") + scale_fill_gradientn(colours=colormap)+
  geom_text(aes(label=day),size=3)+
  facet_wrap(~monthf ,nrow=3) + scale_y_reverse()+
  xlab("Day") + ylab("Week of the month")
```

- **出处**：(p.191)(p.193)(p.194)

### 4.6 螺旋图系列（螺旋柱形图 / 螺旋热力图 / 径向图 / 螺旋面积图）

- **用途 / 适用数据**：沿阿基米德螺旋线画基于时间的数据，从中心点向外发展；节省空间显示大时间段趋势、直观表达周期性 (p.194)(p.195)。数据结构一般为 (Date, Value)，Date 沿螺旋线展开，Value 同时映射到柱形高度和色带 (p.195)。
- **变体**：螺旋柱形图（Value → 柱高 + 色带）、螺旋热力图（Value → 方块颜色）；径向柱形图、径向热力图（螺旋排布换成径向排布）(p.195)(p.196)。「总的来说，螺旋柱形图和径向柱形图都是使用柱形高度和颜色两个视觉特征展示数据的」(p.196)。螺旋面积图「只是将图 6-3-2(a) 的柱形展示换成面积展示，这样更加适合连续的时序数据的可视化」，图 6-3-5(b) 为颜色映射填充版 (p.197)。
- **实现 / 关键参数**：柱形版用 `ggplot2::geom_polygon()` 自定义 4 个顶点 `(x,y)、(x,y+width)、(x+width)、(x+width, y+width)` 绘制四边形（width 为多边形的高度与宽度数值），再 `coord_polar()` (p.196)；数据读取用 `readxl::read_excel()`，聚合用 `dplyr` (p.196)；`N`（一圈的时间单位数，如 24 小时）、`width`（柱宽）、`group=interaction(hour, day)`。面积版纯色填充用 `geom_ribbon()`，颜色映射填充用 `geom_linerange()` + `geom_line()` (p.198)；阿基米德螺旋线构造：按年给 `Asst` 赋 `seq(i*Step, (i+1)*Step, length.out=...)`，`Step=5` (p.198)；`Height`（值归一化上限）、`coord_polar(theta="x", start=0)`。

```r
library(dplyr); library(ggplot2); library(readxl); library(RColorBrewer)
dat <- read_excel("SpiralChart_Data.xlsx")   # 3732 x 3："Date","Time","Value"
dat$time <-  with(dat, as.POSIXct(paste(Date, Time), tz="GMT"))
dat$hour <-  as.numeric(dat$time) %% (24*60*60) / 3600
dat$day <- as.Date(dat$time); dat$datt<-as.numeric(strftime(dat$day , "%d"))-min(as.numeric(strftime(dat$day,"%d")))
dat$Value <- as.numeric(dat$Value); dat$Value2<-dat$Value/max(dat$Value)
N<-24; width<-0.5
bars <- dat %>%
  mutate(hour.group = as.numeric(as.character(cut(hour, breaks=seq(0,24,width), labels=seq(0,23.75,width),include.lowest=TRUE)))) %>%
  group_by(datt, hour.group) %>% summarise(meanTT = mean(Value2))  %>%
  mutate(value=meanTT*max(dat$Value), xmin= hour.group, xmax = hour.group + width, ymin = datt*N + hour.group, ymax = datt*N + hour.group + meanTT*N*1.1)
poly <- bars %>% rowwise() %>%
  do(with(., data_frame(day=datt, date=day, hour=hour.group, value=value,
                        x = c(xmin, xmax, xmax, xmin), y = c(ymin , ymin + width, ymax + width, ymax ))))
ggplot(poly, aes(x, y, group = interaction(hour, day),fill=value)) +
  geom_polygon(colour="black",size=0.25) + coord_polar() +
  scale_x_continuous(limits=c(0,N), breaks=seq(0,N-1,1), minor_breaks=0:N, labels=paste0(rep(c(12,1:11),1), rep(c("AM","PM"),each=12))) +
  scale_y_continuous(limits=c(-N/2, max(poly$y)), breaks=seq(N,max(poly$y),N), labels=unique(dat$day) )+
  scale_fill_gradientn(colours= brewer.pal(9,'YlGnBu'))+ ylab("Date")+ xlab("")+ theme_bw()
```

（螺旋面积图：构造 + 绘图）

```r
library(ggplot2); library(data.table); library(RColorBrewer)
dtData <- data.table(date = seq(as.Date("1/01/2014", "%d/%m/%Y"), as.Date("31/12/2017", "%d/%m/%Y"),"days"), ValueCol = runif(1461))
dtData$Year<- as.integer(strftime(dtData$date, '%Y'))
dtData$DateNum<-as.numeric(dtData$date)-as.numeric(as.Date(paste(as.character(strftime(dtData$date, "%Y")),"-01-01", sep = ""))))
Step<-5; dtData$Asst<-rep(Step,nrow(dtData)); YearRange<-unique(dtData$Year)
for(i in 1:length(YearRange)){ dtData$Asst[dtData$Year==YearRange[i]]<-seq(i*Step, (i+1)*Step, length.out = length(dtData$Asst[dtData$Year==Year[i]])))}
Height<-4.8; dtData$Valueht<-(dtData$ValueCol-min(dtData$ValueCol))/(max(dtData$ValueCol)-min(dtData$ValueCol))*Height
circlelabel<-c("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec")
circlemonth<-seq(15,345,length=12); circlebj<-rep(c(-circlemonth[1:3],rev(circlemonth[1:3])),2)
ggplot()+
 geom_linerange(data=dtData,aes(x=DateNum,ymin=Asst- Step,ymax=Asst+Valueht- Step,color=ValueCol),size =1)+
  geom_line(data=dtData,aes(x=DateNum,y=Asst+Valueht- Step,group=Year),size =0.25,color="black")+
  geom_line(data=dtData,aes(x=DateNum,y=Asst- Step,group=Year),size =0.25,color="grey20")+
  geom_text(data=NULL,aes(x=circlemonth,y=28,label= circlelabel, angle=circlebj),size=4,color="grey50")+
  coord_polar(theta="x",start=0)+
  scale_x_continuous(breaks=c(1,31,59,90,120,151,181,212,243,273,304,334)))+
  scale_y_continuous(limits=c(-Step,28),breaks=c(2.5,7.5,12.5,17.5),labels=c("2014","2015","2016","2017"))+
  scale_color_gradientn(colours= rev(brewer.pal(11,'Spectral'))))+ ylab("Year")+ theme_bw()
```

- **出处**：(p.194)(p.195)(p.196)(p.197)(p.198)(p.199)

### 4.7 量化波形图 / 河流图 / 主题河流图（stream graph / theme river chart）

- **用途 / 适用数据**：「是堆积面积图的一种变形，通过"流动"的形状来展示不同类别的数据随时间的变化情况」；不同于堆积面积图，它「将数据分散到一个变化的中心基准线上（该基准线不一定是笔直的）」(p.199)。用颜色区分类别，流向与表示时间的 X 轴平行，每个类别的数值与波浪的宽度成比例 (p.199)。
- **何时别用 / 坑**：见「第 10 部分」——大型数据集下混乱、小数值类别被"淹没"、无法读取精确数值 (p.200)；另一坑：「由于没有使用交互技术，而只是静态图表，从而导致数据系列太多时，很难将图例与图表中的波形数据系列一一对应」→「在展示量化波形图前，最好先根据数据系列最大值进行排序处理」(p.200)。
- **实现 / 关键参数**：`ggTimeSeries::stat_steamgraph()`；排序「先使用 apply() 函数求取每个数据系列的最大值，然后使用 sort() 函数对所有数据系列的最大值进行排序」(p.201)。替代：时间序列的峰峦图 (p.201)。`levels=colnames(df_series)[Col_Sort$ix]` 按系列最大值降序重排因子水平。

```r
library(ggplot2); library(reshape2); library(ggTimeSeries)
df<-read.csv("StreamGraph_Data.csv",header=TRUE)
df_series<-df[,2:ncol(df)]
Col_Max<-apply(df_series,2,max)
Col_Sort<-sort(Col_Max,index.return=TRUE,decreasing = TRUE)
mydata<-melt(df,id="time")
mydata$variable<-factor(mydata$variable,levels=colnames(df_series)[Col_Sort$ix])
ggplot(mydata, aes(x = time, y = value, group = variable, fill = variable)) +
  stat_steamgraph(colour="black",size=0.25)+
  xlab('Time') + ylab('') + theme_light()
```

- **出处**：(p.199)(p.200)(p.201)

### 4.8 地平线图（horizon graph）

- **用途 / 适用数据**：「在 Panopticon 软件开发时提出的一种时序数据可视化方法」，最初被金融投资经理用来展示同一时间的股票数据 (p.202)；用途见「第 10 部分」(p.202)。输入＝多个数据系列的长时序数据（书例 15 个 series × 250 点），X 为时间/序号，Y 为数值。
- **何时别用 / 坑**：折线图/面积图「无法观察到异常的数据，且对于大数据集的图表占用面积较大」，这才是地平线图的适用场景 (p.202)。构造步骤（图 6-5-2）：(1) 用基于起始日期数值的百分比替代实际价格，保证不同系列同高、增强对比；(2) 双向渐变颜色主题用于颜色条带，蓝=正值、红=负值，每个条带高度对应数据变化比例（图中为 10%）；(3) 把红色（负值）条带折叠对应负值部分，降低高度；(4) 双伪色调着色技术（two-tone pseudo colourig）把条带平移到 X 轴，可将图表高度降低 2/3；(5) 用分面展示技术（small multiple）纵向排列多个系列 (p.203)。
- **实现 / 关键参数**：`latticeExtra::latticeExtra()` 和 `ggalt::geom_horizon()` 都可绘制地平线图（ggalt 安装：`devtools::install_github("hrbrmstr/ggalt")`）(p.204)；`geom_horizon(bandwidth=10)`（每个颜色条带的数值带宽，书图 6-5-2(b) 条带高度代表 10% 的数据变化）(p.203)、`scale_fill_manual(values=colormap)`（双向渐变色板）、`facet_wrap(~variable, ncol=1, strip.position="left")`（small multiple 纵向排列）、`panel.spacing.y`（压缩分面间距）。

```r
library(ggplot2); library(RColorBrewer); library(reshape2)
library(ggalt) # ggalt 的下载语句：devtools::install_github("hrbrmstr/ggalt")
colormap <- colorRampPalette(rev(brewer.pal(11,'RdYlBu')))(15)
df<-as.data.frame(matrix(cumsum(rnorm(250 * 15)), ncol = 15))
colnames(df) <- paste("series", LETTERS[1:15]); df$x<-rownames(df)
dfData<-melt(df,id='x')
ggplot(dfData, aes(x =as.numeric(x), y = value) )+
  geom_horizon(colour=NA,size=0.25,bandwidth=10)+
  facet_wrap(~variable, ncol = 1,strip.position = "left")+
  scale_fill_manual(values=colormap)+ xlab('Time') + ylab('') + theme_bw()+
  theme(strip.background = element_blank(), strip.text.y = element_text(hjust=0, angle=180,size=10),
        axis.text.y=element_blank(), panel.grid = element_blank(), panel.spacing.y=unit(-0.05, "lines"),
        panel.grid.major.y=element_blank(), panel.grid.minor.y =element_blank(), axis.ticks.y = element_blank())
```

- **出处**：(p.202)(p.203)(p.204)

---

## 第 5 部分：局部整体型图表（第 7 章，pp.205–215）

### 5.0 家族定义与通用警告

**家族成员**：「局部整体型图表能显示出局部组成成分与整体的占比信息，主要包括饼图、圆环图、旭日图、华夫饼图、矩形树状图等」(p.82，第 1 章 1.8.5)。第 7 章展开：饼图、圆环图、复合饼图系列、马赛克图、华夫饼图。通用警告：「这类图很难去精确比较不同组成的大小」(p.82)。

### 5.1 饼图的 4 条否定性判断（原文完整还原）

1. 「不适用于多分类的数据，原则上一张饼图不可多于 9 个分类。因为随着分类的增多，每个切片就会变小，最后导致大小区分不明显，每个切片看上去都差不多大」(p.206)
2. 「相对具备同样功能的其他图表（比如百分比堆积柱形图、圆环图），饼图需要占据更大的画布空间，所以饼图不适合用于数据量大的场景」(p.206)
3. 「很难在多个饼图之间进行数值比较，此时可以使用百分比堆积柱形图或者百分比堆积条形图替代」(p.206)
4. 「不适合多变量的连续数据的占比可视化，此时应该使用百分比堆积面积图展示数据，比如多变量的时序数据」(p.206)

### 5.2 饼图排序规则（必做）

- 「在绘制饼图前一定注意要把多个类别按一定的规则排序，但不是简单地升序或者降序」(p.206)；「千万不要将饼图的类别数据按从小到大、顺时针方向展示……最不重要的部分就会占据图表最显著的位置」(p.206)
- 人「阅读饼图就如同阅读钟表一样，会潜意识地从 12 点开始顺时针往下阅读」(p.206)
- 最大占比 **>50%**：最大块放 12 点**右边**，第二大放 12 点**左边**，其余**逆时针**，最小块落到底部（图 7-1-1(a)）(p.206)
- 最大占比 **<50%**：从 12 点右侧起**从小到大、顺时针**排列（图 7-1-1(b)）(p.206)

### 5.3 饼图（pie chart）

- **用途**：将圆饼按分类占比切成扇形切片，整圆代表总量，所有切片加和等于 100%，表示不同分类的占比 (p.206)
- **适用数据**：一维分类 + 一个数值（绝对量或已归一化占比），单数据系列，分类数 ≤9 (p.206)
- **何时别用 / 坑**：见 5.1 节的 4 条否定性判断 (p.206)；必须排序，禁止「从小到大 + 顺时针」(p.206)
- **实现路径**：`graphics::pie()`（**书中推荐**）；备选 `ggplot2::geom_bar()` + 直角坐标转极坐标 + `geom_text()`；配色 `RColorBrewer::brewer.pal()`；排序 `dplyr::arrange()`
- **最小可运行代码**（图 7-1-1(a)，最大占比 >50% 排布）：

```r
library(RColorBrewer)
library(dplyr)
library(graphics)
df <- data.frame(value = c(24.20,75.90,12.50,12.30,8.10,12.10),
                 group = c('LVS','SJM','MCE','Galaxy','MGM','Wynn'))
df <- arrange(df, desc(value))
df$color <- rev(brewer.pal(nrow(df), "Oranges"))
df <- df[c(2:nrow(df),1),]           # 最大块移到 12 点右侧
labs <- paste0(df$group," \n(", round(df$value/sum(df$value)*100,2), "%)")
pie(df$value, labels=labs, init.angle=90, col = df$color, border="black")
```

(p.207)；图 7-1-1(b)（<50%，从小到大顺时针）：

```r
df <- arrange(df, value)             # 升序
labs <- paste0(df$group," \n(", round(df$value/sum(df$value)*100,2), "%)")
pie(df$value, labels=labs, init.angle=90, col = brewer.pal(nrow(df), "Reds"),
    border="black")
```

(p.208)

- **关键参数**：`x`（数值向量）、`labels`（`paste0` 拼名称+百分比）、`init.angle=90`（起始于 12 点）、`col`（配色）、`border="black"` (p.207-208)
- **出处**：(p.206-208)

### 5.4 圆环图（donut chart）

- **用途**：将饼图中间挖空，展示各分类占比并支持多个整体之间的对比 (p.208)
- **适用数据**：同饼图（分类 + 占比），场景是需要并排比较多个整体
- **何时别用 / 坑**：「饼图的整体性太强，会让我们将注意力集中在比较饼图内各个扇形之间占整体比重的关系。但如果我们将两个饼图放在一起，则很难同时对比两个图」——跨图比较改用圆环图 (p.208)
- **实现路径**：书中**未给出**圆环图代码；依赖饼图思路（`graphics::pie()` 叠加空白圆，或 `ggplot2::geom_bar()+coord_polar()`），第 7 章未列出专用包
- **最小可运行代码**：原文无代码块 (p.208)
- **关键参数**：书中仅说明空心区域用途——显示标题等文本信息 (p.208)
- **出处**：(p.208)

### 5.5 复合饼图系列（compound scatter/bubble and pie chart）

- **用途**：在每个坐标位置画一个小饼图，同时表达位置/大小 + 一组内部占比 (p.208)
- **适用数据**：散点复合饼图 = 3 变量 `(x, y, P)`，x、y 决定位置，P 为饼图各类别占比 (p.208)；气泡复合饼图 = 4 变量 `(x, y, z, P)`，z 决定气泡大小 (p.208)
- **何时别用 / 坑**：`geom_scatterpie()` **只能**结合 `ggplot2::coord_fixed()` 使用，以保证 X、Y 轴使用同一最小单位 (p.209)；「推荐根据数据集每个数据系列的均值做排序处理后，再绘制饼图展示数据，使读者能更好地发现数据规律」(p.210)
- **实现路径**：`scatterpie` 包的 `geom_scatterpie()`、`geom_scatterpie_legend()` + `ggplot2::coord_fixed()` + `RColorBrewer::brewer.pal()`（教程 https://cran.r-project.org/web/packages/scatterpie/vignettes/scatterpie.html）(p.209)
- **最小可运行代码**（图 7-1-3(b) 气泡复合饼图）— 数据准备：

```r
library(ggplot2)
library(scatterpie)
library(RColorBrewer)
colormap <- colorRampPalette(brewer.pal(7, "Set2"))(7)
crime <- read.csv("crimeRatesByState2005.tsv", header = TRUE, sep = "\t", stringsAsFactors = F)
radius <- sqrt(crime$population / pi)
Max_radius <- max(radius)
Bubble_Scale <- 0.1
crime$radius <- Bubble_Scale * radius/Max_radius
mydata <- crime[,c(2,4,3,5:8)]        # 数据集的选择与排序处理
Col_Mean <- apply(mydata, 2, mean)
Col_Sort <- sort(Col_Mean, index.return=TRUE, decreasing = TRUE)
mydata <- mydata[,Col_Sort$ix]
#对 X 轴和 Y 轴变量数值做归一化处理至[0, 1]区间
x <- (mydata$murder-min(mydata$murder))/(max(mydata$murder)-min(mydata$murder))+0.00001
y <- (mydata$Robbery-min(mydata$Robbery))/(max(mydata$Robbery)-min(mydata$Robbery))+0.00001
mydata1 <- data.frame(x, y, radius=crime$radius)
mydata2 <- cbind(mydata1, mydata)
Legnd_label <- colnames(mydata2)[4:10]
colnames(mydata2)[4:10] <- LETTERS[1:7]  #按字母顺序重新命名数据系列的列名
```

(p.210)；绘图（原文另有 xbreak/ybreak 刻度换算语句，见 p.210 中段）：

```r
ggplot() +
  geom_scatterpie(aes(x=x, y=y, r=radius), data=mydata2,
                  cols=colnames(mydata2)[4:10], alpha=0.9, size=0.25) +
  scale_fill_manual(values=colormap, labels=Legnd_label)+
  geom_scatterpie_legend(mydata2$radius, x=0.1, y=0.95, n=5,
      labeller=function(x) round((x* Max_radius / Bubble_Scale)^2*pi))+
  scale_x_continuous(breaks=xbreak, labels=xlabel)+
  scale_y_continuous(breaks=ybreak, labels=ylabel)+
  xlab("murder")+ ylab("Robbery")+
  coord_fixed()
```

(p.210)

- **关键参数**：`aes(x, y, r)`（r 为饼图半径）、`cols`（参与饼图的数据列名向量）、`geom_scatterpie_legend(radius, x, y, n, labeller)`（气泡图例与反算标签）、`coord_fixed()` (p.210)
- **出处**：(p.208-210)

### 5.6 马赛克图（mosaic plot / marimekko chart）

- **用途**：显示**分类数据中一对变量之间**的关系，原理类似双向的 100% 堆叠式条形图，所有条形在数值轴上等长并再分段 (p.211)
- **适用数据**：二维列表型分类数据（行 segment 分组、列 variable 类别）：先按行求每个 variable 的占比，再按行求和得到列宽占比 (p.211)
- **何时别用 / 坑**：「主要缺点在于难以阅读，特别是当含有大量分段的时候」(p.211)；「很难准确地对每个分段进行比较，因为它们并非沿着共同基线排列在一起。因此，马赛克图比较适合提供数据概览」(p.211)；非均匀马赛克图「关注的数据维度非常多，一般的用户很难直观理解，在多数情况下可以被拆解成多个不同的图表」(p.211)；边界：马赛克图 = 非关系型列表数据，矩形树状图 = 关系型树形数据 (p.213)
- **实现路径**：`ggplot2::geom_rect()`（**书中推荐**，「虽然代码比其他三种方法稍微复杂，但是可以绘制得更加美观」）；备选 `ggmosaic::geom_mosai()`、`graphics::mosaicplot()`、`vcd::mosaic()`；辅助 `reshape2::melt()`、`plyr::ddply()`、`plyr::join()`、`RColorBrewer` (p.212)
- **最小可运行代码** — 数据计算：

```r
library(ggplot2)
library(RColorBrewer)
library(reshape2)  # 提供 melt()函数
library(plyr)      # 提供 ddply()函数,join()函数
df <- data.frame(segment = c("A", "B", "C","D"),
                     Alpha = c(2400,1200,600,250),
                     Beta  = c(1000,900, 600,250),
                     Gamma = c(400,600,400,250),
                     Delta = c(200,300,400,250))
melt_df <- melt(df, id="segment")
segpct <- rowSums(df[,2:ncol(df)])
for (i in 1:nrow(df)){
  for (j in 2:ncol(df)){
    df[i,j] <- df[i,j]/segpct[i]*100  # 将数字转换成百分比
  }
}
segpct <- segpct/sum(segpct)*100
df$xmax <- cumsum(segpct)
df$xmin <- (df$xmax - segpct)
dfm <- melt(df, id = c("segment","xmin","xmax"), value.name="percentage")
dfm1 <- ddply(dfm, .(segment), transform, ymax = cumsum(percentage))
dfm1 <- ddply(dfm1, .(segment), transform, ymin = ymax - percentage)
dfm1$xtext <- with(dfm1, xmin + (xmax - xmin)/2)
dfm1$ytext <- with(dfm1, ymin + (ymax - ymin)/2)
dfm2 <- join(melt_df, dfm1, by = c("segment","variable"), type="left", match="all")
```

(p.212)；绘图：

```r
ggplot()+
geom_rect(aes(ymin=ymin, ymax=ymax, xmin=xmin, xmax=xmax, fill=variable), dfm2, colour="black") +
 geom_text(aes(x=xtext, y=ytext, label=value), dfm2, size=4)+
 geom_text(aes(x=xtext, y=103, label=paste("Seg ", segment)), dfm2, size=4)+
 geom_text(aes(x=102, y=seq(12.5,100,25), label=c("Alpha","Beta","Gamma","Delta")), size=4, hjust=0)+
 scale_x_continuous(breaks=seq(0,100,25), limits=c(0,110))+
 theme(panel.background=element_rect(fill="white",colour=NA),
       panel.grid.major = element_line(colour="grey60",size=.25,linetype="dotted"),
       panel.grid.minor = element_line(colour="grey60",size=.25,linetype="dotted"),
       text=element_text(size=15), legend.position="none")
```

(p.212-213)

- **关键参数**：`geom_rect(aes(xmin,xmax,ymin,ymax,fill=))`（xmin/xmax 承载列宽占比，ymin/ymax 承载行内累积百分比）、`ddply(..., transform, ymax=cumsum(percentage))`（分组累积求边界）、`scale_x_continuous(limits=)`（留右侧标签空间）(p.212-213)
- **出处**：(p.211-213)；构成元素（非均匀马赛克图）：①非均匀分类坐标轴；②面积、颜色均有含义的矩形块；③图例 (p.211)；历史：1844 年 Minard 的 “Tableau Graphique”，宽度对应路程、高度对应旅客或货物种类比例，是当代马赛克图先驱 (p.213)

### 5.7 华夫饼图（waffle chart / dot matrix chart）

- **用途**：用由小方格（或点）组成的矩阵表示总数据的组类别情况，快速检视不同类别的分布和比例，并**与其他数据集的分布和比例进行比较** (p.214)
- **适用数据**：一维分类 + 频数/占比；块状分**堆积型**（展示类别数值）与**百分比堆积型**（展示类别占比）(p.214)
- **何时别用 / 坑**：点状华夫饼图「当只有一个变量/类别时（所有点都是相同颜色），相当于比例面积图」(p.214)——单类别时退化为比例面积图，不再表达构成
- **实现路径**：`waffle` 包的 `geom_waffle()`（百分比堆积型块状，教程 https://github.com/hrbrmstr/waffle）；`ggplot2::geom_tile()`（块状）；`ggplot2::geom_point()`（点状）；`RColorBrewer::brewer.pal()`；`reshape2`；点状堆积柱形图用 `ggplot2::facet_wrap()` 按列分面 (p.215)
- **最小可运行代码**（图 7-3-1(b) 块状百分比堆积型；注释行切换为点状）：

```r
library(ggplot2)
library(RColorBrewer)
library(reshape2)
nrows <- 10
categ_table <- round(table(mpg$class ) * ((nrows*nrows)/(length(mpg$class))))
sort_table <- sort(categ_table, index.return=TRUE, decreasing = FALSE)
df <- expand.grid(y = 1:nrows, x = 1:nrows)
df$category <- factor(rep(names(sort_table),sort_table), levels=names(sort_table))
Colormap <- brewer.pal(length(sort_table), "Set2")
ggplot(df, aes(x = y, y = x, fill = category)) +
  geom_tile(color = "white", size = 0.25) +  #图 7-3-1(b)块状百分比堆积型华夫饼图
  #geom_point(color = "black",shape=21,size=6) + #图 7-3-2(b) 点状百分比堆积型华夫饼图
  coord_fixed(ratio = 1)+
  scale_x_continuous(trans = 'reverse') +
  scale_y_continuous(trans = 'reverse') +
  scale_fill_manual(name = "Category", values = Colormap)+
  theme(panel.background  = element_blank(),
        plot.title = element_text(size = rel(1.2)), legend.position = "right")
```

(p.215)

- **关键参数**：`nrows`（网格边长，总格数 = nrows²）、`categ_table`（`round(table(class)*(nrows²/N))` 把频数折算成格子数）、`coord_fixed(ratio=1)`（保证正方格）、`scale_x/y_continuous(trans='reverse')`（翻转方向）、`geom_tile(color,size)` 与 `geom_point(shape,size)` 切换块状/点状 (p.215)
- **出处**：(p.214-215)；拓展：用 `facet_wrap()` 按列分面可得点状堆积柱形图 / 点状百分比堆积柱形图（图 7-3-3）(p.215)

### 5.8 六种图表取舍对照

| 图表 | 适用类别数 / 场景 | 书中判断 |
|---|---|---|
| 饼图 | ≤9 个分类、单系列占比 | 分类多→切片不可辨；数据量大→太占画布；多饼图难比较；连续多变量占比→百分比堆积面积图 (p.206) |
| 圆环图 | 需**跨图比较**多个整体、需在中心放标题/文本 | 中间挖空让人「更关注长度而不是面积」，比饼图更易多图对比；空间利用率高，空心区可显示文本 (p.208) |
| 复合饼图系列 | 每个位置还要展示一组内部占比 | 散点复合饼图 3 变量 (x, y, P)；气泡复合饼图 4 变量 (x, y, z, P) (p.208) |
| 马赛克图 | **两个**分类变量（列表数据、非关系型） | 「比较适合提供数据概览」；分段多时难阅读、分段不共基线难精确比较 (p.211)；非均匀马赛克图维度多、难直观理解，「多数情况下可以被拆解成多个不同的图表」(p.211) |
| 华夫饼图 | 类别占比/分布，需与其他数据集比例**对比** | 块状（waffle chart）与点状（dot matrix chart）两类；单变量时点状华夫饼图≈比例面积图 (p.214) |
| 矩形树状图 | **树形/层次**数据（关系型） | 「矩形树状图用于展示树形数据，是关系型数据。马赛克图用于分析列表数据，是非关系型数据」(p.213)；能结合颜色展示紧致的类别空间 (p.213) |

- 唯一明确的二选一规则：**有层次/树形结构 → 矩形树状图；按行或列比较多类别 → 马赛克图** (p.213)
- 华夫饼图「适合用来快速检视数据集中不同类别的分布和比例，并与其他数据集的分布和比例进行比较」(p.214) —— 跨数据集对比正是饼图弱项 (p.206)
- 矩形树状图绘制实现在第 9 章 9.5 节（treemapify / treemap 包），不在第 7 章抽取范围。

---

## 第 6 部分：高维数据可视化（第 8 章，pp.216–241）

### 6.0 前提定义与方法分类

**前提定义**：「高维是指数据具有多个独立属性；多变量是指数据具有多个相关属性」(p.217)；「往往不能使用空间数据的可视化方法处理高维数据」(p.217)。

**四类方法划分与适用范围（表 8-0-1，原文还原）**

| 编码对象 / 方法 | 基于点 | 基于线 | 基于区域 | 基于样本 |
|---|---|---|---|---|
| 单属性值 | 无 | 轴坐标 | 带颜色的点 | 基本可视化元素 |
| 全属性值 | 无 | 轴坐标的链接 | 填充颜色块 | 可视化元素组合 |
| 多属性关系 | 无 | 轴坐标的对比 | 以属性为索引的填充颜色块对比 | 无 |
| 多数据点关系 | 散点布局 | 折线段的相似性 | 以数据序号为索引填充颜色块对比 | 样本的排列对比 |
| **适应范围** | 分析数据点的关系 | 分析各数据属性的关系 | **大规模数据集**的全属性同步比较 | **少量数据点**的全属性同步比较 |

(p.218)。四类定义：①基于点——以点为基础展现单个数据点与其他数据点的关系（相似性、距离、聚类）(p.217)；②基于线——采用轴坐标编码各维度属性值，体现属性间关联 (p.217)；③基于区域——将全部数据点的全部属性以区域填充方式布局于二维平面 (p.217)；④基于样本——采用图标或基本统计图表编码单个高维数据点并排列对比 (p.217)

### 6.1 按维度数量选择（原文实际给出的维数判断，逐条带页码）

> 书中**未出现**「2-3 维 / 4-10 维 / >10 维」的显式分段表。以下是原文中全部与维数相关的判断性表述。

- **1~3 个变量**：「可以采用散点图、气泡图、曲面图等」(p.81，第 1 章)
- **多于 3 个变量**：「可以采用高维数据可视化方法，如平行坐标系、矩阵散点图、径向坐标图、星形图和切尔若夫脸谱图等」(p.81，第 1 章)
- **三维/四维**：「当我们用三维图表表示三维或者四维数据的时候，其实就已经有点不容易清晰地观察数据规律与展示数据信息了」→ **引入分面图** (p.221)
- **四到五维**：分面图「可以适用于四到五维的数据结构类型」(p.222)
  - 三维 → 列分面**散点图**（tau、SOD + Class 分面），可加 `stat_smooth(method="loess")` (p.223)
  - 四维 → 列分面**气泡图**（tau、SOD、age 大小 + Class 分面）(p.224)
  - 五维 → 矩阵分面**气泡图**（tau、SOD、age + 行分面 Gender + 列分面 Class），「其中三维为连续数据，二维为离散数据」(p.224-225)
- **极高维（书中实例 93 维）**：PCA 与 t-SNE 均给出「93 维数据的 train 数据集」的降维结果图 (p.219, p.220)
- **维数不多**：图标法「适用于维数不多但是某些维含有特别的含义并且在二维平面上具有良好展开属性的数据集」(p.233)
- 各方法的维数上限警告：矩阵散点图「当维数增加时，矩阵会受到屏幕大小的限制，而且它只能够发现两个维度数据之间的关系，很难发现多个维度数据之间的关系」(p.225-226)；平行坐标系「表达维数决定于屏幕的水平宽度，当维数增加时，引起垂直轴靠近，辨认数据的结构和关系稍显困难」(p.231)；基于柱形的图标法「并不适应于展示维数太高的数据」(p.236)；RadViz「可显示的维度大」但「海量信息对象投影点的交叠问题严重」(p.232)

### 6.2 降维方法的选择（8.1 节）

- 线性：PCA（主成分分析）、MDS（多维尺度分析）、NMF（非矩阵分解）(p.218)；非线性：ISOMAP（等距特征映射）、LLE（局部线性嵌套）(p.218)，t-SNE 也属非线性 (p.220)
- PCA 与 t-SNE 的分工：PCA 是**线性**算法，「它不能解释特征之间的复杂多项式关系」；t-SNE「基于在邻域图上随机游走的概率分布来找到数据内的结构」(p.220)
- 图标可辨识度排序：「柱形图直接将变量映射到长度，最容易比较变量之间的大小关系；星形图……可辨识程度次之；饼图是最难判定变量的关系，仅仅将变量映射到角度」(p.233)

### 6.3 主成分分析法（Principal Components Analysis, PCA）

- **用途**：线性变换到新坐标系，使投影到第一主成分的方差最大、第二主成分方差第二大，从而减少维数并保留方差贡献最大的特征（保留低阶主成分、忽略高阶主成分）(p.218)
- **适用数据**：数值型多维矩阵（示例：4 维 iris、93 维 train）(p.219)
- **何时别用 / 坑**：PCA 是**线性**算法，「不能解释特征之间的复杂多项式关系」→ 复杂非线性结构用 t-SNE (p.220)
- **实现路径**：`FactoMineR::PCA()` 降维 + `factoextra::fviz_pca_ind()` 以散点展示个体；`ggplot2` (p.219)
- **最小可运行代码**（图 8-1-2(a)）：

```r
library(ggplot2)
library(factoextra)
library(FactoMineR)
df <- iris[c(1, 2, 3, 4)]
iris.pca <- PCA(df, graph = FALSE)
fviz_pca_ind(iris.pca,
             geom.ind = "point",
             pointsize = 3, pointshape = 21, fill.ind = iris$Species, # color by groups
             palette = c("#00AFBB", "#E7B800", "#FC4E07"),
             addEllipses = TRUE, # Concentration ellipses
             legend.title = "Groups", title="")+theme_grey()
```

(p.219-220)

- **关键参数**：`PCA(df, graph=FALSE)`（关闭自带图形）、`geom.ind="point"`（只画点）、`pointsize`/`pointshape`/`fill.ind`（点大小/形状/按组填充）、`palette`、`addEllipses=TRUE`（添加聚集椭圆）(p.219-220)
- **出处**：(p.218-220)

### 6.4 t-SNE 算法（t-distributed Stochastic Neighbor Embedding）

- **用途**：非线性降维，「非常适用于将高维数据降维到二维或者三维，再使用散点图等基本图表进行可视化」；基于邻域图上随机游走的概率分布找数据结构 (p.220)
- **适用数据**：数值型高维矩阵（示例：4 维 iris、93 维 train）(p.220)
- **何时别用 / 坑**：①「t-SNE 倾向于保存局部特征，对于本征维数（intrinsic dimensionality）本身就很高的数据集，是不可能完整地映射到二到三维空间的」(p.220-221)；②「t-SNE 没有唯一最优解，且没有预估部分。如果想要做预估，则可以考虑在降维之后构建一个回归方程之类的模型。但是要注意，在 t-SNE 中，距离本身是没有意义的，都是概率分布问题」(p.221)
- **实现路径**：`Rtsne::Rtsne()` 降维（取结果 `$Y`）+ `ggplot2::geom_point()` (p.221)
- **最小可运行代码**：

```r
library(Rtsne)
library(ggplot2)
iris_unique <- unique(iris)   # 去除重复数据
set.seed(42)
tsne_out <- Rtsne(as.matrix(iris_unique[,1:4]))
mydata <- data.frame(tsne_out$Y, iris_unique$Species)
colnames(mydata) <- c("t_DistributedY1","t_DistributedY2","Group")
ggplot(data=mydata, aes(t_DistributedY1, t_DistributedY2, fill=Group))+
  geom_point(size=4, colour="black", alpha=0.7, shape=21)+
  scale_fill_manual(values=c("#00AFBB", "#FC4E07","#E7B800","#2E9FDF"))
```

(p.221)

- **关键参数**：`Rtsne(mat)` 输入必须为 `as.matrix()` 数值矩阵；结果坐标取 `tsne_out$Y`；`set.seed()` 保证可复现（无唯一最优解）(p.221)
- **出处**：(p.220-221)；Laurens van der Maaten 与 Geoffrey Hinton 2008 年提出 (p.220)；SNE 两步：①高维对象间构建概率分布（相似对象概率高）②低维空间构建分布并使之尽量相似 (p.220)

### 6.5 分面图（facet_wrap / facet_grid）

- **用途**：「根据类别属性绘制一系列子图，类似于邮票图（small multiples）」，用散点图、气泡图、柱形图或曲线图等基础图表按行/列展示，揭示数据关系 (p.222)
- **适用数据**：四到五维数据结构；三维/四维用三维图表已难观察时改用分面 (p.221-222)
- **何时别用 / 坑**：三维散点图把系列画在不同平面时「由于数据的遮挡，这样并不能很好地展示数据」(p.223)；三维气泡图展示四维时「已经很难观察数据的变化关系」(p.221)
- **实现路径**：`ggplot2::facet_wrap()`（列分面/矩形排布）、`ggplot2::facet_grid()`（行×列矩阵分面）；配色 `wesanderson::wes_palette(name="Darjeeling")` (p.224-225)
- **函数签名（原文照录）**：

```r
facet_grid(rows = NULL, cols = NULL, scales = "fixed", labeller = "label_value", facets)
facet_wrap(facets, nrow = NULL, labeller = "label_value", strip_position = "top")
```

(p.222)

- **最小可运行代码**（列分面气泡图，图 8-2-3(a)，四维）：

```r
library(ggplot2)
Alz <- read.csv("Alzheimers.csv", header = T)
ggplot(Alz, aes(x = tau, y = SOD, fill= Class, size = age)) +
#其气泡的颜色填充由 Class 映射，大小由 age 映射
  geom_point(shape=21, colour="black", alpha=0.7) +
#设置气泡类型为空心的圆圈，边框颜色为黑色，填充颜色透明度为 0.7
  facet_wrap( ~ Class)  # 类别 Class 为列变量
```

(p.225)；矩阵分面气泡图（图 8-2-4，五维）：

```r
library(ggplot2)
Alz <- read.csv("Alzheimers.csv", header = T)
ggplot(Alz, aes(x = tau, y = SOD, fill= Class, size = age)) +
  geom_point(shape=21, colour="black", alpha=0.7) +
  facet_grid(Gender ~ Class) # 性别 Gender 为行变量、类别 Class 为列变量
```

(p.225)

- **关键参数**：`rows`/`cols`（行/列分面变量，`vars(drv)` 形式，可多个分类变量）；`scales`：`"free"`（X、Y 轴都调整）/`"free_x"`/`"free_y"`/`"fixed"`（统一取值范围）；`facets`（网格分面中尽量不用，改用 rows/cols）；`labeller`、`strip_position="top"` (p.222)
- **分面系统速查（表 8-2-1）**：`t + facet_grid(.~ fl)` 按列排布；`t + facet_grid(year ~ .)` 按行排布；`t + facet_grid(year ~ fl)` 行列矩阵排布；`t + facet_wrap(~ fl)` 按矩形排布；`t + facet_grid(drv ~ fl, scales="free")` 调整 X、Y 轴取值范围（其中 `t <- ggplot(mpg, aes(cty, hwy, fill=fl)) + geom_point(size=3, stroke=0.3, alpha=0.8)`）(p.222-223)
- **出处**：(p.221-225)

### 6.6 矩阵散点图（scatter plot matrix）

- **用途**：「将高维度数据的每两个变量组成一个散点图，再将它们按照一定的顺序组成矩阵散点图」，展示所有变量两两之间的关系 (p.225)
- **适用数据**：多列数值型变量 + 可选分组变量（示例：iris 4 特征 + Species）(p.225)
- **何时别用 / 坑**：优点「能够直观解释所有的任意二维数据之间的关系，而不受数据集大小和维数多少的影响」(p.225)；缺点「当维数增加时，矩阵会受到屏幕大小的限制，而且它只能够发现两个维度数据之间的关系，很难发现多个维度数据之间的关系」(p.225-226)
- **实现路径**：`GGally::ggpairs()`（**书中推荐**，「很大的优势是可以通过语句控制上下和对角线部分展示的图表类型」）；备选 `graphics::pairs()`；辅助 `wesanderson::wes_palette()` (p.227)
- **最小可运行代码**（图 8-3-1(b)）：

```r
library(GGally)
library(ggplot2)
library(wesanderson)
ggpairs_theme <- theme_bw()+theme(panel.grid.major = element_blank(),#删除主要网格线
                panel.grid.minor = element_blank(),  #删除次要网格线
                panel.border = element_rect(colour="black", fill=NA, size=0.25),
                axis.title=element_text(size=8,face="plain",color="grey30"),
                axis.text = element_text(size=8,face="plain",color="grey30"),
                strip.background = element_blank())
#修改 GGally 包的默认颜色主题方案为 wesanderson 包的 Darjeeling
ggplot <- function(...) ggplot2::ggplot(...) +
  scale_fill_manual(values=wes_palette(n=3, name="Darjeeling"))+
  scale_color_manual(values=wes_palette(n=3, name="Darjeeling"))
unlockBinding("ggplot",parent.env(asNamespace("GGally")))
assign("ggplot",ggplot,parent.env(asNamespace("GGally")))
ggpairs(iris, columns = 1:4, mapping = ggplot2::aes(fill=Species, colour=Species),
  lower=list(continuous = wrap("points",size=1,shape=21)), #下半部分绘制矩阵散点图
  diag = list(continuous = wrap("densityDiag",alpha=0.5,colour="black",size=0.25)),
  upper= list(continuous = wrap("cor",size = 3, alignPercent = 0.9)))) #上半部分显示相关系数
ggpairs_theme
```

(p.227)

- **关键参数**：`columns`（参与矩阵的变量列）、`mapping`（分组映射）、`lower`/`diag`/`upper`（下三角/对角线/上三角图表类型，形如 `list(continuous=wrap(...))`）；`wrap("points", size, shape)` 散点、`wrap("densityDiag", alpha, colour, size)` 核密度曲线、`wrap("cor", size, alignPercent)` 相关系数数值 (p.227)
- **出处**：(p.225-227)；图 8-3-1(a) 单系列版：下三角带线性拟合散点图、对角线统计直方图、上三角相关系数 (p.225)

### 6.7 热力图（heat map）

- **用途**：「将规则化矩阵数据转换成颜色色调」，每个单元对应数据的某些属性，属性值经颜色映射填充规则单元；常与层次聚类结合展示数据内在规律 (p.227)
- **适用数据**：规则化数值矩阵（示例 `scale(mtcars)`）；「表格坐标的排列和顺序都是可以通过参数控制的，合适的坐标排列和顺序可以很好地帮助读者发现数据的不同性质」(p.227)
- **何时别用 / 坑**：需先用 `scale()` 标准化「以消除量纲对数据结构的影响」再做聚类与配色 (p.228)；多图共享图例时两图必须共用同一组 `Colormap` 与 `breaks` (p.229)
- **实现路径**：`pheatmap::pheatmap()`（**书中采用**）；备选 `gplots::heatmap.2()`、`Complexheatmap` 包的 `heatmap()`（教程 https://jokergoo.github.io/ComplexHeatmap-reference/book/）；多图排布与共享图例 `cowplot::plot_grid()`（手册 https://cran.r-project.org/web/packages/cowplot/index.html）；配色 `RColorBrewer` + `colorRampPalette()` (p.228-229)
- **最小可运行代码**（图 8-4-1；原文顺序为 colormap→breaks→`df<-scale(mtcars)`，此处按可运行顺序整理）：

```r
library(RColorBrewer)
library(pheatmap)
colormap <- colorRampPalette(rev(brewer.pal(n = 7, name = "RdYlBu")))(100)
df <- scale(mtcars) #使用 scale 方法来对数据进行标准化，以消除量纲对数据结构的影响
breaks = seq(min(unlist(c(df))), max(unlist(c(df))), length.out=100)
pheatmap(df, color=colormap, breaks=breaks, border_color="black",
         cutree_col = 2, #设定列聚类成 2 类
         cutree_row = 4) #设定行聚类成 4 类
```

(p.228)；共享图例的多个热力图（图 8-4-2）：

```r
library(RColorBrewer)
library(pheatmap)
library(cowplot)
set.seed(1020543)
df1 <- data.frame(matrix(rnorm(100,10,3), ncol=10))
colnames(df1) <- LETTERS[1:10]; rownames(df1) <- letters[1:10]
df2 <- data.frame(matrix(rnorm(100,15,5), ncol=10))
colnames(df2) <- LETTERS[1:10]; rownames(df2) <- letters[1:10]
Colormap <- colorRampPalette(rev(brewer.pal(n = 7, name = "RdYlBu")))(100)
breaks <- seq(min(unlist(c(df1, df2))), max(unlist(c(df1, df2))), length.out=100)
p1 <- pheatmap(df1, color=Colormap, breaks=breaks, border_color="black", legend=TRUE)
p2 <- pheatmap(df2, color=Colormap, breaks=breaks, border_color="black", legend=TRUE)
plot_grid(p1$gtable, p2$gtable, align = 'vh', labels = c("A", "B"), ncol = 2)
```

(p.229)

- **关键参数**：`color`（颜色向量）、`breaks`（数值分段，与 color 等长）、`border_color`、`cutree_col`/`cutree_row`（按聚类树切分块数）、`legend`；组合时取 `pheatmap()` 返回对象的 `$gtable` 传给 `plot_grid(align, labels, ncol)` (p.228-229)
- **出处**：(p.227-229)

### 6.8 平行坐标系图（parallel coordinates chart）

- **用途**：「将多维数据属性空间通过多条等距离的平行轴映射到二维平面上」，每条轴代表一个属性维度（取值范围从该属性最小值到最大值均匀分布），每个数据项用一条跨越平行轴的折线段表示，「相似的对象具有相似的折线走向趋势」(p.230)
- **适用数据**：多列**连续**数值变量 + 一个分组变量（示例：`reading > 523` 切分为 Class1/Class2）(p.231)
- **何时别用 / 坑**：优点「表达数据关系非常直观，易于理解」、「具有良好的数学基础，其射影几何解释和对偶特性使它很适合用于可视化数据分析」(p.230-231)；缺点「表达维数决定于屏幕的水平宽度，当维数增加时，引起垂直轴靠近，辨认数据的结构和关系稍显困难」、「对大数据集进行可视化时，由于折线密度增加产生大量交叠线，难以辨识」、「坐标之间的依赖关系很强，平行轴的安排序列性也是影响发现数据之间关系的重要因素」(p.231)；大数据集折线重叠造成视觉混淆 → 「一般会设置折线的透明度（alpha of line）」(p.230)；风格上「推荐使用简洁的背景风格，只保留主要的图表元素，比如坐标轴及坐标轴标题」(p.231)
- **实现路径**：`GGally::ggparcoord()`；**类别型数据**的平行坐标系用 `ggforce::geom_parallel_sets()`——「每条平行的横轴代表不同的分类变量，每条横轴的组成线段代表该分类变量的不同分类结果」（教程 https://www.data-imaginist.com/2019/the-ggforce-awakens-again/）(p.231)
- **最小可运行代码**（图 8-5-3(b) 多数据系列）：

```r
library(GGally)
dlarge <- read.csv("Parallel_Coordinates_Data.csv", header=TRUE)
dlarge <- transform(dlarge, Class=ifelse(reading> 523, "Class1", "Class2"))
ggparcoord(data = dlarge, columns = 1:6, mapping=aes(color=Class), groupColumn=7,
           showPoints = FALSE, boxplot = FALSE, alphaLines = 0.7)+
  scale_x_discrete(position = "top")+
  scale_colour_manual(values=c("#90C539","#45BFFC" ))+
  theme_minimal()
```

(p.231)

- **关键参数**：`columns`（作为平行轴的变量列）、`groupColumn`（分组列号）、`mapping=aes(color=)`、`showPoints`、`boxplot=TRUE`（「则会绘制每个属性维度下的箱形图」）、`alphaLines`（折线透明度，解决重叠）(p.231)
- **出处**：(p.230-231)；Alfred Inselberg 1985 年提出，1990 年 E.J.Wegman 用于探索性分析与可视化设计 (p.230)

### 6.9 RadViz 图（radial coordinate visualization）

- **用途**：「将一系列多维空间的点通过非线性方法映射到二维空间」，基于**弹簧张力最小化算法**：n 维 = n 个弹簧均匀分布在圆周上，第 i 维归一化值 ki 作为第 i 个弹簧的弹性系数，合力为零的点即投影点 (p.232)
- **适用数据**：需先归一化到 [0,1] 的多维数值数据；支持单数据系列（高密度）与多数据系列（气泡）(p.232)
- **何时别用 / 坑**：优点「计算复杂度低，表达数据关系非常简单、直观、易于理解，而且可显示的维度大，相似多维对象的投影点十分接近，容易发现聚类信息」(p.232)；缺点「海量信息对象投影点的交叠问题严重，如 (0,0,…,0) 与 (a,a,…,a) 的投影点一样」(p.232)——归一化后方向相同但量级不同的样本会重合；「还需要前期进行较多的数据处理」(p.233)
- **实现路径**：`Radviz` 包的 `bubbleRadviz()`、`make.S()`、`do.L()`、`do.radviz()`、`cosine()`、`do.optim()`、`get.optim()`（另提供等高线图函数 `contour()`）；配色 `wesanderson::wes_palette()` (p.233)
- **最小可运行代码**（图 8-6-1(b)）：

```r
library(Radviz)
library(wesanderson) #提供颜色主题方案 Darjeeling
data(iris)  #使用鸢尾花（Anderson’s Iris data set）数据
das <- c('Sepal.Length','Sepal.Width','Petal.Length','Petal.Width')
S <- make.S(das)
scaled <- apply(iris[,das], 2, do.L)          # 归一化
rv <- do.radviz(scaled, S)
sim.mat <- cosine(scaled)
new <- do.optim(S, sim.mat, iter=10, n=100)   # 优化维度在圆周上的排布
new.S <- make.S(get.optim(new))
new.rv <- do.radviz(scaled, new.S)
pop.cols <- setNames(c(wes_palette(n=3, name="Darjeeling"))), levels(iris$Species))
bubbleRadviz(new.rv,
                bubble.color=c(wes_palette(n=3, name="Darjeeling")))[as.integer(iris$Species)],
                bubble.fg='black', scale=0.05, decreasing=TRUE)
```

(p.233)

- **关键参数**：`make.S(das)`（把变量名映射到圆周坐标）、`do.L`（按列归一化，配合 `apply(..., 2, do.L)`）、`do.radviz(scaled, S)`（计算投影）、`cosine()`（相似度矩阵）、`do.optim(S, sim.mat, iter, n)` + `get.optim()`（优化维度顺序）、`bubbleRadviz(..., bubble.color, bubble.fg, scale, decreasing)` (p.233)
- **出处**：(p.232-233)

### 6.10 图标法（glyph）—— 总述

- **用途**：「使用具有多个可视特征的图标来表达多维信息，图标的每一个可视特征都可用来表示多维信息的一维」(p.233)
- **适用数据**：「适用于维数不多但是某些维含有特别的含义并且在二维平面上具有良好展开属性的数据集」(p.233)
- **何时别用 / 坑**：「由于一个视觉空间只能排放一定数目的图标，从而限制了图标可视化的分辨率；图标法在数据的确定性方面也有一定的限制，需要用户花费一定的精力解读数据」(p.233)
- **三种图标可辨识度排序（明确判断）**：柱形图（映射**长度**）最容易比较大小 > 星形图（映射**不同方向的长度**）次之 > 饼图（映射**角度**）最难判定变量关系 (p.233)
- **实现路径**：`graphics::stars()`（星形）、`ggplot2::facet_wrap()+geom_bar()`（柱形）、`aplpack::faces()`（脸谱）(p.233-239)
- **出处**：(p.233-234)

### 6.11 基于星形图的图标法（star glyph）

- **用途**：每个属性值映射为从中心点向四周辐射的一个坐标轴上的点，相邻点连成星状多边形；「星状的大小和形状提供了对象属性值的视觉描述」，扫一眼即可辨别两个对象的差异 (p.234)
- **适用数据**：多维数据（示例：`diamonds` 抽样 100 行取第 2-6 列）；通常所有属性值映射至 [0,1] 区间 (p.234)；散点星形图额外需两列作 X/Y（书中 `log10(carat)`、`log10(price)`）(p.234)
- **何时别用 / 坑**：每个对象使用单独坐标系，「每个对象映射成一个多边形」(p.234)
- **实现路径**：`graphics::stars()`（可绘制星形图与散点星形图）；辅助 `RColorBrewer::brewer.pal()`、`dplyr::sample_n()`、`ggplot2` (p.234-236)
- **最小可运行代码**（图 8-7-3 星形图 / 图 8-7-4 散点星形图）：

```r
library(graphics)
library(RColorBrewer)
library(dplyr)
library(ggplot2)
data(diamonds)
dstar <- sample_n(diamonds, 100)
dstar$log10carat <- log10(dstar$carat)
dstar$log10price <- log10(dstar$price)
dstar <- dstar[order(dstar$cut, decreasing=T),]
#星形图
stars(dstar[,2:6], key.loc = c(-2, 10), scale = TRUE,
      locations = NULL, len =1, radius = TRUE,
      full = TRUE, labels = NULL, draw.segments = TRUE,
      col.segments=palette(brewer.pal(7,"Set1")))[1:5])
#散点星形图
loc <- data.matrix(dstar[,11:12])
stars(dstar[,2:6], key.loc = c(-1, 3), scale = TRUE,
      locations = loc, len =0.07, radius = TRUE,
      full = TRUE, labels = NULL, draw.segments = TRUE,
      col.segments=palette(brewer.pal(7,"Set1")))[1:5],
      frame.plot=TRUE, axes = TRUE,
      xlab="log10(carat)", ylab="log10price", xlim=c(-0.7,0.7))
```

(p.236)

- **关键参数**：`x`（数据矩阵/数据框，每列一个属性）、`scale=TRUE`（按列归一化）、`locations=NULL`（普通星形图）/`locations=loc`（散点星形图 XY 坐标矩阵）、`len`（星形半径缩放）、`radius=TRUE`、`full=TRUE`（全圆）、`draw.segments`+`col.segments`、`key.loc`（图例位置）、`labels` (p.236)
- **出处**：(p.234-236)；星形图由 Chambers 于 1983 年首次提出 (p.234)

### 6.12 基于柱形图的图标法（bar glyph / profile glyph）

- **用途**：「直接将变量映射到长度，最容易比较变量之间的大小关系」，每个样本一组柱形 (p.236)
- **适用数据**：多维数据，需先把 factor 转 numeric、再把各列归一化到 [0,1]（示例：`diamonds` 抽样 500 取前 100 行的第 2-6 列）(p.237)
- **何时别用 / 坑**：「柱形图并不适应于展示维数太高的数据。因为柱形基于水平线排列，很难单独从柱形图中区分一个变量的趋势或者异常数据，但是通过颜色区别变量类别，可以在一定程度上解决这种问题」(p.236)
- **实现路径**：`ggplot2::facet_wrap()` 分面 + `geom_bar(stat="identity")`；预处理 `reshape::melt()`、`dplyr::sample_n()`；配色 `RColorBrewer::brewer.pal(7,"Set1")` (p.237-238)
- **最小可运行代码** — 数据预处理：

```r
library(ggplot2)
library(RColorBrewer) #提供颜色主题方案 brewer.pal(7,"Set1")
library(dplyr)        #提供随机抽样函数 sample_n ()
library(reshape)      #提供数据融合函数 melt()
data(diamonds)
dsmall <- sample_n(diamonds, 500)
mydata <- data.frame(dsmall[1:100,2:6])
for (i in 1:ncol(mydata))
{
  #将 factor 类型的变量数据转换成 numeric 数值型的数据
  if(sum(as.integer(class(mydata[,i])=="factor"))))
  { levels(mydata[,i]) <- seq(0,length(levels(mydata[,i]))))-1,1)
    mydata[,i] <- as.numeric(mydata[,i])
  }
  #将数据归一化处理至[0, 1]区间中
  temp <- mydata[,i]; Dmin <- min(temp); Dmax <- max(temp)
  mydata[,i] <- (temp-Dmin)/(Dmax-Dmin)
}
mydata <- mydata[order(mydata$cut, decreasing=T),] #按照第 4 列 cut 变量降序排序
mydata$category <- as.integer(seq(1,nrow(mydata),1))
Meltdata <- melt(mydata, id.vars="category")
```

(p.237-238)；绘图：

```r
ggplot(Meltdata, aes(variable, value, fill=variable)) +
  geom_bar(stat="identity", colour="black", size=0.25, width=1.0)+
  scale_fill_manual(values=brewer.pal(7,"Set1")[1:5])+
  facet_wrap(~category)
```

(p.238)

- **关键参数**：`facet_wrap(~category)`（每个样本一个分面 = 一个 glyph）、`geom_bar(stat="identity", width=1.0)`、`scale_fill_manual`（用颜色区分变量类别以缓解高维难辨）(p.238)
- **出处**：(p.236-238)

### 6.13 切尔诺夫脸谱图（chernoff face）

- **用途**：「使用人脸特征编码不同变量的值，人的每个部位都代表不同属性」，如脸的形状、高度和宽度、眼的高度和宽度等；利用人类擅长人脸识别的能力观察细微变化 (p.238)
- **适用数据**：多维数值数据（示例：美国各州犯罪类型数据，7 个变量 + 州名标签）(p.238-239)
- **何时别用 / 坑**：「在绘制图表前，要先根据其中一项重要的指标对数据集进行排序后再展示」（书中按 `murder` 降序）(p.239)；「人对脸部的各个部位特征的感知度不同，根据属性的优先级选择人脸的映射部位」(p.238)
- **实现路径**：`aplpack::faces()`；配色 `RColorBrewer::brewer.pal()` + `colorRampPalette()` (p.239)
- **最小可运行代码**（图 8-7-7）：

```r
library(aplpack)
library(RColorBrewer)
crime <- read.csv("Faces_Data.csv")
crime_filled <- cbind(crime[,1:6], rep(0, length(crime$state)), crime[,7:8])
crime_filled <- crime_filled[order(crime_filled$murder, decreasing=T),]
faces(crime_filled[,2:8],
      col.face = colorRampPalette(brewer.pal(9, "Reds")))(20),
      col.hair= colorRampPalette(brewer.pal(9, "Blues")))(20),
      labels= crime_filled$state, cex=1)
```

(p.239)

- **关键参数**：第一个参数为变量矩阵（书中取 2:8 列）、`col.face`（脸部颜色渐变，映射某一变量）、`col.hair`（头发颜色渐变，映射另一变量）、`labels`（每个脸的名称）、`cex`（大小）(p.239)
- **出处**：(p.238-239)；拓展：也可用「花（flower）」展示多维数据，每片花瓣大小代表一维，图 8-7-8(a) 六维（X/Y 各一维 + 4 个花瓣）、(b) 七维 (p.240)

### 6.14 表格图（table plot）

- **用途**：「用于探索和分析大数据集的可视化方法，可以用于探索变量之间的关系、发现数据的内在模式、检查缺失数据的产生与选择」(p.241)
- **适用数据**：「主要用于可视化多变量的数据集和大量的数据记录，至少有 1000 个数据」(p.241)；整个数据集按某变量排序（书中 `sortCol=price`），每列一个变量，每行一个 row bin 箱体 (p.241)
- **何时别用 / 坑**：**记录数少于 1000 时不适用**（「至少有 1000 个数据」）(p.241)；「由于数据信息较多，为保证数据图表的美观，推荐使用单色渐变系列作为各个子图的颜色主题，如绿色"Greens"、紫色"Purples"、橙色"Oranges"」(p.241)
- **实现路径**：`tabplot::tableplot()`；配色 `RColorBrewer::brewer.pal()` + `palette()` (p.241)
- **最小可运行代码**（图 8-8-1）：

```r
library(tabplot)
library(ggplot2)
library(RColorBrewer)
data(diamonds)
tableplot(diamonds, sortCol =price,
        select = c(price,carat,cut, color, clarity,depth, table),
        pals = list(cut=palette(brewer.pal(9,"Purples")))[c(2,3,4,5,7,8)],
                 color=palette(brewer.pal(9,"Oranges")))[c(2:9)],
                 clarity=palette(brewer.pal(9,"Greens")))[1:8]))
```

(p.241)

- **关键参数**：`sortCol`（排序变量，决定行箱体顺序）、`select`（展示哪些列及顺序）、`pals`（`list(变量=颜色向量)`，按变量指定调色板）(p.241)
- **出处**：(p.241)

---

## 第 7 部分：层次关系型图表（第 9 章，pp.242–259）

### 7.0 层次图表的选择规则（含原书否定性判断）

层次关系 = 「包含」与「从属」两类，如公司部门组织、洲-国家包含关系 (p.243)。书中分**两大类**：

**(1) 节点链接（node-link）图** (p.243)：成员为正交/径向布局的节点链接图、树形图（图 9-0-1 a-d）

- 定性：「这种方法直观、清晰，适合表示承接的层次关系型数据。」
- **否定判断**：「但是当个体数目太多时，尤其是**广度和深度相差较大**时，该方法由于数据量太多而导致不能清晰、完整地在有限的屏幕空间中展示数据，从而可读性较差。」(p.243)

**(2) 空间填充（space-filling）图** (p.243)：成员为冰柱图、旭日图、圆填充图、矩形树状图（图 9-0-1 e-h）

- 定性：「**和节点链接图相比，这种方法更适合表示包含和从属的关系**，而且具有**高效的空间利用率，可以表示更多的数据量**。」
- **否定判断**：「其缺点在于**数据层次关系的表现清晰度不如节点链接图**。」(p.243)

**空间填充类内部的对比**

| 对比项 | 原书判断 | 页码 |
|---|---|---|
| 圆堆积图 vs 矩形树状图 | 「圆堆积图虽然看起来漂亮，但**不及矩形树状图般节省空间**（因为圆圈内会有很多空白处），可是它**实际上比矩形树状图更能有效显示层次结构**。」Shneiderman 起初对演变的圆堆积图「是不认同的」 | p.255, p.259 |
| 矩形树状图 vs 传统树形结构图 | 「矩形树状图能更有效地利用空间，并且拥有展示占比的功能。」 | p.257 |
| 矩形树状图缺点 | 「当分类占比太小的时候，文本会变得很难排布。」「相比分叉树形图，矩形树状图的**树形数据结构表达得不够直观、明确**。」 | p.257 |
| 旭日图 vs 圆环图 | 「单层的旭日图其实类似于圆环图，但是多层的旭日图展示了外层环状数据与内层环状数据的关系信息。」 | p.252 |
| Voronoi 树图 | 「可以克服矩形空间长宽比的困扰，采用任意多边形来替代矩形空间」 | p.259 |
| 径向布局 vs 正交布局 | 径向「它的节点数据量随着层次而增加，可以容纳更多的节点，更加合理地提高了空间的利用率」 | p.244 |

**层级数与数据规模的显式线索**（书中只有实例值，无通则是/否阈值）：

- 节点链接图 ggraph `dendrogram` 示例为「有 **3 层**层次关系」(p.247)；旭日图实例 `Season→Month→Week` 也是 **3 层**，代码用 `filter=(depth<=3 & depth>0)` 截断绘制深度 (p.254)。
- 圆堆积图实例用 ggraph 自带 `flare`（大型软件类依赖图），靠 `filter=leaf` 只给叶节点打标签来扛大节点量 (p.256)。
- 矩形树状图实例 `index=c("parent","id")` 为 **2 层** (p.258)。

→ 可继承的推荐链：层级浅/节点少且要「直观清晰」→ 节点链接图 (p.243)；空间不够、节点随层膨胀 → 空间填充类 (p.243)；要「占比/部分-整体」→ 矩形树状图或旭日图 (p.253, p.257)；要「层次结构更好看清」→ 圆堆积图优于矩形树状图 (p.255, p.259)。

### 7.1 节点链接图（层次型，node-link）

- **用途**：展示承接式层次关系，用节点表示个体、连线表示层次关系 (p.243)；核心问题「如何在屏幕上放置节点，以及如何绘制节点与节点之间的链接关系」(p.243)
- **适用数据**：边列表 edgelist（`from`/`to` 两列数据框）+ 可选节点属性表 `vertices`（第一列为 `name`）(p.244-245)
- **何时别用 / 坑**：个体数目太多、尤其广度深度相差较大时可读性差 (p.243)；「最好先对数据根据某些特征进行排序处理，比如最外层的同组节点的总数、叶节点的特征数值等」，排序后「可以很好地展示数据，帮助读者快速了解数据表达的信息」(p.245-246)；若指定 `vertices` 则「**edges 中指定的链接序列必须都包含在 df 的第一列中**」(p.245)
- **实现路径**：`igraph::graph_from_data_frame()` → `ggraph::ggraph()` + `geom_edge_*()` / `geom_node_*()` (p.244-247)

**数据构造 + 排序**

```r
library(ggraph); library(igraph); library(tidyverse); library(RColorBrewer)
set.seed(1)
d11 <- data.frame(from="origin", to=paste("group", seq(1,10), sep=""))
d21 <- data.frame(from=sort(sample(rep(d11$to, each=100),100,replace=FALSE))),
                  to=sample(paste("subgroup", seq(1,100), sep="_"),100,replace=FALSE)))
edges <- rbind(d11[,1:2], d21[,1:2])
vertices_name <- unique(c(as.character(edges$from), as.character(edges$to))))
vertices <- data.frame(name=vertices_name, value=runif(length(vertices_name))))
rownames(vertices) <- vertices_name
d2 <- d21 %>% mutate(order2=as.numeric(factor(from,
    levels=unique(from)[sort(summary(as.factor(from)),index.return=TRUE,decreasing = T)$ix],
    order=TRUE)))) %>% arrange(order2)   # 按最外层同组节点总数降序
d2 <- d2 %>% left_join(vertices, by=c("to" = "name")) %>% arrange(order2, desc(value))
edges <- rbind(d11[,1:2], d2[,1:2])
list_unique <- unique(c(as.character(edges$from), as.character(edges$to))))
vertices <- data.frame(name=list_unique, value=vertices[list_unique,'value'])
vertices$group <- edges$from[match(vertices$name, edges$to)]
myleaves <- which(is.na(match(vertices$name, edges$from)))
```

(p.246)

**标签角度 + 径向/正交绘图**

```r
nleaves <- length(myleaves)
vertices$id <- nleaves/360*90
vertices$id[myleaves] <- seq(1:nleaves)
vertices$angle <- 90 - 360 * vertices$id / nleaves
vertices$angle <- ifelse(vertices$angle < -90, vertices$angle+180, vertices$angle)
mygraph <- graph_from_data_frame(edges, vertices = vertices, directed = TRUE)
# circular = TRUE 径向布局(图9-1-4)；FALSE 为正交布局(图9-1-3)
ggraph(mygraph, layout = 'dendrogram', circular = TRUE) +
  geom_edge_diagonal(aes(colour=..index..)) + scale_edge_colour_distiller(palette = "RdPu") +
  geom_node_text(aes(x = x*1.25, y=y*1.25, angle = angle, label=name, color=group), size=2.7, alpha=1) +
  geom_node_point(aes(x = x*1.07, y=y*1.07, fill=group, size=value), shape=21, stroke=0.2, color='black', alpha=1) +
  scale_colour_manual(values= rep(brewer.pal(9,"Paired"), 30)) +
  scale_fill_manual(values= rep(brewer.pal(9,"Paired"), 30)) +
  scale_size_continuous(range = c(0.1,7)) + expand_limits(x = c(-1.3, 1.3), y = c(-1.3, 1.3)) +
  theme_void() + theme(legend.position="none", plot.margin=unit(c(0,0,0,0),"cm"))
```

(p.247)

- **关键参数**：`graph_from_data_frame(edges, directed, vertices)`，`directed` 默认 `TRUE`、`vertices` 默认 `NULL` (p.244-245)；`layout` 定义节点放置，「可以访问 igraph 中可用的所有布局功能，而且还提供了自己的大量选择，如蜂箱图（hive plot）、矩形树状图（treemap）和圆圈堆积图（circle packing）」(p.245)；`circular` 切换径向/正交 (p.247)；`geom_node_tile()`「只在绘制树形图和冰柱图时使用」，`geom_node_point()`「更加通用」(p.245)；「若这些链接是由布局所决定的（例如矩形树状图），则不需要绘制连接线」(p.245)
- **出处**：(p.243-247)

### 7.2 第 9 章出现的 ggraph 布局

| layout | 效果 | 页码 |
|---|---|---|
| `'dendrogram'` | `circular=TRUE` 径向（根节点在圆心，节点到圆心距离对应深度，越外层同心圆越大，同层在同心圆上划分区间）；`FALSE` 为正交 | p.244, p.247 |
| `'partition'` | `circular=TRUE` → 旭日图，配 `geom_node_arc_bar()`；直角坐标 → 冰柱图，配 `geom_node_tile()` | p.254-255 |
| `'circlepack'` | 圆堆积图，配 `geom_node_circle()`，`weight=` 指定面积变量 | p.256 |
| `'hive'` | 蜂巢网络图（ggraph 额外布局之一） | p.245 |
| `'treemap'` | ggraph 额外提供（本章未给实例） | p.245 |

### 7.3 树形图（dendrogram）

- **用途**：「表示**连续合并的每对类之间的属性距离**的示意图」，为避免线交叉而图形化排布，使被合并的每对类的成员相邻 (p.248)
- **适用数据**：数值矩阵/数据框 → `dist()` 距离 → `hclust()` 层次聚类对象。算法：算每对类距离 → 迭代合并最近的一对 → 每次合并更新距离，「合并类特征时采用的距离将用于构建树形图」(p.248)
- **四型**：纵向树形图、横向树形图、环形树形图、进化树形图 (p.248)
- **何时别用 / 坑**：表达的是距离合并而非「包含/从属」归属；后者宜用空间填充类 (p.243)
- **实现路径**：`ggdendro::ggdendrogram()` / `ggraph(layout="dendrogram")` / `factoextra::fviz_dend()`；书中明确「**factoextra 包绘制的树形图更加美观**，图 9-2-2 所示的树形图都是使用 factoextra 包绘制的」(p.249)。环形树形图另可用 `circlize::circlize_dendrogram()`、`ggtree::ggtree()` (p.258)

```r
library(factoextra)
data(USArrests)
dd <- dist(scale(datasets::mtcars), method = "euclidean")  # 中心化后求欧式距离
hc <- hclust(dd, method = "ward.D2")                       # 层次聚类方法
fviz_dend(hc, k = 4,                                       # 聚类的类别数目为 4
          cex = 0.8,                                       # 数据标签的字体大小
          k_colors = c("#2E9FDF", "#00AFBB", "#E7B800", "#FC4E07"),
          color_labels_by_k = FALSE, rect = TRUE,          # 用彩色矩形框标定类别
          rect_border = c("#2E9FDF", "#00AFBB", "#E7B800", "#FC4E07"), rect_fill = TRUE)
```

- **关键参数**：`horiz=TRUE` 坐标轴转置→横向树形图 (p.250)；`type=c("rectangle","circular","phylogenic")` 分别对应纵向/横向、环形、进化树形图 (p.250)；`k` 聚类数、`rect`/`rect_fill`/`rect_border` 彩色矩形框 (p.249-250)
- **出处**：(p.248-250)

### 7.4 组合图：径向布局热力图 + 环状树形图

- 用途：「在环状树形图的基础上，还可以添加每个数据的具体数值，使用径向布局的热力图表示。这样可以更加全面地展示数据信息」(p.250)
- 实现：`circos.track()` 构造每层圆环；最外层 `circos.rect()` 画径向热力图，最内层 `circos.dendrogram()`（正文亦写作 `circlize_dendrogram()`）画环状树形图，最后 `ComplexHeatmap::Legend()` 造图例 (p.251)

```r
library(circlize); library(RColorBrewer); library(ComplexHeatmap)
col <- colorRamp2(seq(-2,2,length.out=7), rev(brewer.pal(n = 7, name = "RdYlBu"))))
set.seed(1234)
data <- matrix(rnorm(100 * 10), nrow = 10, ncol = 100)
factors <- rep(letters[1:2], times = c(30, 70))
data_list <- list(a = data[, factors == "a"], b = data[, factors == "b"])
dend_list <- list(a = as.dendrogram(hclust(dist(t(data_list[["a"]]))))),
                  b = as.dendrogram(hclust(dist(t(data_list[["b"]])))))
circos.par(cell.padding = c(0, 0, 0, 0), gap.degree = 5)
circos.initialize(factors = factors, xlim = cbind(c(0, 0), table(factors)))
circos.track(ylim = c(0, 10), bg.border = NA, panel.fun = function(x, y) {
    sector.index = get.cell.meta.data("sector.index")
    d2 = data_list[[sector.index]][, order.dendrogram(dend_list[[sector.index]])]  # 列序对齐聚类
    col_data = col(d2); nr = nrow(d2); nc = ncol(d2)
    for (i in 1:nr) { circos.rect(1:nc - 1, rep(nr - i, nc), 1:nc, rep(nr - i + 1, nc),
                                  border = 'black', col = col_data[i, ], size=0.1) }
    circos.text(CELL_META$xcenter, CELL_META$cell.ylim[1] + uy(25, "mm"), CELL_META$sector.index)})
max_height <- max(sapply(dend_list, function(x) attr(x, "height")))
circos.track(ylim = c(0, max_height), bg.border = NA, track.height = 0.5,
             panel.fun = function(x, y) circos.dendrogram(
               dend_list[[get.cell.meta.data("sector.index")]], max_height = max_height))
circos.clear()   # 图例：Legend(at=c(-2,-1,0,1,2), col_fun=col, title="value") + grid.draw() 叠加 (p.252)
```

(p.251-252；关键：`order.dendrogram()` 使列序与树一致、`max_height` 统一树高基准、`track.height` 控制树的圆环宽度、`gap.degree` 控制扇区间隙)

### 7.5 旭日图（sunburst diagram / multi-level pie chart / 径向树图）

- **用途**：「通过一系列的圆环显示层次结构，再按不同类别节点进行切割。每个圆环代表层次结构中的一个级别，中心圆点表示根节点，层次结构从这个点往外推移」(p.252)
- **适用数据**：层级路径宽表（实例 `Season, Month, Week, Value, label`）→ 自行展开成 `from`/`to` 边表 + 叶节点属性表 (p.254)
- **何时别用 / 坑（关键）**：「该函数**暂时不能直接实现分割角度的均等平分，因而无法使分割角度与其某个数值成比例**……但是我们可以构造数据，从而实现分割角度与其某个数值成比例的旭日图和冰柱图」(p.253) → 必须伪造叶节点；单层旭日图 ≈ 圆环图，无增益 (p.252)；「推荐使用不同颜色突出显示层次分组或特定类别」(p.253)
- **实现路径**：`ggraph(layout='partition')` + `geom_node_arc_bar()`（旭日图）/ `geom_node_tile()`（冰柱图）+ `geom_node_text()` (p.253-255)

**数据构造：用 `fake_circle` 让角度与 Value 成比例**

```r
library(ggraph); library(igraph); library(RColorBrewer); library(dplyr)
df <- read.csv('旭日图.csv', header=TRUE, stringsAsFactors=FALSE)
fake_circle <- c()                                   # 每个 Week 重复 round(10*Value) 次
for (i in 1:nrow(df)){ fake_circle <- append(fake_circle, rep(df$Week[i], round(10*df$Value[i]))) }
edges <- data.frame(rbind(cbind(rep('origin',4), unique(as.character(df$Season)))),
  as.matrix(df[!duplicated(df[c('Season','Month')]),1:2]),
  as.matrix(df[!duplicated(df[c('Month','Week')]),2:3]),
  cbind(fake_circle, as.character(1:length(fake_circle)))))
colnames(edges) <- c('from','to')
df_leaf <- df[,c('Week','Value','label')]
df_leaf$angle <- 90-(cumsum(df_leaf$Value)-df_leaf$Value/2)/sum(df_leaf$Value)*360
df_leaf$angle <- ifelse(df_leaf$angle < -90, df_leaf$angle+180, df_leaf$angle)
vertices <- left_join(data.frame(name=unique(c(as.character(edges$from), as.character(edges$to))))),
                      df_leaf, by=c('name'='Week'))
df_color <- data.frame(rbind(as.matrix(df[!duplicated(df[c('Season','Season')]),c(1,1)]),
  as.matrix(df[!duplicated(df[c('Season','Month')]),c(1,2)]),
  as.matrix(df[!duplicated(df[c('Season','Week')]),c(1,3)])))
colnames(df_color) <- c('Season','name')
vertices <- left_join(vertices, df_color, by='name')
graph <- graph_from_data_frame(edges, vertices = vertices)
```

(p.254)

**绘图：一个开关切换旭日图 / 冰柱图**

```r
# 图 9-3-1(b) 旭日图
ggraph(graph, layout ='partition', circular = TRUE) +
  geom_node_arc_bar(aes(filter =(depth<=3 & depth>0 ), fill = Season), size=0.1)+
  geom_node_text(aes(filter =(depth<=2 & depth>0), label=name, size=-depth), angle=0, colour="black") +
  geom_node_text(aes(label=label, angle=angle), size=2, colour="black")+
  scale_size(range=c(3,4)) + coord_fixed() + scale_fill_brewer(palette="Reds", direction=-1) +
  guides(size="none", fill="none") + theme_void()
# 图 9-3-2(b) 冰柱图
ggraph(graph, layout ='partition')+
  geom_node_tile(aes(filter =(depth<=3 ), fill = Season), size = 0.1)+
  geom_node_text(aes(filter =(depth<=2 & depth>0), label=name, size=-depth), angle=90, colour="black") +
  geom_node_text(aes(label=label), size=2, angle=90, colour="black")+
  scale_size(range=c(3,4)) + scale_y_reverse() + guides(size="none", fill="none") +
  scale_fill_brewer(palette="Reds", na.value = "#FFF2EC") + theme_void()
```

(p.254-255)

- **关键参数**：`layout='partition'` + `circular` 是唯一区分旭日图/冰柱图的开关 (p.254)；`depth` 为 ggraph 自动算出的层级，`filter=(depth<=3 & depth>0)` 控制画到第几层 (p.254)；`size=-depth` 字号随层级递减 (p.254)；`scale_y_reverse()` 让冰柱图根在上 (p.255)
- **出处**：(p.252-255)

### 7.6 冰柱图（icicle diagram / 分区层图 partition layer chart）

「**就是直角坐标系下的旭日图**」，因像屋檐冰柱得名，宽度与数值成正比 (p.252-253)；实现同上 (p.254-255)。**出处** (p.252-255)

### 7.7 圆堆积图（circle packing / 圆形树状图）

- **用途**：「树形图的变体，使用圆形（而非矩形）一层又一层地代表整个层次结构：树木的每个分支由一个圆圈表示，而其子分支则以圆圈内的圆圈来表示」；圆面积可表示额外数值（数量、文件大小），颜色可分类或表示另一变量 (p.255)
- **适用数据**：边列表（左边 `from` 列隶属于右边 `to` 列）+ 节点属性表（须含面积变量 `size`）(p.256)；实例用 ggraph 自带 `data(flare)`（`flare$edges`、`flare$vertices`、`shortName` 列）(p.256)
- **何时别用 / 坑**：「不及矩形树状图般节省空间（因为圆圈内会有很多空白处），可是它实际上比矩形树状图更能有效显示层次结构」(p.255)；相关变体只提及未给代码：方形树状图 squarified treemap、缓冲树状图 cushion treemap、Voronoi 树图 (p.259)
- **实现路径**：`igraph::graph_from_data_frame()` → `ggraph(layout='circlepack')` + `geom_node_circle()` + `geom_node_text()` (p.256)

```r
library(ggraph); library(igraph); library(tidyverse); library(viridis)
data(flare)
edges <- flare$edges %>% filter(to %in% from) %>% droplevels()
vertices <- flare$vertices %>% filter(name %in% c(edges$from, edges$to)) %>% droplevels()
vertices$size <- runif(nrow(vertices))
mygraph <- graph_from_data_frame(edges, vertices=vertices)
ggraph(mygraph, layout = 'circlepack', weight="size" ) +
  geom_node_circle(aes(fill = depth)) +
  geom_node_text(aes(label=shortName, filter=leaf, fill=depth, size=size)) +
  theme_void() + theme(legend.position="FALSE") + scale_fill_viridis()
```

(p.256)

- **关键参数**：`layout='circlepack'`、`weight="size"`（面积变量）、`fill=depth`（按层级着色）、`filter=leaf`（只给叶节点打标签以抗重叠）(p.256)
- **出处**：(p.255-256, p.259)

### 7.8 矩形树状图（treemap / rectangular tree）

- **用途**：「利用嵌套式矩形显示层次结构的方法，同时通过**面积大小显示每个类别的数量**」，父子层次用矩形嵌套隐喻 (p.256)；「矩形面积越大，表示子数据在整体中的占比越大」(p.257)
- **适用数据**：层级表，实例 `Treemap_Data.csv` 含 `parent`、`id`、`value` 三列 (p.258)
- **何时别用 / 坑**：「当分类占比太小的时候，文本会变得很难排布」(p.257)；「相比分叉树形图，矩形树状图的**树形数据结构表达得不够直观、明确**」(p.257)；**包的取舍原书明说**：treemapify 路线「需要的数据计算与转换相对比较复杂。所以**推荐读者直接使用 treemap 包的 treemap() 函数**」(p.257-258)；矩形长宽比困扰可用 Voronoi 树图（`voronoiTreemap` 包）克服 (p.259)
- **实现路径**：首选 `treemap::treemap()`；备选 `treemapify::treemapify()` + `geom_rect()` + `geom_text()` (p.257-258)

```r
library(treemap); library(RColorBrewer)
proglangs <- read.csv("Treemap_Data.csv ")
treemap(proglangs, index=c("parent", "id"), vSize="value", vColor="parent", type="index",
        border.lwds=c(2,0.1), fontcolor.labels=c('white',"grey10"), title="",
        align.labels = list(c("center", "center"), c("right", "bottom")),
        fontsize.labels=c(12, 9), palette="Set1")
```

(p.258)

- **关键参数**：`index` 层级变量向量（顺序即嵌套顺序）；`vSize` 决定面积；`vColor` + `type="index"` 按 index 变量上色；`border.lwds`、`align.labels`、`fontsize.labels` 均按层级顺序传向量/列表 (p.258)
- **出处**：(p.256-259)

---

## 第 8 部分：网络关系型图表（第 10 章，pp.260–286）

### 8.0 网络图表的选择规则

「网络（network）数据是指那些**不具备层次结构**的关系数据。与层次关系型数据不同，网络关系型数据并不具备自底向上或者自顶向下的层次结构，表达的数据关系更加自由和复杂。」用图 `G=(V, E)` 表示，每条边 `exy=(x, y)` 连接两顶点 (p.261)。

**按「方向 × 权重」四维划分（本书的配图依据）** (p.261)

| 数据类型 | 书中示例 | 书中给的图 | 页码 |
|---|---|---|---|
| 有向 + 有权重 | 国家→国家人口迁移 | 相邻矩阵热力图、和弦图、桑基图 | p.261-262, p.265, p.272 |
| 无向 + 无权重 | 文章共同作者合作关系 | 相邻矩阵热力图、节点链接图 | p.261, p.263, p.273 |
| 无向 + 有权重 | 同学关系紧密程度（日均聊天时长） | 未给单独实例 | p.261 |
| 有向 + 无权重 | 药物是否对某基因响应 | 未给单独实例 | p.261 |

**书中网络图类清单**（图 10-0-1 共 9 类）：热力图、桑基图、和弦图、节点链接图、曲线链接的径向布局节点链接图、直线链接的径向布局节点链接图、弧长链接图、蜂箱图、边绑定图 (p.261)

**规模 / 结构相关的原书判断**

- 节点链接图是**首要选择**：「是最自然的可视化布局。它容易被用户理解和接受……**因而是网络数据可视化的首要选择**」；「**群体分析也是网络数据可视化的一个主要目的**」(p.273)
- 节点/链接庞大时 → 蜂巢网络图「**解决了当节点数和节点链接庞大时，经典节点链接图乱糟糟的视觉混乱感**」(p.281)
- 边交错重叠时 → 边绑定图「针对节点链接图中因关系过多造成的**链接线相互交错与重叠，导致难以看清的情况**」的压缩算法 (p.283)
- 和弦图有连接数上限：「和弦图的缺点是**过于混乱，尤其是当要显示太多连接的时候**」；强项是「比较数据集或不同数据组之间的相似性」(p.265)
- 相邻矩阵必稀疏：「由于节点数目多，而两两节点之间不一定都存在关系，从而导致相邻矩阵**一般都是稀疏的**。因此**需要对稀疏矩阵进行排序**，将非零元素尽可能排到主对角线附近，使得矩阵中的数值尽量聚集到一起而主对角占优势，这样不仅可以减少矩阵计算的开销，而且还能更好地展示网络结构中的规律、增强可视化结果的可读性」(p.263)
- 一维布局（径向/弧长）取舍：「**不能像二维布局那样表达网络图的全局结构**，但是也可以清晰地展现数据结构」(p.277)
- 实测规模：OpenFlights 全球 **3275 个机场、37153 个航线**用力导向布局仍出现遮挡——「亚洲和北美洲之间的航线从图上不容易观察清晰，主要是因为亚洲与北美的中间隔了欧洲，被遮挡在了下面」(p.277)
- 流量守恒场景 → 桑基图：「要保持**能量的守恒**……不能在中间过程创造出数据，流失（损耗）的数据应该流向表示损耗的支点」(p.270-271)

### 8.1 相邻矩阵图（adjacency matrix）

- **用途**：N×N 矩阵表达 N 个节点的关系，位置 (i,j) 表示第 i 与第 j 个节点的关系；无权重用零壹矩阵，有权重用数值表示紧密程度；无向网络是对角线对称矩阵，有向网络不具对称性；对角线表达节点与自己的关系 (p.262)
- **适用数据**：方阵（行 = 出发/Region，列 = 抵达）；四类均可，热力图路线尤其适合**有权重的有向**网络 (p.262)
- **何时别用 / 坑**：稀疏且规模大时必先排序/聚类 (p.263)；`ComplexHeatmap::Heatmap()`「输入的数据类型为矩阵结构的数据」(p.264)
- **实现路径**：① `reshape2::melt()` + `ggplot2::geom_tile()`；② 需层次聚类时用 `ComplexHeatmap::Heatmap()` + `circlize::colorRamp2()` (p.262, p.264)

**① 有权重有向 + 行/列排序（ggplot2 路线）**

```r
library(RColorBrewer); library(ggplot2); library(reshape2)
df <- read.csv("AdjacencyDirectedWeighted.csv", header=TRUE, stringsAsFactors = FALSE)
df_sum <- apply(df[,2:ncol(df)], 2, sum)                     # 按每行 "TO" 的总和排序
order <- sort(df_sum, index.return=TRUE, decreasing = FALSE)
df_melt <- melt(df, id.vars = 'Region')
colnames(df_melt) <- c("from","to","value")
df_melt$to <- gsub("\\.", " ", df_melt$to)
df_melt$to <- factor(df_melt$to, levels=df$Region[order$ix], order=TRUE)
ggplot(df_melt, aes(x = from, y = to, fill = value, label=value)) +
  geom_tile(colour="black") + scale_fill_gradientn(colors=brewer.pal(9,'YlGnBu'))+
  xlab('FROM') + ylab('TO') + coord_equal()+
  theme(axis.text.x = element_text(angle=90, hjust=1, colour='black'),
        axis.text.y = element_text(angle=0, hjust=1, colour='black'))
```

(p.262)

**② 无权无向 + 层次聚类（ComplexHeatmap 路线）**

```r
library(ComplexHeatmap); library(circlize)
df <- read.csv("AdjacencyUndirectedUnweighted.csv", row.names=1, header=TRUE, check.names = FALSE)
df <- df[which(rowSums(df, na.rm =TRUE)>=3), which(colSums(df, na.rm =TRUE)>=3)]  # 过滤低频节点
df[is.na(df)] <- 0
col_fun <- colorRamp2(c(0,1), c("#440154","#FDE725"))
Heatmap(as.matrix(df), name = "mat", col = col_fun, cluster_columns = TRUE, show_row_dend = TRUE,
        rect_gp = gpar(col= "gray", lwd=0.05), column_names_side = "bottom", row_names_side = "right",
        column_names_gp = gpar(fontsize = 8), row_names_gp = gpar(fontsize = 8),
        heatmap_legend_param = list(at = c(0,1), labels = c(0,1), title = "value",
                                    legend_height = unit(4, "cm"))))
```

(p.264-265)

- **关键参数**：`melt(df, id.vars='Region')` 宽转长；`geom_tile(colour="black")` 描边；`coord_equal()` 保证格为正方 (p.262)；`rowSums>=3`/`colSums>=3` 是书中处理稀疏的实际手段 (p.264)
- **出处**：(p.262-265)

### 8.2 和弦图（chord diagram）

- **用途**：「显示不同实体之间的相互关系和彼此共享的一些共通之处，因此这种图表**非常适合用来比较数据集或不同数据组之间的相似性**」；节点绕圆周分布，以弧线或贝塞尔曲线连接，「给每个连接分配数值（通过每个圆弧的大小比例表示）」，颜色区分类别 (p.265)
- **适用数据**：既可用 data.frame（长表 `from`/`to`/`value`），也可用 matrix（`M[i,j]` 表示 Y 第 i 类与 X 第 j 类的关系数值）(p.267)
- **何时别用 / 坑**：「和弦图的缺点是**过于混乱，尤其是当要显示太多连接的时候**」(p.265)。复杂度分级可作选型标尺：入门级（只表示存在关系，可指示位置信息 A-C 或单向 A-D）、普通级（接触面积赋数值意义）、高手级（弧线按源或目标数据着色）、殿堂级（两端粗细不同的定向弧）、神话级（弧是否触圆区分行列）(p.265-266)
- **实现路径**：`circlize::chordDiagram()` + `circos.par()` 预设 + `circos.trackPlotRegion()` 加标签/坐标轴 (p.267-269)

```r
library(circlize); library(viridis); library(reshape2)
df <- read.csv("AdjacencyDirectedWeighted.csv", header=TRUE, stringsAsFactors = FALSE, check.names = FALSE)
df_melt <- melt(df, id.vars = 'Region'); colnames(df_melt) <- c('from','to','value')
df_melt$to <- as.character(df_melt$to)
df_sum <- apply(df[,2:ncol(df)],2,sum) + apply(df[,2:ncol(df)],1,sum)   # from/to 总和双向
order <- sort(df_sum, index.return=TRUE, decreasing = TRUE)
df_melt$from <- factor(df_melt$from, levels=df$Region[order$ix], order=TRUE)
df_melt <- dplyr::arrange(df_melt, from)
mycolor <- viridis(10, alpha = 1, begin = 0, end = 1, option = "D"); names(mycolor) <- df$Region
circos.clear()
circos.par(start.degree = 90, gap.degree = 4, track.margin = c(-0.1, 0.1), points.overflow.warning = FALSE)
par(mar = rep(0, 4))
chordDiagram(x = df_melt, grid.col = mycolor, transparency = 0.25,
             directional = 1, direction.type = c("arrows", "diffHeight"), diffHeight = -0.04,
             annotationTrack = "grid", annotationTrackHeight = c(0.05, 0.1),
             link.arr.type = "big.arrow", link.sort = TRUE, link.largest.ontop = TRUE)
circos.trackPlotRegion(track.index = 1, bg.border = NA, panel.fun = function(x, y) {
    xlim = get.cell.meta.data("xlim"); sector.index = get.cell.meta.data("sector.index")
    circos.text(x = mean(xlim), y = 3.2, labels = sector.index, facing = "bending", cex = 1)
    circos.axis(h = "top", major.at = seq(from = 0, to = xlim[2],
                  by = ifelse(test = xlim[2]>10, yes = 2, no = 1))),
                minor.ticks = 1, major.tick.percentage = 0.5, labels.niceFacing = FALSE)})
```

(p.267-269)

- **关键参数**：`directional=1` + `direction.type=c("arrows","diffHeight")` + `diffHeight` 表达方向与粗细差 (p.266, p.268)；`link.sort=TRUE`、`link.largest.ontop=TRUE` 排序并让大连线置顶；`link.arr.type="big.arrow"` 箭头样式；`annotationTrack="grid"` + `annotationTrackHeight` 外围刻度带；`grid.col` 命名颜色向量按扇区上色；`transparency` 透明度 (p.268)；`circos.par(start.degree=90, gap.degree=4)` 起始角与扇区间隙 (p.268)
- **出处**：(p.265-270)

### 8.3 桑基图（Sankey diagram）

- **用途**：别名决策树/流程图/冲击图（alluvial diagram），「对其最准确的定义应当是：桑基图」；「有利于展现**分类维度间的相关性**，以流的形式呈现共享同一类别的元素数量。特别适合表达集群的发展……通常应用于**能源、材料成分、金融**等数据的可视化分析」(p.270)
- **结构三要素**：边（流动的数据）、流量（具体数值）、节点（不同分类）(p.270)
- **适用数据**：邻接矩阵宽表 → `from`/`to`/`weight` → ggalluvial 路线下再 melt 成 `variable`(from/to) × `Region` × `weight` × `group` 长表 (p.272)
- **何时别用 / 坑（核心）**：「起始流量和结束流量相同，所有主支宽度的总和与所有分出去的分支宽度总和相等，保持能量的平衡」(p.270)；「无论数据怎样流动，数据的总量从开始到结束都不能有任何变化，**不能在中间过程创造出数据，流失（损耗）的数据应该流向表示损耗的支点**」(p.271)；边越宽数值越大 (p.270)
- **实现路径**：`ggalluvial::geom_flow()` + `geom_stratum()`（正文作 `geom_stratu()`）+ `ggplot2::ggplot()` + `geom_text(stat="stratum")` (p.271-272)

```r
library(ggalluvial); library(ggplot2); library(viridis); library(RColorBrewer); library(reshape2)
df <- read.csv("AdjacencyDirectedWeighted.csv", header=TRUE, stringsAsFactors = FALSE, check.names = FALSE)
df_melt <- melt(df, id.vars = 'Region'); colnames(df_melt) <- c('from','to','weight')
df_melt$to <- as.character(df_melt$to)
df_melt$group <- seq(1,nrow(df_melt))                        # alluvium：每条流动股的唯一编号
df_melt <- melt(df_melt, id.vars = c('weight','group'), value.name ='Region', factorsAsStrings=FALSE)
df_sum <- apply(df[,2:ncol(df)],2,sum)                       # 按抵达数据 "to" 的总和解序
order <- sort(df_sum, index.return=TRUE, decreasing = TRUE)
df_melt$Region <- factor(df_melt$Region, levels=df$Region[order$ix])
df_melt$variable <- factor(df_melt$variable, levels=c('from','to'))
mycolor <- colorRampPalette(brewer.pal(9,'YlGnBu')))(13)
ggplot(df_melt,
       aes(x = variable, y = weight, stratum = Region, alluvium = group, fill = Region, label = Region)) +
  geom_flow(alpha = 0.7, width=0.25, color = "darkgray") + geom_stratum(alpha =1, width=0.25) +
  geom_text(stat = "stratum", size = 3.5, angle=0) + scale_fill_manual(values= mycolor) + theme_test()+
  theme(legend.position = "none", axis.text.y = element_blank(),
        axis.line = element_blank(), axis.ticks = element_blank())
```

(p.272)

- **关键参数**：`stratum=Region` 决定支点划分；`alluvium=group` 决定每条流的走向，`group` 须逐行唯一；「`geom_stratu()` 函数控制节点的视觉通道映射设定，主要数值由 `stratum` 和 `weight` 决定；`geom_flow()` 函数控制边的视觉通道映射设定，主要由 `alluvium` 和 `weight` 决定」(p.271)；`width` 控制支点与流带宽度；`geom_text(stat="stratum")` 写标签 (p.272)
- **出处**：(p.270-273)

### 8.4 节点链接图（网络型，node-link）

- **用途**：「最自然的可视化布局……因而是网络数据可视化的首要选择」；配 `walktrap.community()` 可做「群体分析」（community），「群体里的人关系紧密，而不同群体之间的关系比较松散」(p.273)
- **适用数据**：稀疏邻接矩阵 → `gather()` 宽转长 → `from`/`to`/`value`；节点属性为「每个节点的链接总数」`n` (p.275-276)
- **三种形态**：①二维力导向 `layout='fr'` + `geom_edge_link()` (p.276)；②径向：改「`ggraph()` 函数的 layout 参数为：`layout = 'linear', circular = TRUE`；再将链接线使用直线链接函数 `geom_edge_link()` 或者曲线链接函数 `geom_edge_arc()`」(**坑**：「要设定每个节点的标签的角度（angle）」) (p.278)；③弧长链接图（arc diagram，节点置于线性轴、圆弧连接）：「`layout = 'linear', circular = FALSE`」+ `geom_edge_arc()`，可用 `coord_flip()` 垂直放置 (p.277, p.279)
- **何时别用 / 坑**：一维布局「**不能像二维布局那样表达网络图的全局结构**」(p.277)；力导向在空间数据上会遮挡 (p.277)；大型网络改蜂巢图 (p.281)；边重叠改边绑定图 (p.283)
- **实现路径**：`igraph::graph_from_data_frame()` + `igraph::walktrap.community()` + `ggraph::ggraph()` (p.275-277)

**① 邻接矩阵 → graph → 社区识别**

```r
library(tidyverse); library(igraph); library(ggraph); library(colormap); library(wesanderson)
dataUU <- read.csv("AdjacencyUndirectedUnweighted.csv", header=TRUE, check.names = FALSE)
connect <- dataUU %>% gather(key="to", value="value", -1) %>%
  mutate(to = gsub("\\.", " ",to)) %>% na.omit()
c(as.character(connect$from), as.character(connect$to)) %>% as.tibble() %>%
  group_by(value) %>% summarize(n=n()) -> vertices
colnames(vertices) <- c("name", "n")
mygraph <- graph_from_data_frame(connect, vertices = vertices, directed = FALSE)
com <- walktrap.community(mygraph)                      # 识别群体 community
vertices <- vertices %>% mutate(group = com$membership) %>%
  mutate(group=as.numeric(factor(group,
      levels=sort(summary(as.factor(group)), index.return=TRUE, decreasing = T)$ix, order=TRUE)))) %>%
  filter(group < 10) %>% arrange(group, desc(n)) %>% mutate(name=factor(name, name))
connect <- connect %>% filter(from %in% vertices$name) %>% filter(to %in% vertices$name) %>%
  left_join(vertices, by=c('from'='name'))
mygraph <- graph_from_data_frame(connect, vertices = vertices, directed = FALSE)
mycolor <- wes_palette("Darjeeling1", max(vertices$group), type = "continuous")
mycolor <- sample(mycolor, length(mycolor))
```

(p.275-276)

**② 力导向二维图 `layout='fr'`（图 10-4-1(a)）**

```r
ggraph(mygraph, layout='fr') +
  geom_edge_link(edge_colour="black", edge_alpha=0.2, edge_width=0.3) +
  geom_node_point(aes(size=n, fill=as.factor(group)), shape=21, color='black', alpha=0.9) +
  scale_size_continuous(range=c(0.5,10)) + scale_fill_manual(values=mycolor) +
  geom_node_text(aes(label=ifelse(n>20, as.character(name), "")), size=3, color="black") +
  expand_limits(x = c(-1.2, 1.2), y = c(-1.2, 1.2)) + theme_minimal() +
  theme(legend.position="none", panel.grid = element_blank(), axis.line = element_blank(),
        axis.ticks = element_blank(), axis.text = element_blank(), axis.title = element_blank())
```

(p.276-277)

**③ 径向布局 `layout='linear', circular=TRUE`（图 10-4-4(b)）**

```r
number_of_bar <- nrow(vertices); vertices$id <- seq(1, nrow(vertices))
angle <- 360 * (vertices$id-0.5) / number_of_bar
vertices$hjust <- ifelse(angle>180, 1, 0)
vertices$angle <- ifelse(angle>180, 90-angle+180, 90-angle)
mygraph <- graph_from_data_frame(connect, vertices = vertices, directed = FALSE)
ggraph(mygraph, layout = 'linear', circular = TRUE) +
  geom_edge_arc(aes(edge_colour=as.factor(group)), edge_alpha=0.5, edge_width=0.3) +
  geom_node_point(aes(size=n, fill=as.factor(group)), shape=21, color='black', alpha=0.9) +
  scale_size_continuous(range=c(0.5,10)) + scale_fill_manual(values=mycolor) +
  geom_node_text(aes(x = x*1.05, y=y*1.05, label=name, angle=angle, hjust=hjust,
                     color=as.factor(group)), size=3) +
  scale_color_manual(values=mycolor) + scale_edge_color_manual(values=mycolor) +
  expand_limits(x = c(-1.6, 1.6), y = c(-1.6, 1.6)) + coord_fixed() + theme_minimal()
```

(p.278-279)

**④ 弧长链接图 `layout="linear"`（图 10-4-5）**

```r
ggraph(mygraph, layout="linear") +
  geom_edge_arc(aes(edge_colour=as.factor(group)), edge_alpha=0.5, edge_width=0.3, fold=TRUE) +
  geom_node_point(aes(size=n, fill=as.factor(group)), shape=21, color='black', alpha=0.9, stroke=0.1) +
  scale_size_continuous(range=c(0.5,10)) + scale_fill_manual(values=mycolor) +
  scale_edge_colour_manual(values=mycolor) +
  geom_node_text(aes(label=name, color=as.factor(group)), angle=90, hjust=1, nudge_y = -1.5, size=2) +
  scale_color_manual(values=mycolor) +
  expand_limits(x = c(-1.2, 1.2), y = c(-5.6, 1.2)) + theme_minimal()
```

(p.279)

- **关键参数**：`walktrap.community()` 的 `$membership` 用于社区着色，`filter(group<10)` 是书中的降噪手段 (p.276)；`geom_edge_arc(fold=TRUE)` 的 `fold` 让弧线折回 (p.279)；`angle`/`hjust` 须先算进 `vertices` 再重建 graph (p.278)；`edge_colour`/`edge_alpha`/`edge_width` 为非 aes 的整体边设定 (p.276)
- **出处**：(p.273-280)

### 8.4.1 网络节点链接图的布局清单（ggraph layout，抄自图 10-4-2 图注）

书中所述「主要」两类：「力引导布局（force-directed layout）」和「基于距离的多维尺度分析（multidimensional scaling，MDS）布局」(p.273)。书中点名解释的四个：`fr`=Fruchterman-Reingold 力导向、`mds`=多尺度分析、`nicely`=「简单决策树」（原书写作 simpe decision tree）、`gem`=「GEM 算法的力导向布局」(p.274-275)。图中出现但仅列图未解释的：`star`、`components`、`circle`、`grid`、`sphere`、`randomly`（图中印作 "andomly"）、`dh`、`drl`、`graphopt`、`kk`、`lgl` (p.274-275)。

> 编者注：书中 p.275 原文作「常用**局部**参数包括……」，依上下文应为「布局参数」。

### 8.4b 组合图：径向布局热力图 + 节点链接图

用 `circlize` 的 `circos.track()` 造环：外层 `circos.rect()` 画径向热力图，内层 `circos.link()` 依次连接有链接关系的两点，`ComplexHeatmap::Legend()` 造图例 (p.280)；核心调用 `circos.link("a", df_link$from[i]+0.5, "b", df_link$to[i]+0.5, h = 0.8)`，`df_link` 为 `from`/`to` 坐标点表 (p.281)。**出处** (p.279-281)

### 8.5 蜂巢网络图（hive plot / 蜂箱图）

- **用途**：「呈现网络图的新型方法……网络图的节点被放在辐射状线轴上，而网络图的边被绘制为每条辐射状线轴上节点与节点间的连接」(p.281)
- **何时别用 / 坑（核心卖点）**：「蜂巢网络图简单易懂，**解决了当节点数和节点链接庞大时，经典节点链接图乱糟糟的视觉混乱感**」(p.281)；变体「圆形组合堆叠条形图」用于「基因拼接（genomic assembly）的质量评估」(p.283)
- **适用数据**：边列表 + 一个分轴的**分类变量**（实例为把 `degree(graph, mode='in')` 分箱成 Few/Medium/Many）+ 一个轴内排序的**数值变量**（实例为 `count`）；用 `igraph` 自带 `highschool` 数据集 (p.282)
- **实现路径**：`igraph::graph_from_data_frame()` + `igraph::degree()` + `ggraph(layout='hive')` + `geom_edge_hive()` + `geom_axis_hive()` (p.282)

```r
library(ggraph); library(igraph); library(wesanderson)
graph <- graph_from_data_frame(highschool)
V(graph)$friends <- degree(graph, mode = 'in')
V(graph)$friends <- ifelse(V(graph)$friends < 5, 'Few', ifelse(V(graph)$friends >= 15, 'Many', 'Medium'))
V(graph)$count <- degree(graph, mode = 'in')
mycolor <- wes_palette("Darjeeling1", length(unique((V(graph)$friends))), type = "continuous")
ggraph(graph, 'hive', axis = 'friends', sort.by ='count') +
  geom_edge_hive(colour = 'black', edge_alpha = 0.3) +
  geom_axis_hive(color='black', size = 1, label = TRUE) +
  geom_node_point(aes(size=count, fill=friends), shape=21, colour = 'black', stroke=0.2, alpha = 0.95)+
  scale_size_continuous(range=c(0.5,8)) + scale_fill_manual(values=mycolor) +
  guides(fill='none') + coord_fixed() + theme_minimal()
```

(p.282)

- **关键参数**：`axis='friends'` 按顶点属性把节点分配到辐射轴；`sort.by='count'` 决定节点在轴上的径向位置；`geom_axis_hive(label=TRUE)` 画轴与轴标签；`geom_edge_hive()` 画轴间边 (p.282)
- **出处**：(p.281-283)

### 8.6 边绑定图（edge bundling）

- **用途**：「针对节点链接图中因关系过多造成的链接线相互交错与重叠，导致难以看清的情况，而设计的一种**数据可视化压缩算法**。其核心思想就是在**保持信息量（即不减少边和节点总数）**的情况下，将图上互相靠近的边捆绑成束，从而达到去繁就简的效果」(p.283)
- **适用数据**：层次 `edges` + `vertices` + **额外的叶节点间链接表 `connect`**；实例是在图 9-1-1(b) 排序后的层次节点链接图基础上「增加不同节点之间的链接关系」，同色节点表示同组 (p.283)
- **何时别用 / 坑**：须先有径向层次布局画布；链接端点要用 `match(connect$from, vertices$name)` 映射为 graph 的**顶点索引**，否则 `get_con()` 无法绑定 (p.283, p.285)
- **实现路径**：`igraph::graph_from_data_frame()` + `ggraph(layout='dendrogram', circular=TRUE)` + `ggraph::get_con(from=, to=)` + `ggraph::geom_conn_bundle()` (p.285-286)

**① 层次数据（数据构造与 9.1 同源，此处为完整序列）+ 链接索引**

```r
library(ggraph); library(igraph); library(tidyverse); library(RColorBrewer)
d1 <- data.frame(from="origin", to=paste("group", seq(1,10), sep=""))
d2 <- data.frame(from=sort(sample(rep(d1$to, each=100),100,replace=FALSE))),
                 to=sample(paste("subgroup", seq(1,100), sep="_"),100,replace=FALSE)))
d2 <- d2 %>% mutate(order2=as.numeric(factor(from,
        levels=unique(from)[sort(summary(as.factor(from)), index.return=TRUE, decreasing = T)$ix],
        order=TRUE)))) %>% arrange(order2)
edges <- rbind(d1[,1:2], d2[,1:2])
vertices_name <- unique(c(as.character(edges$from), as.character(edges$to))))
vertices_value <- runif(length(vertices_name)); names(vertices_value) <- vertices_name
d2 <- d2 %>% left_join(data.frame(name = vertices_name, value = vertices_value), by = c("to" = "name")) %>%
  arrange(order2, desc(value))
edges <- rbind(d1[,1:2], d2[,1:2])
list_unique <- unique(c(as.character(edges$from), as.character(edges$to))))
vertices <- data.frame(name = list_unique, value = vertices_value[list_unique])
vertices$group <- edges$from[match(vertices$name, edges$to)]
myleaves <- which(is.na(match(vertices$name, edges$from))); nleaves <- length(myleaves)
vertices$id[myleaves] <- seq(1:nleaves)
vertices$angle <- 90 - 360 * vertices$id / nleaves
vertices$hjust <- ifelse(vertices$angle < -90, 1, 0)
vertices$angle <- ifelse(vertices$angle < -90, vertices$angle+180, vertices$angle)
mygraph <- graph_from_data_frame(edges, vertices=vertices)
all_leaves <- paste("subgroup", seq(1,100), sep="_")
connect <- rbind(data.frame(from=sample(all_leaves, 100, replace=T), to=sample(all_leaves, 100, replace=T)),
  data.frame(from=sample(head(all_leaves), 30, replace=T), to=sample(tail(all_leaves), 30, replace=T)),
  data.frame(from=sample(all_leaves[25:30], 30, replace=T), to=sample(all_leaves[55:60], 30, replace=T)),
  data.frame(from=sample(all_leaves[75:80], 30, replace=T), to=sample(all_leaves[55:60], 30, replace=T))))
from <- match(connect$from, vertices$name); to <- match(connect$to, vertices$name)
```

(p.284-285)

**② 绑定绘图**

```r
ggraph(mygraph, layout = 'dendrogram', circular = TRUE) +
  geom_node_point(aes(filter = leaf, x = x*1.07, y=y*1.07, fill=group, size=value), alpha=0.8, shape=21, stroke=0.2) +
  geom_conn_bundle(data = get_con(from = from, to = to), aes(edge_colour=group),
                   tension=1, alpha=0.3, edge_width=0.5) +
  geom_node_text(aes(x = x*1.15, y=y*1.15, filter = leaf, label=name, angle = angle, hjust=hjust, colour=group),
                 size=3, alpha=1) +
  scale_size_continuous(range = c(0.1,5)) +
  scale_colour_manual(values= rep(brewer.pal(9,"Paired"), 30)) +
  scale_edge_colour_manual(values= rep(brewer.pal(9,"Paired"), 30)) +
  scale_fill_manual(values= rep(brewer.pal(9,"Paired"), 30)) +
  expand_limits(x = c(-1.4, 1.4), y = c(-1.3, 1.3)) + coord_fixed() +
  theme_minimal() + theme(legend.position="none")
```

(p.285-286)

- **关键参数**：`get_con(from=, to=)` 由「**顶点索引**」构造连接对象 (p.283, p.285)；`tension=1` 控制绑定曲率/张力 (p.285)；`filter=leaf` 只对叶节点画点与标签 (p.285)；画布基准 `layout='dendrogram', circular=TRUE` (p.285)
- **出处**：(p.283-286)

### 8.6.1 ggraph 的 geom 与适用图表对照

| 类别 | 函数 | 配合 layout / 说明 | 页码 |
|---|---|---|---|
| 边 | `geom_edge_diagonal()` | `dendrogram` 层次树曲线边 | p.247 |
| 边 | `geom_edge_link()` | 直线边；`fr` 与径向直连 | p.276, p.278 |
| 边 | `geom_edge_arc()` | 曲线边；`fold=TRUE` 用于弧长链接图 | p.278-279 |
| 边 | `geom_edge_hive()` | `'hive'` 蜂巢轴间边 | p.282 |
| 边 | `geom_conn_bundle()` + `get_con()` | 边绑定 | p.285 |
| 节点 | `geom_node_point()` / `geom_node_text()` | 「更加通用」 | p.245 |
| 节点 | `geom_node_tile()` | 「只在绘制树形图和冰柱图时使用」 | p.245, p.255 |
| 节点 | `geom_node_arc_bar()` | 旭日图扇形块 | p.254 |
| 节点 | `geom_node_circle()` | 圆堆积图圆圈 | p.256 |
| 轴 | `geom_axis_hive()` | 蜂巢图辐射轴与标签 | p.282 |
| 标度 | `scale_edge_colour_distiller()` / `scale_edge_color_manual()` / `scale_edge_colour_manual()` | 边配色 | p.247, p.279, p.285 |

---

## 第 9 部分：地理空间型图表（第 11 章）

> 本章公共数据对象（反复使用）：`df_map`＝`fortify()` 后的地图多边形数据框（long/lat/group）；`df_city`＝城市业务数据框（long/lat/city 及 orange/apple/banana/watermelon 等数值列）。

### 9.0 地图数据的获取方式（前置，必读）

**三类地图数据素材**（原文判断性表述）(p.292–293)

1. **地图包内置地图素材**：「R 语言的 maps 包就提供了加拿大、法国、意大利、美国和其他地区的地理地图信息」(p.292)
2. **SHP 格式**：「一般国家地理信息统计局和世界地理信息统计单位可以提供下载 SHP 格式的地图数据素材……中国地理信息统计局官网就提供了国家、省级和县级的地图数据素材，可以免费供大家下载使用」(p.292)；全国地理信息资源目录服务系统提供「中国 1∶100 万基础地理数据，共 77 幅 1∶100 万图幅……等 12 类地图要素层」，网址 `http://www.webmap.cn/commres.do?method=result100W` (p.294)；合规提醒：「用户利用下载的地理信息数据编制地图的，应当严格执行《地图管理条例》有关规定」(p.294)
3. **JSON 格式**：「优势在于它的地理信息储存在一个独一无二的文件中。但是这种格式的文件相对于分文本格式的文件，体积较大」(p.293)

**书中使用的数据获取函数（准确抄录）**：`map_data("world")`（maps 包，世界地图数据）(p.293)；`rgdal::readOGR("Virtual_Map1.shp")`（读 SHP → **SpatialPolygonsDataFrame**，SP 格式）(p.294–295, p.304)；`sf::st_read("Virtual_Map1.shp")`（读 SHP → **data.frame**，SF 格式，几何列封装为 list）(p.294, p.304)；`baidumap::getBaiduMap()`（百度局部地图）(p.299)；`ggmap::get_map()` / `ggmap::ggmap()` / `qmap()`（局部地图底图）(p.300)。原文**未出现** `getData()`、`leaflet`、`coord_sf`（仅见 `coord_map()`）

**SP vs SF：为什么优先 sf**（原文判断）(p.295–296)：SP 需分离「描述层（可用 `data@data` 提取）+ 几何映射层（多层嵌套 list，需用 `fortify()` 转数据框）」，绘制时要「为两者指定连接的 id（主键）……总共需要合并两次数据……三次合并」；SF 仅需「数据描述层和业务指标数据的合并」一次 (p.296)

- 标准预处理范式：`dataProjected@data$id <- rownames(dataProjected@data); watershedPoints <- fortify(dataProjected); df_map <- full_join(watershedPoints, dataProjected@data, by="id")` (p.297)

**`geom_polygon()` 与 `geom_path()` 原理**（原文）(p.298)

- 「geom_polygon()函数可以通过数据点的路径控制绘制任意形状的闭合区域；geom_path()函数可以通过数据点的路径控制绘制任意形状的曲线。使用 geom_polygon()函数的数据框的第一行和最后一行的数据是一样的，这样才能确保区域的闭合。」

### 9.1 地理投影要点（coord_map / coord_quickmap）

- **投影三特性（不可兼得）** (p.289)：**等角度**（正形投影，角度和形状保持正确）、**等面积**（面积经主比例放大后不变）、**等距离**（标准经纬线上无长度变形）；「现有的地图投影方法没有一种投影方法可以同时满足以上 3 个特性」。分类：按变形性质分等角/等积/任意投影（等距投影属任意投影，多用于交通图）；按构成方式分几何投影（方位/圆锥/圆柱）与解析投影（伪方位/伪圆锥/伪圆柱/多圆锥）(p.289)
- **6 种常用投影与前 3 种最常用的取舍（原文判断）** (p.289–292)
  - **墨卡托投影**（正轴等角圆柱）：无角度变形但面积变形明显；「常用于航海图、航空图和导航图」；球体半径取 WGS 1984 长半轴 **6378137.0 米**；「最适合用于赤道附近地区」(p.289–290)
  - **阿伯斯投影**（正轴等积割圆锥）：「被广泛应用于着重表现国家或地区面积的地图的绘制，特别适用于东西跨度较大的中低纬度地区，比如中国和美国」；画中国地图时「起始的纬度是 0 度或 10 度；中央经线是 105 度或 110 度，第一标准纬线是 25 度，第二标准纬线是 45 度或者 47 度」(p.290)
  - **方位角投影**：属等距投影，「也尝尝被用于表示被地震影响情况的地图，震中被设定为原点」(p.290)
  - **等距圆柱/球面投影**：「既不是等面积的，也不是等角的，会造成相当大的失真……适用于索引地图」(p.291)
  - **正射投影**：「多用于美观的展示图而不是技术应用」（斜轴法最常用）(p.292)
  - **兰勃特等积方位投影**：「常用于东、西半球图和分洲图……可处理较大区域」；「软件无法处理距中心点超过 90°的任何区域」(p.292)；赤道投影适合非洲、东南亚、澳洲、加勒比海和中美洲，斜轴适合北美洲、欧洲和亚洲 (p.292)
- **R 中的投影设置**（原文）(p.293)：「ggplot 包还提供了 coord_map()函数可以设置地图的投影方法，几乎包括了常见的十几种地图投影方法。」书中给出的可切换写法：
  `coord_map("mercator", xlim=c(-180,180), ylim=c(-90,90))` / `coord_map("albers", parameters=c(0,0))` / `coord_map("gilbert", orientation=c(90,0,0))` / `coord_cartesian()` / `coord_map("ortho", orientation=c(0,30,0))` / `coord_map("azequalarea", orientation=c(0,30,0))` (p.293)
- **跨章补充（第 1 章）** (p.48)：「coord_quickmap()函数是一种保留经纬直线的快速近似绘制的地理坐标系，它最适合靠近赤道的较小区域展示。coord_map()函数可以通过设定 projection 投影参数，从而实现不同投影的地理空间坐标系，包括墨卡托投影、兰勃特等角圆锥投影、Albers 等积正割圆锥投影、等距圆柱投影和正交投影等。」

### 9.2 世界地图（11.1.1）

- **用途**：展示各国/全球范围的指标分布（书中以各国 Scale 数值分级填色为例）
- **适用数据**：国家名 + 数值（两列：`Country`、`Scale`）
- **实现路径**：`maps`（`map_data("world")`）+ `ggplot2`（`geom_map()` 填色、`geom_path()` 画国界、`coord_map()` 设投影）+ `RColorBrewer`
- **坑**：「maps 包就提供了世界地图的绘图数据」但国家名必须与 `map_data("world")` 的 region 名一致，否则填色缺失（书中用 `na.value="grey75"` 兜底）(p.293–294)

```r
library(maps); library(ggplot2); library(RColorBrewer)
colormap<-c(rev(brewer.pal(9,"Greens")[c(4,6)]), brewer.pal(9,"YlOrRd")[c(3,4,5,6,7,8,9)])
mydata<-read.csv("Country_Data.csv",stringsAsFactors=FALSE)
names(mydata)<-c("Country","Scale")
mydata$million<-mydata$Scale/1000000
mydata$fan<-cut(mydata$million,
                breaks=c(min(mydata$million,na.rm=TRUE),0,300,600,900,1200,1500,1800,2100,2400,
                         max(mydata$million,na.rm=TRUE))),
                labels=c(" <=0","0~300","300~600","600~900","900~1200","1200~1500",
                         "1500~1800","1800~2100","2100~2400"," >=2400"),order=TRUE)
world_map <- map_data("world")
ggplot()+
  geom_map(data=mydata,aes(map_id=Country,fill=fan),map=world_map)+
  geom_path(data=world_map,aes(x=long,y=lat,group=group),colour="black",size=.2)+
  coord_map("mercator",xlim=c(-180,180), ylim=c(-90, 90))+
  scale_fill_manual(name="million dollars",values= colormap,na.value="grey75")+
  guides(fill=guide_legend(reverse=TRUE)) + theme_minimal()
```

(p.293–294)

### 9.3 国家地图（11.1.2）

- **用途**：行政区划（省/国家）多边形的填色或分类型着色
- **适用数据**：SHP/JSON 边界 + 描述层类别变量（如 `type`=mainland/island、`country`=PETER/EELIN/JACK…）
- **实现路径**：`rgdal::readOGR()` → `fortify()` → `dplyr::full_join()` → `ggplot2::geom_polygon()`；备选 `sf::st_read()`；备选 `tmap`（`tm_shape()/tm_fill()/tm_borders()/tm_scale_bar()/tm_compass()/tm_layout()/tm_legend()`）
- **何时别用或坑**（原文判断）(p.298)：「tmap 包绘制的图表基本都能用 ggplot2 包绘制实现，所以本节依旧以 ggplot2 包展示地理空间数据」；tmap「里面的图表参数名字跟 ggplot2 不一样……对于新手，还需要一定的时间学习」(p.298)；tmap「默认地理空间数据为 WGS84 坐标系。如果 SHP 文件自带投影文件, 则需要读取投影文件」(p.299)

```r
library(dplyr); library(rgdal); library(ggplot2)
dataProjected <- readOGR("Virtual_Map0.shp")
dataProjected@data$id <- rownames(dataProjected@data)
watershedPoints <- fortify(dataProjected)
df_map <- full_join(watershedPoints, dataProjected@data, by = "id")
ggplot()+
  geom_polygon(data=df_map, aes(x=long, y=lat, group=group,fill=type),colour="black",size=0.25)
```

(p.297)（国家版把 `fill=type` 换成 `fill=country`，数据换 `Virtual_Map1.shp`）(p.297)

```r
library(rgdal); library(tmap)
df_map <- readOGR("Virtual_Map1.shp")
tm_shape(df_map) +
  tm_fill("country", palette="Set2") +
  tm_borders("black", lwd = 1) +
  tm_scale_bar(position=c("left", "bottom")) +
  tm_compass(type = "4star", position=c("left", "top")) +
  tm_layout(inner.margins=c(0.12,0.03,0.08,0.03))+
  tm_legend(position = c("right", "bottom"))
```

(p.299)（tmap 优势：可添加**比例尺**和**指北针** (p.298)）

### 9.4 局部地图（11.1.3）

- **用途**：「具体到地图更加细致的区域，包括街道信息等」(p.299)
- **实现路径**：`baidumap::getBaiduMap()` + `ggmap::ggmap()`；或 `ggmap::get_map()` + `ggmap::ggmap()`
- **函数签名（原样抄录）** (p.299)：`getBaiduMap(location, width = 400, height = 400, zoom = 10, scale = 2, color = "color", messaging = TRUE)`
  - `zoom`：「是一个整数，从 3（洲）到 21（building），默认值是 10」；`color`：`"color" or "bw"` (p.299–300)
- **坑**：「如果直接运行该函数，则会出现这个提示语句：Apply an application from here: http://lbsyun.baidu.com/apiconsole/key。Then register you key by running `options(baidumap.key = '×××')`」(p.300)
- **底图风格参数** (p.300)：`maptype = c("terrain","terrain-background","satellite","roadmap","hybrid","toner","watercolor","terrain-labels","terrain-lines","toner-2010","toner-2011","toner-background","toner-hybrid","toner-labels","toner-lines","toner-lite")`，`source = c("google","osm","stamen","cloudmade")`；Google 4 种常见形式 `terrain(默认)/satellite/roadmap/hybrid`；Stamen 三种 `terrain/watercolor/toner`

```r
library(baidumap); library(ggmap)
baidumap.key ='azNwlAshVwYSOLC2GOkPW'
p <- getBaiduMap('北京', color='bw',messaging=FALSE); ggmap(p)
library(ggmap)
m <- get_map("beijing",zoom=12,maptype="terrain",source="stamen"); ggmap(m)
# 水彩风格：qmap('beijing', zoom = 11, source = 'stamen',maptype = 'watercolor')
```

(p.300)

### 9.5 分级统计地图 choropleth map（11.2）

- **用途**：「在地图分区上使用视觉符号（通常是颜色、阴影或者不同疏密的晕线）来表示一个范围值的分布情况的地图……常见用于选举和人口普查数据的可视化」(p.300)
- **适用数据**：区划单元（国家/省份/市县）+ 每个单元一个（相对）数量指标
- **假设与最大坑**（原文判断）(p.300, p.301)：「分级统计地图假设数据的属性是在一个区域内部的平均分布」；「**分级统计地图最大的问题在于数据分布和地理区域大小的不对称**。通常大量数据集中于人口密集的区域，而人口稀疏的地区却占有大多数的屏幕空间……这种不对称还常常会造成用户对数据的错误理解……因此有时候可以用其他的地理空间图表来更合理地表示区域数据，比如六角形地图。」
- **三种颜色映射方案** (p.301)：单色渐变系 / 双向渐变系 / 完整色谱变化；「当数据的值域大或者数据的类型多样时，选择合适的颜色映射相当有挑战性」
- **实现路径**：`rgdal::readOGR` → `fortify` → `dplyr::left_join(df_map, df_city, by="country")` → `geom_polygon()` + `scale_fill_gradientn()` 或 `scale_fill_gradient2()`

```r
df_city<-read.csv("Virtual_City.csv")
df <- left_join(df_map, df_city[c('country','orange')], by = "country")
# 单色渐变系
ggplot()+
  geom_polygon(data=df, aes(x=long, y=lat, group=group,fill=orange),colour="black",size=0.25)+
  geom_text(data=df_city,aes(x=long, y=lat, label=country),colour="black",size=3)+
  scale_fill_gradientn(colours = rev(brewer.pal(9,'YlGnBu')))+
  theme(legend.position = c(0.9,0.2), legend.background = element_blank())
# 双色渐变系
ggplot()+
  geom_polygon(data=df, aes(x=long, y=lat, group=group,fill=orange),colour="black",size=0.25)+
  geom_text(data=df_city,aes(x=long, y=lat, label=country),colour="black",size=3)+
  scale_fill_gradient2(low="#00A08A",mid="white",high="#FF0000", midpoint = mean(df_city$orange)))+
  theme(legend.position = c(0.9,0.2), legend.background = element_blank())
```

(p.301–302)

### 9.6 Cartogram 示意图（11.2 附）

- **用途**：「按照地理区域的属性值对各个区域进行适当的变形，以克服分级统计地图对空间使用的不合理性」(p.302)
- **两类算法与取舍**（原文判断）(p.302)：**非连续型**「将地图中的区域按照其属性数值放大或者缩小，并保持区域的原始形状。但是这种方法很难保证各个区域之间的相对位置，可能使得某些原本相邻的区域不再相邻，从而影响读者对数据位置信息的阅读。」；**连续型**「先保证区域之间的邻接和相对位置不变，通过改变区域的形状来实现面积与属性成正比。由于区域的相对位置保持不变，这样方便读者识别区域数据信息。」
- **实现路径**：`cartogram::cartogram_cont()`（输入 SpatialPolygonsDataFrame，按 @data 某列变形）+ `rgeos::gCentroid()`（算多边形中心）+ `fortify()`
- **关键参数**：`cartogram_cont(dataProjected, 'orange')`；`fortify(my_cartogram, region='country')`

```r
library(rgdal); library(ggplot2); library(dplyr); library(RColorBrewer)
library(cartogram); library(rgeos)
dataProjected <- readOGR("Virtual_Map1.shp")
df_city<-read.csv("Virtual_City.csv")
dataProjected@data <-left_join(dataProjected@data,df_city[c('country','orange')],by = "country")
my_cartogram <- cartogram_cont(dataProjected, 'orange')
carto_fortified <- fortify(my_cartogram,region='country')
carto_fortified <- carto_fortified %>% left_join(. , my_cartogram@data, by=c("id"="country"))
df_centers <- cbind.data.frame(data.frame(gCentroid(my_cartogram, byid=TRUE),id=my_cartogram@data$country))
ggplot() +
  geom_polygon(data = carto_fortified, aes(fill = orange, x = long, y = lat, group = group) ,
               size=0.05, alpha=0.9, color="black") +
  geom_text(data=df_centers, aes(x=x, y=y, label=id), color="black", size=2, alpha=0.6)
```

(p.303)（六角形＋连续型 Cartogram 见 9.16 (p.329)）

### 9.7 点描法地图 dot map（11.3）

- **用途**：「观察对象在地理空间上分布情况的理想方法……可以很方便地掌握数据的总体分布情况」(p.304)
- **两种类型**（原文）(p.304)：一对一（一个点一个对象，「必须保证点位于正确的空间地理位置」）；一对多（一个点代表聚合单元，「不能将点理解为实际的位置，这里的点代表聚合数据，往往是任意放置在地图上的」）
- **何时别用**（原文判断）(p.304)：「但是当需要观察单个具体的数据时，它是不太适合的。」多系列「可以使用不同形状表示不同类型的数据点」
- **实现路径**：`geom_polygon()` 底图 + `geom_point()`（`shape=21`）或 `geom_label()`；「多数据系列的点描法地图可以使用不同形状表示不同类型的数据点」(p.304)
- **关键参数**：`geom_point(..., shape=21, fill='red', colour="black", size=4)`；`geom_text(..., vjust=1.5, size=3)`；`geom_label(..., fill='orange')`

```r
# 标准点描法地图
ggplot()+
  geom_polygon(data=df_map, aes(x=long, y=lat, group=group),fill='white',colour="black",size=0.25)+
  geom_point(data=df_city,aes(x=long, y=lat),shape=21,fill='red',colour="black",size=4)+
  geom_text(data=df_city,aes(x=long, y=lat, label=city),vjust=1.5,colour="black",size=3)
# 标签型
ggplot()+
  geom_polygon(data=df_map, aes(x=long, y=lat, group=group),fill='white',colour="black",size=0.25)+
  geom_label(data=df_city,aes(x=long, y=lat, label=city),fill='orange',colour="black",size=3)
```

(p.305)

### 9.8 带气泡的地图 bubble map（11.3 附）

- **用途**：「根据数据(lat,long,value)在地图上绘制气泡……数据的大小 value 映射到气泡面积大小，有时候还存在第四维类别变量 catergory，可以使用颜色区分数据系列」(p.305)
- **判断与坑**（原文）(p.305)：「带气泡的地图比分级统计图更适用于比较带地理信息的数据的大小，但是当地图上的气泡过多、过大时，气泡间会相互遮盖而影响数据展示，所以在绘制时需要考虑设定气泡的透明度。」
- 书中图 11-3-2(b) 为**双视觉通道**版（数值同时映射到气泡大小和颜色），「图表的清晰表达程度比图 11-3-1(a)（数值映射到单个视觉通道）更好」。

```r
# (a) 单视觉通道：仅 size=orange，fill 用常量 '#EF5439'，其余同下
# (b) 双视觉通道（书中推荐，清晰表达程度更好）
ggplot()+
  geom_polygon(data=df_map, aes(x=long, y=lat, group=group),fill='white',colour="black",size=0.25)+
  geom_point(data=df_city,aes(x=long, y=lat,size=orange,fill=orange),shape=21,colour="black")+
  geom_text(data=df_city,aes(x=long, y=lat, label=city),vjust=2,colour="black",size=3)+
  scale_size(range=c(2,9),name='price')+
  scale_fill_gradientn(colours = brewer.pal(9,'YlOrRd'),name='price')
```

(p.305–306)

**带双气泡的地图**（多系列即南丁格尔玫瑰图 (p.306)）——**实现路径与坑**（原文）(p.307)：`ggforce::geom_arc_bar()` 参数「主要有 x0（X 轴位置）、y0（Y 轴位置）、r（半径）、start（数据系列的起始角度）和 end（数据系列的终止角度）」；「**都需要将坐标系设定为 coord_fixed()类型，保证 X 轴和 Y 轴使用同等最小单位，不然绘制的图形会出现压扁变形的情况**」(p.307, p.310)

```r
library(ggplot2); library(ggforce)
df1<-data.frame(r=c(4,2), start=c(-pi/2, pi/2), end=c(pi/2,3*pi/2), group=c('a','b'))     # 水平双气泡
df2<-data.frame(r=c(4,2), start=c(0,pi), end=c(pi,2*pi), group=c('a','b'))                 # 竖直双气泡
df3<-data.frame(r=c(4,3,1,2), start=c(0,90,180,270)/180*pi,
                end=(c(0,90,180,270)+90)/180*pi, group=c('a','b','c','d'))                 # 玫瑰图(4 系列)
ggplot(df1)+
  geom_arc_bar(aes(x0=0,y0=0,r0=0,r=r, start=start, end=end, fill=group)))+
  xlim(-4,4)+ ylim(-4,4)+ coord_fixed()
```

(p.306–307)

```r
library(ggforce); library(reshape2)
Map_Scale<-0.75
min_lat<-min(df_map$lat); max_lat<-max(df_map$lat); min_long<-min(df_map$long); max_long<-max(df_map$long)
df_map$x<-(df_map$long-min_long)/(max_long-min_long)
df_map$y<-(df_map$lat-min_lat)/(max_lat-min_lat)*Map_Scale
df_city<-df_city[c("lat","long","city","orange","apple")]
df_city<-melt(df_city,id.vars=c("lat","long","city"))
df_city$start<- rep(c(0, pi), each=nrow(df_city)/2)
r <- 0.04; scale <- r/max(sqrt(df_city$value))
df_city$x<-(df_city$long-min_long)/(max_long-min_long)
df_city$y<-(df_city$lat-min_lat)/(max_lat-min_lat)*Map_Scale
ggplot()+
  geom_polygon(data=df_map, aes(x=x, y=y, group=group),fill='white',colour="black",size=0.25)+
  geom_arc_bar(data=df_city,aes(x0 = x, y0 = y, r0 = 0, r = sqrt(value)*scale,
                                start = start, end = start + pi, fill = variable), color="black",size=0.2)+
  geom_text(data=df_city,aes(label = city, x = x, y = y),vjust=2.25,size =3)+
  xlab("long") + ylab("lat") + coord_fixed()
```

(p.307–308)（另需 `scale_x_continuous(breaks=breaks_x,labels=labels_x)` 还原经纬刻度 (p.308)）

### 9.9 带饼图的地图 pie map（11.4）

- **用途**：「地图和饼图两个图层的叠加，可以用饼图系列表示某地理位置的一系列类别的数值占比情况，饼图的占比对应类别的数据，不同的类别也可以使用不同的颜色区分」(p.309)
- **实现路径**：`scatterpie::geom_scatterpie()` + `geom_scatterpie_legend()`；备选 `ggforce::geom_arc_bar()`
- **坑**（原文）(p.310)：「都需要将坐标系设定为 coord_fixed()类型……不然绘制的图形会出现压扁变形的情况」
- **关键参数**：半径归一化 `radius<-sqrt(Sumindex/pi); df_city$radius<-radius/Max_radius*Bubble_Scale`（`Bubble_Scale<-0.04`）；`geom_scatterpie_legend(df_city$radius, x=0.9, y=0.1, n=5, labeller=...)`

```r
library(scatterpie)
Map_Scale<-0.75
df_map$x<-(df_map$long-min_long)/(max_long-min_long)
df_map$y<-(df_map$lat-min_lat)/(max_lat-min_lat)*Map_Scale
df_city$x<-(df_city$long-min_long)/(max_long-min_long)
df_city$y<-(df_city$lat-min_lat)/(max_lat-min_lat)*Map_Scale
df_city$Sumindex<-rowSums(df_city[,c("orange","apple","banana","watermelon")])
Bubble_Scale<-0.04; radius<-sqrt(df_city$Sumindex/pi); Max_radius<-max(radius)
df_city$radius<-radius/Max_radius*Bubble_Scale
ggplot()+
  geom_polygon(data=df_map, aes(x=x, y=y, group=group),fill='white',colour="black",size=0.25)+
  geom_scatterpie(data=df_city,aes(x=x, y=y, group=city,r=radius),
                   cols=c("orange","apple","banana","watermelon"), color="black", alpha=1,size=0.1)+
  geom_scatterpie_legend(df_city$radius, x=0.9, y=0.1, n=5,
                         labeller=function(x) round((x* Max_radius/Bubble_Scale)^2*pi)))+
  xlab("long") + ylab("lat") + coord_fixed()
```

(p.310)（经纬度归一化 + `scale_x_continuous(breaks=breaks_x,labels=labels_x)` 刻度还原同 p.308–310）

### 9.10 带柱形的地图 bar map（11.5）

- **用途**：「地图和柱形图两个图层的叠加，可以用柱形系列表示地理位置的一系列数据指标，柱形的高度对应指标的数据，不同的指标使用不同的颜色区分」(p.311)
- **实现路径**：`ggplot2::geom_rect()`——「只需要设定矩形的左下角坐标(xmin,ymin)和右上角坐标(xmax,ymax)，然后使用 geom_rect()函数就可以实现绘制多数据系列的柱形图」(p.311)；变体：南丁格尔玫瑰图
- **关键参数**：高度归一化 `MaxH<-max(df_city[,selectCol]); Scale<-3; width<-1.1`；`hjust1/hjust2` 控制同组柱形并排偏移

```r
selectCol<-c("orange","apple","banana","watermelon")
MaxH<-max(df_city[,selectCol]); Scale<-3; width<-1.1
df_city[,selectCol]<-df_city[,selectCol]/MaxH*Scale
df_city<-melt(df_city[c('lat','long','group','city',selectCol)], id.vars=c('lat','long','group','city'))
df_city<-transform(df_city,hjust1=ifelse(variable=='orange',-width,
                       ifelse(variable=='apple',-width/2, ifelse(variable=='banana',0,width/2)))),
                          hjust2=ifelse(variable=='orange',-width/2,
                       ifelse(variable=='apple',0, ifelse(variable=='banana',width/2,width)))))
ggplot() +
  geom_polygon(data=df_map, aes(x = long, y = lat,group=group), fill="white",colour="black",size=0.25)+
  geom_rect(data = df_city, aes(xmin = long +hjust1, xmax = long+hjust2,
                           ymin = lat, ymax = lat + value , fill= variable),
            size =0.25, colour ="black", alpha = 1)+
  geom_text(data=df_city[!duplicated(df_city$city),],aes(x=long,y=lat-0.5,label=city),size=4)+
  labs(fill='type')
```

(p.311–312)

### 9.11 沃罗诺伊地图 Voronoi map（11.6）

- **用途**：「特别适用于如分析星巴克咖啡、7-11 便利店等的最大覆盖区域」(p.312)；原理「基于一组特定点将平面分割成不同区域，而每一区域又仅包含唯一的特定点，并且该区域内任意位置到该特定点的距离比到其他特定点的都要更近」(p.312)
- **实现路径**：`sp::SpatialPointsDataFrame()` → 自写 `SPointsDF_to_voronoi_SPolysDF()`（依赖 `deldir::deldir()` + `tile.list()`）→ `raster::intersect()` 逐个求与行政区的交集 → `fortify()` → `geom_polygon()`
- **关键参数/坑**：`deldir(sp@coords[,1], sp@coords[,2], rw=c(105,135,30,60))` 的 `rw` 为外接矩形范围；`df_pi$group=as.numeric(df_pi$group)+runif(1,0,100)` 用于避免 group 冲突。参考资料：`https://www.codesd.com/item/fill-the-voronoi-polygons-with-ggplot.html` (p.313)

```r
library(ggplot2); library(sp); library(deldir); library(raster)
df_city<-read.csv("Virtual_City.csv")
dati<-data.frame(x=df_city$long,y=df_city$lat,z=df_city$orange,city=df_city$city)
vor_pts <- SpatialPointsDataFrame(cbind(dati$x,dati$y),dati, match.ID=TRUE)
SPointsDF_to_voronoi_SPolysDF <- function(sp) {
  vor_desc <- tile.list(deldir(sp@coords[,1], sp@coords[,2],rw=c(105,135,30,60))))
  lapply(1:(length(vor_desc)), function(i) {
    tmp <- cbind(vor_desc[[i]]$x, vor_desc[[i]]$y); tmp <- rbind(tmp, tmp[1,])
    Polygons(list(Polygon(tmp)), ID=i)
  }) -> vor_polygons
  sp_dat <- sp@data
  rownames(sp_dat) <- sapply(slot(SpatialPolygons(vor_polygons),'polygons'),slot, 'ID')
  SpatialPolygonsDataFrame(SpatialPolygons(vor_polygons),data=sp_dat)
}
```

(p.313–314)

```r
vor <- SPointsDF_to_voronoi_SPolysDF(vor_pts)
group<-1:length(vor)
mypolys<-lapply(group, function(x) {
  tmp = intersect(dataProjected, vor[x,]); df_pi= fortify(tmp)[c('long','lat','group')]
  df_pi$city=as.character(vor[x,]@data$city[1]); df_pi$group=as.numeric(df_pi$group)+runif(1,0,100); df_pi })
df_vor<-data.frame(long=numeric(0),lat=numeric(0),group=numeric(0),city=character(0))
for (i in group ){ df_vor<-rbind(df_vor,mypolys[[i]])}
ggplot() +
  geom_polygon(data=df_vor,aes(x = long, y = lat,group=group,fill=city), color="black", size=0.5,alpha=0.6)+
  geom_point(data = dati, aes(x, y),size=4,shape=21,color="black",fill="red",stroke=0.1)
```

(p.314)

### 9.12 带连接线的地图（11.7）：连接地图 + 流向地图

- **连接地图 connection map**：「用直线或曲线连接地图上不同地点的一种图表……非常适合用来显示地理连接和关系」；典型场景飞机航线 (p.314)
- **流向地图 flow map**：「在地图上显示信息或物体从一个位置到另一个位置的移动及其数量……单一流向线所代表的移动规模或数量由其粗细程度表示」(p.315)
- **坑与建议**（原文判断）(p.315)：连接地图「如果数据量较大，则很容易存在大量的线段重叠和交叉的情况。为避免这种情况带来的数据信息表达不完整，可以设置线条的透明度。」流向地图「箭头可用于表示方向，或者移动是进入还是外出。不用箭头则可以用来代表贸易往来。**建议将流向线合并或者捆绑在一起并避免彼此交叠，以免造成视觉混乱。**」
- **实现路径**：`ggplot2::geom_curve()`；「可以通过定义起始点(x,y)和终止点(xend,yend)，从而连接两点」(p.316)
- **关键参数**：「参数 curvature 为[0,1]，可以控制直线的弯曲程度；arrow = arrow((length = unit(0.25, "cm")) 可以设定直线的末端箭头的大小」(p.316)；直线连接用 `curvature = 0`，曲线用 `curvature = 0.1`；`scale_size(range=c(0.5,1.5))`

```r
df_connect<-read.csv("Virtual_Connect.csv")
df_connect<-df_connect %>% left_join(df_city,by=c('start'='city'))%>% left_join(df_city,by=c('end'='city'))
# (a) 直线连接地图 curvature = 0
ggplot() +
geom_polygon(data=df_map, aes(x = long, y = lat,group=group), fill="white",colour="black",size=0.25)+
geom_curve(data=df_connect,aes(x=long.x,y=lat.x,xend=long.y,yend=lat.y), size=0.75,colour="black",curvature = 0)+
geom_point(data =df_connect,aes(x=long.y,y=lat.y), size=4,shape=21,fill="#F00000",colour="black",stroke=0.1)
# (c) 无箭头的流向地图（size 映射流量）
geom_curve(data=df_connect,aes(x=long.x,y=lat.x,xend=long.y,yend=lat.y,colour=start,size=value),curvature = 0.1)
# (d) 带箭头的流向地图
geom_curve(data=df_connect,aes(x=long.x,y=lat.x,xend=long.y,yend=lat.y, size=value,colour=start),
           arrow = arrow(length = unit(0.25, "cm")),curvature = 0.1)
```

(p.316)

### 9.13 等位地图 isopleth map / 等值线地图（11.8）

- **用途**：「可以说是地图和等高线图两个图层的叠加，常用于表示地面海拔高度的变化曲面、温度变化数据、降雨量数据」(p.317)
- **两条技术路线**（原文）(p.317)：① `geom_contour()` 直接在地图上叠加等高线图层；② `geom_tile()` 或 `geom_raster()` 先插值再绘制整个地图热力图
- **二维核密度估计等位地图**：`sm::sm.density()` → 转 `SpatialPixelsDataFrame` → `!is.na(over())` 求与地图重合区域 → `geom_raster()` + `geom_contour()` (p.317–318)
- **二维插值等位地图**：可选「多项式回归插值、LOESS 局部回归插值、克里格（Kriging）空间插值」；「普通克里格插值方法可以使用 gstat 包的 krige()函数实现……另外，geoR 包和 ields 包也提供了克里格插值方法」(p.319)
- **关键参数**：`ngrid=500`（核密度网格数）；`breaks_lines<-seq(min_z,max_z,by=(max_z-min_z)/20)`（核密度）或 `/10`（插值）(p.318, p.321)；`colormap<-colorRampPalette(rev(brewer.pal(11,'Spectral')))(32)`

```r
library(sm)
cycle_dens<- sm.density(data.frame(df_huouse$long, df_huouse$lat),
                        display= "image", ngrid=500, ylim=c(30,60),xlim=c(105,135))
Density_map<-SpatialPoints(expand.grid(x=cycle_dens$eval.points[,1], y=cycle_dens$eval.points[,2]))
Density_map<-SpatialPixelsDataFrame(Density_map,
              data.frame(kde = array(cycle_dens$estimate, length(cycle_dens$estimate))))
mypolys<-lapply(group, function(x) { tmp = !is.na(over(Density_map, dataProjected[x,])); Density_map[tmp[,1],] })
min_z<-min(df_density$kde); max_z<-max(df_density$kde)
breaks_lines<-seq(min_z,max_z,by=(max_z-min_z)/20)
ggplot() +
  geom_raster(data=df_density,aes(x=x,y=y,fill=kde))+
  geom_contour(data=df_density,aes(x=x,y=y,z=kde),color="white",breaks=breaks_lines)+
  scale_fill_gradientn(colours=colormap)+
  geom_path(data=df_map, aes(x=long, y=lat, group=group),colour="black",size=0.25)+
  coord_cartesian()
```

(p.318–319)

```r
# LOESS 局部回归插值：span 为带宽；control = loess.control(surface="direct") 表示拟合可延伸到现有数据之外
long_mar <-seq(105,135, 0.05); lat_mar <- seq(30,60,0.05)
elev.loess <- loess(value ~ long * lat, df_huouse,span=0.3, control = loess.control(surface = "direct"))
elev.interp <- predict(elev.loess, expand.grid(long=long_mar,lat=lat_mar))
df_loessmap<-data.frame(matrix(elev.interp, nrow=length(long_mar),ncol=length(lat_mar)))
colnames(df_loessmap)<-lat_mar; df_loessmap$long<-long_mar
df_loessmap<-melt(df_loessmap,id.vars='long', variable.name ="lat",value.name = "value")
df_loessmap$lat<-as.numeric(as.character(df_loessmap$lat))  # 原书另有一行，插值版此处同样需要
Interp_map<- SpatialPixelsDataFrame(SpatialPoints(df_loessmap[c('long','lat')]),
                                    data.frame(value = df_loessmap$value))
# 二次多项式回归插值：z=a+bx+cy+dx2+ey2+fxy
formula <- as.formula(value ~ lat + long + I(lat*lat)+I(long*long) + I(lat*long))
lm <- lm(formula, data=df_loessmap); grd<-expand.grid(long= long_mar, lat= lat_mar)
Interp_map<- SpatialPixelsDataFrame(SpatialPoints(grd), data.frame(value = predict(lm, newdata=grd)))
```

(p.320–321)（后续裁剪与绘图同核密度版，`breaks_lines<-seq(min_z,max_z,by=(max_z-min_z)/10)` (p.321)）

### 9.14 线型地图（11.9）

- **用途**：「也可以看成是地图版的峰峦图，使用横向的线条或者带填充的面积绘制二维数据，可以展示一种波澜起伏、峰峦重叠的感觉」(p.322)
- **数据结构坑**（原文判断）(p.322)：「线型地图的数据结构是 Y 轴方向的数据间隔较大，而 X 轴方向的数据间隔较小；**如果给定数据集的 X 轴方向数据间隔较大，有时候需要使用插值处理后，再绘制曲线**。」另有 p.323：「其问题在于有时候会出现间断的经度，也会使用直线连接，所以需要对数据根据经度数值的间断情况做判断处理」
- **参数**（原文）(p.322)：「经度（X 轴方向）的步长为 0.05，纬度（Y 轴方向）的步长为 0.60，loess()函数的带宽（span）为 0.05」
- **实现路径与关键参数**：`ggplot2::geom_linerange()`（垂直线）+ `ggalt::geom_xspline()`（光滑顶部曲线，`spline_shape=-0.1`）+ `scale_color_gradientn()`；`scale<-10; threshold1<-0.15`（低于阈值的高度置 0）；间断判定 `(df_temp$long[k+1]-df_temp$long[k])>long_steps*1.1` 则断开 group

```r
long_steps<-0.05; lat_steps<-0.60
long_mar <-seq(105,135, long_steps); lat_mar <- seq(30,60, lat_steps)
elev.loess <- loess(value ~ long * lat, df_huouse,span=0.05, control = loess.control(surface = "direct"))
elev.interp <- predict(elev.loess, expand.grid(long=long_mar,lat=lat_mar))
# ……同 9.13 构造 Interp_map / mypolys（df_region<-cbind(mypolys[[i]]@coords,mypolys[[i]]@data)）
library(ggalt)
scale<-10; threshold1<-0.15; max_value<-max(df_loessmap$value)
p<-ggplot()+ geom_polygon(data=df_map, aes(x=long, y=lat, group=group),fill='white',colour="NA",size=0.25)
for (i in group){
  df_region<-cbind(mypolys[[i]]@coords,mypolys[[i]]@data)
  df_region$height<-df_region$value/ max_value*scale
  df_region[df_region$height<threshold1,'height']<-0
  df_region$group<-i+runif(1,0,1)
  for (j in list_sort(unique(df_region$lat),decreasing=TRUE)){
    df_temp<-df_region[df_region$lat==j,]
    if (nrow(df_temp)>2) { n<-1
      # 经度间断判定：相邻点经度差 > long_steps*1.1 则断开 group，避免直线连接间断区域
      for (k in 1:(nrow(df_temp)-1)){ if ((df_temp$long[k+1]-df_temp$long[k])>long_steps*1.1){
          df_temp$group[n:k]<-df_temp$group[n:k]+runif(1,0,1)/10; n<-k+1 } }
      p<-p+ geom_linerange(data=df_temp,aes(x=long,ymin=lat,ymax=lat+height, color=value),size=0.3,alpha=1)+
        geom_xspline(data=df_temp,aes(x=long,y=lat+height,group=group),
                     spline_shape=-0.1,colour="black",size=0.8) } } }
p+scale_color_gradientn(colours=colormap)
```

(p.323–324)（另有被注释掉的 `geom_ribbon(aes(x=long,ymin=lat,ymax=lat+height,group=group),fill="white")` 面积版 (p.324)）

### 9.15 点状地图（11.10）

- **用途**：「将连续的地图离散成散点……往往是将散点（long, lat）的数值（value）映射到颜色和大小两个视觉通道。点状地图可以用于二维统计直方的地图展示」(p.324)
- **实现路径**：`expand.grid()` 生成经纬网格 → `findInterval()` 求二维统计直方 → 构造 `SpatialPixelsDataFrame` → `!is.na(over())` 裁剪 → `geom_point()`（建议 `shape=21, stroke=0.1`）
- **参数**（书中取值）：`long_mar <-seq(105,135, 0.6); lat_mar <- seq(30,60, 0.8)`；**三维柱形地图**（点状地图的三维展示）用 `lattice::cloud()` 或 `plot3D::hist3D()`；「推荐使用单色渐变系作为颜色主题」(p.326)

```r
long_mar <-seq(105,135, 0.6); lat_mar <- seq(30,60, 0.8)
grd<-expand.grid(long=long_mar, lat= lat_mar)
df_freq0 <-as.data.frame(table(findInterval(df_huouse$long, long_mar,all.inside=TRUE),
                          findInterval(df_huouse$lat,lat_mar,all.inside=TRUE))))
df_freq0$long <- long_mar[df_freq0[,1]]; df_freq0$lat <- lat_mar[df_freq0[,2]]
df_freq0<-left_join(grd,df_freq0,by=c('long','lat'))
df_freq0[is.na(df_freq0$Freq),'Freq']<-0
freq_map<- SpatialPixelsDataFrame(SpatialPoints(df_freq0[c('long','lat')]), data.frame(value=df_freq0$Freq))
# ……!is.na(over()) 裁剪得到 df_freq（同 9.13）
ggplot() +
  geom_point(data=df_freq,aes(x=long,y=lat,fill=value),size=3,shape=21,stroke=0.1)+
  scale_fill_gradientn(colours=colormap)
```

(p.325)

```r
library(plot3D); library(reshape2)
df_freq1<-left_join(grd,df_freq,by=c('long','lat'))
z<- dcast(df_freq1[c('long','lat','value')],long~lat); rownames(z)<-z$lat
cols<-colorRampPalette(c("#F7FBFF", "red"))(20)   # 推荐单色渐变系颜色主题
pmar <- par(mar = c(5.1, 4.1, 4.1, 6.1))
hist3D(x=long_mar,y=lat_mar,z=as.matrix(z[,2:ncol(z)]), col = cols, border = "black",space=0,alpha = 1,lwd=0.1,
       xlab = "long", ylab = "lat",zlab = "Count", clab="Count", ticktype = "detailed",bty = "f",box = TRUE,
       theta = 35, phi = 20, d=3, colkey = list(length = 0.5, width = 1)))
```

(p.326–327)

### 9.16 简化示意图（11.11）：矩形 / 圆圈 / 六角形 / 网格分面

- **为什么用**（原文判断）(p.327)：「由于各等级（如省份、国家等）的面积大小不一样，但是这又与展示的数据大小无关，这种数据的不对称容易造成用户对数据的错误理解……导致面积小的省份可能在地图上难以识别。我们可以在尽量保证地理区域的相对位置一致的情况下，将各等级地理区域统一大小，使用六角形、矩形或者圆圈代替。」
- **实现路径**：矩形 `geom_tile()`；圆圈 `geom_point(shape=21, size=14)`；六角形 `geom_polygon()`（需六顶点坐标 x,y + 中心 Centerx,Centery + 分组 Province）；自动转换 `geogrid::calculate_grid()`「可以将实际不同级别的行政区域，转换成相应的六角形或者方形示意图」(p.329)；网格分面 `geofacet::facet_geo()`

```r
library(ggplot2)
df_point<-read.csv("China_Grid.csv",stringsAsFactors=TRUE)   # 列：row, col, name(拼音), code(中文名) (p.327)
# (a) 矩形
ggplot(data= df_point,aes(x=col,y=row))+
    geom_tile(colour="black",size=0.1,fill="white")+
    geom_text(aes(label=code),size=3)+ xlim(0.5,7.5)+ scale_y_reverse(limits =c(8.5,0.5))
# (b) 圆圈
ggplot(data= df_point,aes(x=col,y=row))+
  geom_point(shape=21,colour="black",size=14,fill="white")+
  geom_text(aes(label=code),size=3)+ xlim(0.5,7.5)+ scale_y_reverse(limits =c(8.5,0.5))
# (c) 六角形
df_hexmap<-read.csv("ChinaMap.csv",stringsAsFactors=FALSE)
ggplot()+
  geom_polygon(data= df_hexmap, aes(x=x, y=y, group=Province), fill="white", colour="black",size=0.25)+
  geom_text(data= df_hexmap, aes(x=Centerx, y=Centery-0.01, group=Province,label=Province),size=2)
```

(p.328–329)（连续型 Cartogram 六角形示意图见 p.329；geogrid：https://github.com/jbaileyh/geogrid）

```r
library(geofacet); library(ggplot2); library(plyr)
Griddata<-read.csv("China_Grid.csv",stringsAsFactors=TRUE)
sdata<-read.csv("Province_data.csv",stringsAsFactors=TRUE); colnames(sdata)<-c("code","value")
mydata<-join(x=Griddata,y=sdata,by=c("code"))
ggplot(mydata, aes(x=value,fill=code)) +
  geom_density(alpha=1,colour="black",size=0.25)+
  facet_geo(~ code,grid=Griddata)+
  theme_light()+
  theme(legend.position = "none", panel.grid.minor =element_blank())
```

(p.331)（`facet_geo()`「可以将一系列的子图表按地理空间位置放置展示。但是要先提供子图表的地理空间位置数据信息」(p.330)）

### 9.17 邮标法（11.12）

- **用途**：「在地图三维数据（long，lat，value）的基础上，常常再添加一个维度：时间变量（time），这样就需要邮标法，即用分面的方法展示地理空间数据」；「也可以添加一个不同类变量的维度」(p.331)
- **实现路径**：`left_join(df_map, df_city)` → `reshape2::melt()` 宽转长 → `facet_wrap(~variable)` 或 `facet_grid()`；书中图 11-12-1 为网格分面示意，图 11-12-2 为等级统计示意 (p.331–332)

```r
df <- left_join(df_map[c('country','long','lat','group')],
                df_city[c('country','orange','apple','banana','watermelon')], by = "country")
df_melt<-melt(df,id.vars = c('country', 'group','long','lat'))
ggplot()+
  geom_polygon(data=df_melt, aes(x=long, y=lat, group=group,fill=value),colour="black",size=0.25)+
  geom_text(data=df_city,aes(x=long, y=lat, label=country),colour="black",size=3)+
  scale_fill_gradient2(low="#00A08A",mid="white",high="#FF0000", midpoint = mean(df_city$orange)))+
  facet_wrap(~variable)+ theme(strip.text = element_text(size=12))
```

(p.332–333)

### 9.18 地铁线路图（11.13）

- **11.13.1 示意地铁线路图**：数据靠**拾取**获得——「先从网上下载相应的地铁线路图片……然后使用数据拾取工具拾取数据。需要拾取两个方面的数据：（1）地铁站的坐标位置信息；（2）地铁线路的位置信息」(p.334)；工具为「GetData 和 Excel 插件 EasyCharts 等的数据拾取功能」(p.335)。实现：`geom_path()`（线路，`linejoin="bevel", lineend="square"`）+ `geom_point()`（站点，`shape=21`）
- **11.13.2 实际地铁线路图**：关键判断 (p.335)——「现在我们平时看到的地铁站的地铁线路图不是实际的地铁线路，而是设计的示意路线。我们做数据分析时还需要得到实际的地铁线路的经纬坐标位置。」获取方式：「先从网上下载各个地铁站的名称以及对应的站号，再使用 Python 语言根据地铁站名，在高德地图自动查找对应的地理经纬坐标（long, lat）」，底图用 `ggmap::get_map()`。设计学出处：1932 年 Harry Beck 伦敦地铁图「除了每条线路一个颜色，设计重点在于**全图只有 90 度和 45 度角**，均衡各站点距离」(p.335)
- **11.13.3 应用**：房价分布案例——「获得方圆 3km 内所知的二手房每平方米的价格，然后求取均值」(p.338)；距离公式 `D = arc cos(sin(lat1)×sin(lat2)＋cos(lat1)×cos(lat2)×cos(long1-long2))×rearth`，「rearth 为地球平均半径，具体数值为 6371.004 km，D 的单位为 km」(p.338)

```r
library(ggplot2)
mydata_station<- read.csv("深圳地铁线路图_Station.csv", header=T,sep=",")
mydata_Path<- read.csv("深圳地铁线路图_Path.csv", header=T)
mydata_Path$Subway_Num<-factor(mydata_Path$Subway_Num)
mydata_station$Subway_Num<-factor(mydata_station$Subway_Num)
ggplot()+
  geom_path (data=mydata_Path,aes(x=x,y=y,group=Subway_Num,colour=Subway_Num),
             size=1,linejoin = "bevel", lineend = "square")+
  geom_point(data=mydata_station,aes(x=x,y=y,group=Subway_Num,colour=Subway_Num),
             shape=21,size=3,fill="white")
```

(p.335)

```r
# 房价散点叠在实际地铁线路上（底图用 ggmap::get_map()，实际经纬坐标）
mydata_house<- read.csv("ShenzhenHousing_Price_WithLocation.csv", header=T,sep=",")
ggplot()+
  geom_point(data=mydata_house,aes(x=longitude,y=latitude,colour=unit_price),shape=19,size=1,alpha=0.8)+
  geom_path (data=mydata_station,aes(x=long,y=lat,group=Subway_Num),size=0.5,linejoin="bevel",lineend="square")+
  geom_point(data=mydata_station,aes(x=long,y=lat),shape=21,size=2,fill="white",color='black',stroke=0.1)+
  scale_color_distiller(palette = 'RdYlGn',direction=FALSE)+ xlab("long")+ ylab("lat")
# 地铁站房价分级气泡（cut 分级 + size/fill 双通道 + theme_void()）
mydata_station$Unit_Price2<-cut(mydata_station$Unit_Price,
  breaks=c(0,30000,40000,50000,60000,70000,80000,90000,max(mydata_station$Unit_Price,na.rm=TRUE)),
  labels=c(" <=30000","30000~40000","40000~50000","50000~60000",
           "60000~70000","70000~80000","80000~90000"," >=90000"),order=TRUE)
ggplot()+
  geom_path (data=mydata_Path,aes(x=x,y=y,group=Subway_Num,colour=Subway_Num),size=1,linejoin="bevel",lineend="square")+
  geom_point(data=mydata_station,aes(x=x,y=y,group=Subway_Num2,size=Unit_Price2,fill=Unit_Price2),shape=21)+
  guides(fill = guide_legend((title="二手房均价(平方米)")), size = guide_legend((title="二手房均价(平方米)")))+
  theme_void()+ theme(legend.position = "right")
```

(p.338–339)

---

## 第 10 部分：同类图表的选型决策规则（跨笔记汇总）

> 以下每条均为原书明确给出的判断性表述，可直接作为 Skill 的选型规则使用。

### 10.1 数据分布型：按样本量与分布特征怎么选

- **直方图 vs 核密度估计图**：核密度图「是直方图的变种，使用平滑曲线来绘制水平数值，从而得出更平滑的分布」；「核密度估计图比直方图优胜的地方是，它们不受所使用分组数量的影响，所以能更好地界定分布形状」(p.157) → 直方图强依赖 `binwidth`/`bins` (p.159)，核密度强依赖 `bw`/`kernel` (p.158–159)。
- **看分布细节优先抖动散点 → 但点会重合**：「由于随机生成数据点的 X 轴数值，所以很容易存在数据点重合叠加的情况，不利于观察数据的分布规律」(p.162)。
- **要避免随机重叠 → 蜂巢图 / 点阵图**：「每个类别数据点沿着 X 轴类别标签中心线向两侧，同时逐步向上均匀而对称的展开，整体较为美观，也方便读者观察数据的分布规律」(p.162)；点阵图「向两侧均匀而对称地展开……很方便读者观察数据的分布规律」(p.163)。
- **多组比较优先箱形图**：「虽然与直方图或密度图相比似乎有点原始，但它们占用较少空间，当要比较很多组或数据集之间的分布时便相当有用」(p.167)。
- **箱形图的致命局限**：「简单的设计往往隐藏了有关数据分布的重要细节，例如在使用箱形图时，我们不能了解数据分布是双模还是多模的」；「箱形图可以很好地用于观察数据的分布，但是无法适用于双峰及多峰分布的数据」(p.167)。补救：「在箱形图的基础上添加抖动散点图或者点阵图，可以方便读者观察原始数据的分布情况」(p.167)。
- **样本量 → 箱形图选型**：中等数据集（n < 1000）「对四分位数之外数据的估计可能不可靠……对于一个数据集大小为 n 的高斯样本来说，异常值（outlier）和远外值（far-out value）通常小于 10」(p.169)；大数据集（**n ≈ 10,000 − 100,000**）「可以提供更加精准的四分位数之外的数据估计，同时可以展示大量的异常值（约 0.4 + 0.007n）」→ 用 **letter-value 箱形图** (p.169)，但「它与传统箱形图存在一个同样的问题，即无法识别多峰分布的情况」(p.169)。
- **带误差线的柱形图 vs 箱形图**：「对于实验数据的分析与展示，很多人会使用常见的带误差线的柱形图……但是这样展示数据，信息量是非常低的。而使用箱形图能够提供更多的数据分布信息」；Nature Methods 2013 年文章中「有 100 个带误差线的柱形图，而只有 20 个箱形图」；结论「箱形图能够比带误差线的柱形图更好地展示数据的分布情况」(p.170)。
- **均值+标准差的坑**：mm 为双峰分布，「但是其与其他三个类别的均值与标准差基本相同，没有较大区别」(p.164) → 用均值+标准差会完全掩盖双峰。
- **小提琴图 vs 箱形图**：小提琴图「结合了箱形图和密度图的特征」；「虽然小提琴图可以比箱形图显示更多详情，但它们也可能包含较多干扰信息，而且绘图时需要设定核密度估计的带宽」(p.170)。书中做法：在小提琴图里再添加箱形图「这样能更加全面地展示数据」(p.171)。
- **海盗图**：「虽然能完整地表达数据的所有信息，但是过于复杂」；「建议将该图表用于前期数据分布的探索，再具体确定选择合适的图表类型展示数据」(p.170)。
- **云雨图（书中推荐）**：「推荐大家使用云雨图，云雨图可以看成核密度估计曲线图、箱形图和抖动散点图的组合图表，清晰、完整、美观地展示了所有数据信息」；「相比于海盗图，它显得没那么冗余。相比于小提琴图，它又在省却多余的核密度估计曲线的同时，增加了抖动散点图」(p.172)。
- **箱形图的 5 个观察维度**：①关键数值（平均值、中位数、上下四分位数）②任何异常值及其数值 ③分布是否对称 ④数据分组有多紧密 ⑤是否偏斜及方向 (p.166)。
- **异常值判定与耐抗性**：小于 Q1−1.5IQR 或大于 Q3+1.5IQR (p.167)；IQR = Q3−Q1，Norm IQR = IQR×0.7413（相当于正态分布中的 SD）(p.166)；箱形图「绘制依靠实际数据，不需要事先假定数据服从特定的分布形式」，四分位数「具有一定的耐抗性，多达 25% 的数据可以变得任意远而不会很大地干扰四分位数」(p.167)；3σ/z 分数法「产生的异常值个数不会多于总数的 0.7%」，用于非正态数据「其有效性是有限的」(p.167)。

### 10.2 时间序列型：折线图 / 面积图 / 地平线图 / 量化波形图 / 螺旋图 / 日历图怎么选

- **折线图**：「用于在连续间隔或时间跨度上显示定量数值，最常用来显示趋势和关系（与其他折线组合起来）」；X 轴为类别型或序数型（文本坐标轴 / 序数坐标轴如日期坐标轴），Y 轴为数值型；「折线图主要应用于时间序列数据的可视化」(p.187)。
- **折线图 vs 曲线图**：「在曲线图中，X 轴也表示时间变量，但是必须为数值格式，这是两者之间最大的区别。所以，如果 X 轴变量为数值格式，则应该使用曲线图来显示数据，而不是折线图」(p.187)。
- **不要三维折线图**：「因为图表的三维透视效果很容易让读者误解数据，所以不推荐使用三维折线图」(p.187)。
- **堆积/百分比堆积折线图 → 改用面积图**：「堆积折线图和百分比堆积折线图等推荐使用相应的面积图，例如，堆积折线图的数据可以使用堆积面积图绘制，展示的效果将会更加清晰和美观」(p.187)。
- **面积图 vs 折线图（多系列）**：「多数据系列的面积图如果使用得当，那么效果可以比多数据系列的折线图美观很多」，但「颜色要带有一定的透明度，透明度可以很好地帮助使用者观察不同数据系列之间的重叠关系，避免数据系列之间的遮挡」；「数据系列最好不要超过 3 个，不然图表看起来会比较混乱」——**「当数据系列较多时，建议使用折线图、分面面积图或者峰峦图展示数据」**(p.187)。
- **颜色映射填充面积图**：「这种图表只适用于单数据系列的面积图。多数据系列的面积图由于存在互相遮挡的情况，所以会导致数据表达过于冗余，反而影响数据的清晰表达」(p.187)。
- **两条折线间填充面积图**：「这种图表只适用于双数据系列的数值差异比较展示」(p.188)。
- **堆积面积图 vs 堆积柱形图**：「堆积面积图侧重于表现不同时间段（数据区间）的多个分类累加值之间的趋势。百分比堆积面积图表现不同时间段（数据区间）的多个分类占比的变化趋势。而堆积柱形图和堆积面积图的差别在于，堆积面积图的 X 轴上只能表示连续数据（时间或者数值），堆积柱形图的 X 轴上只能表示分类数据」(p.190)；「所以层叠面积图不适用于表示带有负值的数据集」(p.190)。
- **日历图**：「我们平常的日历也可以当作可视化工具，适用于显示不同时间段，以及活动事件的组织情况。时间段通常以不同单位显示，例如日、周、月和年」；两种形式：以年为单位、以月为单位；数据结构一般为 (Date, Value)，Value 映射到颜色 (p.191)(p.192)。
- **螺旋图**：沿阿基米德螺旋线画基于时间的数据，从中心点向外发展；两大好处——「（1）显示大型数据集：螺旋图能大幅度地节省空间，可用于显示大时间段数据的变化趋势；（2）绘制周期性数据：螺旋图每一圈的刻度差相同，当每一圈的刻度差是数据周期的倍数时，能够直观地表达数据的周期性」(p.194)(p.195)。
- **量化波形图**：「很适合用来显示大容量的数据集，以便查找各种不同类别随着时间推移的趋势和模式。比如，波浪形状中的季节性峰值和谷值可以代表周期性模式。量化波形图也可以用来显示大量资产在一段时间内的波动率」(p.199)；但其「缺点在于它们存在不易读的问题，当显示大型数据集时，这类图就显得特别混乱。具有较小数值的类别经常会被"淹没"，以让出空间来显示具有更大数值的类别，使我们不能看到所有数据。此外，我们也不可能读取到量化波形图中所显示的精确数值」(p.200) →「量化波形图还是比较适合不想花太多时间深入解读图表和探索数据的人，它适合用来显示一般表面的数据趋势……除非使用交互技术，否则量化波形图无法精准地表达数据」(p.200) → 替代：「其实，量化波形图是多个时间序列的数据系列对称堆叠而成的，无法精准地表达数据的具体数值。所以，我们也可以使用时间序列的峰峦图展示数据」并把数值映射到渐变颜色条 (p.201)。
- **地平线图**：起因「平常的股票时序数据……常见的数据可视化方法主要是折线图或者面积图，但是这样无法观察到异常的数据，且对于大数据集的图表占用面积较大，所以这才有了地平线图」(p.202)；三个用途「（1）辨识异常数据、异常变化和主要的数据规律；（2）在合理的精度范围内观察每个数据系列（股票）随时间的变化；（3）比较不同数据系列（股票）的数值情况」(p.202)。

### 10.2.1 类别比较：并列 / 堆积 / 百分比堆积怎么选

- `identity`：不做调整，多分类柱形图**不可行**（序列间遮盖）；但多序列散点图、折线图可行 (p.94)
- `stack`（堆积）：用于「单个项目与整体之间的关系」，比较各类别每个数值占总数值大小 (p.94, p.97)
- `dodge`（簇状/并列）：用于直接比较各系列**绝对值** (p.94, p.97)
- `fill`（百分比堆积）：用于比较**占比**而非绝对值 (p.94, p.98)

### 10.3 局部整体型：饼图 / 圆环图 / 复合饼图 / 马赛克图 / 华夫饼图 / 矩形树状图怎么选

- **饼图**：仅当分类数 ≤9、单系列占比、且不需要跨图精确比较时使用；否则 (p.206)：
  - 分类多 / 数据量大 → 百分比堆积柱形图或圆环图
  - 需要在多个整体间比较 → 百分比堆积柱形图/条形图，或圆环图
  - 多变量连续数据（如时序占比）→ 百分比堆积面积图
- **圆环图**：需**跨图比较**多个整体，或需在中心放置标题/文本时使用；「中间挖空让人更关注长度而不是面积」，比饼图更易多图对比，空间利用率高 (p.208)
- **复合饼图系列**：每个坐标位置还要展示一组内部占比时使用；散点复合饼图承载 3 变量 `(x, y, P)`，气泡复合饼图承载 4 变量 `(x, y, z, P)` (p.208)
- **马赛克图**：恰好**两个分类变量**的**列表数据（非关系型）**，只需提供「数据概览」时使用 (p.211)(p.213)
- **矩形树状图**：**树形/层次数据（关系型）**；「矩形树状图用于展示树形数据，是关系型数据。马赛克图用于分析列表数据，是非关系型数据」(p.213) → **唯一明确的二选一规则**
- **华夫饼图**：需快速检视类别分布/比例，并**与其他数据集的比例做对比**时使用 (p.214)；单类别时点状华夫饼图退化为比例面积图，不再表达构成 (p.214)
- **旭日图 vs 圆环图**：「单层的旭日图其实类似于圆环图，但是多层的旭日图展示了外层环状数据与内层环状数据的关系信息」(p.252) → 单层占比用圆环图，多层层次占比用旭日图

### 10.4 高维数据：按维度数量怎么选方法

- **1~3 个变量**：「可以采用散点图、气泡图、曲面图等」(p.81)
- **多于 3 个变量**：「可以采用高维数据可视化方法，如平行坐标系、矩阵散点图、径向坐标图、星形图和切尔若夫脸谱图等」(p.81)
- **三维/四维**：用三维图表「其实就已经有点不容易清晰地观察数据规律与展示数据信息了」→ **改用分面图** (p.221)
- **四到五维**：分面图「可以适用于四到五维的数据结构类型」(p.222)
  - 三维 → 列分面散点图（可加 `stat_smooth(method="loess")`）(p.223)
  - 四维 → 列分面气泡图 (p.224)
  - 五维 → 矩阵分面气泡图（3 连续 + 2 离散）(p.224-225)
- **极高维（书中实例 93 维）**：用降维（PCA / t-SNE）后再画散点图 (p.219, p.220)
- **降维的线性 vs 非线性**：线性有 PCA、MDS、NMF；非线性有 ISOMAP、LLE、t-SNE (p.218)(p.220)。PCA「不能解释特征之间的复杂多项式关系」；t-SNE「基于在邻域图上随机游走的概率分布来找到数据内的结构」(p.220)
- **维数不多 + 某维有特殊含义** → 图标法 (p.233)
- **大规模数据集的全属性同步比较** → 基于区域的方法（热力图）；**少量数据点的全属性同步比较** → 基于样本的方法（图标法）(p.218)

### 10.5 层次关系型：节点链接 vs 空间填充怎么选

- **节点链接图**：「这种方法直观、清晰，适合表示承接的层次关系型数据」(p.243)；**否定判断**——「当个体数目太多时，尤其是广度和深度相差较大时……可读性较差」(p.243)
- **空间填充图**：「和节点链接图相比，这种方法更适合表示包含和从属的关系，而且具有高效的空间利用率，可以表示更多的数据量」(p.243)；**否定判断**——「数据层次关系的表现清晰度不如节点链接图」(p.243)
- **径向 vs 正交布局**：径向「它的节点数据量随着层次而增加，可以容纳更多的节点，更加合理地提高了空间的利用率」(p.244)
- **圆堆积图 vs 矩形树状图**：圆堆积「不及矩形树状图般节省空间（因为圆圈内会有很多空白处），可是它实际上比矩形树状图更能有效显示层次结构」(p.255, p.259) → 要省空间用矩形树状图，要层次清晰用圆堆积图
- **矩形树状图 vs 传统树形结构图**：「矩形树状图能更有效地利用空间，并且拥有展示占比的功能」(p.257)；但「当分类占比太小的时候，文本会变得很难排布」，且「树形数据结构表达得不够直观、明确」(p.257)
- **长宽比困扰** → Voronoi 树图「可以克服矩形空间长宽比的困扰，采用任意多边形来替代矩形空间」(p.259)
- **推荐链**：层级浅/节点少且要「直观清晰」→ 节点链接图 (p.243)；空间不够、节点随层膨胀 → 空间填充类 (p.243)；要「占比/部分-整体」→ 矩形树状图或旭日图 (p.253, p.257)；要「层次结构更好看清」→ 圆堆积图优于矩形树状图 (p.255, p.259)

### 10.6 网络关系型：按节点数 / 边密度 / 是否有流向权重怎么选

- **默认首选**：节点链接图「是最自然的可视化布局。它容易被用户理解和接受……因而是网络数据可视化的首要选择」(p.273)
- **按方向 × 权重选图**：
  - 有向 + 有权重 → 相邻矩阵热力图、和弦图、桑基图 (p.261-262, p.265, p.272)
  - 无向 + 无权重 → 相邻矩阵热力图、节点链接图 (p.261, p.263, p.273)
  - 无向 + 有权重、有向 + 无权重 → 书中未给单独实例 (p.261)
- **节点/链接庞大** → 蜂巢网络图「解决了当节点数和节点链接庞大时，经典节点链接图乱糟糟的视觉混乱感」(p.281)
- **边交错重叠严重** → 边绑定图（保持边与节点总数的压缩算法）(p.283)
- **要比较多组数据的相似性** → 和弦图（强项）；但「和弦图的缺点是过于混乱，尤其是当要显示太多连接的时候」(p.265)
- **要表现流量/能量守恒的过程** → 桑基图 (p.270-271)
- **节点多且关系稀疏** → 相邻矩阵图，但「需要对稀疏矩阵进行排序」将非零元素排到主对角线附近 (p.263)
- **只需局部结构、不要全局结构** → 一维布局（径向/弧长链接图）：「不能像二维布局那样表达网络图的全局结构，但是也可以清晰地展现数据结构」(p.277)
- **规模实测**：OpenFlights 全球 3275 个机场、37153 条航线用力导向布局仍出现遮挡 (p.277)

### 10.7 数值关系型：散点 / 气泡 / 三维 / 分面怎么选

- 两个数值变量看趋势与相关性 → 二维散点图 + `geom_smooth()` (p.118, p.122)
- 第三维数值 → 气泡图（**面积映射**），且静态图最好只到三维 (p.129, p.131)
- 第四维为**类别** → 不用气泡图，改用分面图（栅栏图）(p.131)
- 三个数值变量 → 三维散点图（可再映射颜色/大小到第四维），但 R 中三维图元素难控制 (p.132–133)
- 四维且要内部结构 → 切面图 `slice3D()` (p.140–141)
- 三维关系想要更可读 → 退化成二维散点 + 等高线（用颜色表示 z）(p.137, p.139)
- 三组分体系 → 三元相图 (p.142–143)

### 10.8 地理空间型：地图类型怎么选

- **全球/跨国范围的国别指标** → 世界地图 `map_data("world")` + `geom_map()` 分级填色 (p.293–294)
- **行政区划的填色/分类型着色** → 国家（省/市）地图，SHP 优先用 `sf::st_read()` (p.294, p.297)
- **需要比例尺和指北针** → `tmap::tm_scale_bar()` / `tm_compass()`（但参数命名与 ggplot2 不同，学习成本高）(p.298)
- **街道级别** → 局部地图 `baidumap::getBaiduMap()` 或 `ggmap::get_map()` (p.299–300)
- **区域单元上的聚合指标** → 分级统计地图；**但要注意**「数据分布和地理区域大小的不对称」，必要时改用六角形地图 (p.300–301)
- **看对象的空间分布** → 点描法地图（一对一保证位置正确，一对多的点代表聚合）；不适合看单个具体数据 (p.304)
- **带大小的地理数据比较** → 带气泡的地图，「比分级统计图更适用于比较带地理信息的数据的大小」，但需注意透明度与遮盖 (p.305)
- **每个位置还要表达一组占比** → 带饼图的地图 / 带双气泡的地图（南丁格尔玫瑰图）(p.306, p.309–310)
- **每个位置有多个指标** → 带柱形的地图 `geom_rect()` (p.311)
- **最大覆盖区域分析**（如门店） → 沃罗诺伊地图 (p.312–314)
- **连接关系 / 方向性流动** → 连接地图 / 流向地图，用 `geom_curve(curvature=, arrow=)`；量大设透明度、流向线建议捆绑避免交叠 (p.314–316)
- **连续场数据（海拔/温度/降雨）** → 等位地图，核密度路线 `sm::sm.density()` 或插值路线（多项式/LOESS/克里格 `gstat::krige()`）(p.317–321)
- **连续场 + 起伏感** → 线型地图（地图版峰峦图）(p.322–324)
- **二维统计直方的地图展示** → 点状地图；三维版用 `lattice::cloud()` 或 `plot3D::hist3D()` (p.324–327)
- **区域面积与数据大小不对称** → 简化示意图（矩形/圆圈/六角形），自动转换用 `geogrid::calculate_grid()` (p.327–329)
- **分组子图按地理位置排布** → `geofacet::facet_geo()` (p.330–331)
- **再加一个时间（或类别）维度** → 邮标法（分面）(p.331–333)

---

## 第 11 部分：高频踩坑清单

**第 3 章 · 类别比较型**

1. 「用 R 语言绘制柱形图和条形图的最大潜在问题就是排序问题」——必须改因子水平，只排数据框无效 (p.94–95)
2. X 轴变量按输入数据顺序绘制，Y 轴变量与图例变量按字母顺序绘制 (p.94–95)
3. X 轴为序数型（Fair→Ideal、年月）时不要排序，直接按顺序绘制 (p.95)
4. 多数据系列柱形图应按**第 1 个数据系列**降序 (p.97)
5. 堆积柱形图应先 `colSums()` 求各类别总和再降序 (p.97)
6. 序数型图例须按顺序显示，不能按字母序 (p.98)
7. 百分比堆积柱形图应按**重点系列（一般取占比最大系列）的占比**降序 (p.98)
8. `position="identity"` 在多分类柱形图中不可行，序列间会遮盖 (p.94)
9. 不等宽柱形图不是 `geom_bar()`，须累积求和不算 `xmin`/`xmax` (p.100–101)
10. 棒棒糖图/克利夫兰点图只在**数据量较多**时优于柱形图 (p.101)
11. 雷达图：多个多边形会互相覆盖、变量过多轴线杂乱、数值不如直线轴易比 (p.110)
12. 直接用 `geom_polygon()+coord_polar()` 画雷达图会出现「起点和终点绘制在同一 X 轴位置」；补行后须用 `scale_x_continuous(breaks=, labels=)` 修正标签 (p.110–111)
13. 南丁格尔玫瑰图「由于半径和面积是平方的关系……会将数据的比例大小夸大」；且「面积较大的外围部分会更加引人注目，这跟数值的增量成反比」(p.105)
14. 径向柱形图与玫瑰图的关键区别只在 `ylim()` 是否从 0 开始；ymin=0 会退化成玫瑰图 (p.108–109)
15. 词云图「分析精度不足，主要是为了美观」；较长的词、含升部/降部的词会被过度关注；颜色通常「毫无意义」(p.113–114)

**第 4 章 · 数值关系型**

16. 散点图「两个变量之间的相关性并不等同于确定的因果关系」(p.118)
17. 标准化残差落在 (−2, 2) 区间以外 → 95% 置信度判为异常点，不参与回归线拟合 (p.122)
18. 气泡大小**必须**映射到面积而非半径/直径，否则圆大小呈指数级变化并造成视觉误差 (p.129)
19. 气泡图数据容量有限，静态气泡图最好只表达三个维度 (p.131)
20. 第四维为类别时不要用多系列气泡图，改用分面图（栅栏图）(p.131)
21. 「使用交互可视化方法制作的图表几乎不应用在学术图表中」(p.131)
22. `geom_text()` 容易数据标签重叠，改用 `ggrepel::geom_text_repel()` (p.130)
23. R 中三维图表只能用函数编程实现，坐标轴标题位置、网格线等元素难控制 (p.133)
24. 书中三维图投影方式全部为**正交投影**（orthographic projection）(p.133)
25. 曲面拟合两种方式的取舍不可混用：插值（LOESS）过所有数据点，逼近（多项式+最小二乘）只求接近 (p.136–137)
26. 等高线图若只有颜色没有等值线则无法精确读值；加数值标签后不需要颜色图例 (p.139)
27. Q-Q 图比直方图更有效，但「理解 Q-Q 图则需要更多的背景知识」(p.125)
28. 相关系数矩阵**不要用椭圆图**——「椭圆图比较失败，因为它将最大的面积留给了相关性最弱的数据」(p.152)
29. 相关矩阵配色须用**色差较大的双色序列**（红=正、蓝=负）以体现正负号，而非一般矩阵配色 (p.151–152)
30. 韦恩图超过 5 个集合不适合使用 (p.153–154)

**第 5 章 · 数据分布型**

31. 直方图结果强依赖 `binwidth`/`bins` 分组设置 (p.157, p.159)
32. 核密度估计「不同的带宽得到的估计结果差别很大」(p.158)
33. 抖动散点图随机生成 X 值，「很容易存在数据点重合叠加的情况」(p.162)
34. 箱形图「不能了解数据分布是双模还是多模的」，无法适用于双峰/多峰数据 (p.167)
35. 中等数据集（n < 1000）「对四分位数之外数据的估计可能不可靠」(p.169)
36. 只用均值 + 标准差会完全掩盖双峰分布 (p.164)
37. 带误差线的柱形图「信息量是非常低的」，箱形图更好 (p.170)
38. 小提琴图与瓶状图「绘图时需要设定核密度估计的带宽」(p.170)
39. 海盗图「过于复杂」，建议只用于前期数据探索 (p.170)
40. `geom_boxplot() + coord_flip()` 水平翻转后**图例仍是竖直的**，需换 `ggstance::geom_boxploth()` (p.179)
41. `geom_raster()` 与 `geom_tile()` 的主要区别是前者有 `interpolate` 参数可平滑热力图 (p.139)

**第 6 章 · 时间序列型**

42. 不推荐使用三维折线图——「三维透视效果很容易让读者误解数据」(p.187)
43. 堆积/百分比堆积折线图应改用相应的堆积/百分比堆积面积图 (p.187)
44. X 轴变量为**数值格式**时应用曲线图而非折线图 (p.187)
45. 多系列面积图必须设透明度，且「数据系列最好不要超过 3 个」，多则用折线图/分面面积图/峰峦图 (p.187)
46. 颜色映射填充面积图只适用于**单数据系列** (p.187)
47. 两条折线间填充面积图只适用于**双数据系列** (p.188)
48. 堆积（层叠）面积图**不适用于带负值的数据集** (p.190)
49. 堆积面积图 X 轴只能表示连续数据（时间/数值）；分类数据请用堆积柱形图 (p.190)
50. 量化波形图不易读、小数值类别被"淹没"、无法读取精确数值，只适合展示表面趋势 (p.200)
51. 静态量化波形图系列太多时图例难对应，绘制前应先按各系列最大值排序 (p.200)
52. `ggTimeSeries::ggplot_calendar_heatmap()` 不能设定每个时间单元的边框格式，须改用 `stat_calendar_heatmap()` (p.193)

**第 7 章 · 局部整体型**

53. 饼图分类不可多于 9 个 (p.206)
54. 饼图比百分比堆积柱形图、圆环图更占画布空间 (p.206)
55. 多个饼图之间很难进行数值比较 → 用百分比堆积柱形图/条形图 (p.206)
56. 饼图不适合多变量连续数据占比 → 用百分比堆积面积图 (p.206)
57. 千万不要把饼图类别「按从小到大、顺时针方向展示」——最不重要的部分会占据最显著位置 (p.206)
58. `geom_scatterpie()` 只能配合 `coord_fixed()` 使用 (p.209)
59. 马赛克图「难以阅读，特别是当含有大量分段的时候」，且分段「并非沿着共同基线排列」难以精确比较 (p.211)
60. 非均匀马赛克图「在多数情况下可以被拆解成多个不同的图表」(p.211)
61. 点状华夫饼图在只有单一类别时退化为比例面积图，不再表达构成 (p.214)

**第 8 章 · 高维数据**

62. 矩阵散点图「当维数增加时，矩阵会受到屏幕大小的限制」，且只能发现两维关系 (p.225–226)
63. 平行坐标系「表达维数决定于屏幕的水平宽度」，大数据集折线密度增加会大量交叠 (p.231)
64. RadViz「海量信息对象投影点的交叠问题严重」，如 (0,0,…,0) 与 (a,a,…,a) 投影点相同 (p.232)
65. 柱形图标法「并不适应于展示维数太高的数据」(p.236)
66. 热力图聚类前须先 `scale()` 标准化「以消除量纲对数据结构的影响」(p.228)
67. 多个热力图共享图例时，两图必须共用同一组 `Colormap` 与 `breaks` (p.229)
68. 平行坐标系「推荐使用简洁的背景风格，只保留主要的图表元素」(p.231)

**第 9 章 · 层次关系型**

69. 节点链接图在「个体数目太多时，尤其是广度和深度相差较大时」可读性较差 (p.243)
70. 空间填充类「数据层次关系的表现清晰度不如节点链接图」(p.243)
71. 圆堆积图「不及矩形树状图般节省空间（因为圆圈内会有很多空白处）」(p.255)
72. 矩形树状图「当分类占比太小的时候，文本会变得很难排布」(p.257)
73. 矩形树状图「树形数据结构表达得不够直观、明确」(p.257)
74. ggraph 旭日图「暂时不能直接实现分割角度的均等平分，因而无法使分割角度与其某个数值成比例」→ 必须构造 fake 叶节点数据 (p.253)
75. 指定 `vertices` 时，「edges 中指定的链接序列必须都包含在 df 的第一列中」(p.245)
76. 所有 radial/线性布局都要先把 `angle`/`hjust` 算进 `vertices` 再重建 graph (p.247, p.278, p.285)

**第 10 章 · 网络关系型**

77. 相邻矩阵「一般都是稀疏的」，绘制前必须对稀疏矩阵排序/聚类 (p.263)
78. 和弦图「过于混乱，尤其是当要显示太多连接的时候」(p.265)
79. 一维布局「不能像二维布局那样表达网络图的全局结构」(p.277)
80. 边绑定的链接端点须用 `match(connect$from, vertices$name)` 映射为**顶点索引**，否则 `get_con()` 无法绑定 (p.283, p.285)
81. 力导向布局在空间数据上会出现遮挡（OpenFlights 3275 机场 / 37153 航线实例）(p.277)

**第 11 章 · 地理空间型**

82. 地图数据的国家名必须与 `map_data("world")` 的 region 名一致，否则填色缺失 (p.293–294)
83. 分级统计地图「最大的问题在于数据分布和地理区域大小的不对称」→ 可改用六角形地图 (p.300–301)
84. 点描法地图「当需要观察单个具体的数据时，它是不太适合的」(p.304)
85. 一对多点描法的点「不能将点理解为实际的位置」(p.304)
86. 带气泡的地图气泡过多过大时会相互遮盖，须设透明度 (p.305)
87. 带双气泡/饼图/玫瑰图的地图**必须** `coord_fixed()`，否则图形压扁变形 (p.307, p.310)
88. 线型地图 X 轴方向数据间隔较大时需先插值再绘制曲线 (p.322)
89. 线型地图会「出现间断的经度，也会使用直线连接」，须按经度间断情况做分组断开判定 (p.323)
90. SP 格式需「总共需要合并两次数据……三次合并」，SF 只需一次 → 优先 `sf::st_read()` (p.296)
91. `baidumap::getBaiduMap()` 需先申请 key 并用 `options(baidumap.key='×××')` 注册 (p.300)
92. 使用下载的地理信息数据编制地图须「严格执行《地图管理条例》有关规定」(p.294)

---

## 附录：书中未出现的常见包名（防止误引用）

以下内容摘自各章笔记末尾的「核查」段落，**原样保留**，供 Skill 编写者核对，避免在生成代码时凭空引用书中并不存在的包。

**第 3–4 章（类别比较型 / 数值关系型）**

任务清单中提到的 `ggradar`、`ggwordcloud`、`ggcorrplot`、`ggVennDiagram`、`akima`、`plotly` 在 ch03/ch04 原文中**均未出现**；对应的图在书中分别由 `fmsb::radarchart()`/自制 `coord_radar()`、`wordcloud::wordcloud()`、`corrplot::corrplot()`/`ggplot2::geom_tile()`、`VennDiagram::venn.diagram()`、`plot3D::persp3D()`/`slice3D()` 实现。若 Skill 需用这些包，属书外补充，不应标注本书页码。

**第 7–8 章（局部整体型 / 高维数据）**

`fastPCA`、`symbols()`、`ggdendro` 均**未在第 7、8 章出现**。书中 PCA 实际用 `FactoMineR::PCA()` + `factoextra::fviz_pca_ind()`，非 `fastPCA` (p.219)；星形图实际用 `graphics::stars()`，非 `symbols()` (p.234, p.236)；热力图聚类分块由 `pheatmap()` 的 `cutree_col`/`cutree_row` 控制，未用 `ggdendro` (p.228)。（`ggrepel`、`ggally`、`ggalluvial`、`lattice`、`plot3D` 仅在第 1 章 p.82 作为工具链提及。）

> 跨章补充：`ggdendro` 虽未出现在第 7–8 章，但在**第 9 章 p.249** 作为 `ggdendro::ggdendrogram()` 出现；`ggforce::geom_parallel_sets()` 虽未出现在第 9–10 章，但在**第 8 章 p.231** 出现。引用时须按实际出现的章节标注页码。

**第 9–10 章（层次关系型 / 网络关系型）**

反向校验：`dendextend`、`tidygraph`、`ggforce::geom_parallel_sets`、`packcircles`、`networkD3`、`visNetwork` 在这两章（全章核对 p.242-286）**均未出现**——Skill 勿凭空引用。

**第 11 章（地理空间型）**

原文**未出现** `getData()`、`leaflet`、`coord_sf`（仅见 `coord_map()`）。

