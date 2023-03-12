## Implementační dokumentace k 1. úloze do IPP 2022/2023
### Jméno a příjmení: Timotej Halenár
### Login: xhalen00

## Štruktúra programu
Pri implementácií som využil triedu DOMDocument. Hlavnú časť skriptu predstavuje `while` slučka, ktorá načítava vstup po riadkoch, a taktiež `switch`. Každá inštrukcia má vlastný `case`, no jednotlivé inštrukcie sú rozdelené do skupín podľa typov očakávaných argumentov. Pri každej skupine sa volá funkcia `line_to_xml()`, inkrementuje sa označovač poradia `$order` a kontroluje sa správnosť počtu a typov argumentov pre danú skupinu inštrukcií. Správnosť zápisu argumentu je kontrolovaná pri spracovávaní riadku vo funkcii `line_to_xml()`, a kontrola správnosti kombinácie argumentov pre danú inštrukciu je vykonávaná v hlavnom `switch`i (funkcia `line_to_xml()` nevie, akú inštrukciu práve spracuvávame).
## kontroly argumentov
### 1.
Najdôležitejšiu úlohu spĺňa funkcia `determine_arg_type()`, ktorá zisťuje typ argumentu, a taktiež kontroluje správnosť zápisu pomocou regulárnych výrazov. Táto funkcia vracia dvojprvkové pole `$type_value`, ktoré obsahuje na indexe 0 typ argumentu, a na indexe 1 samotný argument pripravený na vloženie do XML dokumentu (pri väčšine typov ide o časť argumentu za označovačom _@_, pri _label_ a _var_ je to celý argument). `determine_arg_type()` je volaný funkciou `line_to_xml()` pri spracovávaní riadka, ale aj ďalšími pomocnými funkciami pri kontrolách.
### 2.
Pri jednotlivých skupinách `case` prvkov sú volané funkcie `check_symb()`, `check_var()`, `check_type()` a `check_label()`. Ich úlohou je zistiť, či je pre danú inštrukciu použitá valídna kombinácia typov argumentov. Všetky okrem `check_type()` volajú `determine_arg_type()` a jej výstup porovnávajú s očakávaným typom argumentu pomocou funkcie `check_arg()`. Funkcia `check_type()` iba porovnáva svoj vstup s reťazcami _string_, _int_ a _bool_. V prípade nezhody očakávaného a skutočného typu argumentu je program ukončený s návratovým kódom 23. 
