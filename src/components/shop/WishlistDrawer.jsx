import React from "react";
import {Link} from "react-router-dom";
import {useWishlist} from "../../context/WishlistContext";
import {useCart} from "../../context/CartContext";
export default function WishlistDrawer({open,onClose}){
 const {items,removeFromWishlist}=useWishlist();const {addToCart}=useCart();
 return <aside className={`drawer ${open?"open":""}`}><div className="drawer-head"><h3>Wishlist</h3><button onClick={onClose}>×</button></div><div className="drawer-body">{!items.length?<p className="muted">Your wishlist is empty.</p>:items.map(p=><div className="drawer-item" key={p.id}><img src={p.image} alt=""/><div><Link to={`/product/${p.id}`} onClick={onClose}><b>{p.name}</b></Link><p>PKR {Number(p.sale_price??p.price).toLocaleString()}</p><button className="link-btn" onClick={()=>{addToCart({...p,salePrice:p.sale_price});removeFromWishlist(p.id)}}>Move to bag</button></div></div>)}</div></aside>
}
