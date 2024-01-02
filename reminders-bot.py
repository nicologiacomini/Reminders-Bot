import telepot
from telepot.loop import MessageLoop
import time
import requests
import datetime
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

bot = telepot.Bot('')


idDaEliminareConfermato = -1

giorno = 0
mese = 0
data = 0
ora = 0
minuto = 0
promemoria = ""
idPromemoria = 0
giornoMax = 0
stringaMese = ''

listaEventi = []

start = False
letturaOra = False
letturaGiorno = False
letturaMese = False
inviato = False
erroreOra = False
testoAcaso = True
eliminazione = False
eliminazioneFallita = False
richiestaConferma = False
nonLeggereComandi = False
erroreGiorno = False
erroreMese = False

numeroMesi = {'1': 'Gennaio', '2': 'Febbraio', '3': 'Marzo', '4': 'Aprile', '5': 'Maggio', '6': 'Giugno',
        '7': 'Luglio', '8':'Agosto', '9':'Settembre', '10':'Ottobre', '11':'Novembre', '12':'Dicembre'}
mesiNumero = {'Gennaio': '1', 'Febbraio': '2', 'Marzo': '3', 'Aprile': '4', 'Maggio': '5', 'Giugno': '6',
        'Luglio':'7', 'Agosto':'8', 'Settembre':'9', 'Ottobre':'10', 'Novembre':'11', 'Dicembre':'12'}
mesiGiorni = {'Gennaio':31, 'Febbraio':28, 'Marzo':31, 'Aprile':30, 'Maggio':31, 'Giugno':30,
        'Luglio':31, 'Agosto':31, 'Settembre':30, 'Ottobre':31, 'Novembre':30, 'Dicembre':31, 'Febbraio2':29}


class Evento:
    idPromemoria = 0
    promemoria = ""
    data = ""
    ora = ""
    minuto = ""
    utente = 0

    def __init__(self, idPromemoria, promemoria, data, ora, minuto, utente):
        self.idPromemoria = idPromemoria
        self.promemoria = promemoria
        self.data = data
        self.ora = ora
        self.minuto = minuto
        self.utente = utente

    def setPromemoria(self, testoPromemoria):
        self.promemoria = testoPromemoria

    def setOra(self, ora):
        self.ora = ora

    def setMinuto(self, minuto):
        self.minuto = minuto

    def setUtente(self, idUtente):
        self.utente = idUtente

    def setIdPromemoria(self, idPromemoria):
        self.idPromemoria = idPromemoria


def salvaPromemoria(testoPromemoria):
    if testoPromemoria != '':
        return testoPromemoria
    else:
        return None

def salvaOrario(testoOrario):
    if not testoOrario.find(':')==-1:
        orario = testoOrario.split(':',1)
        return orario
    elif not testoOrario.find('.')==-1:
        orario = testoOrario.split('.',1)
        return orario
    else:
        return None


def generaTastieraMesi():
    conta = 1
    keyboard = []
    riga = []
    for i in range(4):
        for j in range(3):
            riga.insert(j, KeyboardButton(text=str(numeroMesi[str(conta)])))
            conta+=1
        keyboard.insert(i, riga)
        riga = []
    return keyboard


def generaTastieraGiorni(mese):
    if mese == 'Febbraio':
        meseAttuale = datetime.date.today().month
        annoAttuale = datetime.date.today().year
        if 1 <= meseAttuale <= 2:
            if (annoAttuale%4) == 0:
                mese = 'Febbraio2'
        elif 3 <= meseAttuale <= 12:
            if ((annoAttuale+1)%4) == 0:
                mese = 'Febbraio2'
    conta = 1
    fine = False
    keyboard = []
    riga = []
    for i in range(4):
        for j in range(8):
            riga.insert(j,KeyboardButton(text=conta))
            conta+=1
            if conta > int(mesiGiorni[mese]):
                fine = True
                break
        keyboard.insert(i,riga)
        riga = []
        if fine:
            break
    return keyboard


def salvaData(testoData):
    stringa = ''
    giorno = testoData[:2]
    if 0 < int(giorno) < 10:
        giornoDaSalvare = '0'+str(giorno[0])
        mese = testoData[2:]
    else:
        giornoDaSalvare = str(giorno)
        mese = testoData[3:]
    meseDaSalvare = mesiNumero[str(mese)]
    if str(mese) in mesiNumero:
        if 0 < int(giorno) <= 31:
            stringa = str(giornoDaSalvare)+'-'+str(meseDaSalvare)
    return stringa


def dimmiData(numero):
    giorno = datetime.date.today().day
    giorno += numero
    stringaMese = numeroMesi[str(datetime.date.today().month)]
    stringa = str(giorno)+' '+stringaMese
    return stringa


