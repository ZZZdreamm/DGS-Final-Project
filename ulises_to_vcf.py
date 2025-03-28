import json
import datetime


def generate_vcf_from_json(json_file, output_file):
    """
    Genera un archivo VCF a partir de un archivo JSON con variantes genéticas
    usando solo coordenadas GRCh37 e información específica de fenotipo.

    Args:
        json_file (str): Ruta al archivo JSON con información de variantes
        output_file (str): Nombre del archivo VCF de salida
    """
    # Load JSON data
    with open(json_file, 'r') as f:
        variants_data = json.load(f)

    # Create VCF
    with open(output_file, "w") as vcf:
        # Create Header VCF
        current_date = datetime.datetime.now().strftime("%Y%m%d")
        vcf.write("##fileformat=VCFv4.2\n")
        vcf.write(f"##fileDate={current_date}\n")
        vcf.write("##source=ScriptPython\n")
        vcf.write("##reference=GRCh37\n")

        # Create Metadata for INFO
        vcf.write('##INFO=<ID=PHENOTYPE,Number=.,Type=String,Description="Disease phenotype">\n')
        vcf.write('##INFO=<ID=INTERPRETATION,Number=.,Type=String,Description="Variant interpretation">\n')
        vcf.write('##INFO=<ID=INTERPRETATION_REASON,Number=.,Type=String,Description="Reason for interpretation">\n')
        vcf.write('##INFO=<ID=CLINICAL_ACTIONABILITY,Number=.,Type=String,Description="Clinical actionability">\n')
        vcf.write('##INFO=<ID=GENE,Number=.,Type=String,Description="Gene symbol">\n')
        vcf.write('##INFO=<ID=VARIANT_ID,Number=1,Type=String,Description="Variant identifier">\n')

        # Write Mandatory Columns for VCF
        vcf.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")

        # Process each variant
        for variant in variants_data:
            # Extract positional info for GRCh37 assembly
            grch37_info = None
            for assembly in variant["assemblies"]:
                if assembly["assembly"] == "GRCh37":
                    grch37_info = assembly
                    break

            if not grch37_info:
                continue  # Drop the variant if not GRCh37 position is available

            # Prepare information for each phenotype
            for phenotype_info in variant["phenotypes"]:
                # Prepare information for INFO filed
                info_parts = [
                    f"PHENOTYPE={phenotype_info['phenotype']}",
                    f"INTERPRETATION={phenotype_info['classification']['value']}",
                    f"INTERPRETATION_REASON={phenotype_info['classification']['reason']}",
                    f"CLINICAL_ACTIONABILITY={phenotype_info['clinical_actionability']}",
                    f"GENE={','.join(variant['genes'])}",
                    f"VARIANT_ID={variant['variant_id']}"
                ]
                info_field = ";".join(info_parts)

                # Write each variant line
                vcf.write(f"{grch37_info['chromosome']}\t{grch37_info['start']}\t{variant['variant_id']}\t"
                          f"{grch37_info['ref']}\t{grch37_info['alt']}\t.\tPASS\t{info_field}\n")


# Run script
if __name__ == "__main__":
    generate_vcf_from_json("path_to_ulises_file", "path_for_storage/variants_ulises.vcf")