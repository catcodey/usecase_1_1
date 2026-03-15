import re
import nltk
from nltk.corpus import stopwords

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def clean_text(text):
    if not text: return ""
    text = re.sub(r'[^a-zA-Z0-9\s\.\?\!]', '', text).lower()
    stop_words = set(stopwords.words('english'))
    fillers = {'um', 'uh', 'ah', 'er', 'basically', 'actually', 'you know', 'sort of', 'like'}
    words = text.split()
    return " ".join([w for w in words if w not in stop_words and w not in fillers]).strip()



