FROM kalilinux/kali-rolling

ENV DEBIAN_FRONTEND=noninteractive

# Force official Kali mirror to avoid broken ones
RUN echo "deb http://http.kali.org/kali kali-rolling main contrib non-free non-free-firmware" > /etc/apt/sources.list

# Ensure proper DNS resolution (fixes network issues inside Docker)
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf

# Install system dependencies with --fix-missing to retry failed downloads
RUN apt-get update --fix-missing && apt-get upgrade -y && apt-get install -y \
    curl dnsutils wget nmap sqlmap autopsy john vim python3-pip git python-is-python3 \
    zaproxy docker.io && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install zaproxy (with break-system-packages to avoid pip errors)
RUN pip install --break-system-packages zaproxy

# Install Google Chrome (fixed version)
WORKDIR /home/
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /root/

# Install RustScan
RUN wget https://github.com/RustScan/RustScan/releases/download/2.2.2/rustscan_2.2.2_amd64.deb \
    && dpkg -i rustscan_2.2.2_amd64.deb \
    && rm rustscan_2.2.2_amd64.deb \
    && apt-get install -y iputils-ping

# Install Nettacker (without removing critical dependencies)
RUN mkdir /opt/nettacker \
    && git clone https://github.com/OWASP/Nettacker.git /opt/nettacker \
    && apt-get install --reinstall -y python3-cryptography \
    && pip3 install --break-system-packages -r /opt/nettacker/requirements.txt \
    && chmod +x /opt/nettacker/nettacker.py \
    && ln -s /opt/nettacker/nettacker.py /usr/local/bin/nettacker

# Copy project files
COPY . /root/

# Install project's Python dependencies
RUN pip3 install --break-system-packages --default-timeout=1000 --no-cache-dir --use-deprecated=legacy-resolver -r /root/requirements.txt

WORKDIR /root/tars/

# Expose the necessary port
EXPOSE 8501

# Entry point for the container
ENTRYPOINT ["/bin/bash", "-c", "source /root/.env && exec streamlit run /root/frontend/main.py --server.port=8501 --server.address=0.0.0.0"]
