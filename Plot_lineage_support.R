#!/usr/bin/env Rscript
library(ggplot2)
library(dplyr)
library("colorspace")
library(cowplot)
library(grid)
library(gridExtra) 
library(ggpubr)

args = commandArgs(trailingOnly=TRUE)

dat<-read.csv(args[1],  sep=" ", header=T)
ind<-read.csv(args[2],header=F)$V1
out_name<-args[3]


# Index of lineage support  
dat$index=dat$rate_DP*dat$freq_read


#ordering data according to le list provided and the values of index
dat=dat %>% arrange(factor(ID, levels = rev(ind)), desc(index) )
dat <- dat %>% mutate(ordering = row_number())
dat$ID<-factor(dat$ID,levels=c(unique(dat[order(dat$ordering),1])))
dat$lineage=as.factor(dat$lineage)

### Define colors 
mycolor <- RColorBrewer::brewer.pal(length(unique(dat$lineage)), "Set1")


legend=as_ggplot(cowplot::get_legend(ggplot(dat, aes(x =index , y = ID, fill = lineage))+
                             geom_bar(stat="identity")+
                             scale_fill_manual(values = mycolor)))

plot=ggplot(dat, aes(x =index , y = ID, fill = interaction(-ordering, ID))) + 
  geom_bar(stat="identity")+
  scale_fill_manual("lineage", values =mycolor[dat$lineage],
                    breaks = with(dat, interaction(-ordering, ID)))+
  theme(legend.position="none")+
  xlab('Lineages support')+
  ylab('')


pdf(paste(out_name,".pdf", sep='')) 
ggarrange(plot, legend, ncol = 2, nrow = 1 )
dev.off()