def riassegnaId(idUtente):
    j = 1
    for i in range(len(listaEventi)):
        if listaEventi[i].utente == idUtente:
            listaEventi[i].idPromemoria = j
            j += 1

# def getOra(testoOrario):
#     orario = salvaOrario(testoOrario)
#     return orario[0]
#
#
# def getMinuto(testoOrario):
#     orario = salvaOrario(testoOrario)
#     return orario[1]


def verificaFormato(testo):
    for i in range(len(testo)):
        if testo[i] == ':':
            return True
    return False

def stampaLista():
    for i in range(len(listaEventi)):
        print('\nPromemoria '+str(listaEventi[i].idPromemoria))
        print('\tTesto: '+listaEventi[i].promemoria)
        print('\tData: '+listaEventi[i].data)
        print('\tOra: '+str(listaEventi[i].ora))
        print('\tMinuto: '+str(listaEventi[i].minuto))
        print('\tUtente: '+str(listaEventi[i].utente))

def trovaIndice(id):
    for i in range(len(listaEventi)):
        if listaEventi[i].idPromemoria == id:
            return i


#metodi per l'invio della notifica
def get_payload(messaggio, chat_id):
    payload = {'chat_id': chat_id, 'text': messaggio, 'parse_mode': 'HTML'}
    return payload

def notify(txt_notify, userId):
    payload = get_payload(txt_notify, userId)
    requests.post(
        "https://api.telegram.org/bot1037333347:AAGBlv___nlbKiR32yb5uJXY0SiW8z7Gsrc/sendMessage".format(token=bot),
        data=payload)
#fine metodi per l'invio della notifica


def controllaMessaggio(testo):
    if not testo == "":
        return True
    return False

def inviaLista(idUtente):
    messaggio = ''
    for i in range(len(listaEventi)):
        if listaEventi[i].utente == idUtente:
            messaggio += '/'
            messaggio += str(listaEventi[i].idPromemoria) + '    '
            messaggio += str(listaEventi[i].promemoria) + '    '
            messaggio += str(listaEventi[i].data) + '    '
            messaggio += 'ore: '+ str(listaEventi[i].ora) + ':' + str(listaEventi[i].minuto) + '    \n'
    return messaggio

def eliminaIndice(idDaEliminare, idUtente):
    num = trovaIndice(idDaEliminare)
    del listaEventi[num]
    riassegnaId(idUtente)

def corrispondenzaData(data):
    giorno = data[0:2]
    mese = data[3:]
    if int(giorno) == datetime.date.today().day:
        if int(mese) == datetime.date.today().month:
            return True
    return False

def eventiDaInviare(lista):
    now = datetime.datetime.now()
    stringaOra = str(now.time())
    oraAttuale = stringaOra.split(':')
    for i in lista:
        promemoriaSalvato = i.promemoria
        oraSalvata = i.ora
        dataSalvata = i.data
        minutoSalvato = i.minuto
        userSalvato = i.utente
        if corrispondenzaData(dataSalvata):
            if str(oraSalvata) == oraAttuale[0]:
                if str(minutoSalvato) == oraAttuale[1]:
                    notify('AVVISO: '+promemoriaSalvato, userSalvato)
                    print('Il messaggio è stato inviato\tuser='+str(userSalvato))
                    eliminaIndice(i.idPromemoria, userSalvato)


