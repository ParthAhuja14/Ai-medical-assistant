import api from "./api";

export const authService = {
  register: (data) => api.post("/auth/register", data),
  login: (email, password) => {
    const form = new URLSearchParams();
    form.append("username", email);
    form.append("password", password);
    return api.post("/auth/login", form, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
  },
  me: () => api.get("/auth/me"),
};

export const diagnosisService = {
  listSymptoms: () => api.get("/diagnosis/symptoms"),
  submit: (payload) => api.post("/diagnosis/", payload),
  history: () => api.get("/diagnosis/history"),
  nearbySpecialists: (sessionId) => api.get(`/diagnosis/${sessionId}/specialists`),
};
