library(networkD3)
library(dplyr)
library(htmlwidgets)
library(webshot)

# 读取CCI数据
cci_data <- read.csv("C:/Users/ausu/Desktop/CellGAT_data/Cardiac_cells.csv")

# 提取 Prob 值前50的数据
top_50 <- cci_data %>%
  arrange(desc(Prob)) %>%
  slice(1:10)

# 创建节点数据
nodes <- data.frame(name = unique(c(top_50$Src, top_50$`Src.Cell`, top_50$Dst)))
nodes$color <- ifelse(nodes$name %in% top_50$Src, top_50$Src, ifelse(nodes$name %in% top_50$`Src.Cell`, top_50$`Src.Cell`, top_50$Dst))

# 创建连接数据，从 Src 到 Src.Cell
links_src_to_cell <- data.frame(
  source = match(top_50$Src, nodes$name) - 1,
  target = match(top_50$Src.Cell, nodes$name) - 1,
  value = top_50$Prob,
  color = top_50$Src  # 设置连接的颜色与出发节点颜色相同
)

# 创建连接数据，从 Src.Cell 到 Dst
links_cell_to_dst <- data.frame(
  source = match(top_50$Src.Cell, nodes$name) - 1,
  target = match(top_50$Dst, nodes$name) - 1,
  value = top_50$Prob,
  color = top_50$Src.Cell  # 设置连接的颜色与出发节点颜色相同
)

# 合并连接数据
all_links <- rbind(links_src_to_cell, links_cell_to_dst)



# 绘制Sankey图
sankey <- sankeyNetwork(Links = all_links, Nodes = nodes, Source = "source", Target = "target",
                        Value = "value", NodeID = "name", units = "Probability",
                        LinkGroup = "color",
                        fontSize = 15,  # 将标签字体大小设置为0，即隐藏标签
                        nodeWidth = 100)  # 设置节点宽度

# 保存Sankey图为HTML文件
saveWidget(sankey, 'sankey.html', selfcontained = TRUE)

# 使用webshot将HTML文件转换为PNG图片，确保你已经安装了PhantomJS
webshot('sankey.html', 'C:/Users/ausu/Desktop/CellGAT_data/Cardiac_cells.png', vwidth = 1000, vheight = 600)
