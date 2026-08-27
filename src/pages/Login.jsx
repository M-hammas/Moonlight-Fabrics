
import React,{useState} from "react";
import {useAuth} from "../context/AuthContext";
import {useNavigate,Link} from "react-router-dom";
export default function Login(){const {login}=useAuth();const nav=useNavigate();const [email,setEmail]=useState("");const [password,setPassword]=useState("");const [error,setError]=useState("");
 return <section className="section"><div className="container auth-card"><h1 className="section-title">Sign in</h1><form onSubmit={async e=>{e.preventDefault();try{await login(email,password);nav("/")}catch(x){setError(x.message)}}} style={{display:"grid",gap:12,marginTop:30}}><input required type="email" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} style={{padding:14}}/><input required type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} style={{padding:14}}/>{error&&<p>{error}</p>}<button className="btn btn-primary">Sign in</button></form><p className="auth-switch">New here? <Link to="/register">Create an account</Link></p><div className="demo-login"><b>Admin demo</b><span>admin@sidra-fabrics.local</span><span>Admin@12345</span></div></div></section>}
