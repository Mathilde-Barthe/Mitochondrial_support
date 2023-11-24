# Mitochondrial_support
Here is a pipeline to estimate cross-contamination that have been designed for close related species/lineages. 

Disentangling gene flow from cross-contamination could be difficult, however in the first case individuals are expected to have only one mitochondrion contrary to cross-contamination were at least two mitochondrion are expected. Considering that, this pipeline aims to estimate for each individuals if its mitochondrial read supports for one or multiple lineages. 

# Installation 
```
git clone https://github.com/Mathilde-Barthe/Mitochondrial_support.git
```

# Dependencies 
PAUP : https://phylosolutions.com/paup-documentation/paupmanual.pdf

bam-readcount : https://github.com/genome/bam-readcount

Python

R packages ggplot2, dplyr, colorspace, cowplot, grid, gridExtra, ggpubr
```
install.packages(c(“ggplot2”, “dplyr”, “colorspace”, “cowplot”, “grid”, “gridExtra”, “ggpubr”)
```

# Usage
## 1/ Get the list of Diagnostic Positions to explore

First, it is required to list the positions that are specific to the different lineages tested, called Diagnostic Positions (DP). You can identify them using PAUP for example.


## 2/Extract the read support for these DP
Then using `bam-readcount` extract the read support for your list of diagnostic positions 

 `-f` Indicate your reference mitogenome

`<bam_file>` Your mitochondrial mapping file  

 `-l`  List of diagnostic positions in bed format 

 `-w` Maximum number of warnings 
 
 `-q`  Minimal mapping quality

  Feel free to adapt bam-readcount parameters to your pipeline.
 
```
bam-readcount -f <reference_genome> <bam_file> -l <list_DP> -w 0 -q 20 | sort -u  > "$ID"_read_count.txt
```

## 3/ Estimate the lineages support for your individuals

For a given individual, this script estimate the support for all lineages by outputting the rate of DP, the read frequency and the total DP by lineages. To be considered, a DP has to be supported by at least 3 reads.

`-r` Readcount file of your individual from the step 2 

`-d` DP assignment to the corresponding species/lineage following this tab-separated format : position \t nucleotide \t lineage

`-i` Name or ID of the individual

`-o` Path and name of your output file

```
Estimate_lineage_support.py -r "$ID"_read_count.txt -d <DP_assignment_file> -i <ID> -o <Output_lineage_support>
```
## 4/Plot these results using R

Finally, the lineage support is estimated as the product of the rate of DP and the read frequency.

/!\ The argument order matters. 

Please, indicate in first position `<Output_lineage_support>` the output of the step 3 . Then,`<Individual_order>` the list of all your individuals in the desired order for the plot. Finaly, indicate `<Output.png>` the path and name of the output plot. 
```
Plot_lineage_support.R <Output_lineage_support> <Individual_order> <Output.png>
```

# Exemple
You can try the steps 3 and 4 using the test files and run :
```
cd data/

for ID in IND_1 IND_2
do
./Estimate_lineage_support.py -r "$ID"_read_count.txt -d DP_assignment.csv -i "$ID" -o ./Out_lineage_support.txt
done

./Plot_lineage_support.R Out_lineage_support.txt Individual_order ./Figure_Lineage_support.png
```
