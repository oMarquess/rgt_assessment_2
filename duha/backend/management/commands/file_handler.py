from django.core.management.base import BaseCommand, CommandError
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from tqdm import tqdm
import os

class Command(BaseCommand):
    help = 'Process PDF and CSV documents'

    def add_arguments(self, parser):
        parser.add_argument('file_paths', nargs='+', type=str, help='Paths to the PDF or CSV files')

    def handle(self, *args, **options):
        for file_path in options['file_paths']:
            # Determine file type and choose the appropriate loader
            file_extension = os.path.splitext(file_path)[1].lower()
            if file_extension == '.pdf':
                loader = PyPDFLoader(file_path)
            elif file_extension == '.csv':
                loader = CSVLoader(file_path)
            else:
                raise CommandError(f"Unsupported file type for {file_path}")

            # Load documents with a progress bar
            self.stdout.write(f"Loading documents from {file_path}...")
            docs = [doc for doc in tqdm(loader.load(), desc='Loading')]

            # Split documents with a progress bar
            self.stdout.write("Splitting documents...")
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=5)
            docs = [doc for doc in tqdm(text_splitter.split_documents(docs), desc='Splitting')]

            # Embedding process
            self.stdout.write("Embedding documents...")
            embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            # Load into Chroma with a persistent directory
            db = Chroma.from_documents(docs, embedding_function, ids=None, collection_name="langchain", persist_directory="./chroma_db")
            
            self.stdout.write(self.style.SUCCESS(f'Successfully processed and embedded documents from {file_path}'))
