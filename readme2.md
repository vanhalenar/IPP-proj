## Implementační dokumentace k 2. úloze do IPP 2022/2023
### Jméno a příjmení: Timotej Halenár
### Login: xhalen00

## Návrh
V skripte sa nachádzajú triedy Program, InstructionFactory, Instruction a zdedená trieda pre každú inštrukciu. 
### `class Instruction`
- Triedne atribúty:
- - `inst_counter`
- - `arg_num`
- - `order_numbers`  
- Inštančné atribúty:
- - `opcode`
- - `args`
- - `order` 

Trieda Instruction je základná trieda, z ktorej dedia všetky triedy pre inštrukcie. Nie je nikdy vytvorená inštancia tejto triedy, iba jej podtried (abstraktná trieda). Obsahuje zoznam argumentov `args`, v ktorom každý argument je slovník obsahujúci dva kľúče: `arg_type`  a `arg_value`. 
### `class InstructionFactory`
úlohou triedy `InstructionFactory` je tvorba inštancií tried inštrukcií podľa prečítaného operačného kódu. Obsahuje jedinu inštančnú metódu `create_instruction()`.
### `class Program` 
- Inštančné atribúty:
- - `instructions`
- - `frames_stack`
- - `global_frame`
- - `local_frame`
- - `temporary_frame`
- - `frames_stack`
- - `instruction_index`
- - `labels`
- - `call_stack`
- - `data_stack`  

Pri triede `Program` je využitý návrhový vzor Singleton - je vytvorená jediná inštancia tejto triedy, ktorá obsahuje zoznam všetkých inštancií tried inštrukcií, pamäťové rámce, návestia, dátový zásobník a zásobník volaní a metódy na prístup k nim.
## Beh programu
Pri spustení programu sú vykonané nasledujúce kroky:  
### 1. spracovanie vstupných argumentov
Vstupné argumenty sú spracované pomocou modulu `argparse`. `Source` a `Input` súbory sú priradené do premenných `sourcefile` a `inputfile`. V prípade, že jeden z nich chýba, je do danej premennej priradený `sys.stdin`. 
### 2. spracovanie XML
Na spracovanie XML súboru je využitý modul `xml.etree.ElementTree`, ktorý taktiež kontroluje, či je XML dobre formátovaný. Po zavolaní `ET.parse()` je výsledný strom prejdený dvakrát: raz kvôli kontrolám správnosti, druhýkrát sa vytvárajú inštrukcie.
### 3. tvorba inštrukcií
Inštrukcie sú vytvorené pomocou `InstructionFactory` a sú uložené do zoznamu `program.instructions`. Následne je zoznam zoradený a znovu prejdený, kedy sú sledované inštrukcie `LABEL` a ukladané do `program.labels` spoločne s ich poradím v zoradenom zozname. 
### 4. vykonávanie programu
Program je vykonávaný v cykle, ktorý iteruje cez všetky inštrukcie v `program.instructions`, pre každú volá metódy `check_arg_quantity()` a `execute()`. Kvôli skokovým inštrukciám nebolo možné použiť obyčajný `for i in program.instructions` cyklus a bolo potrebné zaviezť inštančnú premennú `program.instruction_index`. Ukončovacou podmienkou vykonávacieho cyklu je stav, kedy `program.instruction_index` je väčší alebo rovný počtu inštrukcií v zozname.
## Vykonávanie jednotlivých inštrukcií
Každá inštrukcia má vlastnú triedu, ktorá dedí z triedy `Instruction` a reimplementuje metódu `execute()`. Vo vačšine prípade je ako argument inštrukcie zadaný jeden alebo viac symbolov - premenná alebo konštanta. Trieda `Instruction` má metódu `retrieve_argument()`, ktorá vráti hodnotu premennej, v prípade že je argument premenná, alebo konštantu, ktorá už je obsiahnutá v argumente pri inštrukcii. Na získavanie premennej z pamäťového rámca sa používa metóda `get_variable()` triedy `Program`, a na ukladanie `save_to_variable()`.