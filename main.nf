#!/usr/bin/env nextflow

nextflow.enable.dsl=2

params.ref = '' 
params.fna_read = ""  //fna file
params.read = '' //single end reads files 
params.read1 = ''  //pair end reads files
params.read2 = ''  //pair end reads files 
params.reads = ''  //bulk processing paired end reads files
params.snpEff_db = '' 
params.chr_name=''
params.ref_strain = ''
params.datadir = ''
params.main_db = ''
params.new_db = ''
params.exist_db = ''
params.output_dir = ''
params.qual = '20'  


process indexReference {
    input:
    path reference

    output:
    path "${reference}*"

    script:
    """
    bwa index -p $reference $reference
    """
}

process trim_single_end {
    memory '2 GB'
     maxForks 4
    input:
        path fastq

    output:
        path "${fastq}*"

    script:
        """
        fastp -i $fastq -o ${fastq}_trimmed.fastq.gz
        """
}


process align_single_end {
    memory '2 GB'

 maxForks 2
    input:
        path ref_index
        path fastq
        path reference

    output:
        path "${fastq}*.sam"

    script:
        """
         bwa mem $reference $fastq > ${fastq}.sam
        """
}


process trim_pair_end {
    memory '2 GB'
     maxForks 4

    input:
    tuple path(raw1), path(raw2)
    output:
    tuple path("${raw1}_trimmed.fastq"), path("${raw2}_trimmed.fastq")
    script:
    """
    echo "Trimming raw data. Inputs: ${raw1} and ${raw2} Quality: ${params.qual}"
    fastp -i $raw1 -I $raw2 -o ${raw1}_trimmed.fastq -O ${raw2}_trimmed.fastq -q ${params.qual}
    """
}

process align_pair_end {
    memory '2 GB'
    maxForks 1
    input:
    path ref_index
    tuple path(forward), path(reverse)
    path reference
    
    output:
    path "*.sam"

    script:
        """
    echo "Aligning Reads. Reference: ${reference}"
    bwa mem -p $reference $forward $reverse > ${forward}.sam
        """
}

process alignReads{
memory '2 GB'
 maxForks 4
    input:
        path ref_index
        path fastq
        path reference

    output:
        path "${fastq}*.sam"

    script:
        """
         bwa mem $reference $fastq > ${fastq}.sam
        """
}

process samToBam {
    input:
        path sam
    
    output:
        path "${sam}*.bam"
    
    script:
        """
        samtools view -Sb $sam > ${sam}.bam
        """
}

process sorting {
    input:
        path bam
    
    output:
        path "${bam}*.bam"
    
    script:
        """
        samtools sort $bam -o ${bam}_sorted.bam
        """
}

process duplicatereads {
    input:
        path bam


    output:
        path "${bam}*.bam"

    script:
        """
        samtools markdup $bam ${bam}_dedup.bam
        """
}

process variantCalling {
    memory '3 GB'
    maxForks 4
     publishDir "variant_vcf_file", mode: 'copy'
    input:
        path sorted
        path reference
    
    output:
        path "${sorted}*.vcf"
    
    script:
        """
        bcftools mpileup -Ou -f $reference $sorted | bcftools call -vm -o ${sorted}.vcf
        """
}

process exChromName {
 

    input:
       path vari


    output:
        path "${vari}*.vcf" 

    script:
        """    
        sed 's/^${params.chr_name}/Chromosome/' $vari > ${vari}.vcf
        """
}


process annotation {
    memory '3 GB'
    maxForks 2
    input:
        path annotate

 publishDir './annn/', mode: 'copy'
    output:
        path "${annotate}*.vcf"
    

    script:
        """
          java -jar ${params.datadir}/snpEff.jar -dataDir ${params.datadir}/data -v ${params.snpEff_db} $annotate > ${annotate}.vcf
       """
}

process filterSNPs {


    input:
         path filtter

    output:
        path "${filtter}*.vcf"

    script:
        """
         echo "${filtter}"
    vcftools --gzvcf $filtter --minDP 4 --max-missing 0.2 --minQ 30 --recode --recode-INFO-all --out ${filtter}.vcf
        """
}

