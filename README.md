# bioinformatics

## Finding subsequences in genomes
- We can find the number of ocurrences of k-mers in a genome.
- Recall that these k-mers actually represent binding sites for proteins.
- If the protein doesn't care to which strand it binds, we should group counts of complements.
- Understand what value of k should you use. Bacterial DnaA boxes (for replication) are typically 9 nucleotides long, so k=9.
- If we have the hypothesis that a certain region of the genome we want to find (e.g. ori) has many sites of a particular sequence, we should also check whether it repeats all across the genome, perhaps it is simply a common k-mer.

## Use cases for k-mers app
- [x] Upload genome from .txt file
- [ ] Search for genome by name
- [ ] Obtain most frequent k-mers in genome
- [ ] Visualize distribution of specified k-mer in genome