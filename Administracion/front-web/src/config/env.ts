const apiUrl = import.meta.env.VITE_API_URL;

if (!apiUrl) {
  throw new Error("Falta VITE_API_URL: el frontend se construyó sin la URL de su API");
}

export const API_URL: string = apiUrl;
