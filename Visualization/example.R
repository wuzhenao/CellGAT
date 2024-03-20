library(circlize)

# 设置随机种子以确保可重现性
set.seed(999)

# 创建示例矩阵
mat <- matrix(sample(18, 18), 3, 6) 
rownames(mat) <- paste0("S", 1:3)
colnames(mat) <- paste0("E", 1:6)

# 创建示例数据框
df <- data.frame(from = rep(rownames(mat), times = ncol(mat)),
                 to = rep(colnames(mat), each = nrow(mat)),
                 value = as.vector(mat),
                 stringsAsFactors = FALSE)
df
# 绘制弦图
grid.col <- c(S1 = "#E66F51", S2 = "#8AB07D", S3 = "#F3A261",
              E1 = "#8AB07D", E2 = "grey", E3 = "#2A9D8C", E4 = "grey", E5 = "#E9C46B", E6 = "grey")
chordDiagram(mat, grid.col = grid.col, annotationTrack = c("grid"), annotationTrackHeight = mm_h(c(5, 3)))

# 将输出保存为300dpi的PNG图像
png("C:/Users/ausu/Desktop/CellGAT_data/example.png", width = 800, height = 800, res = 600)
chordDiagram(mat, grid.col = grid.col, annotationTrack = c("grid"), annotationTrackHeight = mm_h(c(5, 3)))
dev.off()