def on_chat_message(msg):
    global start, letturaOra, data, ora, giorno, mese, minuto, promemoria, usersId, listaEventi, \
        idPromemoria, erroreOra, testoAcaso, eliminazione, \
        idDaEliminareConfermato, richiestaConferma, eliminazioneFallita, nonLeggereComandi,\
        letturaData, erroreGiorno, letturaGiorno, letturaMese, erroreMese, erroreGiorno, giornoMax, stringaMese

    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        # EVENTUALE OPERAZIONE: 2 - chiede la conferma dell'eliminazione o l'annullamento dell'operazione
        if richiestaConferma:
            if msg['text'] == 'Si' or msg['text'] == 'SI' or msg['text'] == 'si':
                bot.sendMessage(chat_id, 'Ok, operazione confermata, il promemoria è stato eliminato')
                eliminaIndice(idDaEliminareConfermato, chat_id)
                eliminazione = False
                richiestaConferma = False
                testoAcaso = True
                nonLeggereComandi = False
            elif msg['text'] == 'No' or msg['text'] == 'NO' or msg['text'] == 'no':
                bot.sendMessage(chat_id, 'Ok, operazione annullata')
                idDaEliminareConfermato = -1
                eliminazione = False
                richiestaConferma = False
                nonLeggereComandi = False
                testoAcaso = True
            else:
                bot.sendMessage(chat_id, 'Mi dispiace, il messaggio inserito non è valido.'
                                         'Rispondi con Si oppure No')
                eliminazione = False
                nonLeggereComandi = True
                richiestaConferma = True

        # EVENTUALE OPERAZIONE: 3- richiede l'invio del numero del promemoria da eliminare
        if eliminazione:
            idDaEliminare = msg['text']
            print('id da eliminare \n\n'+idDaEliminare+'\n')
            print('\n'+idDaEliminare[0])
            if idDaEliminare[0] == '/':
                idDaEliminare = idDaEliminare.split('/')
                print('formato id da eliminare\n\n')
                print(str(idDaEliminare))
                print('\n\n')
                print(idDaEliminare[1])
                if idDaEliminare[1].isnumeric():
                    if int(idDaEliminare[1]) <= len(listaEventi):
                        bot.sendMessage(chat_id, 'Sei sicuro di voler eliminare il promemoria numero '+idDaEliminare[1]+'?')
                        idDaEliminareConfermato = int(idDaEliminare[1])
                        riassegnaId(chat_id)
                        nonLeggereComandi = True
                        richiestaConferma = True
                        eliminazione = False
                    else:
                        bot.sendMessage(chat_id, 'Mi dispiace, il promemoria che vuoi eliminare non esiste')
                        eliminazione = False
                        nonLeggereComandi = False
                else:
                    bot.sendMessage(chat_id, 'Mi dispiace, il messaggio inviato non è nel formato adatto.'
                                             'Inserisci \"/\" prima del numero del promemoria')
                    eliminazione = True
                    nonLeggereComandi = True
            else:
                bot.sendMessage(chat_id, 'Mi dispiace, il messaggio inviato non è nel formato adatto.'
                                         'Inserisci \"/\" prima del numero del promemoria')
                eliminazione = True
                nonLeggereComandi = True

#-----------------------------------------------------------------------------------------------------------------------

        # OPERAZIONE PRINCIPALE: 4 - chiede di inviare l'orario a cui essere notificato
        if letturaOra:
            testoAcaso = False
            erroreOra = False
            orario = salvaOrario(msg['text'])
            print(orario)

            try: ora = orario[0]
            except IndexError: erroreOra = True

            numOra = -1
            if ora.isnumeric():
                print('\n\nORA APPENA LETTO: ' + str(ora))
                numOra = int(ora)
            else:
                erroreOra = True

            if 0 <= numOra <= 23 and not erroreOra:
                try: minuto = orario[1]
                except IndexError or AttributeError: erroreOra = True

                numMin = -1
                if minuto.isnumeric():
                    print('\n\nMINUTO APPENA LETTO: ' + str(minuto))
                    numMin = int(minuto)
                else:
                    erroreOra = True

                if 0 <= numMin <= 59 and not erroreOra:
                    erroreOra = False
                    idPromemoria += 1
                    letturaOra = False
                    evento = Evento(idPromemoria, promemoria, data, ora, minuto, chat_id)
                    bot.sendMessage(chat_id, 'Perfetto il promemoria è stato salvato\n'
                                             'L\'evento '+str(evento.promemoria)+' verrà notificato il giorno '+str(evento.data)+' alle ore '+ str(evento.ora)+':'+str(evento.minuto))
                    print('evento = ' + str(evento.promemoria) + '\ndata = ' + str(evento.data) + '\nora = ' + str(evento.ora) +
                          '\nminuto = ' + str(evento.minuto) + '\nuser =' + str(evento.utente))
                    listaEventi.append(evento)
                    stampaLista()
                    testoAcaso = True
                    nonLeggereComandi=  False
                else:
                    erroreOra = True
            else:
                erroreOra = True

        # OPERAZIONE PRINCIPALE: 4.1 - gestisce l'errore nella
        if erroreOra:
            testoAcaso = False
            bot.sendMessage(chat_id, 'Formato orario non corretto...\nPer favore inserisci l\'ora in questo formato hh:mm')
            erroreOra = False
            nonLeggereComandi = True
            letturaOra = True

        # OPERAZIONE PRINCIPALE: 3 - chiedi di inviare il giorno della notifica
        if letturaGiorno:
            testoAcaso = False
            stringaGiorno = msg['text']
            print('data ricevuta: '+stringaGiorno)
            giornoDaSalvare = 0
            try:
                giornoDaSalvare = int(stringaGiorno)
            except ValueError:
                erroreGiorno = True

            if not erroreGiorno:
                if 1 <= giornoDaSalvare <= int(giornoMax):
                    erroreGiorno = False
                    letturaGiorno = False
                    letturaOra = True
                    if 0 < giornoDaSalvare < 10:
                        giorno = '0' + str(giornoDaSalvare)

                    else:
                        giorno = str(giornoDaSalvare)
                    data = giorno+ '-' + str(mese)
                    print('La data salvata è: '+data)
                    bot.sendMessage(chat_id, 'Bene, a che ora vuoi essere notificato? (hh:mm)')
                else:
                    erroreGiorno = True

        # OPERAZIONE PRINCIPALE: 3.1 - gestisce l'errore nell'invio del giorno
        if erroreGiorno:
            testoAcaso = False
            erroreGiorno = False
            nonLeggereComandi = True
            letturaGiorno = True
            bot.sendMessage(chat_id, 'Formato data non corretto...\nPer favore inserisci premi uno dei pulsanti', reply_markup=ReplyKeyboardMarkup(
                keyboard = generaTastieraGiorni(stringaMese)
            ))

        # OPERAZIONE PRINCIPALE: 2 - chiedi di inviare il mese della notifica
        if letturaMese:
            testoAcaso = False
            stringaMese = msg['text']
            print('data ricevuta: '+stringaMese)
            try:
                meseDaSalvare = mesiNumero[stringaMese]
                giornoMax = mesiGiorni[stringaMese]
                print('data salvata: ' + meseDaSalvare)
                mese = int(meseDaSalvare)
                bot.sendMessage(chat_id, 'Bene, scegli il giorno del mese di ' + str(
                    stringaMese) + ' in cui vuoi essere notificato', reply_markup=ReplyKeyboardMarkup(
                    keyboard=generaTastieraGiorni(stringaMese)
                ))
                erroreMese = False
                letturaMese = False
                letturaGiorno = True
            except KeyError:
                erroreMese = True

        # OPERAZIONE PRINCIPALE: 2.1 - gestisce l'errore nell'invio del mese
        if erroreMese:
            testoAcaso = False
            erroreMese = False
            nonLeggereComandi = True
            letturaMese = True
            bot.sendMessage(chat_id, 'Formato data non corretto...\nPer favore, premi uno dei pulsanti', reply_markup=ReplyKeyboardMarkup(
                keyboard = generaTastieraMesi()
            ))

        # OPERAZIONE PRINCIPALE: 1 - chiedi il giorno della notifica
        if start:
            # variabili di controllo settate nuovamente
            testoAcaso = False
            letturaMese = True
            start = False
            nonLeggereComandi = True
            promemoria = salvaPromemoria(msg['text'])
            print('Promemoria: '+promemoria)
            bot.sendMessage(chat_id, 'Bene, scegli il mese della data in cui essere notificato', reply_markup=ReplyKeyboardMarkup(
                keyboard = generaTastieraMesi()
            ))

