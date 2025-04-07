import psycopg2
import vcfpy

DB_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5332"
}

def setup_database():
    query = """
    CREATE TABLE IF NOT EXISTS variants_delfos (
        id SERIAL PRIMARY KEY,
        chromosome VARCHAR(255),
        position INT,
        reference VARCHAR(255),
        alternate VARCHAR(255),
        quality FLOAT,
        filter VARCHAR(255),
        info TEXT
    );
    """
    try:
        with psycopg2.connect(**DB_PARAMS) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()
    except Exception as e:
        print("Database insertion error:", e)

def insert_variant(chrom, pos, ref, alt, qual, fltr, info):
    query = """
    INSERT INTO variants_delfos (chromosome, position, reference, alternate, quality, filter, info)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    try:
        with psycopg2.connect(**DB_PARAMS) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (chrom, pos, ref, alt, qual, fltr, info))
    except Exception as e:
        print("Database insertion error:", e)

def process_vcf(vcf_file):
    setup_database()
    reader = vcfpy.Reader.from_path(vcf_file)
    for record in reader:
        chrom = record.CHROM
        pos = record.POS if record.POS is not None else 1
        ref = record.REF
        alt = ",".join(str(a) for a in record.ALT)
        qual = record.QUAL
        fltr = ",".join(record.FILTER) if record.FILTER else "PASS"
        info = str(record.INFO)

        insert_variant(chrom, pos, ref, alt, qual, fltr, info)

# Run the process
vcf_file = "variants_ulises.vcf"
process_vcf(vcf_file)