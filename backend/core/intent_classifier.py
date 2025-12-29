import joblib
import os
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# Mengatur agar NLTK mencari data di folder lokal jika di server cloud
# Ini mencegah error 'permission denied' di beberapa server deploy
nltk_data_path = os.path.join(os.path.expanduser("~"), "nltk_data")
if nltk_data_path not in nltk.data.path:
    nltk.data.path.append(nltk_data_path)

# Pastikan resource NLTK tersedia
try:
    nltk.download("stopwords", quiet=True)
    nltk.download("wordnet", quiet=True)
    nltk.download("omw-1.4", quiet=True)
except Exception as e:
    print(f"⚠️ NLTK Download Warning: {e}")

class IntentClassifier:
    def __init__(self):
        # Mendapatkan path absolut ke folder 'UAS' agar tidak salah lokasi
        # __file__ adalah posisi intent_classifier.py
        # path ini akan mundur 2 tingkat ke folder utama
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Lokasi model (Sesuaikan dengan folder 'model' Anda)
        self.model_path = os.path.join(base_dir, "model", "intent_model.pkl")
        self.vectorizer_path = os.path.join(base_dir, "model", "tfidf_vectorizer.pkl")
        
        # Load model dan vectorizer
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.vectorizer_path):
                self.model = joblib.load(self.model_path)
                self.vectorizer = joblib.load(self.vectorizer_path)
                print(f"✅ Intent Classifier loaded successfully from: {self.model_path}")
            else:
                print(f"❌ File model tidak ditemukan di: {self.model_path}")
                self.model = None
                self.vectorizer = None
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model = None

        self.lemmatizer = WordNetLemmatizer()
        try:
            self.stop_words = set(stopwords.words("english"))
        except:
            self.stop_words = set()

    def _preprocess(self, text):
        """Membersihkan teks input user sebelum diprediksi"""
        if not text:
            return ""
        # Menghapus karakter selain huruf dan mengubah ke lowercase
        text = re.sub(r"[^a-z\s]", "", text.lower())
        # Tokenisasi, Lemmatization, dan Hapus Stopwords
        tokens = [self.lemmatizer.lemmatize(w) for w in text.split() if w not in self.stop_words]
        return " ".join(tokens)

    def predict(self, user_input):
        """Menebak intent dari input user"""
        if self.model is None or self.vectorizer is None:
            return "unknown"
        
        try:
            cleaned_text = self._preprocess(user_input)
            # Jika hasil preprocess kosong, kembalikan unknown
            if not cleaned_text.strip():
                return "unknown"
                
            vectorized_text = self.vectorizer.transform([cleaned_text])
            prediction = self.model.predict(vectorized_text)
            
            return prediction[0]
        except Exception as e:
            print(f"⚠️ Prediction Error: {e}")
            return "unknown"

# Inisialisasi instance untuk digunakan di file lain
classifier = IntentClassifier()