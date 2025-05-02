**Pa_var_db**

Introduction:

Antimicrobial resistance (AMR) is one of the top global health threats, as stated by the World
Health Organization (WHO). It leads to resistance against antibiotics, making infections harder
to treat. Pseudomonas aeruginosa is a major concern in AMR due to its resistance, which makes
treating infections such as bloodstream infections and respiratory system infections more
challenging.

To address this issue, there is a need for a variant database that aids in clinical studies, and
therapeutic research. This tool is designed to create a variant database using FASTA, FASTQ,
and metadata CSV files. It generates VCF, CSV, and database (DB) files as output and provides a
web interface for analysis.

Follow the user manual to download, install, and run this tool for study purposes.

Includes:

   ** Dockerfile**
   
   ** main.nf**
   
   ** User manual**
   
   ** snpEff **

   ** sqlite **  # Streamlit for Visualization 
   
This tool is currently supported both Linux-based and Windows-based systems.

SnpEff Database:

 The preloaded SnpEff database is available only for Pseudomonas aeruginosa.Download the files and save them in a single directory.
 If users require a database for any other species, they need to create a new SnpEff database manually.

 Directory schema:

project-root/

├── Docker/
    ├── gui.py
    ├── Docker file

├── Streamlit/

├── files/
    ├── sample1.fastq
    
    ├── reference.fasta
    
    ├── main.nf      
    
    ├── snpEff/   
    └── snpEff.config    
    └── snpEff.jar
    └── data/
        └──Pseudomonas aeruginosa /      
           ├── cds.fa                    
           ├── protein.fa                    
           ├── genes.gff                 
           ├── sequences.fa                    
           ├── sequences.fa.fai
           ├── snpEffectPredictor.bin
           ├── genes.gtf.bak
           └── genes.gtf
├── output/

└── usage_manual.pdf # User Manual

    
Future Development:

**     Large Language model integration.**

The next version will be released soon.
