#### DATA EXTRACTION ####

#ClinVar: https://www.ncbi.nlm.nih.gov/clinvar/
Expression = '"Hypertrophic Cardiomyopathy"[Disease/Phenotype]'
ClinVar = hermes::get_clinvar_data_by_expression(Expression, clean_phenotype = TRUE, keyword = "hypertrophic")

#GWAS: https://www.ebi.ac.uk/gwas/home
GWAS = hermes::get_GWAS_data_by_phenotype("Hypertrophic Cardiomyopathy", FALSE)

#LOVD: https://www.lovd.nl
RelevantGenes = c("MYH7", "LOC126861897", "MHRT", "MYBPC3" )
LOVD = hermes::get_lovd_data_from_gene_list(RelevantGenes, TRUE, "hypertrophic")

#### INTEGRATION ####
Integration= hermes::integrate_datasets(list(ClinVar, GWAS, LOVD))

#### DATA PREPARATION ####

Hermes = hermes::prepare_data_for_ulises(Integration, FALSE, TRUE)


#### FILES GENERATION ####
HermestoJSON = hermes::to_json(Hermes)
hermes::write_json(HermestoJSON, "HermesData.json")
jsonlite::write_json(RelevantGenes, "RelevantGenes.json")

