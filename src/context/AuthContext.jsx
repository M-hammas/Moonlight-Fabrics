import React,{createContext,useContext,useEffect,useState} from "react";
import api from "../services/api";
const AuthContext=createContext(null);
const TOKEN="sidra-fabrics_access_token";
const USER="sidra-fabrics_user";

export function AuthProvider({children}){
  const [user,setUser]=useState(()=>{try{return JSON.parse(localStorage.getItem(USER))||null}catch{return null}});
  const [loading,setLoading]=useState(true);

  useEffect(()=>{
    let active=true;
    const token=localStorage.getItem(TOKEN);
    if(!token){setLoading(false);return ()=>{active=false};}
    api.get("/auth/me").then(me=>{
      if(active){setUser(me);localStorage.setItem(USER,JSON.stringify(me));}
    }).catch(()=>{
      localStorage.removeItem(TOKEN);localStorage.removeItem(USER);if(active)setUser(null);
    }).finally(()=>{if(active)setLoading(false)});
    return ()=>{active=false};
  },[]);

  useEffect(()=>{
    const expire=()=>{localStorage.removeItem(TOKEN);localStorage.removeItem(USER);setUser(null)};
    window.addEventListener("sidra-auth-expired",expire);
    return ()=>window.removeEventListener("sidra-auth-expired",expire);
  },[]);

  const login=async(email,password)=>{
    setLoading(true);
    try{
      const data=await api.post("/auth/login",{email,password});
      localStorage.setItem(TOKEN,data.access_token);localStorage.setItem(USER,JSON.stringify(data.user));setUser(data.user);return data;
    }finally{setLoading(false)}
  };
  const register=async(name,email,password)=>{
    const data=await api.post("/auth/register",{name,email,password});
    localStorage.setItem(TOKEN,data.access_token);localStorage.setItem(USER,JSON.stringify(data.user));setUser(data.user);return data;
  };
  const logout=()=>{localStorage.removeItem(TOKEN);localStorage.removeItem(USER);setUser(null)};
  const value={user,loading,login,register,logout,isAuthenticated:!!user,isAdmin:user?.role==="admin"};
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
export function useAuth(){const c=useContext(AuthContext);if(!c)throw new Error("useAuth must be inside AuthProvider");return c}
export default AuthContext;
