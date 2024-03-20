library(circlize)
library(dplyr)

# 加载数据
df <- read.csv("C:/Users/ausu/Desktop/CellGAT_data/Pre_pro_2.csv")

# 选择Prob值最大的前10行
top_10 <- df %>% arrange(desc(Prob)) %>% head(10)

# 创建连接数据框，指定源和目标
links <- data.frame(
  source = top_10$Src,
  target = top_10$Dst,
  value = top_10$Prob
)

# 绘图前设置
circos.clear()
circos.par(gap.degree = 1)

# 绘制chord图
chordDiagram(
  x = links, 
  annotationTrack = c("grid"), 
  annotationTrackHeight = mm_h(5)
)

# 字体
par(cex = 0.25)

# 在每个扇区中添加标签
for(si in get.all.sector.index()) {
  xlim <- get.cell.meta.data("xlim", sector.index = si, track.index = 1)
  ylim <- get.cell.meta.data("ylim", sector.index = si, track.index = 1)
  circos.text(
    mean(xlim), mean(ylim), si, sector.index = si, 
    track.index = 1,  facing = "bending.inside", 
    niceFacing = TRUE, col = "black"  # 将字体颜色改为黑色
  )
}

# chord图输出为.png   300dpi
png("C:/Users/ausu/Desktop/CellGAT_data/chord/Pre_pro_2.png", width = 800, height = 800, res = 300)

# 绘制chord图
chordDiagram(
  x = links, 
  annotationTrack = c("grid"), 
  annotationTrackHeight = mm_h(5)
)

par(cex = 0.35)

# 在每个扇区中添加标签
for(si in get.all.sector.index()) {
  xlim <- get.cell.meta.data("xlim", sector.index = si, track.index = 1)
  ylim <- get.cell.meta.data("ylim", sector.index = si, track.index = 1)
  circos.text(
    mean(xlim), mean(ylim), si, sector.index = si, 
    track.index = 1,  facing = "bending.inside", 
    niceFacing = TRUE, col = "black"  # 将字体颜色改为黑色
  )
}

dev.off()