process filterNonsymous {
    publishDir "vcf_file/csv", mode: 'copy'

    input:
        path filtered_snps

    publishDir './nonsynonymous_snpsfile/', mode: 'copy'

    output:
        path "${filtered_snps}*.vcf"

    script:
        """
        bcftools filter -i 'INFO/ANN[*] ~ "missense"' $filtered_snps -Oz -o ${filtered_snps}.vcf
        """
}

process vcfToCSV {

    input:
        path finalnon
    
    output:
        path "${finalnon}*.csv"

    script:
        """      
      
        sed 's/^Chromosome/${params.chr_name}/; s/^strain/${params.ref_strain}/' $finalnon > ${finalnon}.vcf

        echo "Chromosome,Position,ID,REF,ALT,QUAL,Allele,Annotation_Type,Annotation_Impact,Gene_Name,Gene_ID,Feature_Type,Feature_ID,BioType,Rank,HGVS_c,HGVS_p,cDNA.pos/cDNA.length,CDS.pos/CDS.length,AA.pos/AA.length,Ref_Strain" > ${finalnon}.csv

        bcftools query -f '%CHROM,%POS,%ID,%REF,%ALT,%QUAL,[%INFO/ANN\n]' ${finalnon}.vcf | 
        awk -F"|" 'BEGIN {OFS=","} {print \$1,\$2,\$3,\$4,\$5,\$6,\$7,\$8,\$9,\$10,\$11,\$12,\$13,\$14,\$15,\$16,\$17}' |
        awk 'BEGIN {FS=","; OFS=","} { \$23=""; \$24=""; \$25=""; print \$1,\$2,\$3,\$4,\$5,\$6,\$7,\$8,\$9,\$10,\$11,\$12,\$13,\$14,\$15,\$16,\$17,\$18,\$19,\$20,"${params.ref_strain}" }' >> ${finalnon}.csv
       """
   
}

process aa_add {

    input:
        path csv_file

    output:
        path "*.csv"

    script:
    """
    cut -d ',' -f 1-21 ${csv_file} | paste -d ',' - <(cut -d ',' -f 17 ${csv_file}) | sed -E '2,\$s/p\\.([A-Za-z]{3})[0-9]+([A-Za-z]{3})/\\1-\\2/' > ${csv_file}.csv   
     """ 
}

process add_aa_name {
     publishDir "./aa_cgk", mode: 'copy'
    input:
        path csv_file

    output:
        path "*.csv"

    script:
        """
        awk -F',' 'NR==1 {\$17="AA_change"} 1' OFS=',' ${csv_file} > ${csv_file}.csv
        """
}


process addGenomeId {
   publishDir "${params.output_dir}/csvdata", mode: 'copy'
    input:
    path csv_file

    output:
       path "processed_dir/*.csv"//   genome_id=$(basename "${csv_file}" | sed -E 's/^([^.]+).*/\1/')
   
    script:
    """
    
    # Extract genome_id from the CSV file name
 
    mkdir -p processed_dir
genome_id=\$(basename "${csv_file}" | sed -E 's/^([0-9]+\\.[0-9]+|SRR[0-9]+|ERR[0-9]+|DRR[0-9]+).*/\\1/')
output_file="processed_dir/\${genome_id}.csv"
# Check if genome_id starts with SRR, ERR, or DRR
if [[ "\$genome_id" =~ ^(SRR|ERR|DRR) ]]; then
    header="SRA Accession"
    awk -F',' -v genome_id="\$genome_id" 'BEGIN {OFS=","} {if (NR==1) print "SRA Accession,Genome ID", \$0; else print genome_id, "", \$0}' "${csv_file}" > "\$output_file"
elif [[ -n "\$genome_id" ]]; then
    header="Genome ID"
    awk -F',' -v genome_id="\$genome_id" 'BEGIN {OFS=","} {if (NR==1) print "SRA Accession,Genome ID", \$0; else print "", genome_id, \$0}' "${csv_file}" > "\$output_file"
else
    echo "No valid genome ID found."
    exit 1
fi

    # Rename the resulting file to clean up the filename      

    """
   
}