#-----------------------------------------------------------------------------------------------------------------------

        # OPERAZIONE INIZIALE: 0 - saluta e chiedi il cosa ricordare
        if msg['text'] == '/start' or msg['text'] == '/new' and not nonLeggereComandi:
            if msg['text'] == '/start':
                testoAcaso = True
                bot.sendMessage(chat_id, 'Ciao! Questo è un bot che permette di notificare i tuoi promemoria')
            else:
                testoAcaso = False
                start = True
                nonLeggereComandi = True
                bot.sendMessage(chat_id, 'Cosa vuoi ricordare?')
                print('ID da rispondere: '+str(chat_id))

        # EVENTUALE OPERAZIONE: 1 - mostra la lista dei promemoria e se richiesto richiede quale promemoria eliminare
        if msg['text'] == '/show' or msg['text'] == '/delete' and not nonLeggereComandi:
            messaggio = inviaLista(chat_id)
            if len(messaggio) == 0:
                bot.sendMessage(chat_id, 'Non sono presenti promemoria')
            else:
                if msg['text'] == '/show':
                    bot.sendMessage(chat_id, 'I tuoi promemoria:\n\n'+messaggio)
                else:
                    bot.sendMessage(chat_id, 'Scegli il promemoria da eliminare:\n\n' + messaggio)
                    eliminazione = True
                    testoAcaso = False

        # ALTRA OPERAZIONE - abilita soltanto una variabile testoAcaso, in modo che venga mostrato il menu
        if msg['text'] == '/help' and not nonLeggereComandi:
            testoAcaso = True

        # ALTRA OPERAZIONE - invia un messaggio contenente la lista delle operazioni che sono eseguibili
        if testoAcaso:
            bot.sendMessage(chat_id, 'Per eseguire delle operazioni utilizza i comandi seguenti:\n\n'
                                     '/new - Crea nuovo promemoria\n'
                                     '/show - Mostra la lista dei promemoria\n'
                                     '/delete - Elimina un comando')


# crea un nuovo thread per ogni richiesta, quindi ogni utente ha il proprio thread
MessageLoop(bot, on_chat_message).run_as_thread()


while 1:
    time.sleep(10)
    eventiDaInviare(listaEventi)

# Modificare l'interazione con l'utente e renderla più intuitiva
# Gestire in modo migliore la numerazione per utente
# IMPORTANTE verificare che le variabili di controllo siano corrette per ogni stato
