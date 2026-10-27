import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    # TODO
    txt_sezione_aggiungi = ft.Text("Aggiungi Nuovo Strumento", size=20)

    input_tipo = ft.TextField(label="Tipo", width=200)
    input_marca = ft.TextField(label="Marca", width=200)
    input_anno = ft.TextField(label="Anno di acquisto", width=130)

    # Contatore per il valore in euro dello strumento (usiamo una lista per la mutabilità)
    valore_euro = [0.0]
    input_valore = ft.TextField(
        value=str(valore_euro[0]),
        label="Valore (€)",
        width=100,
        text_align=ft.TextAlign.RIGHT,
        read_only=True
    )
    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    # TODO
    def decrementa_valore(e):
        if valore_euro[0] >= 10.0:
            valore_euro[0] -= 10.0
        else:
            valore_euro[0] = 0.0
        input_valore.value = str(valore_euro[0])
        input_valore.update()

    def incrementa_valore(e):
        valore_euro[0] += 10.0
        input_valore.value = str(valore_euro[0])
        input_valore.update()

    def aggiungi_strumento_click(e):
        tipo = input_tipo.value.strip()
        marca = input_marca.value.strip()
        anno_str = input_anno.value.strip()
        valore_str = input_valore.value.strip()

        # Controllo campi vuoti
        if not tipo or not marca or not anno_str:
            alert.show_alert("Errore: Tutti i campi di testo devono essere compilati.")
            return

        # Validazione anno (intero)
        try:
            anno = int(anno_str)
        except ValueError:
            alert.show_alert("Errore: L'anno di acquisto deve essere un numero intero valido.")
            return

        # Validazione valore (float)
        try:
            valore = float(valore_str)
        except ValueError:
            alert.show_alert("Errore: Il valore dello strumento non è valido.")
            return

        # Inserimento nel deposito (richiama il metodo del Lab03)
        try:
            deposito.aggiungi_strumento(tipo, marca, anno, valore)
        except Exception as ex:
            alert.show_alert(f"Errore durante l'aggiunta: {str(ex)}")
            return

        # Svuota i campi e resetta il contatore
        input_tipo.value = ""
        input_marca.value = ""
        input_anno.value = ""
        valore_euro[0] = 0.0
        input_valore.value = "0.0"

        input_tipo.update()
        input_marca.update()
        input_anno.update()
        input_valore.update()

        # Aggiorna la vista della lista
        aggiorna_lista_strumenti()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    # TODO
    btn_meno = ft.IconButton(icon=ft.Icons.REMOVE, on_click=decrementa_valore)
    btn_piu = ft.IconButton(icon=ft.Icons.ADD, on_click=incrementa_valore)
    pulsante_aggiungi = ft.Button("Aggiungi strumento", on_click=aggiungi_strumento_click)

    row_contatore = ft.Row(
        [ft.Text("Valore (€):"), btn_meno, input_valore, btn_piu],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER)
    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),

        # Sezione 3
        # TODO
        txt_sezione_aggiungi,
        ft.Row(
            controls=[input_tipo, input_marca, input_anno],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        row_contatore,
        ft.Row(
            controls=[pulsante_aggiungi],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