process runPythonScript {
    publishDir "./db1_output/", mode: 'copy'
    debug true
    input:
        path db_file

    output:
         path db_file

    script:
    """
#!/usr/bin/env python3
import os
import pandas as pd 
import sqlite3

# Define paths using Nextflow parameters
database_path = '${params.exist_db}' if '${params.exist_db}' else '${params.new_db}/finalbn_database.db'
metadata_path = '${params.main_db}'  # Metadata CSV file
variants_dir = '${params.output_dir}/csvdata/processed_dir' # Directory containing variant CSV files

# Check if the database exists or create a new one
if os.path.exists(database_path):
    print(f\"Updating existing database: {database_path}\")
else:
    print(f\"Creating a new database: {database_path}\")

# Connect to SQLite database
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Create strains table
cursor.execute(\"\"\"
CREATE TABLE IF NOT EXISTS strains (
    genome_id TEXT DEFAULT NULL,           
    sra_accession TEXT DEFAULT NULL,
    isolation_country TEXT,
    geographic_group TEXT,
    taxon_id INTEGER,
    genome_name TEXT,
    antibiotic TEXT,
    resistant_phenotype TEXT,
    PRIMARY KEY (sra_accession, genome_id, antibiotic)
);
\"\"\")

# Create variants table
cursor.execute(\"\"\"
CREATE TABLE IF NOT EXISTS variants (
    genome_id TEXT DEFAULT NULL,
    sra_accession TEXT DEFAULT NULL,
    chromosome TEXT,
    position INTEGER,
    id TEXT,
    ref TEXT,
    alt TEXT,
    qual REAL,
    allele TEXT,
    annotation_type TEXT,
    annotation_impact TEXT,
    gene_name TEXT,
    gene_id TEXT,
    feature_type TEXT,
    feature_id TEXT,
    biotype TEXT,
    rank TEXT,
    hgvs_c TEXT,
    aa_change TEXT,
    cdna_pos_length TEXT,
    cds_pos_length TEXT,
    aa_pos_length TEXT,
    ref_strain TEXT,
    hgvs_p TEXT,
    FOREIGN KEY (sra_accession, genome_id) REFERENCES strains(sra_accession, genome_id)
);
\"\"\")

index_queries = [
    \"CREATE INDEX IF NOT EXISTS idx_isolation_country ON strains (isolation_country);\",
    \"CREATE INDEX IF NOT EXISTS idx_geographic_group ON strains (geographic_group);\",
    \"CREATE INDEX IF NOT EXISTS idx_genome_name ON strains (genome_name);\",
    \"CREATE INDEX IF NOT EXISTS idx_antibiotic ON strains (antibiotic);\",
    \"CREATE INDEX IF NOT EXISTS idx_resistant_phenotype ON strains (resistant_phenotype);\", 
    \"CREATE INDEX IF NOT EXISTS idx_gene_name ON variants (gene_name);\",
    \"CREATE INDEX IF NOT EXISTS idx_country_geo ON strains (isolation_country, geographic_group);\",
    \"CREATE INDEX IF NOT EXISTS idx_gene_strain ON variants (gene_name, genome_id);\",
    \"CREATE INDEX IF NOT EXISTS idx_antibiotic_pheno ON strains (antibiotic, resistant_phenotype);\",
    \"CREATE INDEX IF NOT EXISTS idx_country_geo_full ON strains (isolation_country, geographic_group, antibiotic, resistant_phenotype);\"
    ]

for query in index_queries:
    cursor.execute(query)

print(\"Tables and indexes created successfully.\")

# Load the metadata file
main_data = pd.read_csv(metadata_path, dtype=str)
print(\"Metadata loaded:\")
print(main_data.head())

# Process each CSV file in the directory
for filename in os.listdir(variants_dir):
    if filename.endswith(\".csv\"):
        try:
            print(f\"Processing file: {filename}\")

            # Extract Genome ID or SRA Accession
           
        
          
            # Determine genome_id and sra_accession
            if \"SRR\" in filename or \"ERR\" in filename or \"DRR\" in filename:
                sra_accession = filename.rsplit('.', 1)[0]  # Extract SRA Accession
                genome_id = None
            else:
                genome_id = filename.rsplit('.', 1)[0]  # Extract Genome ID
                sra_accession = None

           

            print(f\"Extracted genome_id: {genome_id}, sra_accession: {sra_accession}\")
            print(f\"Extracted genome_id: {sra_accession}, sra_accession: {genome_id}\")

            cursor.execute(\"\"\"
                SELECT COUNT(*) FROM strains WHERE genome_id = ? OR sra_accession = ?
            \"\"\", (genome_id, sra_accession))
            result = cursor.fetchone()
            if result and result[0] > 0:
                print(f\" Genome ID {genome_id or sra_accession} already exists. Skipping {genome_id or sra_accession} processing.\")
                continue


            # Load CSV data
            genome_data = pd.read_csv(
                os.path.join(variants_dir, filename), on_bad_lines='skip', dtype=str
            )
            print(f\"Data from {filename}:\\n\", genome_data.head())

            # Filter metadata for genome_id or sra_accession
            genome_metadata = main_data[(main_data['Genome ID'].astype(str) == str(genome_id))|(main_data['SRA Accession'].astype(str) == str(sra_accession))]
            if not genome_metadata.empty:
                for _, meta_row in genome_metadata.iterrows():
                    cursor.execute(\"\"\"
                        INSERT OR IGNORE INTO strains (
                            genome_id, sra_accession, isolation_country, geographic_group,
                            taxon_id, genome_name, antibiotic, resistant_phenotype
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    \"\"\", (
                        genome_id,
                        sra_accession,
                        meta_row['Isolation Country'],
                        meta_row['Geographic Group'],
                        meta_row['Taxon ID'],
                        meta_row['Genome Name'],
                        meta_row['Antibiotic'],
                        meta_row['Resistant Phenotype']
                    ))
                print(f\"Inserted strain data for {genome_id or sra_accession}\")

            # Insert rows into variants table
            for _, row in genome_data.iterrows():
                cursor.execute(\"\"\"
                    INSERT INTO variants (
                        genome_id, sra_accession, chromosome, position, id, ref, alt, qual, allele, annotation_type,
                        annotation_impact, gene_name, gene_id, feature_type, feature_id, biotype, rank,
                        hgvs_c, aa_change, cdna_pos_length, cds_pos_length, aa_pos_length, ref_strain, hgvs_p
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                \"\"\", (
                    genome_id,
                    sra_accession,
                    row.get('Chromosome'),
                    row.get('Position'),
                    row.get('ID'),
                    row.get('REF'),
                    row.get('ALT'),
                    row.get('QUAL'),
                    row.get('Allele'),
                    row.get('Annotation_Type'),
                    row.get('Annotation_Impact'),
                    row.get('Gene_Name'),
                    row.get('Gene_ID'),
                    row.get('Feature_Type'),
                    row.get('Feature_ID'),
                    row.get('BioType'),
                    row.get('Rank'),
                    row.get('HGVS_c'),
                    row.get('AA_change'),
                    row.get('cDNA.pos/cDNA.length'),
                    row.get('CDS.pos/CDS.length'),
                    row.get('AA.pos/AA.length'),
                    row.get('Ref_Strain'),
                    row.get('HGVS_p')
                ))
            print(f\"Inserted variant data for: {sra_accession or genome_id}\")

        except Exception as e:
            print(f\"Error processing {filename}: {e}\")

# Commit changes and close the database connection
try:
    conn.commit()
    print(\"Changes committed to the database.\")
finally:
    conn.close()
    print(\"Database connection closed.\")


    """
}

