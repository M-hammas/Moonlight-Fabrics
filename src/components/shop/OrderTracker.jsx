import React from "react";
const statuses=["pending","confirmed","processing","shipped","delivered"];
export default function OrderTracker({status="pending"}){
 const active=statuses.indexOf(status);
 return <div className="order-tracker">{statuses.map((s,i)=><div className={`track-step ${i<=active?"done":""}`} key={s}><span>{i<=active?"✓":i+1}</span><b>{s}</b></div>)}</div>
}
