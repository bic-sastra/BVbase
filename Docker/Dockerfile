# Step 1: Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Step 2: Set interactive mode
ENV DEBIAN_FRONTEND=interactive

# Step 3: Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    git \
    unzip \
    gcc \
    g++ \
    make \
    perl \
    python3 \
    python3-pip \
    sqlite3 \
    openjdk-21-jdk \
    samtools \
    bcftools \
    vcftools \
    bwa \
    fastp \
    sed \
    gawk \
    coreutils \
    python3-tk \
    libx11-6 \
    libxext6 \
    libxrender1 \
    x11-apps \
    nano \
    gedit \
    && rm -rf /var/lib/apt/lists/*

# Step 4: Ensure `python` points to `python3`
RUN ln -s /usr/bin/python3 /usr/bin/python

# Step 5: Install Python libraries for GUI and web-based interfaces
RUN pip3 install --no-cache-dir pandas flask streamlit matplotlib PyQt5 pymysql

# Step 6: Install SnpEff
RUN mkdir -p /opt/snpeff \
    && cd /opt/snpeff \
    && wget https://snpeff.blob.core.windows.net/versions/snpEff_latest_core.zip \
    && unzip snpEff_latest_core.zip \
    && rm snpEff_latest_core.zip

# Step 7: Set SnpEff environment variables
ENV PATH="/opt/snpeff/snpEff:$PATH"
ENV SNPEFF_HOME="/opt/snpeff/snpEff"

RUN chmod 777 /opt/snpeff/snpEff/snpEff.jar

# Step 8: Create an alias for SnpEff
RUN echo 'alias snpeff="java -jar /opt/snpeff/snpEff/snpEff.jar"' >> ~/.bashrc

# Step 9: Install Nextflow
RUN curl -fsSL https://get.nextflow.io | bash \
    && mv nextflow /usr/local/bin/

# Step 10: Install Prokka
RUN apt-get update && apt-get install -y \
    prokka \
    gffread \
    emboss \
    && rm -rf /var/lib/apt/lists/*

# Step 11: Set up Prokka database
RUN git clone https://github.com/tseemann/prokka.git /opt/prokka_repo && \
    mkdir -p /root/.local/lib/prokka/db && \
    cp -r /opt/prokka_repo/db/* /root/.local/lib/prokka/db/ && \
    prokka --setupdb && \
    rm -rf /opt/prokka_repo  # Cleanup

# Step 12: Verify installations
RUN java -version && python3 --version && nextflow -version

# Set working directory inside the container
WORKDIR /app

# Copy all application files from the host to the container
COPY . /app/

# Step 13: Expose necessary ports (Flask: 5000, Streamlit: 8501)
EXPOSE 5000 8501

# Step 14: Default command
CMD ["python3", "gui.py"]
