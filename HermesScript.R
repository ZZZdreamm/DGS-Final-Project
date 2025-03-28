#### DATA EXTRACTION #### 

#ClinVar: https://www.ncbi.nlm.nih.gov/clinvar/ 
Expression = '"NAME OF THE PHENOTYPE"[Disease/Phenotype]'
ClinVar = hermes::get_clinvar_data_by_expression(Expression, clean_phenotype = TRUE, keyword = "KEYWORD TO FILTER THE RESULTS")

#GWAS: https://www.ebi.ac.uk/gwas/home 
GWAS = hermes::get_GWAS_data_by_phenotype("NAME OF THE PHENOTYPE", FALSE)

#LOVD: https://www.lovd.nl
RelevantGenes = c("LIST OF RELEVANT GENES (SEE POLIFORMAT)" )
LOVD = hermes::get_lovd_data_from_gene_list(RelevantGenes, TRUE, "KEYWORD TO FILTER THE RESULTS")

#### INTEGRATION #### 
Integration= hermes::integrate_datasets(list(ClinVar, GWAS, LOVD))

#### DATA PREPARATION #### 

Hermes = hermes::prepare_data_for_ulises(Integration, FALSE, TRUE)


#### FILES GENERATION ####
HermestoJSON = hermes::to_json(Hermes)
hermes::write_json(HermestoJSON, "your_path\\HermesData.json")
jsonlite::write_json(RelevantGenes, "your_path\\RelevantGenes.json")