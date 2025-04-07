import psycopg2
import vcfpy

DB_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5332"
}

variants_vcf_file = "variants_ulises.vcf"
patients_vcf_file = "patient_vcf_file.vcf"

def setup_database():
    query = """
    CREATE TABLE IF NOT EXISTS variants_delfos (
        id SERIAL PRIMARY KEY,
        position INT,
        chromosome VARCHAR(10000),
        reference VARCHAR(10000),
        alternate VARCHAR(10000),
        quality FLOAT,
        filter VARCHAR(10000),
        info TEXT
    );
    """

    query2 = """
    CREATE TABLE IF NOT EXISTS variants_patients (
        id SERIAL PRIMARY KEY,
        position INT,
        chromosome VARCHAR(10000),
        reference VARCHAR(10000),
        alternate VARCHAR(10000),
        quality FLOAT,
        filter VARCHAR(10000),
        info TEXT
    );
    """
    try:
        with psycopg2.connect(**DB_PARAMS) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                cur.execute(query2)
                conn.commit()
    except Exception as e:
        print("Database insertion error:", e)
        

def insert_variant(table, chrom, pos, ref, alt, qual, fltr, info):
    query = f"""
    INSERT INTO {table} (chromosome, position, reference, alternate, quality, filter, info)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    try:
        with psycopg2.connect(**DB_PARAMS) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (chrom, pos, ref, alt, qual, fltr, info))
    except Exception as e:
        print(f"Database insertion error for table {table}: {e}")

def process_vcf(vcf_file):
    reader = vcfpy.Reader.from_path(vcf_file)

    while True:
        try:
            record = next(reader)
            chrom = record.CHROM
            pos = record.POS if record.POS is not None else 1
            ref = record.REF
            alt = ";".join(str(a) for a in record.ALT)
            qual = record.QUAL
            fltr = ";".join(record.FILTER) if record.FILTER else "PASS"
            info = str(record.INFO)

            if vcf_file == variants_vcf_file:
                table = "variants_delfos"
            else:
                table = "variants_patients"
            insert_variant(table, chrom, pos, ref, alt, qual, fltr, info)

        except StopIteration:
            break
        except ValueError as _:
            continue

def comparison_algorithm():
    query = """
            SELECT 
    json_array_elements_text(REPLACE(d.info, '''', '"')::json -> 'PHENOTYPE') AS phenotype,
    json_array_elements_text(REPLACE(d.info, '''', '"')::json -> 'CLINICAL_ACTIONABILITY') AS clinical_actionability,
    json_array_elements_text(REPLACE(d.info, '''', '"')::json -> 'INTERPRETATION') AS interpretation
        FROM  
        variants_delfos d
        JOIN 
            variants_patients p 
        ON 
            d.chromosome = SUBSTRING(p.chromosome FROM 4) AND
            d.position = p.position AND
            d.reference = p.reference AND
            d.alternate = p.alternate;
        """
    # Execute query
    try:
        with psycopg2.connect(**DB_PARAMS) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                results = cur.fetchall()
                print("Number of matches: ", len(results))
                for row in results:
                    print()
                    print("Phenotype associated: ", row[0], ", Clinical actionability: ", row[1], ", Interpretation: ", row[2])
    except Exception as e:
        print("Database query error:", e)

def drop_tables():
    query1 = "DROP TABLE IF EXISTS variants_delfos;"
    query2 = "DROP TABLE IF EXISTS variants_patients;"

    try:
        with psycopg2.connect(**DB_PARAMS) as conn:
            with conn.cursor() as cur:
                # Execute both queries to drop the tables if they exist
                cur.execute(query1)
                cur.execute(query2)
                conn.commit()
                print("Tables dropped successfully.")
    except Exception as e:
        print("Error while dropping tables:", e)


if __name__ == "__main__":
    setup_database()
    process_vcf(variants_vcf_file)
    process_vcf(patients_vcf_file)
    comparison_algorithm()