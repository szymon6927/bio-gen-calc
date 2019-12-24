import re
from typing import List
from typing import NamedTuple
from typing import Set
from typing import Union

import requests

from app.mail_scrapper.validators import is_email_valid


class NCBIObject(NamedTuple):
    email: str
    publication_id: str
    publication_url: str


class NCBIPubScrapper:
    def __init__(self):
        self.search_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
        self.fetch_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'

    def get_publication_id_list(self, start_from: int, limit_to: int) -> List[str]:
        """Get all publication ID from NCBI API from provided range"""

        parameters = {'db': 'pubmed', 'term': 'genetics', 'retmode': 'json', 'retstart': start_from, 'retmax': limit_to}

        response = requests.get(url=self.search_url, params=parameters)

        if response.status_code != 200:
            return []

        response_json = response.json()
        publications_id_list = response_json.get('esearchresult').get('idlist')

        return publications_id_list

    def get_publication_content(self, publication_id: str) -> Union[str, None]:
        parameters = {'db': 'pubmed', 'id': publication_id}

        response = requests.get(url=self.fetch_url, params=parameters)

        if response.status_code != 200:
            return None

        return response.content.decode()

    def get_extracted_emails(self, publication_content: str) -> Set[str]:
        regex = re.compile(
            (
                r"([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                r"{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                r"\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"
            )
        )

        content = publication_content.lower()
        parsed_emails = (email[0] for email in re.findall(regex, content) if not email[0].startswith('//'))

        unique_emails = set()

        for parsed_email in parsed_emails:
            if is_email_valid(parsed_email):
                unique_emails.add(parsed_email)

        return unique_emails

    def create_ncbi_object(self, email: str, publication_id: str):
        ncbi_publication_root_url = 'https://www.ncbi.nlm.nih.gov/pubmed/'

        return NCBIObject(
            email=email, publication_id=publication_id, publication_url=f'{ncbi_publication_root_url}{publication_id}'
        )

    def run(self, start_from: int, limit_to: int) -> List[NCBIObject]:
        publication_id_list = self.get_publication_id_list(start_from, limit_to)

        result: List[NCBIObject] = []

        for publication_id in publication_id_list:
            publication_content = self.get_publication_content(publication_id)

            if publication_content:
                emails = self.get_extracted_emails(publication_content)

                ncbi_objects = [self.create_ncbi_object(email, publication_id) for email in emails]
                result.extend(ncbi_objects)

        return result
