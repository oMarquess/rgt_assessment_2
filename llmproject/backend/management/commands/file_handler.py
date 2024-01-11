from django.core.management.base import BaseCommand, CommandError
from langchain.document_loaders import PyPDFLoader, CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from tqdm import tqdm
import os

class Command(BaseCommand):
    help = 'Loads, splits, embeds, and stores PDF or CSV documents in Chroma database'

    def add_arguments(self, parser):
        # Positional argument for the file path
        parser.add_argument('file_path', type=str, help='Path to the PDF or CSV file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        file_extension = os.path.splitext(file_path)[1].lower()

        # Check if the file is PDF or CSV
        if file_extension not in ['.pdf', '.csv']:
            raise CommandError('Error: Only PDF or CSV files are supported.')

        try:
            # Load PDF or CSV
            if file_extension == '.pdf':
                loaders = [PyPDFLoader(file_path)]
            else:  # CSV
                loaders = [CSVLoader(file_path)]
            
            docs = [doc for loader in tqdm(loaders, desc=f'Loading {file_extension.upper()}s') for doc in loader.load()]

            # Split text with progress bar (if applicable)
            additional_message = ''
            if file_extension == '.pdf':
                text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
                docs = [doc for doc in tqdm(text_splitter.split_documents(docs), desc='Splitting Text')]
                additional_message = 'split, '

            # Create the embedding function
            embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

            # Load into Chroma with a persistent directory
            db = Chroma.from_documents(docs, embedding_function, ids=None, collection_name="Initialfiles", persist_directory="./chroma_db")

            self.stdout.write(self.style.SUCCESS(f'Successfully loaded, {additional_message}embedded, and stored documents in Chroma DB from {file_path}'))

        except Exception as e:
            raise CommandError(f'Error: {e}')
