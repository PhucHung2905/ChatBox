import os
import json
import re
from pathlib import Path
from typing import List, Dict
import PyPDF2
from docx import Document

class KnowledgeBaseManager:
    """Manages loading and processing documents for the knowledge base"""
    
    @staticmethod
    def load_documents(documents_path: str) -> List[Dict]:
        """
        Load documents from various formats (txt, pdf, docx, json)
        Returns: List of dicts with 'content' and 'metadata'
        """
        documents = []
        
        if not os.path.exists(documents_path):
            print(f"⚠ Documents path not found: {documents_path}")
            return documents
        
        # Load from all supported formats
        txt_docs = KnowledgeBaseManager._load_txt_files(documents_path)
        pdf_docs = KnowledgeBaseManager._load_pdf_files(documents_path)
        docx_docs = KnowledgeBaseManager._load_docx_files(documents_path)
        json_docs = KnowledgeBaseManager._load_json_files(documents_path)
        
        documents.extend(txt_docs)
        documents.extend(pdf_docs)
        documents.extend(docx_docs)
        documents.extend(json_docs)
        
        return documents
    
    @staticmethod
    def _load_txt_files(path: str) -> List[Dict]:
        """Load .txt files"""
        documents = []
        for file in Path(path).glob('**/*.txt'):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.strip():
                        # Split into chunks for better retrieval
                        chunks = KnowledgeBaseManager._split_text(content)
                        for chunk in chunks:
                            documents.append({
                                'content': chunk,
                                'metadata': {
                                    'source': str(file),
                                    'type': 'text'
                                }
                            })
            except Exception as e:
                print(f"Error loading {file}: {e}")
        return documents
    
    @staticmethod
    def _load_pdf_files(path: str) -> List[Dict]:
        """Load .pdf files"""
        documents = []
        for file in Path(path).glob('**/*.pdf'):
            try:
                with open(file, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    text = ''
                    for page in reader.pages:
                        text += page.extract_text() + '\n'
                    
                    if text.strip():
                        chunks = KnowledgeBaseManager._split_text(text)
                        for chunk in chunks:
                            documents.append({
                                'content': chunk,
                                'metadata': {
                                    'source': str(file),
                                    'type': 'pdf'
                                }
                            })
            except Exception as e:
                print(f"Error loading {file}: {e}")
        return documents
    
    @staticmethod
    def _load_docx_files(path: str) -> List[Dict]:
        """Load .docx files"""
        documents = []
        for file in Path(path).glob('**/*.docx'):
            try:
                doc = Document(file)
                text = '\n'.join([para.text for para in doc.paragraphs])
                
                if text.strip():
                    chunks = KnowledgeBaseManager._split_text(text)
                    for chunk in chunks:
                        documents.append({
                            'content': chunk,
                            'metadata': {
                                'source': str(file),
                                'type': 'docx'
                            }
                        })
            except Exception as e:
                print(f"Error loading {file}: {e}")
        return documents
    
    @staticmethod
    def _load_json_files(path: str) -> List[Dict]:
        """Load .json files containing documents"""
        documents = []
        for file in Path(path).glob('**/*.json'):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Handle different JSON structures
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict):
                                content = item.get('content') or item.get('text') or str(item)
                                if content:
                                    chunks = KnowledgeBaseManager._split_text(content)
                                    for chunk in chunks:
                                        documents.append({
                                            'content': chunk,
                                            'metadata': {
                                                'source': str(file),
                                                'type': 'json',
                                                'original': item
                                            }
                                        })
                    elif isinstance(data, dict):
                        content = data.get('content') or data.get('text') or str(data)
                        if content:
                            chunks = KnowledgeBaseManager._split_text(content)
                            for chunk in chunks:
                                documents.append({
                                    'content': chunk,
                                    'metadata': {
                                        'source': str(file),
                                        'type': 'json'
                                    }
                                })
            except Exception as e:
                print(f"Error loading {file}: {e}")
        return documents
    
    @staticmethod
    def _split_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
        """
        Split text into overlapping chunks for better context retrieval
        Args:
            text: Text to split
            chunk_size: Size of each chunk in characters
            overlap: Overlap between chunks
        """
        # Clean text
        text = re.sub(r'\s+', ' ', text).strip()
        
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start = end - overlap
        
        return chunks
