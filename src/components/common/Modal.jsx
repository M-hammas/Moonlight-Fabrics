import React,{useEffect} from "react";
export default function Modal({open,onClose,title,children}){
 useEffect(()=>{if(!open)return;const fn=e=>e.key==="Escape"&&onClose();window.addEventListener("keydown",fn);return()=>window.removeEventListener("keydown",fn)},[open,onClose]);
 if(!open)return null;
 return <div className="modal-backdrop" onMouseDown={e=>e.target===e.currentTarget&&onClose()}><div className="modal"><div className="modal-head"><h3>{title}</h3><button onClick={onClose}>×</button></div>{children}</div></div>
}