// fna file workflow
workflow fna_run {
    println "Workflow mode: To annotate the variants"
    println "Warning! Only one assembled fasta(reads) file was included. It will be assumed to be a single-end file and not using Trimming Process"
    
    if (params.ref && params.fna_read) {
        println "Reference genome: ${params.ref}"
        def reads_list = params.fna_read.tokenize(' ')  // Handles multiple file paths
        println "Input reads: ${reads_list}"
        reads_channel = Channel.fromPath(reads_list)
        indexReference(params.ref)
        alignReads(indexReference.out, reads_channel, params.ref)
        samToBam(alignReads.out )
        sorting(samToBam.out )
        duplicatereads(sorting.out )
        variantCalling(duplicatereads.out,  params.ref)
        exChromName(variantCalling.out)
        annotation(exChromName.out)
        filterSNPs(annotation.out)
        filterNonsymous(filterSNPs.out)
        vcfToCSV(filterNonsymous.out)
        aa_add(vcfToCSV.out)
        add_aa_name(aa_add.out)
        addGenomeId(add_aa_name.out)
        addGenomeId.out.collectFile(name: 'collected_csv_files').set { collected_csv_files }
        runPythonScript(collected_csv_files)
        
    } else {
        error "Please provide valid paths for the reference genome and input reads."
    }
}

