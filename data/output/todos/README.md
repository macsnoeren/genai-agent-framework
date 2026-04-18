# Documentatie: Todo Output

Deze directory bevat de resultaten van de **Todo Agent**. Alle analyses en de geconsolideerde database worden nu direct in deze map opgeslagen voor een eenvoudiger beheer.

## Bestanden in deze map

- **`todo_master_list.jsonl`**: De centrale database waarin alle taken van alle bronnen worden samengevoegd.

## Beheer van taken

1.  **Inzien**: Gebruik de webinterface (bijvoorbeeld via de `index.html` in deze map of de centrale `web/` omgeving) om de takenlijst te bekijken.
2.  **Interactie**: Klik op items om ze af te vinken. Belangrijke taken kunnen als "Urgent" worden gemarkeerd om ze bovenaan de lijst te houden.
3.  **Opschoning**: Voltooide taken die ouder zijn dan 30 dagen worden automatisch gefilterd om de lijst actueel te houden.

## Belangrijke Opmerkingen
- **Geen Done-directory**: De configuratie is aangepast zodat bronbestanden niet langer automatisch naar een `done` map worden verplaatst. Beheer de invoerbestanden handmatig of pas de agent-instellingen aan indien archivering gewenst is.
- **Database Integriteit**: Wijzig `todo_master_list.jsonl` niet handmatig. Dit voorkomt fouten bij het inladen of opslaan via de webinterface.
- **Automatisering**: Bij het voltooien van alle taken word je getrakteerd op een confetti-feest! 🎉

---
*Onderdeel van het GenAI Agent Framework.*