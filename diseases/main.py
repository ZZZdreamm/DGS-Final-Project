DB_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

def insert_variant(chrom, pos, ref, alt, qual, fltr, info):
    query = """
    INSERT INTO variants (chromosome, position, reference, alternate, quality, filter, info)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    try:
        with psycopg2.connect(**DB_PARAMS) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (chrom, pos, ref, alt, qual, fltr, info))
    except Exception as e:
        print("Database insertion error:", e)

# Parse VCF file and insert variants into PostgreSQL
def process_vcf(vcf_file):
    reader = vcfpy.Reader.from_path(vcf_file)
    for record in reader:
        chrom = record.CHROM
        pos = record.POS
        ref = record.REF
        alt = ",".join(str(a) for a in record.ALT)  # Join multiple ALT values
        qual = record.QUAL
        fltr = ",".join(record.FILTER) if record.FILTER else "PASS"
        info = str(record.INFO)  # Store INFO as a JSON-like string

        insert_variant(chrom, pos, ref, alt, qual, fltr, info)

# Run the process
vcf_file = "variants.vcf"  # Replace with your VCF file path
process_vcf(vcf_file)