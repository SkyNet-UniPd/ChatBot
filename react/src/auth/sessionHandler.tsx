import { deleteApiKey, setApiKey, encrypt } from "./authService";

/* Variabili inutilizzate
let isLoginProcedure = false;
let isLogoutProcedure = false;
const loginMessages: string[] = ['login', 'accesso', 'autenticazione', 'autenticato'];
const abortMessages: string[] = ['chiudi', 'annulla', 'stop', 'fine'];
const logoutMessages: string[] = ['logout', 'log-out', 'esci', 'exit', 'uscire'];
const yesWords: string[] = ["sì", "si", "ok", "yes", "s", "y", "vai"]
*/
const errors: string[] = ['400', '401', '402', '403', '500'];

const loginSuccess = "Login effettuato correttamente!"
const logoutSuccess = "Logout eseguito correttamente!"

/**
 * 
 * @param message 
 * @param wordList 
 * @returns ritorna true sse il messaggio contiene una delle parole della lista, false altrimenti
 */
function matchMessage(message: string, wordList: string[]): boolean {
  let isMatch:boolean = false;
  if(wordList.some(el=> message.includes(el))) {
    isMatch = true;
  }
  return isMatch;
}

/**
 * Controlla che non venga ritornato un errore, in tal caso cancella l'api key dal local storage
 * @param message 
 */
export function sessionErrorHandler(message: string): void {
  const errorMatched = matchMessage(message, errors);
  if(errorMatched) {
    deleteApiKey();
    // isLoginProcedure = false;
  }
}


/**
 * Test nuova funzione che gestisce il login e il logout
 */

 export function handleSession(reply: string, message: string) {
  try{
   if (reply.includes(loginSuccess)){
     const enc_apy_key = encrypt(message);
     setApiKey(enc_apy_key);
   }else if(reply.includes(logoutSuccess)){
     deleteApiKey();
   }
  } catch (error) {
     console.log(error);
     return null;
   }
}

/*
 * Vecchia funzione che gestisce il login e il logout

 export function handleSessionOld(message: string) {
    try {
      const abortMatched = matchMessage(message, abortMessages);
      const API_KEY = getApiKey();
      if(abortMatched) { // viene annullata l'operazione quindi
        isLoginProcedure = false;
        isLogoutProcedure = false;
        return null;
      }
      const loginMatched = matchMessage(message, loginMessages);
      if(loginMatched && !API_KEY) { // viene iniziata la procedura di login
        isLoginProcedure = true;
        return null;
      }
      if(isLoginProcedure) { // viene fatto il login e salvata l'api key nel local storage
        setApiKey(message);
        isLoginProcedure = false;
      }
      const logoutMatched = matchMessage(message, logoutMessages);
      if(logoutMatched) { // viene iniziata la procedura di logout
        isLogoutProcedure = true;
      }
      const yesMatched = matchMessage(message, yesWords);
      if(isLogoutProcedure && yesMatched) { // viene fatto il logout ed eliminata l'api key dal local storage
        deletApiKey();
        isLogoutProcedure = false;
      }
      return API_KEY;
    } catch (error) {
      console.log(error);
      return null;
    }
} */
