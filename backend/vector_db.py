import os
import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss

class VectorDatabase:
    """Manages vector embeddings and similarity search"""
    
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.embeddings = []
        self.documents = []
        self.index = None
        self.metadata = []
        
    def add_documents(self, documents):
        """
        Add documents to the vector database
        Args:
            documents: List of dicts with 'content' and 'metadata' keys
        """
        print(f"Embedding {len(documents)} documents...")
        
        for doc in documents:
            content = doc.get('content', '')
            if content:
                embedding = self.model.encode(content, convert_to_numpy=True)
                self.embeddings.append(embedding)
                self.documents.append(content)
                self.metadata.append(doc.get('metadata', {}))
        
        # Build FAISS index
        if self.embeddings:
            embeddings_array = np.array(self.embeddings).astype('float32')
            self.index = faiss.IndexFlatL2(embeddings_array.shape[1])
            self.index.add(embeddings_array)
            print(f"✓ Added {len(self.embeddings)} documents to vector database")
    
    def search(self, query, k=5):
        """
        Search for similar documents
        Args:
            query: Search query string
            k: Number of results to return
        Returns:
            List of dicts with 'content', 'metadata', and 'score'
        """
        if self.index is None or len(self.documents) == 0:
            return []
        
        query_embedding = self.model.encode(query, convert_to_numpy=True)
        query_embedding = np.array([query_embedding]).astype('float32')
        
        distances, indices = self.index.search(query_embedding, min(k, len(self.documents)))
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.documents):
                results.append({
                    'content': self.documents[int(idx)],
                    'metadata': self.metadata[int(idx)],
                    'score': float(1 / (1 + distance))  # Convert distance to similarity
                })
        
        return results
    
    def save(self, path):
        """Save vector database to disk"""
        os.makedirs(path, exist_ok=True)
        
        if self.index:
            faiss.write_index(self.index, os.path.join(path, 'index.faiss'))
        
        with open(os.path.join(path, 'documents.json'), 'w', encoding='utf-8') as f:
            json.dump({
                'documents': self.documents,
                'metadata': self.metadata
            }, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Vector database saved to {path}")
    
    def load(self, path):
        """Load vector database from disk"""
        if os.path.exists(os.path.join(path, 'index.faiss')):
            self.index = faiss.read_index(os.path.join(path, 'index.faiss'))
        
        if os.path.exists(os.path.join(path, 'documents.json')):
            with open(os.path.join(path, 'documents.json'), 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.documents = data['documents']
                self.metadata = data['metadata']
        
        print(f"✓ Vector database loaded from {path}")
