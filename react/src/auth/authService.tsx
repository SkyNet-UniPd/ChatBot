/**
 * @returns ritorna l'api key salvata nel locale storage
 */
export function getApiKey(): string {
    return localStorage.getItem('api_key');
}

/**
 * Salva l'api key nel local storage
 * @param message 
 */
export function setApiKey(message: string): void {
    localStorage.setItem('api_key',message);
}

/**
 * viene eliminata l'api key dal local storage
 */
export function deleteApiKey(): void {
    localStorage.removeItem('api_key');
}

/**
 * 
 * @param message 
 * @returns l'API Key criptata usando l'algoritmo AES
 */
export function encrypt(message: string): string {
    const CryptoJS = require("crypto-js");
    let key = '2442264529482B4D';
    key = CryptoJS.enc.Utf8.parse(key);
    const encApiKey = CryptoJS.AES.encrypt(message, key, {mode: CryptoJS.mode.ECB});
    return encApiKey.toString();
}