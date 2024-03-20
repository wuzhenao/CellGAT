library(networkD3)
library(dplyr)
library(htmlwidgets)
library(webshot)
# 读取CCI数据
cci_data <- read.csv("C:/Users/ausu/Desktop/CellGAT_data/Pre_pro_0.csv")

# 提取不同的 Src 和 Dst 数据，并确保它们不相等
unique_pairs <- cci_data %>%
  filter(Src != Dst) %>%
  distinct(Src, Dst, .keep_all = TRUE)

# 只取前十个不同的 Src 和 Dst 相互作用对
top_10 <- head(unique_pairs, 10)

# 创建节点数据
nodes <- data.frame(name = unique(c(top_10$Src, top_10$Dst)))

# 创建连接数据，从 Src 到 Dst
links <- data.frame(
  source = match(top_10$Src, nodes$name) - 1,
  target = match(top_10$Dst, nodes$name) - 1,
  value = 1,  # 设置连接的值为1，表示相互作用对的存在
  color = top_10$Src  # 设置连接的颜色与出发节点颜色相同
)

# 绘制Sankey图
sankey <- sankeyNetwork(Links = links, Nodes = nodes, Source = "source", Target = "target",
                        Value = "value", NodeID = "name", units = "Count",
                        LinkGroup = "color", 
                        fontSize = 0,  # 设置标签字体大小
                        nodeWidth = 100)  # 设置节点宽度
# 保存Sankey图为HTML文件
saveWidget(sankey, 'sankey.html', selfcontained = TRUE)

# 使用webshot将HTML文件转换为PNG图片，确保你已经安装了PhantomJS
webshot('sankey.html', 'C:/Users/ausu/Desktop/CellGAT_data/Pre_pro_0.png', vwidth = 1000, vheight = 600) 
