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