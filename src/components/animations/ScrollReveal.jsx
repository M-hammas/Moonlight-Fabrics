import React,{useEffect,useRef,useState} from "react";
export default function ScrollReveal({children,className=""}){
 const ref=useRef(null),[visible,setVisible]=useState(false);
 useEffect(()=>{const el=ref.current;if(!el)return;const io=new IntersectionObserver(([e])=>{if(e.isIntersecting){setVisible(true);io.disconnect()}},{threshold:.08});io.observe(el);return()=>io.disconnect()},[]);
 return <div ref={ref} className={`${className} ${visible?"is-visible":"reveal-hidden"}`}>{children}</div>;
}
