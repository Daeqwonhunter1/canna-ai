import httpx
from bs4 import BeautifulSoup

from app.scraper.models import ScrapedProfile

USER_AGENT = "canna-ai-research-bot/0.1 (personal project, low volume, contact: you@example.com)"
class LeaflyScraper:

    def __init__(self):
        self.client = httpx.Client(
            headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"},
            timeout=30,
            follow_redirects=True,
        )

    def get_strain(
        self,
        strain_slug: str,
    ) -> ScrapedProfile | None:

        url = (
            f"https://www.leafly.com/"
            f"strains/{strain_slug}"
        )

        response = self.client.get(url)

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "lxml",
        )

        return self.parse_strain(
            soup=soup,
            source_url=url,
        )

    def base_soup(self,soup,element,class_name):
        atrr = soup.find('body').find('main').find('section').find(element, class_=class_name)
        return atrr

    def replace_text(self,*args):
        effects_list = []
        for effect in args:
            print(effect.replace("Loading...", "").strip())
            effects_list.append(effect.replace("Loading...", "").strip())

        return effects_list

    def extract_name(self,soup):
        name = self.base_soup(soup,'h1','heading--l')
        print(name.text)
        return name.text.replace("strain", "").strip()

    def extract_thc(self,soup):
        # thc = self.base_soup(soup,'span','text-xs font-bold pt-px pl-2 border border-transparent')
        thc = soup.find('body').find('main').find('section').find('span',
                                                                  class_='text-xs font-bold pt-px pl-2 border border-transparent',
                                                                  attrs={'data-testid': 'THC'})
        print(thc.text)
        return float("".join(filter(str.isdigit, thc.text)))

    def extract_terpenes(self,soup):
        terps = soup.find('body').find('main').find('section').find('div', class_='mb-sm text-xs').find('div', class_='block font-bold underline mb-sm')

        terp_list = []
        for terp in terps.next_siblings:
            terp_list.append(terp.text)
            print(terp.text)

        return terp_list

    def extract_effects(self,soup):
        effects = soup.find('body').find('main').find('section').find('div', class_='mr-[24px] text-xs font-bold').find('div', class_='block font-bold underline mb-md')
        effects1 = effects.next_sibling.text
        effects2 = effects.next_sibling.next_sibling.text
        effects3 = effects.next_sibling.next_sibling.next_sibling.text

        return self.replace_text(effects1,effects2,effects3)

    def extract_flavors(self,soup):
        flavors = soup.find('body').find('main').find('section').find('div', class_='text-xs font-bold').find('div', class_='block font-bold underline mb-md')
        flavors1 = flavors.next_sibling.text
        flavors2 = flavors.next_sibling.next_sibling.text
        flavors3 = flavors.next_sibling.next_sibling.next_sibling.text

        return self.replace_text(flavors1,flavors2,flavors3)

    def extract_description(self,soup):
        desc = soup.find('body').find('main').find('section').find('div', class_='mt-lg mb-xxl').find('p')
        print(desc.text)
        return desc.text

    def extract_type(self,soup):
        strain_type = self.base_soup(soup,'span', 'inline-block text-xs px-sm rounded font-bold text-default bg-leafly-white')
        print(strain_type.text)
        return strain_type.text

    def extract_cbd(self,soup):
        cbd = soup.find('body').find('main').find('section').find('span', class_='text-xs font-bold pt-px pl-2 border border-transparent', attrs={'data-testid': 'CBD'})
        # cbd = self.base_soup(soup, 'span', 'text-xs font-bold pt-px pl-2 border border-transparent').select_one('[data-testid="CBD"]')
        print(cbd.text)
        return float("".join(filter(str.isdigit, cbd.text)))

    def parse_strain(
        self,
        soup: BeautifulSoup,
        source_url: str,
    ) -> ScrapedProfile:

        return ScrapedProfile(
            strain_name=self.extract_name(soup),
            strain_type=self.extract_type(soup),
            thc_pct_typical=self.extract_thc(soup),
            cbd_pct_typical=self.extract_cbd(soup),
            terpenes=self.extract_terpenes(soup),
            top_effects=self.extract_effects(soup),
            top_flavors=self.extract_flavors(soup),
            description=self.extract_description(soup),
            source_name="leafly",
            source_url=source_url,
        )