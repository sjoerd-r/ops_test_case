De volgende codebase is een geminimaliseerde replica van één van onze APIs, ontworpen voor het beheren van het magazijn. De nadruk van de opdracht ligt op het begrijpen van de bestaande structuur, het verbeteren van de opzet en het realiseren van de werkendheid.

Begin met het pullen van de codebase en het installeren van de benodigde dependencies.

De eerste stap is het herorganiseren van de codebase. De huidige structuur is vrij diep genest en kan overzichtelijker. Richt de mappen en modules zo in dat de opzet logisch is en aansluit bij gangbare GraphQL-best practices, met een duidelijke scheiding tussen modellen, resolvers en services. Omdat we zelf nog twijfelen over de beste aanpak, zijn we benieuwd naar je overwegingen: documenteer kort waarom je bepaalde keuzes maakt en hoe je tot een structuur komt die volgens jou het meest begrijpelijk en toekomstbestendig is.

Kopieer vervolgens het bestand `.env.example`, vul je eigen database-URL in en voer de migraties uit met Alembic. Zodra dat gelukt is, kun je de Docker-container starten en via de GraphiQL-interface aan de slag gaan.

In de root van de codebase vind je een bestand genaamd `test_cases.graphql`, waarin twee queries en twee mutaties staan die de belangrijkste functionaliteit van de API vertegenwoordigen. Jouw doel is om deze vier operaties correct uit te voeren.

De codebase is niet volledig afgerond en met opzet gebroken; je zult merken dat er enkele functies ontbreken of nog aangevuld moeten worden. Ik ben benieuwd hoe je met de bestaande code omgaat, problemen oplost en ontbrekende onderdelen aanvult waar nodig.

Aan het einde van de opdracht lever je een heringerichte codebase op met een logische(re) mappenstructuur. De GraphQL API moet volledig werkend zijn, de database moet correct geïntegreerd zijn en alle testcases uit het `.graphql`-bestand moeten succesvol uitgevoerd en getoond kunnen worden. Voeg tot slot een korte toelichting toe waarin je beschrijft waarom je de nieuwe structuur op deze manier hebt opgezet, wat je hebt verbeterd en welke keuzes voor jou het verschil maakten in overzicht en onderhoudbaarheid.

Commit al je wijzigingen stapsgewijs met duidelijke beschrijvingen, zodat ik je denkproces goed kunnen volgen.