//fastq file  workflow single end reads

workflow single_end_run{
    println "Workflow mode: To annotate the variants"
    println "Warning! Only one reads file was included. It will be assumed to be a single end file"
    def reads_list = params.read.tokenize(' ')  // Handles multiple file paths
    println "Input reads: ${reads_list}"
    reads_channel = Channel.fromPath(reads_list)
    indexReference(params.ref)
    trim_single_end(reads_channel)
    align_single_end(indexReference.out,params.read, params.ref)
    samToBam(align_single_end.out )
    sorting(samToBam.out )
    duplicatereads(sorting.out )
    variantCalling(duplicatereads.out,  params.ref)
    exChromName(variantCalling.out)
    annotation(exChromName.out)
    filterSNPs(annotation.out)
    filterNonsymous(filterSNPs.out)
    vcfToCSV(filterNonsymous.out)
    aa_add(vcfToCSV.out)
    add_aa_name(aa_add.out)
    addGenomeId(add_aa_name.out)
    addGenomeId.out.collectFile(name: 'collected_csv_files').set { collected_csv_files }
    runPythonScript(collected_csv_files)
    
    }


//fastq file  workflow pair end reads

workflow pair_end_run{
    println "Workflow mode: To annotate the variants and bulk processing paired-end reads and single file paired-end reads"
    indexReference(params.ref)
    if (params.read1 != "" && params.read2 != "") {
            def paired_reads_channel = tuple(params.read1, params.read2)
            trim_pair_end(paired_reads_channel)
    }
    else {
        paired_reads_channel = Channel.fromFilePairs("${params.reads}")
        paired_reads_channel = paired_reads_channel.map { pair -> [pair[1][0], pair[1][1]] }
        trim_pair_end(paired_reads_channel)
    }
    align_pair_end(indexReference.out, trim_pair_end.out,params.ref)
    samToBam(align_pair_end.out )
    sorting(samToBam.out )
    duplicatereads(sorting.out )
    variantCalling(duplicatereads.out,  params.ref)
    exChromName(variantCalling.out)
    annotation(exChromName.out)
    filterSNPs(annotation.out)
    filterNonsymous(filterSNPs.out)
    vcfToCSV(filterNonsymous.out)
    aa_add(vcfToCSV.out)
    add_aa_name(aa_add.out)
    addGenomeId(add_aa_name.out)
    addGenomeId.out.collectFile(name: 'collected_csv_files').set { collected_csv_files }
    runPythonScript(collected_csv_files)
    
    }



workflow bulk_pair_end_run {
    println "Workflow mode: To annotate the variants and bulk processing paired-end reads"
    indexReference(params.ref)
    paired_reads_channel = Channel.fromFilePairs("${params.reads}")
    paired_reads_channel = paired_reads_channel.map { pair -> [pair[1][0], pair[1][1]] }
    trim_pair_end(paired_reads_channel)
    align_pair_end(indexReference.out, trim_pair_end.out, params.ref)
    samToBam(align_pair_end.out)
    sorting(samToBam.out)
    duplicatereads(sorting.out)
    variantCalling(duplicatereads.out, params.ref)
    exChromName(variantCalling.out)
    annotation(exChromName.out)
    filterSNPs(annotation.out)
    filterNonsymous(filterSNPs.out)
    vcfToCSV(filterNonsymous.out)
    aa_add(vcfToCSV.out)
    add_aa_name(aa_add.out)
    addGenomeId(add_aa_name.out)
    addGenomeId.out.collectFile(name: 'collected_csv_files').set { collected_csv_files }
    runPythonScript(collected_csv_files)
}

