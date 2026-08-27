
import React from "react";
import { Link } from "react-router-dom";
import { useCart } from "../context/CartContext";
export default function Cart(){
 const {items,updateQuantity,removeFromCart,subtotal}=useCart();
 return <section className="section"><div className="container">
  <h1 className="section-title">Your Bag</h1>
  {!items.length ? <p className="muted">Your bag is empty. Add products from your storefront.</p> :
  <div style={{display:"grid",gap:16,maxWidth:900}}>
   {items.map(i=><div key={i.id} style={{display:"grid",gridTemplateColumns:"80px 1fr auto",gap:16,alignItems:"center",padding:"16px 0",borderBottom:"1px solid #eee"}}>
    <img src={i.image} alt="" style={{width:80,height:90,objectFit:"cover",background:"#f5f5f5"}}/>
    <div><b>{i.name}</b><div className="muted">PKR {Number(i.salePrice??i.price).toLocaleString()}</div></div>
    <div><input type="number" min="1" value={i.quantity} onChange={e=>updateQuantity(i.id,Number(e.target.value))} style={{width:65,padding:8}}/><button className="btn btn-secondary" onClick={()=>removeFromCart(i.id)}>Remove</button></div>
   </div>)}
   <h2>Subtotal: PKR {subtotal.toLocaleString()}</h2><Link className="btn btn-primary" to="/checkout">Continue to checkout</Link>
  </div>}
 </div></section>
}
