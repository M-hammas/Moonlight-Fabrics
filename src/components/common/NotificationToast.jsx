import React,{useEffect,useState} from "react";
export default function NotificationToast(){
 const [message,setMessage]=useState("");
 useEffect(()=>{const fn=e=>{setMessage(e.detail);clearTimeout(window.__lmToast);window.__lmToast=setTimeout(()=>setMessage(""),2800)};window.addEventListener("sidra-fabrics-toast",fn);return()=>window.removeEventListener("sidra-fabrics-toast",fn)},[]);
 return message?<div className="toast-global">✓ {message}</div>:null;
}
