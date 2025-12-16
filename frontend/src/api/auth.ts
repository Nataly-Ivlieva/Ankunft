const BASE = import.meta.env.VITE_API_BASE_URL;

export async function apiSignup(email: string, password: string): Promise<{ token: string, role: string }> {
  const res = await fetch(BASE + "/auth/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.detail || "Fehler bei der Registrierung");
  }

  return res.json();
}

export async function apiLogin(email: string, password: string): Promise<{ token: string, role: string }> {
  const res = await fetch(BASE + "/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.detail || "Fehler beim Login");
  }

  return res.json();
}