workflow all_in_one_run {
    println "Workflow mode: To annotate the variants from fna, single-end, and paired-end reads"

    // Index the reference genome
    indexReference(params.ref)

    // Initialize channels for collecting outputs
    collected_align_reads = Channel.empty()
    collected_align_single_end = Channel.empty()
    collected_align_pair_end = Channel.empty()

    // Process fna file
    if (params.fna_read) {
        def reads_list = params.fna_read.tokenize(' ')  // Handles multiple file paths
        println "Input reads: ${reads_list}"
        reads_channel = Channel.fromPath(reads_list)
        alignReads(indexReference.out, reads_channel, params.ref)
        alignReads.out.collectFile().set { collected_align_reads }
    }

    // Process single-end reads
    if (params.read) {
        def reads_list = params.reads.tokenize(' ')  // Handles multiple file paths
        println "Input reads: ${reads_list}"
        input_channel = Channel.fromPath(reads_list)
        trim_single_end(input_channel)
        align_single_end(indexReference.out, params.read, params.ref)
        align_single_end.out.collectFile().set { collected_align_single_end }
    }

    // Process paired-end reads
    if (params.read1 && params.read2) {
        println "Processing paired-end reads"
        def paired_reads_channel = tuple(params.read1, params.read2)
        trim_pair_end(paired_reads_channel)
        align_pair_end(indexReference.out, trim_pair_end.out, params.ref)
        align_pair_end.out.collectFile().set { collected_align_pair_end }
    }

    // Process bulk paired-end reads
    if (params.reads) {
        println "Processing bulk paired-end reads from directory: ${params.reads}"
        paired_reads_channel = Channel.fromFilePairs("${params.reads}")
        paired_reads_channel = paired_reads_channel.map { pair -> [pair[1][0], pair[1][1]] }
        trim_pair_end(paired_reads_channel)
        align_pair_end(indexReference.out, trim_pair_end.out, params.ref)
        align_pair_end.out.collectFile().set { collected_align_pair_end }
    }

    // Merge the collected outputs into a single channel
merged_alignments = Channel.empty()
    if (collected_align_reads) {
        merged_alignments = merged_alignments.mix(collected_align_reads)
    }
    if (collected_align_single_end) {
        merged_alignments = merged_alignments.mix(collected_align_single_end)
    }
    if (collected_align_pair_end) {
        merged_alignments = merged_alignments.mix(collected_align_pair_end)
    }
    // Continue with the downstream processes using the merged alignments
    samToBam(merged_alignments)
    sorting(samToBam.out)
    duplicatereads(sorting.out)
    variantCalling(duplicatereads.out, params.ref)
    exChromName(variantCalling.out)
    annotation(exChromName.out)
    filterSNPs(annotation.out)
    filterNonsymous(filterSNPs.out)
    vcfToCSV(filterNonsymous.out)
    aa_add(vcfToCSV.out)
    add_aa_name(aa_add.out)
    addGenomeId(add_aa_name.out)
    addGenomeId.out.collectFile(name: 'collected_csv_files').set { collected_csv_files }
    runPythonScript(collected_csv_files)
}

// Main workflow
workflow {
    if (params.fna_read && !params.read && !params.read1 && !params.read2 && !params.reads) {
        fna_run()
    } else if (params.read && !params.read1 && !params.read2 && !params.fna_read && !params.reads) {
        single_end_run()
    } else if ((params.read1 && params.read2) && !params.reads && !params.fna_read && !params.read) {
        pair_end_run()
    } else if (params.reads && !params.fna_read && !params.read && !params.read1 && !params.read2) {
        bulk_pair_end_run()
    } else if (params.fna_read || params.read || (params.read1 && params.read2) || params.reads) {
        all_in_one_run()
    } else {
        error "Please provide valid paths for the reference genome and input reads."
    }
}

