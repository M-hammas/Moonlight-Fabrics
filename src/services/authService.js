import api from "./api";
export const authService={
 register:(payload)=>api.post("/auth/register",payload),
 login:(payload)=>api.post("/auth/login",payload),
 me:()=>api.get("/auth/me"),
 forgotPassword:(email)=>api.post("/auth/forgot-password",{email}),
 resetPassword:(payload)=>api.post("/auth/reset-password",payload)
};
