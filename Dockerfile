# Gunakan Python versi 3.10
FROM python:3.10

# Tentukan folder kerja di dalam container
WORKDIR /code

# Tambahkan folder /code ke dalam PYTHONPATH agar Python bisa menemukan modul 'backend'
ENV PYTHONPATH=/code

# Copy file requirements dulu agar proses install library lebih cepat (cached)
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Download data NLTK yang dibutuhkan oleh intent_classifier.py
RUN python -m nltk.downloader stopwords wordnet omw-1.4

# Copy seluruh isi proyek ke dalam folder /code di container
COPY . .

# Berikan izin akses (read/write) agar NLTK bisa menulis data jika diperlukan
RUN chmod -R 777 /code

# Jalankan FastAPI menggunakan uvicorn di port 7860
# Gunakan format backend.main:app karena file main.py ada di dalam folder backend/
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]